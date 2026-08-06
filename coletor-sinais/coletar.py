#!/usr/bin/env python3
"""
Coletor de sinais precoces — classe 6 (talento).

Porquê existe: o motor de inflexões detetava temas tarde (~4 semanas do mainstream
no caso do CPO) porque as duas classes de sinal mais precoces estavam inacessíveis.
As vagas de emprego são a mais precoce de todas: uma empresa contrata para uma
tecnologia trimestres antes de a vender, e anos antes de ela ter nome na imprensa.

O que mede: DIFUSÃO — não quantas vagas existem, mas em quantas empresas DISTINTAS
um termo técnico aparece. Uma empresa a pedir "engenheiro de X" é uma empresa;
oito empresas independentes a pedir o mesmo é uma indústria a nascer. É a mesma
definição de inflexão que o motor já usa ("quem pode fornecer isto passa de
pergunta aberta a lista fechada de 3-8 nomes"), agora observável em tempo real.

Uso:  python3 coletar.py            # retrato de hoje + comparação com o anterior
      python3 coletar.py --top 40   # mostrar mais termos
"""
import json, re, sys, urllib.request, argparse
from collections import defaultdict
from datetime import date
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

BASE = Path(__file__).parent
UA = {'User-Agent': 'inflection-research/1.0'}

# Ruído de RH e generalidades: não são sinal de tecnologia.
STOP = set("""senior staff principal lead junior manager director head chief vp associate
engineer engineering technician specialist analyst scientist developer designer architect
software hardware mechanical electrical systems product program project operations technical
of and for the in to a an at on with new we our you your is are be as by from will can
i ii iii iv sr jr level intern internship contract remote hybrid onsite full time part
united states usa us ca tx wa ny co ma washington california texas austin seattle
team support sales marketing finance hr people talent recruiter legal counsel office
manufacturing production quality test testing assembly maintenance facilities safety
research development applied general application applications experienced entry
customer success business partner executive assistant vice president account
communications brand employer career acquisition recruiting compensation benefits
strategy strategic partnerships partnerships partner accounting controller payroll
administrative executive coordinator generalist advisor consultant representative
success solutions services enablement onboarding training learning workplace
early campus university graduate deployed forward""".split())

def fetch(entry):
    """Devolve (nome, [títulos]) — tolerante a falhas: uma empresa em baixo não mata a corrida."""
    ats, tok = entry['ats'], entry['token']
    urls = {'greenhouse': f'https://boards-api.greenhouse.io/v1/boards/{tok}/jobs',
            'lever':      f'https://api.lever.co/v0/postings/{tok}?mode=json',
            'ashby':      f'https://api.ashbyhq.com/posting-api/job-board/{tok}'}
    try:
        raw = urllib.request.urlopen(urllib.request.Request(urls[ats], headers=UA), timeout=25).read()
        d = json.loads(raw)
        jobs = d.get('jobs', d) if isinstance(d, dict) else d
        titles = [j.get('title') or j.get('text') or '' for j in jobs]
        return tok, [t for t in titles if t]
    except Exception as e:
        print(f"  ! {tok} ({ats}): {type(e).__name__}", file=sys.stderr)
        return tok, []

def terms(title):
    """N-gramas de 1-3 palavras, sem ruído de RH. Preserva termos compostos ('fuel recycling')."""
    words = [w for w in re.findall(r"[a-z0-9][a-z0-9\-\+/\.]{1,}", title.lower()) if w not in STOP]
    out = set(words)
    for n in (2, 3):
        for i in range(len(words) - n + 1):
            out.add(' '.join(words[i:i+n]))
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--top', type=int, default=25)
    args = ap.parse_args()

    universo = json.load(open(BASE / 'universo.json'))
    print(f"A recolher {len(universo)} empresas...")
    with ThreadPoolExecutor(max_workers=12) as ex:
        results = dict(ex.map(fetch, universo))

    # difusão: termo -> conjunto de empresas distintas
    dif = defaultdict(set)
    for comp, titles in results.items():
        for t in titles:
            for term in terms(t):
                dif[term].add(comp)

    hoje = date.today().isoformat()
    snap = {'data': hoje,
            'empresas': len(results),
            'vagas': sum(len(v) for v in results.values()),
            'titulos': results,                                    # dados brutos: permite reanálise futura
            'difusao': {k: sorted(v) for k, v in dif.items() if len(v) >= 2}}
    (BASE / 'snapshots' / f'{hoje}.json').write_text(json.dumps(snap, ensure_ascii=False, indent=1))

    print(f"\n{snap['vagas']:,} vagas · {snap['empresas']} empresas · guardado em snapshots/{hoje}.json")

    # comparação com o retrato anterior — é aqui que nasce o sinal
    ants = sorted(p for p in (BASE / 'snapshots').glob('*.json') if p.stem != hoje)
    if not ants:
        print("\nPrimeiro retrato: sem comparação possível. O sinal nasce no segundo.")
        print(f"\n=== Termos mais difundidos hoje (referência) ===")
        for term, comps in sorted(dif.items(), key=lambda x: -len(x[1]))[:args.top]:
            if len(term) > 4:
                print(f"  {len(comps):2} empresas · {term}")
        return

    prev = json.load(open(ants[-1]))
    pdif = {k: set(v) for k, v in prev['difusao'].items()}
    print(f"\n=== MOVIMENTO desde {prev['data']} ===")
    novos = [(t, c) for t, c in dif.items() if t not in pdif and len(c) >= 2 and len(t) > 4]
    subiu = [(t, c, pdif[t]) for t, c in dif.items() if t in pdif and len(c) > len(pdif[t]) and len(t) > 4]

    if novos:
        print("\n  TERMOS NOVOS (difusão ≥2 empresas, não existiam antes):")
        for t, c in sorted(novos, key=lambda x: -len(x[1]))[:args.top]:
            print(f"    +{len(c)} empresas · {t}  [{', '.join(sorted(c)[:4])}]")
    if subiu:
        print("\n  DIFUSÃO A CRESCER (mais empresas a pedir o mesmo):")
        for t, c, p in sorted(subiu, key=lambda x: -(len(x[1]) - len(x[2])))[:args.top]:
            print(f"    {len(p)}→{len(c)} empresas · {t}")
    if not novos and not subiu:
        print("  Sem movimento de difusão. Resultado válido — não se força sinal.")

if __name__ == '__main__':
    main()
