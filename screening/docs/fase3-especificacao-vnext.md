# Fase 3 — Especificação do pipeline vNext

**Data:** 30 de julho de 2026 · **Base:** Fases 0-2 + T1, T2 e amostra de spreads de 30-07
**Âmbito:** especificação. A implementação é matéria da Fase 4.

---

## 1. Fases de execução e contratos

Sete fases. Cada uma tem contrato de entrada, contrato de saída e política de falha própria.

### FASE A — Construção do universo
**Entrada:** nenhuma (raiz)
**Saída:** `universo.parquet` — colunas `Ticker`, `type`, `exch`, `nome`, `split_estado`, `split_ultima_data`, `serie_estado`, `sessoes_em_falta`

| Passo | Regra exacta | Fonte | Falha |
|---|---|---|---|
| A1 | `ultima_sessao_esperada()` em hora ET; cache tem de terminar aí | local | aborta |
| A2 | `type == "CS"` **e** `exch ∈ {XNAS, XNYS, XASE}` | Polygon `/v3/reference/tickers` | aborta |
| A3 | **Corporate actions.** `split ≤ 90 dias` → `EXCLUIDO_SPLIT_RECENTE`. `90 < split ≤ 365` → `split_estado = RECENTE`, janela de range truncada | Polygon `/v3/reference/splits` | **aborta** (`VERIFICACAO_INCOMPLETA`) |
| A4 | OHLCV grouped por sessão | Polygon | aborta |
| A5 | Quarentena: faltas acima da linha de base do mercado > 3 → `INTERRUPCAO` \| `SERIE_CURTA` \| `ILIQUIDEZ` | local | etiqueta |

**A3 é o único componente que aborta a corrida inteira.** É a raiz contaminante: sem splits verificados, nenhum indicador a jusante é interpretável.

### FASE B — Gates técnicos (zero chamadas)
**Entrada:** `universo.parquet` com `serie_estado == OK`
**Saída:** `shortlist.parquet`

| Passo | Regra | Tipo | Medido em 29-07 |
|---|---|---|---|
| B1 | `1.00 ≤ preço ≤ 7.00` | gate | 1.133 |
| B2a | `AvgVolShares_63 > 100.000` | gate | 860 |
| **B2b** | **`AvgVolUSD_63 > $1.000.000`** | gate | **670** |
| B3 | Indicadores: RSI(14, **janela 63 fixa**), SMA20, RVOL, RVOL_pico_20, Eco, Vol20d, MedVol_63 | — | — |
| B4 | `RVOL_sessao > 1,2` — denominador: média das 63 sessões anteriores, **excluindo a corrente** | gate | — |
| B5 | `RSI ≤ 60` (**tecto apenas**; piso passa a feature `rsi_zona`) | gate | — |
| B6 | `SMA20_pct > −15%` | gate | — |
| B7 | Range 52s calculado de 252 sessões, truncado no último split; `range_estado` | **feature** | — |
| B8 | `A ∨ B ∨ C` — sinal C exige **≥2 dos 3** componentes | gate | 48 |

**Flags produzidas em B (nunca excluem):** `risco_listagem`, `extensao`, `volume_assimetrico`, `rsi_zona`.

### FASE C — Identidade
**Entrada:** shortlist · **Saída:** `+ conid`, `cik`, `tier_listagem`, `identidade_estado`
Ordem de consulta: **IBKR** (autoritativa) → **Yahoo** (árbitro, só em falha ou divergência).
Três estados: `OK` · `REVER` (ticker e bolsa batem, nome diverge) · `FAIL`.
Custo: 1 chamada/candidato com IBKR (era 2 com Yahoo).

### FASE D — Fundamentais
**Entrada:** shortlist com `identidade_estado ≠ FAIL`
| Passo | Regra | Fonte principal | Fallback |
|---|---|---|---|
| D1 | Acções: facto com `end` mais recente; somar classes distintas do mesmo `end`; `accn` mais recente em empate; `freshness ≤ 120 dias` | **SEC XBRL** `dei:EntityCommonStockSharesOutstanding` | Finnhub `profile2` → `MCapEstado = FALLBACK` |
| D2 | `MCapM = acções × preço USD`; gate `50 ≤ MCapM ≤ 500` | derivado | — |
| D3 | `regime_reporte ∈ {10-Q, 20-F}` pelos formulários dos últimos 12 meses | EDGAR | — |

### FASE E — Red flags (exclusão estrutural)
| Red flag | Regra | Estado em falha |
|---|---|---|
| Going concern | conclusão afirmativa, não avaliação (ASC 205-40) | `A_REVER` → não aprovado |
| Delisting | 8-K item **3.01** | `FALHA_REDE` → não aprovado |
| Reverse split | já aplicado em A3 | — |
| Queda >80% sem recuperação (P4) | `High52_pct ≤ −80` **e** recuperação desde o mínimo `< 15%`, **sobre o range calculado em B7** | não decide se `range_estado ≠ OK` |
| Volume <50k | coberto por B2a (mais exigente) | — |
| OTC | coberto por A2 | — |

Emissores `20-F`: o gate de going concern **não é satisfazível**; ficam em `REVISAO_20F`, nunca aprovados automaticamente.

### FASE F — Enriquecimento (features, nunca excluem)
`insider_P_30d` · `spread_pct` e profundidade do livro (IBKR, **só com mercado aberto**) · `formularios_diluicao` · breakout (`resistencia`, `toques`, `dist_pct`, `tolerancia=2%`, `janela=60`) · notícias (Marketaux só na fila de evento) · `cobertura_estado = SEM_FONTE`

### FASE G — Classificação, ordenação e observabilidade
Ver secções 4 e 5.

---

## 2. Estados possíveis — seis, nunca colapsados

| Estado | Significado | Efeito |
|---|---|---|
| `OK` | verificado e dentro do critério | prossegue |
| `FORA_DO_CRITERIO` | verificado e fora | excluído, com razão |
| `DATA_INSUFFICIENT` | dado ausente | posto de lado (indeterminado) |
| `DATA_INVALID` | dado presente mas impossível (ex.: mínimo 52s > preço) | posto de lado + alerta |
| `DATA_STALE` | dado válido mas fora da janela de freshness | posto de lado |
| `SOURCE_DISAGREE` | fontes divergem acima do limiar | `REVER` |
| `NETWORK_FAILURE` | falha de rede após backoff | red flag: bloqueia · feature: passa com etiqueta |

**Regra invariante:** nenhuma destas condições pode ser convertida noutra. `SEM_FONTE ≠ SEM_SINAL ≠ NETWORK_FAILURE`.

---

## 3. Fontes e fallbacks

| Campo | Principal | Fallback | Comparador | Freshness |
|---|---|---|---|---|
| OHLCV | Polygon | — | — | última sessão fechada |
| Universo/tipo/bolsa | Polygon reference | — | Yahoo `fullExchangeName` (tier) | 1 dia |
| Splits | Polygon | — | — | 365 dias |
| Identidade | **IBKR** | Yahoo | — | sessão |
| Acções em circulação | **SEC XBRL** | Finnhub | Finnhub | 120 dias |
| Range 52s | **Polygon calculado** | — | Finnhub metric | 252 sessões |
| Filings/red flags | EDGAR | — | — | 12 meses |
| Insiders | Finnhub | EDGAR Form 4 | — | 30 dias |
| Spread e profundidade | **IBKR** | — | — | **só sessão regular** |
| Notícias | Marketaux | Finnhub | — | 8 dias |
| Macro | FRED | — | — | 1 dia |
| Cobertura de analistas | **nenhuma** | — | — | — |

---

## 4. Classificação de setups

Cinco setups mutuamente exclusivos, avaliados por **precedência lexicográfica**. Sem score, sem pesos.

| # | Setup | Regra exacta | Pergunta de falsificação | 30-07 |
|---|---|---|---|---|
| 1 | **ACUMULAÇÃO INFORMADA** | `insider_P_30d > 0` **e** `Eco ≥ 1,5` | É diluição disfarçada? → shelf/ATM, saldo de vendas | 2 |
| 2 | **REVERSÃO CONFIRMADA** | `B_rsi` **e** (`B_macd` ∨ `B_bounce`) **e** `Eco ≥ 1,5` | A reversão tem causa ou é ressalto técnico? | 3 |
| 3 | **BASE A TESTAR RESISTÊNCIA** | `C≥2 componentes` **e** `dist_resistencia ≥ −10%` **e** `extensao ≤ +15%` | Quem vende no nível, e porquê? | 2 |
| 4 | **EVENTO ÚNICO** | `Eco ≤ 1,15` **e** `RVOL ≥ 2` | O que aconteceu, é durável, já está no preço? | 7 |
| 5 | **CONTINUAÇÃO DE EVENTO** | `Eco ≥ 1,5` **e** `A` | Quem continua a comprar depois do dia grande? | 12 |
| 9 | **NÃO CLASSIFICADO** | residual | — | 22 |

**Resultado medido: residual desce de 54% para 46%.** Melhoria real mas insuficiente.

**Diagnóstico do residual (22 candidatos):** **14 têm `Eco` entre 1,15 e 1,5** — nem o evento é hoje, nem houve um dia claramente maior. Estão numa zona morta entre os setups 4 e 5. Oito têm `Eco ≤ 1,15` mas `RVOL < 2`.

**NÃO RESOLVIDO — exige decisão.** Duas saídas, e recuso escolher sozinho:
- **(a)** Baixar o corte de `RVOL` do setup 4 de 2 para 1,5 → recupera 4 dos 22. Mas 1,5 seria escolhido para reduzir o residual, que é overfitting pelo mesmo mecanismo do R9 que rejeitei.
- **(b)** Aceitar que a zona `Eco ∈ [1,15; 1,5]` **não é um setup**. Um candidato sem pico recente nem evento hoje pode simplesmente não ter tese. Nesse caso o residual é resposta, não falha — e o tecto de 10 nunca lá chega.

Inclino-me para (b), mas é decisão tua.

---

## 5. Ordenação determinística

**Sem score agregado.** Três níveis, aplicados por ordem:

1. **Precedência de setup** — 1 a 5, pela ordem da tabela. O setup 9 nunca entra na shortlist final.
2. **Nível de confirmação** dentro do setup — `n_sinais` (1, 2 ou 3), decrescente.
3. **Desempate declarado** — `AvgVolUSD_63` decrescente. **Escolhido por ser a única variável do funil que não é usada em nenhuma regra de classificação**, o que a torna ortogonal e não circular. Registado em `desempate_aplicado`.

Empates remanescentes ficam empatados e são assinalados. **Nenhuma ordem implícita.**

**Tecto duro de 10.** Excedente vai para `saida_reserva.csv` com `razao_corte`. Menos de 5 → `razao_lista_curta` obrigatória.

**A ordem invertida das prioridades (R10) está incorporada nos setups 1 e 2**, mas continua **PROPOSTA**: o critério de promoção exige 5 sessões, das quais ≥2 sem o BYRN na shortlist. Em 30-07, os setups 1 e 2 dão 5 candidatos — BYRN, HDSN, NG, OPK, SIGA — pelo que a regra já produz resultado sem depender só do BYRN. **Uma sessão não é validação.**

---

## 6. Observabilidade

Registado por corrida em `metricas.json`:

- **Funil:** sobreviventes após cada gate; **removidos em exclusivo por cada gate** (o teste que reprovou o Critério 8)
- **Estabilidade:** sobreposição da shortlist e da ordenação com a sessão anterior
- **Concentração:** `concentracao_top_sector_pct`, `n_industrias`, flag se >50%
- **Missingness:** por campo e por fonte; contagem de cada um dos seis estados
- **Custo:** chamadas por fornecedor, tempo total, percentagem de quota usada
- **Classificação:** distribuição por setup, `residual_pct`
- **Qualidade:** divergências entre fontes, casos `DATA_INVALID`, anomalias de B8
- **Macro:** regime FRED e índice de stress

---

## Handoff — Fase 3

**Decisões fechadas:** sete fases com contratos de entrada e saída; seis estados nunca colapsáveis; tabela de fontes com fallback, comparador e freshness; taxonomia de cinco setups com precedência lexicográfica e pergunta de falsificação por setup; ordenação em três níveis sem score, com desempate declarado e justificado; tecto de 10; conjunto de observabilidade.

**Evidência utilizada:** a taxonomia foi **medida**, não proposta às cegas — corrida sobre os 48 sobreviventes de 29-07 pós-T1 e T2, com dados de insiders reais.

**Decisões provisórias:** os limiares `Eco ≥ 1,5`, `Eco ≤ 1,15` e `RVOL ≥ 2` na classificação derivam de duas sessões. O `MAX_SPREAD_PCT = 2%` é sustentado por 17 observações de uma única sessão e entra como gate **com revisão marcada** para 5 sessões.

**Questões abertas:** a decisão (a)/(b) sobre a zona morta do `Eco`. E a **profundidade do livro** — o eixo que a amostra de spreads mostrou ser o mais discriminante (NRXS com bid de 1 acção, ENGS com ask de 18) — não está especificado em lado nenhum. Não tenho amostra para o calibrar.

**Inputs necessários para a Fase 4:** decisão sobre a zona morta. Confirmação de que o desempate por `AvgVolUSD_63` é aceitável, ou proposta alternativa.

**Riscos de avançar:** a Fase 4 converte isto em backlog. Se a decisão da zona morta for (a), a regra do setup 4 muda e o backlog muda com ela.

**Condição para iniciar a Fase 4:** resposta a (a) ou (b).
