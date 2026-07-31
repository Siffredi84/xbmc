# Fase 4 — Plano de implementação

**Data:** 30 de julho de 2026 · **Base:** especificação da Fase 3
**Decisão aplicada:** zona morta do `Eco` **não é setup** — residual é resposta, não falha. Nenhum limiar de classificação é ajustado para o reduzir.

---

## 0. Estratégia de migração

**Lado a lado, não substituição.** O pipeline actual (`run.py`) continua a correr sem alterações enquanto o vNext é construído em `vnext/`. Isto é obrigatório: a Fase 5 exige um shadow run com os mesmos snapshots, e não há shadow run se o original for modificado.

Regra: **nenhum ticket pode alterar ficheiros do pipeline actual**, com três excepções explícitas (D0-1, D0-2, D0-3 — defeitos de robustez que afectam ambos).

**Snapshots congelados** em `snapshots/2026-07-29/` e `2026-07-30/` antes de qualquer trabalho. Sem isto a comparação da Fase 5 é irreprodutível.

---

## 1. Backlog

Ordenado por dependência. `P0` = bloqueia outros · `P1` = caminho crítico · `P2` = paralelizável · `P3` = pode esperar.

### Épico D0 — Defeitos de robustez (afectam ambos os pipelines)

| ID | Trabalho | Módulo | Prio | Dep. | Risco |
|---|---|---|---|---|---|
| D0-1 | `polygon.py` lê `POLYGON_KEY` no import → mover para dentro de `_get()` | `polygon.py` | **P0** | — | Nulo. Hoje impede testar sem credenciais |
| D0-2 | `queda_sem_recuperacao(None, x)` levanta `TypeError` → devolver `None` (etiqueta) | `finnhub.py` | **P0** | — | Nulo. Viola o princípio invariante |
| D0-3 | `except Exception` largo no bloco de splits do `run.py` → restringir a excepções de rede | `run.py` | P1 | — | Baixo. Hoje um erro de código é indistinguível de dia sem splits |
| D0-4 | Backoff da SEC: 5 → 8 tentativas, até 60 s, com jitter | `edgar.py` | P1 | — | Baixo. 503 esgotou o backoff em 30-07 |

**Teste de aceitação D0:** `import polygon` sem variáveis de ambiente não levanta. `queda_sem_recuperacao(None, 10)` devolve `None`. Injecção de 503 em 6 tentativas consecutivas não interrompe a corrida.

### Épico E1 — Núcleo de estados e contratos

| ID | Trabalho | Módulo | Prio | Dep. | Risco |
|---|---|---|---|---|---|
| E1-1 | `vnext/estados.py`: enum dos seis estados + `Resultado(valor, estado, fonte, proveniencia)`; proibir coerção entre estados | novo | **P0** | — | Baixo |
| E1-2 | `vnext/contratos.py`: schema de entrada/saída por fase, validado em runtime | novo | **P0** | E1-1 | Médio — schema demasiado rígido trava iteração |
| E1-3 | `vnext/config.py`: todos os limiares, cada um com `origem` (documento / decisão / medição / **provisório**) | novo | **P0** | — | Nulo |

**Teste:** unitário sobre cada transição proibida (`SEM_FONTE → SEM_SINAL` levanta). Validação de contrato falha com mensagem que nomeia a coluna em falta.

### Épico A — Universo

| ID | Trabalho | Módulo | Prio | Dep. | Risco |
|---|---|---|---|---|---|
| A-1 | `vnext/universo.py`: A1 calendário + A2 tipo/bolsa | novo | P1 | E1-2 | Baixo — porte directo |
| A-2 | **A3 corporate actions no topo.** Split ≤90 d → exclusão; 90-365 d → `split_estado=RECENTE` + janela truncada | `vnext/corporate.py` | **P1** | A-1 | **Médio** — regra nova, remove 72 de 932 |
| A-3 | A5 quarentena (porte de `quarentena.py`, ligado ao novo modelo de estados) | `vnext/quarentena.py` | P1 | E1-1 | Baixo |

**Teste de integração A:** AMIX, GMM, JBDI e YYGH excluídos na Fase A sobre o snapshot de 29-07. Contagem de chamadas por candidato **zero** para os excluídos.

### Épico B — Gates técnicos

| ID | Trabalho | Módulo | Prio | Dep. | Risco |
|---|---|---|---|---|---|
| B-1 | B1/B2a porte | `vnext/gates.py` | P1 | A-3 | Nulo |
| B-2 | **B2b gate de volume USD** `> $1M` | `vnext/gates.py` | **P1** | B-1 | **Médio** — remove 205 de 860; T2 validou a distribuição de sinais |
| B-3 | B3 indicadores com **janela RSI fixa em 63** e `MedVol_63` | `vnext/indicadores.py` | P1 | B-2 | Baixo — mas altera valores de RSI face ao actual |
| B-4 | B5 tecto de RSI apenas; `rsi_zona` como feature | `vnext/gates.py` | P1 | B-3 | Baixo |
| B-5 | **B7 range de 252 sessões, truncado no último split** | `vnext/range52.py` | **P1** | A-2, backfill | **Alto** — depende do backfill e substitui a fonte do P4 |
| B-6 | **B8 sinais A/B/C; C exige ≥2 de 3; gate `≥1`** | `vnext/sinais.py` | **P1** | B-3 | Médio — regra nova, prevalência do C por medir |
| B-7 | Flags `risco_listagem`, `extensao`, `volume_assimetrico` | `vnext/flags.py` | P2 | B-3, C-1 | Baixo — não excluem |

**Teste de integração B:** sobre o snapshot de 29-07, a shortlist tem **48 candidatos**. SOUN excluído por B8.

### Épico C — Identidade

| ID | Trabalho | Módulo | Prio | Dep. | Risco |
|---|---|---|---|---|---|
| C-1 | `vnext/identidade.py`: IBKR primária → Yahoo árbitro; três estados; `tier_listagem` | novo | P1 | E1-1 | Médio |
| C-2 | **Adaptador IBKR.** As ferramentas são MCP e não são chamáveis do Python. Contrato `IBKRSource` com duas implementações: `ib_insync` (produção) e `ficheiro` (injecção manual) | `vnext/fontes/ibkr.py` | **P1** | C-1 | **Alto** — sem `ib_insync` configurado, o vNext corre em modo degradado com o Yahoo |

**Teste:** regressão dos 12 tickers conhecidos, incluindo o par `BW`/`BBW`. SNDL continua a dar `REVER` (nome desactualizado no funil).

### Épico D — Fundamentais

| ID | Trabalho | Módulo | Prio | Dep. | Risco |
|---|---|---|---|---|---|
| D-1 | `vnext/fontes/sec.py`: `companyconcept` com as cinco regras (end mais recente, soma de classes no mesmo end, accn mais recente, freshness 120 d, fallback) | novo | **P1** | C-1 | **Alto** — semântica XBRL não validada (lacuna L8) |
| D-2 | D2 market cap canónico + gate | `vnext/fundamentais.py` | P1 | D-1 | Médio |
| D-3 | D3 regime de reporte | `vnext/fundamentais.py` | P2 | C-1 | Baixo |

**Teste:** TOP → $78M (não $1.305M). AMIX → $52M (não $2,5M). **NKLR → $540M e excluído.** Divergentes < 5% da shortlist.

### Épico E — Red flags

| ID | Trabalho | Módulo | Prio | Dep. | Risco |
|---|---|---|---|---|---|
| E-1 | Porte de going concern e itens de 8-K | `vnext/redflags.py` | P1 | C-1, D0-4 | Baixo |
| E-2 | **P4 sobre o range calculado**; não decide se `range_estado ≠ OK` | `vnext/redflags.py` | **P1** | B-5 | **Alto** — a lista de 6 exclusões vai mudar |
| E-3 | Fila `REVISAO_20F` explícita | `vnext/redflags.py` | P2 | D-3 | Baixo |

### Épico F — Enriquecimento

| ID | Trabalho | Módulo | Prio | Dep. | Risco |
|---|---|---|---|---|---|
| F-1 | Insiders (código P, 30 dias) — porte | `vnext/insiders.py` | P2 | C-1 | Baixo |
| F-2 | **Spread e profundidade do livro** via adaptador IBKR; gate `≤2%`, exclusão dura `>5%`; **só com mercado aberto** | `vnext/execucao.py` | P2 | C-2 | **Alto** — limiar de 17 observações numa sessão |
| F-3 | Breakout com parâmetros expostos (tolerância 2%, janela 60) | `vnext/descoberta.py` | P2 | B-3 | Baixo |
| F-4 | Notícias (só fila de evento) e diluição | `vnext/noticias.py` | P3 | G-1 | Baixo |

### Épico G — Classificação, ordenação, observabilidade

| ID | Trabalho | Módulo | Prio | Dep. | Risco |
|---|---|---|---|---|---|
| G-1 | **`vnext/setups.py`: cinco setups por precedência lexicográfica**; residual sem tratamento especial | novo | **P1** | B-6, F-1 | Médio |
| G-2 | `vnext/ordenacao.py`: 3 níveis, desempate por `AvgVolUSD_63`, tecto de 10, `razao_lista_curta` | novo | P1 | G-1 | Baixo |
| G-3 | `vnext/metricas.py`: funil, exclusivos por gate, estabilidade, concentração, missingness, custo, residual | novo | P2 | G-2 | Baixo |
| G-4 | Tripwire Finviz com guarda de sessão (porte) | `vnext/tripwire.py` | P3 | G-2 | Baixo |

**Teste G:** sobre 29-07, distribuição **2/1/1/4/6/12** reproduzida exactamente sobre os **26** candidatos que passam os gates fundamentais. Nenhuma corrida devolve >10. Toda a posição explicável por uma regra nomeada.

> **Corrigido pela Fase 5 §0.** Este teste dizia 2/3/2/7/12/22 — números medidos sobre os 48 sobreviventes dos gates *técnicos*, sem lhes aplicar market cap e range de 52 semanas. `tests/test_snapshot.py` fixa as duas leituras sobre `snapshot/setups_3007.csv`: 2/3/2/7/12/22 é o que lá está para os 48, e os 14 classificados nomeados na correcção são os que sobrevivem aos gates fundamentais.

### Épico H — Infraestrutura

| ID | Trabalho | Prio | Dep. | Notas |
|---|---|---|---|---|
| H-1 | **Backfill de 181 sessões** (~39 min) | **P0** | D0-1 | Bloqueia B-5 e E-2 |
| H-2 | Congelar snapshots de 29-07 e 30-07 | **P0** | — | Bloqueia toda a Fase 5 |
| H-3 | `vnext/run.py` a encadear A→G | P1 | todos | — |
| H-4 | Harness de shadow run | P2 | H-2, H-3 | Fase 5 |
| H-5 | Repositório: `requirements`, `.gitignore`, README do vNext | P2 | — | — |

---

## 2. Caminho crítico

```
D0-1 ──► H-1 (backfill 39 min) ──► B-5 (range) ──► E-2 (P4) ──► G-1 ──► G-2
   └──► E1-1 ──► E1-2 ──► A-1 ──► A-2 ──► A-3 ──► B-1 ──► B-2 ──► B-3 ──► B-6 ──┘
                                                     C-1 ──► C-2 ──► D-1 ──► D-2
```

**Dois bloqueadores duros:** H-1 (backfill) e H-2 (snapshots). Ambos P0, ambos executáveis já, ambos sem dependências.

**Três tickets de risco alto:** B-5 (range), D-1 (semântica XBRL), C-2 (adaptador IBKR). Nenhum é resolúvel por mais código — **todos dependem de informação que ainda não temos.**

---

## 3. Testes

**Unitários** (sem rede, com stubs):
`estados` transições proibidas · `corporate` fronteiras 89/90/91 dias · `gates` fronteiras $1,00/$7,00/$1M · `indicadores` RSI reprodutível com janela fixa · `sinais` C com 1 vs 2 vs 3 componentes · `sec` end/accn/classes/freshness · `setups` precedência e exclusividade mútua · `ordenacao` desempates e tecto.

**Integração** (sobre snapshot congelado de 29-07):
| Etapa | Esperado |
|---|---|
| Universo | 5.299 → exclui 144 por split ≤90 d |
| Gates B | shortlist **48** |
| Identidade | 47 `OK`, 1 `REVER` (SNDL) |
| Market cap | NKLR excluído; divergentes <5% |
| Red flags | PYPD reprovado; ABEO/ACB `NETWORK_FAILURE` |
| Setups | **2/1/1/4/6/12** sobre 26 elegíveis (corrigido na Fase 5 §0) |
| Ordenação | ≤10, todas explicáveis |

**Regressão congelada:** os 12 tickers de identidade + os quatro removidos pelo T1 + os quinze do T2.

---

## 4. Critérios de aceitação do vNext

1. Todos os testes unitários e de integração passam sobre o snapshot congelado.
2. Zero ocorrências de coerção entre estados.
3. Nenhum candidato aprovado com `DATA_INSUFFICIENT`, `DATA_INVALID` ou `DATA_STALE` num gate de elegibilidade.
4. Corrida normal **< 10 min** com cache quente; backfill **< 4 h**.
5. Reserva de quota respeitada em todos os fornecedores.
6. Toda a posição na ordenação explicável por uma regra nomeada; zero desempates implícitos.
7. Cada limiar em `config.py` tem `origem` declarada; nenhum classificado como `provisório` é usado como gate duro sem revisão marcada.
8. `metricas.json` produzido em todas as corridas, incluindo as que devolvem zero candidatos.

---

## Handoff — Fase 4

**Decisões fechadas:** 33 tickets em 8 épicos, ordenados por dependência; estratégia de migração lado a lado com o pipeline actual intocado (3 excepções nomeadas); caminho crítico com dois bloqueadores P0 executáveis imediatamente; matriz de testes unitários e de integração com valores esperados retirados de medições reais; oito critérios de aceitação.

**Evidência utilizada:** todos os números esperados nos testes de integração vêm de corridas medidas (29-07 e 30-07), não de estimativas.

**Decisões provisórias:** o limiar de spread (F-2) entra com 17 observações de uma sessão. A prevalência do sinal C com a regra "≥2 componentes" (B-6) nunca foi medida — só a regra antiga foi.

**Questões abertas:** **L8 continua a bloquear D-1.** As cinco regras de semântica XBRL estão especificadas mas nenhuma foi validada contra dados reais da SEC. É o ticket de maior risco do backlog e o único onde o custo de errar é um gate de elegibilidade errado. E **C-2 depende de o `ib_insync` ser configurado** — sem isso o vNext corre permanentemente em modo degradado com o Yahoo como fonte primária de identidade, o que anula a arquitectura tri-fonte.

**Inputs necessários para a Fase 5:** H-1 e H-2 executados. Confirmação de que o shadow run compara **29-07** (sessão com funil completo medido) e não 30-07.

**Riscos de avançar:** a Fase 5 define o critério de promoção do vNext. Sem histórico de resultados (lacuna L4), "superior" só pode significar coerência interna, cobertura de dados e explicabilidade — nunca qualidade de candidatos. Isso tem de ficar explícito no critério, sob pena de se promover um pipeline mais rigoroso que produz piores decisões sem que nada o detecte.

**Condição para iniciar a Fase 5:** confirmação da data do shadow run e aceitação de que o critério de promoção não mede rendibilidade.
