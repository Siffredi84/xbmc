# Teste: documento de critérios vs. ferramenta construída

**Data:** 29 de julho de 2026 · corrida de referência: sessão de 28-07, 20 aprovados + 1 reprovado

Cada critério do documento foi confrontado com o que o código faz de facto, e onde havia dúvida corri o cálculo em vez de assumir.

---

## 1. Filtros quantitativos obrigatórios — **4/4 conformes**

| Critério | Estado | Nota |
|---|---|---|
| Preço $1,00–$7,00 | ✅ | `config.PRECO_MIN/MAX` |
| Market cap $50M–$500M | ✅ | Finnhub `marketCapitalization` |
| Volume médio > 100k | ✅ | mas ver desvio abaixo |
| NYSE/NASDAQ/AMEX | ✅ | `type == CS` + exchanges US |

**Desvio registado e aprovado:** o documento diz "Volume Médio (30d)". A ferramenta usa **63 sessões**, por decisão tua de 29-07, para manter comparabilidade com o Finviz e resistir à contaminação do próprio pico. O documento deve ser actualizado — não o código.

**Melhoria não prevista:** o filtro `type == CS` exclui automaticamente ETFs, fundos fechados, warrants e units de SPAC. O documento não pedia isto e foi por isso que EAD e TSI entraram nos primeiros finalistas do dia.

## 2. Filtros técnicos — **4/4 conformes**

RSI(14) 25–60, preço vs MA20 > −15%, volume relativo > 1,2×, e ≤ −10% do máximo de 52 semanas. Todos implementados e parametrizados no `config.py`.

## 3. Indicadores de momentum — **parcialmente, e a regra central não é aplicada**

O documento exige **pelo menos um** de três sinais. A ferramenta **não impõe essa condição** — passa candidatos que não têm nenhum.

| Sinal | Estado |
|---|---|
| **A — volume spike** | ✅ `RelVol`, `TendVol`, `Eco` (mais fino que o documento) |
| **B — reversão técnica** | ❌ não implementado |
| **C — accumulation** | ⚠️ parcial: o `Eco` distingue continuação de evento, mas não detecta consolidação lateral, higher lows nem coiling |

Corri o sinal B e as componentes do C sobre os 21 finalistas:

- **RSI a sair de oversold (<30 → >35):** SIGA, SNDL, BYRN, CIA — 4 nomes.
- **Coiling (vol 20d < 80% da vol 40d anterior):** CMRC, AQST, SUPX, PACB, AVIR, MBI, XPOF — 7 nomes.
- **Higher lows:** PACB, AVIR, PMVP, CRDL, ANIX — 5 nomes.

São ~35 linhas de código sobre dados que já estão em memória. Zero chamadas adicionais. É a lacuna mais barata de fechar de todas.

## 4. Filtros sectoriais — **não implementados**

O documento pede priorização por Tier 1 e Tier 2. A ferramenta guarda `Industria` (Finnhub) e **nunca a usa**.

Mapeando os 21 finalistas: **16 em Tier 1**, 2 em Tier 2, 3 fora (SUPX serviços ao consumidor, SND energia, XPOF lazer).

Achado incómodo: a concentração em Tier 1 é ilusória. Dos 16, **onze são biotech/pharma**. Não é o funil a preferir tecnologia — é a estrutura do universo: micro-caps a $1-7 com volume anormal são desproporcionalmente biotech. Sem filtro sectorial explícito, o funil tem um enviesamento que ninguém escolheu. Clean energy e space tech, dois dos quatro Tier 1 do documento, não aparecem de todo.

## 5. Red flags — **4/6 conformes, 1 aproximado, 1 em falta**

| Red flag | Estado |
|---|---|
| Aviso de delisting | ✅ item 3.01 do 8-K — código exacto, sem falsos positivos |
| Going concern no último 10-Q | ✅ três estados; apanhou o ABOS |
| Reverse split | ⚠️ item 5.03 (alteração de estatutos) é proxy, não confirmação |
| Volume < 50k | ✅ gate é 100k, mais exigente |
| OTC / pink sheets | ✅ `type == CS` + exchanges US |
| **Queda > 80% em 12 meses sem recuperação** | ❌ **não implementado** |

Testei o último: **TLRY (−82,6%), SUPX (−91,4%) e BYRN (−87,0%)** face ao máximo de 52 semanas estão os três aprovados. Pelo documento, os três deviam ser excluídos.

Isto merece discussão em vez de implementação automática. O BYRN é o candidato com mais sinais de acumulação da lista — insiders compradores, zero diluição, volume a acelerar. O critério "queda >80%" existe para apanhar empresas em espiral; o "sem recuperação" é a parte que qualifica, e não está definido de forma computável. **Recomendo transformá-lo em bandeira, não em exclusão** — na mesma lógica do `Vol20d`.

## 6. Descoberta precoce — **2/5**

| Sinal | Estado |
|---|---|
| Insider buying 30d | ✅ Finnhub, com ressalva sobre exercícios de opções |
| Próximo de breakout (resistência 2-3×) | ✅ com contagem de toques |
| Partnerships sem hype | ⚠️ indirecto: 8-K item 1.01 |
| Menções Reddit < 100/semana | ❌ sem fonte |
| Nova cobertura de analistas | ❌ sem fonte no plano actual (verificado) |

## 7. Selecção final e ordenação — **não implementado**

O documento pede 5-10 candidatos, com ≥2 sinais de actividade, em sectores prioritários, ordenados por quatro níveis de prioridade. A ferramenta entrega **20 candidatos sem ordenação**.

Esta é a lacuna com maior impacto prático: o documento pedia uma decisão e a ferramenta devolve uma lista.

---

## O que a ferramenta faz que o documento nunca pediu

Estes vieram dos erros do dia, não do desenho inicial, e não devem ser perdidos numa reconciliação:

- **Gate de identidade tri-fonte** — nasceu do bug do parser Finviz
- **Quarentena de séries** — nasceu do NVA a desaparecer em silêncio
- **Regime de reporte 10-Q vs 20-F** — nasceu da decisão cotação vs domicílio
- **Encaminhamento evento vs continuação** — trabalho de verificação distinto por grupo
- **Gate macro FRED** — regime antes de candidatos
- **Tripwire com guarda temporal** — duas fontes independentes a discordar
- **Princípio transversal:** dados em falta produzem etiqueta, nunca decisão

---

## Veredicto

**Conformidade: 19 de 27 critérios verificáveis.** Onde diverge, na maioria dos casos a ferramenta é mais exigente ou mais informada que o documento.

Três lacunas por ordem de custo-benefício:

1. **Sinais B e C** — ~35 linhas, zero chamadas, dados já em memória. E a regra "pelo menos um sinal" passa a poder ser aplicada.
2. **Selecção final e ordenação** — converte lista em decisão. Precisa das tuas quatro prioridades traduzidas em regras.
3. **Filtro sectorial** — decidir se prioriza ou apenas etiqueta, sabendo que hoje o funil tem um enviesamento biotech não escolhido.

E uma decisão pendente: o que fazer com a queda >80%, que hoje aprovaria TLRY, SUPX e BYRN contra a letra do documento.
