---
name: estudo-20-semanal
description: >
  Estudo retrospectivo dos movers de 20% numa semana: screener bull+bear,
  anatomia do registo de 4%, float, preço, posição de 52 semanas, reverse
  splits e flags Three-Lynch; testa H1-H8 com números e acumula resultados
  num ledger. Usar para "estudo dos 20%", "movers da semana", "quem subiu
  20% esta semana", "onde começou o movimento", "chart book", "caça ao
  registo de 4%", "estudo de 300% num ano", ou para testar se preço baixo,
  float baixo e partir de mínimos sobrevivem aos dados. Não substitui o
  gate de qualidade de um breakout nem o scanner de entradas do dia:
  trabalha retrospectivamente sobre coortes.
---

# Estudo 20% Semanal — v1.1

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
python3 scripts/movers_study.py --date 2026-07-24 \
  --security-database ~/.local/share/scan-us-breakouts/market.sqlite3 \
  --alpha-k-repo /caminho/alpha-k-data-pipeline
python3 scripts/movers_study.py --modo caca
python3 scripts/movers_study.py --lag 252 --threshold 300
python3 scripts/movers_study.py --rebuild-stats     # H1-H8 sobre o ledger inteiro
```

### Setup — chaves

Os segredos são lidos **apenas de variáveis de ambiente**. Nunca os passar
como argumentos CLI — ficam visíveis no histórico e na lista de processos —
nem gravá-los no skill:

```bash
export US_BREAKOUT_POLYGON="..."
export US_BREAKOUT_TWELVE="..."       # validação Alpha-K
export ESTUDO20_GITHUB_TOKEN="..."    # ledger remoto, opcional
export ALPHA_K_DATA_REPO="/caminho/alpha-k-data-pipeline"
```

Os nomes canónicos `POLYGON_API_KEY`, `TWELVE_DATA_API_KEY` e
`GITHUB_TOKEN` também são aceites. Sem token GitHub, o estudo corre mas não
grava no ledger; `--no-ledger` torna essa decisão explícita.

### Estágio 0 — universo e movers

`--provider auto` tenta duas chamadas Polygon
`grouped/locale/us/market/stocks/{data}` (T e T−lag). Se o endpoint não
pertencer ao plano, usa downloads Yahoo em chunks retomáveis sobre o
security master SQLite indicado por `--security-database` (ou a cache
Polygon de tipos). O fallback fica marcado `PROVISIONAL`; nunca se apresenta
como equivalência silenciosa ao feed primário.

O retorno da coorte usa **Adjusted Close**, mas os filtros de preço e volume
usam os valores brutos da sessão. Splits detectados ou divergências materiais
entre retorno bruto e ajustado ficam em `corporate_action_review` e não entram
na coorte como falsos movers.

Filtros da fonte: **preço ≥ $5, volume ≥ 100k**, universo **ADR + common US
+ ETF**; warrants, units, rights e preferred ficam de fora.

O calendário de sessões usa cache local e uma série SPY em uma única
chamada Polygon; Yahoo é apenas fallback. Nunca recua dia-a-dia — com
`--lag 252` isso custaria centenas de chamadas.

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
| H8 | O lado comprador oferece mais oportunidades | contagem bull vs bear, também separada entre equities e ETF/ETV |

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

## Assunções declaradas (D1-D9)

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
- **D9 — fundos não são oportunidades accionistas equivalentes.** H8 mantém
  a contagem total fiel ao universo da fonte, mas expõe `por_segmento` para
  separar common/ADR de ETF/ETV. A interpretação principal usa equities.

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
linearidade e classificação biotech · `[ASSUNÇÃO]` qualquer desvio a D1-D9,
e o universo não tipificado quando a cache de tipos falha ·
`[AMOSTRA-PEQUENA]` sempre que n<50.

Coorte vazia é resultado válido, não falha. `SEM-DADOS` e `SEM-BASELINE`
são veredictos honestos — nunca substituir por uma conclusão.

## Estado de validação (honesto)

- **Suites de regressão, verdes:** `test_movers_study.py` (inclui agora
  detecção da origem incl. contra-exemplos, pos52, flags Three-Lynch,
  retorno ajustado/splits, segmentação, Spearman, veredictos, ledger e chart book)
  e `test_pipeline_offline.py` (orquestração dos 3 modos + coorte sub-$5 +
  chart book + ajuste de data, com a rede substituída por fixtures).
  Correr ambas depois de qualquer alteração ao motor.
- **Ensaio real concluído em 2026-07-27:** o endpoint grouped do plano
  Polygon respondeu `403 plan_restricted`; o fallback Yahoo produziu a
  coorte e a reconciliação EOD Alpha-K verificou 8 dos 15 movers de maior
  amplitude. Os 7 restantes ficaram `disputed` por divergências de
  open/low/volume, mas preservaram o retorno close-to-close e a classificação
  ±20%. ADVB demonstrou ainda porque uma barra intradiária incompleta não
  pode ser usada como gate de liquidez antes do EOD.
- **Reensaio em 2026-07-28:** com o runtime reconfigurado, Polygon grouped
  respondeu com 12.402/12.388 símbolos em T/T−5. `auto` escolheu correctamente
  o feed primário; o fallback permanece coberto para planos sem esse acesso.
- **Screening integral de 2026-07-27:** 12.142 símbolos no merge → 4.610
  após preço/volume → 4.400 após tipo → 28 bull e 32 bear. Em equities foram
  20 bull/19 bear; ETF/ETV acrescentaram 8/13, validando a necessidade de D9.
  A reconciliação top-15 preservou a classificação ±20% em todos os nomes:
  4 `verified`, 10 `disputed` e 1 `fallback_only`. Duas anatomias bear
  ficaram sem histórico suficiente. O baseline amostrado de reverse splits
  foi 5%.
- **Sem track record:** todos os thresholds (4% do gatilho, 75% de
  cobertura em D2, buckets, ±0.15 de Spearman para o veredicto) são
  proposta inicial, não calibração. Calibram-se com o ledger acumulado,
  pela mesma disciplina do gate.

## Limitações conhecidas

- Estágio 1 é sequencial no `Ticker.info` (float/sector) — ~60 nomes levam
  ~1 min. `--no-fundamentals` salta e perde H3/H5.
- `Ticker.info` é a peça mais frágil: falhas ficam `null` com flag, nunca
  silenciadas nem inventadas. H5 não interpreta sector `null` como
  “não-biotech”; se todos os metadados falharem devolve `SEM-DADOS`.
- H4 sem `--baseline-sample` não tem termo de comparação e diz-o
  (`SEM-BASELINE`) em vez de fingir um veredicto.
- H5 é descritiva: sem a base rate de biotech no universo, "40% da coorte é
  biotech" não prova sobre-representação.
- **Core standalone por desenho:** a descoberta, anatomia, hipóteses e
  chart book não importam skills irmãos. A reconciliação Alpha-K é opcional,
  activada apenas com `--alpha-k-repo`; sem esse repo o resultado declara
  `validation.status=not_run`.

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

**v1.1** — runtime seguro por ambiente, discovery `auto` com fallback Yahoo,
retornos ajustados e exclusão de corporate actions mecânicas, H8 segmentada
(D9), reconciliação opcional Alpha-K e validação EOD real.
