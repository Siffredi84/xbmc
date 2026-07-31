# Fase 0 — Reconstrução do registo de decisões

**Data:** 30 de julho de 2026
**Corridas de referência:** sessões de fecho de 28-07-2026 e 29-07-2026
**Âmbito:** exclusivamente registo factual. Nenhuma arquitectura proposta.

---

## 1. Objectivo canónico — validado com cinco divergências

O objectivo canónico provisório é **aceite como enunciado**, com uma ressalva de método: os seis pontos que o compõem não são todos rastreáveis ao framework original. Três emergiram das corridas. Isso não os invalida, mas devem ser registados como acrescentos e não como leitura do documento.

| # | Divergência | Framework original | Objectivo canónico | Classificação |
|---|---|---|---|---|
| D1 | Cardinalidade da shortlist | *"Selecção Final: Escolhe 5-10"* + *"Exemplo de Output Ideal"* com exactamente 5 tickers nomeados | 5-10 é alvo operacional, não quota; pode devolver menos | **CONTRADIÇÃO** — o original trata como entregável esperado |
| D2 | Fiabilidade dos dados como objectivo | ausente | *"possuam dados suficientemente fiáveis para justificar análise"* | **ACRESCENTO** vindo das corridas |
| D3 | Taxonomia de setups | sinais A/B/C + 4 prioridades, sem classe de setup | *"classificadas segundo um setup reconhecível"* | **ACRESCENTO** — não existe no original |
| D4 | Natureza do sistema | workflow manual multi-ferramenta, *"30-45 minutos para 50-100 acções"* | pipeline determinístico automatizado | **DIVERGÊNCIA ESTRUTURAL** aceite implicitamente, nunca formalizada |
| D5 | Papel do sector | critério de selecção final (Tier 1/Tier 2) | métrica de observabilidade (ver Critério 10) | **PROPOSTA** decorrente da evidência |

**NÃO RESOLVIDO:** D1 exige decisão. Se 5-10 é alvo operacional, a corrida de 29-07 devolveu 26 candidatos com ≥2 sinais e é conforme; se é quota, é uma falha de 260%.

---

## 2. Inventário funcional dos Critérios 1–13

| # | Critério | Tipo declarado hoje | Tipo que a evidência sustenta | Implementado |
|---|---|---|---|---|
| 1 | Preço $1–$7 | hard gate | hard gate + feature de risco de listagem | ✅ |
| 2 | Market cap $50–500M | hard gate | hard gate + flag de proveniência | ✅ (P2) |
| 3 | Volume médio >100k | hard gate | hard gate incompleto (falta eixo USD) | ⚠️ parcial |
| 4 | NYSE/NASDAQ/AMEX | hard gate | hard gate + feature de tier | ✅ (P5) |
| 5 | RSI(14) 25–60 | hard gate bilateral | hard gate unilateral (só tecto) | ✅ |
| 6 | Preço vs SMA20 >−15% | hard gate unilateral | hard gate + flag de extensão | ✅ |
| 7 | RVOL >1,2× | hard gate | hard gate + feature de pico recente | ✅ |
| 8 | ≤90% do máximo 52s | hard gate | candidato a feature; dados inadequados | ✅ mas suspeito |
| 9 | ≥1 sinal A/B/C | gate declarado | não aplicado; hoje é feature | ❌ |
| 10 | Tier 1/Tier 2 | filtro de priorização | observabilidade | ❌ |
| 11 | Red flags (6 itens) | exclusão estrutural | exclusão + corporate action mal posicionada | ⚠️ 4 de 6 |
| 12 | Descoberta precoce (5 itens) | bonus/feature | feature | ⚠️ 2 de 5 |
| 13 | Selecção final + prioridade | regra de ranking | taxonomia incompleta | ❌ |

**Contagem:** 6 conformes, 4 parciais, 3 não implementados.

---

## 3. Matriz resumida de evidência

| # | Poder discriminatório | Qualidade dos dados | Evidência-chave (28-07 → 29-07) |
|---|---|---|---|
| 1 | Forte (define o universo) | Fiável (8/8 vs Yahoo) | 38 excluídos em $0,90-1,00 vs 14 em $7,00-7,10 |
| 2 | Forte (32 de 67) | **Condicional** | 22/67 divergentes; TOP $78M vs $1.305M; NKLR errado no sentido inverso |
| 3 | Moderado | Fiável (desvio 0,1%) | 15/67 abaixo de $1M/dia; JBDI a $0,15M |
| 4 | Nulo (1 de 5.300) | Fiável (67/67) | 38 dos 67 em NasdaqCM/GM |
| 5 | Moderado, assimétrico | Fiável, mas convergência ±5 pts | 9 cortados, todos acima de 60; 0 abaixo de 25 |
| 6 | **Forte** (32 de 99) | Fiável | −20%→81, −15%→67, −10%→52 |
| 7 | **Muito forte** (933→122) | Fiável mas semanticamente frágil | mediana do universo 0,59; AMIX 171×, média/mediana 38× |
| 8 | **Nulo** (1 de 67) | **Inadequada** | mínimo Finnhub do EU acima do preço; HCTI 1225 vs 612 |
| 9 | Desconhecido (não aplicado) | Fiável | B: 21,1% antes vs 28,4% depois; SOUN sem sinal e aprovado |
| 10 | Não aplicado | Fiável | biotech 67% → 37%; universo 31% |
| 11 | Forte (3 reprovados) | Mista | AMIX split 21:1 detectado tarde; SEC 503 esgotou backoff |
| 12 | Fraco (2 de 27 com sinal) | Condicional | 23 A/M ignoradas; analistas None em 27/27 |
| 13 | Nulo (taxonomia incompleta) | n/a | 14 de 26 no escalão residual |

### Reconciliação exacta do funil de 29-07 (item aberto do Critério 11)

```
universo Polygon                 13.479 tickers
  type=CS + bolsa (P5)            5.299
  série íntegra (quarentena)      4.784        (504 em quarentena)
  preço $1-7 + vol >100k            933
  RVOL >1,2×                        122
  RSI 25-60 + SMA20 >-15%            67   ← shortlist
```

Da shortlist (67) para finalistas (32), com sobreposições explícitas:

| Falha | Contagem |
|---|---|
| market cap fora da banda | 32 |
| 52W high >−10% | 1 (CCO) |
| P4 queda sem recuperação | 6 |
| **união** | **35** |
| sobrevivem | **32** |

Sobreposição: `mcap ∩ P4` = 3 (BRAI, HCTI, XXI). P4 exclusivo = 3 (EU, TLRY, UPB). 52W exclusivo = 0.

Dos 32 finalistas: 3 reprovados (AMIX split, NKLR item 3.01, PYPD going concern), 2 FALHA_REDE (ABEO, ACB), **27 aprovados**. Destes, 26 com ≥2 sinais A/B/C.

**A soma 32+1+6=39 ≠ 35 é explicada pelas sobreposições acima.** Nenhuma contagem estava errada; faltava a reconciliação.

---

## 4. Alterações já implementadas

**IMPLEMENTADO** e confirmado por execução nas duas sessões:

| ID | Alteração | Verificação |
|---|---|---|
| P1 | Insiders: só `transactionCode=P`, janela 30 dias; A/M contadas em campo separado | 23 A/M ignoradas; BYRN e HDSN os únicos com compra real |
| P2 | Market cap canónico = `shareOutstanding × preço USD`; Finnhub como comparador; `MCapEstado` | 22/67 etiquetados DIVERGENTE |
| P3 | Reverse split via `/v3/reference/splits` do Polygon; falha da fonte → `VERIFICACAO_INCOMPLETA` | AMIX 21:1 de 24-06 detectado |
| P4 | Exclui se queda >80% **e** recuperação desde o mínimo <15% | 6 excluídos; BYRN preservado a +36,8% |
| P5 | `type == CS` **e** `exch ∈ {XNAS,XNYS,XASE}` | CBOE removido; deixou de depender do endpoint |
| N4 | Polygon `_get`: backoff exponencial em 5xx (antes só 429) | 503 no primeiro pedido de 29-07 matava o pipeline |
| — | Cache Finnhub com hash dos parâmetros | corrigia contaminação silenciosa da janela do P1 |
| — | Guarda de calendário | primeiro teste real em 29-07: passou |

**Nota de proveniência:** o hash da cache do Finnhub foi introduzido pelo trabalho de correcção, não por mim, e corrigiu um defeito que teria anulado o P1 sem qualquer sinal.

---

## 5. Decisões activas

| # | Decisão | Origem | Estado |
|---|---|---|---|
| A1 | Janela de volume: 63 sessões (não 30) | comparabilidade com Finviz e histórico EL | **DECISÃO ACEITE** — contradiz a letra do documento original |
| A2 | Universo por cotação, não domicílio; campo `regime_reporte` 10-Q vs 20-F | leitura literal de "listadas em NYSE/NASDAQ/AMEX" | **DECISÃO ACEITE** |
| A3 | Emissores 20-F entram, mas red flags falham por omissão neles | não existe 10-Q para verificar | **DECISÃO ACEITE** |
| A4 | Encaminhamento evento vs continuação pelo rácio Eco (pico 20d ÷ RVOL hoje) | perguntas de falsificação distintas; poupa quota Marketaux | **DECISÃO ACEITE** |
| A5 | Excluir closed-end funds e SPACs | consequência de `type == CS` | **DECISÃO ACEITE** |
| A6 | Quarentena por sessões em falta acima da linha de base (>3) | ver A8 | **DECISÃO ACEITE** |
| A7 | Volatilidade 20d é flag, não gate | BYRN a 171% ≠ TLRY a 36% | **DECISÃO ACEITE** |
| A8 | **Princípio invariante:** dados em falta produzem etiqueta, nunca decisão | 6 falhas reais com a mesma forma | **DECISÃO ACEITE** — restrição transversal |
| A9 | Acções em circulação passam a vir da SEC (XBRL `companyconcept`); Finnhub → comparador | NKLR: 110,5M SEC vs 70,3M Finnhub | **DECISÃO ACEITE**, não implementada |
| A10 | Manter A/B/C **depois** dos gates técnicos | ver S1 | **DECISÃO ACEITE** (reafirmada) |

---

## 6. Decisões SUPERSEDED

**S1 — Avaliar sinais A/B/C antes dos gates técnicos**

- *Razão original (29-07, manhã):* com 21 finalistas, o Sinal B disparava 8 vezes; inferi que os gates de SMA20 e RVOL eliminavam a população onde a reversão vive, tornando o Sinal B inaplicável.
- *Evidência que a contrariou (29-07, tarde):* sobre 932 candidatos da base pós-preço-volume, o Sinal B ocorre em **21,1%**; sobre os 67 pós-gates, em **28,4%**. O componente RSI-oversold triplica (4,5% → 14,9%) e o bounce em suporte duplica (7,5% → 16,4%). Os gates **concentram** o padrão.
- *Regra que permanece activa:* A10 — A/B/C depois dos gates técnicos.
- *Registo:* já marcada como SUPERSEDED na memória do projecto.

**S2 — "O funil duplica a concentração biotech"**

- *Razão original (29-07, manhã):* shortlist com 67% biotech/pharma contra 31% no universo elegível; atribuí a mecanismo causal (eventos clínicos geram picos de volume).
- *Evidência que a contrariou (29-07, tarde):* a shortlist de 67 candidatos apresenta **37%**, próximo dos 31% do universo. A inferência anterior assentava em 21 observações.
- *Regra que permanece activa:* nenhuma. A concentração sectorial passa a métrica de observabilidade (Critério 10).
- *Classificação da hipótese:* **NÃO RESOLVIDO** — duas sessões não distinguem variância amostral de enviesamento intermitente.

**S3 — "Volumes não são comparáveis entre fontes"**

- *Razão original:* BYRN com 2.488.990 no Polygon contra 2.084.547 na IBKR.
- *Evidência que a contrariou:* Polygon e Yahoo concordam a 0,1% de desvio mediano em 8 amostras. O outlier é a IBKR, que consolida de forma diferente.
- *Regra que permanece activa:* usar uma fonte de volume e não misturar; mas a afirmação sobre incomparabilidade geral era falsa.

---

## 7. Propostas não validadas

**PROPOSTA** — nenhuma destas está aprovada nem implementada.

| ID | Proposta | Critério | Evidência de apoio | Risco de overfitting |
|---|---|---|---|---|
| R1 | Flag de risco de conformidade de listagem abaixo de $1,20, cruzada com tier | 1, 4 | 38 excluídos junto a $1; 38/67 em NasdaqCM/GM | Baixo — mecanismo regulatório conhecido, não ajuste a dados |
| R2 | Aplicar `MIN_USD_VOL_90D` a par do gate em acções | 3 | 15/67 abaixo de $1M/dia | Baixo — limiar já no config, não derivado das corridas |
| R3 | Range de 52 semanas calculado do OHLCV Polygon | 8, 11 | mínimo do EU acima do preço; HCTI 1225 vs 612 | Nulo — correcção de invalidez |
| R4 | Guardar mediana de volume; flag se média/mediana >5× | 3, 7 | AMIX 408.244 vs 10.814 | **Médio** — limiar de 5× derivado de um caso |
| R5 | Flag de extensão acima de +15% da SMA20, cruzada com posição no range | 6 | DCX +18,9% e a 71% do mínimo; VRRM +20,3% em título saudável | **Médio** — dois casos, um por sessão |
| R6 | Sinal A reformulado: 2× ao pico de 20 dias, não ao dia corrente | 7, 9 | 23 cumprem literal vs 44 reformulado | Baixo — reconcilia gate e sinal do próprio documento |
| R7 | Corporate actions antes dos indicadores técnicos | 11 | AMIX consumiu enriquecimento antes de ser reprovado | Baixo — dependência técnica, não ajuste |
| R8 | Aplicar a regra "≥1 sinal A/B/C" | 9 | SOUN aprovado sem sinal | Baixo |
| R9 | Apertar consolidação lateral de 1,6× para ~1,3× | 9 | dispara em 40/67 (60%) e 17/21 (81%) | **Alto** — limiar escolhido para produzir prevalência desejada |
| R10 | Inverter ordem de prioridades (insider+reversão → consolidação+breakout → volume+sector) | 13 | escalões 2 e 3 vazios na ordem original nas duas sessões | **Alto** — ver secção 8 |
| R11 | Backoff mais longo para a SEC | 11 | 503 esgotou 5 tentativas; 200 imediato à mão | Nulo |
| R12 | Piso do RSI: manter, remover ou converter em feature | 5 | 0 cortados em 29-07, 2 em 28-07 | Baixo |
| R13 | Earnings calendar do Finnhub para o 4.º nível de prioridade | 13 | escalão residual com 14 de 26 | Baixo |

---

## 8. Contradições e inconsistências

**C1 — Gate de RVOL (1,2×) vs Sinal A do documento (2×+).** Nas duas sessões, mais de um terço da shortlist passa o gate de actividade sem cumprir o sinal de actividade definido no mesmo documento. 26/67 entre 1,2 e 1,5. **NÃO RESOLVIDO.**

**C2 — Especificação de breakout: 2-3 toques vs código 2-8.** O SEER qualifica com 4 toques. Divergência introduzida por mim durante a implementação, nunca decidida. **Exige decisão formal num dos dois sentidos.**

**C3 — Desempate por RVOL no ranking.** Introduzido em execução para produzir uma lista ordenada; não existe na especificação. Viola a restrição 4.1 (ordenação sem critério declarado). **Exige especificação ou remoção.**

**C4 — Janela de volume: documento diz 30 dias, código faz 63.** Decisão A1 é activa e consciente, mas o documento original nunca foi actualizado. Dois artefactos em contradição.

**C5 — O P4 assenta na fonte menos fiável do funil.** É a correcção mais recente e depende do mínimo de 52 semanas do Finnhub, que se demonstrou inválido para títulos pós-reverse-split — exactamente a população que o P4 visa. O EU foi excluído com um input impossível (mínimo acima do preço). **Excluiu pela razão certa por acaso.**

**C6 — "Aritmeticamente ajustado" ≠ "semanticamente válido".** DCX com máximo de 52 semanas de $3.408 e preço de $1,08 é correcto sob ajustamento de splits e inútil como sinal. A distinção não está formalizada em nenhum ponto do pipeline.

**C7 — `MAX_SPREAD_PCT` e `MIN_USD_VOL_90D` declarados e não aplicados.** Defeito D2 da primeira auditoria, aberto desde então. O código promete uma camada de execução que não existe.

**C8 — Critério 8 é gate com poder discriminatório nulo nas duas sessões.** Corta 3/50 e 1/67. Mantido por custo zero, mas ocupa a posição de gate sem exercer a função.

---

## 9. Lacunas de contexto

**CONTEXTO EM FALTA:**

| ID | Lacuna | Bloqueia |
|---|---|---|
| L1 | `alpha-k-data-pipeline` não foi fornecido | integrar os guards de rate limit e as classes de evidência (OFFICIAL/OBSERVED/INTERNAL/INFERRED) já existentes; substituir os guards primitivos actuais |
| L2 | Conector IBKR indisponível desde 30-07 | camada de execução (spread, USD-vol 90d, volume de opções); terceira fonte independente de identidade |
| L3 | Apenas 71 sessões de OHLCV em cache | range de 52 semanas calculado (R3) exige ~252; custo estimado 3,3 h de descarga inicial |
| L4 | Sem histórico de resultados posteriores | impossível medir falsos positivos/negativos reais; toda a avaliação é de coerência interna, não de rendibilidade |
| L5 | Fonte de cobertura de analistas | Finnhub free devolve HTML com 200; Twelve Data exige plano ultra |
| L6 | Fonte de menções sociais | nenhuma identificada |
| L7 | Fonte de calendário PDUFA | nenhuma gratuita identificada |
| L8 | Semântica de `dei:EntityCommonStockSharesOutstanding` | data de referência, classes múltiplas, múltiplos valores no mesmo filing — A9 não é implementável sem isto |
| L9 | Duas sessões consecutivas, ambas de verão, ambas com mercado em RISK_ON | nenhuma distribuição observada pode ser assumida estrutural |

---

## 10. Perguntas a responder antes da auditoria arquitectural

**Bloqueantes de Fase 1:**

1. **D1 — cardinalidade.** 5-10 é alvo operacional ou quota? Determina se o Critério 13 é uma falha ou está conforme.
2. **C2 — breakout.** 2-3 toques (documento) ou 2-8 (código)? Uma das duas fontes tem de mudar.
3. **C4 — janela.** O documento original é actualizado para 63 sessões, ou a decisão A1 é revertida?
4. **A9 — SEC.** As oito questões de semântica XBRL (L8) são respondidas por quem? Sem isso, a decisão aceite não é implementável.
5. **R10 — inversão de prioridades.** É promovida a decisão ou fica em teste? Duas sessões, ambas com o BYRN no topo, e a restrição 4.3 proíbe optimizar para ele.

**Bloqueantes de Fase 2:**

6. **Política de falha por componente.** A8 diz "etiqueta, nunca decisão", mas não distingue *fail-open*, *fail-closed* e `DATA_INSUFFICIENT`. Hoje o `edgar.py` faz fail-closed e o `evento.py` faz fail-open — sem que ninguém o tenha decidido.
7. **Orçamento de chamadas por corrida.** R7 (corporate actions primeiro) e R3 (range calculado) aumentam o custo a montante. Qual é o tecto aceitável?
8. **Critério 8.** Permanece gate, passa a feature, ou é removido? C8 sustenta as três leituras.

**Bloqueantes de Fase 5:**

9. **Snapshots.** A validação comparativa exige dados congelados. A cache Polygon é reproduzível; a Finnhub é indexada por sessão mas os valores mudam intra-sessão. Como se congela o estado do Finnhub para um shadow run?
10. **Critério objectivo de promoção do vNext.** Sem L4, "melhor" só pode significar coerência interna, cobertura de dados e explicabilidade — não qualidade de candidatos. Isto é aceitável como critério de promoção?

---

## Handoff — Fase 0

**Decisões fechadas:** objectivo canónico validado com cinco divergências registadas (D1-D5); inventário dos 13 critérios com tipo declarado vs tipo sustentado pela evidência; reconciliação exacta do funil de 29-07, incluindo as sobreposições que faltavam; oito alterações confirmadas como IMPLEMENTADAS; dez decisões activas (A1-A10); três SUPERSEDED documentadas com razão original e evidência contrária (S1-S3).

**Evidência utilizada:** exclusivamente o registo factual dos Critérios 1-13 fornecido, mais a reconciliação de contagens executada sobre os artefactos das duas corridas. Nenhum número foi inferido.

**Decisões provisórias:** treze propostas (R1-R13), das quais três marcadas com risco de overfitting médio a alto — R4 (limiar 5× de um caso), R9 (limiar escolhido para produzir prevalência) e R10 (inversão validada em duas sessões com o mesmo vencedor no topo).

**Questões abertas:** dez, agrupadas por fase bloqueada. Cinco impedem a Fase 1.

**Inputs necessários:** respostas às perguntas 1-5; `alpha-k-data-pipeline` (L1); decisão sobre o orçamento de chamadas (pergunta 7).

**Riscos de avançar sem isto:** a Fase 1 exige classificar cada critério como gate, feature, sinal ou confirmação. Sem resolver D1 e C2, dois critérios (13 e 12) não têm especificação de referência contra a qual ser auditados — a auditoria produziria uma classificação assente numa leitura minha, não numa decisão registada.

**Condição para iniciar a Fase 1:** respostas às perguntas 1, 2 e 3. As perguntas 4 e 5 podem ficar em aberto se forem explicitamente registadas como NÃO RESOLVIDO na Fase 1, mas nesse caso os Critérios 2 e 13 saem da Fase 1 sem alteração candidata.
