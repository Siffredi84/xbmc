#!/usr/bin/env python3
"""
test_pipeline_offline.py — orquestração dos 3 modos, sem rede

Corre o main() completo (estudo, caça, anual, coorte sub-$5, chart book)
com Polygon e yfinance substituídos por fixtures sintéticas. Valida o que
os testes unitários não vêem: o encadeamento dos estágios, a passagem de
argumentos, a forma do JSON de saída e o handoff.

O que continua por exercitar: as chamadas reais a Polygon/yfinance — só
possíveis numa máquina com acesso a esses hosts (ver SKILL.md, "Estado de
validação").
"""

import contextlib
import io as _io
import json
import os
import sys

import numpy as np
import pandas as pd

import movers_study as ms
from test_movers_study import check, FAILS, make_df

CAL = [d.strftime("%Y-%m-%d") for d in pd.bdate_range("2024-01-01", "2026-07-24")]
DATE_T = CAL[-1]

# Universo sintético: 3 movers bull, 1 bear, 1 sub-$5, ruído
SPEC = {
    "BIOX": {"lag5": 6.0, "t": 9.0, "vol": 3_000_000, "float": 900_000, "type": "CS"},
    "LOWF": {"lag5": 8.0, "t": 11.0, "vol": 1_200_000, "float": 2_500_000, "type": "CS"},
    "ADRZ": {"lag5": 20.0, "t": 25.0, "vol": 800_000, "float": 40_000_000, "type": "ADRC"},
    "DOWN": {"lag5": 30.0, "t": 21.0, "vol": 900_000, "float": 60_000_000, "type": "CS"},
    "PENN": {"lag5": 2.0, "t": 3.2, "vol": 4_000_000, "float": 700_000, "type": "CS"},
    "FLAT": {"lag5": 50.0, "t": 50.5, "vol": 2_000_000, "float": 80_000_000, "type": "CS"},
    "WARR": {"lag5": 6.0, "t": 9.0, "vol": 1_000_000, "float": 500_000, "type": "WARRANT"},
    "THIN": {"lag5": 6.0, "t": 9.0, "vol": 20_000, "float": 500_000, "type": "CS"},
}


def grouped_for(date_str):
    key = "t" if date_str == DATE_T else "lag5"
    rows = []
    for tk, s in SPEC.items():
        px = s[key]
        rows.append({"ticker": tk, "Open": px * 0.98, "High": px * 1.03,
                     "Low": px * 0.96, "Close": px, "Volume": float(s["vol"])})
    return pd.DataFrame(rows)


def history_for(tickers, date_t, sessions_needed):
    out = {}
    for tk in tickers:
        s = SPEC.get(tk)
        if not s:
            continue
        start, end = s["lag5"], s["t"]
        # 250 sessões em queda lenta (castigada) + 5 dias de movimento com dia de 4%
        decline = list(np.linspace(start * 2.2, start, 250))
        step = (end / start) ** (1 / 5)
        run = [start * step ** i for i in range(1, 6)]
        closes = decline + run
        idx_start = CAL[-(len(closes))]
        df = make_df(closes, start=idx_start, vol=s["vol"])
        df = df.set_index(pd.bdate_range(end=pd.Timestamp(DATE_T), periods=len(closes)))
        df["Stock Splits"] = 0.0
        if tk in ("BIOX", "PENN"):
            df.loc[df.index[-40], "Stock Splits"] = 1 / 20
        out[tk] = df
    return out


def fundamentals_for(ticker):
    s = SPEC.get(ticker, {})
    bio = ticker in ("BIOX", "PENN")
    return {"float_shares": s.get("float"), "shares_outstanding": (s.get("float") or 0) * 2,
            "sector": "Healthcare" if bio else "Industrials",
            "industry": "Biotechnology" if bio else "Machinery", "info_error": False}


def patch():
    os.environ["US_BREAKOUT_POLYGON"] = "offline-test"
    ms.trading_calendar = lambda end_date, sessions: CAL
    ms.fetch_grouped = lambda date_str, key: grouped_for(date_str)
    ms.load_universe_types = lambda key, refresh_days=7, force=False: {t: s["type"] for t, s in SPEC.items()}
    ms.fetch_history_batch = history_for
    ms.fetch_fundamentals = fundamentals_for
    ms.polygon_shares = lambda t, k: None


def run_cli(argv):
    sys.argv = ["movers_study.py"] + argv
    buf = _io.StringIO()
    with contextlib.redirect_stdout(buf):
        ms.main()
    return json.loads(buf.getvalue())


def t_modo_estudo():
    r = run_cli(["--date", DATE_T, "--no-ledger"])
    tickers = [x["ticker"] for x in r["cohort_bull"]]
    check(r["date_T"] == DATE_T and r["lag_sessions"] == 5, "modo estudo resolve T e lag")
    check(set(tickers) == {"BIOX", "LOWF", "ADRZ"}, "coorte bull correcta", str(tickers))
    check([x["ticker"] for x in r["cohort_bear"]] == ["DOWN"], "coorte bear correcta")
    # liquidez=6 (PENN cai por preço, THIN por volume) → tipo=5 (WARR cai por tipo)
    check(r["funnel"]["liquidez"] == 6 and r["funnel"]["tipo_ADR_CS_ETF"] == 5,
          "filtro de tipo removeu a warrant", str(r["funnel"]))
    check("PENN" not in tickers, "PENN (sub-$5) fora do scan fiel à fonte [D8]")
    check("THIN" not in tickers, "THIN fora por volume")

    rec = next(x for x in r["cohort_bull"] if x["ticker"] == "BIOX")
    check(rec["origin_date"] is not None and not rec["no_4pct_origin"], "origem de 4% identificada")
    check(rec["float_shares"] == 900_000 and rec["float_quality"] in ("HIGH", "MEDIUM", "LOW"),
          "float e float_quality preenchidos")
    check(rec["is_biotech"] is True, "flag biotech pelo sector/indústria [D6]")
    check(rec["reverse_split_12m"] is True, "reverse split de 1:20 detectado no histórico")
    check(rec["pos52_at_origin"] is not None and rec["pos52_at_origin"] < 0.2,
          "pos52 no terço inferior (ação castigada)", str(rec.get("pos52_at_origin")))
    check(rec["ret20_before"] is not None and rec["ret20_before"] < 0, "ret20 negativo antes da origem")
    check(rec["consolidation_capped"] is True,
          "consolidação truncada na janela de 60d é declarada, não fingida")

    H = r["hipoteses"]
    check(len(H) == 8, "as 8 hipóteses são devolvidas", str(list(H)))
    check(all("veredicto" in v for v in H.values()), "toda a hipótese traz veredicto")
    check(H["H8_lado_comprador_domina"]["racio_bull_bear"] == 3.0, "H8 conta 3 bull / 1 bear")
    check(H["H8_lado_comprador_domina"]["por_segmento"]["equity"] == {"bull": 3, "bear": 1},
          "H8 separa equities de fundos [D9]")


def t_coorte_sub5():
    r = run_cli(["--date", DATE_T, "--no-ledger", "--coorte-sub5"])
    sub = r.get("coorte_sub5")
    check(sub is not None, "coorte sub-$5 presente com --coorte-sub5")
    check([x["ticker"] for x in sub["cohort_bull"]] == ["PENN"], "PENN aparece na coorte sub-$5 [D8]")
    check("hipoteses" in sub and len(sub["hipoteses"]) == 8, "hipóteses recalculadas na coorte sub-$5")


def t_modo_caca():
    r = run_cli(["--modo", "caca", "--date", DATE_T, "--no-ledger"])
    check(r["modo"] == "caca" and r["lag_sessions"] == 1, "modo caça usa lag=1 e threshold 4%")
    check("shortlist" in r and "rejeitados" in r, "caça devolve shortlist e rejeitados")
    check("breakout-quality-gate" in r["handoff"], "handoff obrigatório para o gate está no output")
    check("{date_T}" not in r["handoff"] and DATE_T in r["handoff"],
          "handoff traz a data real, não o placeholder", r["handoff"])
    for cand in r["shortlist"]:
        check(cand["close_T"] <= 5.0, f"{cand['ticker']} respeita o tecto de preço da caça")
        check(cand.get("float_shares") is None or cand["float_shares"] <= 10_000_000,
              f"{cand['ticker']} respeita o tecto de float")
    check(all("motivos_rejeicao" in x or x.get("error") for x in r["rejeitados"]),
          "cada rejeitado traz o motivo explícito")


def t_modo_anual():
    r = run_cli(["--date", DATE_T, "--lag", "252", "--threshold", "300", "--no-ledger"])
    check(r["lag_sessions"] == 252 and r["threshold_pct"] == 300.0, "modo anual parametrizado")
    check(r["date_T_lag"] == CAL[-253], "T-252 resolvido no calendário de sessões")
    check(isinstance(r["cohort_bull"], list), "coorte devolvida (vazia é resultado válido)")


def t_chartbook_cli(tmp="/tmp/estudo20_cli_chartbook.html"):
    r = run_cli(["--date", DATE_T, "--no-ledger", "--chartbook", tmp])
    check(r.get("chartbook") == tmp and "chartbook_error" not in r,
          "chart book gerado pelo CLI", str(r.get("chartbook_error")))
    html = open(tmp).read()
    check("base64" in html and "BIOX" in html, "chart book contém os painéis da coorte")


def t_data_ajustada():
    r = run_cli(["--date", "2026-07-26", "--no-ledger"])  # sábado
    check(r["date_T"] == DATE_T and r["data_ajustada"] is True,
          "data de fim-de-semana recua para a sessão real e declara-o")


def main():
    patch()
    for fn in (t_modo_estudo, t_coorte_sub5, t_modo_caca, t_modo_anual,
               t_chartbook_cli, t_data_ajustada):
        print(f"\n--- {fn.__name__} ---")
        fn()
    print("\n" + "=" * 60)
    if FAILS:
        print(f"FALHARAM {len(FAILS)}: " + "; ".join(FAILS))
        sys.exit(1)
    print("Pipeline offline: todos os testes passaram.")


if __name__ == "__main__":
    main()
