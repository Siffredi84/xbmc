"""Camada Finnhub com cache por dia de mercado.

Sem cache, cada passagem repetia 144 chamadas (3,5 min) — incompativel com
iteracao e com a politica de reserva de quota. O cache e indexado pela ultima
sessao fechada: muda de dia, invalida-se sozinho.
"""
import hashlib, json, math, os, time
import requests
import config

CACHE = "fh_cache"
_S = requests.Session()


def _key():
    return os.environ["FINNHUB_KEY"]


def _get(path, sessao, **params):
    os.makedirs(f"{CACHE}/{sessao}", exist_ok=True)
    # A janela e o metric fazem parte da identidade do pedido. Sem isto, uma
    # cache de insiders a 6 meses era reutilizada num pedido a 30 dias.
    assinatura = hashlib.sha256(
        json.dumps(params, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()[:12]
    nome = (path.replace("/", "_") + "_" + params.get("symbol", "x") +
            "_" + assinatura + ".json")
    cp = f"{CACHE}/{sessao}/{nome}"
    if os.path.exists(cp):
        return json.load(open(cp))
    params["token"] = _key()
    for _ in range(3):
        r = _S.get(f"https://finnhub.io/api/v1/{path}", params=params, timeout=25)
        time.sleep(config.FINNHUB_PACE_S)
        if r.status_code == 429:
            time.sleep(5)
            continue
        if r.status_code == 200:
            try:
                j = r.json()
            except ValueError:
                # 200 com HTML: endpoint fora do plano. Nao e dado, e ausencia
                # de acesso — devolve None e o chamador etiqueta.
                return None
            json.dump(j, open(cp, "w"))
            return j
        if r.status_code in (401, 403):
            return None                      # fora do plano: nao insistir
    return None


def _numero(valor):
    """Float finito ou None. NaN e ausencia, nao valor — e um NaN que atravessa
    uma comparacao devolve False em silencio."""
    try:
        n = float(valor)
    except (TypeError, ValueError):
        return None
    return n if math.isfinite(n) else None


def _positivo(valor):
    try:
        n = float(valor)
    except (TypeError, ValueError):
        return None
    return n if math.isfinite(n) and n > 0 else None


def calcula_market_cap(profile, preco):
    """Market cap canonico em USD milhoes.

    O Finnhub documenta ``shareOutstanding`` em milhoes de accoes; multiplicar
    pelo preco USD produz directamente milhoes de USD. O market cap fornecido
    fica como verificacao cruzada, nunca como decisor.
    """
    shares_m = _positivo(profile.get("shareOutstanding"))
    preco = _positivo(preco)
    fonte_m = _positivo(profile.get("marketCapitalization"))
    if shares_m is None or preco is None:
        return None
    calculado_m = shares_m * preco
    divergencia = (abs(fonte_m / calculado_m - 1) * 100
                   if fonte_m is not None else None)
    estado = ("SEM_COMPARADOR" if divergencia is None else
              "DIVERGENTE" if divergencia > config.MCAP_DIVERGENCIA_MAX_PCT
              else "COERENTE")
    return {
        "MCapM": calculado_m,
        "MCapFinnhubM": fonte_m,
        "SharesOutstandingM": shares_m,
        "MCapDivergenciaPct": divergencia,
        "MCapEstado": estado,
    }


def queda_sem_recuperacao(high52_pct, low52_pct):
    """True = red flag, False = limpo, None = indeterminado.

    D0-2: com um dos lados em falta isto levantava TypeError, e a alternativa
    obvia — tratar a ausencia como False — seria exactamente a falha que o
    principio invariante proibe: um 52 semanas que o Finnhub nao devolveu a
    disfarcar-se de 'nao houve colapso'. None obriga o chamador a decidir, e a
    decisao correcta e nao aprovar sem verificacao.
    """
    alto, baixo = _numero(high52_pct), _numero(low52_pct)
    if alto is None or baixo is None:
        return None
    return (alto <= config.QUEDA_52S_MAX_PCT
            and baixo < config.RECUPERACAO_52S_MIN_PCT)


def enriquece(tickers, sessao, prices, desde="2025-07-29", ate="2026-07-29"):
    """Devolve (registos, falhas). Uma resposta vazia NUNCA vira um NaN que o
    filtro descarta em silencio — vai para falhas e o chamador decide."""
    out, falhas = [], []
    for t in tickers:
        pr = _get("stock/profile2", sessao, symbol=t)
        me = _get("stock/metric", sessao, symbol=t, metric="all")
        fi = _get("stock/filings", sessao, symbol=t, **{"from": desde, "to": ate})
        metric = (me or {}).get("metric") if isinstance(me, dict) else None
        mcap = calcula_market_cap(pr or {}, prices.get(t))
        high52 = _positivo((metric or {}).get("52WeekHigh"))
        low52 = _positivo((metric or {}).get("52WeekLow"))
        if not pr or me is None or fi is None or mcap is None or high52 is None or low52 is None:
            falhas.append(t)
            continue
        forms = {f.get("form") for f in (fi or []) if isinstance(f, dict)}
        regime = ("10-Q" if any(f and f.startswith("10-") for f in forms)
                  else "20-F" if any(f and f.startswith(("20-", "6-")) for f in forms)
                  else "DESCONHECIDO")
        out.append({"Ticker": t, **mcap,
                    "Pais": pr.get("country"),
                    "Industria": pr.get("finnhubIndustry"),
                    "High52": high52,
                    "Low52": low52,
                    "regime_reporte": regime})
    return out, falhas
