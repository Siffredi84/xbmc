"""
Arquitectura tri-fonte.

    FINVIZ   -> largura      : produz o universo. NUNCA valida.
    IBKR     -> profundidade : identidade autoritativa, liquidez, execucao, opcoes.
    YAHOO    -> arbitro      : so e consultado quando as duas primeiras divergem.

Regra estrutural: nenhuma fonte pode ocupar dois papeis. O papel de arbitro so
tem valor enquanto for independente, por isso o Yahoo nao entra no caminho
normal — se entrasse em todas as linhas deixaria de ser um desempate e passaria
a ser um segundo validador correlacionado com o primeiro.

Limitacao conhecida do ambiente: as ferramentas IBKR sao MCP, invocaveis na
conversa e nao a partir deste processo. A camada IBKR e por isso um ADAPTADOR:
o codigo define o contrato, os dados sao injectados via `load_ibkr(path)`.
Em producao local, substituir por chamadas a ib_insync/TWS Gateway mantendo a
mesma assinatura.
"""
import difflib, json, os, re, time
import pandas as pd
import requests

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")
import config
US_EXCH_YAHOO = config.EXCH_YAHOO
US_EXCH_IBKR = config.EXCH_IBKR
_STOP = re.compile(r"\b(inc|corp|corporation|co|ltd|limited|plc|nv|sa|ag|holdings?|group|the|"
                   r"company|technologies|technology|pharmaceuticals?|therapeutics?|"
                   r"sciences?|labs?|laboratories|fund|trust|incorporated)\b")
# Descritores de classe de titulo: o Polygon inclui-os no nome, a IBKR nao.
# Sem os remover, 'Byrna Technologies, Inc. Common Stock' vs 'BYRNA TECHNOLOGIES INC'
# dava 0.43 e reprovava no gate — falso negativo puro.
_CLASSE = re.compile(
    r"\b(common|ordinary|preferred|subordinate|voting|restricted)?\s*"
    r"(stock|shares?|share|units?|adr|ads|american depositary (?:share|receipt)s?)\b"
    r"|\bclass [a-z]\b|\bseries \d+\b|\bpar value\b|\bcdi\b|\bnew\b")

# Limiares da camada de execucao. Explicitos para serem discutiveis, nao magicos.
MAX_SPREAD_PCT = config.SPREAD_MAX_PCT
MIN_USD_VOL_90D = config.USD_VOL_90D_MIN


class IdentityError(RuntimeError):
    """Fail-closed: identidade nao confirmada. O pipeline para."""


class SchemaError(RuntimeError):
    """O dataframe nao cumpre o contrato entre etapas."""


# Contrato entre etapas: toda a saida de um funil traz estas colunas.
COLUNAS = ("Ticker", "Nome")
_ALIAS_NOME = ("Nome", "FinvizCompany", "Company", "name")


def normaliza(df):
    """Aceita a saida de qualquer funil e devolve-a no schema canonico.
    Falha alto se nao houver coluna de nome — comparar contra string vazia
    produzia 'nome diverge (0.00)' em todas as linhas e abortava o pipeline
    por um defeito de integracao disfarcado de falha de identidade."""
    df = df.copy()
    if "Ticker" not in df.columns:
        raise SchemaError("falta a coluna Ticker")
    for a in _ALIAS_NOME:
        if a in df.columns and df[a].notna().any():
            if a != "Nome":
                df["Nome"] = df[a]
            break
    else:
        raise SchemaError(
            f"nenhuma coluna de nome encontrada; esperava uma de {_ALIAS_NOME}")
    vazios = df["Nome"].isna() | (df["Nome"].astype(str).str.strip() == "")
    if vazios.any():
        raise SchemaError(f"nome em falta para {list(df.loc[vazios, 'Ticker'])}")
    return df


def _norm(s):
    s = re.sub(r"[^a-z0-9 ]", " ", str(s).lower())
    s = _CLASSE.sub(" ", s)
    return re.sub(r"\s+", " ", _STOP.sub(" ", s)).strip()


def name_match(a, b):
    return difflib.SequenceMatcher(None, _norm(a), _norm(b)).ratio()


# ---------------------------------------------------------------- IBKR (depth)
def load_ibkr(path="ibkr_depth.json"):
    """Adaptador. Espera {ticker: {description, exchange, conid, last, bid, ask,
    usd_vol_90d, call_vol, put_vol, iv_pct_52w, hist_vol_annual}}."""
    if not os.path.exists(path):
        return {}
    with open(path) as f:
        return json.load(f)


def ibkr_check(ticker, nome, depth):
    """Tres estados, nao dois. Ticker e exchange a bater com nome divergente nao
    e uma falha de identidade — e uma etiqueta a mudar, um rebrand ou um nome
    desactualizado numa das fontes. Reprovar seria decidir sobre dados ambiguos;
    aprovar seria ignora-los. Vai para REVER."""
    d = depth.get(ticker)
    if d is None:
        return None, "sem cobertura IBKR"
    if d.get("exchange") not in US_EXCH_IBKR:
        return "FAIL", f"exchange fora do universo: {d.get('exchange')}"
    sim = name_match(nome, d.get("description", ""))
    if sim < config.NOME_SIMILARIDADE_MIN:
        return "REVER", f"nome diverge ({sim:.2f}): funil '{nome}' vs IBKR '{d.get('description')}'"
    return "OK", f"{d['description']} @ {d['exchange']}"


def execution_profile(ticker, depth):
    """Nao valida identidade — mede se o candidato e negociavel na pratica."""
    d = depth.get(ticker)
    if not d:
        return {}
    bid, ask = d.get("bid"), d.get("ask")
    spread = round((ask - bid) / ((ask + bid) / 2) * 100, 2) if bid and ask else None
    cv, pv = d.get("call_vol") or 0, d.get("put_vol") or 0
    return {"spread_pct": spread,
            "usd_vol_90d": d.get("usd_vol_90d"),
            "call_put_ratio": round(cv / pv, 1) if pv else (cv if cv else None),
            "iv_pct_52w": d.get("iv_pct_52w"),
            "hist_vol_annual": d.get("hist_vol_annual"),
            "liquido": (d.get("usd_vol_90d") or 0) >= MIN_USD_VOL_90D}


# ------------------------------------------------------------- YAHOO (arbitro)
def yahoo_identity(ticker, session=None, retries=3):
    s = session or requests.Session()
    s.headers.update({"User-Agent": UA})
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?range=1d&interval=1d"
    for _ in range(retries):
        try:
            m = s.get(url, timeout=25).json()["chart"]["result"][0]["meta"]
            return {"ticker": m.get("symbol"),
                    "name": m.get("longName") or m.get("shortName"),
                    "exchange": m.get("exchangeName"),
                    "price": m.get("regularMarketPrice")}
        except Exception:
            time.sleep(2)
    return None


def yahoo_check(ticker, finviz_company, session=None):
    ref = yahoo_identity(ticker, session)
    if ref is None:
        return None, "sem resposta do arbitro"
    if (ref["ticker"] or "").upper() != ticker.upper():
        return False, f"ticker diverge: {ref['ticker']}"
    sim = name_match(finviz_company, ref["name"])
    if sim < config.NOME_SIMILARIDADE_MIN:
        return False, f"nome diverge ({sim:.2f}): '{ref['name']}'"
    if ref["exchange"] not in US_EXCH_YAHOO:
        return False, f"exchange nao-US: {ref['exchange']}"
    return True, f"{ref['name']} @ {ref['exchange']}"


# ------------------------------------------------------------------- pipeline
def cobertura(df, depth):
    """Tickers do funil corrente ausentes do adaptador IBKR."""
    return [t for t in normaliza(df)["Ticker"] if t not in depth]


def resolve(df, depth, verbose=True):
    """IBKR decide. O Yahoo so e chamado quando a IBKR falha ou nao cobre."""
    s = requests.Session()
    out = []
    df = normaliza(df)
    for _, r in df.iterrows():
        t, comp = r["Ticker"], r["Nome"]
        est, det = ibkr_check(t, comp, depth)
        arbitro = ""
        if est is None:                      # sem cobertura: o arbitro decide
            y_ok, y_det = yahoo_check(t, comp, s)
            arbitro = f" | arbitro: {'OK' if y_ok else 'FAIL'} {y_det}"
            est = "OK" if y_ok else "FAIL"
            time.sleep(0.3)
        elif est == "REVER":                 # arbitro informa, nao absolve
            y_ok, y_det = yahoo_check(t, comp, s)
            arbitro = (f" | arbitro {'concorda com o funil' if y_ok else 'tambem diverge'}"
                       f": {y_det}")
            time.sleep(0.3)
        rec = {"Ticker": t, "estado": est, "identidade_ok": est == "OK",
               "fonte": det + arbitro}
        rec.update(execution_profile(t, depth))
        out.append(rec)
        if verbose:
            print(f"  {est:5s} {t:6s} {rec['fonte']}")
    res = pd.DataFrame(out)
    falhas = res[res.estado == "FAIL"]
    if len(falhas):
        raise IdentityError(f"GATE FAIL-CLOSED: {list(falhas.Ticker)}")
    rever = res[res.estado == "REVER"]
    if len(rever) and verbose:
        print(f"  -> {len(rever)} para revisao manual: {list(rever.Ticker)}")
    return res
