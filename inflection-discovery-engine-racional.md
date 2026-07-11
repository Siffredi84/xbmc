# Motor de Discovery de Inflexões — Racional das Escolhas

**Data:** 11/07/2026
**Companheiro de:** `inflection-discovery-engine.json` (framework autónomo, v1.0)
**Propósito:** Justificar cada escolha de design do motor, ancorada na evidência empírica da série (sessão v1 de 20/10/2025, post-mortem, engenharia reversa das duas forças), e explicar porque cada bloco torna as pesquisas mais granulares e a triangulação mais forte do que no step_1/critério 5 originais.

---

## 1. A decisão-mãe: industrializar competência, não descrever intenções

O step_1 do v1 produziu um resultado 4/4 — mas o post-mortem mostrou que o mérito estava no *operador*, não no *contrato*: as instruções eram inexequíveis ("Institutional rotation data (BlackRock, State Street reports)" — dados que não existem para uma sessão LLM) e os critérios de qualificação eram adjetivos sem instrumento de medida ("institutional_attention: Present mas not saturated" — presente segundo quem? saturado medido como?). Quando o operador é excelente, o resultado é excelente; quando não é, o mesmo contrato produz confabulação com aspeto de análise — o risco central identificado na auditoria v4.

**Toda a arquitetura do motor deriva desta decisão:** cada fase converte um comportamento que o operador de 20/10/2025 executou por competência própria num procedimento com template, contagem e critério de reprovação. A pergunta de design foi sempre: *"que instrução teria forçado um operador medíocre a fazer o que o operador excelente fez espontaneamente?"*

---

## 2. Justificação fase a fase

### Fase 0 — Definição operacional de "inflexão"

**O que o v1 tinha:** nada. "Emerging themes ANTES mainstream" sem definir "emerging" nem "antes".

**Porquê esta escolha:** sem definição do alvo, qualquer narrativa interessante qualifica como tema — e a sessão só não caiu nisso porque o operador trazia a definição na cabeça. Definir inflexão como *mudança de regime na taxa de compromissos custosos* tem três virtudes: (a) é **observável** (os 3 observáveis da fase 0 são pesquisáveis: aceleração de sinais L3+, lead times, gradiente de cobertura); (b) é **falsificável** (um tema sem observáveis reprova, por muito boa que seja a prosa); (c) distingue **derivada de nível** — a anti-definição ("tendência estabelecida não é inflexão") mata à entrada o erro mais comum do retail, que é comprar o tema certo tarde demais.

**Porque torna a pesquisa mais granular:** a pesquisa deixa de ser "o que está a acontecer no setor X?" (pergunta de enciclopédia) e passa a ser "a taxa de compromissos na camada X mudou nos últimos 90 dias?" (pergunta de deteção, com resposta sim/não/dados).

### Fase 1 — Cinco motores de hipóteses em vez de "ler fontes"

**O que o v1 tinha:** uma lista de 4 "sources_obrigatorias" (duas inexistentes/inacessíveis) e a esperança de que os temas emergissem da leitura.

**Porquê cinco motores:** a engenharia reversa mostrou que os 3 temas de 20/10/2025 saíram todos do mesmo molde cognitivo (gargalo + segunda linha). Um molde que funcionou 3 vezes merece ser template — mas um só molde é um single point of failure cognitivo: há inflexões que não são gargalos físicos. Os motores 2-4 generalizam o mecanismo para as outras formas conhecidas de capex forçado:

| Motor | Tipo de inflexão que deteta | Exemplo do padrão (da própria série) |
|---|---|---|
| 1 — Gargalo | Física/capacidade trava o doubling | Bump pitch <2 µm → hybrid bonding obrigatório |
| 2 — Derivada segunda | Procura já visível nos bookings, ainda não na receita | ASMPT bookings +71,6% YoY vs receita +32% (Q1 2026) — o gap ERA o sinal |
| 3 — Standards | Lista de fornecedores cristaliza | Specs OCP de liquid cooling (Tema 3); HBM4/JEDEC |
| 4 — Política financiada | Estado converte apropriação em POs | NAPMP $1,4B final awards (não a proposta — o award) |
| 5 — Segunda linha | O vencedor mainstream cria a camada invisível seguinte | "Vertiv já é mainstream → CDUs/manifolds/integradores" (movimento explícito da sessão) |

**A regra do formato obrigatório da hipótese** ("A camada X da cadeia Y vai receber capex forçado porque [restrição]") é o primeiro filtro anti-narrativa: uma hipótese que não consegue nomear camada + restrição não é uma tese de inflexão, é um tema de conversa.

**Porque torna a pesquisa mais granular:** cada motor tem o seu campo "onde_procurar" com fontes de *tipo* diferente (imprensa técnica, releases de bens de capital, calendários de standards, diários de awards públicos, teardowns/supply chain). O v1 pedia uma leitura genérica do mundo; o motor pede 5 varrimentos dirigidos, cada um com critério próprio de "há sinal aqui". Cinco perguntas estreitas e respondíveis batem uma pergunta larga e vaga — tanto para um humano como para uma sessão LLM com pesquisa web.

### Fase 2 — Cartografia da portagem

**O que o v1 tinha:** o critério 5 falava de "mapa de liquidez" e "liderança interna" mas nunca pedia o mapa — a sessão de 20/10 desenhou-o (testar→colar→inspecionar→embalar) por iniciativa própria.

**Porquê esta escolha:** a engenharia reversa concluiu que o 4/4 não foi diversificação — foi **cobertura de etapas sequenciais do mesmo fluxo físico** (quatro monopólios funcionais, uma única aposta real: "vai passar tráfego?"). O procedimento de 5 passos força exatamente essa construção: fluxo → operadores → concentração → elasticidade → modo de falha.

Duas escolhas dentro da fase merecem justificação individual:

- **"Cobra por unidade do volume novo" (passo 4):** separa portagens de beneficiários difusos. FORM cobra por die testado; um "beneficiário de IA" genérico cobra por sentimento. A elasticidade por unidade é o que liga a tese física à conta de resultados sem precisar de modelos de valuation.
- **"Modo de falha" (passo 5):** é a generalização do insight ONTO — *a portagem mais defensável vende à dor do tema, não ao sucesso*: a procura por inspeção cresce com os problemas de yield, que crescem com a complexidade, que cresce mesmo quando as margens do tema apertam. Nenhum framework que eu conheça pede isto explicitamente; a sessão de 20/10 fê-lo intuitivamente ("ONTO não vende ao tema; vende ao modo de falha do tema") e o resultado (+129% com a tese intacta ao longo de um crash setorial) valida promovê-lo a passo obrigatório.

**A regra anti-correlação** (um ticker por etapa) converte a lição de risco do post-mortem (4 nomes = correlação ~1, contida por teto de exposição no sistema de execução) em disciplina de construção da própria watchlist.

### Fase 3 — Triangulação por sinais custosos (o coração, e a resposta direta à pergunta "porquê mais granular")

**O que o v1 tinha:** "institutional_attention: present mas not saturated" — um juízo. A sessão de 20/10 substituiu-o, por competência, pela pilha Kinex+HBM4+TSMC+Amkor+NAPMP. A fase 3 é essa pilha transformada em gramática.

**As três escolhas estruturais e porquê:**

1. **Sete classes de emissor** (vs nenhuma taxonomia no v1). A força epistémica da triangulação vem da *independência entre classes* — um fornecedor, uma memória, uma foundry, um Estado e um cliente final não erram em cascata, porque têm funções, incentivos e horizontes diferentes. Contar *classes* (não sinais) impede que 5 press releases do mesmo ecossistema contem como 5 confirmações. As classes 6 (talento) e 7 (infraestrutura física) são as duas dimensões que o v1 nem tocava e que **antecedem a imprensa por trimestres**: vagas para "hybrid bonding process engineers" e permits de obra aparecem 6-12 meses antes do primeiro artigo financeiro — são os sinais mais "invisíveis ao retail" de toda a taxonomia, e é por isso que estão lá.

2. **Hierarquia L1-L5 de custo do sinal** (vs tudo ao mesmo nível no v1). O princípio — *quem paga para falar > quem é pago para falar* — converte "revealed preference" em regra de contagem: capex irreversível (L5) pesa mais do que um produto lançado (L4), que pesa mais do que um contrato (L3), e o discurso (L1) **nunca conta**. A regra L1-como-pointer preserva a única utilidade legítima da opinião: o PT da Oppenheimer a 14/10 não provou nada, mas apontou para onde procurar os L4/L5 — foi exatamente assim que a sessão o usou, e a regra codifica esse uso e proíbe o abuso.

3. **Janela dupla 90/30 dias** (vs "theme freshness <30 days" aplicado só a media coverage no v1). A concentração temporal é o detetor de inflexão: sinais custosos espalhados por 2 anos descrevem uma indústria; concentrados em semanas, descrevem uma mudança de regime. A exigência de ≥1 sinal nos últimos 30 dias ("rajada") é a formalização do que a sessão fez ao datar tudo ("últimos 30 dias", "últimos 7 dias", "3 dias") — a v1 exigia frescura da *cobertura*; o motor exige frescura do *compromisso*, que é o que realmente importa.

**Porque a triangulação fica melhor:** no v1, triangular era um talento; aqui é uma contagem com teste de independência e regra anti-cascata ("sinais que citam a mesma fonte primária contam como um"). O output é auditável: qualquer pessoa pode re-verificar `classes_convergentes: 5` seguindo as fontes datadas — o que é impossível com "institutional attention present".

### Fase 4 — Teste de invisibilidade (gradiente de cobertura)

**O que o v1 tinha:** "retail_awareness: Minimal - not em mainstream financial media" — direcionalmente certo, sem instrumento.

**Porquê o gradiente de 4 níveis:** "invisível ao retail" não é binário — a informação viaja por um corredor previsível (imprensa técnica → sell-side especializado → imprensa financeira → retail media), e o edge morre progressivamente ao longo dele. Medir *em que nível está a sub-camada* (não o tema-mãe — distinção crítica: "IA" era mainstream em out/2025, "hybrid bonding tooling" estava no nível 1-2, e foi aí que a sessão viu o edge) dá três coisas que o v1 não tinha: **(a)** um critério de entrada verificável (≤ nível 2), **(b)** um critério de *saída do edge* (nome próprio na imprensa financeira, ETF temático dedicado — o v1 não tinha nenhum conceito de morte do tema), e **(c)** uma métrica de lead time para a fase 6.

**A regra "ausência verificada, não assumida"** obriga a procurar ativamente o tema nos níveis 3-4 e a registar o que se encontrou — sem isto, "não está no retail" degenera em "não me apeteceu procurar".

### Fase 5 — Cartões de tese (o critério 5 reconstruído)

**O que o v1 tinha:** o critério 5 como bloco pontuado (peso 20) a meio da análise técnica — a auditoria v4 mostrou a circularidade (pontuar o tema que já filtrou os candidatos) e o post-mortem mostrou o dano (a nota 9,0 do tema mascarou o momentum fraco da ONTO).

**Porquê o cartão padronizado de 8 campos:** cada campo é uma lição paga da série:

| Campo do cartão | Lição de origem |
|---|---|
| `etapa_da_portagem` | O 4/4 veio de um ticker por etapa (engenharia reversa §2.2) |
| `frase_da_restricao` (reprova se precisar de "narrativa"/"hype") | Separa capex forçado de momentum de sentimento — o teste que a ONTO passava e uma meme stock não passa |
| `perna_produto` / `perna_procura` / `perna_validacao` | O padrão fractal "3 pernas" detetado em todos os tickers da sessão (engenharia reversa §3.2) |
| `gradiente_cobertura` do ticker | Um tema invisível pode ter um ticker já visível (e vice-versa) — medem-se separados |
| `calendario_do_instrumento` obrigatório | A falha mais cara do post-mortem: a sessão sabia o call da BESI (23/10) e ignorou os earnings da AMKR (27/10), FORM (29/10) e ONTO (06/11). Um cartão sem calendário **não pode ser entregue** — é a única proibição absoluta da fase 5 |
| `invalidadores` pré-registados | Anti-survivorship: a tese declara à nascença o que a mataria; impede racionalização retroativa e alimenta a métrica de honestidade preditiva da fase 6 |
| `estado` | Liga o cartão ao ciclo de vida da fase 6 |

**Liquidez parametrizada à conta** (`max($5M, 100 × posição máxima)`): o post-mortem provou os dois erros simétricos — o v1 com ">500k shares" deixava entrar tudo; o v2 com $100M fixos excluía 3 dos 4 vencedores (AMKR $80M, FORM $40M, ASMPT $38M). A liquidez correta é função do tamanho de quem executa, logo é parâmetro, nunca constante.

**A fronteira dura de âmbito** (watchlist + calendário, zero execução): é a conclusão de toda a série destilada numa regra — a narrativa informa convicção e prioridade, **nunca** decide entrada, stop ou tamanho. O motor entrega candidatos a *qualquer* sistema de execução; a contaminação narrativa→execução (o pecado original do v1, onde o mesmo documento fazia as duas coisas) torna-se estruturalmente impossível porque o output não contém os campos.

### Fase 6 — Registo e autoavaliação

**O que o v1 tinha:** nada. Nenhum conceito de ciclo de vida, arquivo ou medição do próprio motor.

**Porquê:** toda esta série de auditorias só foi possível porque existia rasto (a transcrição de 20/10). A fase 6 desenha o rasto à partida: estados datados (embrião→qualificado→maduro→morto), arquivo imutável de cartões e pilhas, revisão mensal com 4 passos, e — a escolha mais importante — **métricas do próprio motor**: lead time até ao mainstream (o motor chega mesmo cedo?), taxa de maturação (os temas qualificados realizam-se?) e honestidade preditiva (os invalidadores pré-registados foram os que mataram as teses mortas, ou eram decorativos?). Um motor de teses sem estas métricas é infalsificável por construção — acumula os acertos na memória e deixa os erros evaporar. Com elas, o motor pode ser auditado daqui a 12 meses exatamente como esta série auditou o v1.

---

## 3. O dry-run: o motor contra 20/10/2025

Teste de desenho — o motor tem de reproduzir o acerto do v1 E apanhar a falha que o v1 deixou passar:

- **Fase 1:** Motor 1 gera "hybrid bonding/AP" (bump pitch <2 µm); Motor 5 gera a mesma camada a partir de NVDA/HBM; Motor 4 gera-a a partir do NAPMP. Três motores a convergir na mesma camada já é sinal.
- **Fase 2:** o mapa produz as 5 etapas (testar/colar/inspecionar/embalar/+equipar) com FORM, ASMPT+BESI, ONTO+CAMT, AMKR — e identifica a inspeção como modo de falha.
- **Fase 3:** contagem = 5 classes ≥L3 (Kinex L4 classe 1; HBM4 L4 classe 2; TSMC AZ L5 classe 2/3; Amkor $7B L5 classe 3; NAPMP L5 classe 5), com rajada (Kinex 07/10, 13 dias antes) → **QUALIFICADO, convicção máxima**. Oppenheimer = L1, não conta, funcionou como pointer.
- **Fase 4:** sub-camada nos níveis 1-2 (Semiconductor Engineering, IEEE, imprensa técnica) → invisível. ✔
- **Fase 5:** 4 cartões, um por etapa — e o campo obrigatório `calendario_do_instrumento` teria posto **AMKR 27/10, FORM 29/10, ONTO 06/11** na primeira página do output. A informação que faltou ao plano de execução do v1 estaria no deliverable do motor por construção.
- **Fase 6:** os cartões de 20/10/2025 teriam hoje: tema "maduro" (a sub-camada ganhou cobertura generalista no 1S2026), lead time ≈ 6-8 meses, e os invalidadores nunca acionados — métricas que provariam, com dados, que o motor chegou cedo.

O motor passa o teste nas duas direções: reproduz a descoberta e teria evitado a omissão mais cara.

---

## 4. Limites declarados (o que este motor não resolve)

1. **Timing fino:** a fase 3 deteta que a inflexão está a acontecer (rajada), mas "física certa, calendário errado" continua possível — a defesa é a janela de 90/30 dias + os invalidadores, não uma garantia. O acoplamento a um sistema de execução com confirmação por preço continua a ser onde o timing se resolve.
2. **Qualidade do operador continua a importar:** os templates reduzem a variância, não a eliminam — o Motor 1 nas mãos de quem não percebe a física da cadeia produz mapas rasos. O motor industrializa o *procedimento* das duas forças; a profundidade de domínio continua a ser input humano (ou de modelo com bom conhecimento técnico).
3. **Acesso a dados:** as classes 6-7 (vagas, permits) e o teste de invisibilidade dependem de pesquisa web efetiva; num ambiente com egress restrito (como o desta sessão), a cobertura degrada-se e deve ser declarada campo a campo — regra de honestidade nº 2.
4. **N=1 continua a ser N=1:** o desenho inteiro assenta num episódio brilhantemente documentado + mecanismos com validade estrutural independente. A fase 6 existe precisamente para converter N=1 em N=muitos com rasto auditável.

---

*O `inflection-discovery-engine.json` está pronto a usar como system prompt autónomo. O output dele (cartões + calendário) é deliberadamente compatível com qualquer sistema de execução — incluindo, se um dia quiseres, o v2 desta série, através do Overlay de Convicção já especificado na engenharia reversa. Mas não depende dele em nada.*
