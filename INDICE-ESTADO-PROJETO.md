# Índice de Estado do Projeto — do Kristjan Discovery System ao Operador Epistemológico

**Data:** 13/07/2026 · **Branch:** `claude/handoff-audit-0w2a31` · **31 commits, 30 artefactos**
**Uma frase:** o que começou como auditoria a um framework JSON de trading terminou num **perfil epistemológico de operador** — um documento habitável, validado por 8 testes, que faz um LLM produzir teses de descoberta de ações do calibre de um DD de topo, em qualquer domínio, sem confabular.

---

## 0. O arco em cinco atos

1. **Auditoria** — auditar um handoff que auditava um framework de trading (Kullamägi). → v5.
2. **Reconstrução** — reescrever esse framework corrigido (v2 JSON) e fazer o post-mortem de uma execução real.
3. **Descoberta** — engenharia reversa das duas forças que fizeram a v1 acertar; construção de um motor autónomo de discovery.
4. **A viragem** — perceber (com a insistência do utilizador) que o objetivo não era um pipeline mais correto, mas replicar a *mente* do operador. → o Perfil.
5. **Validação** — 8 testes que provam que o perfil funciona, generaliza e não incha.

O documento central hoje é o **`perfil-epistemologico-operador.md`**. Tudo o resto é a sua genealogia e as suas provas.

---

## 1. Os artefactos vivos (usar estes)

| Ficheiro | O que é | Estado |
|---|---|---|
| **`perfil-epistemologico-operador.md`** | **O artefacto central.** Documento habitável que faz um LLM *ser* o operador. Parte I = racional; Parte II = o perfil a colar. | **Vivo, v pós-T4** (3 emendas + 3 podas) |
| `arquivo-inflexoes.md` | Registo longitudinal (fase 6): estados de temas, log do programa de testes, métricas. Atualizado a cada corrida. | Vivo |
| `t9-grelha-avaliacao-pre-commit.md` | A grelha cega contra a qual toda a tese é avaliada. | Vivo (estável) |
| `t2-seed-…` / `t5-seed-…` / `t10-seed-…` / `t11-seed-nao-fisico.md` | Sementes prontas a colar no ChatGPT para correr o operador com diferentes restrições. | Vivos (kits) |
| `plano-de-testes-motor-inflexoes.md` | O programa de 8 famílias de testes. | Vivo (guia) |

## 2. A genealogia (como chegámos aqui — referência, não uso diário)

| Ficheiro | Ato | Papel |
|---|---|---|
| `handoff-auditoria-kristjan-v5.md` | 1 | Meta-auditoria: verificou a v4 contra fontes, corrigiu 2 erros, fechou pontos em aberto |
| `kristjan-discovery-system-v2.json` | 2 | O framework de trading reescrito (pipeline de 8 gates) |
| `post-mortem-discovery-20251020.md` | 2 | Post-mortem da execução real de 20/10/2025 (AMKR/ONTO/ASMPT/FORM +118-176%) |
| `engenharia-reversa-v1-forcas.md` | 3 | As **duas forças** que fizeram o 4/4: leitura de gargalo em 2.ª ordem + triangulação de compromissos custosos |
| `inflection-discovery-engine.json` + `-racional.md` | 3 | O motor autónomo de discovery (v1.1) que industrializou as duas forças |
| `corrida-inflexoes-2026-07-11.md` | 3 | Teste de fumo do motor (silicon photonics / CPO) |
| `parecer-caminho-framework.md` | 4 | **A viragem:** o parecer que reconheceu que o objetivo era a mente, não o pipeline (+ adenda pós-leitura integral da conversa ChatGPT) |

## 3. As provas (os testes e os seus outputs)

Cada teste tem semente/grelha + tese(s) + avaliação. Ver `arquivo-inflexoes.md` para o log canónico.

| Teste | Pergunta | Resultado | Ficheiros |
|---|---|---|---|
| **T9 batismo** | O perfil nasce vivo? (produz DD sem tema nem priming) | **VÁLIDO** — "A portagem sobre a derivada" (dP/dt), acima do padrão | `t9-tese-…`, `t9-avaliacao-…` |
| **T2 variância de mente** | Mentes diferentes, mesma semente → resultados diferentes? | **PASSA** — Claude vs ChatGPT: mesmo método, teses divergentes e complementares, zero picks em comum | `t2-tese-chatgpt`, `t2-avaliacao-comparativa` |
| **T5 generalização ex-IA** | Funciona fora do domínio-casa? | **PASSA** — energéticos de defesa (Chemring); descobriu a gravidade real = capex forçado, não "IA" | `t5-tese-chatgpt`, `t5-avaliacao` |
| **T8 invalidadores retroativos** | Os falsificadores são operáveis ou decorativos? | **PASSA** — 14/14 operáveis, mudos em 2 crashes, 1 disparo certo 2 meses antes | `teste-t8-invalidadores-retroativos` |
| **T3 adversarial** | Os gates resistem a armadilhas desenhadas? | **PASSA 5/5** — quantum/cascata/hidrogénio/drones/6G todas rejeitadas | `teste-t3-adversarial-gates` |
| **T10 regime conjeturado** | Consegue ser cedo/herético sem confabular? | **VÁLIDO (o mais forte para o seu alvo)** — força de rede/estabilidade; fidelidade máxima sob tentação máxima | `t10-tese-claude`, `t10-avaliacao` |
| **T11 domínio não-físico** | O método é geral ou só deteta física? | **VÁLIDO (nível mais alto)** — fiscalidade em tempo real (Vertex); a portagem sobreviveu sem gargalo físico | `t11-tese-claude`, `t11-avaliacao` |
| **T4 ablação de regras** | Que regras fazem trabalho? Inchou? | **CONCLUÍDO** — não inchou; 3 podas aplicadas; princípio de governação estabelecido | `t4-ablacao` |
| **Manus (externo)** | Como se comporta num modelo fraco? | válido c/ ressalva grave (tese-química/pick-metal) → gerou 2 emendas | `analise-manus` |

---

## 4. O que aprendemos (as conclusões que sobrevivem)

1. **O edge do operador v1 eram duas forças, não o scoring:** ler o gargalo uma camada abaixo do consenso, e triangular compromissos custosos de emissores independentes. O scoring era teatro.
2. **A forma mata ou salva o framework, não o conteúdo.** Schemas convidam à obediência; prosa habitável transmite temperamento. Os operadores reconstruídos morreram por forma, não por regras erradas.
3. **Uma única fronteira dura:** liberdade cognitiva quase total; fidelidade absoluta na representação. Os dois tracks (Claude e ChatGPT) convergiram nisto por caminhos opostos — a evidência mais forte da série.
4. **A gravidade de domínio real não é "IA" nem "física" — é a convergência de compromissos custosos.** O perfil é um detetor geral de inflexões por sinal custoso (provado em defesa, rede elétrica, e fiscalidade regulatória).
5. **A sub-ponderação do regime conjeturado era escolha, não incapacidade** (T10): forçado a ele, o perfil executa-o com a fidelidade mais rigorosa da série.
6. **As emendas são redes de segurança** — grátis para modelos fortes, salva-vidas para fracos (T4, via a experiência natural do Manus).

---

## 5. Estado por peça

- **Perfil:** validado como método causal geral; enxuto pós-T4. **Pronto a usar.**
- **Motor JSON (v1.1):** superado pelo perfil como artefacto central, mas continua válido e o seu vocabulário (portagens, compromissos custosos, regimes) vive dentro do perfil. Serve quem quiser a versão procedimental.
- **Framework de trading v2 (JSON):** o ramo "execução" da história — pipeline de gates para *executar* setups, distinto da *descoberta*. Independente e completo.
- **Programa de testes:** 8 de 10+ testes concluídos; ver §6.

## 6. O que fica em aberto

| Item | Natureza | Bloqueio |
|---|---|---|
| **T1 longitudinal forward** | Em curso (manual). O ÚNICO que mede outcomes reais no tempo. Corrida #1 (11/07) arquivada. | Automação (Routine) bloqueada por aprovação; corre-se manualmente ("corre a corrida") |
| **T6 degradação sob fome de dados** | Pendente. Correr o operador com orçamentos de pesquisa decrescentes. | Requer operador metered |
| **T7 integração a jusante** | Pendente. Entregar cartões ao pipeline de execução (v2 via Overlay de Convicção) + a um leitor humano. | Maioritariamente fazível na sessão principal |
| **Lados ChatGPT de T10/T11** | Pendentes. O par de variância de mente no regime conjeturado e no não-físico. | Requer o utilizador correr no ChatGPT (kits prontos) |
| **T2/operador Claude** | Limite de gastos da conta intermitente | claude.ai/settings/usage |

**Verificação factual pendente (transversal):** nenhuma das teses produzidas é verificável por mim à data (13/07/2026) — foram avaliadas por craft, disciplina e fidelidade, não por verdade de base. O T1 é o que, com o tempo, converte isto em outcomes medidos.

---

## 7. Se recomeçares numa sessão limpa — o mínimo a saber

- O artefacto a usar é `perfil-epistemologico-operador.md` (Parte II).
- Para correr o operador: semear uma sessão limpa só com a Parte II + um mandato neutro (ver `t2-seed-…`); avaliar o output contra `t9-grelha-…`; arquivar em `arquivo-inflexoes.md`.
- Regra de governação: **não emendar o perfil sem uma justificação de ablação** (uma falha real observada).
- Todo o rasto está no branch `claude/handoff-audit-0w2a31`, commit a commit, em ordem cronológica.

*Fim do índice. Este documento é o mapa; `arquivo-inflexoes.md` é o diário vivo; o perfil é o produto.*
