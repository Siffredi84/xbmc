# Handover — funil de descoberta de small-caps

**Data:** 29 de julho de 2026 · **Sessão de referência:** fecho de 28-07-2026
**Repositório:** `/screening` · **Entrada única:** `run.py` (11 etapas)

---

## 1. O que estamos a construir e porquê

Um funil que varre o mercado accionista americano e devolve uma lista curta de small/micro-caps ($1-7, $50-500M) com actividade anormal, verificadas contra red flags, prontas para análise qualitativa humana.

O ponto de partida foi um documento de critérios escrito pelo utilizador (13 critérios em 7 secções). O código implementa esse documento, mas **diverge dele em pontos deliberados** — todos registados na secção 8. O documento não é a especificação canónica; é o ponto de partida.

**A ferramenta não decide.** Produz uma lista com etiquetas e as razões por trás delas. Todo o julgamento final é do utilizador.

## 2. O princípio invariante

Se levares só uma coisa deste handover, leva esta:

> **Dados em falta produzem etiqueta, nunca decisão.**

Não é filosofia. Emergiu de cinco falhas reais numa única sessão, todas com a mesma forma — uma ausência de dados a disfarçar-se de facto sobre o mundo:

| Falha | O que pareceu | O que era |
|---|---|---|
| `pandas.read_html` no Finviz | tickers falsos (`AABOS`) | `<span>` do logótipo concatenado com o ticker |
| Finnhub sem pacing | 18 candidatos fora dos critérios | rate limit → `NaN` → filtro descartou em silêncio |
| NVA ausente do funil | reprovado nos gates | 11 sessões em falta (suspensão por redomiciliação) |
| EDGAR em rajada | 17 empresas "sem registos na SEC" | estrangulamento HTTP |
| Emissores 20-F | aprovados no gate de going concern | não existe 10-Q para verificar |

Está codificado em quatro sítios: `quarentena.py` (integridade de série), `finnhub.py` (resposta vazia → `falhas`), `identidade.py` (estado `REVER`), `edgar.py` (`FalhaRede` distinto de `SEM_SUBMISSOES`).

**Corolário arquitectural:** nenhuma fonte ocupa dois papéis. Quem descobre não valida.

```
POLYGON    largura         universo inteiro, OHLCV bruto. Nunca valida.
IBKR       profundidade    identidade autoritativa, liquidez, opções.
YAHOO      árbitro         só quando as duas primeiras divergem.
FINNHUB    fundamentais    market cap, 52W, regime de reporte, insiders.
EDGAR      red flags       going concern, delisting, splits, catalisadores 8-K.
FRED       macro           regime de risco.
MARKETAUX  notícias        só na fila de evento (quota 100/dia).
FINVIZ     tripwire        funil paralelo, só para detectar divergência.
```

## 3. Estado do código

11 etapas, ~18 s com cache quente, ~17 min a frio (74 chamadas Polygon a 13 s).

| Módulo | Papel | Estado |
|---|---|---|
| `config.py` | todos os limiares | ⚠️ `TIPO_VALIDO` definido e não usado |
| `polygon.py` | universo + guarda de calendário | ok |
| `fase0.py` | indicadores, quarentena, gates técnicos | ok |
| `finnhub.py` | enriquecimento, cache por sessão | ok |
| `identidade.py` | gate tri-fonte, 3 estados | ok |
| `encaminhamento.py` | evento vs continuação | ok |
| `quarentena.py` | integridade de série | ok |
| `edgar.py` | red flags e catalisadores | ⚠️ reverse split por proxy errado |
| `fred.py` | gate macro | ok |
| `continuacao.py` | insiders e diluição | ❌ sinal de insider errado |
| `evento.py` | notícias e sentimento | ok, mas cobertura fraca |
| `descoberta.py` | sinais precoces | ⚠️ parcial |
| `tripwire.py` | divergência Finviz | ok, só válido pós-fecho |
| `run.py` | orquestração | ok |

**Resultado da corrida de referência:** 13.034 tickers → 5.291 common stocks → 940 (preço+volume) → 111 (volume relativo) → 50 shortlist → 21 finalistas → 20 aprovados (ABOS reprovado por going concern).

## 4. Conformidade critério a critério

Cada um foi testado empiricamente, não lido. Ficheiros de teste em `/mnt/user-data/outputs/`.

| # | Critério | Estado | Achado principal |
|---|---|---|---|
| 1 | Preço $1-7 | ✅ | preço bate com Yahoo em 8/8; **15× mais massa junto a $1 do que a $7** |
| 2 | Market cap $50-500M | ⚠️ | **2 de 21 errados**: CRDL em CAD (+42%), SUPX desactualizado (−38%) |
| 3 | Volume médio >100k | ✅ | desvio de fonte 0,1%; CIA passa por 1,1× apenas |
| 4 | NYSE/NASDAQ/AMEX | ⚠️ | correcto **por acidente** — o código não filtra bolsa |
| 5 | RSI(14) 25-60 | ✅ | corta 30%, quase todo pelo tecto; Wilder varia ±5 pts com o comprimento da série |
| 6 | Preço vs MA20 >−15% | ✅ | corta 36%; **unilateral** — nada trava o excesso para cima |
| 7 | Volume relativo >1,2× | ✅ | corta 88%; **mediana do universo é 0,51** — o gate é muito mais duro do que parece |
| 8 | <90% do máximo 52s | ✅ | corta 3 em 50; **inútil** — a base está toda no fundo |
| 9 | ≥1 sinal A/B/C | ❌ | regra não implementada; todos a cumprem hoje |
| 10 | Tier 1 / Tier 2 | ❌ | **o funil duplica a concentração biotech**: 31% → 67% |
| 11 | Red flags | ⚠️ | reverse split falhou o único caso; queda >80% ausente |
| 12 | Descoberta precoce | ⚠️ | **sinal de insider mede atribuições, não compras** |
| 13 | Selecção final 5-10 | ❌ | ordenação colapsa: 10 de 13 no primeiro escalão |

## 5. Correções prioritárias

### P1 — Insider buying mede a coisa errada (`continuacao.py`, `descoberta.py`)

Somamos `change` de todas as transacções em 6 meses. O Finnhub devolve `transactionCode` que ignorávamos: **P** = compra em mercado aberto, **A** = atribuição, **M** = exercício de opções.

Com a implementação actual, PMVP e SIGA aparecem como tendo insiders compradores tendo comprado **zero** acções — são atribuições da empresa aos executivos, sinal oposto. E o TOI, que teve 33.000 acções compradas em mercado aberto nos últimos 30 dias, não é sinalizado porque vendas antigas afundam o saldo bruto.

Filtrar `transactionCode == 'P'` e usar janela de 30 dias (como o documento pede). Passam a três: **BYRN** (96.987 acções, quase tudo no último mês), **ANIX** (24.797, zero atribuições), **TOI**.

Duas linhas. É a correcção com maior impacto na qualidade do sinal.

### P2 — Market cap sem verificação (`finnhub.py`)

O campo `currency` não resolve: SNDL diz CAD e está correcto em USD; CRDL diz CAD e está em CAD. Só o cálculo independente revela quem está errado.

Calcular `shareOutstanding × preço USD` e usar o valor do Finnhub como verificação cruzada. Divergência >5% vira etiqueta. Hoje não muda aprovações (ambos ficam dentro da banda), mas o TOI está a 1% do tecto de $500M — um erro de 42% junto à fronteira inverte a decisão.

### P3 — Reverse split pelo método errado (`edgar.py`)

Usamos o item 5.03 do 8-K como proxy. Encontrou **zero**. O endpoint `/v3/reference/splits` do Polygon (já no plano, uma chamada) mostra **1.257 reverse splits em 12 meses**, dos quais **167 no universo elegível (17,8%)** e um nos finalistas aprovados: **TLRY**.

### P4 — Red flag "queda >80% sem recuperação" (ausente)

Tornou-se computável usando o mínimo de 52 semanas: excluir quando `High52_pct <= -80` **e** preço a menos de 15% do mínimo.

| Ticker | Abaixo do máx. | Acima do mín. | Veredicto |
|---|---|---|---|
| SUPX | −91,4% | +6,1% | excluir |
| TLRY | −82,6% | +6,1% | excluir |
| BYRN | −87,0% | **+25,4%** | manter — há recuperação |

O qualificador "sem recuperação" existe precisamente para salvar casos como o BYRN, que é o candidato com melhor perfil da lista.

### P5 — Filtro de bolsa explícito (`fase0.py:39`)

Só filtramos `type == "CS"`. Zero OTC aparece, mas por propriedade do endpoint Polygon, não por regra nossa. Se o plano ou o fornecedor mudarem, entram pink sheets sem aviso. Adicionar `exch in {"XNAS","XNYS","XASE"}` e ligar o `config.TIPO_VALIDO` que já existe e não é usado.

## 6. Redundâncias e gates que não trabalham

- **Máximo de 52 semanas (critério 8):** corta 3 em 50. Os outros gates já garantem que nada está perto do topo. O risco real está no extremo oposto, coberto pelo P4. Manter (custo zero), mas não contar com ele.
- **Limite inferior do RSI:** corta 2, o superior corta 19. O intervalo é efectivamente "RSI < 60".
- **Consolidação lateral (sinal C):** dispara em 17 de 21 com a definição actual (amplitude <1,6× em 60 sessões). Um teste que 81% passam não distingue. Apertar para ~1,3× antes de activar a regra do critério 9.
- **`MAX_SPREAD_PCT` e `MIN_USD_VOL_90D`:** definidos em `config.py`, nunca aplicados. A camada de execução tem dados para 1 de 21 nomes. Ou se preenche com o mercado aberto, ou se remove a promessa.

## 7. Contradições internas do documento original

Não são bugs do código — são tensões na especificação que alguém tem de resolver.

1. **Gate de RSI vs Sinal B.** O gate corta abaixo de 25; o sinal B quer acções a sair de oversold (<30 → >35). O gate elimina a população onde o sinal vive. Resultado: o sinal B dispara 8 vezes em 21. Baixar o piso para 20 custa 2 candidatos e devolve sentido ao sinal.
2. **Gate de volume relativo vs Sinal A.** O gate exige 1,2×; o sinal A define spike como 2×+. Só 4 de 21 finalistas cumprem o sinal A; 12 estão entre 1,2 e 1,5. Sugestão: exigir 2× ao **pico dos últimos 20 dias**, não ao dia corrente — captura a intenção sem descartar continuação.
3. **Filtro sectorial agrava o problema que devia resolver.** O funil já duplica a concentração biotech (31% do universo → 67% dos finalistas), provavelmente porque eventos clínicos produzem exactamente o pico de volume que o gate procura. Aplicar Tier 1 removeria os únicos três nomes fora de saúde e deixaria a lista 89% biotech. Recomendação contrária à letra do documento: **limitar concentração** em vez de priorizar sector.
4. **Ordem de prioridade invertida.** A prioridade 1 ("volume spike + sector prioritário") absorve 10 de 13; as prioridades 2 e 3 ficam vazias. São conjunções raras — e são as que descrevem teses. Inverter: insider+reversão primeiro, consolidação+breakout depois, volume+sector por último.

## 8. Decisões já tomadas (não reabrir sem motivo)

| Decisão | Razão |
|---|---|
| Janela de volume: **63 sessões**, não 30 | comparabilidade com Finviz e histórico; resiste à contaminação pelo próprio pico |
| Universo por **cotação**, não domicílio | o documento diz "listadas em NYSE/NASDAQ/AMEX"; campo `regime_reporte` (10-Q vs 20-F) trata a diferença de reporte |
| Emissores 20-F entram, mas **red flags falham por omissão** neles | não existe 10-Q para verificar |
| Encaminhamento **evento vs continuação** por rácio Eco (pico 20d ÷ hoje) | perguntas de falsificação diferentes; poupa quota Marketaux |
| Excluir closed-end funds e SPACs | `type == CS` fá-lo automaticamente |
| Quarentena por sessões em falta (>3) | ver princípio invariante |
| Volatilidade 20d é **bandeira, não gate** | BYRN a 171% anualizado é diferente de TLRY a 36% |

## 9. Armadilhas do ambiente e das fontes

- **Finviz:** filtros não reconhecidos são **silenciosamente ignorados** (`sh_price_1to7`, `ta_rsi_os60` não existem). Verificar sempre o título da página. Códigos de vista: 111 Overview, 141 Performance, 171 Technical.
- **Finviz não tem data de referência** — mostra sempre agora. O tripwire só é válido entre o fecho e o pre-market seguinte. `mesma_sessao()` discrimina por **volume** (ordem de grandeza), não por preço (que em pre-market varia décimas e engana).
- **SEC EDGAR estrangula rajadas** mesmo abaixo dos 10 req/s documentados. Backoff exponencial obrigatório.
- **"Going concern" no texto ≠ going concern.** A frase aparece em quase todo o 10-Q de biotech como política contabilística (ASC 205-40). Distinguir avaliação de conclusão. Três estados: CONFIRMADO / ALIVIADO / A_REVER.
- **S-8 não é diluição** — são planos de acções para empregados. S-3/S-1/424B* é que são.
- **Finnhub free:** `recommendation-trends` devolve **HTML com status 200**; `upgrade-downgrade` devolve 403. Um 200 não garante JSON.
- **Determinismo só com o mercado fechado.** A meio da sessão os valores do Finnhub mudam entre execuções.
- **O container apaga-se entre sessões.** A cache Polygon (198 MB, 74 chamadas) e a Finnhub não sobrevivem.

## 10. Por construir

1. **Regra "≥1 sinal A/B/C"** — os oito sub-sinais estão validados em `teste_sinais_abc.csv`; falta integrá-los. Apertar o C primeiro.
2. **Selecção final e ordenação** — com prioridades invertidas (secção 7.4).
3. **Cobertura de analistas** — sem fonte no plano actual. Exige Benzinga, MarketBeat ou scraping.
4. **Menções Reddit** — sem fonte.
5. **Catalisadores pendentes** (FDA/PDUFA, earnings) — quarto nível de prioridade do documento. Finnhub tem calendário de earnings; PDUFA não tem fonte livre.
6. **Camada de execução** (spread, USD-vol) — precisa de snapshots IBKR com o mercado aberto.
7. **Equivalente 20-F ao gate de going concern** — CRDL, SNDL, SUPX à espera.
8. **Agendar o tripwire** numa janela pós-fecho.
9. **Twelve Data como desempate** — papel definido, zero integração.

## 11. Pendentes do utilizador

- **Rodar as cinco chaves de API** — foram partilhadas em texto simples e continuam válidas. É a única acção urgente.
- Decidir: **NVA** volta ao funil com janela pós-redomiciliação?
- Decidir: quatro nomes em quarentena por série curta (AGNT, AMSS, QMLS, BIOT).
- Resolver as quatro contradições da secção 7.

## 12. Primeiros passos sugeridos

1. Ler este documento e `auditoria-projeto-screening.md` (defeitos D1-D5, E1-E6).
2. Correr `run.py` a frio uma vez, com o mercado fechado, para ver o funil inteiro.
3. Aplicar P1 a P5 — são todas pequenas e independentes.
4. Só depois mexer na especificação (secção 7), que exige decisões do utilizador.

**Não faças isto:** não relaxes um gate para "arranjar" um resultado estranho. Cinco vezes nesta sessão o resultado estranho era um bug de dados, e a etiqueta separada foi sempre a resposta certa. Quando um candidato parece errado, a primeira hipótese é que a fonte falhou — não que o critério está mal calibrado.
