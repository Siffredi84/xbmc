# Corrida do Motor de Inflexões — 07/08/2026
## T1 longitudinal — ponto de dados #5

**Comando executado:** `INICIAR MOTOR DE INFLEXÕES — CORRIDA COMPLETA`  
**Data de referência / cutoff factual:** 07/08/2026  
**Corrida T1 anterior:** 05/08/2026 — ponto #4  
**Sessão de mercado usada:** EUA — fecho regular completo de 07/08/2026  
**Modo:** manual, pesquisa live com cutoff histórico + dados Interactive Brokers  
**Infraestrutura:** o branch canónico `claude/handoff-audit-0w2a31` foi encontrado apagado no início da corrida e restaurado exatamente no último commit canónico conhecido `c449812d618d445ec20dcdc04602be780638cf24`, antes de qualquer nova escrita.

> **Disclaimer:** investigação e watchlist. Não é aconselhamento financeiro. Não contém níveis de entrada, stops, sizing ou timing de execução.

---

## Cabeçalho de honestidade

1. As classes 6 — talento — e 7 — infraestrutura física local — não foram pesquisadas sistematicamente; permanecem **NÃO OBTÍVEL** sem fontes dedicadas.
2. Esta é uma corrida histórica: nenhuma evidência publicada depois de 07/08/2026 é usada como sinal da corrida. Páginas atuais foram usadas apenas quando a cronologia nelas exposta permite verificar que o facto relevante já existia, ou não existia, até ao cutoff.
3. Nenhuma data futura de earnings foi estimada. Ausência de calendário é tratada segundo a regra canónica de `RETIDO`; a segunda falha de desbloqueio implica `MORTO`.
4. O IBKR não devolveu histórico diário da Ibiden/TSEJ por falta de permissão de market data nesta sessão. O preço de 07/08 fica **NÃO OBTÍVEL** no proxy; não foi substituído silenciosamente por outra fonte.
5. SCWO tinha a próxima ação de desbloqueio marcada como **revisão mensal**. Como essa revisão ainda não venceu em 07/08, a ausência de calendário/liquidez não é contada como segunda falha nesta corrida.
6. Preço não substitui invalidadores industriais, classes convergentes, materialidade económica ou calendário.

---

# PARTE A — Ações pendentes tratadas primeiro

## A.1 — Segunda tentativa de calendário: OII, FTI, FORM, TER e Ibiden

A corrida de 05/08 deixou os cinco cartões em `RETIDO — tentativa 1/2`, exclusivamente porque o evento trimestral já tinha ocorrido e a empresa ainda não publicara a data do trimestre seguinte.

### Verificação em 07/08

| Ticker | Evidência oficial disponível até ao cutoff | Resultado da ação | Estado |
|---|---|---|---|
| **OII** | O IR continuava sem anúncio de resultados do Q3; o último anúncio de agendamento era o Q2 e o release Q2 não fixava data do Q3 | 2.ª falha | **MORTO** |
| **FTI** | A página de Upcoming Events continuava a mostrar apenas o evento Q2 de 30/07; não havia anúncio Q3 | 2.ª falha | **MORTO** |
| **FORM** | O IR continuava a mostrar como último evento financeiro o Q2 de 29/07; não havia anúncio Q3 | 2.ª falha | **MORTO** |
| **TER** | O calendário/press releases continuavam sem anúncio de resultados Q3 após a call de 29/07 | 2.ª falha | **MORTO** |
| **Ibiden** | O calendário FY2026 listava apenas 04/08 como anúncio Q1; a data Q2 ainda não estava publicada | 2.ª falha | **MORTO** |

### Estado industrial

Não foi encontrado entre 05/08 e 07/08 qualquer novo evento oficial que acionasse os invalidadores industriais pré-registados destes cartões. As mortes acima são, portanto, **procedimentais por calendário**, não mortes da tese económica.

- **OII:** mantém como última evidência material Q2 a utilização ROV de 66%, receita SSR de US$232M e crescimento agregado de SSR+OPG+IMDS; awards trimestrais SSR continuam NÃO OBTÍVEL.
- **FTI:** mantém como última evidência material backlog Subsea de US$15,833B, book-to-bill 1,0x e margem EBITDA Subsea de 23,2%.
- **FORM:** nenhum sinal novo demonstrou insourcing, esvaziamento de parceria, ausência de CPO/SiPh ou adiamento da rampa para 2028+.
- **TER:** nenhum sinal novo demonstrou falha Quantifi/ficonTEC; Robotics continua sem dominar economicamente o grupo na última leitura disponível.
- **Ibiden:** não surgiu evidência nova que demonstre utilização <80%, devolução de pré-pagamentos ou equilíbrio antecipado do défice de substratos.

**Consequência:** CPO, flexible pipe e integridade subsea continuam como temas vivos, mas deixam de ter FORM/TER, FTI/OII como cartões entregáveis por aplicação literal do motor.

---

## A.2 — NOV: segunda tentativa de materialidade económica

### Pergunta de desbloqueio imutável

Consegue-se demonstrar, através de disclosure público, que `flexible pipe` representa mais de 20% da receita do grupo ou mais de 20% do crescimento?

### Evidência

A NOV continua a divulgar a expansão de Açu, o investimento de aproximadamente US$200M, utilização elevada e backlog de flexible pipe até 2028, além de contratos de risers/flowlines. Contudo, a informação pública disponível até 07/08 não isola receita nem crescimento do negócio de flexible pipe de forma suficiente para executar o teste >20% exigido pela Fase 5.

Não se estima a contribuição.

**Resultado:** segunda tentativa falhada.  
**Estado:** `RETIDO → MORTO`.

A morte é por **materialidade não verificável**, não porque a portagem industrial tenha sido invalidada.

---

## A.3 — SCWO: ação mensal ainda não vencida

SCWO permanece `RETIDO — tentativa 1/2`.

A revisão mensal não é antecipada apenas porque foi executado um T1 adicional dois dias depois.

### Observação IBKR, sem contar como nova tentativa

Usando as 20 sessões terminadas em 07/08 e `fecho × volume` como proxy de dollar volume diário, a média foi de aproximadamente **US$88,4 mil/dia**, contra o gate de US$5M. A distância permanece superior a 50×.

- Fecho 04/08: US$2,21
- Fecho 07/08: US$2,15
- Variação: **−2,71%**

Não foi encontrada data oficial futura de earnings até ao cutoff. Como a ação está calendarizada para revisão mensal, **não se incrementa o contador de falhas**.

---

## A.4 — FEIM e timing/sincronização espacial

FEIM já estava `MORTO` desde 05/08 por segunda falha do calendário e continua morto.

A tese industrial não é rebaixada: os contratos de US$18M e US$8M identificados na corrida anterior permanecem sinais reforçadores, mas pertencem à mesma classe de emissor e não criam um novo cartão.

**Tema:** `QUALIFICADO, sem cartão entregável`.

---

## A.5 — Tese “O funil a meio do ciclo” / LEU

### Correção factual do arquivo

A revisão encontrou um problema cronológico na definição original dos gatilhos:

- em **01/07/2026**, a Centrus anunciou a assinatura do contrato DOE de **US$900M** para expansão de enriquecimento HALEU;
- o acordo material foi arquivado na SEC em 02/07;
- a tese `O funil a meio do ciclo` foi criada apenas em **19/07/2026**.

Logo, o gatilho arquivado “novo task order DOE” **já tinha ocorrido antes da criação da tese**. Não pode ser contado como validação forward posterior.

Isto não é reescrito retroativamente como sucesso. Fica registado como erro de cronologia do gatilho original.

Também não foi demonstrado que este contrato HALEU, por si só, satisfaça a condição distinta de financiamento necessária para converter os aproximadamente US$2,4B de compromissos LEU contingentes em produção comercial firme.

### Gatilho de preço — agora calculável

O histórico diário IBKR permitiu calcular diretamente a MA200 em 07/08:

- fecho LEU 07/08: **US$191,37**;
- MA200 calculada sobre os 200 fechos anteriores/incluindo 07/08: aproximadamente **US$223,70**.

O preço estava cerca de 14,5% abaixo da MA200.

**Conclusão:** o gatilho de preço “rutura confirmada acima da MA200” **não disparou**.

**Estado:** `WATCHLIST_ESTACIONADA`.

---

## A.6 — Prazos que ainda não venceram em 07/08

- Média tensão: re-teste em **11/08** — não antecipado.
- Energetics / arm-and-fire: re-teste em **18/08** — não antecipado.
- Subsea/PFAS: re-teste de invisibilidade entre **29/08 e 12/09**.
- Radioisótopos/cGMP: novo re-teste em **02/09**.
- CPO: reavaliação obrigatória do gradiente até **05/09**.
- SCWO: segunda ação de desbloqueio apenas na revisão mensal.

---

## A.7 — Proxy IBKR, ponto #5

Variações contra o último ponto disponível da corrida de 05/08.

| Instrumento | Referência anterior | Fecho 07/08 | Variação |
|---|---:|---:|---:|
| OII | US$50,43 — 04/08 | **US$47,97** | **−4,88%** |
| FTI | US$70,02 — 04/08 | **US$69,62** | **−0,57%** |
| NOV | US$19,99 — 04/08 | **US$19,65** | **−1,70%** |
| SCWO | US$2,21 — 04/08 | **US$2,15** | **−2,71%** |
| FORM | US$120,30 — 04/08 | **US$117,39** | **−2,42%** |
| TER | US$403,56 — 04/08 | **US$379,31** | **−6,01%** |
| SOXX | US$542,21 — 04/08 | **US$543,27** | **+0,20%** |
| Ibiden | ¥20.750 — 05/08 | **NÃO OBTÍVEL IBKR** | **NÃO OBTÍVEL** |
| FEIM | US$70,34 — 04/08 | **US$74,43** | **+5,81%** |
| LEU | US$189,24 — 04/08 | **US$191,37** | **+1,13%** |

O proxy é observacional. Nenhuma destas variações altera um estado por si só.

---

# PARTE B — Descoberta nova: fases 0–5

## B.1 — Fase 0

Critério mantido: procurar uma mudança de regime na taxa de compromissos custosos de capital numa subcamada específica **antes** de a subcamada ganhar cobertura financeira generalista.

---

## B.2 — Fase 1: cinco motores

| Motor | Hipótese em bruto | Leitura |
|---|---|---|
| Gargalo | `A camada de transmissões/propulsão mission-critical de veículos e navios militares vai receber capex forçado porque a procura europeia de plataformas acelera mais depressa que a capacidade qualificada.` | RENK mostra bookings/backlog muito fortes, mas a própria aceleração já é coberta pela Reuters; edge fraco/morto |
| Segunda derivada | `A camada de equipamento de geração e compressão para power/LNG/data centers vai receber capex forçado porque bookings crescem muito acima da receita.` | Baker Hughes IET: orders US$7,1B e b2b 2,2x; industrialmente forte, mas família power/data-center já madura |
| Standards | `A camada de ferramentas de implementação de SPC/TSN industrial vai receber gasto obrigatório porque standards harmonizados estão a fechar.` | Standards reais; não foram encontrados contratos/encomendas L3+ de três classes independentes |
| Política financiada | `A camada de refinação doméstica de minerais críticos vai receber capex forçado porque awards federais estão a converter política em capacidade física.` | ReElement recebeu US$25M; apenas uma classe nova e sobreposição com NdFeB já maduro |
| Segunda linha | `A infraestrutura térmica/elétrica de data centers vai cobrar por MW incremental porque a densidade do compute força expansão de capacidade.` | Vertiv e Baker Hughes confirmam procura; a subcamada já tem cobertura financeira ampla e não é invisível |

Nenhuma hipótese é promovida por obrigação de produzir novidade.

---

## B.3 — Fase 2: mapas abreviados das hipóteses sobreviventes

### Propulsão/transmissões de defesa

`orçamento público → OEM/plataforma → transmissão/propulsão certificada → integração → manutenção`

A transmissão mission-critical é uma portagem funcional e a RENK cobra por plataforma. Contudo, a descoberta não mostrou três classes independentes novas nesta corrida e o tema já aparece em imprensa financeira generalista.

### Power/gas equipment

`necessidade de MW → turbine/compression equipment → integração → grid/site → commissioning → serviço`

Baker Hughes e outros fornecedores têm exposição direta, mas esta família já está arquivada como equipamento elétrico/power maduro. A força dos bookings é confirmação industrial, não novo edge.

### Refinação crítica

`feedstock → separação/refinação → metal/ligas → magneto → qualificação`

A refinação pode ser portagem. O award ReElement é um L3/L5 financiado conforme a natureza da despesa, mas representa uma única classe de emissor nesta nova observação; não reabre o tema NdFeB já classificado `MADURO`.

### Implementação de standards

`standard → ferramentas/software/metrologia → qualificação do processo → auditoria → produção`

Não foi demonstrada uma portagem cotada com três classes L3+ e materialidade económica >20%.

---

## B.4 — Fase 3: triangulação

| Hipótese | Classes independentes L3+ demonstradas nesta corrida | Rajada | Veredito |
|---|---:|---:|---|
| Propulsão/transmissões de defesa | <3 nesta corrida | Sim, atividade recente | **NÃO QUALIFICADO como nova inflexão** |
| Power/gas equipment para energia/data center | Tema já possui densidade industrial, mas não é novo | Sim | **MADURO quanto ao edge** |
| Refinação doméstica crítica | 1 nova classe claramente identificada | Sim | **EMBRIÃO dentro de tema maduro** |
| Implementação SPC/TSN | 0 classes L3+ suficientes | Não demonstrada | **EMBRIÃO** |

Nenhum tema novo passa o gate central.

---

## B.5 — Fase 4: invisibilidade

Não se abre teste completo para embriões.

A hipótese mais forte industrialmente nesta janela — propulsão/transmissões de defesa — recebeu cobertura Reuters em **06/08/2026** sobre recorde de encomendas da RENK, backlog e book-to-bill. Isso é nível 3 explícito e mata a condição de invisibilidade para a narrativa de rearmamento/propulsão enquanto nova discovery.

Power/data-center infrastructure permanece igualmente mainstream.

---

## B.6 — Fase 5

**Nenhum cartão novo.**

---

# PARTE C — Estados após a corrida

## Temas

| Tema | Estado em 07/08/2026 |
|---|---|
| Industrialização CPO | **QUALIFICADO — TRANSICAO_2_PARA_3**, agora sem cartão entregável |
| Tubo flexível submarino | **QUALIFICADO — TRANSICAO_2_PARA_3**, sem cartão entregável |
| Integridade/intervenção subsea | **QUALIFICADO — nível 1–2**, sem cartão entregável |
| Destruição permanente de PFAS | **QUALIFICADO COM RESERVA — TRANSICAO_2_PARA_3**; SCWO ainda retido |
| Timing/sincronização espacial | **QUALIFICADO, sem cartão entregável** |
| SRM/energéticos | **QUALIFICADO, sem cartão entregável** |
| Radioisótopos/cGMP | **EMBRIÃO** — re-teste 02/09 |
| Média tensão | **EMBRIÃO** — re-teste 11/08 |
| Arm-and-fire | **EMBRIÃO** — re-teste 18/08 |
| Equipamento elétrico/power pesado | **MADURO** |
| NdFeB/DFARS | **MADURO** |
| Funil nuclear | **WATCHLIST_ESTACIONADA** — trigger DOE original corrigido como pré-existente; MA200 não disparou |

## Cartões

| Ticker | Estado em 05/08 | Estado em 07/08 | Motivo |
|---|---|---|---|
| OII | RETIDO 1/2 | **MORTO** | 2.ª falha calendário |
| FTI | RETIDO 1/2 | **MORTO** | 2.ª falha calendário |
| FORM | RETIDO 1/2 | **MORTO** | 2.ª falha calendário |
| TER | RETIDO 1/2 | **MORTO** | 2.ª falha calendário |
| Ibiden | RETIDO 1/2 | **MORTO** | 2.ª falha calendário |
| NOV | RETIDO, 1.ª falha materialidade | **MORTO** | 2.ª falha em provar >20% receita/crescimento de flexible pipe |
| SCWO | RETIDO 1/2 | **RETIDO 1/2** | revisão mensal ainda não vencida |
| FEIM | MORTO | **MORTO** | inalterado |

**Watchlist ativa:** zero cartões.

---

# Calendário de ações futuras

| Data/janela | Ação |
|---|---|
| 11/08/2026 | Re-teste média tensão |
| 18/08/2026 | Re-teste arm-and-fire |
| próxima revisão mensal | 2.ª ação de desbloqueio SCWO: calendário oficial + dollar volume 20d >US$5M |
| 29/08–12/09/2026 | Re-teste de invisibilidade subsea/PFAS |
| 02/09/2026 | Re-teste radioisótopos/cGMP |
| até 05/09/2026 | Reavaliação obrigatória do gradiente CPO |
| cada T1 | LEU: confirmar financiamento que converta compromissos LEU contingentes e calcular MA200 |

---

# Nota de governação — falha operacional agora reproduzida

A corrida de 07/08 transforma o defeito de calendário observado em 05/08 numa falha **repetível e causalmente identificável**.

### Falha observada

Cinco cartões — OII, FTI, FORM, TER e Ibiden — mantêm a última evidência industrial sem invalidador acionado, mas morrem porque foram executadas duas revisões de calendário com apenas dois dias de intervalo e as empresas ainda não anunciaram a data do trimestre seguinte.

### Ligação causal

A regra “duas revisões falhadas → morto” mede o **número de corridas**, não o tempo económico necessário para o campo poder mudar. Logo, a frequência manual do T1 altera o destino do cartão mesmo quando a realidade industrial é idêntica.

### Menor alteração candidata — NÃO aplicada

O contador de falhas de um campo de calendário deveria distinguir uma nova oportunidade real de obtenção da mera repetição da mesma ausência pós-evento — por exemplo, usando uma janela de manutenção pós-earnings ou um requisito temporal mínimo entre tentativas.

Nenhuma regra foi alterada nesta corrida. O motor canónico permanece intacto até aprovação explícita segundo a governação do projeto.

---

# Correção de integridade — tese nuclear

Foi também documentada uma falha diferente: o gatilho “novo task order DOE” da tese de 19/07 já tinha ocorrido em 01/07. Um gatilho anterior à tese não é validação forward.

A correção é apenas epistemológica/cronológica: o evento permanece facto, mas é retirado do conjunto de eventos capazes de validar prospectivamente a tese. Não se reescreve o histórico como se o operador o tivesse antecipado.

---

# Métricas do motor

- **T1 longitudinal:** 5 pontos de dados.
- **Temas novos qualificados nesta corrida:** 0.
- **Invalidadores industriais acionados:** 0.
- **Cartões mortos nesta corrida:** 6 — OII, FTI, FORM, TER, Ibiden, NOV.
- **Cartões mortos acumulados por regra procedimental/materialidade:** 7, incluindo FEIM.
- **Cartões retidos ativos:** 1 — SCWO.
- **Watchlist ativa:** 0.
- **Falhas operacionais documentadas:** (i) contador de calendário dependente da frequência de revisão; (ii) trigger nuclear pré-existente à tese.

---

# Fontes principais e proveniência

## Estado e calendário
- Oceaneering IR — Q2 2026 results, 22/07/2026; Financial News index.
- TechnipFMC IR — Upcoming Events e Financial News Releases; último earnings Q2 30/07/2026.
- FormFactor IR — Events & Presentations / Press Releases; Q2 29/07/2026.
- Teradyne IR — IR Calendar / Press Releases; Q2 call 29/07/2026.
- Ibiden — IR Calendar FY2026; Q1 04/08/2026, sem Q2 publicado até ao cutoff.
- NOV IR — Flexible Pipe Manufacturing Expansion, 25/03/2026; News Releases; disclosures segmentados disponíveis.
- Interactive Brokers — OHLCV diário de OII, FTI, NOV, SCWO, FORM, TER, SOXX, FEIM e LEU até 07/08/2026.

## Tese nuclear
- Centrus Energy — contrato DOE de US$900M anunciado 01/07/2026.
- SEC — Form 8-K da Centrus, filing 02/07/2026, Entry into a Material Definitive Agreement.
- Interactive Brokers — histórico diário LEU usado para calcular MA200 em 07/08/2026.

## Discovery
- Baker Hughes — Q2 2026 results, 26/07/2026: IET orders US$7,1B; book-to-bill 2,2x; record IET RPO US$37,1B.
- Vertiv — Q2 2026 results, 29/07/2026: sales +24% e expansão de capacidade numa família já mainstream.
- Manufacturing.gov / Department of War — investimento de US$25M na ReElement, 13/07/2026.
- RENK — H1 2026 publication, 06/08/2026; Reuters 06/08/2026 cobriu recorde de order intake/backlog, confirmando nível 3 de cobertura.
- AIAG–VDA / IEEE — standards recentes usados como pointers; nenhum L1 foi contado como triangulação.
