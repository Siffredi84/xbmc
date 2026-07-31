"""Etapa 2 do pipeline: indicadores + gates tecnicos + quarentena.

Materializado durante a auditoria de 29-07: ate aqui esta logica so existia
em heredocs na conversa (defeito D5 da auditoria). Reproduz o codigo dos
heredocs SEM alteracoes de logica — incluindo o defeito D1 (a "janela 63"
usa na pratica 59 sessoes) — para que a re-execucao seja comparavel.
Le pg_universe.json, escreve pg_shortlist63.csv e pg_universo_diag.csv.
"""
import json
import numpy as np
import pandas as pd
import quarentena as q
import config as C


def universo_valido(meta):
    return (meta.get("type") == C.TIPO_VALIDO
            and meta.get("exch") in C.EXCH_POLYGON)


def rsi(c, n=C.JANELA_RSI):
    d = np.diff(c)
    g, l = np.where(d > 0, d, 0), np.where(d < 0, -d, 0)
    ag, al = g[:n].mean(), l[:n].mean()
    for i in range(n, len(d)):
        ag = (ag * (n - 1) + g[i]) / n
        al = (al * (n - 1) + l[i]) / n
    return 100.0 if al == 0 else 100 - 100 / (1 + ag / al)


def main():
    u = json.load(open("pg_universe.json"))
    bars, ref = u["bars"], u["ref"]

    por_dia = {}
    for t, bs in bars.items():
        for b in bs:
            por_dia.setdefault(b["d"], []).append(t)
    sess = q.sessoes_mercado(por_dia)

    rows = []
    for t, bs in bars.items():
        m = ref.get(t)
        if not m or not universo_valido(m):
            continue
        bs = sorted(bs, key=lambda x: x["d"])
        datas = [x["d"] for x in bs]
        dest, motivo, det = q.diagnostico(datas, sess)
        c = np.array([x["c"] for x in bs])
        v = np.array([x["v"] for x in bs])
        if (len(bs) < 25 or bs[-1]["d"] != sess[-1]) and not dest:
            dest, motivo, det = "QUARENTENA", "SERIE_CURTA", {"faltas": len(sess) - len(bs)}
        # D1 corrigido: a janela conta SESSOES DE MERCADO, nao posicoes do slice.
        # v[-1] e o dia corrente; a media usa as C.JANELA_VOLUME sessoes anteriores.
        calc = q.indicadores_fiaveis(dest) and len(c) >= C.JANELA_VOLUME + 1
        a63 = v[-(C.JANELA_VOLUME + 1):-1].mean() if calc else np.nan
        a20 = v[-(C.JANELA_TENDENCIA + 1):-1].mean() if calc else np.nan
        rows.append({
            "Ticker": t, "Nome": m["name"], "destino": dest or "PASSA_FASE0",
            "motivo": motivo, "faltas": det.get("faltas"),
            "Price": c[-1], "AvgVolN": a63,
            "RelVol": v[-1] / a63 if calc and a63 else np.nan,
            "TendVol": a20 / a63 if calc and a63 else np.nan,
            "RSI": rsi(c) if calc else np.nan,
            "SMA20_pct": (c[-1] / c[-C.JANELA_SMA:].mean() - 1) * 100 if calc else np.nan,
            "Eco": (v[-C.JANELA_TENDENCIA:] / a63).max() / (v[-1] / a63) if calc and a63 else np.nan,
            "Vol20d": np.std(np.diff(np.log(c[-(C.JANELA_TENDENCIA + 1):]))) * np.sqrt(252) * 100 if calc else np.nan,
        })
    d = pd.DataFrame(rows)
    d.to_csv("pg_universo_diag.csv", index=False)

    ok = d[d.destino == "PASSA_FASE0"]
    s = ok[(ok.Price.between(C.PRECO_MIN, C.PRECO_MAX)) & (ok.AvgVolN > C.VOL_MEDIO_MIN) &
           (ok.RelVol > C.RELVOL_MIN) & (ok.RSI.between(C.RSI_MIN, C.RSI_MAX)) &
           (ok.SMA20_pct > C.SMA20_MIN_PCT)]
    s.to_csv("pg_shortlist63.csv", index=False)
    print(f"universo CS: {len(d)} | integros: {len(ok)} | "
          f"quarentena: {(d.destino == 'QUARENTENA').sum()} | shortlist: {len(s)}")


if __name__ == "__main__":
    main()
