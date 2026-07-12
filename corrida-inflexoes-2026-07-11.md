# Corrida do Motor de Inflexões — 11/07/2026 (teste live do framework)

**Comando executado:** `corrida_semanal` do `inflection-discovery-engine.json` v1.0
**Data de referência:** 11/07/2026 (sábado; última sessão de mercado: 10/07/2026)
**Duplo propósito:** (1) output real da corrida; (2) teste do framework — a meta-avaliação está na secção final.

**Restrições declaradas (regra de honestidade nº 2 do motor):** toda a evidência vem de pesquisa web por excertos (WebFetch bloqueado pela política de rede do ambiente). As classes de emissor 6 (talento) e 7 (infraestrutura física) não foram pesquisáveis com fiabilidade nesta sessão — os campos aparecem como NÃO OBTÍVEL, nunca estimados. Contexto de mercado: ~5 semanas após o crash setorial de 05/06/2026 (miss da Broadcom; SOXX -10% num dia) — registado como contexto; não é gate deste motor.

**Disclaimer:** output de research/watchlist. Não é aconselhamento financeiro. Não contém níveis de entrada, stops nem sizing (fronteira de âmbito do motor).

---

## Fase 1 — Hipóteses em bruto (5 motores)

| # | Hipótese (formato obrigatório) | Motores que a geraram |
|---|---|---|
| H1 | A camada **[equipamento elétrico pesado: transformadores/turbinas]** da cadeia **[energia para data centers de IA]** vai receber capex forçado porque **[lead times de 3-5 anos, turbinas esgotadas até 2029, preços +50% em 6 meses]** | M1 (gargalo), M2 (preços) |
| H2 | A camada **[redutores de precisão/atuadores]** da cadeia **[humanoides]** vai receber capex forçado porque **[<10 fornecedores mundiais; lead times de 26 semanas; três programas (Optimus/Figure/Apollo) em produção piloto simultânea desde o Q2 2026]** | M1, M2 (Nabtesco a duplicar capacidade), M5 (segunda linha dos humanoides) |
| H3 | A camada **[industrialização do CPO: substratos ABF + teste eletro-ótico wafer-level + montagem ótica]** da cadeia **[interconexão ótica de IA]** vai receber capex forçado porque **[COUPE da TSMC e switches CPO da NVIDIA entram em produção em volume no 2H26; défice de substrato ABF projetado >20-26% em 2027; o gargalo declarado da produção em massa é o teste]** | M1, M2 (preços/pré-pagamentos), M3 (standard OIF), M5 (BOM do Rubin) |
| H4 | A camada **[solid rocket motors/energéticos]** da cadeia **[rearmamento/munições]** vai receber capex forçado porque **[crise de capacidade documentada; o Estado está a converter apropriações em awards nominais e equity direto]** | M4 (política financiada), M1 |

**Seleção para profundidade (fases 2-5):** H3 (mais motores convergentes, sinais mais recentes) e H2 (sinais fortes — mas ver fase 4). H1 e H4 seguem em avaliação abreviada.

---

## Fase 2 — Mapa de portagens (H3: industrialização do CPO)

**Cadeia:** interconexão ótica para IA (CPO/silicon photonics), rampa 2H26-2027.

| Etapa | Operadores | Concentração | Cobra por unidade de | Modo de falha? |
|---|---|---|---|---|
| 1. Filme ABF (material) | Ajinomoto (>95% do filme) | monopólio | m² de filme por substrato | — |
| 2. Substrato ABF/FC-BGA | Ibiden (~35%), Shinko (~18%), Unimicron (~14%), AT&S (~10%), Nan Ya (~5%) | oligopólio | substrato por GPU/switch (área e camadas a crescer por geração) | — |
| 3. PIC foundry (COUPE) | TSMC (dominante) | monopólio funcional | wafer fotónico | — |
| 4. Motor ótico / laser | Coherent, Lumentum | oligopólio | laser/motor ótico por porto | — |
| 5. Montagem ótica de precisão / FAU | Fabrinet, ficonTEC (privada), US Conec (privada), TFC | oligopólio pouco claro | alinhamento/attach por dispositivo | parcial |
| 6. **Teste eletro-ótico wafer-level** | FormFactor(+Advantest), Teradyne(+Quantifi/ficonTEC) | duopólio emergente | **die fotónico testado** | **SIM — "o gargalo crítico da produção em massa de CPO é o teste" (TrendForce)** |

**Leitura:** o modo de falha da cadeia é o teste — não se embarca um die ótico não testado num pacote de $40k. A etapa 6 é a portagem mais defensável; a etapa 2 é a portagem de volume com défice quantificado; a etapa 5 é a menos clara (risco de desintermediação: o CPO pode canibalizar a montagem de pluggables — registado nos invalidadores).

---

## Fase 3 — Triangulação por sinais custosos

### H3 — Industrialização do CPO

| Classe | Nível | Sinal | Emissor | Fonte / Data |
|---|---|---|---|---|
| 4 (cliente final) | **L5** | $4B investidos em Coherent + Lumentum, com compromissos de compra plurianuais e prioridade de capacidade para CPO | NVIDIA | genaitech/imprensa técnica, **02/03/2026** |
| 4 (cliente final) | L3 | Lock-in de capacidade de substrato ABF via contratos de longo prazo + pré-pagamentos | NVIDIA | TrendForce/BigGo, 18/05/2026 |
| 2 (produtor) | **L5** | COUPE(-on-substrate) em produção em massa no 2H26; validação 1.6T concluída em 2025 | TSMC | TrendForce, 01/04 e 18/05/2026 |
| 1 (equipamento) | **L5** | ¥500B (~$3,2B) de capex FY2026-28 — a maior expansão de substratos da história; objetivo 2,5× capacidade até 2028; pré-pagamentos de clientes a subir | Ibiden | digitimes/substack especializado, dez/2025-2026 |
| 1 (equipamento) | L4 | Célula de teste wafer-level de silicon photonics para HVM (parceria); sistema 300 mm double-sided (Teradyne+ficonTEC, 1º da indústria, mar/2025); aquisição da Quantifi Photonics (2025) | FormFactor+Advantest; Teradyne | formfactor.com; imprensa técnica, 2025-2026 |
| 3 (integrador) | L3 | Utilização ABF ~90% na Unimicron; défice projetado >20-26% em 2027 | Unimicron/analistas | digitimes/TrendForce, 2026 |
| 2 (material) | L3 | Aumento de preço de 30% do filme ABF notificado para o Q3 2026 | Ajinomoto | substack especializado/imprensa técnica, 2026 |
| — (standards) | L4-equiv | 1º standard de co-packaging da indústria (3.2T Co-Packaged Module IA) + Co-Packaging Framework IA | OIF | oiforum.com |
| 6 (talento) | — | NÃO OBTÍVEL nesta sessão | — | — |
| 7 (infra física) | — | NÃO OBTÍVEL nesta sessão | — | — |

**Contagem: 4 classes independentes com sinais ≥L3** (1, 2, 3, 4) + standard fechado + material com pricing power. **Rajada:** sinais de 02/03 e 18/05/2026 (≤130 dias; o lock-in de maio a ~54 dias). Teste anti-cascata: NVIDIA/TSMC/Ibiden/Ajinomoto têm funções e incentivos distintos; nenhum sinal cita o mesmo press release. → **VEREDITO: QUALIFICADO (convicção alta — 4 classes, dois L5 estruturais).**

### H2 — Atuadores de humanoides (abreviada — ver fase 4)

Sinais fortes: Nabtesco a duplicar capacidade de redutores RV até 2026 (L5, classe 1); HDS com encomendas humanoides ~¥1,3B/trimestre a duplicar/triplicar (L3, classe 1); Optimus+Figure+Apollo em produção piloto simultânea Q2 2026 (L3/L4, classe 4); lead times 26 semanas (M1). ≥3 classes? Classe 1 (dois emissores), classe 4 — **3 classes marginais**. Qualificaria na fase 3 — **mas morre na fase 4** (abaixo).

### H4 — SRM/energéticos (abreviada)

Estado (classe 5): $1B de equity direto na L3Harris Missile Solutions (jan/2026, L5); DPA Title III $43,7M Anduril (fev/2026, 2.º award, L5) + $27,3M PacSci EMC (L5). Produtores (classe 2/3): groundbreaking do campus Prometheus Energetics no Indiana (Kratos+RTX, L5); Mach Industries compra Exquadrum por $50M citando a escassez (mai/2026, L5). Cliente (classe 4): US Navy seleciona Northrop para 2.º estágio SRM (L3). **4 classes, rajada ✓ → QUALIFICADO.** Problema adiante: fase 5.

### H1 — Equipamento elétrico pesado (abreviada)

Sinais L3+ abundantes (turbinas esgotadas 2029, preços +50%/6 meses, lead times 3-5 anos) — mas ver fase 4: reprova antes de justificar o mapa completo.

---

## Fase 4 — Teste de invisibilidade (gradiente de cobertura)

| Hipótese | Evidência encontrada nos níveis 3-4 (procurada ativamente) | Nível | Veredito |
|---|---|---|---|
| **H3 — industrialização CPO** | Sub-camadas (ABF, teste eletro-ótico) cobertas por: TrendForce/digitimes/SemiEngineering (nível 1), substacks especializados e X/analistas (nível 2). "CPO stocks" já aparece como cesto nomeado em agregadores financeiros de nicho (BigGo) — o TEMA-MÃE ótico (Lumentum/Coherent) está no nível 3; **as etapas 2 e 6 não aparecem em imprensa generalista nem ETFs dedicados** | **Sub-camadas: 1-2 ✓** | **PASSA** — com nota: densidade crescente de substacks = transição 2→3 provável em meses; reavaliar em 8 semanas |
| H2 — atuadores humanoides | **ETF retail dedicado existe e está distribuído**: KOID (KraneShares), $241M AUM, nas plataformas Merrill desde 10/06/2026; artigos Motley Fool/Seeking Alpha sobre os holdings; a própria sub-camada está nos top holdings (Leader Drive 2,33%, Novanta 2,20%) e nos top performers (Schaeffler +134%, China Northern Rare Earth +159%); newsletters retail a fazer stock-picking do nome-chave ("Harmonic Drive: Positioned to 10X?") | **4** | **REPROVA — tema MADURO.** O edge informacional morreu: o retail já detém a sub-camada via ETF |
| H1 — equipamento elétrico | Cobertura generalista abundante ("Everyone Is Watching the AI Boom…" no Medium; POWER Magazine; Utility Dive; peças de opinião a declarar o gargalo) — o tema tem nome próprio na imprensa há meses | **3-4** | **REPROVA — MADURO** (era o Tema 2 da corrida de out/2025; 9 meses depois, mainstream) |
| H4 — SRM/energéticos | Cobertura: Breaking Defense, InsideDefense, SpaceNews (nível 1); techtimes/stocktitan (nível 2-3 pontual). Sem ETF dedicado à sub-camada; sem cestos nomeados generalistas encontrados | **1-2 ✓** | **PASSA** |

---

## Fase 5 — Cartões de tese

Temas sobreviventes: **H3** e **H4**. Regra um-ticker-por-etapa aplicada.

### Cartão 1 — FORM (FormFactor) — ENTREGUE ✅

- **etapa_da_portagem:** teste eletro-ótico wafer-level (etapa 6 de H3 — o modo de falha da cadeia)
- **frase_da_restricao:** nenhum die fotónico entra num pacote CPO de milhares de dólares sem teste wafer-level prévio — e o alinhamento ótico sub-mícron em HVM só existe em duas cadeias de fornecimento (FormFactor+Advantest; Teradyne+ficonTEC)
- **perna_produto:** sistemas de probing de silicon photonics com alinhamento automático de FAU e sensing de deslocamento Z sub-mícron; célula de teste WLT com Advantest para HVM
- **perna_procura:** rampa COUPE/switches CPO NVIDIA no 2H26 [TrendForce, 04-05/2026]; TrendForce: "o gargalo crítico da produção em massa de CPO é o teste" [2026]
- **perna_validacao:** parceria Advantest (L4); NVIDIA $4B em CPO a 02/03/2026 (procura a jusante); nota histórica: portagem de teste já validada no ciclo HBM (probe cards DRAM/HBM em recordes — resultados Q3 2025)
- **gradiente_cobertura (ticker):** 2-3 (mid-cap coberta por sell-side; entrou no Russell 1000 em jun/2026; a *tese fotónica* específica está no nível 1)
- **calendario_do_instrumento:** **earnings Q2 2026: 29/07/2026** [confirmado — press release de 08/07/2026]; sem outros eventos corporativos conhecidos
- **invalidadores:** (1) TSMC/foundries insourçam o teste fotónico sem sistemas FormFactor; (2) dissolução/esvaziamento da parceria Advantest; (3) dois trimestres após a rampa COUPE sem receita SiPh visível no mix; (4) rampa CPO da NVIDIA adiada para 2028+
- **estado:** qualificado

### Cartão 2 — TER (Teradyne) — ENTREGUE ✅ (com ressalva de pureza)

- **etapa_da_portagem:** a mesma etapa 6, via cadeia alternativa (Quantifi Photonics, adquirida em 2025 + ficonTEC, parceria) — **exceção declarada à regra um-ticker-por-etapa:** FORM e TER são as duas cadeias do duopólio da mesma portagem; entregue como par consciente, não como diversificação
- **frase_da_restricao:** idêntica à do Cartão 1
- **perna_produto:** 1.º sistema da indústria de wafer probe 300 mm double-sided para silicon photonics (com ficonTEC, mar/2025); instrumentação Quantifi
- **perna_procura / perna_validacao:** as do Cartão 1 (mesma cadeia de procura); aquisição Quantifi = L5 próprio
- **gradiente_cobertura (ticker):** 3 (large-cap muito coberta — a tese fotónica é uma fração pequena do grupo; ressalva de pureza: reprova o espírito da regra_2 de pure-play, entregue como hedge do duopólio)
- **calendario_do_instrumento:** **earnings Q2 2026: 28/07/2026, after close** [confirmado]
- **invalidadores:** (1) integração Quantifi falhada/abandonada; (2) ficonTEC capturada em exclusivo por rival; (3) o segmento robótico (UR) a deteriorar-se ao ponto de dominar a narrativa do grupo
- **estado:** qualificado

### Cartão 3 — Ibiden (4062.T) — **RETIDO** ⏸️

- **etapa_da_portagem:** substrato ABF (etapa 2 — a portagem de volume, défice >20-26% projetado 2027)
- **frase_da_restricao:** cada GPU/switch CPO de nova geração exige substratos ABF maiores e com mais camadas, e só 5 empresas no mundo os fazem — com o líder (~35% de quota) a 90%+ de utilização no setor
- **perna_produto:** FC-BGA/ABF de alta camada; Kawama Cell 6 (¥220B) alvo FY2027
- **perna_procura:** pré-pagamentos de clientes a subir 2026-2027; lock-in da NVIDIA (18/05/2026)
- **perna_validacao:** ¥500B capex próprio (L5); Ajinomoto +30% no filme (pricing power a montante confirma escassez)
- **gradiente_cobertura (ticker):** 2 (substacks especializados chamam-lhe "the hidden bottleneck"; sem cobertura generalista encontrada)
- **calendario_do_instrumento:** **NÃO OBTÍVEL nesta sessão** (padrão histórico: resultados trimestrais no final de julho/início de agosto — não confirmado para 2026)
- **invalidadores:** (1) atraso/corte do Kawama Cell 6; (2) utilizações do setor <80% ou devolução de pré-pagamentos; (3) défice 2027 revisto para equilíbrio
- **estado:** qualificado — **cartão RETIDO pela regra do calendário obrigatório**: "um cartão sem calendário está incompleto e não pode ser entregue". Ação: confirmar a data no IR da Ibiden e só então promover a entregue.

### Registos sem cartão (regra_4 da fase 5 — o mapa fica completo)

- **Ajinomoto (2802.T):** monopólio do filme ABF (>95%) — reprova a regra de pureza (conglomerado alimentar; ABF é fração pequena). Registado como portagem não investível em pure-play.
- **ficonTEC, US Conec, Quantifi (integrada), Senko:** portagens privadas da etapa 5/6.
- **Etapa 5 (montagem/FAU):** portagem pouco clara + risco de desintermediação (o CPO pode canibalizar a montagem de transceivers pluggable — a Fabrinet não mostrou, nas pesquisas desta corrida, posição confirmada na montagem CPO). Sem cartão; reavaliar quando houver sinal L3+ de design win de montagem CPO.
- **H4 (SRM/energéticos) — tema QUALIFICADO sem cartão entregável:** as portagens puras são privadas (Anduril, Mach, PacSci, X-Bow) ou diluídas em mega-caps (NOC, LHX) ou em nomes já retail (KTOS — nível 3-4, JV Prometheus com RTX). Registado para monitorização: IPOs deste universo (Anduril em particular) seriam o evento que torna o tema investível — invalidador inverso.

### Calendário consolidado de eventos

| Data | Evento |
|---|---|
| 28/07/2026 | TER — resultados Q2 (after close) [confirmado] |
| 29/07/2026 | FORM — resultados Q2 [confirmado, PR de 08/07/2026] |
| 17 ou 24/08/2026 | FN (Fabrinet) — resultados Q4 FY26 [fontes divergem — confirmar; relevante para a etapa 5 mesmo sem cartão] |
| por confirmar | Ibiden — resultados trimestrais [bloqueia o Cartão 3] |

---

## Fase 6 — Estados iniciais arquivados (corrida de 11/07/2026)

| Tema | Estado | Próxima ação |
|---|---|---|
| Industrialização do CPO (H3) | **qualificado** | Reavaliar gradiente em ~8 semanas (risco de transição 2→3); confirmar calendário Ibiden |
| SRM/energéticos (H4) | **qualificado (sem cartão)** | Monitorizar IPOs do universo privado |
| Atuadores humanoides (H2) | **maduro** | Sem novas entradas com edge; registar para a métrica de lead time (a camada demorou <12 meses de McKinsey a ETF retail) |
| Equipamento elétrico pesado (H1) | **maduro** | Idem — confirma o lead time do Tema 2 de out/2025: ~9 meses até mainstream |

---

## Meta-avaliação do framework (o teste em si)

| Critério do protocolo | Resultado | Evidência |
|---|---|---|
| 1. Executabilidade | **PASSA, com fricções** | Todos os templates foram preenchíveis com dados reais datados em ~11 pesquisas. Fricções: classes 6-7 não pesquisáveis por excertos (declaradas); calendários de earnings japoneses difíceis de confirmar |
| 2. Discriminação | **PASSA** | 2 hipóteses mortas na fase 4 (H1, H2 — ambas com sinais L5 na fase 3!), 1 cartão retido na fase 5 (Ibiden), 1 tema qualificado sem cartão (H4). O motor não qualificou tudo — e as regras que reprovaram eram as certas |
| 3. Honestidade | **PASSA** | 2 campos NÃO OBTÍVEL na pilha de sinais; cartão retido por calendário em vez de data inventada; ressalva de pureza explícita no TER; divergência de fontes declarada (FN) |
| 4. Diferenciação | **PASSA** | Uma resposta naive a "o que está quente em julho/2026" daria humanoides, grid e memória — exatamente o que o motor reprovou. O output final (teste eletro-ótico wafer-level + substratos ABF) está nos níveis 1-2 e não apareceu em nenhuma manchete generalista encontrada |

**Fricções que justificam correções ao JSON do motor (follow-up, não aplicadas aqui):**
1. **Fase 4 — estado de transição:** o gradiente devia ter um marcador formal "2→3 em curso" com prazo de reavaliação obrigatório (o caso H3: substacks a multiplicarem-se são o aviso prévio da morte do edge).
2. **Fase 5 — formalizar o cartão RETIDO:** hoje a regra do calendário só proíbe entregar; devia existir o estado explícito "retido" com a ação de desbloqueio nomeada (foi improvisado nesta corrida).
3. **Fase 5 — campo `risco_de_desintermediacao`:** o caso da etapa 5 (o CPO pode matar a montagem de pluggables) mostra que a própria tecnologia do tema pode ser o invalidador de uma etapa vizinha — merece campo próprio no cartão.
4. **Fase 3 — par-de-duopólio:** quando uma etapa é um duopólio, a regra um-ticker-por-etapa devia prever explicitamente a entrega em par consciente (FORM+TER), em vez de exceção ad-hoc.
5. **Classes 6-7:** exigem fontes dedicadas (job boards, bases de permits); em ambientes de pesquisa limitada ficam sistematicamente NÃO OBTÍVEL — o motor devia declarar isso como limitação estrutural conhecida em vez de o redescobrir a cada corrida.

**Nota de fecho do teste:** a corrida reproduziu o comportamento desenhado — incluindo uma simetria notável com a história desta série: a FORM, vetada pelo v2 em outubro/2025 (dollar volume) e +174% depois, reaparece 9 meses mais tarde como portagem do modo de falha de um tema novo, agora com $9-10B de capitalização e liquidez folgada. E os dois temas de outubro/2025 (advanced packaging, grid) aparecem hoje como MADUROS — o que dá ao motor a sua primeira medição empírica de lead time: **~6-9 meses entre a inflexão detetável e o mainstream.**

---

## Fontes principais desta corrida

- [TrendForce — TSMC COUPE 2H26 / Samsung 2029](https://www.trendforce.com/news/2026/04/01/news-silicon-photonics-race-intensifies-as-tsmc-targets-2026-coupe-production-samsung-eyes-2029-cpo-turnkey/) · [TrendForce — COUPE on substrate + NVIDIA lock-in ABF (18/05/2026)](https://www.trendforce.com/news/2026/05/18/news-tsmc-targets-2h26-coupe-on-substrate-nvidia-could-eye-long-term-substrate-deals-amid-cpo-push/) · [TrendForce Insights — "o gargalo do CPO é o teste"](https://insights.trendforce.com/p/cpo-testing-market-opportunities)
- [NVIDIA $4B Coherent+Lumentum (02/03/2026)](https://www.genaitech.net/p/nvidias-4b-cpo-bet-scaleout-first) · [NVIDIA Tech Blog — CPO/AI factories](https://developer.nvidia.com/blog/scaling-ai-factories-with-co-packaged-optics-for-better-power-efficiency/)
- [FormFactor+Advantest — célula WLT SiPh para HVM](https://www.formfactor.com/press-release/formfactor-and-advantest-partner-on-silicon-photonics-wafer-level-test-cell-to-enable-high-volume-manufacturing/) · [FormFactor — resultados Q2 a 29/07/2026](https://www.globenewswire.com/news-release/2026/07/08/3324417/0/en/FormFactor-to-Announce-Second-Quarter-2026-Financial-Results-on-July-29th.html)
- [OIF — 1.º standard de co-packaging (3.2T)](https://www.oiforum.com/oif-launches-the-industrys-first-co-packaging-standard-the-3-2t-co-packaged-module-implementation-agreement/) · [SemiEngineering — standards CPO](https://semiengineering.com/new-standards-push-co-packaged-optics/)
- [digitimes — expansão ABF Taiwan](https://www.digitimes.com/news/a20251218PD207/abf-substrate-packaging-expansion-ai-gpu-capacity.html) · [Substack — Ibiden hidden bottleneck / ABF gap 2027](https://nikhs.substack.com/p/ibiden-the-hidden-bottleneck-beneath) · [Substack — Ajinomoto/filme ABF](https://nextfinancial.substack.com/p/the-msg-monopoly-how-a-japanese-food)
- [McKinsey — humanoid supply chain](https://www.mckinsey.com/industries/industrials/our-insights/turning-humanoid-supply-chain-constraints-into-billion-dollar-wins) · [KraneShares KOID](https://kraneshares.com/etf/koid/) · [KOID em Merrill (10/06/2026)](https://kraneshares.com/humanoid-robotics-etf-koid-now-available-on-merrill-lynch-platforms/) · [Motley Fool — ETF humanoide (31/05/2026)](https://www.fool.com/investing/2026/05/31/humanoid-robots-etf-stocks-best-to-buy/)
- [Utility Dive — turbinas 5 anos](https://www.utilitydive.com/news/5-year-waits-and-rising-costs-how-demand-is-redefining-the-gas-turbine-mar/813385/) · [pv magazine — transformadores 4 anos (11/05/2026)](https://pv-magazine-usa.com/2026/05/11/u-s-transformer-market-faces-severe-supply-constraints-as-lead-times-extend-to-four-years/)
- [Breaking Defense — SRM crunch (01/2026)](https://breakingdefense.com/2026/01/with-the-boom-for-solid-rocket-motors-for-missiles-a-perilous-crunch-in-the-supply-chain/) · [Kratos/Prometheus groundbreaking](https://www.stocktitan.net/news/KTOS/prometheus-energetics-breaks-ground-on-new-solid-rocket-motor-du6xka9a5cmr.html) · [Mach/Exquadrum $50M (25/05/2026)](https://www.techtimes.com/articles/317132/20260525/mach-industries-buys-exquadrum-50m-solid-rocket-motor-shortage-drove-deal.htm)

---

*Fim da corrida de teste. O motor produziu 2 cartões entregues, 1 retido, 2 temas maduros identificados como tal, 1 tema qualificado sem portagem investível — e 5 correções para a versão 1.1 do próprio motor.*
