# Arquivo Longitudinal — Motor de Discovery de Inflexões (fase 6)

**Função:** registo imutável entre corridas — estados de temas, cartões, prazos, e o log do programa de testes. Nada se apaga; transições são datadas e justificadas. Este ficheiro é atualizado por cada corrida (T1) e lido no início dela.

---

## Estado dos temas

| Tema | Estado | Desde | Prazo/ação pendente | Histórico |
|---|---|---|---|---|
| Industrialização do CPO (substratos ABF + teste eletro-ótico WL + montagem) | **qualificado** (marcador TRANSICAO_2_PARA_3) | 11/07/2026 | **Reavaliação obrigatória do gradiente até 05/09/2026** (8 semanas) — falhar o prazo = despromover a maduro por precaução | Corrida #1: 4 classes ≥L3, dois L5 (NVIDIA $4B 02/03/2026; Ibiden ¥500B). Corrida #2 (17/07): perna ABF reforçada (Moody's: escassez substrato PCB→2027); gradiente ainda 1-2 |
| SRM / energéticos | **qualificado (sem cartão entregável)** | 11/07/2026 | Monitorizar IPOs do universo privado (Anduril, Mach, PacSci, X-Bow) — um IPO torna o tema investível | Corrida #1: 4 classes, rajada ✓; portagens puras privadas/diluídas |
| Atuadores de humanoides | **maduro** | 11/07/2026 | Sem novas entradas com edge; contribui para métrica de lead time (<12 meses McKinsey→ETF retail) | Corrida #1: reprovado fase 4 (KOID $241M em plataformas retail desde 10/06/2026) |
| Equipamento elétrico pesado (transformadores/turbinas) | **maduro** | 11/07/2026 | Contribui para métrica de lead time (~9 meses desde detetável em out/2025) | Corrida #1: reprovado fase 4 (cobertura generalista). Corrida #2 (17/07): curva industrial AINDA a subir (Siemens Energy b2b 1,72, backlog €154B; GEV backlog 100→110 GW) → "maduro" = perda de edge de cobertura, ≠ pico industrial |

## Cartões

| Ticker | Etapa | Estado | Calendário | Ação pendente | Invalidadores (resumo) |
|---|---|---|---|---|---|
| FORM | Teste eletro-ótico WL (par de duopólio com TER) | **entregue** 11/07/2026 | Earnings 29/07/2026 [confirmado] | Reavaliar pós-earnings 29/07 | Insourcing do teste por foundries; parceria Advantest esvaziada; 2 trimestres pós-COUPE sem receita SiPh; rampa CPO adiada 2028+. **Corrida #2 (17/07): 0 invalidadores; + sinal reforçador — aquisição da Keystone Photonics (15/12/2025), optical probing SiPh/CPO** |
| TER | Teste eletro-ótico WL (par de duopólio com FORM) | **entregue** 11/07/2026 (ressalva de pureza) | Earnings 28/07/2026 AC [confirmado] | Reavaliar pós-earnings 28/07 | Integração Quantifi falhada; ficonTEC perdida; segmento robótico a dominar a narrativa. **Corrida #2 (17/07): 0 invalidadores; robótica = motor, não lastro; título "−13,63%" sem data confirmável, NÃO contado** |
| Ibiden (4062.T) | Substrato ABF | **entregue** 17/07/2026 (era retido) | **Resultados 04/08/2026 [confirmado — Investing.com]** | Reavaliar pós-resultados 04/08 | Atraso/corte Kawama Cell 6; utilização setor <80% ou devolução de pré-pagamentos; défice 2027 revisto para equilíbrio. **Desbloqueado à 2.ª tentativa (data confirmada) — 1.ª validação forward do mecanismo retido→entregue** |

## Registos sem cartão (portagens não investíveis — regra_4)

- Ajinomoto (2802.T): monopólio do filme ABF >95% — conglomerado, reprova pureza.
- ficonTEC, US Conec, Quantifi (integrada TER), Senko: privadas (etapas 5-6 CPO).
- Etapa 5 CPO (montagem/FAU): portagem pouco clara + risco de desintermediação de pluggables; reavaliar com sinal L3+ de design win de montagem CPO. Evento relevante: FN earnings 17 ou 24/08/2026 (data por confirmar).
- Forgent Power Solutions (grid): corrida #2 (17/07) — book-to-bill 2,3×, backlog $1,98B; nome menos coberto MAS tema grid maduro (sub-camada já retail) → não abre pure-play com edge. Registado, sem cartão.
- Anduril, Mach Industries, PacSci EMC, X-Bow: privadas (tema SRM).

## Calendário consolidado

| Data | Evento | Relevância |
|---|---|---|
| 28/07/2026 | TER Q2 (after close) | Cartão entregue — 1.º teste forward de invalidadores |
| 29/07/2026 | FORM Q2 | Cartão entregue — 1.º teste forward de invalidadores |
| 04/08/2026 | **Ibiden resultados [confirmado]** | Cartão entregue (desbloqueado na corrida #2) |
| 17 ou 24/08/2026 | FN Q4 FY26 (confirmar) | Etapa 5 CPO (sem cartão) |
| até 05/09/2026 | Reavaliação gradiente tema CPO | Prazo TRANSICAO_2_PARA_3 |

## Métricas do motor (acumuladas)

| Métrica | Valor | Base |
|---|---|---|
| Lead time inflexão→mainstream | ~6-9 meses (estimativa inicial, 2 observações retroativas: AP out/2025→1S2026; grid out/2025→1S2026) | Refinamento corrida #2: "mainstream" = perda de edge de cobertura, ≠ pico industrial (grid ainda a subir industrialmente com b2b 1,72) |
| Taxa de maturação | sem dados forward ainda | — |
| Honestidade preditiva dos invalidadores | **1.º ciclo forward limpo (17/07): 0 disparos falsos, 0 disparos reais em FORM/TER** | Nenhuma tese morta ainda; primeiro ponto forward |
| Mecanismo retido→entregue | **1.ª validação forward (17/07): Ibiden desbloqueado à 2.ª tentativa por fonte real** | O mecanismo do cartão retido funciona no tempo |
| Proxy de valor (cabaz cartões vs benchmark) | Baseline 10/07/2026: FORM $121,42 · SOXX $584. **Corrida #2 (16/07): FORM $110,21 (−9,23%) · TER $321,99 (1.º registo) · SOXX $530,50 (−9,16%)** | Cabaz em linha com benchmark em 6 dias (sem significado de tese — arranque da série) |

---

## Log do programa de testes (plano-de-testes-motor-inflexoes.md)

| Teste | Estado | Registo |
|---|---|---|
| **T1 — Longitudinal forward** | **EM CURSO (modo manual) — 2 pontos de dados** | Ponto #1 = corrida-inflexoes-2026-07-11.md. **Ponto #2 = corrida-inflexoes-2026-07-17.md** (Ibiden desbloqueado RETIDO→ENTREGUE 04/08; 1.º ciclo forward de invalidadores limpo em FORM/TER + sinal reforçador Keystone; nenhum tema novo qualificado; proxy iniciado; insight "maduro≠pico industrial"). Automação ainda pendente: 6 tentativas de create_trigger bloqueadas por "MCP tool call requires approval" (3 em 11/07, 3 em 17/07) — a superfície móvel/web não apresenta o carimbo de aprovação do servidor de agendamento; ativar a partir de app/IDE/Routines no browser (spec abaixo). Até lá, corrida manual por pedido; este arquivo garante a continuidade. Duração prevista: 3-6 meses → relatório de calibração |
| T2 — Variância do operador | **CONCLUÍDO 13/07/2026 — PASSA** | t2-tese-chatgpt + t2-avaliacao-comparativa. Mesma semente, Claude vs ChatGPT: ambos → energia de IA / transição 800 VDC (convergência de personalidade + domínio), MAS bens escassos diferentes (dP/dt vs fronteira de falha) e ZERO sobreposição de picks (FLNC/VICR/MLCC vs ETN/ABBN/LFUS/ULS). Método reconhecível, conteúdo divergente e complementar → o perfil potencia, não substitui. ChatGPT superior em fontes (primárias), convicção graduada, e fechou em recomendação sem a emenda à secção 6 (valida a emenda). **Gravidade de domínio confirmada nas 2 mentes → T5 (ex-IA) promovido a crítico** |
| T3 — Adversarial | **CONCLUÍDO 11/07/2026 — PASSA 5/5** | teste-t3-adversarial-gates.md: quantum (contagem, margem de 1 classe), cascata NVIDIA (anti-cascata), hidrogénio (rajada; lacuna: reversões sem campo na fase 3), drones/3 ETFs (verificação ativa), 6G (L1-nunca-conta). +1 correção candidata (sinais_negativos) → 5 acumuladas para a v1.2. Suite reutilizável como regressão |
| T4 — Ablação | pendente | Aguarda ≥4-6 corridas arquivadas |
| T5 — Generalização (ex-IA) | **CONCLUÍDO 13/07/2026 — PASSA** | t5-tese-chatgpt + t5-avaliacao. Lado Claude falhou por limite de gastos (parcial: escolheu energéticos de defesa). Lado ChatGPT = resultado primário: "A portagem do milissegundo" (energéticos de defesa qualificados, CHG/Chemring) — DD mais profunda e de fidelidade mais rigorosa de toda a série, FORA do domínio-casa. **Conclusão refinada:** o perfil generaliza (profundidade não degrada fora de IA — refuta o vício de domínio), MAS as duas mentes convergiram no MESMO 2.º domínio (rearmamento) → a gravidade real não é "IA", é para supersiclos de capex forçado com convergência de compromissos custosos (a máquina a funcionar como desenhada). Característica: sub-pondera o regime CONJETURADO (descartou PFAS/esterilização/MRO). **Próximo: T10 — forçar regime conjeturado.** |
| T6 — Degradação graciosa | **CONCLUÍDO 13/07/2026 — PASSA** | t6-tese-claude + t6-avaliacao. Tema fixado (CTC / faturação eletrónica obrigatória na Europa) sob restrição dura de **3 WebSearch no total** — o desenho que mais tenta a confabulação. O operador **encolheu e declarou que encolheu**: abriu com aviso de corte de conhecimento (jan/2026), marcou estatutos de cotação como não-reconfirmados (Esker/Generix/Comarch possível take-private; Cegedim-como-PA "não confirmei nesta corrida, se não for PA cai"), rotulou o facto-charneira (1 set 2026 + piloto 23 fev + 101 PAs) como "fonte primária no conjunto mas lida via agregação, a confirmar", auto-check de coerência assumiu VERX como bem "adjacente, não idêntico" (P&L maioritário = sales tax EUA), lista franca de "não obtive", respeitou o cap (3 pesquisas contadas). Picks: VERX primária/líquida-mas-diluída, Cegedim-CGM secundária-contingente, SAP embed; Sovos/Basware/Tungsten/Avalara declaradas privadas (portagem mais pura já capturada por PE). **Refuta ao vivo o medo v4 de confabulação sob fome — a fronteira de fidelidade aperta *mais* na escassez, não menos.** **CURVA COMPLETA depois construída (10/5/3/2/1 pesquisas, `t6-curva-degradacao` + `t6-curva-teses-verbatim`):** degradação graciosa confirmada como propriedade **contínua**, sem ponto de rutura — riqueza da tese desce em rampa suave (entregável em todos os patamares), fidelidade plana e densidade de honestidade a **subir** com a fome (o patamar de 2 chega a despromover o VAT gap de facto-charneira por não o verificar), e a **decisão central é INVARIANTE ao orçamento** (VERX primária / TRI rede-pura-diluída / SAP embed + o mesmo auto-check "parcial" sobre a VERX nos 5 patamares). Os cap de pesquisa foram respeitados à letra em todos (10/5/3/2/1). Achado extra: a 10 e 5 pesquisas o operador *descobriu factos que matam candidatos* (Comarch delisted, Esker delisted) e reordenou — a abundância gera precisão, não exuberância. **O orçamento move a evidência, nunca o método nem a verdade.** |
| T7 — Integração a jusante | pendente | Cartões FORM/TER disponíveis |
| **T9 — Qualidade de tese (batismo)** | **CONCLUÍDO 13/07/2026 — BATISMO VÁLIDO** | t9-tese-batismo + t9-avaliacao (grelha pré-committada em 68dca5f7). Operador semeado só com o perfil, mandato neutro, sem tema: produziu "A portagem sobre a derivada" (dP/dt / GW-por-segundo como bem escasso) — acima do padrão fundador, forma própria, falsificadores operáveis, rasto íntegro, zero teatro/jaula. Ressalva única: gravidade de domínio (ficou em infraestrutura de IA) → testar com T5 ex-IA |
| T8 — Invalidadores retroativos | **CONCLUÍDO 11/07/2026 — PASSA** | teste-t8-invalidadores-retroativos.md: 14/14 operáveis, 0 disparos falsos em nov/2025 e 05/06/2026, 1 disparo correto (JEDEC/altura HBM, ~2 meses antes do preço), controlo negativo 3/3 reprovado. 4 correções candidatas à v1.2 (aplicar junto com as do T3) |

## Especificação da Routine T1 (pendente de ativação pelo utilizador)

Para ativar a automação do T1 a partir da interface do Claude Code (agendamento/Routines), usar exatamente:

- **Nome:** T1 — Corrida semanal do Motor de Inflexões
- **Cadência:** sábados, 10:00 UTC (cron `0 10 * * 6`)
- **Prompt:** "[T1 — teste longitudinal, corrida semanal automática] Executa a corrida semanal do Motor de Discovery de Inflexões: (1) lê arquivo-inflexoes.md e inflection-discovery-engine.json (v1.1+) no branch claude/handoff-audit-0w2a31; (2) trata primeiro as ações pendentes do arquivo — prazos de reavaliação TRANSICAO_2_PARA_3, ações de desbloqueio de cartões retidos, verificação de invalidadores dos cartões entregues e do calendário de eventos; (3) corre as fases 0-5 com pesquisa live (orçamento ~10-15 pesquisas), aplicando as regras de honestidade do motor: fonte+data em cada sinal, NÃO OBTÍVEL declarado, L1 nunca conta, cartão sem calendário fica retido com ação de desbloqueio; (4) grava o output como corrida-inflexoes-AAAA-MM-DD.md, atualiza arquivo-inflexoes.md (estados, histórico, métricas, proxy de valor com fechos mais recentes de FORM/TER/SOXX e novos cartões), commit e push ao branch claude/handoff-audit-0w2a31; (5) na resposta final, resume apenas mudanças de estado materiais. Isto é research/watchlist, não aconselhamento financeiro — mantém o disclaimer no output."

## Atualização T10 (13/07/2026)

| Teste | Estado | Registo |
|---|---|---|
| **T10 — Regime conjeturado** | **CONCLUÍDO 13/07/2026 — VÁLIDO (o mais forte para o seu alvo)** | t10-tese-claude + t10-avaliacao. Lado Claude completo (perfil emendado). Tese "O gargalo invisível da transição elétrica" (força de rede/estabilidade de tensão, Merus Power/MERUS.HE). Regime conjeturado cumprido com sofisticação (compromissos custosos na periferia AU, conjetura no centro EU); fidelidade a mais rigorosa da série (recusou inventar os compromissos ausentes — refuta o medo de confabulação da v4 no teste mais duro); falsificador de regime produzido; **as duas emendas do Manus validadas ao vivo** (auto-check desqualificou AMSC + recusou pick falso = anti-Manus; facto-charneira primário respeitado). Conclusão: a sub-ponderação do conjeturado no T5 era de ESCOLHA, não incapacidade. Gravidade de domínio refinada: foi para rede elétrica (excluídas IA+defesa) → assinatura = transformações físicas de energia/infraestrutura; sub-explora não-físico → propõe T11 (domínio não-físico forçado). **Lado ChatGPT CONCLUÍDO 17/07/2026 (t10-tese-chatgpt + t10-avaliacao-comparativa):** VÁLIDO. Tese "A guerra aos corantes sintéticos" (substituição funcional da cor sintética em aplicações difíceis / azul a baixo pH; Sensient SXT primária, Givaudan GIVN secundária, dsm-firmenich menção). Correu em Deep Research (caveat de paridade: mais fontes por ferramenta, não por mente). **Par de variância de mente mais limpo da série:** mesma semente → domínios SEM sobreposição (rede elétrica vs corantes) + ZERO picks comuns + fidelidade igualmente rigorosa no regime mais duro (ChatGPT recusou inventar take-or-pay/capex setorial = réplica cruzada do anti-confabulação). As 2 emendas presentes nas 2 mentes (auto-check anti-Manus: ChatGPT rejeitou Kraft/GM/Pepsi/Walmart como lado-da-procura; facto-charneira endereçado — mais forte no lado Claude, apagão ENTSO-E primário, mais mole no ChatGPT). Traço cruzado confirmado (T2/T5/T10): Claude gravita ao físico/infraestrutural, ChatGPT ao regulatório/comercial. O perfil potencia a mente, não a substitui. |

## Atualização T11 (13/07/2026)

| Teste | Estado | Registo |
|---|---|---|
| **T11 — Domínio não-físico** | **CONCLUÍDO 13/07/2026 — VÁLIDO (nível mais alto)** | t11-tese-claude + t11-avaliacao. Lado Claude completo (perfil emendado, 2.ª corrida). Tese "O Estado dentro da transação" (fiscalidade em tempo real / CTC / e-invoicing, Vertex/VERX). Bem escasso puramente não-físico (portão de licenciamento regulatório + abstração multi-jurisdicional informacional + função de confiança); a lógica de portagem SOBREVIVEU sem gargalo físico (portagem por transação; modo de falha existencial "não faturar→não receber"). Lampejo de topo: a inexistência de pure-play limpo É a confirmação custosa (Avalara/Pagero/Sovos já privatizadas por biliões). As 2 emendas do Manus validadas 2.ª vez no caso mais difícil (auto-check apanhou que a portagem dominante da Vertex é determinação-EUA, não clearance-CTC, e disse-o; facto-charneira flagado secundário). **Conclusão final da gravidade de domínio:** a assinatura funda do perfil NÃO é física/energia/IA — é a CONVERGÊNCIA DE COMPROMISSOS CUSTOSOS; é um detetor geral de inflexões por sinal custoso, indiferente à natureza do gargalo. Perfil validado como método causal geral. |

## Atualização T4 (13/07/2026)

| Teste | Estado | Registo |
|---|---|---|
| **T4 — Ablação de regras** | **CONCLUÍDO 13/07/2026** | t4-ablacao. Método: 2 experiências naturais (Manus = perfil sem as 2 emendas → falhou onde elas atacam = LOAD-BEARING; ChatGPT-T2 = sem regra de fecho → fechou na mesma = PARTIAL/dependente do modelo) + contrafactual sobre o arquivo. Resultado: perfil NÃO inchou (9 LB / 3 redes de segurança / 2-3 vocabulário). 3 podas propostas (não aplicadas, ficam para decisão): taxonomia de edge → vocabulário; 12 liberdades → ~7; facto-charneira → reforço da S4, não regra separada. **Princípio de governação estabelecido: a próxima emenda exige justificação de ablação (falha real observada), não só boa história — vacina contra o inchaço.** |

## Atualização T7 (13/07/2026)

| Teste | Estado | Registo |
|---|---|---|
| **T7 — Integração a jusante** | **CONCLUÍDO 13/07/2026** | t7-integracao-jusante. Handoff real gate-a-gate (VERX/T11 principal; FLNC/T9, Merus/T10 cruzamentos). Consumidor humano fundamental: costura LIMPA (campos ausentes = entrada/stop/sizing são corretamente do consumidor). Consumidor pipeline v2 (momentum): MISMATCH revelador — as teses de descoberta são pré-momentum (VERX -66%, FLNC deprimida, Merus ilíquida) e falhariam o passo 2/0/3 do v2 hoje. **Conclusão central:** a fronteira descoberta≠execução é real mas os dois edifícios estão DESFASADOS NO TEMPO — sequenciais, não simultâneos. O handoff não é "passa o ticker", é "estaciona numa watchlist com 2 gatilhos" (preço rompe→v2 momentum; ou sinal industrial confirma→ator fundamental); o Overlay de Convicção ativa-se no momento posterior da rutura, não na descoberta. Refinamento proposto (não aplicado): estado WATCHLIST_ESTACIONADA no overlay. Valida a decisão de fronteira e refina-a: "quem faz o quê E quando na vida do trade". Integração executada (ver a costura a funcionar no tempo) = trabalho do T1. |

## Atualização E2E (13/07/2026)

| Teste | Estado | Registo |
|---|---|---|
| **E2E — cadeia completa, perfil PODADO** | **CONCLUÍDO 13/07/2026** | e2e-tese-claude + e2e-relatorio. 1.ª corrida ao vivo do perfil pós-podas do T4 (mandato neutro). Tese "a portagem debaixo da portagem" (tempo-para-energia → transformador não-substituível → GOES). **Regressão das podas: PASS emphático** — todas as disciplinas intactas (facto-charneira integrado marcou charneira secundário + corroborou com book-to-bill primário; auto-check recusou vestir a CLF de "jogada do GOES" = anti-Manus mais fino da série; S8 usado proativamente; vocabulário de edge + 7 liberdades sem perda). As 3 podas eram pura legibilidade. **Descoberta do E2E:** o comutador a jusante do T7 tem **3 posições**, não 2 — este fluxo exercitou-as todas: (1) ambas as curvas alinhadas → handoff+boost AGORA (GEV, coreanos 267260/298040); (2) pré-momentum → parquear (caso T7); (3) sem veículo limpo → parquear com gatilho de aparecimento-de-veículo (GOES; a descoberta recusa entregar a CLF à execução = a fronteira a proteger-se). O framework corre inteiro, não é coleção de partes. Domínio: energia/rede (atractor confirmado 5×), ângulo novo. |

## Regras de atualização deste arquivo

1. Cada corrida acrescenta uma linha ao histórico dos temas que tocou e atualiza estados/prazos — nunca reescreve histórico.
2. Transições de estado exigem justificação datada.
3. Cartões retidos: registar cada tentativa de desbloqueio; 2 falhas → morto.
4. O proxy de valor regista o fecho mais recente disponível de cada cartão entregue e do benchmark, por corrida.
