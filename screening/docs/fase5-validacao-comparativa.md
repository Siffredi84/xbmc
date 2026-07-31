# Fase 5 — Validação comparativa

**Data:** 30 de julho de 2026 · **Sessão de referência:** 29-07-2026
**Condição aceite:** o critério de promoção **não mede rendibilidade**. Sem histórico de resultados (lacuna L4), "superior" significa coerência interna, cobertura de dados e explicabilidade — nada mais.

---

## 0. Correcção obrigatória à Fase 3

**Cometi um erro na medição da taxonomia de setups e corrijo-o antes de qualquer comparação.**

Na Fase 3 apliquei a classificação aos **48 sobreviventes dos gates técnicos**, sem lhes aplicar os gates fundamentais (market cap e range de 52 semanas). A população incluía candidatos fora do universo — BHC a $1.748M, CLVT a $1.374M, ALVO a $1.102M.

**Números corrigidos:**

| Setup | Fase 3 (errado) | Corrigido |
|---|---|---|
| 1 Acumulação informada | 2 | **2** — BYRN, HDSN |
| 2 Reversão confirmada | 3 | **1** — SIGA |
| 3 Base a testar resistência | 2 | **1** — SEER |
| 4 Evento único | 7 | **4** — EPRX, GAU, TLRY, UROY |
| 5 Continuação de evento | 12 | **6** — ABEO, AVIR, DMAC, ENGS, NKLR, SNDL |
| 9 Não classificado | 22 | **12** |
| **Total** | 48 | **26** |

O residual mantém-se em 46% por coincidência. Mas o comentário da Fase 3 de que "os setups 1 e 2 dão cinco candidatos, portanto a regra não depende do BYRN" **fica invalidado**: dão **três** — BYRN, HDSN e SIGA — e dois deles são o mesmo par que aparece no setup 1. A restrição 4.3 continua tão viva como antes.

Os testes de integração da Fase 4 que citam "2/3/2/7/12/22" têm de ser actualizados para **2/1/1/4/6/12**.

---

## 1. Desenho do shadow run

| Parâmetro | Valor |
|---|---|
| Sessão | **29-07-2026** (fecho) |
| Universo inicial | 13.479 tickers, cache Polygon congelada |
| Snapshots | `snapshots/2026-07-29/` — Polygon OHLCV, referência, splits, Finnhub, EDGAR |
| Pipeline A | `run.py` actual, sem alterações |
| Pipeline B | `vnext/run.py` |
| Fontes externas | **nenhuma chamada nova** — ambos lêem do snapshot |

**Requisito absoluto:** o snapshot inclui as respostas da SEC para D-1. Sem elas o pipeline B corre em fallback Finnhub e a comparação mede outra coisa.

---

## 2. Divergência medida, candidato a candidato

**Pipeline A: 27 aprovados. Pipeline B: 26 elegíveis. Comuns: 20.**

### Sete só no A — todos pela mesma causa

| Ticker | USD/dia | Spread (30-07) |
|---|---|---|
| USIO | $0,30M | 2,36% |
| INVE | $0,58M | 1,10% |
| BTMD | $0,63M | 2,76% |
| CRDL | $0,67M | 0,82% |
| DTI | $0,75M | não medido |
| NRXS | $0,75M | **4,73%** |
| TOP | $0,50M | não medido |

**Todos os sete saem pelo gate de volume USD (B2b).** Nenhuma outra causa. O T2 verificou que a distribuição de sinais deste grupo é indistinguível da dos sobreviventes (Mann-Whitney, p entre 0,054 e 0,717) — o gate separa por liquidez, não por qualidade.

Cinco dos sete têm spread medido; **dois ultrapassam 2%** e o NRXS tem bid de **uma acção**.

### Seis só no B

ABEO, ACB, EU, NKLR, TLRY, UPB.

Aqui está a assimetria que importa: **ABEO e ACB estavam em `FALHA_REDE` no pipeline A** — não foram reprovados, foram não-verificados. **EU, TLRY e UPB foram excluídos pelo P4** com base no range do Finnhub, que demonstrámos ser inválido para esta população (o mínimo do EU vinha acima do preço). **NKLR** aparece em B porque o pipeline B ainda não tem o gate SEC implementado; com D-1, o NKLR passa a $540M e é **excluído** — logo o B deve produzir **25**, não 26.

**Conclusão da divergência:** o pipeline B não é mais permissivo. As seis entradas são, na sua maioria, exclusões do A que assentavam em dados inválidos ou em falhas de rede. As sete saídas são todas por um gate novo e validado.

---

## 3. Métricas comparativas

| Métrica | A | B | Direcção |
|---|---|---|---|
| Candidatos aprovados | 27 | 25-26 | — |
| Com setup atribuído | 0 (não existe) | 14 | **B** |
| Residual sem classificação | 100% | 46% | **B** |
| Ordenação explicável por regra nomeada | não (desempate por RVOL não especificado) | sim | **B** |
| Exclusões assentes em dados inválidos | ≥3 (EU, TLRY, UPB via P4) | 0 esperado | **B** |
| Candidatos não-verificados no output | 2 (`FALHA_REDE` misturados) | 0 (estado próprio) | **B** |
| Estados distintos de missingness | 3 | 6 | **B** |
| Chamadas por corrida | ~510 | ~430 estimado | **B** |
| Limiares com origem declarada | 0 | todos | **B** |
| **Qualidade das decisões de investimento** | **desconhecida** | **desconhecida** | **—** |

A última linha é a que importa e é a que não sabemos responder.

---

## 4. Critérios de promoção, revisão ou rejeição

### PROMOVER — todos obrigatórios

1. Todos os testes unitários e de integração passam sobre o snapshot congelado, com os números corrigidos (2/1/1/4/6/12).
2. **Cada divergência candidato a candidato é explicada por uma regra nomeada.** Zero divergências inexplicadas.
3. Zero aprovados com `DATA_INSUFFICIENT`, `DATA_INVALID` ou `DATA_STALE` num gate de elegibilidade.
4. Zero coerções entre os seis estados.
5. NKLR excluído; TOP a $78M; AMIX a $52M.
6. Corrida < 10 min com cache quente.
7. Toda a posição na ordenação explicável; zero desempates implícitos.
8. `metricas.json` produzido, inclusive em corridas de zero candidatos.

### REVER — qualquer um basta

- Divergência inexplicada em ≥1 candidato.
- Residual > 60% ou < 10%. Acima de 60% a taxonomia não classifica; abaixo de 10% classifica de mais e provavelmente por regras demasiado largas.
- Prevalência do sinal C fora de 20-50% com a regra "≥2 componentes".
- Gate com contribuição exclusiva **zero** em ≥3 sessões — o teste que reprovou o Critério 8.
- Taxa de `FALLBACK` no market cap > 20%.

### REJEITAR

- Um gate do B exclui um candidato que o A aprovava **e** a exclusão assenta em dado inválido ou em falha de rede não etiquetada.
- O adaptador IBKR (C-2) não é configurável: o vNext ficaria em modo degradado permanente com o Yahoo como fonte primária, o que anula a arquitectura tri-fonte e torna B arquitecturalmente inferior a A no eixo da identidade.

---

## 5. O que este desenho não consegue provar

**Nenhum critério acima mede se os candidatos do B são melhores investimentos.** O B é demonstravelmente mais rigoroso, mais explicável e assenta em dados mais fiáveis. Nada disso implica melhores retornos.

Três hipóteses ficam por testar, e todas exigem tempo:

- **O gate USD pode custar oportunidades.** Os sete removidos negoceiam entre $0,30M e $0,75M. Um deles pode duplicar. O T2 mostrou que os sinais são indistinguíveis — o que também significa que não há razão para crer que sejam piores.
- **O corte de splits ≤90 dias pode ser demasiado largo.** Remove 72 de 932. O AMIX caiu 23,6% no dia seguinte, mas isso é uma observação, não evidência.
- **A taxonomia pode estar a classificar ruído.** Cinco setups sobre duas sessões.

**O que recomendo, e é a única coisa que resolve isto:** correr A e B em paralelo durante ≥20 sessões, registar as duas shortlists, e só depois medir os retornos a 5, 10 e 20 dias de cada. Até lá, promover B é uma decisão sobre **qualidade de engenharia**, não sobre qualidade de selecção — e deve ser assumida como tal.

---

## Handoff — Fase 5

**Decisões fechadas:** correcção dos números da Fase 3; desenho do shadow run sobre snapshot congelado de 29-07 sem chamadas externas; divergência medida e explicada candidato a candidato (7 saídas por uma causa única e validada, 6 entradas maioritariamente por correcção de dados inválidos); tabela de métricas comparativas; três conjuntos de critérios — promover, rever, rejeitar.

**Evidência utilizada:** medições sobre as corridas de 29-07 e 30-07, incluindo a amostra de spreads de 17 tickers com o mercado aberto.

**Decisões provisórias:** o pipeline B produzirá 25 e não 26 assim que D-1 estiver implementado — por confirmar na execução.

**Questões abertas:** as três hipóteses da secção 5. Nenhuma é resolúvel com o desenho actual.

**Inputs necessários:** execução de H-1 (backfill, 39 min) e H-2 (congelar snapshots). **Este container apaga-se entre sessões** — os snapshots têm de ser persistidos fora dele antes de a Fase 4 começar, ou toda esta fase é irreprodutível.

**Riscos:** promover B com base nestes critérios é defensável em engenharia e silencioso em investimento. Se o objectivo for melhores decisões e não apenas melhor código, o paralelo de 20 sessões não é opcional.

**Condição para iniciar a implementação:** H-1 e H-2 executados e persistidos fora deste ambiente.
