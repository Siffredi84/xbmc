# Coletor de sinais precoces — classe 6 (talento)

## Porquê existe

O motor de inflexões detetava temas **tarde**. A corrida #3 (06/08/2026) mediu-o pela
primeira vez: o tema CPO foi apanhado a ~4 semanas do mainstream. E o
`teste-retroativo-sinais-precoces-2026-08-06.md` mostrou porquê — as duas classes de
sinal mais precoces (talento e obra física) estavam **estruturalmente inacessíveis** e
apareceram como "NÃO OBTÍVEL" em todas as corridas.

Este coletor abre a primeira: **vagas de emprego**. Uma empresa contrata para uma
tecnologia trimestres antes de a vender, e anos antes de ela ter nome na imprensa.

## O que mede — difusão, não volume

A métrica não é *quantas vagas existem*, é **em quantas empresas DISTINTAS um termo
técnico aparece**:

> Uma empresa a pedir "engenheiro de X" é uma empresa.
> **Oito empresas independentes a pedir o mesmo é uma indústria a nascer.**

É a mesma definição de inflexão que o motor já usa — *"quem pode fornecer isto passa
de pergunta aberta a lista fechada de 3-8 nomes"* — agora observável em tempo real.

**A zona de inflexão é 3-8 empresas.** Acima disso o tema já está estabelecido; abaixo
é ruído de uma empresa só.

## Duas classes

- **Classe 6 — talento** (este diretório): `coletar.py`, vagas de emprego.
- **Classe 7 — obra física**: `obra/coletar_obra.py`, fila de interconexão elétrica.

## Uso

```bash
python3 coletar.py            # retrato de hoje + movimento desde o anterior
python3 coletar.py --top 40   # mais termos
```

Sem chaves, sem autenticação — as APIs de job boards são públicas.

## Estrutura

- `universo.json` — empresas vigiadas (nome, sistema ATS, token). Ampliável.
- `snapshots/AAAA-MM-DD.json` — retrato datado. **Guarda os títulos em bruto**, o que
  permite reanalisar o passado com vocabulário novo sem perder história.
- `coletar.py` — o coletor.

## Como ler o output

O **primeiro** retrato não tem sinal — só referência. O sinal nasce no **segundo**, e
tem duas formas:

1. **Termos novos** — vocabulário que não existia e aparece em ≥2 empresas;
2. **Difusão a crescer** — o mesmo termo a passar de N para N+k empresas.

## Limitações declaradas

- **Cobertura geográfica:** estes sistemas cobrem sobretudo empresas americanas e
  modernas. Ibiden (Japão), Siemens Energy (Alemanha) e os fabricantes coreanos **não
  estão aqui**. Metade das portagens que o framework encontra fica invisível.
- **Universo semeado, não exaustivo:** 38 empresas de fronteira (fusão, quantum,
  robótica, semis, energia, defesa). A difusão é medida *dentro* deste universo — o
  que é válido para a derivada, mas não é uma amostra do mercado.
- **Ruído:** empresas publicam vagas que não preenchem e republicam anúncios antigos.
  Por isso a métrica olha para a *derivada entre retratos*, não para o nível.
- **O filtro de RH é heurístico** e deixa passar termos administrativos. Ajustável na
  lista `STOP` em `coletar.py`.

## Primeiro retrato — 06/08/2026

3.527 vagas · 38 empresas. Dois sinais imediatos na zona de inflexão:

- **`physical design` + `design verification`** (4 empresas cada: Cerebras, Etched,
  Lightmatter) — a camada de projeto físico de silício a formar procura.
- **`power electronics`** (4: Helion, Redwood Materials, Relativity) — três indústrias
  *diferentes* (fusão, baterias, foguetes) a pedir a mesma competência. Confirmação
  independente do bem escasso que a tese T10 identificou (estabilidade de rede /
  eletrónica de potência), vinda de uma classe de sinal que a tese não usou.

*Research/watchlist — não é aconselhamento financeiro.*
