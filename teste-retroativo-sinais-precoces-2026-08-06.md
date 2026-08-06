# Teste retroativo — a fila de interconexão teria detetado o tema da energia antes?

**Data:** 06/08/2026
**Objeto:** validar (ou refutar) a hipótese que motivou a abertura das classes de sinal 6 e 7: *"a deteção tardia do motor explica-se pela ausência dos sinais que chegam primeiro"*.
**Método:** teste **retroativo com dados que já contêm histórico** — o ficheiro `LBNL_Ix_Queue_Data_File_thru2025.xlsx` (38.201 pedidos de interconexão à rede elétrica dos EUA, com data de entrada na fila, região, tecnologia e capacidade). Pergunta: *a fila mostrava a inflexão da procura de energia para data centers antes de o motor a detetar?*
**Fonte:** LBNL Energy Markets & Policy, edição 2026 (dados até ao fim de 2025), licença CC BY.

---

## Resultado: **hipótese CONFIRMADA**

### O ponto de viragem

Filtrando por **gás natural** — a energia *firme*, que é o que um data center exige 24/7 (solar e eólica não servem para carga base):

| Semestre | Pedidos | Capacidade |
|---|---|---|
| 2022-S1 | 37 | 20,5 GW |
| 2022-S2 | 56 | 15,6 GW |
| 2023-S1 | 66 | 17,4 GW |
| 2023-S2 | 63 | 20,6 GW |
| **2024-S1** | **131** | **58,0 GW** ← **viragem: 2,8× num semestre** |
| 2024-S2 | 62 | 25,1 GW |
| 2025-S1 | 177 | 76,9 GW |
| 2025-S2 | 146 | 84,2 GW |

Em base anual: **14,2 GW em 2021 → 161,1 GW em 2025** (11×). O gás passou de tecnologia moribunda a maior fonte de procura de ligação nova.

### A comparação com o histórico do projeto

| Momento | Data |
|---|---|
| **A fila vira** | **1.º semestre de 2024** |
| O operador v1 deteta "energia para IA" (Tema 2 da corrida fundadora) | outubro de 2025 |
| O tema é classificado MADURO no arquivo | julho de 2026 |

**Antecedência do sinal sobre a deteção: ~18 meses. Sobre o mainstream: ~24 meses.**

### Ressalva decisiva sobre disponibilidade

O sinal *existir* não é o mesmo que estar *disponível*:

- **Via ficheiro LBNL** (usado neste teste): publicação **anual**. Os dados de 2024 só saíram em ~maio/2025 → antecedência prática de **~5 meses**.
- **Via filas dos ISOs** (PJM, MISO, ERCOT, SPP publicam **mensalmente**): o mesmo sinal estaria visível a meio de 2024 → antecedência de **~15-18 meses**.

**Conclusão operacional:** o LBNL prova que o sinal é real e mensurável; as filas dos ISOs são a versão utilizável. A diferença entre 5 e 18 meses de antecedência está inteiramente no acesso às fontes mensais.

---

## Achado de segunda ordem (não previsto)

A distribuição geográfica da procura de gás contradiz o consenso:

| Região | Δ 2022→2025 |
|---|---|
| **MISO** (Midwest) | **+55,9 GW** |
| SPP (planícies) | +25,4 GW |
| ERCOT (Texas) | +19,4 GW |
| Southeast | +19,1 GW |
| **PJM** (a "data center alley" da Virgínia) | **+10,5 GW** |

**A região historicamente associada aos data centers foi a penúltima.** Explicação provável (inferência, não observação): a fila de PJM está congestionada e com restrições de ligação, empurrando os projetos novos para regiões com capacidade disponível.

Isto é uma leitura de 2.ª ordem do tipo que o perfil procura — *o gargalo deslocou-se geograficamente* — e não aparecia em nenhuma cobertura mediática de 2024. Estava nos dados.

---

## Implicações para o motor

1. **A causa da deteção tardia fica confirmada com números.** O motor não detetou tarde por falha de raciocínio; detetou tarde porque as classes 6 e 7 estavam inacessíveis, e é nelas que vive o sinal precoce.

2. **Recontextualiza a medição da corrida #3.** Medimos que o motor apanhou o CPO a ~4 semanas do mainstream, sem contrafactual. Agora sabe-se que existem sinais utilizáveis com 1-2 anos de antecedência — a métrica de lead time passa a ter uma referência.

3. **Prioridade alterada:** os domínios dos ISOs (`dataminer2.pjm.com`, `oasis.caiso.com`, `www.ercot.com`, `www.interconnection.fyi`, `api.eia.gov`, `www.ferc.gov`) deixaram de ser "acessório" e passaram a ser **a peça que define a antecedência do sistema**.

4. **Métrica candidata para o coletor:** capacidade de **energia firme pedida por região e semestre**, com alerta na derivada (uma duplicação semestral, como a de 2024-S1, é o padrão a detetar).

---

## Limitações declaradas

- **Um único caso.** Um teste retroativo sobre um tema cujo desfecho já conhecemos. Prova que o sinal *estava lá*; não prova que teria sido *reconhecido* em tempo real, nem que funciona noutros temas.
- **Risco de hindsight:** filtrei por gás natural *porque já sei* que a procura de data centers exige energia firme. Em tempo real, essa escolha de filtro não é óbvia — poderia estar a olhar para solar ou baterias.
- **Não testado:** se o mesmo método detetaria temas fora do domínio da energia (a fila de interconexão só cobre eletricidade).
- Estado de acesso à data: LBNL acessível por ficheiro direto (as páginas HTML têm proteção Cloudflare); ISOs ainda bloqueados na política de rede.

---

*Disclaimer: research/watchlist — não é aconselhamento financeiro.*
