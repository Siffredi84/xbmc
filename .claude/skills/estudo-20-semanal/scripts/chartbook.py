#!/usr/bin/env python3
"""
chartbook.py — o livro de gráficos do estudo-20-semanal

A fonte insiste em imprimir centenas de gráficos e estudá-los todos os dias
("mantinha livros de gráficos no carro"). Este é o equivalente digital: um
painel por vencedor, num único HTML sem dependências externas (PNGs em
base64), publicável como Artifact para rever no telemóvel.

Cada painel mostra o que o estudo pede que se veja, não decoração:
  · preço dos últimos ~6 meses + volume
  · dia da origem (o registo de 4%) marcado com seta e linha vertical
  · zona de consolidação sombreada antes da origem
  · banda do range de 52 semanas com a posição na véspera da origem
  · caixa de metadados: preço, float, reverse split, pos52, flags Three-Lynch
"""

import base64
import io
from datetime import datetime

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402


def _fmt_float(v):
    if v is None:
        return "n/d"
    if v >= 1e9:
        return f"{v / 1e9:.2f}B"
    if v >= 1e6:
        return f"{v / 1e6:.1f}M"
    if v >= 1e3:
        return f"{v / 1e3:.0f}k"
    return f"{v:.0f}"


def _flag(v, yes="sim", no="não"):
    return "n/d" if v is None else (yes if v else no)


def panel_png(rec: dict, df: pd.DataFrame, window: int = 130) -> str | None:
    """Um painel -> PNG base64. Devolve None se não houver dados utilizáveis."""
    if df is None or df.empty:
        return None
    end = pd.Timestamp(rec["date"])
    df = df[df.index <= end + pd.Timedelta(days=8)].tail(window)
    if len(df) < 20:
        return None

    fig, (ax, axv) = plt.subplots(
        2, 1, figsize=(9, 5.2), sharex=True,
        gridspec_kw={"height_ratios": [3, 1], "hspace": 0.06},
    )

    ax.plot(df.index, df["Close"], lw=1.4, color="#1f77b4")
    ax.fill_between(df.index, df["Low"], df["High"], color="#1f77b4", alpha=0.12, lw=0)

    origin = rec.get("origin_date")
    if origin:
        o_ts = pd.Timestamp(origin)
        if o_ts in df.index:
            o_price = float(df.loc[o_ts, "Close"])
            ax.axvline(o_ts, color="#d62728", lw=1.1, ls="--", alpha=0.9)
            # acima-à-esquerda: por baixo o rótulo cai fora dos eixos e é cortado
            ax.annotate(
                f"registo 4%\n{rec.get('origin_pct')}%",
                xy=(o_ts, o_price),
                xytext=(-78, 40), textcoords="offset points", fontsize=8, color="#d62728",
                ha="center", annotation_clip=False,
                bbox={"boxstyle": "round,pad=0.25", "fc": "white", "ec": "#d62728", "alpha": 0.85, "lw": 0.6},
                arrowprops={"arrowstyle": "->", "color": "#d62728", "lw": 1.1},
            )
            cons = rec.get("consolidation_days")
            if cons:
                start = df.index[max(0, df.index.get_loc(o_ts) - int(cons))]
                ax.axvspan(start, o_ts, color="#ff7f0e", alpha=0.10, lw=0)

    hi52, lo52 = rec.get("high_52w"), rec.get("low_52w")
    if hi52 and lo52:
        ax.axhline(hi52, color="#7f7f7f", lw=0.8, ls=":")
        ax.axhline(lo52, color="#7f7f7f", lw=0.8, ls=":")
        ax.text(df.index[0], hi52, " máx 52s", fontsize=7, color="#7f7f7f", va="bottom")
        ax.text(df.index[0], lo52, " mín 52s", fontsize=7, color="#7f7f7f", va="top")

    side = "▲" if rec.get("side") == "bull" else "▼"
    ax.set_title(f"{side} {rec['ticker']} · {rec.get('pct_move')}% em {rec.get('date')}",
                 fontsize=11, loc="left", weight="bold")
    ax.grid(alpha=0.18)
    ax.set_ylabel("preço ($)", fontsize=8)
    ax.tick_params(labelsize=7)

    colors = ["#2ca02c" if c >= o else "#d62728"
              for c, o in zip(df["Close"], df["Open"])]
    axv.bar(df.index, df["Volume"], color=colors, width=1.0, alpha=0.6)
    axv.set_ylabel("volume", fontsize=8)
    axv.grid(alpha=0.18)
    axv.tick_params(labelsize=7)

    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=110, bbox_inches="tight")
    plt.close(fig)
    return base64.b64encode(buf.getvalue()).decode()


def _meta_rows(rec: dict) -> str:
    pos = rec.get("pos52_at_origin")
    pos_txt = "n/d" if pos is None else f"{pos:.2f} ({'terço inferior' if pos < 0.33 else 'terço superior' if pos > 0.66 else 'meio'})"
    items = [
        ("preço na origem", f"${rec.get('price_at_origin')}" if rec.get("price_at_origin") else "n/d"),
        ("pos. no range 52s", pos_txt),
        ("float", _fmt_float(rec.get("float_shares")) + f" [{rec.get('float_quality', 'n/d')}]"),
        ("reverse split 12m", _flag(rec.get("reverse_split_12m")) +
         (f" (1:{round(1 / rec['reverse_split_ratio'])})" if rec.get("reverse_split_ratio") else "")),
        ("ret 20d antes", f"{rec.get('ret20_before')}%" if rec.get("ret20_before") is not None else "n/d"),
        ("consolidação", f"{rec.get('consolidation_days')}d" if rec.get("consolidation_days") else "n/d"),
        ("gap na origem", f"{rec.get('origin_gap_pct')}%" if rec.get("origin_gap_pct") is not None else "n/d"),
        ("vol vs 20d", f"{rec.get('origin_vol_ratio')}x" if rec.get("origin_vol_ratio") else "n/d"),
        ("dia seguinte", f"{rec.get('next_day_ret')}%" if rec.get("next_day_ret") is not None else "n/d"),
        ("sector", rec.get("sector") or "n/d"),
    ]
    tl = [
        ("não subiu 3d", rec.get("tl_not_up_3")),
        ("dia prévio -/inside", rec.get("tl_prev_narrow_or_down")),
        ("fecho perto do máx", rec.get("tl_close_near_high")),
    ]
    cells = "".join(f"<div><span>{k}</span><b>{v}</b></div>" for k, v in items)
    chips = "".join(
        f"<em class='{'ok' if v else 'no' if v is not None else 'nd'}'>{k}: {_flag(v, '✓', '✗')}</em>"
        for k, v in tl)
    r2 = rec.get("tl_linearity_r2")
    if r2 is not None:
        chips += f"<em class='nd'>R² 1.º tramo: {r2}</em>"
    return f"<div class='meta'>{cells}</div><div class='chips'>{chips}</div>"


def build(result: dict, hist: dict, out_path: str, max_panels: int = 20) -> str:
    recs = [r for r in result.get("cohort_bull", []) if not r.get("error")][:max_panels]
    blocks = []
    for rec in recs:
        png = panel_png(rec, hist.get(rec["ticker"]))
        if not png:
            continue
        blocks.append(
            f"<section><img src='data:image/png;base64,{png}' alt='{rec['ticker']}'/>"
            f"{_meta_rows(rec)}</section>"
        )

    hyp = result.get("hipoteses", {})
    hyp_rows = "".join(
        f"<tr><td>{k.split('_')[0]}</td><td>{v.get('afirmacao', '')}</td>"
        f"<td class='v'>{v.get('veredicto', '')}</td><td>{v.get('n', v.get('n_bull', ''))}</td></tr>"
        for k, v in hyp.items())

    f = result.get("funnel", {})
    html = f"""<!doctype html><html lang="pt"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Chart book · movers {result.get('date_T')}</title>
<style>
:root{{color-scheme:light dark}}
body{{font:14px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;margin:0;padding:24px;
background:#fafafa;color:#1a1a1a;max-width:1000px;margin-inline:auto}}
h1{{font-size:20px;margin:0 0 4px}} h2{{font-size:15px;margin:28px 0 8px}}
.sub{{color:#666;font-size:12px;margin-bottom:18px}}
section{{background:#fff;border:1px solid #e3e3e3;border-radius:10px;padding:14px;margin-bottom:18px}}
img{{width:100%;height:auto;display:block}}
.meta{{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:6px 14px;margin-top:10px;font-size:12px}}
.meta span{{color:#777;display:block;font-size:11px}} .meta b{{font-weight:600}}
.chips{{margin-top:10px;display:flex;flex-wrap:wrap;gap:6px}}
.chips em{{font-style:normal;font-size:11px;padding:2px 8px;border-radius:20px;background:#eee}}
.chips .ok{{background:#e3f5e6;color:#17692a}} .chips .no{{background:#fdeaea;color:#9c1f1f}}
table{{border-collapse:collapse;width:100%;font-size:12px;background:#fff;border:1px solid #e3e3e3;border-radius:10px;overflow:hidden}}
td,th{{padding:7px 10px;border-bottom:1px solid #eee;text-align:left;vertical-align:top}}
.v{{font-weight:600;white-space:nowrap}}
.funnel{{font-size:12px;color:#555;background:#fff;border:1px solid #e3e3e3;border-radius:10px;padding:12px}}
@media (prefers-color-scheme:dark){{
body{{background:#141414;color:#e8e8e8}} section,table,.funnel{{background:#1e1e1e;border-color:#333}}
.meta span,.sub,.funnel{{color:#9a9a9a}} td,th{{border-color:#2c2c2c}} .chips em{{background:#2a2a2a}}
.chips .ok{{background:#16351c;color:#7bd68d}} .chips .no{{background:#3a1b1b;color:#e58c8c}}}}
</style></head><body>
<h1>Chart book · movers de {result.get('threshold_pct')}% em {result.get('lag_sessions')} sessões</h1>
<div class="sub">T = {result.get('date_T')} · comparado com {result.get('date_T_lag')} ·
gerado {datetime.now():%Y-%m-%d %H:%M} · {len(blocks)} painéis</div>
<div class="funnel">Funil: universo {f.get('universo_T', '?')} → liquidez {f.get('liquidez', '?')}
→ tipo {f.get('tipo_ADR_CS_ETF', 'sem filtro')} → <b>{f.get('bull', 0)} bull</b> / <b>{f.get('bear', 0)} bear</b></div>
<h2>Hipóteses da fonte, testadas nesta coorte</h2>
<table><tr><th>#</th><th>Afirmação</th><th>Veredicto</th><th>n</th></tr>{hyp_rows}</table>
<h2>Painéis</h2>
{''.join(blocks) or '<p>Sem painéis — nenhuma coorte com histórico utilizável.</p>'}
</body></html>"""

    with open(out_path, "w") as fh:
        fh.write(html)
    return out_path
