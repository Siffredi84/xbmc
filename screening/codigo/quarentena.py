"""Detetor de quarentena por integridade de serie.

Principio: dados em falta nunca produzem uma decisao. Produzem uma etiqueta.
Um candidato sai da Fase 0 com um de tres destinos — PASSA, REPROVA, QUARENTENA —
e nunca desaparece em silencio por ter serie incompleta.

Linha de base: sessoes em que o mercado inteiro negociou. Ficheiros vazios sao
feriados e nao contam contra nenhum ticker.
"""
import numpy as np

import config
LIMIAR_FALHAS = config.QUARENTENA_LIMIAR_FALHAS
RUN_HALT = config.QUARENTENA_RUN_HALT


def sessoes_mercado(por_dia):
    """por_dia: {data: [tickers negociados]}. Devolve as datas com negociacao."""
    return sorted(d for d, ts in por_dia.items() if ts)


def diagnostico(datas_ticker, sessoes):
    """Classifica a integridade da serie de um ticker.

    Devolve (destino, motivo, detalhe) em que destino e '' quando esta integro.
    """
    presentes = set(datas_ticker)
    faltas = [d for d in sessoes if d not in presentes]
    n = len(faltas)
    if n <= LIMIAR_FALHAS:
        return "", "", {"faltas": n}

    # serie curta: comecou depois do inicio da janela (IPO, uplisting, novo ticker)
    idx = {d: i for i, d in enumerate(sessoes)}
    primeiro = min(idx[d] for d in presentes) if presentes else len(sessoes)
    if primeiro > LIMIAR_FALHAS and all(idx[d] < primeiro for d in faltas):
        return ("QUARENTENA", "SERIE_CURTA",
                {"faltas": n, "inicio": sessoes[primeiro]})

    # maior bloco contiguo de sessoes em falta
    run = melhor = 0
    ini_run = ini_melhor = None
    for d in sessoes:
        if d in presentes:
            run = 0
            ini_run = None
        else:
            if ini_run is None:
                ini_run = d
            run += 1
            if run > melhor:
                melhor, ini_melhor = run, ini_run

    if melhor >= RUN_HALT:
        return ("QUARENTENA", "INTERRUPCAO",
                {"faltas": n, "bloco": melhor, "desde": ini_melhor})
    return "QUARENTENA", "ILIQUIDEZ", {"faltas": n}


def indicadores_fiaveis(destino):
    """Indicadores de sequencia (RSI, tendencia de volume) nao sao calculaveis
    sobre uma serie com quebra. Quem esta em quarentena nao recebe score."""
    return destino == ""
