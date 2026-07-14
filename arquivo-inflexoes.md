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
| **T1 — Longitudinal forward** | **EM CURSO desde 11/07/2026 (modo manual)** | Ponto de dados #1 = corrida-inflexoes-2026-07-11.md. Automação pendente: a criação de Routine/agendamento persistente exige aprovação que a sessão de origem não conseguiu apresentar (3 tentativas bloqueadas a 11/07/2026 — create_trigger ×2, send_later ×1). Até lá, cada corrida é disparada manualmente ("corre a corrida"); este arquivo garante a continuidade. Duração prevista: 3-6 meses → relatório de calibração |
| T2 — Variância do operador | **CONCLUÍDO 13/07/2026 — PASSA** | t2-tese-chatgpt + t2-avaliacao-comparativa. Mesma semente, Claude vs ChatGPT: ambos → energia de IA / transição 800 VDC (convergência de personalidade + domínio), MAS bens escassos diferentes (dP/dt vs fronteira de falha) e ZERO sobreposição de picks (FLNC/VICR/MLCC vs ETN/ABBN/LFUS/ULS). Método reconhecível, conteúdo divergente e complementar → o perfil potencia, não substitui. ChatGPT superior em fontes (primárias), convicção graduada, e fechou em recomendação sem a emenda à secção 6 (valida a emenda). **Gravidade de domínio confirmada nas 2 mentes → T5 (ex-IA) promovido a crítico** |
| T3 — Adversarial | **CONCLUÍDO 11/07/2026 — PASSA 5/5** | teste-t3-adversarial-gates.md: quantum (contagem, margem de 1 classe), cascata NVIDIA (anti-cascata), hidrogénio (rajada; lacuna: reversões sem campo na fase 3), drones/3 ETFs (verificação ativa), 6G (L1-nunca-conta). +1 correção candidata (sinais_negativos) → 5 acumuladas para a v1.2. Suite reutilizável como regressão |
| T4 — Ablação | pendente | Aguarda ≥4-6 corridas arquivadas |
| T5 — Generalização (ex-IA) | **CONCLUÍDO 13/07/2026 — PASSA** | t5-tese-chatgpt + t5-avaliacao. Lado Claude falhou por limite de gastos (parcial: escolheu energéticos de defesa). Lado ChatGPT = resultado primário: "A portagem do milissegundo" (energéticos de defesa qualificados, CHG/Chemring) — DD mais profunda e de fidelidade mais rigorosa de toda a série, FORA do domínio-casa. **Conclusão refinada:** o perfil generaliza (profundidade não degrada fora de IA — refuta o vício de domínio), MAS as duas mentes convergiram no MESMO 2.º domínio (rearmamento) → a gravidade real não é "IA", é para supersiclos de capex forçado com convergência de compromissos custosos (a máquina a funcionar como desenhada). Característica: sub-pondera o regime CONJETURADO (descartou PFAS/esterilização/MRO). **Próximo: T10 — forçar regime conjeturado.** |
| T6 — Degradação graciosa | pendente | — |
| T7 — Integração a jusante | pendente | Cartões FORM/TER disponíveis |
| **T9 — Qualidade de tese (batismo)** | **CONCLUÍDO 13/07/2026 — BATISMO VÁLIDO** | t9-tese-batismo + t9-avaliacao (grelha pré-committada em 68dca5f7). Operador semeado só com o perfil, mandato neutro, sem tema: produziu "A portagem sobre a derivada" (dP/dt / GW-por-segundo como bem escasso) — acima do padrão fundador, forma própria, falsificadores operáveis, rasto íntegro, zero teatro/jaula. Ressalva única: gravidade de domínio (ficou em infraestrutura de IA) → testar com T5 ex-IA |
| T8 — Invalidadores retroativos | **CONCLUÍDO 11/07/2026 — PASSA** | teste-t8-invalidadores-retroativos.md: 14/14 operáveis, 0 disparos falsos em nov/2025 e 05/06/2026, 1 disparo correto (JEDEC/altura HBM, ~2 meses antes do preço), controlo negativo 3/3 reprovado. 4 correções candidatas à v1.2 (aplicar junto com as do T3) |

## Especificação da Routine T1 (pendente de ativação pelo utilizador)

Para ativar a automação do T1 a partir da interface do Claude Code (agendamento/Routines), usar exatamente:

- **Nome:** T1 — Corrida semanal do Motor de Inflexões
- **Cadência:** sábados, 10:00 UTC (cron `0 10 * * 6`)
- **Prompt:** "[T1 — teste longitudinal, corrida semanal automática] Executa a corrida semanal do Motor de Discovery de Inflexões: (1) lê arquivo-inflexoes.md e inflection-discovery-engine.json (v1.1+) no branch claude/handoff-audit-0w2a31; (2) trata primeiro as ações pendentes do arquivo — prazos de reavaliação TRANSICAO_2_PARA_3, ações de desbloqueio de cartões retidos, verificação de invalidadores dos cartões entregues e do calendário de eventos; (3) corre as fases 0-5 com pesquisa live (orçamento ~10-15 pesquisas), aplicando as regras de honestidade do motor: fonte+data em cada sinal, NÃO OBTÍVEL declarado, L1 nunca conta, cartão sem calendário fica retido com ação de desbloqueio; (4) grava o output como corrida-inflexoes-AAAA-MM-DD.md, atualiza arquivo-inflexoes.md (estados, histórico, métricas, proxy de valor com fechos mais recentes de FORM/TER/SOXX e novos cartões), commit e push ao branch claude/handoff-audit-0w2a31; (5) na resposta final, resume apenas mudanças de estado materiais. Isto é research/watchlist, não aconselhamento financeiro — mantém o disclaimer no output."

## Regras de atualização deste arquivo

1. Cada corrida acrescenta uma linha ao histórico dos temas que tocou e atualiza estados/prazos — nunca reescreve histórico.
2. Transições de estado exigem justificação datada.
3. Cartões retidos: registar cada tentativa de desbloqueio; 2 falhas → morto.
4. O proxy de valor regista o fecho mais recente disponível de cada cartão entregue e do benchmark, por corrida.
