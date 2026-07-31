import json, os, sys, time
import requests

import config
CACHE = "pg_cache"; PACE = config.POLYGON_PACE_S
os.makedirs(CACHE, exist_ok=True)
S = requests.Session()

# D0-1: a chave era lida no import. Importar o modulo sem credenciais rebentava,
# o que impedia testar qualquer coisa a jusante sem uma chave real — incluindo
# leituras que so tocam na cache. A chave e agora exigida no momento em que uma
# chamada de rede vai mesmo acontecer.
def _chave():
    try:
        return os.environ["POLYGON_KEY"]
    except KeyError:
        raise RuntimeError("POLYGON_KEY nao definida: chamada de rede impossivel") from None

def _get(url, params, cache_path):
    if os.path.exists(cache_path):
        return json.load(open(cache_path))
    params = dict(params, apiKey=_chave())
    # N4: so havia retry em 429. Um 503 transitorio (comum neste fornecedor)
    # rebentava o pipeline inteiro a meio da descarga do universo.
    ultimo = None
    for tent in range(5):
        r = S.get(url, params=params, timeout=45)
        ultimo = r.status_code
        if r.status_code == 200:
            j = r.json()
            json.dump(j, open(cache_path, "w"))
            time.sleep(PACE)
            return j
        if r.status_code == 429:
            time.sleep(PACE * 2)
            continue
        if 500 <= r.status_code < 600:
            time.sleep(2 ** tent)
            continue
        r.raise_for_status()
    raise RuntimeError(f"falhou apos 5 tentativas ({ultimo}): {url}")

def trading_days(n, end="2026-07-28"):
    import datetime as dt
    d = dt.date.fromisoformat(end); out = []
    while len(out) < n:
        if d.weekday() < 5: out.append(d.isoformat())
        d -= dt.timedelta(days=1)
    return sorted(out)

def ultima_sessao_esperada(agora_utc=None):
    """Ultima sessao que ja fechou, em hora de Nova Iorque (UTC-4 no verao).
    Sem isto o pipeline usa a data fixa no codigo e faz screening sobre dados
    velhos sem qualquer aviso — corre bem hoje e silenciosamente mal amanha."""
    import datetime as dt
    agora = agora_utc or dt.datetime.now(dt.timezone.utc)
    et = agora - dt.timedelta(hours=4)
    d = et.date()
    if et.weekday() >= 5 or et.hour < 16 or (et.hour == 16 and et.minute < 15):
        d -= dt.timedelta(days=1)
    while d.weekday() >= 5:
        d -= dt.timedelta(days=1)
    return d.isoformat()


def guarda_calendario(dias_em_cache, esperada=None, max_recuo=5):
    """Confirma que a ultima sessao com dados e a ultima sessao fechada.
    Feriados sao aceites: recua enquanto a data esperada nao tiver negociacao.
    Devolve (ok, esperada_efetiva, detalhe)."""
    import datetime as dt
    esperada = esperada or ultima_sessao_esperada()
    tem = set(dias_em_cache)
    d = dt.date.fromisoformat(esperada)
    for _ in range(max_recuo):
        alvo = d.isoformat()
        if alvo in tem:
            ultima = max(tem)
            if ultima == alvo:
                return True, alvo, "cache alinhada com o calendario"
            return False, alvo, f"cache termina em {ultima}, esperado {alvo}"
        # data ausente da cache: pode ser feriado ou pode faltar mesmo
        j = _get(f"https://api.polygon.io/v2/aggs/grouped/locale/us/market/stocks/{alvo}",
                 {"adjusted": "true"}, f"{CACHE}/g_{alvo}.json")
        if j.get("results"):
            return False, alvo, f"sessao {alvo} existe mas nao estava na cache"
        d -= dt.timedelta(days=1)
        while d.weekday() >= 5:
            d -= dt.timedelta(days=1)
    return False, esperada, "nao foi possivel resolver a ultima sessao"


def grouped(day):
    j = _get(f"https://api.polygon.io/v2/aggs/grouped/locale/us/market/stocks/{day}",
             {"adjusted": "true"}, f"{CACHE}/g_{day}.json")
    return j.get("results") or []

def reference():
    out, url = {}, "https://api.polygon.io/v3/reference/tickers"
    params = {"market": "stocks", "active": "true", "limit": 1000}; page = 0
    while url and page < 15:
        j = _get(url, params, f"{CACHE}/ref_{page}.json")
        for r in j.get("results", []):
            out[r["ticker"]] = {"type": r.get("type"), "exch": r.get("primary_exchange"),
                                "name": r.get("name")}
        url = j.get("next_url"); params = {}; page += 1
    return out


def reverse_splits(desde, ate, tickers=None):
    """Reverse splits executados no intervalo, indexados por ticker.

    Usa o endpoint de corporate actions do Polygon. A classificacao e feita
    tanto pelo campo ``adjustment_type`` como pela razao, para tolerar o schema
    antigo ainda devolvido por `/v3/reference/splits`.
    """
    alvo = set(tickers) if tickers is not None else None
    out, page = {}, 0
    url = "https://api.polygon.io/v3/reference/splits"
    params = {
        "execution_date.gte": desde,
        "execution_date.lte": ate,
        "limit": 1000,
        "sort": "execution_date",
        "order": "desc",
    }
    while url:
        j = _get(url, params, f"{CACHE}/splits_{desde}_{ate}_{page}.json")
        for r in j.get("results", []):
            ticker = r.get("ticker")
            if not ticker or (alvo is not None and ticker not in alvo):
                continue
            tipo = r.get("adjustment_type")
            de, para = r.get("split_from"), r.get("split_to")
            por_razao = (isinstance(de, (int, float)) and
                         isinstance(para, (int, float)) and para < de)
            if tipo == "reverse_split" or por_razao:
                out.setdefault(ticker, []).append({
                    "execution_date": r.get("execution_date"),
                    "split_from": de,
                    "split_to": para,
                })
        url = j.get("next_url")
        params = {}
        page += 1
    for eventos in out.values():
        eventos.sort(key=lambda x: x.get("execution_date") or "", reverse=True)
    return out

if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else \
        int(config.JANELA_VOLUME * config.BUFFER_DIAS_UTEIS) + 4
    fim = ultima_sessao_esperada()
    days = trading_days(n, end=fim)
    print(f"ultima sessao fechada: {fim} | sessoes pedidas: {len(days)}", flush=True)
    ref = reference(); print(f"referencia: {len(ref)} tickers", flush=True)
    bars = {}
    for i, d in enumerate(days, 1):
        rs = grouped(d)
        if not rs: continue
        for r in rs:
            bars.setdefault(r["T"], []).append({"d": d,"c": r["c"],"h": r["h"],"l": r["l"],"v": r["v"]})
        print(f"  {i}/{len(days)} {d}: {len(rs)}", flush=True)
    dias = sorted({b["d"] for bs in bars.values() for b in bs})
    ok, alvo, det = guarda_calendario(dias, esperada=fim)
    print(f"guarda de calendario: {'OK' if ok else 'ALERTA'} — {det}", flush=True)
    if not ok:
        raise SystemExit("pipeline interrompido: dados desalinhados do calendario de mercado")
    json.dump({"bars": bars, "ref": ref, "ultima_sessao": alvo},
              open("pg_universe.json", "w"))
    print("OK", len(bars), "tickers")
