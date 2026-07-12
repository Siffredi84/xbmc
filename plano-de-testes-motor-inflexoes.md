# Programa de Testes — Evolução do Motor de Discovery de Inflexões

**Data:** 11/07/2026
**Objeto:** `inflection-discovery-engine.json` v1.1
**Ponto de partida:** o motor tem, até hoje, **um único teste**: a corrida live de 11/07/2026 — que foi um *teste de fumo* bem-sucedido (executabilidade, discriminação, honestidade, diferenciação), mas com quatro limitações que nenhuma repetição do mesmo teste resolve: **N=1** (uma data), **um operador** (a mesma sessão que desenhou o motor), **zero outcomes medidos** (nenhum cartão viveu tempo suficiente), e **condições favoráveis** (um bull market de semis onde há sinais custosos por todo o lado).

Cada limitação pede uma família de testes própria. Este documento define as 8 famílias, justifica cada uma, e propõe o programa por prioridade.

---

## 0. As quatro ameaças metodológicas transversais (ler primeiro)

Qualquer teste ao motor enfrenta estes problemas — os desenhos abaixo existem para os mitigar, e um teste que os ignore produz confiança falsa:

1. **Leakage/hindsight:** o operador (um LLM) conhece o desfecho de qualquer data passada dentro do seu conhecimento de treino. Backtests "cegos" a datas históricas nunca são verdadeiramente cegos. Mitigação: privilegiar testes *forward* (o futuro é cego para todos), e tratar backtests como evidência fraca com protocolo de leakage declarado.
2. **Avaliador = executor:** até agora, a mesma sessão desenha o motor, corre a corrida e dá as notas. Mitigação: separar papéis — corridas numa sessão, avaliação noutra, sem partilha de contexto além dos artefactos arquivados.
3. **Survivorship do próprio programa:** testes falhados têm de ficar no arquivo com o mesmo destaque que os passados — a fase 6 do motor aplica-se ao programa de testes também.
4. **Dependência de regime:** todos os dados até hoje vêm do regime 2024-2026 (mania de capex de IA). Um motor calibrado só neste regime pode ser um detetor de "IA" disfarçado. Mitigação: forçar diversidade setorial nos testes (ver T4 e T5).

---

## As 8 famílias de testes

### T1 — Teste longitudinal forward (o padrão-ouro) — PRIORIDADE 1

**O que testa:** a única pergunta que importa no fim — *as contagens do motor preveem alguma coisa?* — sem qualquer possibilidade de hindsight.

**Como:** correr a `corrida_semanal` a intervalos fixos (semanal ou quinzenal) durante 3-6 meses, arquivando tudo (a fase 6 já define o arquivo). Nada se apaga; cada cartão nasce com data, janela e invalidadores. Ao fim do período, medir as três métricas que a fase 6 já especifica mas nunca foram alimentadas:
- **Lead time real** (qualificação → nível 3-4 do gradiente) — valida ou corrige a estimativa de ~6-9 meses inferida dos temas de out/2025;
- **Taxa de maturação** (% de qualificados que chegam a maduros vs mortos);
- **Honestidade preditiva** (% de teses mortas cujos invalidadores pré-registados foram os que de facto dispararam).
E uma quarta, proxy de valor (sem execução): retorno de um cabaz equal-weight dos cartões entregues vs benchmark setorial, medido da data do cartão em diante — não porque o motor prometa retornos, mas porque um motor cujos qualificados não se distinguem do benchmark não está a detetar nada.

**Justificação:** é o único teste imune ao leakage e o único que transforma o N=1 em N=muitos com dados limpos. Todas as outras famílias ou alimentam este ou dependem dele. O motor foi desenhado para ser auditável no futuro (fase 6); este teste é essa auditoria a acontecer.

**Custo/operacionalização:** ~10-15 pesquisas por corrida. Automatizável neste ambiente: uma Routine semanal que corre a corrida e arquiva o output no branch — posso configurá-la quando quiseres.

### T2 — Teste de variância do operador (reprodutibilidade) — PRIORIDADE 2

**O que testa:** a alegação central do motor — que ele "industrializa competência", i.e., que o output vem do procedimento e não do talento de quem o corre. Foi exatamente esta a falha do v1 (o step_1 só funcionou porque o operador de 20/10/2025 era bom).

**Como:** a mesma `corrida_semanal`, na mesma data, executada por 3+ sessões independentes sem contexto partilhado (idealmente também modelos/operadores diferentes). Medir sobreposição: % de hipóteses comuns na fase 1, % de temas com o mesmo veredito na fase 3-4, % de tickers comuns na fase 5 — e localizar *em que fase* as corridas divergem.

**Justificação:** se três operadores produzem watchlists disjuntas, o motor é um placebo processual e a competência continua a ser o motor real — é preciso saber isso antes de confiar em qualquer corrida individual. A localização da divergência diz o que corrigir: divergência na fase 1 pede templates de pergunta mais apertados; na fase 3, critérios de contagem mais mecânicos; na fase 4, fontes de gradiente enumeradas.

**Custo:** 3 sessões paralelas, um dia. Barato e de alto valor — devia anteceder qualquer confiança operacional no motor.

### T3 — Teste adversarial / red team dos gates — PRIORIDADE 3

**O que testa:** os falsos positivos. A corrida de 11/07 mostrou discriminação *incidental* (H1/H2 morreram sozinhas); nunca testámos os gates contra armadilhas *desenhadas*.

**Como:** construir um conjunto de temas-armadilha e injetá-los no pipeline via `deep_dive_tema`:
- **Armadilha de narrativa:** tema sedutor e rico em prosa mas pobre em sinais custosos (ex.: uma vaga retail tipo quantum/meme do momento) — a fase 3 tem de o reprovar por falta de ≥3 classes L3+;
- **Armadilha de cascata:** tema onde 5 "sinais" rastreiam todos para o mesmo press release — a regra anti-cascata tem de os colapsar num só;
- **Armadilha de eco temporal:** sinais custosos verdadeiros mas todos com >12 meses (indústria, não inflexão) — a regra da rajada tem de o travar;
- **Armadilha de invisibilidade:** tema que *parece* nível 1-2 mas tem um ETF dedicado pouco conhecido — o teste de "ausência verificada, não assumida" tem de o encontrar;
- **Armadilha L1:** pilha composta só de guidance, price targets e artigos — a regra "L1 nunca conta" tem de zerar a contagem.

**Justificação:** gates que nunca enfrentaram inputs hostis não são gates — são decoração que ainda não falhou. É o equivalente ao teste de segurança de software: não se espera pelo atacante real. Cada armadilha apanhada valida uma regra específica; cada armadilha que passa identifica a correção exata para a v1.2.

**Custo:** meio-dia por bateria; repetível a cada versão do motor (suite de regressão).

### T4 — Teste de ablação das regras — PRIORIDADE 4

**O que testa:** quais regras fazem trabalho real e quais são peso morto — antes de calcificarem. O motor v1.1 tem ~15 regras duras nascidas de UM episódio; é quase certo que nem todas ganham o seu lugar.

**Como:** re-pontuar corridas *já arquivadas* (sem pesquisa nova — só re-aplicar regras modificadas à mesma evidência): desligar uma regra de cada vez (sem "L1 nunca conta"; sem rajada; sem gradiente; sem regra anti-correlação; com janela de 180 dias em vez de 90) e comparar o output com o da corrida original. Uma regra cuja remoção não muda nenhum veredito em N corridas é candidata a simplificação; uma cuja remoção deixa passar armadilhas do T3 é load-bearing e ganha estatuto de intocável.

**Justificação:** frameworks acumulam regras por trauma (cada auditoria desta série acrescentou algumas) e nunca as removem — ao fim de 10 versões, o processo fica tão pesado que ninguém o corre. A ablação é a única defesa disciplinada contra isso, e é quase grátis porque reutiliza corridas arquivadas.

### T5 — Teste de generalização de regime e setor — PRIORIDADE 5

**O que testa:** a ameaça metodológica nº 4 — se o motor é um detetor de inflexões ou um detetor de "capex de IA 2024-2026".

**Como:** duas variantes:
- **Setorial:** forçar corridas com o universo de IA/semis *excluído à partida* (comando com exclusão explícita): o motor encontra inflexões em saúde, indústria, energia tradicional, materiais? Se as fases 1-3 voltarem vazias fora de semis, os motores de hipóteses estão enviesados (as perguntas-template podem estar implicitamente calibradas para hardware).
- **De regime:** correr o `deep_dive_tema` sobre temas históricos de regimes diferentes, com protocolo de leakage declarado (evidência fraca, mas orientadora): GLP-1 em 2021-22, lítio em 2020, shipping em 2020 — o padrão sinais-custosos-antes-do-mainstream existia nesses casos? Em que classes?

**Justificação:** um motor que só funciona num regime é uma posição, não um sistema. E há uma razão estrutural para suspeitar de viés: as 7 classes de emissor e os 5 motores foram destilados de UM tema de hardware. O teste setorial é forward e limpo; o de regime é retrospetivo e fraco, mas barato e diz onde procurar classes de sinal em setores onde "capex" tem outra forma (ensaios clínicos, licenças, FDA...).

### T6 — Teste de degradação graciosa (robustez ao ambiente de dados) — PRIORIDADE 6

**O que testa:** o medo original da auditoria v4 — confabulação sob pressão. As regras de honestidade funcionaram na corrida de 11/07 com pesquisa razoável; nunca foram testadas com fome de dados.

**Como:** correr a mesma corrida sob orçamentos decrescentes (25 → 10 → 5 → 2 pesquisas) e medir o comportamento: o output honesto encolhe (menos cartões, mais NÃO OBTÍVEL, mais retidos) ou o output mantém o tamanho à custa de afirmações sem fonte? Qualquer sinal sem fonte+data que apareça nas corridas famintas é uma falha crítica do motor (não do operador — o motor tem de tornar a confabulação estruturalmente difícil).

**Justificação:** o modo de falha mais perigoso de um sistema destes não é errar — é *parecer completo quando não tem dados*. A degradação tem de ser visível no próprio output. Este teste é a versão empírica da "tolerância zero à imprecisão" que o v1 declarava e violava.

### T7 — Teste de integração a jusante (o consumidor do output) — PRIORIDADE 7

**O que testa:** a fronteira de âmbito. O motor entrega cartões + calendário e jura que qualquer sistema de execução pega neles — isso é uma alegação de interface que nunca foi exercitada.

**Como:** pegar nos cartões reais da corrida de 11/07 (FORM, TER) e correr o handoff completo: (a) para o pipeline v2 (via o Overlay de Convicção já especificado na engenharia reversa) — os gates técnicos do v2 conseguem consumir os cartões sem pedir informação que o cartão não tem? (b) para um humano — um trader que só leia o cartão sabe o que vigiar e quando? Registar cada campo em falta ou ambíguo.

**Justificação:** a separação discovery/execução foi a decisão arquitetural mais importante da série; uma interface nunca testada entre os dois lados é onde ela partiria. Bónus: este teste produz, de graça, o paper-trade combinado motor+v2 — a primeira medição de ponta-a-ponta do sistema completo.

### T8 — Auditoria retroativa dos invalidadores (honestidade preditiva acelerada) — PRIORIDADE 8

**O que testa:** se os invalidadores que o motor escreve são *reais* (disparariam quando deviam) ou *decorativos* (vagos demais para disparar) — sem esperar os 6-18 meses do T1.

**Como:** escrever, com regras do motor, os invalidadores que os temas de out/2025 (advanced packaging, grid, liquid cooling) *teriam tido* à data — e verificar contra o registo de 2026: dispararam quando deviam? Ficaram mudos durante o crash de 05/06/2026 (que NÃO invalidou as teses — as encomendas continuaram)? Um bom conjunto de invalidadores tem de sobreviver a drawdowns de preço sem disparar e disparar em reversões de compromissos.

**Justificação:** é o único pedaço da honestidade preditiva testável já hoje, porque o post-mortem desta série já reconstruiu os outcomes de 2025-26 com fontes. E ataca a fraqueza específica dos invalidadores escritos por LLMs: soarem concretos e serem inoperáveis ("se o tema enfraquecer" não é um invalidador; "book-to-bill <1 dois trimestres seguidos" é).

---

## Matriz de priorização

| # | Teste | Ameaça que ataca | Custo | Quando |
|---|---|---|---|---|
| T1 | Longitudinal forward | N=1, zero outcomes | contínuo, baixo/corrida | **começar já** (Routine semanal) |
| T2 | Variância do operador | avaliador=executor, competência oculta | 1 dia | antes de confiar em corridas individuais |
| T3 | Adversarial dos gates | falsos positivos nunca testados | ½ dia/bateria | já; repetir a cada versão |
| T4 | Ablação de regras | inchaço regulatório | baixo (reusa arquivo) | após 4-6 corridas arquivadas |
| T5 | Generalização regime/setor | detetor-de-IA disfarçado | médio | mês 1-2 |
| T6 | Degradação graciosa | confabulação sob fome de dados | ½ dia | mês 1 |
| T7 | Integração a jusante | interface nunca exercitada | 1 dia | com os cartões de 11/07 ainda frescos |
| T8 | Invalidadores retroativos | invalidadores decorativos | ½ dia | já (o post-mortem já tem os outcomes) |

## Programa proposto (6 meses)

- **Semana 0:** arrancar T1 (Routine semanal de corrida + arquivo no branch); executar T8 e T3 (bateria 1) — três testes imediatos, dois deles sem pesquisa nova.
- **Semanas 1-2:** T2 (3 corridas paralelas na mesma data) e T6; consolidar correções → **v1.2**.
- **Mês 1-2:** T5 (corrida ex-semis; deep-dives históricos com protocolo de leakage); T7 com os cartões de 11/07.
- **Mês 3+:** T4 sobre o arquivo acumulado; primeira leitura das métricas do T1 (maturações, transições de gradiente, retidos desbloqueados).
- **Mês 6:** relatório de calibração — a pergunta final: `classes_convergentes` e os níveis L previram maturação e desempenho relativo? É este relatório que decide se o motor merece uma v2.0 ou uma reforma.

**Regra do programa:** cada teste falhado gera correção versionada com changelog (como a v1.1) — e nenhum teste passado se declara mais do que uma vez: passar deixa de ser notícia, falhar é que evolui o motor.

---

*Nota final: a série inteira nasceu de uma auditoria a um framework que nunca tinha sido testado contra nada. O programa acima é a diferença entre repetir essa história com um framework melhor — e não a repetir.*
