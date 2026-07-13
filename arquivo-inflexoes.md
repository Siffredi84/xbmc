# Arquivo Longitudinal — Motor de Discovery de Inflexões (fase 6)

**Função:** registo imutável entre corridas — estados de temas, cartões, prazos, e o log do programa de testes. Nada se apaga; transições são datadas e justificadas. Este ficheiro é atualizado por cada corrida (T1) e lido no início dela.

---

## Estado dos temas

| Tema | Estado | Desde | Prazo/ação pendente | Histórico |
|---|---|---|---|---|
| Industrialização do CPO (substratos ABF + teste eletro-ótico WL + montagem) | **qualificado** (marcador TRANSICAO_2_PARA_3) | 11/07/2026 | **Reavaliação obrigatória do gradiente até 05/09/2026** (8 semanas) — falhar o prazo = despromover a maduro por precaução | Corrida #1: 4 classes ≥L3, dois L5 (NVIDIA $4B 02/03/2026; Ibiden ¥500B) |
| SRM / energéticos | **qualificado (sem cartão entregável)** | 11/07/2026 | Monitorizar IPOs do universo privado (Anduril, Mach, PacSci, X-Bow) — um IPO torna o tema investível | Corrida #1: 4 classes, rajada ✓; portagens puras privadas/diluídas |
| Atuadores de humanoides | **maduro** | 11/07/2026 | Sem novas entradas com edge; contribui para métrica de lead time (<12 meses McKinsey→ETF retail) | Corrida #1: reprovado fase 4 (KOID $241M em plataformas retail desde 10/06/2026) |
| Equipamento elétrico pesado (transformadores/turbinas) | **maduro** | 11/07/2026 | Contribui para métrica de lead time (~9 meses desde detetável em out/2025) | Corrida #1: reprovado fase 4 (cobertura generalista) |

## Cartões

| Ticker | Etapa | Estado | Calendário | Ação pendente | Invalidadores (resumo) |
|---|---|---|---|---|---|
| FORM | Teste eletro-ótico WL (par de duopólio com TER) | **entregue** 11/07/2026 | Earnings 29/07/2026 [confirmado] | — | Insourcing do teste por foundries; parceria Advantest esvaziada; 2 trimestres pós-COUPE sem receita SiPh; rampa CPO adiada 2028+ |
| TER | Teste eletro-ótico WL (par de duopólio com FORM) | **entregue** 11/07/2026 (ressalva de pureza) | Earnings 28/07/2026 AC [confirmado] | — | Integração Quantifi falhada; ficonTEC perdida; segmento robótico a dominar a narrativa |
| Ibiden (4062.T) | Substrato ABF | **retido** | NÃO OBTÍVEL | **Ação de desbloqueio: confirmar data de resultados trimestrais no IR da Ibiden (ibiden.com/ir/calendar). 1.ª tentativa falhada 11/07/2026; à 2.ª falha → morto** | Atraso/corte Kawama Cell 6; utilização setor <80% ou devolução de pré-pagamentos; défice 2027 revisto para equilíbrio |

## Registos sem cartão (portagens não investíveis — regra_4)

- Ajinomoto (2802.T): monopólio do filme ABF >95% — conglomerado, reprova pureza.
- ficonTEC, US Conec, Quantifi (integrada TER), Senko: privadas (etapas 5-6 CPO).
- Etapa 5 CPO (montagem/FAU): portagem pouco clara + risco de desintermediação de pluggables; reavaliar com sinal L3+ de design win de montagem CPO. Evento relevante: FN earnings 17 ou 24/08/2026 (data por confirmar).
- Anduril, Mach Industries, PacSci EMC, X-Bow: privadas (tema SRM).

## Calendário consolidado

| Data | Evento | Relevância |
|---|---|---|
| 28/07/2026 | TER Q2 (after close) | Cartão entregue |
| 29/07/2026 | FORM Q2 | Cartão entregue |
| 17 ou 24/08/2026 | FN Q4 FY26 (confirmar) | Etapa 5 CPO (sem cartão) |
| até 05/09/2026 | Reavaliação gradiente tema CPO | Prazo TRANSICAO_2_PARA_3 |
| por confirmar | Ibiden resultados | Desbloqueio do cartão retido |

## Métricas do motor (acumuladas)

| Métrica | Valor | Base |
|---|---|---|
| Lead time inflexão→mainstream | ~6-9 meses (estimativa inicial, 2 observações retroativas: AP out/2025→1S2026; grid out/2025→1S2026) | A validar com observações forward |
| Taxa de maturação | sem dados forward ainda | — |
| Honestidade preditiva dos invalidadores | sem dados ainda (nenhuma tese morta) | — |
| Proxy de valor (cabaz cartões vs benchmark) | Baseline 10/07/2026: FORM $121,42 · TER [registar na corrida #2] · SOXX $584 | Medição a partir da corrida #2 |

---

## Log do programa de testes (plano-de-testes-motor-inflexoes.md)

| Teste | Estado | Registo |
|---|---|---|
| **T1 — Longitudinal forward** | **EM CURSO desde 11/07/2026** | Ponto de dados #1 = corrida-inflexoes-2026-07-11.md. Routine semanal ativa (sábados 10:00 UTC) — corre a corrida, atualiza este arquivo, commit+push ao branch. Duração prevista: 3-6 meses → relatório de calibração |
| T2 — Variância do operador | pendente | Requer 3 sessões paralelas na mesma data |
| T3 — Adversarial | pendente | Bateria 1 por desenhar (5 armadilhas) |
| T4 — Ablação | pendente | Aguarda ≥4-6 corridas arquivadas |
| T5 — Generalização | pendente | Corrida ex-semis por agendar |
| T6 — Degradação graciosa | pendente | — |
| T7 — Integração a jusante | pendente | Cartões FORM/TER disponíveis |
| T8 — Invalidadores retroativos | pendente | Outcomes 2025-26 já reconstruídos no post-mortem |

## Regras de atualização deste arquivo

1. Cada corrida acrescenta uma linha ao histórico dos temas que tocou e atualiza estados/prazos — nunca reescreve histórico.
2. Transições de estado exigem justificação datada.
3. Cartões retidos: registar cada tentativa de desbloqueio; 2 falhas → morto.
4. O proxy de valor regista o fecho mais recente disponível de cada cartão entregue e do benchmark, por corrida.
