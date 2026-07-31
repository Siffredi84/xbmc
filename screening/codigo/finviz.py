"""
Extractor Finviz robusto.

Causa do bug anterior: na coluna Ticker, o Finviz injecta um placeholder de logo
    <a class="company-ticker" style="--logo-url: url(...)"><img .../><span>A</span></a>
    <a class="tab-link">ABOS</a>
O <span> contem a INICIAL do ticker (fallback visual do logo). pandas.read_html
concatena todo o texto da <td> -> "A" + "ABOS" = "AABOS".

Correccao: nunca ler o ticker do texto da celula. Ler de data-boxover-ticker
(atributo), com fallback para href="stock?t=...". As restantes colunas nao sao
afectadas e podem vir do read_html.
"""
import io, re, time, sys
import requests, pandas as pd
from bs4 import BeautifulSoup

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")
BASE = "https://finviz.com/screener.ashx"
VIEWS = {"overview": 111, "performance": 141, "technical": 171}
TICKER_RE = re.compile(r"^[A-Z]{1,5}(?:[.-][A-Z])?$")


class TickerIntegrityError(RuntimeError):
    """Fail-closed: levantada quando a identidade dos tickers nao e validavel."""


def _session():
    s = requests.Session()
    s.headers.update({"User-Agent": UA, "Accept": "text/html"})
    return s


def _tickers_from_html(html: str) -> list[str]:
    """Fonte de verdade do ticker: atributos, nunca texto de celula."""
    soup = BeautifulSoup(html, "lxml")
    out = []
    for tr in soup.find_all("tr"):
        td = tr.find("td", attrs={"data-boxover-ticker": True})
        if td:
            out.append(td["data-boxover-ticker"].strip().upper())
            continue
        a = tr.find("a", href=re.compile(r"(?:stock|quote\.ashx)\?t="))
        if a:
            m = re.search(r"[?&]t=([A-Za-z.\-]+)", a["href"])
            if m:
                out.append(m.group(1).strip().upper())
    return out


def _companies_from_html(html: str) -> list[str]:
    soup = BeautifulSoup(html, "lxml")
    return [td.get("data-boxover-company", "").strip()
            for td in soup.find_all("td", attrs={"data-boxover-ticker": True})]



def _parse_table(html: str) -> pd.DataFrame:
    """Parser proprio: cabecalhos dos <th>, celulas dos <td>.
    O ticker NUNCA vem do texto da celula (contaminado pelo <span> do logo)."""
    soup = BeautifulSoup(html, "lxml")
    tbl = None
    cands = soup.select("table.screener_table") or soup.find_all("table")
    for cand in reversed(cands):
        ths = [th.get_text(strip=True) for th in cand.find_all("th")]
        if any(h.startswith("Ticker") for h in ths):
            tbl = cand
            headers = [re.sub(r"\s+", " ", h).strip() for h in ths]
            break
    if tbl is None:
        raise ValueError("tabela do screener ausente (anti-bot ou HTML alterado?)")
    rows = []
    for tr in tbl.find_all("tr"):
        td_t = tr.find("td", attrs={"data-boxover-ticker": True}, recursive=False)
        if not td_t:
            continue
        cells = [td.get_text(" ", strip=True) for td in tr.find_all("td", recursive=False)]
        if len(cells) != len(headers):
            raise TickerIntegrityError(
                f"desalinhamento de colunas: {len(cells)} celulas vs {len(headers)} cabecalhos")
        rec = dict(zip(headers, cells))
        rec["Ticker"] = td_t["data-boxover-ticker"].strip().upper()
        rec["FinvizCompany"] = td_t.get("data-boxover-company", "").strip()
        rows.append(rec)
    df = pd.DataFrame(rows)
    for col in ("Price", "Change", "Volume", "Avg Volume", "Rel Volume", "RSI",
                "SMA20", "SMA50", "SMA200", "52W High", "52W Low", "ATR", "Gap"):
        if col in df.columns:
            df[col] = (df[col].astype(str).str.replace("%", "", regex=False)
                       .str.replace(",", "", regex=False)
                       .str.replace(r"([\d.]+)M$", lambda m: str(float(m.group(1)) * 1e6), regex=True)
                       .str.replace(r"([\d.]+)K$", lambda m: str(float(m.group(1)) * 1e3), regex=True)
                       .str.replace(r"([\d.]+)B$", lambda m: str(float(m.group(1)) * 1e9), regex=True))
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df

def fetch_page(sess, view: int, filters: str, row: int, retries: int = 3):
    url = f"{BASE}?v={view}&f={filters}&r={row}"
    for _ in range(retries):
        try:
            html = sess.get(url, timeout=40).text
            df = _parse_table(html)
            return df, html
        except TickerIntegrityError:
            raise
        except Exception as e:
            print(f"  retry v={view} r={row}: {e}", file=sys.stderr)
            time.sleep(4)
    return None, None


def scrape(filters: str, views: dict = VIEWS, max_rows: int = 2000, pause: float = 1.5):
    sess = _session()
    frames, companies = {}, {}
    for name, v in views.items():
        parts, r = [], 1
        while r <= max_rows:
            df, html = fetch_page(sess, v, filters, r)
            if df is None or df.empty:
                break
            parts.append(df)
            if name == "overview":
                companies.update(dict(zip(df["Ticker"], df["FinvizCompany"])))
            if len(df) < 20:
                break
            r += 20
            time.sleep(pause)
        frames[name] = pd.concat(parts, ignore_index=True).drop_duplicates(subset=["Ticker"])
        print(f"  {name}: {len(frames[name])} linhas", file=sys.stderr)

    m = frames["overview"]
    for name in views:
        if name == "overview":
            continue
        d = frames[name]
        new = ["Ticker"] + [c for c in d.columns if c not in m.columns]
        m = m.merge(d[new], on="Ticker", how="left")
    m["FinvizCompany"] = m["Ticker"].map(companies)
    return m
