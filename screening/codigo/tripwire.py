"""Tripwire de divergencia: o funil Finviz corre em paralelo, so para discordar.

Nao produz candidatos. Serve uma unica funcao: se as duas fontes independentes
deixarem de concordar, alguem esta partido — e a manha de 29-07 mostrou que
essa deteccao vale mais do que qualquer resultado individual.

Divergencia acima do limiar nao interrompe o funil; assinala e nomeia quem
diverge, para investigacao.
"""
import pandas as pd
import finviz

LIMIAR_DIVERGENCIA = 2      # nomes sem explicacao acima disto = investigar
FILTROS = "cap_smallunder,geo_usa,sh_avgvol_o100,sh_price_1to10,sh_relvol_o1"


def _num(x):
    s = str(x).replace(",", "").strip()
    m = {"K": 1e3, "M": 1e6, "B": 1e9, "T": 1e12}
    if s and s[-1] in m:
        try:
            return float(s[:-1]) * m[s[-1]]
        except ValueError:
            return float("nan")
    return pd.to_numeric(s, errors="coerce")


def mesma_sessao(bars, amostra=("AAPL", "MSFT", "F", "T", "PFE")):
    """O Finviz nao tem data de referencia: mostra sempre AGORA. A nossa cache
    e da ultima sessao FECHADA. Em pre-market as duas medem dias diferentes e
    a comparacao produz alarme falso — foi o que aconteceu na primeira execucao
    deste modulo.

    Discrimina-se pelo VOLUME, nao pelo preco: em pre-market o preco de um
    large-cap mexe decimas e passa qualquer tolerancia razoavel, mas o volume
    acumulado e uma fraccao minima do de uma sessao inteira. A diferenca e de
    ordem de grandeza, nao de margem.
    """
    import finviz as fv
    sess = fv._session()
    ok, total = 0, 0
    for t in amostra:
        b = sorted(bars.get(t, []), key=lambda x: x["d"])
        if not b:
            continue
        h = sess.get(f"https://finviz.com/screener.ashx?v=111&t={t}", timeout=40).text
        try:
            linha = fv._parse_table(h)
        except Exception:
            continue
        if linha.empty:
            continue
        total += 1
        vol_fv = float(linha.Volume.iloc[0])
        if vol_fv >= 0.7 * b[-1]["v"]:
            ok += 1
    return (total > 0 and ok / total >= 0.8), f"{ok}/{total} com sessao completa"


def funil_finviz(config):
    d = finviz.scrape(FILTROS)
    d["MCap"] = d["Market Cap"].map(_num)
    d["AvgVol"] = d["Avg Volume"].map(_num)
    return set(d[(d.Price.between(config.PRECO_MIN, config.PRECO_MAX)) &
                 (d.MCap.between(config.MCAP_MIN_M * 1e6, config.MCAP_MAX_M * 1e6)) &
                 (d.AvgVol > config.VOL_MEDIO_MIN) &
                 (d["Rel Volume"] > config.RELVOL_MIN) &
                 (d.RSI.between(config.RSI_MIN, config.RSI_MAX)) &
                 (d.SMA20 > config.SMA20_MIN_PCT) &
                 (d["52W High"] <= config.HIGH52_MAX_PCT)].Ticker)


def compara(polygon_tickers, config, bars=None, explicados=()):
    """`explicados` sao divergencias ja compreendidas — tipicamente os
    emissores nao-domiciliados nos EUA, que o Finviz corta pelo filtro geo_usa
    e o nosso funil mantem por decisao registada (cotacao, nao domicilio)."""
    if bars is not None:
        alinhado, det = mesma_sessao(bars)
        if not alinhado:
            return {"estado": "NAO_COMPARAVEL",
                    "detalhe": f"Finviz noutra sessao ({det}); correr apos o "
                               f"fecho e antes do pre-market seguinte",
                    "alarme": False}
    fv = funil_finviz(config)
    pg = set(polygon_tickers)
    so_pg = sorted(pg - fv - set(explicados))
    so_fv = sorted(fv - pg - set(explicados))
    n = len(so_pg) + len(so_fv)
    return {"estado": "COMPARADO",
            "finviz": len(fv), "polygon": len(pg), "comuns": len(pg & fv),
            "so_polygon": so_pg, "so_finviz": so_fv,
            "divergencia_inexplicada": n,
            "alarme": n > LIMIAR_DIVERGENCIA}
