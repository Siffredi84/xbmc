---
name: estudo-20-semanal
description: >
  Estudo diário retrospectivo dos movers de 20% numa semana (metodologia
  "How to study 20% plus winners in a week"): screener bull+bear de
  close(T)/close(T-5) >= 20% no universo ADR+common+ETF, anatomia de cada
  vencedor (onde começou o movimento — o "registo de 4%" —, float, preço,
  posição no range de 52 semanas, reverse split, flags Three-Lynch), e
  teste mecânico das 8 afirmações da fonte (H1-H8) com veredicto
  SUPORTA/CONTRARIA/INCONCLUSIVO. Acumula tudo num ledger para que ao fim
  de semanas exista evidência e não intuição. Usar quando o utilizador
  pedir "estudo dos 20%", "movers da semana", "quem subiu 20% esta
  semana", "estudo diário", "winners da semana", "onde começou o
  movimento", "livro de gráficos", "chart book", "caça ao registo de 4%",
  "pesquisa de rutura dos 4%", "estudo de 300% num ano", ou quiser testar
  se "preço baixo / float baixo / partir de mínimos" se confirma nos
  dados. NÃO substitui o breakout-quality-gate (valida 1 breakout já
  identificado) nem o breakout-market-scanner (descobre breakouts de
  entrada hoje) — este é retrospectivo e estatístico, sobre coortes.
---

# Estudo 20% Semanal — v1.0

Responde a uma pergunta que nenhum skill irmão responde:

| Skill | Pergunta |
|---|---|
| `breakout-quality-gate` | "este breakout, neste ticker, é tecnicamente limpo?" |
| `breakout-market-scanner` | "que breakouts há hoje em todo o mercado?" |
| **este** | **"o que têm em comum os vencedores da semana — e as regras que me vendem sobrevivem aos dados?"** |

A fonte não pede que se sigam regras: pede que se **verifique cada
afirmação com os próprios olhos**, incluindo as dela. Por isso este skill
não devolve uma lista de compras — devolve uma coorte dissecada e oito
hipóteses testadas, com veredicto que tanto pode ser SUPORTA como
CONTRARIA.

## Modo de execução

`"estudo dos 20% de hoje"`, `"movers da semana"`, `"quem subiu 20% esta
semana"` → modo estudo. `"caça ao registo de 4%"`, `"candidatos de rutura
dos 4%"` → modo caça. `"estudo dos 300% no ano"` → modo anual. Sem data →
assumir a última sessão provável e **declarar a assunção**.

---

## Um motor, três modos

Estudo semanal e estudo anual são o mesmo cálculo com outro lag —
`close(T)/close(T−lag) − 1 ≥ threshold`. Daí não existirem três scripts.

| Modo | Comando | O que devolve |
|---|---|---|
| **A · estudo** (default) | `--date 2026-07-24` | coortes bull e bear (±20% em 5 sessões), anatomia, H1-H8 |
| **B · caça 4%** | `--modo caca` | shortlist forward de hoje: preço baixo + float baixo + a vir de baixo |
| **C · anual** | `--lag 252 --threshold 300` | os movimentos de 300%+ que a fonte manda estudar a fundo |

```bash
python3 scripts/movers_study.py --date 2026-07-24 --chartbook ~/chartbook.html
python3 scripts/movers_study.py --modo caca
python3 scripts/movers_study.py --lag 252 --threshold 300
python3 scripts/movers_study.py --rebuild-stats     # H1-H8 sobre o ledger inteiro
```

### Setup — chaves (desvio deliberado à convenção das skills irmãs)

O gate e o scanner trazem as chaves hardcoded no script. **Aqui não**: este
skill é versionado num repositório, e um PAT do GitHub commitado é um
segredo publicado (o push protection do GitHub bloquearia, e com razão).
As chaves são lidas por esta ordem: variável de ambiente →
`~/.claude/estudo20-keys.json` (local, fora de qualquer repo, `chmod 600`):

```json
{"POLYGON_API_KEY": "...", "GITHUB_TOKEN": "..."}
```

São as mesmas chaves que o `breakout-quality-gate` já usa. Sem
`POLYGON_API_KEY` o script pára e diz o que falta; sem `GITHUB_TOKEN` corre
na mesma e avisa que não grava no ledger. `--no-ledger` desliga a escrita
remota explicitamente.

### Estágio 0 — universo e movers (2 chamadas Polygon, 0 por ticker)

Duas chamadas a `grouped/locale/us/market/stocks/{data}` (T e T−lag),
merge por ticker. Filtros da fonte: **preço ≥ $5, volume ≥ 100k**, universo
**ADR + common US + ETF** (cache local de `reference/tickers`, TTL 7 dias;
warrants, units, rights e preferred ficam de fora).

O calendário de sessões vem de uma série do SPY (1 chamada grátis), não de
recuar dia-a-dia no Polygon — com `--lag 252` isso custaria 252 chamadas a
uma API de 5/min.

### Estágio 1 — anatomia de cada vencedor (yfinance, grátis)

Por nome: **origem do movimento** (o registo de 4%: primeiro dia ≥+4% que
puxa o move), gap e volume nesse dia, **preço e posição no range de 52
semanas na véspera da origem**, retorno 20d/60d anterior, dias de
consolidação, **float** + qualidade do float, **reverse split** nos 12
meses, sector/biotech, flags **Three-Lynch** (não subiu 3 dias · dia prévio
negativo ou inside · fecho perto do máximo · R² do primeiro tramo ·
idade da tendência), e o risco pós-movimento (retorno D+1, drawdown 5d).

### Estágio 2 — as 8 hipóteses

| # | Afirmação da fonte | Como é testada |
|---|---|---|
| H1 | Quanto mais baixo o preço, maior o movimento | Spearman(preço na origem, move) + buckets <$1…>$30 |
| H2 | Os moves partem de mínimos, não de máximos de 52s | distribuição de `pos52`; terço inferior vs superior |
| H3 | Quanto mais baixo o float, mais explosivo | Spearman(float, move) + buckets <1M…>50M |
| H4 | Reverse split recente sobre-representado | taxa na coorte vs base rate do universo (`--baseline-sample N`) |
| H5 | Biotech com catalisador continua depois do gap | % biotech no decil de topo, gap mediano |
| H6 | O dia seguinte é perigoso | mediana do retorno D+1, % negativos |
| H7 | Todo o move de 20% contém um dia de 4% (20/5=4) | % da coorte com origem identificada |
| H8 | O lado comprador oferece mais oportunidades | contagem bull vs bear do mesmo dia |

Veredictos: `SUPORTA` / `CONTRARIA` / `INCONCLUSIVO` / `SEM-DADOS`. Com
`n<50` tudo leva `[AMOSTRA-PEQUENA]` — um dia isolado não decide nada.

### Estágio 3 — acumulação (é aqui que está o valor)

Cada corrida grava `studies/{data}_{modo}_lag{N}.json` e faz upsert em
`study_ledger.csv` no repo `Siffredi84/breakout-pipeline-data`, uma linha
por `(data, ticker, side)`. `--rebuild-stats` recomputa H1-H8 sobre o
ledger inteiro: é o que transforma "seis semanas de estudo diário" numa
afirmação com suporte empírico em vez de memória.

### Chart book

`--chartbook /caminho.html` gera o equivalente digital dos livros de
gráficos da fonte: um painel por vencedor (preço+volume, consolidação
sombreada, seta no dia da origem, bandas de 52 semanas, metadados e chips
Three-Lynch), tudo em base64 num único HTML sem dependências externas.
Publicável como Artifact para rever no telemóvel.

---

## Assunções declaradas (D1-D8)

- **D1** Volume ≥100k aplicado ao dia T — a fonte não diz se é média.
- **D2** Origem = primeiro dia com variação ≥+4% (≤−4% no bear) cuja subida
  acumulada até T cobre ≥75% do threshold. A fonte descreve o conceito
  ("registo de 4%"), não o algoritmo — ajustável em `find_origin`.
- **D3** Float do yfinance é o melhor proxy gratuito (a fonte usa
  MarketSmith). Cross-check com o Polygon → `float_quality` HIGH/MEDIUM/LOW
  em cada nome; float em falta enfraquece H3 nesse nome e isso fica visível.
- **D4** Tipos Polygon `CS/ADRC/ADRP/ADRR/ETF/ETV` = "ADRs, common US e ETFs".
- **D5** `pos52` medido na **véspera da origem**, nunca em T — medir em T
  seria circular: depois de subir 20% está sempre perto do máximo. Esta é a
  assunção que decide H2, a hipótese central da fonte.
- **D6** Biotech classificado por `sector`/`industry` do yfinance.
- **D7** Reverse split relevante = últimos 12 meses.
- **D8 — a tensão da própria fonte.** O scan filtra >$5 mas a conclusão é
  "quanto mais baixo o preço, melhor": H1 nasce truncada pelo próprio
  filtro. Default fiel à fonte; **`--coorte-sub5` corre a coorte $1-$5 em
  paralelo** para testar H1 em toda a amplitude. Sem isto, o skill herdava
  o viés de selecção da fonte sem o assinalar.

---

## Pipeline de execução (o que o agente faz depois do script)

1. Correr o script no modo pedido. O JSON é a fonte de verdade.
2. **Interpretação da coorte (obrigatória, nunca parar no JSON):** 3-5
   frases — onde se concentrou o movimento hoje, que hipóteses o dia
   sustentou ou contrariou, e o que diverge da média acumulada do ledger.
3. **Leitura chart-a-chart do top 5:** para cada um, *onde começou o
   movimento* e a que padrão da fonte corresponde (gap de biotech · float
   residual pós-reverse-split · saída de consolidação prolongada ·
   recuperação de mínimos). É este exercício, repetido, que constrói o
   reconhecimento de padrões — não o scan.
4. **Contradições explícitas:** quando os números contrariarem a fonte,
   dizê-lo com o número à frente. Um skill que só confirma quem o escreveu
   falhou exactamente o método que o vídeo defende.
5. **Handoff obrigatório:** candidatos ainda accionáveis hoje →
   `breakout-quality-gate` (`--ticker X --breakout-date {origem}`, G0
   relativo ao SPY); grade A/B → `breakout-thesis-investigator` (porque é
   que rompeu, há mecanismo económico por trás). Este skill nunca responde
   "porquê" — é deliberadamente outro skill, não uma lacuna a preencher aqui.

## Disciplina epistémica

`[FACTO]` métricas do script, com fonte e data · `[INFERÊNCIA-PROXY]` R² de
linearidade e classificação biotech · `[ASSUNÇÃO]` qualquer desvio a D1-D8,
e o universo não tipificado quando a cache de tipos falha ·
`[AMOSTRA-PEQUENA]` sempre que n<50.

Coorte vazia é resultado válido, não falha. `SEM-DADOS` e `SEM-BASELINE`
são veredictos honestos — nunca substituir por uma conclusão.

## Estado de validação (honesto)

- **Suites de regressão, verdes:** `test_movers_study.py` (44 checks:
  detecção da origem incl. contra-exemplos, pos52, flags Three-Lynch,
  reverse split, funil, Spearman, veredictos, buckets, ledger, chart book)
  e `test_pipeline_offline.py` (orquestração dos 3 modos + coorte sub-$5 +
  chart book + ajuste de data, com a rede substituída por fixtures).
  Correr ambas depois de qualquer alteração ao motor.
- **Por exercitar:** as chamadas reais a Polygon e yfinance nunca correram
  — o container onde o skill foi construído tem esses hosts bloqueados por
  política de egress (só `api.github.com` passa). A **primeira corrida numa
  máquina com acesso é o teste que falta**: confirmar o funil
  (~12k → liquidez → tipo → dezenas de movers), e conferir à mão em 2 nomes
  que `close(T)/close(T−5)−1` bate certo com o histórico — é aí que
  apareceria um desalinhamento de datas entre as duas chamadas grouped.
- **Sem track record:** todos os thresholds (4% do gatilho, 75% de
  cobertura em D2, buckets, ±0.15 de Spearman para o veredicto) são
  proposta inicial, não calibração. Calibram-se com o ledger acumulado,
  pela mesma disciplina do gate.

## Limitações conhecidas

- Estágio 1 é sequencial no `Ticker.info` (float/sector) — ~60 nomes levam
  ~1 min. `--no-fundamentals` salta e perde H3/H5.
- `Ticker.info` é a peça mais frágil: falhas ficam `null` com flag, nunca
  silenciadas nem inventadas.
- H4 sem `--baseline-sample` não tem termo de comparação e diz-o
  (`SEM-BASELINE`) em vez de fingir um veredicto.
- H5 é descritiva: sem a base rate de biotech no universo, "40% da coorte é
  biotech" não prova sobre-representação.
- **Standalone por desenho:** não importa nenhum skill irmão (regra da v1.1
  do scanner). A lógica partilhada está duplicada — ganha independência
  total, perde sincronização automática se um dia recalibrares o gate.

## Governança

Mesma regra do gate: ajustar thresholds dentro de um critério existente é
livre; **promover qualquer hipótese a filtro do funil exige primeiro um
teste de interacção** (filtro ON/OFF × filtros existentes ON/OFF). H1-H8
são instrumentos de medição — no dia em que virarem filtros, deixam de
poder medir o que estavam a testar.

## Versionamento

**v1.0** — build inicial: motor de 3 modos (estudo/caça/anual), anatomia
completa, H1-H8 com veredictos, ledger acumulado com `--rebuild-stats`,
chart book HTML, coorte sub-$5 (D8) e duas suites de regressão.
