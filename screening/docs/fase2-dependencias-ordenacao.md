# Fase 2 — Dependências e ordenação

**Data:** 30 de julho de 2026 · **Base:** Fase 1 + medições sobre a corrida de 29-07
**Ratificações aplicadas:** tectos de custo (4 h backfill / 10 min corrida) e política de falha por tipo de componente.

---

## 1. Grafo de dependências

Dependências **técnicas** — o que é impossível calcular antes do quê. Não preferências.

```
[guarda de calendário]
        │
        ├──────────────────────────────────────────────┐
        ▼                                              ▼
[referência de tickers]                          [OHLCV grouped]
   type, exch, nome                               fechos e volumes
        │                                              │
        └───────────────┬──────────────────────────────┘
                        ▼
              [corporate actions: splits]  ◄── RAIZ CONTAMINANTE
                        │
        ┌───────────────┼───────────────┬──────────────────┐
        ▼               ▼               ▼                  ▼
[integridade de     [indicadores]   [range 52s]      [acções em
 série/quarentena]   RSI SMA20       máx/mín          circulação]
        │             RVOL Eco       truncado          (split altera)
        │             mediana            │                  │
        └───────┬─────────┘               │                  │
                ▼                         │                  │
        [gates técnicos]                  │                  │
       preço, volume, RSI,                │                  │
       SMA20, RVOL                        │                  │
                │                         │                  │
                ▼                         │                  │
        [sinais A/B/C]                    │                  │
                │                         │                  │
                ▼                         │                  │
          ═══ SHORTLIST ═══               │                  │
                │                         │                  │
                ▼                         │                  │
        [identidade + CIK + tier] ────────┼──────────────────┤
                │                         │                  │
        ┌───────┴────────┐                │                  ▼
        ▼                ▼                │          [market cap → gate]
[red flags EDGAR]  [enriquecimento]       │
 going concern      insiders, notícias    │
 8-K itens          breakout, diluição    │
        │                                 │
        ▼                                 │
      [P4] ◄──────────────────────────────┘
        │
        ▼
   [ordenação] ──► [observabilidade: macro, concentração, tripwire]
```

**Três raízes independentes** (calculáveis sem nada a montante): guarda de calendário, referência de tickers, macro FRED.

**Uma raiz contaminante:** corporate actions. Um reverse split altera simultaneamente a série de volume, a interpretação do RVOL, o range de 52 semanas e as acções em circulação. **Tudo o que dele depende é inválido se ele correr depois.**

**Um estrangulamento:** identidade. O CIK é necessário para as acções da SEC (market cap) e para os filings (red flags). Nada de per-candidato caro pode correr antes dela.

---

## 2. Ordem actual vs proposta

| Pos. actual | Componente | Pos. proposta | Dependências reais | Justificação | Impacto medido | Teste |
|---|---|---|---|---|---|---|
| 0 | Macro FRED | **G1** | nenhuma | não é gate; é contexto. Correr no fim evita 5 chamadas em corridas abortadas | −5 chamadas em falhas precoces | nenhum |
| 1 | Universo Polygon + calendário | **A1-A2** | — | inalterado | — | — |
| — | **Corporate actions (splits)** | **A3 (novo)** | referência | **raiz contaminante**. Hoje corre na etapa 9 | **156 dos 932 elegíveis** têm split em 365 d; **72 em 90 d**. Na shortlist: 7 e 4 | Ablação de posição |
| 2 | Integridade / quarentena | **A4** | OHLCV, calendário | inalterado | — | — |
| 2 | Gates técnicos (preço, vol, RVOL, RSI, SMA20) | **B1-B6** | quarentena, splits | ver §3 para a ordem interna | — | — |
| — | **Gate de volume USD** | **B2b (novo)** | preço, OHLCV | filtro mais barato que existe; zero chamadas | **remove 205 de 932** (22%) | Ablação com/sem |
| 3 (Finnhub) | Range 52 semanas | **B7** | OHLCV 252, splits | passa a calculado e a **feature** (Fase 1) | elimina dependência do Finnhub num input inválido | Comparar com Finnhub |
| — | **Sinais A/B/C** | **B8 (novo gate ≥1)** | indicadores | filtro gratuito antes de qualquer chamada por candidato | remove 1 (SOUN) | Ablação |
| 5 | Identidade + CIK + tier | **C1** | shortlist, referência | **sobe 4 posições**. É o estrangulamento: sem CIK não há SEC nem EDGAR | 1-2 chamadas/candidato, baratas | — |
| 3-4 | Market cap → gate | **D1** | identidade (CIK), splits, preço | fonte muda para SEC (A9); split altera acções | 22/67 divergentes hoje | Ablação de fonte |
| 3 | Regime de reporte | **D2** | CIK | inalterado na lógica | — | — |
| 9 | Red flags EDGAR | **E1** | CIK | mantém-se tarde: é caro e não contamina nada | 2 chamadas/candidato | — |
| 4 | P4 queda sem recuperação | **E2** | range calculado (B7) | **depende agora de B7, não do Finnhub** | 6 excluídos hoje, 3 em exclusivo | Recalcular |
| 6 | Encaminhamento evento/continuação | **F1** | indicadores | inalterado | — | — |
| 7-8, 10 | Filas e descoberta precoce | **F2-F4** | shortlist, identidade | inalterado | — | — |
| — | Ordenação com tecto 10 | **G2** | tudo | — | — | Shadow run |
| 11 | Tripwire | **G3** | shortlist, calendário | inalterado; só válido pós-fecho | — | — |

**Cinco deslocações**, todas justificadas por dependência técnica: splits para o topo, identidade para antes do enriquecimento, range para calculado, market cap para depois da identidade, macro para o fim.

---

## 3. Ordem interna dos gates técnicos (B)

Regra: **eliminar mais cedo o que custa menos calcular**, sem violar dependências.

| Ordem | Gate | Custo | Sobreviventes (29-07) |
|---|---|---|---|
| B1 | Preço $1-7 | trivial | 1.225 |
| B2a | Volume acções >100k | trivial | 932 |
| **B2b** | **Volume USD >$1M** | trivial | **727** |
| B3 | Cálculo de indicadores | médio (63 sessões × N) | 727 |
| B4 | RVOL >1,2× | trivial | ~95 (estimado) |
| B5 | RSI ≤60 | trivial | — |
| B6 | SMA20 >−15% | trivial | ~52 (estimado) |
| B7 | Range 52s (feature, não filtra) | alto (252 sessões) | — |
| B8 | Sinais A/B/C ≥1 | médio | ~51 (estimado) |

**Nota sobre B2b:** colocar o gate USD antes do cálculo de indicadores poupa o cálculo de RSI, SMA20 e RVOL para 205 candidatos. É a maior poupança de computação do pipeline e custa zero chamadas.

**Nota sobre B7:** o range é caro em cache mas gratuito em runtime depois do backfill. Fica depois dos gates porque é feature — não filtra ninguém, só informa o P4 mais à frente.

**Estimativa, não medição.** Os sobreviventes de B4 a B8 são extrapolados do funil de 29-07 aplicando o novo gate USD. **Não foram medidos** — a corrida com a nova ordem ainda não existe. Marcado como NÃO RESOLVIDO até ao shadow run.

---

## 4. Política de falha por componente

Ratificada. Aplicação concreta:

| Fase | Componente | Falha de rede | Dado ausente | Dado inválido |
|---|---|---|---|---|
| A3 | Splits | **BLOQUEIA** — `VERIFICACAO_INCOMPLETA`, corrida aborta | n/a | n/a |
| A4 | Quarentena | n/a | etiqueta (`SERIE_CURTA`, `INTERRUPCAO`, `ILIQUIDEZ`) | — |
| B1-B6 | Gates técnicos | n/a | **PÕE DE LADO** — `DATA_INSUFFICIENT` | põe de lado |
| B7 | Range | n/a | `range_estado = DATA_INSUFFICIENT` → E2 não decide | idem |
| B8 | Sinais A/B/C | n/a | **ANOMALIA** — põe de lado *e* regista alerta | idem |
| C1 | Identidade | põe de lado | põe de lado | `REVER` (3.º estado, já implementado) |
| D1 | Market cap | põe de lado | SEC ausente → fallback Finnhub com etiqueta; ambos ausentes → põe de lado | `DESACTUALIZADO` se >120 dias |
| E1 | Red flags EDGAR | **BLOQUEIA** — `FALHA_REDE`, não aprovado | `A_REVER`, não aprovado | não aprovado |
| E2 | P4 | n/a | não decide se `range_estado ≠ OK` | não decide |
| F2-F4 | Features | **DEIXA PASSAR** com etiqueta | `SEM_FONTE` ≠ `SEM_SINAL` ≠ `FALHA_REDE` | etiqueta |
| G | Observabilidade | deixa passar | métrica ausente | — |

**Distinção obrigatória, nunca colapsada:** dado ausente · dado inválido · dado desactualizado · fontes divergentes · falha de rede · candidato legitimamente fora do critério. Seis estados, seis campos de log.

**Uma consequência a assumir:** A3 é o único componente que **aborta a corrida inteira**. Se o Polygon não devolver splits, nada a jusante é confiável — os indicadores seriam calculados sobre séries potencialmente quebradas. É a contrapartida de ele ser a raiz contaminante.

---

## 5. Análise de custo

### Backfill único
| Item | Chamadas | Tempo | Tecto |
|---|---|---|---|
| OHLCV 252 sessões (faltam 181) | 181 | **~39 min** a 13 s | 4 h ✅ |

O tempo real é muito inferior à estimativa anterior de 3h20 — a cache já tem 71 sessões.

### Corrida normal (cache quente, base de 29-07)
| Fase | Chamadas | Notas |
|---|---|---|
| A1-A2 calendário + referência | 12 | 1/corrida |
| A3 splits | 2 | 1/corrida, universo inteiro |
| A4 OHLCV sessão nova | 1 | |
| B1-B8 | **0** | tudo local |
| C1 identidade + tier | ~102 | 2/candidato × 51 |
| D1 market cap SEC | ~51 | 1/candidato, 10/s, sem chave |
| D2 regime | ~51 | Finnhub |
| E1 red flags EDGAR | ~102 | 2/candidato |
| E2 P4 | 0 | local |
| F2-F4 enriquecimento | ~150 | insiders, notícias, breakout |
| G1 macro | 5 | |
| G3 tripwire | ~30 | só pós-fecho |
| **Total** | **~510** | |

**Tempo estimado: 6 a 8 minutos**, dominado pelo pacing do Finnhub (1,35 s) e do EDGAR (0,4 s + backoff). Dentro do tecto de 10 minutos.

**Comparação com a ordem actual:** hoje entram 67 candidatos no enriquecimento; com B2b e A3 entram ~51. **Redução de ~24% nas chamadas por candidato** — cerca de 120 chamadas poupadas por corrida, e o AMIX deixa de consumir enriquecimento antes de ser reprovado.

**Reserva de quota:** com 51 candidatos, o Finnhub usa ~250 chamadas a 1,35 s ≈ 44/min contra o limite de 60 — dentro da reserva de 25%. O Marketaux gasta ≤30 de 100/dia.

---

## 6. Testes de ablação necessários

| ID | Teste | Pergunta | Critério de aceitação |
|---|---|---|---|
| T1 | **Posição de A3** — splits no topo vs na etapa 9 | O AMIX é removido antes do enriquecimento? Quantas chamadas se poupam? | AMIX fora antes de C1. Poupança ≥15% das chamadas por candidato |
| T2 | **Gate USD com/sem** | O que remove e o que perde | Remove 15-25% da base. **Nenhum removido com insider P + RVOL≥3** |
| T3 | **Fonte de market cap** — SEC vs Finnhub | Quantos DIVERGENTE passam a COERENTE | <5% divergentes. NKLR excluído a $540M |
| T4 | **Range calculado vs Finnhub** | Quantos casos inválidos desaparecem | Zero mínimos acima do preço. Divergências explicáveis por split em 100% |
| T5 | **P4 sobre range corrigido** | A lista de 6 exclusões muda? | Cada exclusão justificável candidato a candidato |
| T6 | **Gate A/B/C ≥1** | Quantos remove | 0-10%. Se >10%, é gate a sério e exige revisão |
| T7 | **Sinal C com ≥2 componentes** | A prevalência cai para uma faixa útil? | Entre 20% e 50% |
| T8 | **Limiares de RVOL** 1,0 / 1,2 / 1,5 | Sensibilidade do gate estruturante | Não alterar sem 5 sessões |
| T9 | **Piso do RSI** 25 / 20 / sem piso | Contribuição marginal do piso | ≤5% de alteração → converter em feature |
| T10 | **Ordem de prioridades** original vs invertida | R10 é promovível? | Escalão 1 não vazio e ≤3 em ≥4 de 5 sessões, **incluindo ≥2 sem BYRN** |
| T11 | **Injecção de 503** na SEC e no Polygon | O backoff resiste? | Corrida completa sem interrupção |
| T12 | **Redundância entre gates** | Quantos remove cada gate em exclusivo | Nenhum gate com contribuição exclusiva zero em ≥3 sessões |

**T12 é o teste que já reprovou o Critério 8** (contribuição exclusiva zero em 29-07) e é o critério que deve ser aplicado a todos os gates de forma contínua, não pontual.

---

## Handoff — Fase 2

**Decisões fechadas:** grafo de dependências com três raízes independentes, uma raiz contaminante (corporate actions) e um estrangulamento (identidade); cinco deslocações justificadas por dependência técnica e não por preferência; ordem interna dos gates técnicos por custo crescente; política de falha instanciada componente a componente com seis estados distintos; análise de custo dentro dos dois tectos ratificados.

**Evidência utilizada:** medições sobre a corrida de 29-07 — 205 removidos pelo gate USD sobre a base de 932; 156 candidatos com split em 365 dias e 72 em 90 dias na base elegível; 7 e 4 respectivamente na shortlist de 67.

**Decisões provisórias:** os sobreviventes estimados de B4 a B8 (~95, ~52, ~51) são extrapolações, não medições. A ordem interna de B4-B6 assume que o RVOL continua a ser o gate estruturante, o que é verdade nas duas sessões mas não foi testado com a nova base pós-USD.

**Questões abertas:** o efeito do gate USD sobre a composição da shortlist é desconhecido — remove 22% da base, mas não sabemos se remove candidatos que teriam sinais fortes. T2 responde. A exclusão por split ≤90 dias é uma regra nova sem precedente: remove 72 dos 932, e não está demonstrado que todos mereçam exclusão em vez de flag.

**Inputs necessários para a Fase 3:** confirmação de que a exclusão por split ≤90 dias é exclusão e não flag. Sem isso, a Fase 3 especifica um estado que pode mudar. Segundo: a taxonomia de setups — a Fase 3 tem de a definir, e é a única peça que não deriva de nada do que já existe.

**Riscos de avançar:** a Fase 3 vai especificar contratos de entrada e saída por fase. Se T1 e T2 revelarem que as deslocações têm efeitos não previstos, os contratos mudam. Especificar antes de medir é a ordem inversa da que este projecto tem seguido.

**Condição para iniciar a Fase 3:** decisão sobre split ≤90 dias (exclusão vs flag). Recomendo, adicionalmente, correr T1 e T2 antes da Fase 3 — são baratos, locais, e as suas respostas mudam a especificação.
