#!/usr/bin/env python3
"""
Proxy de valor — a medição que o motor fazia à mão, ticker a ticker.

Porquê existe: a regra 4 do arquivo manda registar, em cada corrida, o fecho mais
recente de cada cartão entregue e do benchmark. Feito à mão, falhou: na corrida de
05/08/2026 o preço do Ibiden ficou por obter, e o arquivo já regista uma divergência
de fornecedor (FORM $110,21 arquivado vs $107,11 numa série posterior) que obrigou à
nota "manter fonte consistente daqui em diante". Este coletor é essa consistência.

O que mede: retorno de cada cartão desde a data de ENTREGA (não desde o início do
ano, não desde a compra — não há compra: a fronteira descoberta≠execução mantém-se),
contra o seu benchmark na mesma janela. A diferença é o excesso.

O que NÃO é: isto não avalia teses. Um cartão pode estar em queda com a tese intacta
— a distinção entre as duas curvas (preço e industrial) é o coração do método, e a
curva industrial vive nos invalidadores, não aqui. O preço é uma das duas curvas,
lida em separado e sem timing.

Fonte: Twelve Data (primária, uma só fonte para toda a série) com Polygon de reserva.
Chaves em TWELVEDATA_API_KEY / POLYGON_API_KEY.

Uso:  python3 coletar_precos.py            # retrato de hoje
      python3 coletar_precos.py --desde 2026-07-01
"""
import argparse, json, os, sys, time, urllib.error, urllib.request
from datetime import date, datetime, timedelta
from pathlib import Path

BASE = Path(__file__).parent
SNAPS = BASE / 'snapshots'
CARTEIRA = BASE / 'carteira.json'
UA = {'User-Agent': 'Mozilla/5.0'}


def _json(url, tentativas=3):
    for i in range(tentativas):
        try:
            return json.load(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30))
        except urllib.error.HTTPError as e:
            return {'_http': e.code}
        except Exception:
            if i == tentativas - 1:
                return {'_err': 'rede'}
            time.sleep(2 ** i)
    return {'_err': 'rede'}


def serie_twelvedata(ticker, desde, exchange=None):
    k = os.environ.get('TWELVEDATA_API_KEY')
    if not k:
        return None, {}
    dias = (date.today() - desde).days + 10
    ex = f'&exchange={exchange}' if exchange else ''
    r = _json(f'https://api.twelvedata.com/time_series?symbol={ticker}&interval=1day'
              f'&outputsize={min(dias, 5000)}{ex}&apikey={k}')
    if not r.get('values'):
        return None, {}
    return {v['datetime']: float(v['close']) for v in r['values']}, (r.get('meta') or {})


def serie_polygon(ticker, desde):
    k = os.environ.get('POLYGON_API_KEY')
    if not k:
        return None, {}
    r = _json(f'https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/day/'
              f'{desde.isoformat()}/{date.today().isoformat()}?adjusted=true&limit=5000&apiKey={k}')
    if not r.get('results'):
        return None, {}
    return ({datetime.utcfromtimestamp(b['t'] / 1000).strftime('%Y-%m-%d'): float(b['c'])
             for b in r['results']}, {'exchange': 'US (polygon)', 'currency': 'USD'})


def obter(ticker, desde, exchange=None):
    """Devolve (série, fonte, meta). A fonte e o instrumento resolvido ficam registados
    no retrato: comparar valores de fornecedores diferentes foi exatamente o erro que o
    arquivo mandou não repetir, e um símbolo ambíguo é pior ainda — 'SLX' devolve a
    Silex Systems (ASX) OU o VanEck Steel ETF (NYSE) conforme o fornecedor decide."""
    s, meta = serie_twelvedata(ticker, desde, exchange)
    if s:
        return s, 'twelvedata', meta
    s, meta = serie_polygon(ticker, desde)
    if s:
        return s, 'polygon', meta
    return None, None, {}


def fecho_em_ou_apos(serie, d, limite=7):
    """Fecho no dia d, ou no primeiro dia de sessão seguinte (feriados, fins de semana)."""
    for i in range(limite):
        k = (d + timedelta(days=i)).isoformat()
        if k in serie:
            return k, serie[k]
    return None, None


def medir(entrada, series):
    t = entrada['ticker']
    s, fonte, meta = series.get(t, (None, None, {}))
    if not s:
        return {'ticker': t, 'rotulo': entrada['rotulo'], 'estado': 'NÃO OBTÍVEL'}
    desde = datetime.strptime(entrada['desde'], '%Y-%m-%d').date()
    d0, p0 = fecho_em_ou_apos(s, desde)
    ult = max(s)
    if not p0:
        return {'ticker': t, 'rotulo': entrada['rotulo'], 'estado': 'NÃO OBTÍVEL',
                'porque': f'sem fecho a partir de {desde}'}
    r = {'ticker': t, 'rotulo': entrada['rotulo'], 'fonte': fonte, 'desde': d0,
         'instrumento': {k: meta.get(k) for k in ('exchange', 'currency', 'type') if meta.get(k)},
         'fecho_inicial': round(p0, 4), 'data_ultimo': ult, 'fecho_ultimo': round(s[ult], 4),
         'retorno_pct': round((s[ult] / p0 - 1) * 100, 2)}
    # Guarda contra símbolo ambíguo: se o retrato declara bolsa/moeda esperadas e o
    # fornecedor devolveu outra coisa, o número é marcado SUSPEITO em vez de passar.
    avisos = []
    for campo, esperado in (('exchange', entrada.get('exchange')), ('currency', entrada.get('moeda'))):
        obtido = meta.get(campo)
        if esperado and obtido and str(obtido).upper() != str(esperado).upper():
            avisos.append(f'{campo}: esperado {esperado}, obtido {obtido}')
    if avisos:
        r['estado'] = 'SUSPEITO — instrumento não corresponde ao declarado'
        r['avisos'] = avisos
    b = entrada.get('benchmark')
    if b and series.get(b, (None,))[0]:
        sb = series[b][0]
        _, b0 = fecho_em_ou_apos(sb, desde)
        ub = max(sb)
        if b0:
            rb = (sb[ub] / b0 - 1) * 100
            r['benchmark'] = b
            r['benchmark_pct'] = round(rb, 2)
            r['excesso_pp'] = round(r['retorno_pct'] - rb, 2)
    for c in ('ressalva', 'proxy_de'):
        if entrada.get(c):
            r[c] = entrada[c]
    return r


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--desde', default='2026-07-09', help='início da janela de descarga')
    args = ap.parse_args()
    if not (os.environ.get('TWELVEDATA_API_KEY') or os.environ.get('POLYGON_API_KEY')):
        sys.exit('Sem TWELVEDATA_API_KEY nem POLYGON_API_KEY no ambiente.')

    cfg = json.loads(CARTEIRA.read_text())
    desde = datetime.strptime(args.desde, '%Y-%m-%d').date()
    itens = [e for grupo in ('cartoes', 'picks_de_tese') for e in cfg[grupo] if e.get('ativo', True)]
    tickers = [b['ticker'] for b in cfg['benchmarks']] + [e['ticker'] for e in itens]

    exch = {e['ticker']: e.get('exchange') for e in itens + cfg['benchmarks']}
    series = {}
    for t in dict.fromkeys(tickers):
        series[t] = obter(t, desde, exch.get(t))
        time.sleep(8)          # limite gratuito do fornecedor: 8 pedidos/minuto

    linhas = [medir(e, series) for e in itens]
    bench = {b['ticker']: medir({**b, 'desde': args.desde, 'benchmark': None}, series)
             for b in cfg['benchmarks']}

    hoje = date.today().isoformat()
    SNAPS.mkdir(exist_ok=True)
    snap = {'data': hoje, 'janela_desde': args.desde, 'posicoes': linhas, 'benchmarks': bench,
            'nota': 'Retornos desde a data de entrega/promoção no arquivo. Sem entradas, '
                    'stops, sizing ou timing — descoberta ≠ execução.'}
    (SNAPS / f'precos-{hoje}.json').write_text(json.dumps(snap, ensure_ascii=False, indent=1))

    print(f"\n=== Proxy de valor · {hoje} ===")
    print(f"{'ticker':<7}{'desde':<12}{'inicial':>10}{'último':>10}{'ret%':>9}{'bench%':>9}{'excesso':>9}  fonte")
    for l in linhas:
        if l.get('estado') == 'NÃO OBTÍVEL':
            print(f"{l['ticker']:<7}{'NÃO OBTÍVEL — ' + l.get('porque', 'fornecedor sem série')}")
            continue
        marca = '  <<< SUSPEITO' if l.get('estado', '').startswith('SUSPEITO') else ''
        print(f"{l['ticker']:<7}{l['desde']:<12}{l['fecho_inicial']:>10.2f}{l['fecho_ultimo']:>10.2f}"
              f"{l['retorno_pct']:>+9.2f}{l.get('benchmark_pct', float('nan')):>+9.2f}"
              f"{l.get('excesso_pp', float('nan')):>+9.2f}  {l['fonte']}"
              f" [{l['instrumento'].get('exchange', '?')}/{l['instrumento'].get('currency', '?')}]{marca}")
        for a in l.get('avisos', []):
            print(f"        ! {a}")
    for t, b in bench.items():
        if b.get('estado') != 'NÃO OBTÍVEL':
            print(f"  [bench] {t}: {b['fecho_inicial']:.2f} → {b['fecho_ultimo']:.2f} ({b['retorno_pct']:+.2f}%)")
    for l in linhas:
        if l.get('ressalva'):
            print(f"\n  RESSALVA {l['ticker']}: {l['ressalva']}")
    print(f"\nGuardado em snapshots/precos-{hoje}.json")
    print("Isto é UMA das duas curvas. A curva industrial vive nos invalidadores, não aqui.")


if __name__ == '__main__':
    main()
