# Classe 7 em série mensal — o que 42 retratos do EIA-860M mostram

**Data:** 06/08/2026
**Objeto:** avaliar o que muda quando a classe de sinal 7 (obra física) passa de uma fonte **anual** (fila de interconexão do LBNL) para uma fonte **mensal** com o nome de quem se comprometeu (geradores planeados do EIA-860M).
**Método:** série completa de 42 retratos mensais, 2023-01 a 2026-06, construída de uma vez a partir do arquivo do EIA. Métrica: capacidade de **energia firme planeada** (gás, nuclear, geotérmica, carvão, petróleo) por região, por ano de operação e por entidade.
**Nota:** os números abaixo saem todos de `coletor-sinais/obra/snapshots/` e são reproduzíveis com `python3 coletar_obra.py`.

---

## 1. O achado que interessa: **a antecedência sobe de ~5 para ~9 meses**

A série mensal:

| | firme planeado (GW) | Δ 12 meses |
|---|---|---|
| 2023-01 | 23,9 | |
| 2024-07 (fundo) | **18,2** | +6% |
| 2024-11 | 26,5 | **+48%** |
| **2025-01** | 28,8 | **+53%** ← *um alarme na derivada dispararia aqui* |
| 2025-03 | 41,3 | **+102%** |
| 2026-06 | **73,6** | **+86%** |

Durante todo o ano de 2023 a capacidade firme planeada **encolheu** (23,9 → 18,1 GW). O fundo é em **julho de 2024**. A viragem é visível em setembro/outubro e torna-se inequívoca em **novembro de 2024** (+4,3 GW num único mês).

**A comparação que importa:**

| Momento | Data |
|---|---|
| Derivada a 12 meses cruza +50% | **janeiro de 2025** |
| Derivada cruza +100% | março de 2025 |
| O operador deteta "energia para IA" | **outubro de 2025** |
| O tema é classificado MADURO no arquivo | julho de 2026 |

**Antecedência: ~9 meses sobre a deteção do motor.** O teste retroativo de manhã, feito com o LBNL, tinha estimado ~5 meses de antecedência prática. A fonte mensal quase duplica-a.

## 2. Uma correção ao teste retroativo: **disponibilidade vence precocidade**

Os dois conjuntos de dados datam a viragem em alturas diferentes, e isso não é contradição — é a mesma onda medida em dois pontos do tubo:

| | LBNL (pedidos de ligação) | EIA-860M (geradores planeados) |
|---|---|---|
| Onde está no processo | **entrada** na fila | já com projeto e data de operação |
| Quando o sinal vira | **2024-S1** | 2024-Q4 |
| Frequência de publicação | anual | **mensal** |
| Quando ficou *disponível* | ~maio de 2025 | **~janeiro de 2025** |

O sinal do LBNL acontece **dois a três trimestres mais cedo** e chega às mãos **quatro meses mais tarde**. Para um sistema de deteção, só conta a segunda coluna.

**A lição generaliza para além da energia:** ao escolher fontes para as classes de sinal precoce, a pergunta não é *"que sinal acontece primeiro?"* mas *"que sinal está publicado primeiro?"*. Uma fonte pior publicada depressa bate uma fonte melhor publicada devagar. Isto muda o critério de seleção de fontes em todo o framework.

## 3. O que a fonte nova tem e a antiga não tinha: **nomes**

O LBNL dá regiões. O EIA-860M dá a entidade que assinou. Isso converte a classe 7 de "termómetro macro" em **gerador de watchlist** — que era exatamente a peça em falta.

**Top de capacidade firme planeada (junho/2026):**

| Entidade | GW | unidades | 1.ª aparição |
|---|---|---|---|
| **Fermi America** | 11,68 | 157 | **2026-03** |
| Entergy Louisiana LLC | 9,48 | 24 | 2024-05 |
| **Fermi Nuclear** | 4,47 | 4 | **2026-03** |
| Homer City Generation, L.P. | 4,40 | 14 | 2025-03 |
| Tennessee Valley Authority | 3,89 | 28 | — |
| Entergy Texas Inc. | 2,53 | 5 | — |

**O salto de março de 2026** (49,1 → 70,9 GW num mês, 331 → 540 unidades) tem uma causa quase única: **Fermi America (+11,68 GW) e Fermi Nuclear (+4,47 GW) entraram no mesmo mês**, somando 16,2 dos 21,8 GW acrescentados. Um único ator passou a ser o maior detentor de capacidade firme planeada dos EUA sem transição — apareceu já no topo.

Isto é um *pointer* de primeira ordem, do tipo que só uma fonte nominativa produz. **Não é uma tese** e não foi investigado aqui: o que a fase de descoberta faria com ele — se há veículo cotado, se a curva industrial confirma, se a tese sobrevive ao mapa de portagens — fica para uma corrida, com as regras da corrida.

## 4. A difusão, medida em betão

O coletor de vocabulário (classe 6) mede quantas **empresas distintas** pedem a mesma competência, com a zona de inflexão em 3-8. O mesmo teste aplicado a capital comprometido:

| | entidades distintas com firme planeado |
|---|---|
| 2023-01 | 56 |
| 2024-01 | 56 |
| 2025-01 | 72 |
| 2026-06 | **94** |

Estagnado durante 2023, **+68% desde então**. Não é uma empresa a construir muito: é o número de atores independentes a crescer — a assinatura de uma indústria a formar-se, não de um projeto grande.

## 5. O falsificador não disparou

A folha *Canceled or Postponed* é o teste simétrico: se a procura fosse anúncio sem substância, a capacidade sairia dos planos ao mesmo ritmo a que entra. O registo é cumulativo, por isso o sinal é a derivada:

| | cancelado/adiado acrescentado em 12 meses |
|---|---|
| 2024-01 | +3,1 GW |
| 2025-01 | +1,6 GW |
| 2026-01 | +2,6 GW |
| planeado acrescentado, 12 meses até 2026-06 | **+34,0 GW** |

**Cerca de 13 GW planeados por cada 1 GW cancelado**, com o ritmo de cancelamento estável desde 2023. O falsificador está ativo e silencioso — que é a única forma de um falsificador valer alguma coisa.

## 6. O achado de segunda ordem confirma-se — noutro conjunto de dados

O teste de manhã encontrou, no LBNL, que a "data center alley" da Virgínia (PJM) era das regiões que **menos** procura de energia firme acrescentava. O EIA-860M, que é um conjunto de dados independente e mede outra coisa, diz o mesmo com mais força:

| Região | 2025-06 | 2026-06 | Δ |
|---|---|---|---|
| **ERCOT** (Texas) | 6,6 | **21,9** | **+15,3** (duplicou) |
| **MISO** (Midwest) | 8,2 | **20,3** | **+12,1** (duplicou) |
| SPP (planícies) | 6,4 | 10,3 | +3,9 |
| **PJM** (Virgínia) | 6,1 | 6,2 | **+0,1** |

Por estado: **Texas 25,2 GW**, Louisiana 9,5, Pensilvânia 4,4. A leitura de 2.ª ordem — *o gargalo deslocou-se geograficamente porque a fila de PJM está congestionada* — passa de inferência sobre um conjunto de dados a observação repetida em dois. Continua a ser inferência quanto à **causa**; o **facto** está agora duplamente medido.

---

## Limitações declaradas

- **Cobertura:** só geração elétrica nos EUA. Um tema que não consuma energia em grande escala, ou que a consuma fora dos EUA, é invisível aqui. A classe 7 não é um detetor geral — é um detetor de transformações intensivas em energia.
- **O alarme é retroativo.** A afirmação "um alarme em janeiro de 2025 teria disparado" é verdadeira sobre os dados, mas o limiar (+50% a 12 meses) foi escolhido **depois** de ver a série. A partir de agora está fixado no coletor e passa a ser testável para a frente; até ao primeiro disparo genuíno, o número de 9 meses é uma medição retroativa, não uma previsão validada.
- **Concentração:** o salto de 2026-03 depende de duas entidades relacionadas. Se esses projetos forem cancelados, uma parte grande do sinal recente desaparece — o que é precisamente o que a folha de cancelamentos passa a vigiar.
- **Não testado noutro domínio.** Continua por demonstrar que a classe 7 deteta seja o que for fora de temas intensivos em energia.
- **O que isto não é:** nenhum nome desta análise foi investigado como tese, nenhum tem veículo verificado, nenhum passou pelo mapa de portagens. São pointers para a fase de descoberta.

---

*Disclaimer: research/watchlist — não é aconselhamento financeiro. Sem entradas, stops, sizing ou timing.*
