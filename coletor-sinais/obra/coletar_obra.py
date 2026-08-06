#!/usr/bin/env python3
"""
Coletor de sinais precoces — classe 7 (obra física).

Porquê existe: um projeto industrial pede ligação à rede elétrica ANOS antes de
haver obra, encomendas ou notícias. É um compromisso administrativo datado e público
— cabe na definição de sinal L2 do motor ("permits obtidos") e é o sinal mais
precoce que existe para qualquer transformação que consuma energia.

Validação: o teste retroativo de 06/08/2026 mostrou que esta fila virou no
1.º semestre de 2024 (20,6 → 58,0 GW de gás num semestre), quando o operador só
detetou o tema em outubro de 2025. ~18 meses de antecedência.

O que mede: capacidade de ENERGIA FIRME pedida por região e semestre. Firme = gás,
nuclear, geotérmica — o que serve carga 24/7. Solar e eólica não servem para carga
base, por isso não sinalizam procura industrial contínua da mesma forma.

O sinal é a DERIVADA: uma duplicação semestral numa região (o padrão de 2024-S1).

Uso:  python3 coletar_obra.py               # análise do ficheiro local
      python3 coletar_obra.py --download    # buscar edição nova ao LBNL
"""
import argparse, json, sys, urllib.request
from pathlib import Path
from datetime import date

BASE = Path(__file__).parent
XLSX = BASE / 'lbnl_queue.xlsx'
# As páginas do LBNL têm Cloudflare (403); os ficheiros em /sites/default/files/ não.
URL = 'https://emp.lbl.gov/sites/default/files/2026-05/LBNL_Ix_Queue_Data_File_thru2025.xlsx'
FIRME = 'Gas|Nuclear|Geothermal|Coal'   # tecnologias de carga base

def descarregar():
    print(f"A descarregar de {URL[:60]}...")
    req = urllib.request.Request(URL, headers={'User-Agent': 'Mozilla/5.0'})
    XLSX.write_bytes(urllib.request.urlopen(req, timeout=120).read())
    print(f"  {XLSX.stat().st_size:,} bytes")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--download', action='store_true')
    ap.add_argument('--desde', type=int, default=2021)
    args = ap.parse_args()
    if args.download or not XLSX.exists():
        descarregar()

    import pandas as pd, warnings
    warnings.filterwarnings('ignore')
    df = pd.read_excel(XLSX, sheet_name='03. Complete Queue Data', skiprows=1)
    df.columns = [str(c).strip() for c in df.columns]
    df['mw'] = pd.to_numeric(df['mw_1'], errors='coerce').fillna(0)
    df['q_date'] = pd.to_datetime(df['q_date'], errors='coerce')
    firme = df[df.type_clean.astype(str).str.contains(FIRME, case=False, na=False)].dropna(subset=['q_date'])
    firme = firme[firme.q_date.dt.year >= args.desde]
    firme['sem'] = firme.q_date.dt.year.astype(str) + '-S' + ((firme.q_date.dt.month > 6).astype(int) + 1).astype(str)

    print(f"\n=== ENERGIA FIRME pedida por semestre (desde {args.desde}) ===")
    tot = firme.groupby('sem').agg(pedidos=('mw', 'size'), gw=('mw', lambda x: x.sum()/1000))
    prev = None
    for s, r in tot.iterrows():
        d = f"  ({r.gw/prev:+.1f}×)" if prev and prev > 0 else ""
        alerta = "  ⚠️ DUPLICAÇÃO" if prev and r.gw > 2*prev else ""
        print(f"  {s}: {int(r.pedidos):4} pedidos · {r.gw:6.1f} GW{d}{alerta}")
        prev = r.gw

    print(f"\n=== POR REGIÃO — últimos 4 semestres (GW) ===")
    piv = firme.pivot_table(index='region', columns='sem', values='mw', aggfunc='sum').fillna(0)/1000
    cols = sorted(piv.columns)[-4:]
    piv = piv[cols].round(1)
    piv['Δ'] = (piv[cols[-1]] - piv[cols[0]]).round(1)
    print(piv.sort_values('Δ', ascending=False).head(8).to_string())

    hoje = date.today().isoformat()
    snap = {'data': hoje, 'fonte': URL,
            'firme_por_semestre': {s: {'pedidos': int(r.pedidos), 'gw': round(r.gw, 1)} for s, r in tot.iterrows()},
            'por_regiao_gw': json.loads(piv.drop(columns=['Δ']).to_json())}
    (BASE / f'snapshot-obra-{hoje}.json').write_text(json.dumps(snap, ensure_ascii=False, indent=1))
    print(f"\nGuardado em snapshot-obra-{hoje}.json")
    print("\nNOTA: o ficheiro LBNL é ANUAL. Para latência mensal são precisas as filas dos")
    print("ISOs — todas exigem registo gratuito (EIA, PJM). Ver README.")

if __name__ == '__main__':
    main()
