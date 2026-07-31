"""EDGAR: red flags e catalisadores directamente da fonte.

Fecha dois buracos com uma so fonte. Os red flags obrigatorios do documento de
criterios (going concern, aviso de delisting, reverse split) vivem nos 10-Q/10-K
e nos itens dos 8-K. E o 8-K e tambem onde estao os catalisadores que nem o
Marketaux nem o Finnhub cobrem — em micro-caps, o 8-K costuma SER a noticia.

Gratuito, sem chave, 10 pedidos/segundo. O 20-F entra pelo mesmo caminho, o que
desbloqueia a fila de emissores estrangeiros.
"""
import json, os, random, re, time
import requests

UA = {"User-Agent": os.environ.get("SEC_UA", "screening-research contacto@exemplo.pt")}
CACHE = "edgar_cache"
PACE = 0.4   # abaixo do limite da SEC (10/s), mas em rajada ela estrangula
TENTATIVAS = 8
BACKOFF_MAX_S = 60
JITTER = 0.25
_S = requests.Session()
_S.headers.update(UA)

# Itens de 8-K que importam. O 3.01 e o aviso de delisting — e um codigo, nao
# uma palavra a procurar num texto: deteccao exacta, sem falsos positivos.
ITENS = {
    "1.01": "acordo material", "1.02": "fim de acordo material",
    "1.03": "falencia ou insolvencia", "2.01": "aquisicao ou alienacao",
    "2.02": "resultados", "2.03": "nova divida", "2.04": "aceleracao de divida",
    "3.01": "AVISO DE DELISTING", "3.02": "venda nao registada de accoes",
    "3.03": "alteracao a direitos dos accionistas",
    "4.01": "mudanca de auditor", "4.02": "demonstracoes nao fiaveis",
    "5.02": "saida ou entrada de administradores", "5.03": "alteracao de estatutos",
    "7.01": "Reg FD", "8.01": "outros eventos",
}
RED_FLAG_ITENS = {"1.03", "2.04", "3.01", "4.01", "4.02"}

# Afirmacao vs avaliacao. "avaliamos se ha duvida substancial" e rotina contabil
# (ASC 205-40) e aparece em quase todos os 10-Q de biotech; "concluimos que
# existe duvida substancial" e o red flag. Confundir os dois marcaria metade do
# sector como em risco.
_AFIRMA = re.compile(
    r"(concluded that substantial doubt exists"
    r"|substantial doubt exists about (?:its|our|the compan)"
    r"|there is substantial doubt about (?:its|our|the compan)"
    r"|raise substantial doubt about (?:its|our|the compan)[^.]{0,200}?\bhas (?:not )?been alleviated)", re.I)
_ALIVIA = re.compile(r"(no substantial doubt|substantial doubt[^.]{0,120}alleviated"
                     r"|does not raise substantial doubt)", re.I)


class FalhaRede(RuntimeError):
    """Distinta de 'nao existe'. Um pedido estrangulado nao pode virar
    'sem submissoes' — seria uma falha de rede disfarcada de facto sobre a
    empresa, o mesmo erro que ja pagamos tres vezes hoje."""


def _get(url, cache_key=None):
    if cache_key:
        cp = f"{CACHE}/{cache_key}"
        os.makedirs(os.path.dirname(cp), exist_ok=True)
        if os.path.exists(cp):
            return open(cp, encoding="utf-8").read()
    for tent in range(TENTATIVAS):
        r = _S.get(url, timeout=40)
        time.sleep(PACE)
        if r.status_code == 200:
            if cache_key:
                open(cp, "w", encoding="utf-8").write(r.text)
            return r.text
        if r.status_code == 404:
            return None                      # nao existe mesmo
        # D0-4: 1,2,4,8,16 s esgotava-se em 31 s e a SEC devolveu 503 durante
        # mais tempo do que isso em 30-07. Oito tentativas com tecto de 60 s
        # dao ~3 min de paciencia; o jitter evita que 40 tickers voltem todos
        # ao mesmo tempo e reconstruam a rajada que causou o estrangulamento.
        time.sleep(min(2 ** tent, BACKOFF_MAX_S) * (1 + random.random() * JITTER))
    raise FalhaRede(f"{url} -> {r.status_code} apos {TENTATIVAS} tentativas")


def mapa_cik(sessao):
    t = _get("https://www.sec.gov/files/company_tickers.json", f"{sessao}/cik.json")
    if not t:
        return {}
    return {v["ticker"]: str(v["cik_str"]).zfill(10) for v in json.loads(t).values()}


def submissoes(cik, sessao):
    t = _get(f"https://data.sec.gov/submissions/CIK{cik}.json", f"{sessao}/sub_{cik}.json")
    return json.loads(t) if t else None


def _texto(cik, acc, doc, sessao):
    url = (f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/"
           f"{acc.replace('-', '')}/{doc}")
    t = _get(url, f"{sessao}/doc_{acc}.htm")
    if not t:
        return ""
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", t))


def going_concern(cik, sub, sessao):
    """Tres estados. Um texto que nao permite concluir vai para A_REVER —
    nunca para aprovado."""
    r = sub["filings"]["recent"]
    idx = [i for i, f in enumerate(r["form"]) if f in ("10-Q", "10-K", "20-F")]
    if not idx:
        return {"gc_estado": "SEM_RELATORIO", "gc_form": "-", "gc_data": "-", "gc_excerto": "-"}
    i = idx[0]
    txt = _texto(cik, r["accessionNumber"][i], r["primaryDocument"][i], sessao)
    base = {"gc_form": r["form"][i], "gc_data": r["filingDate"][i]}
    if not txt:
        return {**base, "gc_estado": "SEM_TEXTO", "gc_excerto": "-"}
    m = _AFIRMA.search(txt)
    if m:
        return {**base, "gc_estado": "CONFIRMADO",
                "gc_excerto": txt[max(0, m.start() - 80):m.end() + 80].strip()[:240]}
    if re.search(r"going concern", txt, re.I):
        if _ALIVIA.search(txt):
            return {**base, "gc_estado": "ALIVIADO", "gc_excerto": "-"}
        return {**base, "gc_estado": "A_REVER",
                "gc_excerto": "mencao a going concern sem conclusao inequivoca"}
    return {**base, "gc_estado": "SEM_SINAL", "gc_excerto": "-"}


def eventos(sub, desde, limite=8):
    r = sub["filings"]["recent"]
    itens_flag, cat = set(), []
    for i, f in enumerate(r["form"]):
        if f != "8-K" or r["filingDate"][i] < desde:
            continue
        its = [x.strip() for x in (r.get("items") or [""] * len(r["form"]))[i].split(",") if x.strip()]
        itens_flag |= (set(its) & RED_FLAG_ITENS)
        cat.append(f"{r['filingDate'][i]}: " +
                   "; ".join(ITENS.get(x, x) for x in its))
        if len(cat) >= limite:
            break
    return itens_flag, cat


def analisa(tickers, sessao, desde_8k, desde_split, reverse_splits=None):
    """Cruza EDGAR com o registo de splits do Polygon.

    ``reverse_splits=None`` significa que a verificacao externa falhou. Nesse
    caso o estado fica incompleto e o candidato nao pode ser aprovado.
    Um dicionario vazio significa consulta bem-sucedida sem ocorrencias.
    """
    cik = mapa_cik(sessao)
    out = []
    for t in tickers:
        c = cik.get(t)
        if not c:
            out.append({"Ticker": t, "estado": "SEM_CIK"})
            continue
        try:
            sub = submissoes(c, sessao)
            if not sub:
                out.append({"Ticker": t, "estado": "SEM_SUBMISSOES"})
                continue
            gc = going_concern(c, sub, sessao)
            flags, cat = eventos(sub, desde_8k)
        except FalhaRede as e:
            out.append({"Ticker": t, "estado": "FALHA_REDE", "detalhe": str(e)[:120]})
            continue
        rs_eventos = None if reverse_splits is None else reverse_splits.get(t, [])
        rs = rs_eventos[0] if rs_eventos else None
        estado = "VERIFICACAO_INCOMPLETA" if rs_eventos is None else "OK"
        ratio = (f"{rs.get('split_from')}:{rs.get('split_to')}" if rs else "-")
        out.append({"Ticker": t, "estado": estado, **gc,
                    "itens_red_flag": ",".join(sorted(flags)) or "-",
                    "reverse_split": rs.get("execution_date") if rs else "-",
                    "reverse_split_ratio": ratio,
                    "eventos_recentes": " | ".join(cat[:3]) or "-",
                    "reprova": gc["gc_estado"] == "CONFIRMADO" or "3.01" in flags
                               or "1.03" in flags or "4.02" in flags
                               or bool(rs)})
    return out
