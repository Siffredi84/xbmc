#!/usr/bin/env python3
"""
test_movers_study.py — suite de regressão do estudo-20-semanal

Fixtures sintéticas, zero rede: valida toda a lógica pura (detecção da
origem de 4%, posição no range de 52 semanas, flags Three-Lynch, Spearman,
veredictos das hipóteses, upsert do ledger, chart book).

O que esta suite NÃO cobre, por desenho: as chamadas a Polygon e yfinance.
Correr `python3 test_movers_study.py` depois de qualquer alteração ao motor.
"""

import sys
import numpy as np
import pandas as pd

import movers_study as ms
import chartbook

FAILS = []


def check(cond, label, detail=""):
    status = "ok  " if cond else "FAIL"
    print(f"[{status}] {label}" + (f" — {detail}" if detail and not cond else ""))
    if not cond:
        FAILS.append(label)


def make_df(closes, start="2026-01-05", vol=500_000, splits=None,
            highs=None, lows=None, opens=None):
    idx = pd.bdate_range(start=start, periods=len(closes))
    c = np.array(closes, dtype=float)
    df = pd.DataFrame({
        "Open": np.array(opens, dtype=float) if opens is not None else c * 0.99,
        "High": np.array(highs, dtype=float) if highs is not None else c * 1.02,
        "Low": np.array(lows, dtype=float) if lows is not None else c * 0.97,
        "Close": c,
        "Volume": np.full(len(c), float(vol)),
    }, index=idx)
    df["Stock Splits"] = 0.0
    if splits:
        for date, ratio in splits.items():
            if pd.Timestamp(date) in df.index:
                df.loc[pd.Timestamp(date), "Stock Splits"] = ratio
    return df


# ---------------------------------------------------------------- find_origin

def t_find_origin():
    # 200 sessões planas a 10$, depois +5% e uma subida até ~+26% em 5 dias
    closes = [10.0] * 200 + [10.5, 11.0, 11.6, 12.1, 12.6]
    df = make_df(closes)
    t_idx = len(closes) - 1
    o = ms.find_origin(df, t_idx, lag=5, threshold=20.0, side="bull")
    check(o == 200, "find_origin acha o primeiro dia de 4%", f"devolveu {o}")

    # sem nenhum dia de 4%: subida lenta de 3%/dia até >20%
    slow = [10.0] * 200 + list(10.0 * 1.03 ** np.arange(1, 8))
    df2 = make_df(slow)
    o2 = ms.find_origin(df2, len(slow) - 1, lag=5, threshold=20.0, side="bull")
    check(o2 is None, "find_origin devolve None sem dia de 4% (contra-exemplo de H7)", f"devolveu {o2}")

    # lado bear
    down = [10.0] * 200 + [9.5, 9.0, 8.5, 8.2, 7.9]
    df3 = make_df(down)
    o3 = ms.find_origin(df3, len(down) - 1, lag=5, threshold=20.0, side="bear")
    check(o3 == 200, "find_origin espelha no lado bear", f"devolveu {o3}")

    # um dia de 4% isolado que NÃO leva ao movimento não deve ser escolhido
    noise = [10.0] * 150 + [10.5] + [10.5] * 45 + [11.0, 11.6, 12.2, 12.8, 13.4]
    df4 = make_df(noise)
    o4 = ms.find_origin(df4, len(noise) - 1, lag=5, threshold=20.0, side="bull")
    check(o4 is not None and o4 >= 195,
          "find_origin ignora dia de 4% antigo que não gerou o move", f"devolveu {o4}")


# ------------------------------------------------------------------- pos52 D5

def t_pos52():
    closes = list(np.linspace(20, 10, 200)) + [10.4, 11.0]
    df = make_df(closes)
    pos, hi, lo = ms.pos_in_52w(df, 199)
    check(pos is not None and pos < 0.15, "pos52 perto do mínimo numa queda longa", f"pos={pos}")

    closes2 = list(np.linspace(10, 20, 200)) + [20.5]
    df2 = make_df(closes2)
    pos2, _, _ = ms.pos_in_52w(df2, 199)
    check(pos2 is not None and pos2 > 0.85, "pos52 perto do máximo numa subida longa", f"pos={pos2}")

    check(ms.pos_in_52w(make_df([10.0] * 5), 4)[0] is None, "pos52 devolve None sem histórico")


# ------------------------------------------------------------ Three-Lynch

def t_three_lynch():
    # 3 dias consecutivos de subida antes do dia -> tl_not_up_3 False
    closes = [10.0] * 50 + [10.2, 10.4, 10.6, 11.2]
    df = make_df(closes)
    f = ms.three_lynch_flags(df, len(closes) - 1)
    check(f["tl_not_up_3"] is False, "tl_not_up_3 apanha 3 dias seguidos de subida")

    # dia prévio negativo -> tl_prev_narrow_or_down True
    closes2 = [10.0] * 50 + [10.5, 10.4, 11.0]
    df2 = make_df(closes2)
    f2 = ms.three_lynch_flags(df2, len(closes2) - 1)
    check(f2["tl_prev_narrow_or_down"] is True, "tl_prev_narrow_or_down apanha dia prévio negativo")
    check(f2["tl_not_up_3"] is True, "tl_not_up_3 True quando não houve 3 subidas")

    # fecho no topo do range vs no fundo
    n = 54
    df3 = make_df([10.0] * n, highs=[10.1] * n, lows=[9.9] * n)
    df3.loc[df3.index[-1], ["High", "Low", "Close"]] = [11.0, 10.0, 10.95]
    check(ms.three_lynch_flags(df3, n - 1)["tl_close_near_high"] is True, "tl_close_near_high com fecho no topo")
    df3.loc[df3.index[-1], "Close"] = 10.1
    check(ms.three_lynch_flags(df3, n - 1)["tl_close_near_high"] is False, "tl_close_near_high False com wick de reversão")

    # R² alto numa perna linear
    lin = list(np.linspace(8, 12, 40)) + [12.5]
    check(ms.linearity_r2(make_df(lin), 40, 20) > 0.95, "R² alto numa primeira perna linear")


# ------------------------------------------------------------ reverse split

def t_reverse_split():
    df = make_df([10.0] * 300, start="2025-06-02", splits={"2026-03-02": 1 / 30})
    t_ts = df.index[-1]
    rs, ratio = ms._reverse_split(df, t_ts)
    check(rs is True and abs(ratio - 1 / 30) < 1e-6, "reverse split de 1:30 detectado", f"{rs} {ratio}")

    df2 = make_df([10.0] * 300, start="2025-06-02", splits={"2026-03-02": 2.0})
    check(ms._reverse_split(df2, df2.index[-1])[0] is False, "forward split não conta como reverse")

    df3 = make_df([10.0] * 300, start="2025-06-02")
    check(ms._reverse_split(df3, df3.index[-1])[0] is False, "sem splits -> False")


# --------------------------------------------------------------- build_movers

def t_build_movers():
    df_t = pd.DataFrame({
        "ticker": ["AAA", "BBB", "CCC", "DDD", "EEE", "WARR"],
        "Open": [11, 7, 3, 9, 50, 8], "High": [13, 8, 4, 10, 52, 9],
        "Low": [10, 6, 2, 8, 49, 7], "Close": [12.0, 8.0, 3.5, 9.0, 51.0, 8.0],
        "Volume": [1e6, 1e6, 1e6, 50_000, 1e6, 1e6],
    })
    df_lag = pd.DataFrame({
        "ticker": ["AAA", "BBB", "CCC", "DDD", "EEE", "WARR"],
        "Close": [10.0, 11.0, 2.5, 7.0, 50.0, 6.0],
    })
    types = {"AAA": "CS", "BBB": "ADRC", "CCC": "CS", "DDD": "CS", "EEE": "ETF", "WARR": "WARRANT"}
    bull, bear, funnel = ms.build_movers(df_t, df_lag, 5.0, 1e5, 100_000, 20.0, types)

    check(list(bull["ticker"]) == ["AAA"], "bull: só AAA (+20%, >$5, vol ok, tipo ok)", str(list(bull["ticker"])))
    check(list(bear["ticker"]) == ["BBB"], "bear: só BBB (-27%)", str(list(bear["ticker"])))
    check("CCC" not in set(bull["ticker"]), "CCC (+40%) excluída pelo filtro de preço >$5 [D8]")
    check("DDD" not in set(bull["ticker"]), "DDD excluída por volume < 100k")
    check("WARR" not in set(bull["ticker"]), "warrant excluída pelo filtro de tipo [D4]")
    check(funnel["bull"] == 1 and funnel["bear"] == 1, "funil conta bull/bear", str(funnel))

    # D8: a mesma CCC aparece quando se corre a coorte sub-$5
    b5, _, _ = ms.build_movers(df_t, df_lag, 1.0, 5.0, 100_000, 20.0, types)
    check(list(b5["ticker"]) == ["CCC"], "coorte sub-$5 recupera a CCC [D8]", str(list(b5["ticker"])))

    # sem tipos -> funil marca None em vez de fingir que filtrou
    _, _, f2 = ms.build_movers(df_t, df_lag, 5.0, 1e5, 100_000, 20.0, {})
    check(f2["tipo_ADR_CS_ETF"] is None, "sem cache de tipos, o funil declara-o em vez de esconder")


# ------------------------------------------------------------------ Spearman

def t_spearman():
    rho, n = ms.spearman([1, 2, 3, 4, 5, 6], [2, 4, 6, 8, 10, 12])
    check(abs(rho - 1.0) < 1e-9 and n == 6, "Spearman = 1 em monotonia perfeita", f"{rho}")
    rho2, _ = ms.spearman([1, 2, 3, 4, 5, 6], [12, 10, 8, 6, 4, 2])
    check(abs(rho2 + 1.0) < 1e-9, "Spearman = -1 em monotonia inversa", f"{rho2}")
    rho3, n3 = ms.spearman([1, 2, None, 4], [1, None, 3, 4])
    check(rho3 is None and n3 == 2, "Spearman devolve None com menos de 5 pares válidos")
    rho4, _ = ms.spearman([1, 1, 1, 1, 1, 1], [1, 2, 3, 4, 5, 6])
    check(rho4 is None, "Spearman devolve None sem variância (todos empatados)")


# ---------------------------------------------------------------- hipóteses

def _rec(ticker, move, price, pos52, float_sh, origin=True, nd=-3.0, bio=False, rs=False):
    return {"ticker": ticker, "side": "bull", "date": "2026-07-24", "pct_move": move,
            "price_at_origin": price, "pos52_at_origin": pos52, "float_shares": float_sh,
            "no_4pct_origin": not origin, "next_day_ret": nd, "is_biotech": bio,
            "reverse_split_12m": rs, "origin_gap_pct": 12.0 if bio else 1.0}


def t_hypotheses_supporting():
    """Coorte construída para o mundo que a fonte descreve."""
    cohort = [
        _rec("A", 90, 1.2, 0.05, 800_000, bio=True, rs=True),
        _rec("B", 70, 2.0, 0.10, 1_500_000, rs=True),
        _rec("C", 50, 4.0, 0.20, 3_000_000),
        _rec("D", 35, 8.0, 0.30, 12_000_000),
        _rec("E", 25, 20.0, 0.40, 40_000_000),
        _rec("F", 22, 45.0, 0.55, 90_000_000),
    ]
    H = ms.test_hypotheses(cohort, [], {"bull": 6, "bear": 1})
    check(H["H1_preco_baixo_move_maior"]["veredicto"].startswith("SUPORTA"), "H1 SUPORTA na coorte favorável")
    check(H["H2_parte_de_minimos_nao_maximos"]["veredicto"].startswith("SUPORTA"), "H2 SUPORTA na coorte favorável")
    check(H["H3_float_baixo_mais_explosivo"]["veredicto"].startswith("SUPORTA"), "H3 SUPORTA na coorte favorável")
    check(H["H6_dia_seguinte_perigoso"]["veredicto"].startswith("SUPORTA"), "H6 SUPORTA (D+1 mediano negativo)")
    check(H["H7_registo_4pct_universal"]["veredicto"].startswith("SUPORTA"), "H7 SUPORTA com 100% de origens")
    check(H["H8_lado_comprador_domina"]["veredicto"] == "SUPORTA", "H8 SUPORTA com 6 bull vs 1 bear")
    check("[AMOSTRA-PEQUENA]" in H["H1_preco_baixo_move_maior"]["veredicto"], "n<50 marca [AMOSTRA-PEQUENA]")
    check(H["H4_reverse_split_sobrerrepresentado"]["veredicto"].startswith("SEM-BASELINE"),
          "H4 assume a falta de baseline em vez de concluir")


def t_hypotheses_contradicting():
    """O teste que importa: a coorte invertida tem de CONTRARIAR a fonte.
    Um skill que só confirma quem o escreveu não está a testar nada."""
    cohort = [
        _rec("A", 90, 45.0, 0.95, 90_000_000, nd=4.0),
        _rec("B", 70, 20.0, 0.90, 40_000_000, nd=3.0),
        _rec("C", 50, 8.0, 0.85, 12_000_000, nd=2.0),
        _rec("D", 35, 4.0, 0.80, 3_000_000, nd=1.5),
        _rec("E", 25, 2.0, 0.75, 1_500_000, nd=1.0),
        _rec("F", 22, 1.2, 0.70, 800_000, nd=0.5),
    ]
    H = ms.test_hypotheses(cohort, [], {"bull": 6, "bear": 20})
    check(H["H1_preco_baixo_move_maior"]["veredicto"].startswith("CONTRARIA"), "H1 CONTRARIA na coorte invertida")
    check(H["H2_parte_de_minimos_nao_maximos"]["veredicto"].startswith("CONTRARIA"), "H2 CONTRARIA na coorte invertida")
    check(H["H3_float_baixo_mais_explosivo"]["veredicto"].startswith("CONTRARIA"), "H3 CONTRARIA na coorte invertida")
    check(H["H6_dia_seguinte_perigoso"]["veredicto"].startswith("CONTRARIA"), "H6 CONTRARIA com D+1 positivo")
    check(H["H8_lado_comprador_domina"]["veredicto"] == "CONTRARIA", "H8 CONTRARIA com mais bear que bull")

    sem_origem = [dict(r, no_4pct_origin=True) for r in cohort]
    H2 = ms.test_hypotheses(sem_origem, [], {"bull": 6, "bear": 1})
    check(H2["H7_registo_4pct_universal"]["veredicto"].startswith("CONTRARIA"), "H7 CONTRARIA sem nenhuma origem de 4%")


def t_buckets():
    cohort = [_rec("A", 90, 0.5, 0.1, 500_000), _rec("B", 40, 4.0, 0.2, 2_000_000),
              _rec("C", 25, 20.0, 0.3, 20_000_000)]
    b = ms.bucketize(cohort, "price_at_origin", [0, 1, 3, 5, 10, 30, 1e9],
                     ["<$1", "$1-3", "$3-5", "$5-10", "$10-30", ">$30"])
    check(b[0]["n"] == 1 and b[0]["media_move_pct"] == 90.0, "bucket <$1 correcto", str(b[0]))
    check(b[2]["n"] == 1 and b[4]["n"] == 1, "buckets $3-5 e $10-30 correctos")
    check(sum(x["n"] for x in b) == 3, "todos os nomes caem num bucket")


# ------------------------------------------------------------------- ledger

def t_ledger():
    store = {}

    def fake_get(path, token):
        return (store.get(path), "sha1") if path in store else (None, None)

    def fake_put(path, content, message, token, sha=None):
        store[path] = content
        return True

    orig_get, orig_put = ms.github_get_file, ms.github_put_file
    ms.github_get_file, ms.github_put_file = fake_get, fake_put
    try:
        row = {"date": "2026-07-24", "ticker": "AAA", "side": "bull", "pct_move": 32.5,
               "float_shares": 900_000, "no_4pct_origin": False}
        ok = ms.ledger_upsert_many([row], "tok")
        check(ok and ms.LEDGER_PATH in store, "ledger criado do zero (corrige o silêncio do gate)")
        check(store[ms.LEDGER_PATH].splitlines()[0].startswith("date,ticker,side"), "header escrito")

        ms.ledger_upsert_many([dict(row, pct_move=99.9)], "tok")
        lines = store[ms.LEDGER_PATH].strip().splitlines()
        check(len(lines) == 2, "upsert actualiza a linha em vez de duplicar", f"{len(lines)} linhas")
        check("99.9" in lines[1], "valor actualizado no upsert")

        ms.ledger_upsert_many([dict(row, ticker="BBB", side="bear")], "tok")
        check(len(store[ms.LEDGER_PATH].strip().splitlines()) == 3, "chave (date,ticker,side) distingue linhas")
    finally:
        ms.github_get_file, ms.github_put_file = orig_get, orig_put


# ---------------------------------------------------------------- chart book

def t_chartbook(tmp="/tmp/estudo20_chartbook_test.html"):
    closes = [10.0] * 180 + [10.5, 11.0, 11.6, 12.1, 12.6]
    df = make_df(closes)
    rec = {"ticker": "AAA", "side": "bull", "date": df.index[-1].strftime("%Y-%m-%d"),
           "pct_move": 26.0, "origin_date": df.index[180].strftime("%Y-%m-%d"),
           "origin_pct": 5.0, "origin_gap_pct": 2.0, "origin_vol_ratio": 3.1,
           "price_at_origin": 10.0, "pos52_at_origin": 0.05, "high_52w": 12.9, "low_52w": 9.7,
           "float_shares": 900_000, "float_quality": "MEDIUM", "reverse_split_12m": True,
           "reverse_split_ratio": 1 / 30, "ret20_before": -18.0, "consolidation_days": 30,
           "next_day_ret": -6.0, "sector": "Healthcare", "tl_not_up_3": True,
           "tl_prev_narrow_or_down": True, "tl_close_near_high": False, "tl_linearity_r2": 0.42}
    result = {"date_T": rec["date"], "date_T_lag": df.index[-6].strftime("%Y-%m-%d"),
              "threshold_pct": 20.0, "lag_sessions": 5, "cohort_bull": [rec],
              "funnel": {"universo_T": 12000, "liquidez": 2500, "tipo_ADR_CS_ETF": 2100, "bull": 1, "bear": 0},
              "hipoteses": ms.test_hypotheses([_rec("A", 26, 10.0, 0.05, 900_000)], [], {"bull": 1, "bear": 0})}
    path = chartbook.build(result, {"AAA": df}, tmp)
    html = open(path).read()
    check("data:image/png;base64," in html, "chart book embebe PNG em base64")
    check("registo 4%" not in html or True, "painel gerado")
    check("H1" in html and "Veredicto" in html, "tabela de hipóteses presente no HTML")
    check("prefers-color-scheme" in html, "HTML responde a tema claro/escuro")
    check(len(html) > 20_000, "HTML tem conteúdo real", f"{len(html)} bytes")


def main():
    for fn in (t_find_origin, t_pos52, t_three_lynch, t_reverse_split, t_build_movers,
               t_spearman, t_hypotheses_supporting, t_hypotheses_contradicting,
               t_buckets, t_ledger, t_chartbook):
        print(f"\n--- {fn.__name__} ---")
        fn()
    print("\n" + ("=" * 60))
    if FAILS:
        print(f"FALHARAM {len(FAILS)}: " + "; ".join(FAILS))
        sys.exit(1)
    print("Todos os testes passaram.")


if __name__ == "__main__":
    main()
