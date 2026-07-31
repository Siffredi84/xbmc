"""Etiqueta de encaminhamento: evento vs continuacao.

Nao e score nem filtro. Determina que trabalho de verificacao cada candidato
recebe a jusante — noticias/sentimento para evento, insiders e diluicao para
continuacao — e por isso tambem quanto do orcamento Marketaux se gasta.
"""
import numpy as np
import config


def classifica(df):
    """Espera Eco e Vol20d ja calculados na fase 0."""
    d = df.copy()
    d["grupo"] = np.where(d.Eco >= config.ECO_CORTE, "CONTINUACAO", "EVENTO")
    d["ambiguo"] = (d.Eco - config.ECO_CORTE).abs() < 0.15
    d["vol_bandeira"] = d.Vol20d > config.VOL20D_BANDEIRA
    return d


def filas(df):
    """Filas de trabalho: so 10-Q entra no caminho automatico."""
    d = classifica(df)
    dez = d[d.regime_reporte == "10-Q"]
    return {"evento": sorted(dez[dez.grupo == "EVENTO"].Ticker),
            "continuacao": sorted(dez[dez.grupo == "CONTINUACAO"].Ticker),
            "fila_20f": sorted(d[d.regime_reporte != "10-Q"].Ticker)}
