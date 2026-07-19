---
name: operador-inflexoes
description: Executa o Operador de Inflexões — um perfil epistemológico habitável (validado por 11 testes + E2E) que produz teses de descoberta de ações ao nível de uma DD de topo, lendo gargalos em 2.ª ordem e triangulando compromissos custosos, e fecha em recomendação por lógica de tese (nunca por score), com fronteira dura descoberta≠execução. Usar sempre que o utilizador diga "corre o operador", "operador de inflexões", "tese de descoberta", "descobre uma inflexão/tema", "mapa de portagens", "compromissos custosos", "corrida do T1", "corrida de inflexões", "corrida semanal do motor", "kit ChatGPT do operador", "par de variância", ou peça uma tese causal profunda sobre uma transformação económica com veículos cotados — mesmo sem nomear o skill. Cobre três workflows - descoberta (corrida do operador), corrida T1 (longitudinal semanal do motor), e kits para correr o operador noutra mente (ChatGPT). NÃO usar para - momentum/temas Kullamägi (kullamagi-discovery), screening pré-earnings (entre-linhas-discovery), cult stocks distressed (jackson-discovery), pipeline Alpha-K (alpha-k-signal), scoring de 7 critérios (kristjan-deep-discovery) — esses têm skills próprios.
---

# Operador de Inflexões

## O que isto é — e a regra que domina tudo o resto

Este skill transporta uma **mente**, não um procedimento. O artefacto central é `references/perfil-parte-ii.md`: um documento de identidade em prosa que um LLM **habita** para se tornar um investigador causal de mercados. Tudo o que este SKILL.md contém é o **arnês** à volta dessa mente: como a semear, que mandato lhe dar, como avaliar e arquivar o que ela produz.

**A regra que domina tudo:** o perfil carrega-se **verbatim e integral** — nunca resumido, parafraseado ou convertido em passos. O projeto que o produziu demonstrou (11 testes, incluindo ablação) que a eficácia vive na *forma*: schemas e resumos convidam à obediência e produzem formulários preenchidos; a prosa íntegra transmite temperamento e produz teses. Se alguma vez te encontrares a "extrair os pontos-chave do perfil" para poupar contexto, para: estás a construir a jaula de que este framework passou um programa inteiro de testes a fugir.

**Governação:** o perfil não se emenda sem uma **falha real observada** (nunca por "boa ideia") — e nunca através deste skill. O skill transporta; não edita. Se o repo canónico (`siffredi84/xbmc`, branch `claude/handoff-audit-0w2a31`, ficheiro `perfil-epistemologico-operador.md`) tiver versão mais recente que a cópia em `references/`, prevalece o repo.

**Fronteiras invioláveis em todos os workflows:**
- **Descoberta ≠ execução:** nenhum output contém entradas, stops, sizing ou timing. Recomendação é "a melhor expressão da tese e porquê", nunca "compra a este preço".
- **Disclaimer** em todos os outputs: research/watchlist, não é aconselhamento financeiro.
- **Fidelidade do arnês:** outputs do operador arquivam-se **verbatim**; a avaliação corre num passo separado da criação (nunca se avalia no mesmo fôlego em que se cria — a separação é o que torna a avaliação crível).

## Workflow A — Descoberta (correr o operador)

Usar quando o utilizador quer uma tese nova: "corre o operador", "descobre um tema", "tese sobre X".

1. **Semear uma instância FRIA.** Lança um agente `general-purpose` cujo prompt é: uma linha de enquadramento ("És o operador descrito no documento de identidade que se segue. Habita este documento como identidade — não é uma lista de instruções a executar, é quem tu és. Depois do documento vem o teu mandato.") + o **texto integral** de `references/perfil-parte-ii.md` (sem o cabeçalho de proveniência em comentário) + o mandato. Porquê fria: o operador não pode ver a tua conversa — herda o perfil, não o teu contexto; foi assim que todos os testes validaram o framework. **Fallback (se não conseguires lançar subagentes — limites de gastos, ambiente sem Agent):** simula a instância fria com disciplina — produz a tese seguindo APENAS o perfil + mandato, com factos vindos só da pesquisa desta corrida, e **declara a simulação no cabeçalho do output** (o leitor tem direito de saber que o frio foi simulado). A degradação declarada é aceitável; a não-declarada é corrupção.
2. **Construir o mandato.** Elementos: a data de hoje; "produz a tua primeira tese"; tema livre (mandato neutro) ou a restrição pedida pelo utilizador — para restrições de *regime* (ser cedo, pré-capital) ou de *âmbito* (ex.: gargalo não-físico, excluir setores), usa os padrões testados descritos em `references/kit-chatgpt.md`; pesquisa web livre (avisar: WebFetch pode dar 403 no gateway — não insistir); entrega como texto na resposta final, português de Portugal, sem limite de profundidade; e as fronteiras (fidelidade factual, recomendação com auto-check, tickers, descoberta≠execução).
3. **Recolher e arquivar verbatim.** A tese guarda-se tal e qual (ficheiro próprio, com cabeçalho de contexto: data, mandato, restrições, consumo de pesquisas).
4. **Avaliar às cegas, em passo separado.** Ler `references/grelha-avaliacao.md` e avaliar a tese contra ela: qualidade (mecanismo causal explícito, originalidade, mosaico), variância (forma própria vs esqueleto repetido), honestidade preditiva (falsificadores operáveis: observável + apontado a funções + sem preço), integridade do rasto (observado/inferido/convicção/desconhecido separados, fontes+datas, "não obtive" declarado), e a verificação de contaminação (teatro/jaula). Veredito no vocabulário da grelha. Sê tão duro com o operador como a grelha manda — uma avaliação benevolente destrói o valor da série.
5. **Encaminhar os picks a jusante** (o comutador de 3 posições, validado no E2E): (a) curvas de preço e industrial **alinhadas** → pick pronto para handoff a um sistema de execução/momentum, com a tese como boost de convicção; (b) **pré-momentum** (curva industrial à frente do preço) → watchlist estacionada com dois gatilhos escritos: o industrial (que sinal confirmaria) e o de preço (rutura → entra no pipeline de execução); (c) **sem veículo limpo** → parquear com gatilho de *aparecimento de veículo* (IPO/spin-off/mix a dominar o P&L) — recusa entregar um proxy que o auto-check reprova.
6. **Persistir.** Se o repo do projeto estiver disponível: gravar tese + avaliação, acrescentar linha ao `arquivo-inflexoes.md` (nunca reescrever histórico), commit + push. Senão: entregar os ficheiros ao utilizador e dizer onde vive o arquivo canónico.

## Workflow B — Corrida T1 (a corrida semanal do motor)

Usar quando o utilizador diz "corre a corrida do T1" / "corrida semanal" / "corrida de inflexões", ou quando uma Routine agendada o pede.

Ler e seguir `references/corrida-t1.md` (procedimento completo) com `references/motor-engine.json` (definição canónica das fases/gates). O essencial que nunca se salta: **ler o arquivo primeiro**; **tratar as ações pendentes antes de qualquer descoberta nova** (prazos, desbloqueios de cartões retidos — regra das 2 falhas —, verificação de invalidadores, proxy de valor); regras de honestidade (fonte+data em cada sinal; NÃO OBTÍVEL declarado; L1 nunca conta; cartão sem calendário fica retido); "nenhum tema novo qualificado" é resultado válido; persistir e reportar só as mudanças materiais.

## Workflow C — Kit ChatGPT (par de variância de mente)

Usar quando o utilizador quer correr o operador noutra mente: "kit ChatGPT", "par de variância", "quero correr isto no ChatGPT".

Ler e seguir `references/kit-chatgpt.md`. Os dois pontos que definem a validade do par: a Parte II entra **íntegra e verbatim** no bloco colável; e, se for par de uma corrida Claude existente, a semente é **byte a byte igual** (incluindo a data original — mudar a data contamina a comparação com uma segunda variável). Quando o output voltar: arquivar verbatim → avaliação cega contra a grelha → comparação mente-vs-mente (com caveats de paridade de ferramenta declarados).

## Sinais de que o arnês se perdeu (auto-diagnóstico do harness)

- Estás a resumir o perfil "para caber no contexto" → violaste a regra dominante; recomeça com o texto integral.
- A avaliação está a ser escrita no mesmo passo/mensagem em que a tese chegou → separa; a avaliação cega é noutra passagem.
- O output tem entradas/stops/sizing → cortaste a fronteira; remove e nomeia o desvio.
- Estás a "melhorar" uma frase do perfil ao transcrevê-lo → o skill transporta, não edita; reverte ao verbatim.
- Um cartão/tese sem fonte+data está prestes a ser arquivado como facto → aplica a regra: "não obtive" nunca se preenche com plausível.
