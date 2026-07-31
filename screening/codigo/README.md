# Funil de descoberta small-caps

Screening de small/micro-caps EUA ($1-7, $50-500M) com verificacao tri-fonte.

## Correr

    pip install -r requirements.txt
    POLYGON_KEY=... FINNHUB_KEY=... python3 run.py

Primeira execucao ~17 min (descarga do universo, 74 chamadas Polygon a 13s).
Execucoes seguintes no mesmo dia de mercado: ~6 s, zero chamadas.

## Arquitectura

    POLYGON   largura      universo inteiro, OHLCV bruto. Nunca valida.
              corporate actions para reverse splits (fonte especifica).
    IBKR      profundidade identidade autoritativa, liquidez, opcoes, execucao.
    YAHOO     arbitro      so quando as duas primeiras divergem ou nao cobrem.
    FINNHUB   fundamentais market cap, 52W high, regime de reporte, filings.
    FRED      macro        gate de regime, percentis de 5 anos da propria serie.
    MARKETAUX noticias     so na fila de evento; segunda fonte Finnhub company-news.
    EDGAR     red flags    going concern, delisting, reverse split, catalisadores 8-K.

Regra estrutural: **nenhuma fonte ocupa dois papeis**. Quem descobre nao valida.

## Principio que governa o desenho

**Dados em falta produzem etiqueta, nunca decisao.** Um `NaN`, uma serie com
buraco ou um nome divergente nao podem virar aprovacao nem reprovacao silenciosa.
Aparece em tres sitios:

- `quarentena.py` — series com sessoes em falta acima da linha de base do
  mercado sao etiquetadas (INTERRUPCAO / SERIE_CURTA / ILIQUIDEZ), nao descartadas.
- `finnhub.py` — resposta vazia vai para `falhas`, nunca para um `NaN` que o
  filtro elimina; market cap e calculado por shares outstanding × preco e o
  valor fornecido fica como comparador.
- `identidade.py` — ticker e exchange a bater com nome divergente da `REVER`,
  nao FAIL.
- `edgar.py` — falha da verificacao Polygon de reverse splits produz
  `VERIFICACAO_INCOMPLETA`, nunca aprovacao.

## Modulos

| Ficheiro | Papel |
|---|---|
| `config.py` | todos os limiares. Nada de numeros magicos noutros ficheiros |
| `polygon.py` | universo + guarda de calendario |
| `fase0.py` | indicadores, quarentena, gates tecnicos |
| `finnhub.py` | enriquecimento com cache por sessao |
| `identidade.py` | gate tri-fonte, tres estados (OK/REVER/FAIL) |
| `encaminhamento.py` | evento vs continuacao, filas de trabalho |
| `quarentena.py` | integridade de serie |
| `finviz.py` | funil alternativo, hoje usado como verificacao cruzada |
| `fred.py` | gate macro, regime RISK_ON/NEUTRO/RISK_OFF |
| `continuacao.py` | insiders e formularios de diluicao |
| `evento.py` | noticias e sentimento, Marketaux + Finnhub |
| `edgar.py` | red flags e catalisadores directamente da SEC |
| `descoberta.py` | sinais de descoberta precoce (etiquetas, nunca score) |
| `tripwire.py` | funil Finviz em paralelo, so para detectar divergencia |
| `run.py` | encadeia tudo |
| `tests/test_prioridades_p1_p5.py` | regressao deterministica das correcoes P1-P5 |

## Saidas

- `saida_finalistas.csv` — finalistas com indicadores, regime e grupo
- `saida_macro.csv` — series FRED com percentil e tendencia
- `saida_continuacao.csv` — insiders e diluicao por candidato
- `saida_evento.csv` — cobertura noticiosa e sentimento
- `saida_edgar.csv` — going concern, itens de 8-K, catalisadores
- `saida_descoberta.csv` — sinais precoces por candidato
- `saida_resumo.json` — filas, sem dados, revisao, diluicao, sem cobertura

## Notas operacionais

- Chaves por variavel de ambiente. Nunca no codigo, nunca num prompt.
- O determinismo so se garante com o mercado fechado; a meio da sessao os
  valores Finnhub mudam entre execucoes.
- `finviz.py` corre em paralelo como tripwire: divergencia superior a 2 nomes
  sem explicacao merece investigacao.
- `High52_pct` mistura fecho Polygon com maximo Finnhub — unico indicador
  hibrido do funil. Resolvivel com ~252 sessoes de cache Polygon.

## Limitacoes conhecidas

**Cobertura noticiosa de micro-caps e fraca nas duas fontes.** Na corrida de
28-07, 9 dos 13 candidatos de evento nao tinham um unico artigo em Marketaux
nem em Finnhub. `SEM_COBERTURA` significa exactamente isso — ausencia de
cobertura, nunca ausencia de acontecimento. Para estes, o catalisador tem de
ser procurado directamente no EDGAR (8-K) ou em press releases.

**Insider buying significa apenas codigo P nos ultimos 30 dias.** Atribuicoes
(A) e exercicios de opcoes (M) sao contabilizados como transaccoes ignoradas,
nunca como compras. Vendas abertas usam codigo S.

**"Going concern" no texto nao e going concern.** A frase aparece em quase
todos os 10-Q de biotech como politica contabilistica (ASC 205-40). O modulo
distingue a avaliacao ("avaliamos se existe duvida substancial") da conclusao
("concluimos que existe duvida substancial") e devolve tres estados —
CONFIRMADO, ALIVIADO, A_REVER. Texto ambiguo vai para A_REVER, nunca para
aprovado.

**Nova cobertura de analistas nao tem fonte no stack actual.** Verificado em
29-07-2026: Finnhub free devolve HTML com 200 em `/stock/recommendation-trends`
e 403 em `/stock/upgrade-downgrade`; Twelve Data Basic exige plano ultra ou
enterprise para ratings. O sinal devolve `None`, nao `False` — nao sabemos, e
diferente de nao existe. Exige fonte nova.

**O tripwire so e valido depois do fecho.** O Finviz nao tem data de
referencia: mostra sempre agora. Em pre-market compara uma sessao a decorrer
com a nossa ultima sessao fechada e produz alarme falso — aconteceu na
primeira execucao. `mesma_sessao()` discrimina pelo volume (ordem de grandeza,
nao margem) e devolve `NAO_COMPARAVEL` fora da janela util.

**S-8 nao e diluicao.** Planos de accoes para empregados aparecem em coluna
separada de S-3/S-1/424B*. Junta-los faria rotina parecer risco.

## Por construir

Fonte para cobertura de analistas; Twelve Data como desempate; correr o
tripwire numa janela pos-fecho (idealmente agendado, nao manual).

## Testes locais

Depois de instalar `requirements.txt`:

    python3 -m unittest discover -s tests -v

Os testes nao usam APIs nem chaves. Cobrem compras abertas a 30 dias, market
cap calculado, reverse splits, queda anual sem recuperacao e filtro de bolsa.

Os CSV incluídos no arquivo são a fotografia da corrida de referência anterior
às correções P1-P5. Não devem ser tratados como uma nova corrida do código.
