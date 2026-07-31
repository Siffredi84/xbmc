"""Fila de evento: o que aconteceu, e durável, ja esta no preco?

Marketaux e o recurso escasso do stack (100/dia). So esta fila lhe toca —
os candidatos de continuacao nao tem noticia para procurar, por definicao.
Uma chamada por ticker, com cache por sessao e tecto de seguranca.
"""
import json, os, time
import requests
import config
import finnhub

CACHE = "mx_cache"
_S = requests.Session()


def _get(ticker, sessao, desde):
    os.makedirs(f"{CACHE}/{sessao}", exist_ok=True)
    cp = f"{CACHE}/{sessao}/{ticker}.json"
    if os.path.exists(cp):
        return json.load(open(cp))
    r = _S.get("https://api.marketaux.com/v1/news/all",
               params={"api_token": os.environ["MARKETAUX_KEY"], "symbols": ticker,
                       "filter_entities": "true", "language": "en",
                       "published_after": desde, "limit": 3},
               timeout=30)
    time.sleep(1.0)
    if r.status_code != 200:
        return None
    j = r.json()
    json.dump(j, open(cp, "w"))
    return j


def _finnhub_news(t, sessao, desde, ate):
    """Segunda fonte de noticias. Nenhum dos dois cobre bem micro-caps, por isso
    'sem noticias' so e afirmavel quando ambos vem vazios — e mesmo assim e
    ausencia de cobertura, nao ausencia de acontecimento."""
    j = finnhub._get("company-news", sessao, symbol=t, **{"from": desde, "to": ate})
    return j if isinstance(j, list) else []


def analisa(tickers, sessao, desde, ate="2026-07-29"):
    if len(tickers) > config.MARKETAUX_DIA_MAX:
        raise RuntimeError(f"{len(tickers)} chamadas excede o tecto diario "
                           f"({config.MARKETAUX_DIA_MAX}); reduzir a fila")
    out = []
    for t in tickers:
        j = _get(t, sessao, desde)
        if j is None:
            out.append({"Ticker": t, "estado": "SEM_DADOS"})
            continue
        arts = j.get("data", [])
        scores, titulos = [], []
        for a in arts:
            for e in a.get("entities", []):
                if e.get("symbol") == t and e.get("sentiment_score") is not None:
                    scores.append(float(e["sentiment_score"]))
            titulos.append(a.get("title", "")[:90])
        fh = _finnhub_news(t, sessao, desde, ate)
        if not titulos and fh:
            titulos = [a.get("headline", "")[:90] for a in fh]
        n = len(arts) + len(fh)
        estado = ("OK" if (arts or fh) else "SEM_COBERTURA")
        out.append({
            "Ticker": t, "estado": estado,
            "n_marketaux": len(arts), "n_finnhub": len(fh),
            "sentimento": round(sum(scores) / len(scores), 3) if scores else None,
            "titulo_recente": titulos[0] if titulos else "-",
        })
    return out
