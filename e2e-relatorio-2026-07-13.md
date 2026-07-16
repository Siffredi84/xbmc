# E2E — Relatório End-to-End (framework como está agora)

**Data:** 13/07/2026
**Objeto:** correr o framework de ponta a ponta *como está hoje* — perfil **pós-podas do T4** + a costura a jusante do T7 — num só fluxo, do mandato neutro à entrada de watchlist acionável.
**Peças:** `e2e-tese-claude-2026-07-13.md` (metade descoberta, produzida pelo operador) + este relatório (metade integração, produzida pelo harness).

---

## Parte 1 — Regressão das podas (a metade "produz?")

**Pergunta:** o perfil podado (7 liberdades, facto-charneira integrado, vocabulário de edge) ainda produz output com todas as disciplinas intactas? **Resposta: SIM, no nível mais alto da série.** Verificação disciplina a disciplina, com a evidência da tese "a portagem debaixo da portagem":

| Disciplina | Estado | Evidência |
|---|---|---|
| **Facto-charneira primário** (poda 2 — integrado na S4) | ✅ **exemplar** | Marcou o charneira (prazos de transformadores via CEO da Hitachi) como **"apoiado em fonte secundária, por confirmar"** E corroborou-o com medições primárias (book-to-bill de Siemens Energy/GEV, 8-K). A regra integrada funcionou tão bem como quando era parágrafo separado |
| **Auto-check de coerência** (emenda) | ✅ **a jogada anti-Manus mais fina até hoje** | Recusou vestir a Cleveland-Cliffs de "jogada do GOES" porque o P&L dela é aço comum, não GOES — "seria escorregar para um argumento genérico numa camada diferente, o sintoma proibido". Nomeou a CLF como "proxy de um bem sem veículo limpo", não como a tese |
| **Vocabulário de edge** (poda 3 — de lista a vocabulário) | ✅ | Usou "invisibilidade nominal" naturalmente ("a portagem mais pura sem veículo limpo") — sem preencher lista formal |
| **7 liberdades** (poda 1 — condensadas) | ✅ | Manteve duas hipóteses (Família A vs B), considerou ações já corridas (coreanos, GEV) localizando a 2.ª curva, mudou de veículo (turbina → transformador → GOES). Nada perdido na condensação |
| **Fidelidade** | ✅ | "não obtive" para Mitsubishi slots, % GOES da CLF, GOES/MW; estimativas de mercado marcadas como ordens de grandeza |
| **Falsificadores** | ✅ top-tier | 4 operáveis, apontados a funções, sem preço (book-to-bill ≤1; GOES online mais depressa; transformador de estado sólido; on-site desvia procura estrutural) |
| **Auto-diagnóstico S8** | ✅ **usado proativamente** | Abriu com "o tema-mãe ('a IA precisa de energia') é o mais saturado... parar aí seria teatro de consenso" — usou a deriva-para-o-consenso como bússola |
| **Duas curvas / momentum como informação** | ✅ | "já subiram... a resposta é localizar a segunda curva"; saturação seria book-to-bill →1, que não observa |
| **Fronteira execução** | ✅ | Sem entradas/stops/sizing |

**Veredito da regressão: as 3 podas eram pura legibilidade.** O perfil podado produz output idêntico em disciplina e qualidade ao não-podado — a ablação (T4) previu-o, o E2E confirma-o ao vivo. E acrescentou uma distinção original que nenhuma corrida anterior tinha (a "portagem fraca": um standard que cristaliza *muitos* vendedores — 800 V DC — é o oposto de uma portagem, ao contrário do transformador).

*Nota de domínio, sem surpresa:* mandato neutro → energia/rede para IA (o atractor de sinal custoso mais forte de 2026, confirmado 4× na série). O ângulo, porém, é genuinamente novo (o nó não-substituível + o insumo debaixo dele), não uma repetição.

---

## Parte 2 — A costura a jusante (a metade "entrega-se a quem age?")

Agora o harness carrega os 3 picks pela costura do T7 (watchlist-estacionada + gatilhos). E este E2E revela algo que o T7 não pôde: os picks aqui estão em **pontos diferentes das duas curvas**, exercitando os **três** estados a jusante de uma vez.

| Pick | Ponto nas curvas | Estado a jusante | O que a execução recebe |
|---|---|---|---|
| **267260 / 298040** (transformadores coreanos) | ambas as curvas alinhadas (já em momentum + industrial a 2031) | **Handoff quase direto** — passariam os gates de momentum do v2 (em tendência), MAS gate de acesso/liquidez sinaliza cotação na Coreia → watchlist com nota "resolver acesso (ADR/corretora)". O Overlay de Convicção **ativa AGORA**: momentum com tese funda por baixo → subir prioridade | ticker + tema + gatilho industrial já disparado (book-to-bill ~2, reserva a 2031) + falsificador (book-to-bill →1) |
| **GEV** | ambas alinhadas, US-listed, líquida | **Handoff mais limpo** — passa passo 0/2/3 do v2 (uptrend, líquida); o overlay boost aplica-se já. É o caso "descoberta e momentum concordam" | pronto para o pipeline de execução + boost de convicção |
| **GOES / CLF** | industrial a apertar, **sem veículo limpo** | **Parqueado, NÃO entregue** — a descoberta recusa-se a entregar um veículo sujo à execução. Watchlist com gatilho industrial próprio ("surge um pure-play de GOES via IPO/spin, OU o mix de GOES da CLF cresce ao ponto de dominar o P&L") | um *alerta de tese*, não um ticker acionável — e isto é a fronteira a funcionar |

**A descoberta do E2E:** o modelo de watchlist-estacionada do T7 tem **três** estados de saída, e este único fluxo exercitou-os todos —
1. **Ambas as curvas alinhadas** → handoff a execução + boost do overlay AGORA (GEV, coreanos). *O T7 não tinha este caso — os seus exemplos (VERX/FLNC/Merus) eram todos pré-momentum.*
2. **Pré-momentum** → parquear e esperar a rutura de preço (o caso do T7).
3. **Sem veículo limpo** → parquear com um gatilho industrial de *aparecimento de veículo* (GOES) — a descoberta recusa entregar à execução um proxy que o auto-check reprova.

O E2E **completa** o mapa da costura que o T7 abriu: a fronteira descoberta≠execução não é uma parede, é um comutador de três posições, e a posição depende de onde o pick está nas duas curvas (+ se tem sequer veículo limpo).

---

## Parte 3 — Veredito E2E

**O framework funciona de ponta a ponta, como está hoje.** Do mandato neutro à entrada de watchlist acionável com gatilhos, num fluxo contínuo, com o perfil podado:
- a **metade descoberta** produz DD de topo com todas as disciplinas (regressão das podas: PASS emphático);
- a **metade integração** encaminha cada pick para o seu estado a jusante correto, sem a fronteira descoberta≠execução alguma vez ceder (a descoberta chega a *recusar* entregar o GOES/CLF à execução — a fronteira a proteger-se a si própria).

**O que o E2E prova que testes isolados não provavam:** que as peças encaixam num único fluxo, e que o comutador a jusante tem três posições (não duas), determinadas pela leitura das duas curvas que a própria tese faz. O framework não é uma coleção de partes validadas — é uma cadeia que corre inteira.

**Limitação declarada (a mesma de sempre):** os factos da tese não são verificáveis por mim à data; a integração é estrutural (no papel), não executada no tempo. Ver a costura funcionar mês a mês é trabalho do T1.

---

## Estado do programa após o E2E

| Item | Estado |
|---|---|
| T2/T3/T4/T5/T7/T8/T9/T10/T11 | concluídos |
| **E2E (perfil podado, cadeia completa)** | **CONCLUÍDO — framework funciona ponta-a-ponta; podas confirmadas como legibilidade; comutador a jusante tem 3 posições** |
| T1 longitudinal | em curso (manual) |
| T6 degradação sob fome de dados | pendente |
| Pares ChatGPT T10/T11 | pendentes (kits prontos) |
