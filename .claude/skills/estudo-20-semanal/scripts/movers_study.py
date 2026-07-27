#!/usr/bin/env python3
"""
movers_study.py — estudo-20-semanal v1.0

Screener + anatomia + teste de hipóteses sobre o estudo diário descrito em
"How to study 20% plus winners in a week": todos os dias, listar as ações
que se moveram >=20% em 5 sessões (bull E bear), dissecar de onde partiu
cada movimento, e converter cada afirmação da fonte numa hipótese testada
com números — em vez de a aceitar por autoridade.

RESPONDE A UMA PERGUNTA DIFERENTE dos skills irmãos:
  breakout-quality-gate     -> "este breakout, neste ticker, é limpo?"
  breakout-market-scanner   -> "que breakouts há hoje no mercado?"
  ESTE                      -> "o que têm em comum os vencedores da semana,
                                e as regras que me vendem sobrevivem aos dados?"

UM MOTOR, TRÊS MODOS (estudo semanal e anual são o mesmo cálculo com outro lag):
  A. estudo (default)  --lag 5   --threshold 20    -> coortes bull e bear
  B. caça 4%           --modo caca                 -> screener forward do dia
  C. estudo anual      --lag 252 --threshold 300   -> movimentos de 300%+/ano

STANDALONE POR DESENHO: não importa nem depende de nenhum outro skill —
mesma regra da v1.1 do breakout-market-scanner. A lógica partilhada
(R² de linearidade, flags tipo C1/C2/C4, helpers de GitHub) está duplicada
aqui, não importada. Trade-off consciente: independência total contra
sincronização manual se um dia calibrares os irmãos.

ASSUNÇÕES DECLARADAS (D1-D8, ver SKILL.md para o racional completo):
  D1. Volume >= 100k aplicado ao dia T (a fonte não diz se é média).
  D2. Origem do movimento = primeiro dia com variação close-to-close >= +4%
      (<= -4% no bear) cuja subida acumulada até T cobre >= 75% do threshold.
      A fonte descreve o conceito ("registo de 4%"), não o algoritmo.
  D3. Float do yfinance é o melhor proxy gratuito; a fonte usa MarketSmith.
      Cross-check com Polygon -> float_quality HIGH/MEDIUM/LOW, nunca escondido.
  D4. Tipos Polygon CS/ADRC/ADRP/ADRR/ETF/ETV == "ADRs, common US e ETFs".
  D5. pos52 medido na VÉSPERA da origem, não em T — medir em T seria circular
      (depois de subir 20% está sempre perto do máximo).
  D6. Biotech classificado por sector/industry do yfinance.
  D7. Reverse split relevante = últimos 12 meses.
  D8. A fonte filtra >$5 mas conclui "quanto mais baixo o preço, melhor" — H1
      nasce truncada. Default fiel à fonte; --coorte-sub5 corre $1-$5 em
      paralelo para testar H1 em toda a amplitude.

Uso:
  python3 movers_study.py --date 2026-07-24
  python3 movers_study.py --date 2026-07-24 --coorte-sub5 --chartbook /tmp/cb.html
  python3 movers_study.py --modo caca --date 2026-07-24
  python3 movers_study.py --lag 252 --threshold 300 --date 2026-07-24
  python3 movers_study.py --rebuild-stats
"""

import argparse
import base64
import csv
import io
import json
import os
import sys
import time
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
import requests
import yfinance as yf

GITHUB_OWNER = "Siffredi84"
GITHUB_REPO = "breakout-pipeline-data"
LEDGER_PATH = "study_ledger.csv"

CACHE_DIR = os.path.expanduser("~/.cache/estudo-20")
KEYS_FILE = os.path.expanduser("~/.claude/estudo20-keys.json")
TYPES_CACHE = os.path.join(CACHE_DIR, "universe_types.json")
# D4 — "ADRs, ações comuns norte-americanas e ETFs" da fonte.
KEEP_TYPES = {"CS", "ADRC", "ADRP", "ADRR", "ETF", "ETV"}

LEDGER_FIELDS = [
    "date", "ticker", "side", "modo", "lag", "pct_move", "close_T", "volume_T",
    "origin_date", "origin_pct", "origin_gap_pct", "origin_vol_ratio", "days_origin_to_T",
    "no_4pct_origin", "price_at_origin", "pos52_at_origin", "ret20_before", "ret60_before",
    "consolidation_days", "float_shares", "float_quality", "shares_outstanding",
    "reverse_split_12m", "reverse_split_ratio", "sector", "industry", "is_biotech",
    "tl_not_up_3", "tl_prev_narrow_or_down", "tl_close_near_high", "tl_linearity_r2",
    "tl_trend_age_days", "next_day_ret", "mdd_5d_after",
]


def _json_default(o):
    if isinstance(o, (np.bool_,)):
        return bool(o)
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.floating,)):
        return float(o)
    if isinstance(o, (pd.Timestamp, datetime)):
        return o.strftime("%Y-%m-%d")
    raise TypeError(f"Object of type {o.__class__.__name__} is not JSON serializable")


def _f(x, nd=4):
    """float seguro: None em vez de NaN, arredondado."""
    try:
        if x is None:
            return None
        v = float(x)
        if not np.isfinite(v):
            return None
        return round(v, nd)
    except (TypeError, ValueError):
        return None


def last_probable_trading_day() -> str:
    d = datetime.now() - timedelta(days=1)
    while d.weekday() >= 5:
        d -= timedelta(days=1)
    return d.strftime("%Y-%m-%d")


def log(msg):
    print(msg, file=sys.stderr, flush=True)


def stored_key(name: str):
    """Chaves NUNCA vivem no código deste skill — ao contrário das irmãs, este
    ficheiro é versionado num repositório, e um PAT hardcoded aqui seria um
    segredo publicado. Ordem: variável de ambiente > ~/.claude/estudo20-keys.json
    (local, fora de qualquer repo). Ver "Setup" no SKILL.md."""
    v = os.environ.get(name)
    if v:
        return v
    try:
        with open(KEYS_FILE) as fh:
            return json.load(fh).get(name)
    except (OSError, json.JSONDecodeError):
        return None


# =====================================================================
# Calendário de sessões — 1 chamada grátis, resolve qualquer lag
# =====================================================================

def trading_calendar(end_date: str, sessions_needed: int) -> list:
    """Lista de dias de sessão até end_date (inclusive), via SPY no yfinance.

    Porquê SPY e não recuar dia-a-dia no Polygon: com --lag 252 o recuo
    dia-a-dia custaria 252 chamadas a uma API de 5/min. Uma única série do
    SPY dá o calendário NYSE exacto (feriados incluídos) de graça.
    """
    span = int(sessions_needed * 1.7) + 20
    start = (datetime.strptime(end_date, "%Y-%m-%d") - timedelta(days=span)).date()
    end = (datetime.strptime(end_date, "%Y-%m-%d") + timedelta(days=1)).date()
    spy = yf.download("SPY", start=start, end=end, progress=False, auto_adjust=False)
    if spy.empty:
        raise SystemExit("[ERRO] Não foi possível obter o calendário de sessões (SPY vazio).")
    idx = pd.to_datetime(spy.index).tz_localize(None).normalize()
    target = pd.Timestamp(end_date).normalize()
    return [d.strftime("%Y-%m-%d") for d in idx if d <= target]


def resolve_dates(end_date: str, lag: int):
    """(data_T, data_T-lag) — ambas sessões reais. Declara se T recuou."""
    cal = trading_calendar(end_date, lag + 10)
    if len(cal) < lag + 1:
        raise SystemExit(f"[ERRO] Calendário insuficiente para lag={lag} (só {len(cal)} sessões).")
    date_t, date_lag = cal[-1], cal[-1 - lag]
    adjusted = date_t != end_date
    return date_t, date_lag, adjusted, cal


# =====================================================================
# Estágio 0 — Universo e movers (2 chamadas Polygon, 0 por ticker)
# =====================================================================

def fetch_grouped(date_str: str, polygon_key: str) -> pd.DataFrame:
    r = requests.get(
        f"https://api.polygon.io/v2/aggs/grouped/locale/us/market/stocks/{date_str}",
        params={"apiKey": polygon_key, "adjusted": "true"},
        timeout=45,
    )
    data = r.json()
    if data.get("status") not in ("OK", "DELAYED") or not data.get("results"):
        raise SystemExit(
            f"[ERRO] Polygon grouped-daily falhou para {date_str}: "
            f"{data.get('status')} {data.get('message', '')}"
        )
    df = pd.DataFrame(data["results"])
    df = df.rename(columns={"T": "ticker", "o": "Open", "h": "High", "l": "Low", "c": "Close", "v": "Volume"})
    return df[["ticker", "Open", "High", "Low", "Close", "Volume"]]


def load_universe_types(polygon_key: str, refresh_days: int = 7, force: bool = False) -> dict:
    """ticker -> type, cacheado 7 dias. Free tier: 5 req/min, ~12 páginas."""
    if not force and os.path.exists(TYPES_CACHE):
        try:
            with open(TYPES_CACHE) as fh:
                blob = json.load(fh)
            age = datetime.now() - datetime.fromisoformat(blob["fetched"])
            if age.days < refresh_days and blob.get("types"):
                return blob["types"]
        except (json.JSONDecodeError, KeyError, ValueError):
            pass

    log("[i] Cache de tipos ausente/expirada — a paginar Polygon reference/tickers (~2-3 min, 5/min).")
    types, url = {}, "https://api.polygon.io/v3/reference/tickers"
    params = {"market": "stocks", "active": "true", "limit": 1000, "apiKey": polygon_key}
    pages = 0
    while url and pages < 30:
        r = requests.get(url, params=params if pages == 0 else {"apiKey": polygon_key}, timeout=45)
        if r.status_code == 429:
            time.sleep(15)
            continue
        data = r.json()
        for row in data.get("results", []) or []:
            if row.get("ticker"):
                types[row["ticker"]] = row.get("type") or "UNKNOWN"
        url = data.get("next_url")
        pages += 1
        if url:
            time.sleep(13)  # 5/min do tier gratuito
    if not types:
        return {}
    os.makedirs(CACHE_DIR, exist_ok=True)
    with open(TYPES_CACHE, "w") as fh:
        json.dump({"fetched": datetime.now().isoformat(), "types": types}, fh)
    log(f"[i] Cache de tipos gravada: {len(types)} tickers.")
    return types


def build_movers(df_t, df_lag, price_min, price_max, vol_min, threshold, types):
    """Merge das duas grouped -> coortes bull/bear + contadores do funil."""
    a = df_t.rename(columns={"Close": "close_T", "Volume": "volume_T", "Open": "open_T",
                             "High": "high_T", "Low": "low_T"})
    b = df_lag[["ticker", "Close"]].rename(columns={"Close": "close_lag"})
    m = a.merge(b, on="ticker", how="inner")
    funnel = {"universo_T": int(len(df_t)), "universo_lag": int(len(df_lag)), "merge": int(len(m))}

    m = m[(m["close_T"] >= price_min) & (m["close_T"] <= price_max) & (m["volume_T"] >= vol_min)]
    funnel["liquidez"] = int(len(m))

    if types:
        m = m[m["ticker"].map(lambda t: types.get(t, "UNKNOWN") in KEEP_TYPES)]
        funnel["tipo_ADR_CS_ETF"] = int(len(m))
    else:
        funnel["tipo_ADR_CS_ETF"] = None  # [ASSUNÇÃO] universo não tipificado

    m = m[m["close_lag"] > 0].copy()
    # round(6): sem isto, 12.0/10.0-1 = 19.999999999999996 e um mover
    # exactamente no threshold cai fora do scan em silêncio.
    m["pct_move"] = ((m["close_T"] / m["close_lag"] - 1) * 100).round(6)

    bull = m[m["pct_move"] >= threshold].sort_values("pct_move", ascending=False)
    bear = m[m["pct_move"] <= -threshold].sort_values("pct_move")
    funnel["bull"] = int(len(bull))
    funnel["bear"] = int(len(bear))
    return bull, bear, funnel


# =====================================================================
# Estágio 1 — Anatomia de cada mover (yfinance, grátis)
# =====================================================================

def fetch_history_batch(tickers: list, date_t: str, sessions_needed: int) -> dict:
    """OHLCV + splits para todos os tickers. Batch primeiro, individual como
    fallback — o batch falha silenciosamente em tickers isolados."""
    if not tickers:
        return {}
    span = int(sessions_needed * 1.7) + 30
    start = (datetime.strptime(date_t, "%Y-%m-%d") - timedelta(days=span)).date()
    end = (datetime.strptime(date_t, "%Y-%m-%d") + timedelta(days=8)).date()
    out = {}
    try:
        raw = yf.download(tickers, start=start, end=end, progress=False, auto_adjust=False,
                          actions=True, group_by="ticker", threads=True)
    except Exception as exc:  # noqa: BLE001 — rede/parsing do yfinance
        log(f"[!] Batch yfinance falhou ({exc}); a cair para downloads individuais.")
        raw = None

    if raw is not None and not raw.empty:
        if isinstance(raw.columns, pd.MultiIndex):
            for t in tickers:
                if t in raw.columns.get_level_values(0):
                    df = raw[t].dropna(how="all")
                    if not df.empty:
                        out[t] = _normalize_hist(df)
        elif len(tickers) == 1:
            out[tickers[0]] = _normalize_hist(raw.dropna(how="all"))

    for t in tickers:
        if t not in out:
            try:
                df = yf.download(t, start=start, end=end, progress=False,
                                 auto_adjust=False, actions=True)
                if isinstance(df.columns, pd.MultiIndex):
                    df.columns = df.columns.get_level_values(0)
                if not df.empty:
                    out[t] = _normalize_hist(df)
            except Exception:  # noqa: BLE001
                continue
    return out


def _normalize_hist(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.index = pd.to_datetime(df.index).tz_localize(None).normalize()
    return df


def fetch_fundamentals(ticker: str) -> dict:
    """float/sector do yfinance (D3/D6). Falha -> None com flag, nunca inventado."""
    try:
        info = yf.Ticker(ticker).get_info()
    except Exception:  # noqa: BLE001
        return {"float_shares": None, "shares_outstanding": None, "sector": None,
                "industry": None, "info_error": True}
    return {
        "float_shares": info.get("floatShares"),
        "shares_outstanding": info.get("sharesOutstanding"),
        "sector": info.get("sector"),
        "industry": info.get("industry"),
        "info_error": False,
    }


def polygon_shares(ticker: str, polygon_key: str):
    try:
        r = requests.get(f"https://api.polygon.io/v3/reference/tickers/{ticker}",
                         params={"apiKey": polygon_key}, timeout=20)
        res = r.json().get("results") or {}
        return res.get("share_class_shares_outstanding") or res.get("weighted_shares_outstanding")
    except Exception:  # noqa: BLE001
        return None


def float_quality(yf_float, yf_shares, poly_shares):
    """D3 — a divergência entre fontes fica exposta, nunca escondida."""
    if yf_float is None:
        return "LOW"
    if poly_shares is None or not yf_shares:
        return "MEDIUM"
    try:
        diff = abs(float(yf_shares) - float(poly_shares)) / float(poly_shares)
    except (TypeError, ZeroDivisionError, ValueError):
        return "MEDIUM"
    return "HIGH" if diff <= 0.10 else "LOW"


def find_origin(df: pd.DataFrame, t_idx: int, lag: int, threshold: float,
                side: str, extra: int = 10, trigger: float = 4.0):
    """D2 — o "registo de 4%": primeiro dia >= +4% (bull) cuja subida
    acumulada até T cobre >= 75% do movimento total exigido."""
    closes = df["Close"].values
    lo = max(1, t_idx - lag - extra)
    need = 0.75 * threshold
    for i in range(lo, t_idx + 1):
        prev = closes[i - 1]
        if prev <= 0:
            continue
        day_pct = (closes[i] / prev - 1) * 100
        cum_pct = (closes[t_idx] / prev - 1) * 100
        if side == "bull" and day_pct >= trigger and cum_pct >= need:
            return i
        if side == "bear" and day_pct <= -trigger and cum_pct <= -need:
            return i
    return None


def pos_in_52w(df: pd.DataFrame, idx: int, window: int = 252):
    lo = max(0, idx - window)
    w = df.iloc[lo:idx + 1]
    if len(w) < 20:
        return None, None, None
    hi, low = float(w["High"].max()), float(w["Low"].min())
    close = float(df["Close"].iloc[idx])
    if hi == low:
        return None, hi, low
    return (close - low) / (hi - low), hi, low


def linearity_r2(df: pd.DataFrame, end_idx: int, lookback: int = 20):
    lo = max(0, end_idx - lookback)
    closes = df["Close"].iloc[lo:end_idx].values
    if len(closes) < 5:
        return None
    x = np.arange(len(closes))
    fitted = np.polyval(np.polyfit(x, closes, 1), x)
    ss_res = float(np.sum((closes - fitted) ** 2))
    ss_tot = float(np.sum((closes - np.mean(closes)) ** 2))
    return 1 - ss_res / ss_tot if ss_tot else 0.0


def three_lynch_flags(df: pd.DataFrame, idx: int):
    """As condições do setup "Three-Lynch" da fonte, medidas no dia da origem.
    Mapeiam 1:1 os C1/C2/C4/C5 do breakout-quality-gate (duplicadas, não
    importadas — ver docstring do módulo)."""
    out = {"tl_not_up_3": None, "tl_prev_narrow_or_down": None,
           "tl_close_near_high": None, "tl_linearity_r2": None, "tl_trend_age_days": None}
    if idx < 4 or idx >= len(df):
        return out
    c = df["Close"].values
    out["tl_not_up_3"] = not (c[idx - 1] > c[idx - 2] and c[idx - 2] > c[idx - 3])

    prev = idx - 1
    negative = bool(c[prev] < c[prev - 1])
    rng = float(df["High"].iloc[prev] - df["Low"].iloc[prev])
    narrow = bool(rng / c[prev] < 0.02) if c[prev] else False
    out["tl_prev_narrow_or_down"] = negative or narrow

    hi, lo_ = float(df["High"].iloc[idx]), float(df["Low"].iloc[idx])
    cl = float(df["Close"].iloc[idx])
    out["tl_close_near_high"] = True if hi == lo_ else bool((hi - cl) / (hi - lo_) <= 0.20)

    out["tl_linearity_r2"] = _f(linearity_r2(df, idx, 20), 3)

    lo_win = max(0, idx - 60)
    lows = df["Low"].iloc[lo_win:idx]
    if len(lows) > 5:
        out["tl_trend_age_days"] = int(idx - (lo_win + int(np.argmin(lows.values))))
    return out


def analyze_mover(ticker, side, row, df, date_t, lag, threshold, fundamentals, poly_shares_val):
    t_ts = pd.Timestamp(date_t)
    if t_ts not in df.index:
        # yfinance pode não ter a sessão (ticker suspenso/delisted nesse dia)
        return {"ticker": ticker, "side": side, "error": "data T ausente no histórico yfinance"}
    t_idx = int(df.index.get_loc(t_ts))
    if t_idx < 25:
        return {"ticker": ticker, "side": side, "error": "histórico insuficiente"}

    rec = {
        "ticker": ticker,
        "side": side,
        "date": date_t,
        "pct_move": _f(row["pct_move"], 2),
        "close_T": _f(row["close_T"], 4),
        "volume_T": int(row["volume_T"]),
    }

    o_idx = find_origin(df, t_idx, lag, threshold, side)
    rec["no_4pct_origin"] = o_idx is None

    ref_idx = o_idx if o_idx is not None else max(1, t_idx - lag)
    prev_idx = max(0, ref_idx - 1)

    if o_idx is not None:
        prev_close = float(df["Close"].iloc[o_idx - 1])
        rec["origin_date"] = df.index[o_idx].strftime("%Y-%m-%d")
        rec["origin_pct"] = _f((df["Close"].iloc[o_idx] / prev_close - 1) * 100, 2)
        rec["origin_gap_pct"] = _f((df["Open"].iloc[o_idx] / prev_close - 1) * 100, 2)
        avg20 = float(df["Volume"].iloc[max(0, o_idx - 20):o_idx].mean() or 0)
        rec["origin_vol_ratio"] = _f(df["Volume"].iloc[o_idx] / avg20, 2) if avg20 else None
        rec["days_origin_to_T"] = int(t_idx - o_idx)
    else:
        rec.update({"origin_date": None, "origin_pct": None, "origin_gap_pct": None,
                    "origin_vol_ratio": None, "days_origin_to_T": None})

    # D5 — posição/preço medidos na VÉSPERA da origem, nunca em T
    pos52, hi52, lo52 = pos_in_52w(df, prev_idx)
    rec["pos52_at_origin"] = _f(pos52, 3)
    rec["high_52w"] = _f(hi52, 4)
    rec["low_52w"] = _f(lo52, 4)
    rec["price_at_origin"] = _f(df["Close"].iloc[prev_idx], 4)

    for name, back in (("ret20_before", 20), ("ret60_before", 60)):
        j = prev_idx - back
        rec[name] = _f((df["Close"].iloc[prev_idx] / df["Close"].iloc[j] - 1) * 100, 2) if j >= 0 else None

    lo_win = max(0, ref_idx - 60)
    highs = df["High"].iloc[lo_win:ref_idx]
    rec["consolidation_days"] = int(ref_idx - (lo_win + int(np.argmax(highs.values)))) if len(highs) > 5 else None

    rec.update(three_lynch_flags(df, ref_idx))

    # Estrutura accionista (D3, D7)
    fs = fundamentals.get("float_shares")
    rec["float_shares"] = int(fs) if fs else None
    rec["shares_outstanding"] = int(fundamentals["shares_outstanding"]) if fundamentals.get("shares_outstanding") else None
    rec["float_quality"] = float_quality(fs, fundamentals.get("shares_outstanding"), poly_shares_val)
    rec["polygon_shares"] = int(poly_shares_val) if poly_shares_val else None
    rec["sector"] = fundamentals.get("sector")
    rec["industry"] = fundamentals.get("industry")
    text = f"{fundamentals.get('sector') or ''} {fundamentals.get('industry') or ''}".lower()
    rec["is_biotech"] = bool("biotech" in text or "drug" in text or "pharmac" in text)

    rec["reverse_split_12m"], rec["reverse_split_ratio"] = _reverse_split(df, t_ts)

    # Risco pós-movimento — "o dia seguinte pode ser perigoso"
    window = df.iloc[max(0, t_idx - lag):t_idx + 1]
    if len(window) > 1:
        rets = window["Close"].pct_change().abs()
        big_idx = int(df.index.get_loc(rets.idxmax()))
        rec["biggest_day"] = df.index[big_idx].strftime("%Y-%m-%d")
        if big_idx + 1 < len(df):
            rec["next_day_ret"] = _f((df["Close"].iloc[big_idx + 1] / df["Close"].iloc[big_idx] - 1) * 100, 2)
        else:
            rec["next_day_ret"] = None
    else:
        rec["biggest_day"], rec["next_day_ret"] = None, None

    after = df["Close"].iloc[t_idx + 1:t_idx + 6]
    if len(after) >= 2:
        base = float(df["Close"].iloc[t_idx])
        rec["mdd_5d_after"] = _f((float(after.min()) / base - 1) * 100, 2)
    else:
        rec["mdd_5d_after"] = None

    return rec


def _reverse_split(df: pd.DataFrame, t_ts: pd.Timestamp):
    """D7 — reverse split nos últimos 12 meses (rácio < 1 no yfinance)."""
    if "Stock Splits" not in df.columns:
        return None, None
    s = df["Stock Splits"]
    s = s[(s > 0) & (s < 1) & (s.index >= t_ts - pd.Timedelta(days=365)) & (s.index <= t_ts)]
    if s.empty:
        return False, None
    return True, _f(float(s.iloc[-1]), 6)


def run_anatomy(cohort_df, side, date_t, lag, threshold, polygon_key,
                max_names, fundamentals_on, sessions_needed):
    tickers = list(cohort_df["ticker"].head(max_names))
    if not tickers:
        return []
    log(f"[i] Anatomia {side}: {len(tickers)} tickers.")
    hist = fetch_history_batch(tickers, date_t, sessions_needed)
    records = []
    for _, row in cohort_df.head(max_names).iterrows():
        t = row["ticker"]
        df = hist.get(t)
        if df is None or df.empty:
            records.append({"ticker": t, "side": side, "error": "sem histórico yfinance"})
            continue
        fund = fetch_fundamentals(t) if fundamentals_on else {
            "float_shares": None, "shares_outstanding": None, "sector": None,
            "industry": None, "info_error": True}
        poly = polygon_shares(t, polygon_key) if (fundamentals_on and fund.get("float_shares")) else None
        try:
            records.append(analyze_mover(t, side, row, df, date_t, lag, threshold, fund, poly))
        except Exception as exc:  # noqa: BLE001 — um ticker mau não parte a corrida
            records.append({"ticker": t, "side": side, "error": f"anatomia falhou: {exc}"})
    return records


# =====================================================================
# Estágio 2 — Hipóteses: as afirmações da fonte, testadas
# =====================================================================

def _ranks(a: np.ndarray) -> np.ndarray:
    order = np.argsort(a, kind="mergesort")
    ranks = np.empty(len(a), dtype=float)
    ranks[order] = np.arange(1, len(a) + 1, dtype=float)
    # média nos empates
    vals = a[order]
    i = 0
    while i < len(vals):
        j = i
        while j + 1 < len(vals) and vals[j + 1] == vals[i]:
            j += 1
        if j > i:
            ranks[order[i:j + 1]] = np.mean(ranks[order[i:j + 1]])
        i = j + 1
    return ranks


def spearman(xs, ys):
    pairs = [(x, y) for x, y in zip(xs, ys) if x is not None and y is not None
             and np.isfinite(x) and np.isfinite(y)]
    if len(pairs) < 5:
        return None, len(pairs)
    x = _ranks(np.array([p[0] for p in pairs], dtype=float))
    y = _ranks(np.array([p[1] for p in pairs], dtype=float))
    sx, sy = x.std(), y.std()
    if sx == 0 or sy == 0:
        return None, len(pairs)
    return float(np.mean((x - x.mean()) * (y - y.mean()) / (sx * sy))), len(pairs)


def bucketize(records, field, edges, labels, value="pct_move"):
    out = []
    for lo, hi, lab in zip(edges[:-1], edges[1:], labels):
        vals = [abs(r[value]) for r in records
                if r.get(field) is not None and r.get(value) is not None and lo <= r[field] < hi]
        out.append({"bucket": lab, "n": len(vals),
                    "media_move_pct": _f(np.mean(vals), 2) if vals else None,
                    "mediana_move_pct": _f(np.median(vals), 2) if vals else None})
    return out


def _verdict(value, supports_when, threshold=0.15, small_n=False):
    """SUPORTA / CONTRARIA / INCONCLUSIVO — nunca 'confirmado'."""
    if value is None:
        return "SEM-DADOS"
    if supports_when == "negative":
        v = "SUPORTA" if value <= -threshold else ("CONTRARIA" if value >= threshold else "INCONCLUSIVO")
    else:
        v = "SUPORTA" if value >= threshold else ("CONTRARIA" if value <= -threshold else "INCONCLUSIVO")
    return v + (" [AMOSTRA-PEQUENA]" if small_n else "")


def test_hypotheses(bull, bear, funnel):
    ok = [r for r in bull if not r.get("error")]
    n = len(ok)
    small = n < 50
    tag = ["[AMOSTRA-PEQUENA]"] if small else []
    H = {}

    moves = [abs(r["pct_move"]) if r.get("pct_move") is not None else None for r in ok]
    rho, npairs = spearman([r.get("price_at_origin") for r in ok], moves)
    H["H1_preco_baixo_move_maior"] = {
        "afirmacao": "Quanto mais baixo o preço, maior o movimento",
        "spearman_preco_vs_move": _f(rho, 3), "n": npairs,
        "buckets": bucketize(ok, "price_at_origin", [0, 1, 3, 5, 10, 30, 1e9],
                             ["<$1", "$1-3", "$3-5", "$5-10", "$10-30", ">$30"]),
        "veredicto": _verdict(rho, "negative", small_n=small), "flags": tag,
    }

    pos = [r["pos52_at_origin"] for r in ok if r.get("pos52_at_origin") is not None]
    low_side = sum(1 for p in pos if p < 0.33)
    high_side = sum(1 for p in pos if p > 0.66)
    H["H2_parte_de_minimos_nao_maximos"] = {
        "afirmacao": "Os grandes movimentos partem de mínimos/consolidação, não de máximos de 52 semanas",
        "n": len(pos), "mediana_pos52": _f(np.median(pos), 3) if pos else None,
        "pct_terco_inferior": _f(100 * low_side / len(pos), 1) if pos else None,
        "pct_terco_superior": _f(100 * high_side / len(pos), 1) if pos else None,
        "veredicto": ("SUPORTA" if pos and low_side > high_side else
                      "CONTRARIA" if pos and high_side > low_side else "SEM-DADOS")
                     + (" [AMOSTRA-PEQUENA]" if small else ""),
        "flags": tag,
    }

    rho3, n3 = spearman([r.get("float_shares") for r in ok], moves)
    H["H3_float_baixo_mais_explosivo"] = {
        "afirmacao": "Quanto mais baixo o float, mais explosivo o movimento",
        "spearman_float_vs_move": _f(rho3, 3), "n": n3,
        "buckets": bucketize(ok, "float_shares", [0, 1e6, 3e6, 1e7, 5e7, 1e15],
                             ["<1M", "1-3M", "3-10M", "10-50M", ">50M"]),
        "veredicto": _verdict(rho3, "negative", small_n=small),
        "flags": tag + ["[D3] float do yfinance; ver float_quality por nome"],
    }

    rs = [r for r in ok if r.get("reverse_split_12m") is not None]
    rate = 100 * sum(1 for r in rs if r["reverse_split_12m"]) / len(rs) if rs else None
    H["H4_reverse_split_sobrerrepresentado"] = {
        "afirmacao": "Ações com reverse split recente e float residual dominam estes movimentos",
        "n": len(rs), "pct_coorte_com_reverse_split_12m": _f(rate, 1),
        "baseline_universo": funnel.get("baseline_reverse_split_pct"),
        "veredicto": ("SEM-BASELINE — correr com --baseline-sample N para comparar"
                      if funnel.get("baseline_reverse_split_pct") is None else
                      ("SUPORTA" if rate and rate > funnel["baseline_reverse_split_pct"] * 1.5 else "INCONCLUSIVO")),
        "flags": tag,
    }

    bio = [r for r in ok if r.get("is_biotech")]
    top_decile = ok[:max(1, n // 10)] if n else []
    gaps = [r["origin_gap_pct"] for r in bio if r.get("origin_gap_pct") is not None]
    H["H5_biotech_gap_continua"] = {
        "afirmacao": "Biotecnologia com catalisador abre em gap e continua a subir no mesmo dia",
        "n_biotech": len(bio), "pct_coorte_biotech": _f(100 * len(bio) / n, 1) if n else None,
        "pct_decil_topo_biotech": _f(100 * sum(1 for r in top_decile if r.get("is_biotech")) / len(top_decile), 1) if top_decile else None,
        "gap_mediano_biotech_pct": _f(np.median(gaps), 2) if gaps else None,
        "veredicto": "DESCRITIVO — comparar com a base rate do universo antes de concluir",
        "flags": tag,
    }

    nd = [r["next_day_ret"] for r in ok if r.get("next_day_ret") is not None]
    H["H6_dia_seguinte_perigoso"] = {
        "afirmacao": "No dia seguinte ao move de maior amplitude, o preço recua com frequência",
        "n": len(nd), "mediana_ret_D1_pct": _f(np.median(nd), 2) if nd else None,
        "pct_D1_negativos": _f(100 * sum(1 for x in nd if x < 0) / len(nd), 1) if nd else None,
        "veredicto": ("SUPORTA" if nd and np.median(nd) < 0 else
                      "CONTRARIA" if nd else "SEM-DADOS") + (" [AMOSTRA-PEQUENA]" if small else ""),
        "flags": tag,
    }

    with_origin = sum(1 for r in ok if not r.get("no_4pct_origin"))
    pct_origin = 100 * with_origin / n if n else None
    H["H7_registo_4pct_universal"] = {
        "afirmacao": "Todo o movimento de 20% contém pelo menos um dia de 4% (20/5=4)",
        "n": n, "pct_com_origem_4pct": _f(pct_origin, 1),
        "veredicto": ("SUPORTA" if pct_origin and pct_origin >= 80 else
                      "PARCIAL" if pct_origin and pct_origin >= 50 else
                      "CONTRARIA" if pct_origin is not None else "SEM-DADOS")
                     + (" [AMOSTRA-PEQUENA]" if small else ""),
        "flags": tag + ["[D2] definição operacional da origem"],
    }

    nb, nbe = funnel.get("bull", 0), funnel.get("bear", 0)
    H["H8_lado_comprador_domina"] = {
        "afirmacao": "O lado comprador oferece muito mais oportunidades que o vendedor",
        "n_bull": nb, "n_bear": nbe,
        "racio_bull_bear": _f(nb / nbe, 2) if nbe else None,
        "veredicto": "SUPORTA" if nb > nbe else ("CONTRARIA" if nbe > nb else "EMPATE"),
        "nota": "Leitura de regime, não lei — inverte-se em bear market (a própria fonte o diz).",
    }
    return H


def baseline_reverse_split(universe_df, sample_n, date_t):
    """Base rate de reverse split no universo, por amostragem — sem isto H4
    não tem termo de comparação e o skill não o esconde."""
    if sample_n <= 0 or universe_df.empty:
        return None
    sample = universe_df.sample(min(sample_n, len(universe_df)), random_state=42)
    hist = fetch_history_batch(list(sample["ticker"]), date_t, 260)
    hits = tot = 0
    t_ts = pd.Timestamp(date_t)
    for _, df in hist.items():
        rs, _r = _reverse_split(df, t_ts)
        if rs is None:
            continue
        tot += 1
        hits += int(rs)
    return _f(100 * hits / tot, 1) if tot else None


# =====================================================================
# Modo B — caça ao registo de 4% (forward, accionável hoje)
# =====================================================================

def run_hunt(bull, date_t, polygon_key, args):
    """Os filtros explícitos da fonte para a pesquisa de rutura dos 4%:
    preço baixo, float baixo, e a ação a vir de baixo (não estendida)."""
    cand = bull[bull["close_T"] <= args.hunt_price_max].head(args.hunt_max)
    log(f"[i] Caça 4%: {len(cand)} candidatos brutos (preço <= ${args.hunt_price_max}).")
    recs = run_anatomy(cand, "bull", date_t, 1, 4.0, polygon_key,
                       args.hunt_max, not args.no_fundamentals, 300)
    shortlist, rejeitados = [], []
    for r in recs:
        if r.get("error"):
            rejeitados.append({**r, "motivo": r["error"]})
            continue
        motivos = []
        if r.get("float_shares") and r["float_shares"] > args.hunt_float_max:
            motivos.append(f"float {r['float_shares']:,} > {args.hunt_float_max:,}")
        if r.get("float_shares") is None:
            motivos.append("float desconhecido [D3]")
        if r.get("ret20_before") is not None and r["ret20_before"] > 0:
            motivos.append(f"não vinha a cair (ret20 {r['ret20_before']}%)")
        if r.get("tl_not_up_3") is False:
            motivos.append("subiu 3 dias seguidos")
        (rejeitados if motivos else shortlist).append({**r, "motivos_rejeicao": motivos} if motivos else r)
    shortlist.sort(key=lambda r: (r.get("float_shares") or 1e15))
    return shortlist, rejeitados


# =====================================================================
# Estágio 3 — Ledger e arquivo no GitHub
# =====================================================================

def _gh_headers(token):
    return {"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json"}


def github_get_file(path, token):
    r = requests.get(f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/contents/{path}",
                     headers=_gh_headers(token), timeout=30)
    if r.status_code != 200:
        return None, None
    blob = r.json()
    return base64.b64decode(blob["content"]).decode("utf-8"), blob["sha"]


def github_put_file(path, content_str, message, token, sha=None):
    payload = {"message": message, "content": base64.b64encode(content_str.encode()).decode()}
    if sha:
        payload["sha"] = sha
    r = requests.put(f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/contents/{path}",
                     headers=_gh_headers(token), json=payload, timeout=30)
    return r.status_code in (200, 201)


def ledger_upsert_many(rows, token):
    """Upsert por (date, ticker, side). Cria o CSV com header se não existir —
    correcção face ao ledger_upsert do gate, que devolvia False em silêncio."""
    content, sha = github_get_file(LEDGER_PATH, token)
    existing = []
    if content:
        existing = list(csv.DictReader(io.StringIO(content)))
    index = {(r.get("date"), r.get("ticker"), r.get("side")): r for r in existing}
    for row in rows:
        key = (row.get("date"), row.get("ticker"), row.get("side"))
        clean = {k: ("" if row.get(k) is None else str(row.get(k))) for k in LEDGER_FIELDS}
        if key in index:
            index[key].update(clean)
        else:
            existing.append(clean)
            index[key] = clean
    out = io.StringIO()
    w = csv.DictWriter(out, fieldnames=LEDGER_FIELDS, extrasaction="ignore")
    w.writeheader()
    for r in existing:
        w.writerow({k: r.get(k, "") for k in LEDGER_FIELDS})
    return github_put_file(LEDGER_PATH, out.getvalue(),
                           f"Estudo 20%: {len(rows)} linhas", token, sha=sha)


def archive_json(subfolder, filename, obj, token):
    path = f"{subfolder}/{filename}"
    _, sha = github_get_file(path, token)
    return github_put_file(path, json.dumps(obj, indent=2, ensure_ascii=False, default=_json_default),
                           f"Archive: {path}", token, sha=sha)


def rebuild_stats(token):
    """Recomputa H1-H8 sobre o ledger acumulado inteiro — é isto que
    transforma 'seis semanas de estudo diário' em evidência."""
    content, _ = github_get_file(LEDGER_PATH, token)
    if not content:
        raise SystemExit("[ERRO] study_ledger.csv ainda não existe no repo de dados.")
    rows = list(csv.DictReader(io.StringIO(content)))
    num = {"pct_move", "price_at_origin", "pos52_at_origin", "float_shares", "next_day_ret",
           "ret20_before", "ret60_before", "origin_gap_pct", "mdd_5d_after"}
    recs = []
    for r in rows:
        rec = dict(r)
        for k in num:
            try:
                rec[k] = float(r[k]) if r.get(k) not in (None, "") else None
            except ValueError:
                rec[k] = None
        rec["no_4pct_origin"] = r.get("no_4pct_origin") == "True"
        rec["is_biotech"] = r.get("is_biotech") == "True"
        rec["reverse_split_12m"] = (r.get("reverse_split_12m") == "True") if r.get("reverse_split_12m") else None
        recs.append(rec)
    bull = [r for r in recs if r.get("side") == "bull"]
    bear = [r for r in recs if r.get("side") == "bear"]
    bull.sort(key=lambda r: -(r.get("pct_move") or 0))
    funnel = {"bull": len(bull), "bear": len(bear)}
    dates = sorted({r.get("date") for r in recs if r.get("date")})
    return {"modo": "rebuild-stats", "linhas_ledger": len(recs),
            "dias_de_estudo": len(dates), "primeiro_dia": dates[0] if dates else None,
            "ultimo_dia": dates[-1] if dates else None,
            "hipoteses_acumuladas": test_hypotheses(bull, bear, funnel)}


# =====================================================================
# main
# =====================================================================

def main():
    ap = argparse.ArgumentParser(description="Estudo diário de movers 20%/semana + teste de hipóteses")
    ap.add_argument("--date", default=None, help="YYYY-MM-DD (default: último dia provável de trading)")
    ap.add_argument("--modo", choices=["estudo", "caca"], default="estudo")
    ap.add_argument("--lag", type=int, default=5, help="Sessões de lookback (5=semana, 252=ano)")
    ap.add_argument("--threshold", type=float, default=20.0, help="Movimento mínimo em %%")
    ap.add_argument("--price-min", type=float, default=5.0)
    ap.add_argument("--price-max", type=float, default=100000.0)
    ap.add_argument("--volume-min", type=float, default=100_000)
    ap.add_argument("--max-names", type=int, default=60, help="Máx. tickers por coorte na anatomia")
    ap.add_argument("--coorte-sub5", action="store_true",
                    help="D8 — corre também a coorte $1-$5 excluída pela fonte")
    ap.add_argument("--baseline-sample", type=int, default=0,
                    help="Amostra do universo para a base rate de reverse split (H4)")
    ap.add_argument("--no-fundamentals", action="store_true", help="Salta float/sector (mais rápido)")
    ap.add_argument("--no-type-filter", action="store_true", help="Salta o filtro ADR/CS/ETF")
    ap.add_argument("--refresh-types", action="store_true", help="Força refresh da cache de tipos")
    ap.add_argument("--hunt-price-max", type=float, default=5.0)
    ap.add_argument("--hunt-float-max", type=float, default=10_000_000)
    ap.add_argument("--hunt-max", type=int, default=40)
    ap.add_argument("--chartbook", default=None, help="Caminho do HTML do chart book")
    ap.add_argument("--polygon-key", default=stored_key("POLYGON_API_KEY"))
    ap.add_argument("--github-token", default=stored_key("GITHUB_TOKEN"))
    ap.add_argument("--no-ledger", action="store_true")
    ap.add_argument("--rebuild-stats", action="store_true")
    ap.add_argument("--json", default=None)
    args = ap.parse_args()

    if args.rebuild_stats:
        if not args.github_token:
            raise SystemExit(_missing_key_msg("GITHUB_TOKEN"))
        result = rebuild_stats(args.github_token)
        _emit(result, args)
        return

    if not args.polygon_key:
        raise SystemExit(_missing_key_msg("POLYGON_API_KEY"))
    if not args.github_token and not args.no_ledger:
        log("[!] Sem GITHUB_TOKEN — a corrida faz-se, mas nada é gravado no ledger.")
        args.no_ledger = True

    lag = 1 if args.modo == "caca" else args.lag
    threshold = 4.0 if args.modo == "caca" else args.threshold
    price_min = 0.0 if args.modo == "caca" else args.price_min
    requested = args.date or last_probable_trading_day()

    date_t, date_lag, adjusted, _cal = resolve_dates(requested, lag)
    log(f"[i] T={date_t} · T-{lag}={date_lag}" + (f" (pedida {requested}, recuada para sessão real)" if adjusted else ""))

    df_t = fetch_grouped(date_t, args.polygon_key)
    df_lag = fetch_grouped(date_lag, args.polygon_key)
    types = {} if args.no_type_filter else load_universe_types(args.polygon_key, force=args.refresh_types)

    bull, bear, funnel = build_movers(df_t, df_lag, price_min, args.price_max,
                                      args.volume_min, threshold, types)
    log(f"[i] Funil: {funnel}")

    result = {
        "modo": args.modo, "date_T": date_t, "date_T_lag": date_lag, "lag_sessions": lag,
        "threshold_pct": threshold, "data_pedida": requested, "data_ajustada": adjusted,
        "filtros": {"price_min": price_min, "price_max": args.price_max,
                    "volume_min": args.volume_min,
                    "tipo": "ADR+CS+ETF" if types else "[ASSUNÇÃO] universo não tipificado"},
        "funnel": funnel,
    }

    if args.modo == "caca":
        shortlist, rejeitados = run_hunt(bull, date_t, args.polygon_key, args)
        result["shortlist"] = shortlist
        result["rejeitados"] = rejeitados
        result["handoff"] = ("Correr breakout-quality-gate sobre cada ticker da shortlist "
                             "(--breakout-date {date_T}) antes de qualquer decisão.")
        _emit(result, args)
        return

    if args.baseline_sample:
        universe_for_baseline = build_movers(df_t, df_lag, price_min, args.price_max,
                                             args.volume_min, 0.0, types)[0]
        funnel["baseline_reverse_split_pct"] = baseline_reverse_split(
            universe_for_baseline, args.baseline_sample, date_t)

    sessions_needed = lag + 300
    recs_bull = run_anatomy(bull, "bull", date_t, lag, threshold, args.polygon_key,
                            args.max_names, not args.no_fundamentals, sessions_needed)
    recs_bear = run_anatomy(bear, "bear", date_t, lag, threshold, args.polygon_key,
                            args.max_names, not args.no_fundamentals, sessions_needed)

    result["cohort_bull"] = recs_bull
    result["cohort_bear"] = recs_bear
    result["hipoteses"] = test_hypotheses(recs_bull, recs_bear, funnel)

    if args.coorte_sub5:  # D8
        b5, be5, f5 = build_movers(df_t, df_lag, 1.0, 5.0, args.volume_min, threshold, types)
        r5 = run_anatomy(b5, "bull", date_t, lag, threshold, args.polygon_key,
                         args.max_names, not args.no_fundamentals, sessions_needed)
        result["coorte_sub5"] = {
            "funnel": f5, "cohort_bull": r5,
            "hipoteses": test_hypotheses(r5, [], f5),
            "nota": "D8 — coorte $1-$5 que a fonte exclui do scan mas usa nas conclusões.",
        }

    if args.chartbook:
        try:
            sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
            import chartbook
            hist = fetch_history_batch([r["ticker"] for r in recs_bull if not r.get("error")][:20],
                                       date_t, sessions_needed)
            chartbook.build(result, hist, args.chartbook)
            result["chartbook"] = args.chartbook
            log(f"[i] Chart book: {args.chartbook}")
        except Exception as exc:  # noqa: BLE001 — chart book nunca deve partir o estudo
            result["chartbook_error"] = str(exc)
            log(f"[!] Chart book falhou: {exc}")

    if not args.no_ledger and args.github_token:
        rows = [{**r, "modo": args.modo, "lag": lag, "date": date_t}
                for r in recs_bull + recs_bear if not r.get("error")]
        ok_ledger = ledger_upsert_many(rows, args.github_token)
        ok_arch = archive_json("studies", f"{date_t}_{args.modo}_lag{lag}.json", result, args.github_token)
        result["ledger"] = {"linhas": len(rows), "ledger_ok": ok_ledger, "arquivo_ok": ok_arch}

    _emit(result, args)


def _missing_key_msg(name: str) -> str:
    return (f"[ERRO] {name} em falta. Exporta a variável de ambiente, ou cria "
            f"{KEYS_FILE} (local, nunca versionado) com:\n"
            f'  {{"POLYGON_API_KEY": "...", "GITHUB_TOKEN": "..."}}\n'
            f"São as mesmas chaves já usadas pelo breakout-quality-gate.")


def _emit(result, args):
    text = json.dumps(result, indent=2, ensure_ascii=False, default=_json_default)
    if args.json:
        with open(args.json, "w") as fh:
            fh.write(text)
        log(f"[i] JSON gravado em {args.json}")
    print(text)


if __name__ == "__main__":
    main()
