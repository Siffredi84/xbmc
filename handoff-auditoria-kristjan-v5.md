# Auditoria ao Handoff v4 — "Kristjan Discovery System" (meta-auditoria, v5)

**Data:** 2026-07-11 (v5)
**Tipo de documento:** Auditoria do handoff de auditoria (meta-auditoria) — verifica a consistência interna da v4, confirma as afirmações factuais contra fontes adicionais, e fecha os pontos em aberto da secção 7 da v4
**Objeto auditado:** Handoff v4 ("Auditoria ao Kristjan Discovery System", 2026-07-11), incluindo releitura do JSON original (Anexo A da v4)
**Autor:** Claude (Fable 5, sessão Claude Code)

---

## 1. Âmbito e método

A v4 terminava com uma nota dirigida a esta auditoria (secção 7), listando 9 pontos por aprofundar. Esta v5 fez três coisas:

1. **Verificação de consistência interna da v4** — números, tabelas, referências cruzadas entre findings, e coerência entre as recomendações e as "decisões pendentes".
2. **Verificação factual alargada** — mais de uma dezena de fontes trianguladas (contra as 2 queries da v4), incluindo duas declarações diretas do próprio Kullamägi (uma citação sobre regras de saída e um tweet sobre earnings) e fontes que a v4 não tinha tocado (Deepvue, ChartMill, Stonks Capital, transcrição Chat With Traders, Grokipedia, statsedgetrading).
3. **Fecho ponto a ponto da secção 7 da v4** — 7 dos 9 pontos ficam resolvidos ou substancialmente resolvidos; 2 continuam abertos (ver secção 6).

**Limitação de acesso desta sessão:** `qullamaggie.com`, `jackcorsellis.com` e `tradingresourcehub.substack.com` devolvem HTTP 403 a leitura direta neste ambiente (proteção anti-bot). O conteúdo dessas fontes foi obtido via excertos indexados por pesquisa, não por leitura integral. O documento do Scribd continua por ler. Ou seja: esta v5 tem mais triangulação e mais granularidade do que a v4, mas a recomendação de validação final contra material primário integral (decisão pendente #12 da v4) **mantém-se em aberto**.

---

## 2. Veredito sobre a v4

**A v4 é globalmente sólida e as suas conclusões estruturais sobrevivem à verificação.** Nenhuma das recomendações centrais foi contrariada: gates binários em vez de scoring ponderado (3.1), escalonamento de saída em vez de entrada (3.2), parâmetros técnicos em vez de research institucional (3.3), teto de exposição agregada em vez de diversificação forçada (3.5), disclaimer com base na taxa de acerto real (3.7), filtro de ambiente de mercado como passo 0 (3.9), e a reordenação fail-fast (secção 5).

**Mas a v4 não está limpa.** Esta auditoria encontrou:

- **2 erros factuais** em conteúdo que a v4 apresenta como "verificado" e pronto a colar no JSON — a regra de volume dos Episodic Pivots (V5-1) e as janelas de lookback do screening (V5-2, que é também uma contradição interna da v4);
- **1 omissão relevante** — a regra real de pirâmide, que torna a reescrita proposta para o critério 3 incompleta (V5-3);
- **2 imprecisões menores** parametrizáveis (V5-4, V5-5);
- **1 tensão entre decisões pendentes** da própria v4 (V5-6);
- **1 refinamento à reordenação proposta** — a posição do critério de volume (V5-7).

**Conclusão prática:** a v4 pode ser usada como base de implementação **depois** de aplicadas as correções V5-1 a V5-3 e resolvida a tensão V5-6. Sem isso, dois números errados entrariam no JSON com o selo de "verificados".

---

## 3. Confirmações — afirmações da v4 que sobrevivem à verificação

| Afirmação da v4 | Estado | Nota |
|---|---|---|
| Taxa de acerto ~25-30% (banda 20-35%) | ✅ Confirmada | Fonte independente da v4 cita "25%" como média anual ("turned $5,000 into $100 million. His win rate was 25%") |
| Risco por trade 0.25-1% da conta | ✅ Confirmada | Com nuance histórica: em contas pequenas arriscava 0.5-1.5% |
| Posição individual 10-20% da conta; nunca >30% overnight num único título | ✅ Confirmada | O limite de 30% é **por título/ETF**, não agregado — a leitura da v4 em 3.5 está correta |
| Saída: vender 1/3-1/2 aos 3-5 dias ou 2-3R; stop para breakeven; resto trailed pela MA10/20; fecho abaixo da MA = saída total | ✅ Confirmada | Citação direta do Kullamägi; a escolha MA10 vs MA20 depende da velocidade do título; em mercados fracos vende mais (1/2 aos 3 dias), em fortes menos (1/3 aos 4-5 dias) |
| Entrada dimensionada de uma vez, não em 3 camadas (finding #2 da v4) | ✅ Confirmada | "Buys his full positions in one go" — a estrutura 25-30/30-40/30-35% do JSON original não tem base no método. Ver porém V5-3 (pirâmide) |
| Sem sistema de scoring ponderado; método funciona por portões pass/fail (finding #1) | ✅ Confirmada | Nenhuma fonte descreve médias ponderadas; todas as implementações públicas são checklists binárias |
| Filtro de mercado MA10 vs MA20 do índice (finding 3.9) | ✅ Confirmada com caveat | Instrumentos de referência: **QQQ e SPY, ambos saudáveis**. Caveat: a mecanização exata (crossover MA10/MA20) só aparece no ecossistema de fontes secundárias — ver V5-8 |
| Subida prévia 30-100%+ em 1-3 meses; consolidação 2-8 semanas; surf da MA10/20 | ✅ Confirmada | Consistente em todas as fontes |
| EP: gap ≥10%, ação parada 3-6+ meses antes, entrada no ORH, stop no low do dia | ✅ Confirmada | Exceto a regra de volume — ver V5-1. Detalhe adicional: ORH no timeframe de 1 min, reforço na quebra do máximo de 5 min, fallback no máximo da 1ª hora |
| Sem research institucional/macro; método puramente técnico (finding #3) | ✅ Confirmada | Reforçada: os temas emergem *bottom-up* dos scans (ver fecho do ponto 7.9, secção 6) |
| Stop nunca mais largo que 1×ADR | ✅ Confirmada com nuance | Algumas formulações próximas do primário dizem "1×, máximo 1.5× ADR/ATR" — ver V5-4 |

---

## 4. Findings novos — correções e refinamentos à v4

| # | Finding | Severidade |
|---|---------|------------|
| V5-1 | Regra de volume dos EPs errada nas secções 3.3 e 3.6 da v4 ("volume >2× a média nos primeiros 15 min") — a regra real é ~uma ordem de grandeza mais exigente | **Alta** |
| V5-2 | Janelas de lookback: a 3.8 da v4 endossa "3/6/12 meses" como corretas, mas o screening real é top gainers absolutos a **1/3/6 meses** — contradição interna com o ponto 7.3 da própria v4 | **Alta** |
| V5-3 | Pirâmide omitida na reescrita proposta do critério 3 — o método real adiciona a vencedores quando há *novo setup*, como trade separado | Média |
| V5-4 | Tolerância do stop: "≤1×ADR" categórico vs "1× a 1.5×" nas fontes | Baixa |
| V5-5 | Threshold de ADR% fixado em ">4-5%" quando as fontes dão uma banda de 3% a >5% | Baixa |
| V5-6 | Tensão entre decisões pendentes #1 ("adotar 8 critérios") e #9 ("decidir destino do critério 5") — a #9 tem de ser decidida primeiro | Média |
| V5-7 | Reordenação: "Volume Validation" na posição 3 como gate autónomo pré-gráficos não corresponde ao método — a validação decisiva de volume é intradiária, no gatilho | Média |
| V5-8 | A mecanização do filtro de mercado (crossover MA10/MA20) circula apenas em fontes secundárias que se citam entre si — deve ser marcada como convenção, não como regra literal do Kullamägi | Média |

### V5-1 — Regra de volume dos Episodic Pivots (Alta)

A v4 escreve, em 3.3 e 3.6, que o EP "Triggered" exige "volume já >2× a média" nos primeiros 15 minutos, e apresenta isto na lista de "definições numéricas verificadas" prontas a substituir os steps do JSON.

**Verificação:** a regra documentada (artigo de EPs do próprio qullamaggie.com, confirmada por ChartMill e outras) é que o título deve negociar **aproximadamente o seu volume médio diário completo nos primeiros 15-20 minutos — ou mais depressa**. Isto não é "2× a média até esse momento do dia": é o volume de *um dia inteiro típico* concentrado nos primeiros minutos, o que projetado para o fecho dá tipicamente 5-10×+ o volume médio diário.

**Impacto:** a regra da v4 é muito mais permissiva do que a real. Um sistema implementado com ">2× a média nos primeiros 15 min" qualificaria como EP muitos gaps medíocres que o método real rejeita — precisamente o tipo de erro que a "tolerância zero à imprecisão" do framework diz querer evitar.

**Correção:** EP "Triggered" = gap ≥10% **+ volume acumulado ≥ volume médio diário (ADV) nos primeiros 15-20 minutos** + entrada na quebra do ORH (1 min; reforço aos 5 min; fallback máximo da 1ª hora) + stop no low do dia (≤1×ADR).

### V5-2 — Janelas de lookback do screening: 1/3/6 meses, não 3/6/12 (Alta)

O `criterio_1` do JSON original pede "força relativa 3, 6, 12 meses vs sector e market". A v4 marcou a metodologia exata como não confirmada (ponto 7.3) — mas ao mesmo tempo, na tabela da secção 3.8, escreveu que "o comprimento da janela (3/6/12 meses) já lá está, não precisa" de correção. Ou seja: a v4 declarou o ponto aberto numa secção e endossou-o implicitamente noutra.

**Verificação:** o screening real documentado é um **scan semanal dos top performers absolutos a 1, 3 e 6 meses** (top 1-2% do universo), com filtros de ADR% e de dollar volume. Duas diferenças relevantes para a implementação:

1. **Janelas: 1/3/6 meses**, não 3/6/12. A janela de 12 meses não aparece em nenhuma fonte; a de 1 mês (a mais curta e mais reativa) é a que o JSON original omite.
2. **Método: momentum absoluto** (percentagem de subida, ranking direto no universo), não "força relativa vs sector e market" à la IBD RS Rating. A comparação com o setor é um subproduto (os líderes do tema emergem do scan), não o cálculo primário.

**Correção:** reescrever `criterio_1.methodology.step_1` como "ranking semanal de % de variação a 1/3/6 meses, top 1-2% do universo, com filtro ADR% e dollar volume" e corrigir a linha correspondente da tabela de frescura da 3.8.

### V5-3 — Pirâmide: adicionar a vencedores é parte do método, como trade novo (Média)

A v4 corrige bem o critério 3 (entrada de uma vez, saída faseada), mas a reescrita proposta ficaria **incompleta ao ponto de proibir implicitamente algo que o método faz**: o Kullamägi adiciona a posições vencedoras — mas **apenas quando o título forma um novo setup completo**, nunca "porque está a ganhar". Cada reforço é tratado como um trade novo, com o seu próprio stop (daí os múltiplos níveis de stop visíveis nos streams dele).

**Correção:** o critério 3 reescrito deve ter três blocos: (a) entrada: dimensionada de uma vez no gatilho (`Account × Risco% ÷ Stop Distance`); (b) reforço: só em novo setup qualificado, avaliado pelo pipeline completo como trade independente com stop independente; (c) saída: 1/3-1/2 aos 3-5 dias/2-3R, breakeven, trailing MA10/20. Isto fecha o ponto 7.4 da v4.

### V5-4 — Tolerância do stop: 1× vs 1.5×ADR (Baixa)

A v4 afirma "stop ≤1×ADR, caso contrário o método manda ignorar o trade" como regra categórica. As formulações mais próximas do primário dizem "não mais do que 1×, **máximo 1.5×** ADR/ATR". Manter 1× como default do sistema é defensável (é a variante conservadora) — mas deve ficar declarado no JSON como escolha de calibração, com a banda documentada, não como número único "do método".

### V5-5 — Threshold de ADR%: banda, não número (Baixa)

A v4 fixa "ADR% > 4-5%". As fontes dão uma banda: ≥3% em implementações públicas (TradingView), 3.5-4% em citações de entrevistas, >5% no screener descrito pela fonte mais detalhada. Recomendação: parametrizar (`adr_min` com default 4%, banda documentada 3-5%) em vez de fixar um número com falsa precisão — o mesmo princípio que a própria v4 aplicou ao scoring em 3.1.

### V5-6 — Ordem das decisões pendentes: #9 antes de #1 (Média)

A decisão pendente #1 da v4 ("adotar 8 critérios — 7 originais + filtro de mercado") pressupõe que o critério 5 (temas setoriais) sobrevive como critério autónomo. Mas a decisão #9 deixa em aberto absorvê-lo no step_1 do pipeline — o que daria 6 critérios + gate, não 8. Se a mission for corrigida para "8" antes de decidir a #9, arrisca-se a repetir exatamente o erro original ("9 critérios" fósseis de uma versão anterior). **Sequência correta: decidir #9 → contar → só então corrigir a mission.** Com o fecho do ponto 7.9 (ver secção 6), a recomendação desta v5 é absorver o critério 5 no pipeline — o que daria "6 critérios + 1 gate" ou "7 passos", conforme a redação escolhida.

### V5-7 — Posição do volume na reordenação (Média)

A reordenação da v4 coloca "Volume Validation" na posição 3, como gate autónomo entre momentum e gráficos. Mas no método real não existe uma "análise forense de volume" pré-trade autónoma: a validação decisiva de volume é **intradiária e acontece no gatilho** — ADV nos primeiros 15-20 min para EPs, expansão de volume na quebra para breakouts (os próprios checkpoints 3.8 da v4 dizem isto). O que faz sentido verificar *antes* dos gráficos é apenas liquidez de base (dollar volume — ver fecho do ponto 7.6).

**Refinamento proposto:** fundir o critério 7 com o critério 6 (o volume passa a ser condição do gatilho, com poder de veto no momento da entrada) e reduzir a posição 3 da reordenação a um filtro simples de liquidez (dollar volume ≥ $100M). Isto também resolve a decisão pendente #10 da v4 (peso 10 desalinhado com "evidência forense"): o volume deixa de ser pontuado e passa a gate do gatilho — um veto não precisa de peso.

### V5-8 — Filtro de mercado: mecanização é convenção secundária (Média)

O gate MA10>MA20 proposto na 3.9 da v4 é direcionalmente correto e deve manter-se. Mas esta v5 constatou que a formulação exata ("quando a MA10 cruza abaixo da MA20, os setups falham repetidamente") circula num conjunto de fontes secundárias que se citam entre si — não foi possível confirmá-la como frase/regra literal do Kullamägi em material primário. O que está bem estabelecido: ele opera tamanho grande apenas com mercado em uptrend confirmado, reduz drasticamente ou para em mercado fraco, e os instrumentos de referência são **QQQ e SPY em conjunto**. Recomendação: manter o gate, referenciá-lo a QQQ+SPY (ambos têm de passar), e anotar no JSON que a mecanização por crossover é convenção de implementação inspirada no método, não citação.

---

## 5. Consistência interna da v4 — verificações que passaram

Para registo do que foi checado e **não** tem problema:

- Soma dos pesos (20+15+10+15+20+10+10 = 100) e a leitura de que "9" é resíduo fóssil: corretas.
- Numeração de findings (1-8 no grupo A, 9-13 no grupo B) e referências cruzadas entre secções: consistentes.
- Tabela de reordenação da secção 5 vs lista numerada: consistentes entre si.
- Aritmética do finding 3.5 (3 posições × 15-20% = 45-60% de exposição agregada correlacionada): correta, e a leitura do limite de 30% como sendo por título individual está certa.
- A definição mecânica de "extensão" via 1×ADR (4.2) como resolução do "Invalidation speed protocol": consistente com as fontes (com a nuance V5-4).
- O disclaimer proposto em 3.7: os números (25-30% win rate, winners 5-20x, perdas ~1R) verificam todos.
- Findings 4.1 (critério 5 circular), 4.2 (referências para a frente), 4.3 (duplicações), 4.4 (contrato de dados) e 4.5 (fail-fast): a lógica mantém-se válida; nada encontrado que os contrarie.

---

## 6. Fecho da secção 7 da v4 — ponto a ponto

1. **Fontes primárias (7.1)** — *Parcialmente resolvido.* Acesso direto a qullamaggie.com/jackcorsellis/substack bloqueado (403) neste ambiente; Scribd por ler. Compensado com triangulação mais larga (≈12 fontes vs 2 queries da v4) incluindo duas declarações diretas do Kullamägi. A validação final contra material primário integral mantém-se como pré-requisito de implementação.

2. **Parabolic shorts (7.2)** — *Resolvido.* É de facto o terceiro setup, com regras documentadas: título a subir 3-5+ dias consecutivos, acelerando; nunca shortar no dia 1 (raramente no 2); entrada no dia 3-5 no primeiro sinal de fraqueza — quebra do opening range **low** (candle de 1 ou 5 min), primeiro candle vermelho de 5 min após gap up, ou (gatilho preferido) bounce falhado no VWAP; alvo = MA10/MA20; stop ≤1×ADR; mesma gestão de saída faseada. **Decisão de âmbito para o framework:** manter long-only é legítimo, mas deve ser declarado explicitamente no JSON (ex.: `"scope": "long-only — parabolic shorts deliberadamente fora de âmbito"`), para que a omissão passe de lacuna a escolha.

3. **Metodologia de ranking de força relativa (7.3)** — *Resolvido.* Ver V5-2: scan de top performers absolutos a 1/3/6 meses (top 1-2% do universo), não percentil vs setor/mercado, e não 3/6/12.

4. **Regras de pirâmide (7.4)** — *Resolvido.* Ver V5-3: reforço só em novo setup completo, tratado como trade independente com stop próprio.

5. **Definição quantitativa de "flat" pré-EP (7.5)** — *Não resolvido.* Nenhuma fonte dá threshold numérico; continua qualitativo ("sideways 3-6+ meses"). Sugestão: operacionalizar com um proxy declarado como convenção própria do framework (ex.: range total do período ≤ N×ADR, N a calibrar em backtest), nunca como "regra do Kullamägi".

6. **Float e liquidez (7.6)** — *Resolvido.* O filtro real é de **liquidez em dólares, não de float**: dollar volume > $100M/dia (títulos que as instituições conseguem negociar), líderes NASDAQ. Não há regra documentada de preferência por float baixo. Correção ao JSON: o filtro `daily_volume: ">500k shares"` do step_2 deve passar a dollar volume — 500k ações de um título de $5 são $2.5M/dia, duas ordens de grandeza abaixo do universo real do método.

7. **Earnings como risco de evento (7.7)** — *Resolvido.* Declaração direta (tweet): *"I only hold through earnings if I have a good profit on the stock and have sold a partial for profit already."* Sem almofada de lucro + parcial já vendida, sai antes do evento. A tensão que a v4 intuía não existe: nos EPs o gap de earnings **é** o catalisador e a entrada é *depois* do evento — não há contradição com evitar *segurar* posições através de earnings. Correção ao JSON: adicionar ao critério de risco/timing a regra "posição sem parcial vendida não atravessa earnings".

8. **Índice do filtro de mercado (7.8)** — *Parcialmente resolvido.* QQQ **e** SPY, em conjunto ("ambos saudáveis"), nas fontes disponíveis — não IWM nem ETF setorial. A verificação adicional de o ETF do tema também estar saudável (como a 3.9 da v4 propõe) é razoável mas é extensão do framework, não regra documentada. Ver também V5-8.

9. **Sourcing do critério de temas setoriais (7.9)** — *Resolvido, na direção que a v4 suspeitava.* O processo real é bottom-up: os temas detetam-se porque **vários títulos do mesmo grupo aparecem simultaneamente nos scans a formar setups** — "se muitos títulos de um grupo estão a preparar-se para romper juntos, isso é pista sobre a rotação". Não há análise diária de ETFs setoriais top-down nem research institucional. Implicação: o critério 5 e o step_1 do pipeline devem ser redefinidos como *agregação dos resultados do scan por tema* (contar setups por grupo), o que reforça a recomendação da v4 (4.1) de o retirar como critério pontuado — e alimenta a decisão V5-6.

---

## 7. Decisões pendentes — lista consolidada (substitui a secção 6 da v4)

1. **Decidir o destino do critério 5 primeiro** (era #9 da v4): recomendação desta v5 — absorver no pipeline como agregação de scans por tema (bottom-up). Só depois corrigir a contagem na `sistema_identity.mission` (era #1).
2. **Reescrever o critério 3 com os três blocos** entrada única / reforço só em novo setup (trade independente) / saída faseada — v4 #2 + V5-3.
3. **Substituir `sources_obrigatorias` por parâmetros técnicos** (v4 #3), agora com os valores corrigidos: scans 1/3/6 meses top 1-2%, ADR% parametrizado (banda 3-5%, default 4%), dollar volume ≥ $100M, MA10/MA20.
4. **Corrigir a regra de volume dos EPs** para "ADV completo nos primeiros 15-20 min" (V5-1) — substitui o ">2× média" da v4 em qualquer implementação.
5. **Teto de exposição agregada por tema + disciplina de stop** (v4 #4) — mantém-se tal como está.
6. **Disclaimer com base estatística real** (v4 #5) — mantém-se tal como está; números todos confirmados.
7. **Substituir contagem de caracteres por checklist** (v4 #6) — mantém-se.
8. **Adotar a reordenação com passo 0**, com o refinamento V5-7: fundir critério 7 no critério 6 (volume como condição de gatilho com veto), posição 3 reduzida a filtro de liquidez. Resolve também o v4 #10 (peso do volume).
9. **Especificar o critério 8 (filtro de mercado)** referenciado a QQQ+SPY, com a mecanização MA10/MA20 anotada como convenção de implementação (V5-8).
10. **Declarar o âmbito long-only** no JSON, ou especificar parabolic shorts como setup adicional (secção 6, ponto 2).
11. **Adicionar a regra de earnings** ao critério de risco/timing (secção 6, ponto 7).
12. **Operacionalizar "flat" pré-EP como convenção declarada** com calibração própria (secção 6, ponto 5).
13. **Validação final contra material primário integral** (v4 #12) — mantém-se aberta; ver limitação de acesso na secção 1. Prioridade: artigo de EPs e "3 timeless setups" no qullamaggie.com, documento Scribd, streams arquivados.

---

## 8. Fontes desta meta-auditoria

Obtidas via pesquisa dirigida (excertos indexados); leitura direta bloqueada por 403 onde indicado.

**Declarações diretas do Kullamägi:**
- [Tweet sobre earnings — @Qullamaggie](https://x.com/Qullamaggie/status/1587130234574356485) — "I only hold through earnings if I have a good profit on the stock and have sold a partial for profit already."
- [Citação sobre regras de saída — via @AsymTrading](https://x.com/AsymTrading/status/1706716710735085833) — "sell 1/3 to 1/2 of the position after 3-5 days, and then move the stop to break even. The rest of the position should be trailed with the 10- or the 20-day moving average."

**Fontes primárias (403 a leitura direta nesta sessão; conteúdo via excertos):**
- [How to master a setup: Episodic Pivots — qullamaggie.com](https://qullamaggie.com/how-to-master-a-setup-episodic-pivots/)
- [3 TIMELESS setups — qullamaggie.com](https://qullamaggie.com/my-3-timeless-setups-that-have-made-me-tens-of-millions/)
- [FAQ — qullamaggie.com](https://qullamaggie.com/faq/)

**Fontes secundárias consultadas nesta v5 (para além das da v4):**
- [He turned $5,000 into $100 million. His win rate was 25% — Stats Edge Trading](https://letters.statsedgetrading.com/p/he-turned-5000-into-100-million-his)
- [Systemizing Kullamägi's Parabolic Short Setup — Stonks Capital](https://stonkscapital.substack.com/p/systemizing-kullamagis-parabolic)
- [Qullamaggie Screens — Deepvue](https://deepvue.com/screener/qullamaggie-screens/)
- [Mastering the Qullamaggie Episodic Pivot Setup — ChartMill](https://www.chartmill.com/documentation/stock-screener/technical-analysis-trading-strategies/494-Mastering-the-Qullamaggie-Episodic-Pivot-Setup-A-Flexible-Stock-Screening-Approach)
- [Qullamaggie on Chat With Traders — transcrição, Trading Resource Hub](https://tradingresourcehub.substack.com/p/qullamaggie-chat-with-traders-reimagined-transcript)
- [Qullamaggie's Breakout Entry Strategy — Grokipedia](https://grokipedia.com/page/Qullamaggies_Breakout_Entry_Strategy)
- [The Episodic Pivot Strategy — Financial Wisdom TV](https://www.financialwisdomtv.com/post/the-episodic-pivot-strategy-qullamaggie-s-high-momentum-setup-explained)
- [Qullamaggie Breakout V2 — TradingView (millerrh)](https://www.tradingview.com/script/5bTajWQM-Qullamaggie-Breakout-V2/)
- [How to Trade Like Qullamaggie — Breakouts Happen](https://breakoutshappen.com/stock-news/how-to-trade-like-qullamaggie-setups-strategy-and-screener) *(já usada na v4)*
- [Legends Of Trading: Qullamaggie — Timothy Sykes](https://www.timothysykes.com/blog/qullamaggie/) *(já usada na v4)*

---

*Fim da meta-auditoria. Este documento é autocontido em conjunto com o handoff v4 — as secções 3-6 referenciam a numeração da v4 diretamente.*
