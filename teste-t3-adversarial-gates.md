# Teste T3 — Adversarial / Red Team dos Gates

**Data:** 11/07/2026
**Objeto:** os gates do `inflection-discovery-engine.json` v1.1 (formato obrigatório da hipótese, contagem da fase 3, anti-cascata, rajada, L1-nunca-conta, verificação ativa de invisibilidade)
**Pergunta do teste:** os gates aguentam inputs *desenhados para os enganar*? Cada armadilha ataca uma regra específica; o critério de aprovação, fixado ex-ante, é: **as 5 armadilhas têm de ser rejeitadas pelo pipeline, registando qual regra apanhou cada uma**. Uma armadilha que chegue a cartão = falha de gate = correção obrigatória.
**Método:** cada armadilha é injetada como `deep_dive_tema` com pesquisa real (não asserção do auditor) — os números abaixo têm fonte e data.

---

## Armadilha 1 — Narrativa sedutora, sinais pobres: "Quantum Computing comercial"

**O pitch que um operador motivado faria:** "McKinsey declara 2026 o *commercial tipping point*; 89% das empresas já estão hands-on; a Pasqal levantou ~$500M a $2B de avaliação; a IonQ tem $54,5M da Air Force e elegibilidade num IDIQ de $151B; o Equal1 pôs um quantum computer em rack de data center. A inflexão é agora."

**O pipeline estrito:**
- Fase 1 (formato obrigatório): "a camada [?] vai receber capex forçado porque [?]" — a restrição física que *força* a compra não se consegue escrever (nenhuma empresa é obrigada a comprar quantum para crescer). Já aqui range.
- Fase 3 (contagem estrita, janela 90 dias): classe 5 (Estado): Infleqtion $11M DoD, 04/2026, L3 ✓ — **1 classe**. IonQ/AFRL $54,5M é de **09/2024** (fora da janela); a elegibilidade SHIELD IDIQ não é award (L1/L2). Classe 4 (clientes finais): 89% "hands-on" mas **só 3% em deployment à escala** — pilotos = L2, não conta. Classe 1 (fornecedores): lançamento Equal1 (06/2026, L4) ✓ — mas é o lado da OFERTA a empurrar; **2 classes ≥L3**. O raise da Pasqal não é nenhuma das 7 classes (investidores a financiar a camada ≠ cadeia a adotá-la). O relatório McKinsey é L1.
- **Contagem final: 2 classes < 3 → REPROVADO (EMBRIÃO, re-testar).**
- Redundância: mesmo que passasse, a fase 4 matava — quantum tem ETFs dedicados e mania retail desde 2025 (nível 4).

**Regra que apanhou:** contagem estrita da fase 3 (com o formato da fase 1 já a ranger). **Nota de margem:** passou a 1 classe de qualificar — a disciplina de contagem (pilotos≠L3; raise≠classe; award velho≠janela) foi o que decidiu. ✅ APANHADA

## Armadilha 2 — Cascata de um só press release: "o boom do CPO validado 5 vezes"

**O pitch:** "Cinco sinais numa semana: a NVIDIA investe $4B; a Coherent recebe compromisso plurianual; a Lumentum idem; os analistas sobem os PTs da ótica; a imprensa declara o boom do CPO."

**O pipeline estrito:** os 5 "sinais" rastreiam todos para **o mesmo anúncio de 02/03/2026**. Regra anti-cascata: "sinais que citam a mesma fonte primária contam como UM, na classe do emissor original" → colapsa para 1 sinal, classe 4, L5. Os PTs e a imprensa são L1/eco (regra anti-eco). **Contagem: 1 classe → insuficiente sozinha.**

**O contraste que valida o desenho:** na corrida real de 11/07, o tema CPO qualificou com 4 classes porque existiam sinais **independentes** do anúncio da NVIDIA (capex TSMC, ¥500B da Ibiden, pricing da Ajinomoto, utilização da Unimicron) — a mesma regra que esmaga a cascata deixa passar a convergência genuína. É exatamente a assimetria pretendida. ✅ APANHADA (anti-cascata + anti-eco)

## Armadilha 3 — Eco temporal / reversão: "Hidrogénio verde — os maiores compromissos L5 da década"

**O pitch:** "Gigafactories de eletrolisadores anunciadas, hubs de $36B, dezenas de GW de capacidade — os sinais custosos mais volumosos de qualquer tema."

**O pipeline estrito:**
- Todos os L5 citáveis são de **2021-2023**. Janela de 90 dias: sem sinais positivos ≥L3. Regra da rajada: falha.
- Pior — os sinais recentes são de **reversão**: ~60 projetos cancelados/adiados desde 01/2025; Air Products saiu de 3 projetos nos EUA com charge de **$3,1B**; BP cancelou o hub de $36B na Austrália; Fortescue a ponderar hibernar a fábrica de 2 GW **por falta de encomendas**; 61 GW de capacidade de fabrico contra procura FID mínima; incentivos 45V cortados (07/2025).
- **REPROVADO** — não é inflexão, é a autópsia de uma.

**Regra que apanhou:** rajada (90/30 dias). **Mas o teste expõe uma lacuna real:** os sinais de *reversão* só existem formalmente na fase 6 (critérios de morte de temas JÁ arquivados) — a fase 3 não tem campo para eles na avaliação de temas NOVOS. Um operador descuidado podia reportar "0 sinais recentes, tema embrião, re-testar" quando a resposta certa é "reversão ativa, não re-testar". → Correção candidata (ver secção final). ✅ APANHADA (com lacuna anotada)

## Armadilha 4 — Invisibilidade falsa: "componentes de drones — a camada que ninguém vê"

**O pitch:** "Toda a gente fala dos primes de defesa; ninguém fala da camada de componentes de drones — motores, óticas, datalinks. Nível 1 de cobertura, edge máximo."

**O pipeline estrito (fase 4, ausência VERIFICADA, não assumida):** a pesquisa ativa nos níveis 3-4 encontra **três ETFs dedicados a drones** — AdvisorShares UAV (o maior pure-play), Defiance JEDI (drones/modern warfare) e REX DRNZ (**80% do peso em pure-plays de drones**, AVAV a 13,1%) — mais listas retail "7 Best Drone Stocks" (US News), guias Motley Fool, e ITA com $14,3B. Isto é o "sinal de morte do edge" textual do motor: ETF temático dedicado. **REPROVADO — nível 4.**

**Regra que apanhou:** a obrigação de procurar ativamente a presença nos níveis 3-4. Uma fase 4 preguiçosa ("parece nicho, não me lembro de ETFs") teria deixado passar. ✅ APANHADA

## Armadilha 5 — Pilha só de L1: "6G — o próximo super-ciclo de telecom"

**O pitch:** "O 3GPP fixou em junho/2026 o calendário do Release 21; a Qualcomm e a Ericsson publicam roadmaps; conferências globais; o 6G é o 5G de 2019 outra vez."

**O pipeline estrito:**
- Fase 1: o Motor 3 (standards) **gera legitimamente** a hipótese — um standard está de facto a formalizar-se. A geração funciona.
- Fase 3: a pilha é composta por decisões de calendário de standardização (freeze funcional em 2028, ASN.1 em 2029, comercial ~2030), roadmaps e blogs — **"the search results do not contain information about binding commitments or formal equipment orders as of mid-2026"**. Tudo L1/L2. Contagem: **0 classes ≥L3 → REPROVADO.**

**Regra que apanhou:** L1-nunca-conta. **E o teste valida a separação geração≠qualificação:** o Motor 3 propôs, a fase 3 matou — é assim que deve ser; um motor de hipóteses agressivo com gates duros é melhor que um motor tímido. A janela do 6G abre quando aparecerem as primeiras encomendas L3 (2028-29?) — ficou como embrião com data. ✅ APANHADA

---

## Resultado

| Armadilha | Regra atacada | Resultado | Margem |
|---|---|---|---|
| 1. Quantum (narrativa) | Contagem fase 3 + formato fase 1 | ✅ Rejeitada (2<3 classes) | **Apertada — 1 classe** |
| 2. Cascata NVIDIA $4B | Anti-cascata + anti-eco | ✅ Colapsada para 1 sinal | Confortável |
| 3. Hidrogénio (eco/reversão) | Rajada 90/30 | ✅ Rejeitada | Confortável, **com lacuna** (reversões sem campo na fase 3) |
| 4. Drones (invisibilidade falsa) | Verificação ativa fase 4 | ✅ Rejeitada (3 ETFs dedicados) | Depende da diligência da pesquisa |
| 5. 6G (só L1) | L1-nunca-conta | ✅ Rejeitada (0 classes) | Confortável |

**VEREDITO: PASSA — 5/5 armadilhas rejeitadas**, cada uma pela regra desenhada para ela. Duas notas de humildade: a margem do quantum foi de UMA classe (a disciplina de contagem é o gate real — reforça a urgência do T2, porque operadores diferentes podem contar diferente); e a armadilha 4 só é apanhada se a pesquisa da fase 4 for feita a sério — a regra é boa, mas é a única cuja robustez depende inteiramente da diligência do operador.

## Correção candidata nova (junta-se às 4 do T8 para a v1.2)

**5. Campo `sinais_negativos` na pilha da fase 3:** cancelamentos, write-offs, mothballing e cortes de incentivos com fonte+data, com regra dura: **qualquer sinal negativo L4/L5 na janela de 12 meses impede o veredito EMBRIÃO** (que convida a re-testar) e força REPROVADO com justificação. Origem: armadilha 3 — hoje a reversão é invisível à fase 3 e só existe na fase 6.

## Registo no programa de testes

T3 **CONCLUÍDO** a 11/07/2026 — PASSA 5/5. Correções acumuladas para a v1.2: **5** (4 do T8 + 1 do T3). Próximos da fila: T7 (integração a jusante, com os earnings de FORM/TER a 28-29/07 como caso vivo) ou T6 (degradação graciosa); T2 exige sessões paralelas independentes.

### Fontes das verificações desta bateria
- Quantum: [McKinsey Quantum Monitor 2026](https://www.mckinsey.com/capabilities/mckinsey-technology/our-insights/mckinsey-quantum-technology-monitor-2026-a-commercial-tipping-point) · [BusinessWire — "capability era" (18/06/2026)](https://www.businesswire.com/news/home/20260618639340/en/) · [Quantum Insider — chip companies (05/06/2026)](https://thequantuminsider.com/2026/06/05/how-many-quantum-chip-companies-are-there/)
- 6G: [RCR Wireless — plenário 3GPP jun/2026](https://www.rcrwireless.com/20260701/6g/6g-standard-qualcomm) · [6G-AI — milestones 2026-2030](https://6g-ai.com/news/3gpp-6g-timeline-milestones-2026-2030) · [Lightreading](https://www.lightreading.com/6g/looking-ahead-ready-or-not-here-comes-6g)
- Drones: [AdvisorShares UAV / Defiance JEDI](https://www.defianceetfs.com/jedi/) · [REX DRNZ (80% pure-play)](https://www.rexshares.com/drnz/) · [US News — Best Drone Stocks 2026](https://money.usnews.com/investing/articles/best-drone-stocks-to-buy)
- Hidrogénio: [Decarbonize Weekly — 60 projetos mortos](https://decarbonizeweekly.com/articles/dd007-green-hydrogen-reset/) · [Hydrocarbon Processing — cancelados/adiados (07/2025)](https://www.hydrocarbonprocessing.com/news/2025/07/update-cancelled-and-postponed-green-hydrogen-projects/) · [EnkiAI — cancelamentos 2024-2026](https://enkiai.com/biggest-hydrogen-project-cancellations-in-2025-and-2024/)
- Cascata: construída sobre o anúncio real NVIDIA $4B de 02/03/2026 (fonte na corrida de 11/07)

---

*T3 fecha com a mesma lição do T8 vista do outro lado: os gates funcionam, mas dois deles (contagem e verificação de invisibilidade) dependem da disciplina de quem os executa — que é exatamente o que o T2 (variância do operador) existe para medir. A suite de armadilhas fica reutilizável como teste de regressão para cada versão futura do motor.*
