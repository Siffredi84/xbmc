# Auditoria final do projeto — aderência ao plano, ideias que mudaram o jogo, e parecer honesto

**Data:** 17/07/2026 · **Branch:** `claude/handoff-audit-0w2a31` · **41 commits de projeto, ~45 artefactos**
**Auditor:** a mesma entidade que executou o projeto — e essa frase é, ela própria, o primeiro achado da auditoria (ver §4.2). Este documento distingue-se da `SINTESE-FINAL` num ponto: a síntese conta o que se provou; a auditoria pergunta *o que pode estar errado no modo como se provou*.

---

## 1. Seguimos o plano?

O plano formal (`plano-de-testes-motor-inflexoes.md`, 11/07/2026) definia 8 famílias de testes para o motor JSON, com prioridades e um calendário de 6 meses. Confronto família a família:

| Plano | Executado? | Desvio (honesto) |
|---|---|---|
| T1 longitudinal (Routine semanal) | **Em curso** — 2 corridas (11/07, 17/07) | **A automação nunca ligou** (6 tentativas bloqueadas por aprovação). Corre manual. A cadência semanal depende do utilizador pedir — risco real de a série morrer por esquecimento |
| T2 variância (3+ sessões) | Feito — **com 2 mentes, não 3+** | Claude + ChatGPT em vez de 3+ sessões; compensado por serem *modelos* diferentes (mais forte que 3 sessões do mesmo modelo), mas o N do plano não foi cumprido à letra |
| T3 adversarial | Feito, 5/5 | Sem desvio |
| T4 ablação | Feito — **por método diferente** | O plano pedia re-pontuar 4-6 corridas arquivadas; foi feito com 2 "experiências naturais" (Manus; ChatGPT-T2) + contrafactual. Mais engenhoso, mas evidência mais fraca do que o desenho original |
| T5 generalização | Feito | Lado Claude falhou por limite de gastos — o resultado primário veio só do ChatGPT (par assimétrico) |
| T6 degradação | Feito — **acima do plano** | O plano pedia 25→10→5→2; foi feita a curva 10/5/3/2/1 com 5 operadores isolados. Excedeu o desenho |
| T7 integração a jusante | Feito — **só estrutural** | Handoff "no papel", gate a gate; a integração *executada no tempo* ficou delegada ao T1, como o próprio T7 declara |
| T8 invalidadores retroativos | Feito, 14/14 | Sem desvio |

**Acrescentos fora do plano:** T9 (batismo com grelha pré-comprometida), T10 (regime conjeturado), T11 (não-físico), E2E, pares ChatGPT de T10/T11, curva completa do T6. **Estes acrescentos — nenhum previsto no plano original — produziram os resultados mais valiosos do programa** (a convergência-de-estrutura do par T11 é o achado nº1 do projeto). O plano cresceu organicamente a partir dos achados, que é o comportamento certo de um programa de investigação; mas registe-se que o mapa final não é o mapa inicial.

**O desvio estrutural maior (que ninguém decidiu formalmente):** o plano foi escrito para o **motor JSON**; a meio do programa o artefacto central passou a ser o **perfil**. T3, T8 e T1 testam o motor; T2, T4, T5, T6, T9, T10, T11 testaram, na prática, o *perfil*. Consequência honesta: **o motor v1.1 nunca recebeu T2 (variância), T4 (ablação das suas ~15 regras), T5 nem T6** — só fumo + T3 + T8 + duas corridas de T1. Isto é defensável (o motor foi despromovido a artefacto secundário; o seu vocabulário vive dentro do perfil), mas o arquivo por vezes lê-se como se "o framework" fosse uma coisa só e toda testada — não é: são **dois artefactos com coberturas de teste diferentes**, mais o v2 de execução (que só serviu de contraparte no T7).

**Veredito de aderência: ~85%.** As 8 famílias foram todas atacadas; 3 com desvios de método ou de N (T2, T4, T7); 1 com o mecanismo de automação falhado (T1); e o programa expandiu-se para além do plano nas direções certas. O espírito do plano — cada teste ataca uma ameaça nomeada — foi mantido sempre.

---

## 2. O plano definia 4 ameaças metodológicas. Foram mitigadas?

O próprio plano (secção 0) deu à auditoria os seus critérios. Confronto:

1. **Leakage/hindsight** — ✅ **bem mitigado.** O programa privilegiou testes forward (T1, T9-T11 com pesquisa live em data corrente); o T8 (retroativo) foi explicitamente rotulado evidência fraca com protocolo declarado. Sem backtests disfarçados de prova.
2. **Avaliador = executor** — ⚠️ **mitigado só em parte, e é a fraqueza nº1 do projeto.** Mitigações reais: grelha pré-comprometida antes de existir tese (T9, commit `68dca5f7` — genuinamente vinculativa); operadores em instâncias frias sem contexto; pares ChatGPT como mente externa. Mas **todas as avaliações foram escritas por mim**, o mesmo agente que desenhou o perfil. A grelha limita o mover-da-fasquia; não limita a generosidade na aplicação da grelha. Um leitor cético deve descontar os superlativos das avaliações ("o mais fino da série", "nível mais alto") — o padrão de PASS/VÁLIDO em cadeia é consistente com um perfil bom *e também* com um avaliador benevolente. A defesa mais forte que o projeto tem contra isto não são as minhas notas: são os **outputs verbatim arquivados** — qualquer humano pode reavaliar as teses contra a grelha sem confiar em mim.
3. **Survivorship do programa** — ✅ **respeitado.** As falhas estão no arquivo com destaque: o lado Claude do T5 morto por limite de gastos, as 6 tentativas falhadas de automação, a falha de coerência do Manus, a ressalva de pureza do TER, o título "−13,63%" não-contado. Nada foi varrido.
4. **Dependência de regime** — ✅ **atacada diretamente e com o melhor resultado do programa.** T5 (ex-IA), T10 (ex-IA e ex-defesa), T11 (ex-tudo-físico) foram desenhados exatamente para isto, e produziram a conclusão da gravidade real (compromissos custosos, não domínio). *Ressalva residual:* todos os dados continuam a vir do regime macro 2024-26; um bear market prolongado ou um regime sem supersiclos de capex nunca foi observado. A dependência de regime está refutada no eixo *setorial*, não no eixo *temporal*.

---

## 3. As ideias que mudaram o framework para melhor (por ordem de impacto)

1. **A viragem: replicar a mente, não corrigir o pipeline** (`parecer-caminho-framework.md`). Veio da insistência do utilizador, não de mim — e a primeira versão do meu parecer estava assente numa leitura em diagonal da conversa ChatGPT, que o utilizador apanhou ("leste na íntegra ou na diagonal?"). Sem esta correção de rumo, o projeto teria polido um pipeline correto e morto. Tudo o que o programa validou de valioso descende desta decisão.
2. **Forma como engenharia: prosa habitável em vez de schema.** A aposta de que "schemas convidam à obediência, prosa transmite temperamento" era uma hipótese estética; os testes tornaram-na empírica (os operadores produzem teses com *forma própria*, não formulários preenchidos — critério 2 da grelha, verificado 7×).
3. **As duas emendas nascidas do Manus** (auto-check de coerência + facto-charneira primário). São o melhor exemplo do ciclo saudável: falha real observada → regra mínima → validação ao vivo (4 aplicações verificadas: AMSC recusada, CLF recusada, Kraft/KKR/Apollo recusados, VERX assumida como impura). Regras que *mordem*, não decoração.
4. **A regra de governação anti-inchaço** ("a próxima emenda exige uma falha real observada"). É a única defesa estrutural contra o destino de todos os frameworks desta linhagem — morrer por acreção. O T4 mostrou que ainda não inchou; a regra é o que impede que venha a inchar.
5. **Fecho em recomendação por lógica de tese, nunca por score.** Nasceu de uma pergunta do utilizador sobre o output do batismo. Transformou o produto de "mapa interessante" em "decisão utilizável" — e o v1 original tinha provado que o scoring era teatro.
6. **O comutador de 3 posições descoberta→execução** (T7+E2E). Corrigiu exatamente o modo de falha da execução real de 2025 (encontrar os nomes certos e executá-los já, à frente de earnings). "Estacionar com gatilhos" é a peça arquitetural nova mais útil para quem for *usar* isto.
7. **O resultado do T6** (a honestidade aperta com a fome; decisão invariante ao orçamento). Converteu o medo fundador da série (confabulação) numa propriedade medida e contínua.
8. **A grelha pré-comprometida** (T9). Ideia pequena, ganho de integridade desproporcionado — é o que dá às avaliações o pouco de independência que têm.
9. **O achado dos pares** (T10 diverge em domínio, T11 converge em estrutura). Cientificamente, o resultado mais profundo: o perfil transmite estrutura, a mente escolhe o domínio.

**Ideias que NÃO renderam (peso morto honesto):** o **v2 de execução (JSON)** ficou parqueado — o seu único uso em todo o programa foi ser a contraparte do T7; o **motor JSON v1.1** foi ultrapassado pelo perfil três dias depois de nascer (continua útil como executor procedimental do T1, mas as suas 15 regras nunca foram abladas); e parte da **proliferação de artefactos** (~45 ficheiros, com sementes quase-duplicadas e verbatims extensos) é custo de auditabilidade que um dia pedirá arrumação — o índice e a síntese mitigam, não resolvem.

---

## 4. As fraquezas que um comprador desta due-diligence deve conhecer

1. **Zero validação preditiva forward.** É a limitação dominante e nenhum teste a contorna: **tudo o que está validado é processo, disciplina e craft — não acerto.** As teses são avaliadas por qualidade de raciocínio e fidelidade, não por serem verdade (os factos vêm de excertos de pesquisa que não pude confirmar em fonte primária — WebFetch bloqueado durante todo o projeto). O único juiz do acerto é o T1, que tem 2 pontos de dados separados por 6 dias. **Qualquer uso deste framework com capital real, hoje, seria um ato de fé no processo, não uma decisão baseada em outcomes.**
2. **Avaliador = construtor** (§2.2). O padrão de vereditos positivos em cadeia deve ser lido com esse desconto. Recomendação concreta: submeter **uma** tese (sugiro a do T11-ChatGPT ou a do E2E) a um avaliador humano independente com a grelha na mão, sem lhe dizer que veredito eu dei.
3. **A fundação assenta num único caso de sucesso.** As "duas forças" foram engenharia reversa de UMA execução que acertou 4/4 (out/2025). O T8 mitigou retroativamente e os T9-T11 mostraram que o método produz teses novas de qualidade — mas o risco de sobre-ajuste da personalidade a um episódio vencedor não desaparece com testes de craft; só o T1 o dissolve.
4. **N=1 por célula de teste.** Cada patamar do T6, cada par, cada batismo correu uma vez. A direção e a forma dos resultados são consistentes entre testes (o que dá confiança agregada), mas a dispersão dentro de cada teste não está medida.
5. **Paridade imperfeita nos pares ChatGPT.** O lado ChatGPT correu com Deep Research (confirmado no T10) — mais fontes por ferramenta. Foi declarado e descontado, mas a comparação "mente-vs-mente" tem este ruído.
6. **Fragilidade operacional do T1.** Sem automação, a série longitudinal — o único teste que importa no fim — depende de memória humana. Seis falhas de ativação estão documentadas; a especificação está pronta; a ligação a partir de um computador é a correção pendente mais importante do projeto inteiro.

---

## 5. Parecer honesto

**O projeto cumpriu — e superou — aquilo em que se redefiniu, e ainda não provou aquilo que originalmente parecia prometer.** As duas metades desta frase têm o mesmo peso.

**A metade forte.** Partiu-se de uma auditoria a um handoff e chegou-se a um artefacto genuinamente original: um perfil epistemológico habitável que faz mentes diferentes produzirem investigação causal de calibre alto, com uma disciplina de honestidade que sobreviveu a todos os ataques que lhe desenhei — escassez de dados, regimes forçados, domínios proibidos, armadilhas adversariais, um modelo fraco (Manus) a servir de crash-test. O processo de trabalho foi exemplar no que esta linhagem de frameworks historicamente falha: falhas arquivadas com destaque, grelha comprometida antes dos resultados, emendas só com falha observada, podas testadas antes de aplicadas. E as melhores ideias do projeto vieram do diálogo — a viragem, o fecho em recomendação, a exigência de leitura integral — o que diz bem do método de trabalho, não só do resultado.

**A metade que exige humildade.** Este framework **nunca previu nada ainda**. Validámos que o operador *pensa como* o operador de outubro de 2025; não validámos que *acerta como* ele. A cadeia de vereditos positivos foi escrita pelo construtor; os factos das teses não foram confirmados em fonte primária; a fundação é um único episódio vencedor; e o teste que responde à única pergunta final — "as previsões datadas cumprem-se? os falsificadores disparam quando devem?" — tem seis dias de vida. Se alguém me perguntasse "confiavas dinheiro a isto hoje?", a resposta honesta é: **ao processo, sim — é o processo de investigação mais disciplinado que sei construir; ao resultado, ainda não — porque resultado, em sentido próprio, ainda não existe.**

**As três correções que recomendo, por ordem:**
1. **Ligar a automação do T1 a partir de um computador** (spec no arquivo). É a diferença entre este projeto ter um veredito final daqui a 3-6 meses ou desvanecer-se sem ele.
2. **Uma avaliação humana independente de uma tese**, com a grelha, às cegas do meu veredito — o antídoto mais barato para a fraqueza nº2.
3. **Não tocar no perfil até o T1 falar.** A regra de governação já o diz; a tentação de melhorar um artefacto validado é exatamente o vício que o T4 vacinou.

**Última linha, sem rodeios:** construímos e testámos a *mente* — com rigor acima do que o plano pedia. O que não fizemos, porque não se pode fazer por esforço, foi ver essa mente acertar no futuro. O projeto está no ponto exato em que deve estar: completo no que depende de trabalho, pendente no que depende de tempo. O erro agora seria confundir as duas coisas.

*(Nada neste projeto é aconselhamento financeiro; as teses são research/watchlist, e a qualidade do craft não é promessa de retorno.)*
