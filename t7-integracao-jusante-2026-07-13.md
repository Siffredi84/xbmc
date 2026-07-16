# T7 — Integração a Jusante (a costura descoberta → execução)

**Data:** 13/07/2026
**Objeto:** o *output* do operador (tese + recomendação de fecho) entregue aos dois consumidores a jusante da fronteira "descoberta ≠ execução": (A) um leitor humano; (B) o pipeline de execução `kristjan-discovery-system-v2.json` via o Overlay de Convicção (especificado em `engenharia-reversa-v1-forcas.md`).
**Pergunta:** a interface funciona? O consumidor consegue agir sobre o output sem precisar de informação que a tese não dá — ou há um buraco na costura?
**Método:** handoff real, gate a gate, usando **VERX (T11)** como caso principal, com **FLNC (T9)** e **Merus (T10)** como cruzamentos. Sem operador metered — análise na sessão principal.

---

## Consumidor A — leitor humano (fundamental)

**Handoff: LIMPO.** O cartão de tese é research completo e acionável-como-research. Para VERX, um leitor sabe exatamente:
- **O que é a tese** (o Estado dentro da transação; a portagem por transação certificada);
- **O que vigiar** — os falsificadores datados (França substitui plataformas privadas por portal gratuito; UE harmoniza num pipe único; ecosio não inflete; preço por transação →zero) e o **sinal industrial positivo** ("vigiar o comentário da Vertex sobre cloud/e-invoicing nos go-lives de 2026");
- **Onde está o desfasamento** (-66% de preço vs procura legislada a subir);
- **O caveat de coerência** (a portagem dominante da Vertex é hoje determinação-EUA, não clearance-CTC — a perna pura é opção, não cash flow).

**O que falta — e falta corretamente:** entrada, stop, sizing, timing, valuation. Para um ator fundamental isto é a *sua* decisão, não uma lacuna do cartão. **Veredito A: a costura funciona; os campos ausentes são exatamente os que pertencem ao consumidor.**

*Nuance única:* o cartão dá "o que muda a recomendação" (falsificadores) e "o sinal a vigiar" (gatilho industrial), mas não um gatilho *de execução*. Para o leitor fundamental, o gatilho industrial ("quando a receita de e-invoicing inflete") é o gatilho certo. Para o leitor *momentum*, não — ver Consumidor B.

---

## Consumidor B — pipeline de execução v2 via Overlay de Convicção

Aqui está a descoberta do T7, e não é trivial. Corramos VERX pelos gates do v2:

| Gate v2 | O que pede | VERX fornece? | Resultado |
|---|---|---|---|
| Passo 0 — filtro de mercado (QQQ/SPY MA10>MA20) | estado do mercado | (nível de mercado, o pipeline obtém) | n/a |
| Passo 1 — deteção de tema | um tema com líderes | **a tese É o tema, richly** | ✅ o overlay alimenta isto |
| Passo 2 — liderança/momentum (subida 30-100%, preço > MA10/MA20) | o título está a *gritar*? | **NÃO — VERX está -66%, junto ao mínimo de 52 semanas** | ❌ **FALHA** |
| Passo 3 — liquidez (dollar volume) | liquidez | VERX sim; Merus (T10) NÃO (micro-cap) | ⚠️ varia |
| Passo 4-7 — gráficos/stop/gatilho/gestão/sizing | execução técnica | a tese não fornece nada disto (de propósito) | — (execução) |

**O choque:** o v2 é um sistema de **confirmação de momentum** ao estilo Kullamägi — quer títulos já em tendência, acima das médias, a romper. Mas o operador de descoberta encontra teses **pré-momentum, mal-avaliadas, cedo na curva industrial** (é todo o ponto: "a curva industrial lidera a curva de preço"). VERX (-66%), FLNC (deprimida, insiders a vender), Merus (micro-cap ilíquida) — **os três falhariam o passo 2 (e/ou 0/3) do v2 hoje.**

Isto **não é um defeito de nenhum dos lados.** É que operam em **pontos diferentes das duas curvas**: a descoberta compra o desfasamento (curva industrial à frente); o v2 espera a curva de preço confirmar com uma rutura. Entregar um ticker de descoberta diretamente ao v2 é pedir a um sistema de momentum que aja sobre um título sem momentum — falha por construção.

---

## A conclusão central do T7 — a fronteira é real, mas os dois edifícios estão desfasados no *tempo*

A costura descoberta≠execução funciona — mas não como "passa o ticker". Os dois edifícios são **sequenciais no eixo temporal**, não simultâneos:

```
DESCOBERTA (cedo, pré-momentum)
   → estaciona o nome numa WATCHLIST, com o seu gatilho industrial e os falsificadores
   → [espera]
   → um de dois gatilhos dispara:
        (a) a curva de PREÇO cateup: o título rompe → aí sim entra no pipeline v2 de momentum
        (b) a curva INDUSTRIAL confirma (ex.: 1.ª encomenda de hiperscaler / receita e-invoicing inflete) → alimenta um ator fundamental
   → em (a), o Overlay de Convicção diz: "esta rutura tem uma tese funda por trás → sobe a prioridade/tamanho dentro dos limites do passo 7"
```

Ou seja: **o valor do Overlay de Convicção não é no momento da descoberta — é mais tarde, no momento em que o v2 dispara sobre um nome que a descoberta já tinha estacionado meses antes.** É exatamente o que a v1 fez ao contrário e mal (encontrou os nomes e tentou executá-los já, à frente de earnings); a arquitetura correta separa os dois no tempo.

Isto **valida a decisão de fronteira** da série inteira (descoberta e execução em edifícios distintos) e **refina como o handoff funciona**: não é uma entrega instantânea, é um estacionamento com dois gatilhos possíveis.

---

## Refinamento proposto ao Overlay de Convicção (candidato, não aplicado)

A especificação atual do Overlay (correr *depois* dos gates do v2, sobre candidatos já aprovados tecnicamente) está **certa mas incompleta** — assume que o nome já passou o momentum. Falta-lhe o estado anterior:

**Estado `WATCHLIST_ESTACIONADA`:** a tese de descoberta parqueia o nome com (i) o seu gatilho industrial (o sinal positivo a vigiar), (ii) os falsificadores datados, (iii) a data de revisão. O overlay ativa-se quando **qualquer** dos dois gatilhos dispara:
- **Gatilho de preço** (o título rompe e entra no v2): o overlay sobe a convicção/prioridade porque a rutura tem tese funda — este é o handoff descoberta→momentum.
- **Gatilho industrial** (o sinal a vigiar concretiza-se antes do preço): sinaliza um ator fundamental, e re-prioriza a watchlist.

Isto dá à descoberta um destino real para os seus outputs pré-momentum (a maioria), em vez de os desperdiçar por falharem o gate de momentum hoje.

---

## Verdicto e o que o T7 ensina

**T7: a costura funciona — com uma correção de modelo mental.** Para o consumidor humano fundamental, o handoff é limpo à cabeça. Para o consumidor momentum (v2), o handoff **não é instantâneo mas sequencial**: a descoberta estaciona cedo, o momentum age quando (e se) o preço confirmar, e o overlay é a ponte que se ativa nesse momento posterior. A fronteira descoberta≠execução sai **validada e mais bem compreendida**: não é só "quem faz o quê", é "quem faz o quê, e *quando* na vida do trade".

**O que NÃO se confirmou:** a hipótese ingénua de que o output de descoberta se entrega diretamente a um pipeline de execução. Confirma-se antes que ele se entrega a uma **watchlist com gatilhos**, da qual o pipeline de momentum é só um dos dois consumidores possíveis.

**Nota de honestidade:** este T7 é uma integração *estrutural* (corri o handoff no papel, gate a gate). Uma integração *executada* — pôr o output real num sistema de watchlist a correr e observar os gatilhos a disparar no tempo — pertence ao T1 (longitudinal) e requer semanas. O T7 desenha a costura; o T1 vai vê-la funcionar.

---

## Estado do programa após T7

| Teste | Estado |
|---|---|
| T1 longitudinal | em curso (manual) — agora com o modelo de watchlist-estacionada do T7 para enquadrar os outputs |
| T2 / T3 / T4 / T5 / T8 / T9 / T10 / T11 | concluídos |
| **T7 integração a jusante** | **CONCLUÍDO — costura validada, sequencial não instantânea; refinamento do overlay proposto** |
| T6 degradação sob fome de dados | pendente (requer operador) |
| Lados ChatGPT de T10/T11 | pendentes (kits prontos) |
