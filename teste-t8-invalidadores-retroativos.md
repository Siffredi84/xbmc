# Teste T8 — Auditoria Retroativa dos Invalidadores

**Data:** 11/07/2026
**Objeto:** a gramática de invalidadores do `inflection-discovery-engine.json` v1.1 (campo `invalidadores` do cartão de tese)
**Pergunta do teste:** os invalidadores que o motor manda escrever são *operáveis* (disparam quando devem, calam-se quando devem, verificáveis por terceiros) ou *decorativos* (soam concretos, não acionam nada)?
**Método:** simular os invalidadores que os temas/tickers de **20/10/2025** teriam tido segundo as regras do motor, e classificá-los contra o registo real de 2025-26 (reconstruído no post-mortem + 2 verificações novas). Inclui grupo de controlo negativo.

## 0. Protocolo e declaração de leakage

**Leakage declarado:** o auditor conhece os desfechos de 2025-26. Três mitigações estruturais:
1. Os invalidadores são derivados **mecanicamente** da gramática do motor — cada perna da tese (produto/procura/validação) recebe a sua condição de morte, usando as formas-padrão do template ("book-to-bill <1 dois trimestres", "cancelamento de expansão nomeada", "standard fecha em direção desfavorável") — não são escolhidos livremente.
2. **Grupo de controlo negativo:** 3 invalidadores deliberadamente decorativos (do tipo que um LLM descuidado escreve) entram na mesma classificação — se os critérios de avaliação não os chumbarem, o teste não discrimina e o resultado é inválido.
3. **Critérios fixados antes da classificação** (secção 1).

**Limite honesto:** a *escolha dos thresholds* ainda pode carregar hindsight inconsciente. Este teste valida a gramática; só o T1 (forward) valida invalidadores escritos verdadeiramente às cegas.

## 1. Critérios de classificação (fixados ex-ante)

| Critério | Pergunta |
|---|---|
| **Operabilidade** | Um terceiro consegue determinar, só com dados públicos, se disparou? (exige observável + threshold + janela) |
| **Silêncio correto** | Ficou mudo na correção de nov/2025 e no crash de 05/06/2026 (eventos de PREÇO que não reverteram compromissos)? |
| **Disparo correto** | Nas pernas que foram de facto feridas, disparou — e com que antecedência sobre o preço? |
| **Disparo falso** | Disparou sem reversão real de compromissos? (falha grave) |

## 2. Invalidadores simulados (as-of 20/10/2025) e classificação

### Tema 1 — Advanced Packaging / Hybrid Bonding

| # | Invalidador simulado | O que aconteceu (2025-26) | Classificação |
|---|---|---|---|
| I1.1 | "JEDEC/fabricantes aliviam a restrição física que força o hybrid bonding (specs de altura/pitch relaxadas), prolongando a viabilidade de TCB/microbumps para além da janela da tese" | **DISPAROU**: JEDEC em discussões para subir a altura HBM de 775µm para 825-900µm+ (HBM4E/HBM5), reduzindo a urgência do HB [TrendForce 01/04/2026]; BESI -13% num dia e -7% noutro quando a imprensa pegou no tema; "Hybrid Bonding Delays Test BESI's Growth Story" | ✅ **Disparo correto** — e ANTECIPADO: o canal de standards acionou a revisão da perna HB ~2 meses antes do crash de preço de junho |
| I1.2 | "Um âncora nomeado cancela/adia materialmente o capex de AP (TSMC AZ, Amkor $7B, rampa HBM4 SK hynix)" | Nenhum cancelou; Amkor ganhou o programa AMD (05/2026) | ✅ Silêncio correto |
| I1.3 | "Book-to-bill dos fornecedores de AP tooling <1 por dois trimestres consecutivos" | BESI Q1 2026 bookings **+104,5%** YoY (€269,7M); ASMPT bookings +71,6% | ✅ Silêncio correto |
| C1 *(controlo decorativo)* | "Se o entusiasmo com a IA arrefecer" | Indeterminável — arrefeceu no crash de junho? Voltou? Sem observável nem threshold | ❌ **Reprovado por inoperabilidade** (controlo funcionou) |

### Cartões individuais (como o motor os teria escrito a 20/10/2025)

| # | Ticker | Invalidador simulado | Registo 2025-26 | Classificação |
|---|---|---|---|---|
| I-O.1 | ONTO | "Guidance Q4 2025 <$220M (sem crescimento sequencial) — o pedido HBM não se materializa em encomendas" | Guidance Q4: $250-265M (+15-21% seq) a 06/11/2025 | ✅ Silêncio correto — **caso exemplar**: a ação caiu ~3% no dia e depois -12% na correção (o preço gritou), o invalidador de compromissos ficou mudo, e a ação fez +129% em 8 meses. O invalidador estava certo; o pânico não |
| I-O.2 | ONTO | "Semilab renegociada para pior ou write-off (sinal de tese de metrologia a falhar)" | Fechou a 17/11/2025 em termos melhorados (-$50M) | ✅ Silêncio correto |
| I-O.3 | ONTO | "Um OEM de bonding fecha o loop de metrologia inline sem ferramentas ONTO" | Sem evidência de disparo; verificação limitada nesta sessão | ⚪ Silêncio (verificação parcial — declarado) |
| I-A.1 | AMKR | "Atraso material anunciado no Arizona ou o cliente âncora desiste" | Oposto: program win da AMD associado ao Arizona (05/2026) | ✅ Silêncio correto |
| I-A.2 | AMKR | "Receita de advanced packaging cai YoY dois trimestres" | Trimestres recorde; ATH a 12/06/2026 — *depois* do crash | ✅ Silêncio correto |
| I-AS.1 | ASMPT | "Encomendas de bonding avançado (TCB **+** HB, agregadas) estagnam dois trimestres" | Bookings +71,6% YoY Q1 2026; encomendas repetidas de TCB chip-to-wafer (06/2026) | ✅ Silêncio correto — **lição de granularidade**: escrito ao nível da PORTAGEM (etapa "colar"), sobrevive à rotação HB→TCB. Escrito só sobre HB, teria disparado e expulsado o trader do ticker certo pela razão errada |
| I-F.1 | FORM | "Receita de probe cards DRAM/HBM cai sequencialmente dois trimestres" | DRAM probe cards em recorde (Q3 2025); FY26 em crescimento | ✅ Silêncio correto |
| C2 *(controlo)* | ASMPT | "Se a concorrência chinesa aumentar" | Sempre verdadeiro, nunca acionável — sem threshold nem janela | ❌ Reprovado por inoperabilidade |

### Tema 2 — Grid & Power (nível de tema)

| # | Invalidador simulado | Registo | Classificação |
|---|---|---|---|
| I2.1 | "Lead times de transformadores normalizam para <24 meses" | Oposto: 3-5 anos em maio/2026; turbinas esgotadas até 2029 | ✅ Silêncio correto |
| I2.2 | "Cancelamentos líquidos de encomendas de equipamento pesado em dois trimestres" | Backlogs recorde; preços +50%/6 meses | ✅ Silêncio correto |

### Tema 3 — Liquid Cooling (nível de tema)

| # | Invalidador simulado | Registo | Classificação |
|---|---|---|---|
| I3.1 | "Standards OCP não convergem — cada OEM proprietário, interoperabilidade falha" | Adoção acelerou; mercado $4-6B em 2026, +31%/ano; Vertiv 45× capacidade CDU; Modine +42% em data centers e $100M numa fábrica de CDUs | ✅ Silêncio correto |
| I3.2 | "Corte de capex guidance em ≥2 dos 4 grandes hyperscalers" | Sem disparo na janela verificada | ✅ Silêncio correto (verificação parcial pós-jan/2026 — declarado) |
| C3 *(controlo)* | "Se houver problemas com leaks" | Leaks pontuais acontecem sempre; sem definição de escala/threshold | ❌ Reprovado por inoperabilidade |

## 3. O teste de silêncio sob stress (a secção decisiva)

Dois eventos de preço violentos, zero reversões de compromissos — o comportamento exigido era silêncio total dos invalidadores:

- **Correção de nov/2025** (SOX -3,35% num dia; 45% dos gestores com "AI bubble" como maior tail risk): **0 disparos** nos 14 invalidadores reais. ✅ O plano v1 de out/2025, baseado em stops de preço, foi expulso da ONTO aqui; a camada de invalidadores de compromissos dizia "tese intacta" — e estava certa.
- **Crash de 05/06/2026** (Broadcom guidance miss; SOXX -10%, ~$1,3 biliões apagados; FORM -17,7% na semana; ONTO -12,5% num dia): **0 disparos**. ✅ Os compromissos não reverteram — BESI +104,5% bookings, ASMPT +71,6%, AMKR fez ATH **sete dias depois** do crash. Nota fina: o miss da Broadcom era um sinal de procura de UM cliente sobre o SEU guidance — nenhum invalidador da camada de AP tooling o referenciava, corretamente.
- **E o único ferimento real da tese** (adoção de HB adiada) **não veio por preço**: veio pelo canal de standards (I1.1), em abril, com ~2 meses de antecedência sobre o stress de junho. O invalidador certo dispara *antes* do mercado, não depois.

## 4. Resultado

| Métrica | Resultado |
|---|---|
| Operabilidade | **14/14** invalidadores reais operáveis (observável + threshold + janela) |
| Silêncio correto em eventos de preço | **14/14** (2 com verificação parcial, declarada) |
| Disparos corretos | **1/1** — I1.1 (JEDEC/altura HBM), com ~2 meses de antecedência sobre o preço |
| Disparos falsos | **0** |
| Grupo de controlo | **3/3 decorativos reprovados** pelos critérios — o teste discrimina |

**VEREDITO: PASSA.** A gramática de invalidadores do motor produz condições operáveis que se calam no ruído de preço e dispararam, no único caso real de ferimento, pelo canal certo e cedo. Com a ressalva declarada: thresholds simulados por quem conhece o desfecho — a validação limpa é o T1.

## 5. Correções propostas ao motor (candidatas à v1.2 — não aplicadas aqui)

1. **Taxonomia mínima de invalidadores no cartão:** exigir ≥1 invalidador por perna da tese (produto/procura/validação) **+ 1 de standards** — o caso JEDEC prova que o Motor 3 funciona ao contrário: um standard pode *des-forçar* o capex que forçava. Hoje o template pede "2-4 concretos" sem cobertura mínima por perna.
2. **Regra da portagem, não da tecnologia:** quando o operador cobre múltiplas tecnologias da mesma etapa (ASMPT: TCB+HB), o invalidador escreve-se ao nível da etapa — a lição I-AS.1.
3. **Proibição explícita de invalidadores de preço/drawdown:** já é implícito ("acontecimentos concretos e observáveis"); tornar literal, com nov/2025 e jun/2026 como racional no próprio JSON.
4. **"Disparo ≠ morte":** um disparo aciona revisão obrigatória com três saídas — *morto*, *ferido/re-scoped* (a tese reescreve-se: o caso HB→TCB deslocou valor dentro da mesma etapa, não matou o tema), ou *reforçado noutra etapa*. O ciclo de vida da fase 6 só tem "morto" — falta o estado intermédio.

## 6. Registo no programa de testes

T8 **CONCLUÍDO** a 11/07/2026 — resultado PASSA com 4 correções candidatas à v1.2 (a aplicar junto com as que saírem do T3, para não fragmentar versões). Arquivo atualizado.

### Fontes novas desta auditoria (para além do registo do post-mortem)
- [Investing.com — BESI -13% após relatório sobre ameaça ao hybrid bonding](https://www.investing.com/news/stock-market-news/besi-shares-tumble-13-after-report-flags-threat-to-hybrid-bonding-demand-4546257) · [Seeking Alpha — BESI plunges](https://seekingalpha.com/news/4561871-besi-plunges-after-ai-chip-makers-ponder-slowdown-in-hybrid-bonding-tech-report) · [MarketScreener — BESI Q1 bookings +104,5%](https://www.marketscreener.com/news/besi-reports-first-quarter-bookings-above-last-year-ce7f59d9dd8bf221) · [TrendForce — JEDEC pondera relaxar specs de altura HBM (01/04/2026)](https://www.trendforce.com/news/2026/04/01/news-jedec-reportedly-plans-to-relax-hbm-height-specs-to-900%C2%B5m-potentially-slowing-hybrid-bonding-adoption/)
- [MarketsandMarkets — liquid cooling market](https://www.marketsandmarkets.com/ResearchInsight/data-center-liquid-cooling-market.asp) · [GMInsights — mercado 2026](https://www.gminsights.com/industry-analysis/data-center-liquid-cooling-market) (Modine +42% DC revenue, $100M CDU facility; Vertiv 45× CDU, CoolChip 09/2025)

---

*T8 fecha com uma conclusão que liga a série toda: em outubro de 2025, um trader com estes 14 invalidadores e sem stops de 3,5% teria atravessado a correção de novembro e o crash de junho dentro das quatro teses certas — e teria recebido, pelo canal de standards, o único aviso que importava, dois meses antes do mercado. A camada que faltava ao v1 não era mais análise; era esta.*
