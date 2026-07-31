"""Sinais de descoberta precoce.

O documento de criterios pede bonus para: insider buying recente, nova cobertura
de analistas, partnerships ainda sem hype, e proximidade de um breakout com a
resistencia ja testada 2-3 vezes.

Nada aqui filtra nem pontua. Sao etiquetas que dizem *porque* um candidato pode
estar cedo — e a ausencia de um sinal nunca e prova da sua ausencia no mundo,
so da sua ausencia nas fontes que consultamos.
"""
import numpy as np
import pandas as pd
import finnhub

JANELA_RESISTENCIA = 60
TOQUE_TOLERANCIA = 0.02      # dentro de 2% do nivel conta como toque
PROXIMIDADE_BREAKOUT = 0.08  # a menos de 8% da resistencia


def cobertura_analistas(tickers, sessao):
    """SEM FONTE no stack actual — verificado em 29-07-2026.

    Finnhub free: /stock/recommendation-trends devolve HTML com 200 e
    /stock/upgrade-downgrade devolve 403 explicito. Twelve Data Basic: ambos
    os endpoints de ratings exigem plano ultra ou enterprise.

    Devolve None em vez de False. False afirmaria que nao ha nova cobertura;
    None diz que nao sabemos — que e a verdade. O sinal fica por construir e
    exige uma fonte nova (Benzinga, MarketBeat) ou scraping.
    """
    return [{"Ticker": t, "analistas": None, "analistas_ha_3m": None,
             "nova_cobertura": None} for t in tickers]
    out = []
    for t in tickers:
        rec = finnhub._get("stock/recommendation-trends", sessao, symbol=t)
        if rec is None:
            out.append({"Ticker": t, "analistas": None, "nova_cobertura": None})
            continue
        r = rec if isinstance(rec, list) else []
        tot = lambda x: sum(x.get(k, 0) or 0 for k in
                            ("strongBuy", "buy", "hold", "sell", "strongSell"))
        agora = tot(r[0]) if r else 0
        antes = tot(r[3]) if len(r) > 3 else (tot(r[-1]) if r else 0)
        out.append({"Ticker": t, "analistas": agora,
                    "analistas_ha_3m": antes,
                    "nova_cobertura": bool(r) and agora > antes})
    return out


def proximidade_breakout(bars, tickers):
    """Resistencia = maximo de fecho na janela, excluindo os ultimos 5 dias
    (senao o proprio movimento de hoje define o nivel e o teste e circular)."""
    out = []
    for t in tickers:
        b = sorted(bars.get(t, []), key=lambda x: x["d"])
        c = np.array([x["c"] for x in b])
        if len(c) < JANELA_RESISTENCIA:
            out.append({"Ticker": t, "resistencia": None, "toques": None,
                        "dist_resistencia_pct": None, "perto_breakout": None})
            continue
        base = c[-JANELA_RESISTENCIA:-5]
        nivel = float(base.max())
        toques = int((base >= nivel * (1 - TOQUE_TOLERANCIA)).sum())
        dist = (c[-1] / nivel - 1) * 100
        out.append({"Ticker": t, "resistencia": round(nivel, 2),
                    "toques": toques, "dist_resistencia_pct": round(dist, 1),
                    "perto_breakout": bool(-PROXIMIDADE_BREAKOUT * 100 <= dist <= 0
                                           and 2 <= toques <= 8)})
    return out


def compila(tickers, sessao, bars, insiders=None, artigos=None):
    d = pd.DataFrame({"Ticker": list(tickers)})
    d = d.merge(pd.DataFrame(cobertura_analistas(tickers, sessao)), on="Ticker", how="left")
    d = d.merge(pd.DataFrame(proximidade_breakout(bars, tickers)), on="Ticker", how="left")
    if insiders is not None:
        cols = ["Ticker", "accoes_compradas", "saldo_insider"]
        d = d.merge(insiders[cols], on="Ticker", how="left")
        # O sinal e a existencia de compra aberta recente, nao o saldo bruto.
        # Uma venda nao apaga o facto verificavel de que houve uma compra P.
        d["insider_comprador"] = d.accoes_compradas.fillna(0) > 0
    if artigos is not None:
        # Proxy de hype: quantos artigos as fontes viram. Baixo = ainda pouco
        # falado — MAS as fontes cobrem mal micro-caps, por isso "0 artigos"
        # tanto pode ser cedo como invisivel. E pista, nao conclusao.
        d = d.merge(artigos[["Ticker", "n_marketaux", "n_finnhub"]], on="Ticker", how="left")
        d["hype_baixo"] = (d.n_marketaux.fillna(0) + d.n_finnhub.fillna(0)) <= 2
    sinais = [c for c in ("nova_cobertura", "perto_breakout",
                          "insider_comprador", "hype_baixo") if c in d.columns]
    d["n_sinais"] = d[sinais].fillna(False).sum(axis=1).astype(int)
    return d.sort_values("n_sinais", ascending=False)
