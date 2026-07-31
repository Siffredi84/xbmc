# Auditoria do projeto de screening small-caps

**Data:** 29 de julho de 2026
**Âmbito:** tudo o que foi construído neste ciclo — extração Finviz, arquitectura tri-fonte, Fase 0 Polygon, enriquecimento Finnhub, encaminhamento evento/continuação, detetor de quarentena — confrontado com o documento de critérios original e com as políticas do alpha-k-data-pipeline.

---

## 1. Estado por componente

| Componente | Estado | Confiança |
|---|---|---|
| `finviz_extract.py` — parser por atributo | Funcional, regressão implícita (178/178, 16/17 reproduzidos pelo caminho independente) | Alta |
| `validate.py` — identidade via Yahoo | Funcional, regressão 12/12 | Alta |
| `pipeline.py` — tri-fonte | Funcional no gate de identidade; **camada de execução incompleta** | Média |
| `pg_fase0.py` — universo Polygon | Funcional, cache em disco, pacing 13 s | Alta |
| Enriquecimento Finnhub (mcap, 52W, regime) | Funcional após correção de pacing; **inline, não é módulo** | Média |
| Encaminhamento evento/continuação (Eco) | Funcional, 21 classificados | Alta |
| `quarentena.py` — integridade de série | Funcional, 467 etiquetados, NVA capturado | Alta |
| Fases 2–6 do framework | **Não construídas** | — |

## 2. Defeitos confirmados nesta auditoria

**D1 — A "janela de 63 sessões" é na prática de 59.** `v[-64:-1]` sobre as 60 sessões de mercado disponíveis usa 59 valores. A decisão registada foi 63; para a cumprir é preciso descarregar até 64+feriados sessões (≈67 dias úteis). Impacto real baixo — a zona é plana, como o teste de sensibilidade mostrou — mas o nome da coluna (`AvgVol63`) afirma uma coisa que o código não faz. Corrigir o download ou o nome; nunca deixar os dois em contradição.

**D2 — Limiares de execução declarados e não aplicados.** `MAX_SPREAD_PCT` está definido em `pipeline.py` e nunca é usado em lado nenhum; `MIN_USD_VOL_90D` só alimenta um campo informativo. A camada de execução tem dados reais para 1 de 17 nomes (BYRN, e colhidos em pre-market, portanto o spread de 12,9% não é utilizável). Tal como está, `pipeline.py` promete uma camada de profundidade que não existe. Ou se preenchem os snapshots com o mercado aberto, ou se remove a promessa do código.

**D3 — O árbitro nunca pode absolver.** Em `resolve()`, quando a IBKR devolve FAIL, o Yahoo é consultado mas o resultado é forçado a `False` (`y_ok and False`). Conservador e defensável — identidade divergente entre corretora e árbitro deve mesmo parar — mas então a chamada ao Yahoo nesse ramo é puro custo. Decidir: ou o árbitro desempata a sério (2-de-3), ou não é chamado em FAIL e o comentário do ficheiro passa a dizê-lo.

**D4 — O detetor de quarentena não está no caminho principal.** `quarentena.py` correu como análise avulsa. A Fase 0 (`pg_fase0.py` + cálculo de indicadores) continua a exigir série completa e a descartar em silêncio — o defeito que o NVA expôs ainda está no código de produção; só o diagnóstico é que existe. Integrar: todo o ticker sai da Fase 0 com destino PASSA/REPROVA/QUARENTENA.

**D5 — O enriquecimento Finnhub vive em heredocs.** Market cap, 52W high e regime de reporte foram calculados em blocos inline, três versões ligeiramente diferentes ao longo do dia. Não há um módulo com o pacing correcto (1,35 s), retries e fail-closed de `NaN` codificados de uma vez. Foi aqui que o bug de rate limit aconteceu; o remédio ficou na conversa, não no código.

## 3. Riscos estruturais

**R1 — Segurança das chaves (o mais grave).** As cinco chaves estão em texto simples no histórico desta conversa e foram exportadas em comandos bash visíveis no transcript. Verifiquei: nenhum ficheiro em `/mnt/user-data/outputs/` nem nenhum script persistido as contém — mas o transcript basta. **Rodar as cinco chaves continua por fazer e é a acção nº 1.** Em produção: variáveis de ambiente ou secrets do GitHub Actions, nunca no corpo de um prompt.

**R2 — Reprodutibilidade: este ambiente apaga-se.** O filesystem do container reinicia entre sessões. O que está salvo em outputs (scripts e CSVs) sobrevive; a cache Polygon (63 ficheiros, ~78 chamadas) e o estado intermédio **não**. Reconstruir custa ~17 minutos de chamadas dentro do rate limit. O projeto ainda não tem casa própria — repositório, requirements, um `run.py` que encadeie as etapas. Sem isso, cada ciclo recomeça por arqueologia da conversa.

**R3 — Mistura de fontes num mesmo indicador.** `High52_pct` divide um fecho Polygon por um máximo Finnhub. Aceitável, mas é o único indicador híbrido do funil e não está assinalado. Com 64+ sessões descarregadas, o máximo de 52 semanas pode vir a ser calculado só de Polygon (precisa de ~252 sessões; 3,3 h de cache inicial, depois incremental) — até lá, documentar a mistura.

**R4 — Dois funis paralelos sem primazia declarada.** O caminho Finviz (17 finalistas) e o caminho Polygon (21) coexistem. A arquitectura aprovada diz que o Polygon é a descoberta e o Finviz passa a verificação cruzada, mas nenhum documento operacional o fixa — o próximo ciclo pode legitimamente correr qualquer um. Fixar por escrito: Polygon é o funil primário; Finviz corre em paralelo como tripwire de divergência (>2 nomes de diferença não explicada = investigar).

## 4. Dívida por construir (do documento de critérios)

Por ordem de dependência, não de importância:

1. **Gate macro FRED (Phase 0 do teu documento)** — zero chamadas feitas até agora. É gratuito e devia correr antes de tudo.
2. **Fila de continuação** — insider transactions (Finnhub), shelf/ATM (EDGAR full-text). 5 nomes à espera.
3. **Fila de evento** — Marketaux (13 chamadas) + Finnhub news. 13 nomes à espera.
4. **Red flags** — going concern, delisting, reverse splits via EDGAR; equivalente 20-F para CRDL/SNDL/SUPX.
5. **Sinais de descoberta precoce** — nova cobertura de analistas (Finnhub recommendation trends), proxy de hype.
6. **Twelve Data como desempate** — papel definido, nenhuma integração; aceitável adiar.

## 5. O que está genuinamente sólido

O princípio que emergiu três vezes e foi codificado — *dados em falta produzem etiqueta, nunca decisão* — é a peça mais valiosa do dia e está agora em dois sítios (fail-closed de identidade, quarentena de série). A separação descoberta≠validação está codificada e comentada no `pipeline.py`. As decisões de desenho (janela, cotação vs domicílio, evento vs continuação, quarentena) estão registadas em memória com a justificação. A cadeia de evidência do bug Finviz está preservada em `auditoria-finviz-tickers.md` com os HTML brutos como prova.

## 6. Prioridades recomendadas

1. **Rodar as cinco chaves** (fora desta conversa).
2. Consolidar num repositório: os 6 módulos + `run.py` + requirements + os limiares num `config` único (63 sessões *a sério*, corte Eco 1,5, quarentena >3, spread 2%, USD-vol $1M).
3. Integrar quarentena e enriquecimento no caminho principal (resolve D4+D5); corrigir D1 no mesmo passo.
4. Só depois: fases 2–6, começando pelo gate FRED porque condiciona tudo o resto.

---

## Adenda — execução real do pipeline (29-07, segunda passagem)

Correu-se o workflow completo de ponta a ponta para verificar o que a leitura de código não mostra. Tempos: etapa 1 (universo Polygon, cache quente) 11 s e zero chamadas; etapa 2 (indicadores+gates+quarentena) 14 s; etapa 3 (enriquecimento Finnhub) 205 s e 144 chamadas. Reprodutibilidade dos resultados: shortlist 48/48 idêntica, finalistas 21/21 idênticos, drift zero em market cap, 52W high e regime de reporte — determinismo total, mas note-se que só se garante com o mercado fechado; a meio da sessão os valores Finnhub mudam e duas execuções no mesmo dia divergirão.

**E1 — As duas metades do projeto não encaixam (o achado principal).** O gate de identidade `pipeline.resolve()` foi escrito para o funil Finviz e espera a coluna `FinvizCompany`; a saída do funil Polygon traz `Nome`. Testado ao vivo: os três primeiros finalistas Polygon falham todos com "nome diverge (0.00)" — o gate compara a descrição da IBKR com uma string vazia — e o fail-closed aborta o pipeline inteiro. O funil primário aprovado não consegue atravessar o seu próprio validador. Correção: contrato de schema único (`Ticker`,`Nome`) entre etapas.

**E2 — O adaptador IBKR está preso ao funil antigo.** `ibkr_depth.json` cobre os 17 finalistas Finviz; faltam MIST, CRDL, SNDL, SUPX e TLRY — precisamente os nomes que só o funil Polygon encontra. Mesmo com o schema corrigido, cinco candidatos cairiam para o árbitro Yahoo em vez de passarem pelo validador primário. O adaptador tem de ser regenerado a partir da saída do funil corrente, não de uma lista congelada.

**E3 — A etapa 2 não existia como ficheiro.** Confirmado por grep: nenhum módulo produzia a shortlist a partir de `pg_universe.json`; a lógica vivia só em heredocs da conversa. Foi materializada durante esta auditoria (`fase0_indicadores.py`, sem alterações de lógica, preservando deliberadamente o D1 para comparabilidade). Antes disso, "correr o pipeline" era impossível sem arqueologia do transcript.

**E4 — O pipeline não sabe em que dia está.** `trading_days(end="2026-07-28")` está fixo no código. A execução de hoje reproduziu ontem por acaso benigno (mercado ainda fechado); executado esta noite, faria screening sobre dados de anteontem sem qualquer aviso. Falta um guarda: "a última sessão em cache é a última sessão completa do calendário de mercado?" — caso contrário, abortar ou descarregar.

**E5 — Re-executar custa a quota inteira do Finnhub.** Sem cache na etapa 3, cada passagem repete as mesmas 144 chamadas (3,5 min). Dentro do limite de 60/min, mas incompatível com iteração rápida e com a política de reserva de 20-25% do alpha-k-data-pipeline se vier a correr em paralelo com outros workflows. Cache com validade de um dia de mercado resolve.

**E6 — Módulos órfãos com convenções divergentes.** `polygon_phase0.py` (usa `PG_KEY`) e `probe_apis.py` coexistem com `pg_fase0.py` (usa `POLYGON_KEY`) no mesmo directório; e a cache tem nomeação dupla (48 symlinks `g_*.json` → `*.json` criados à mão durante a sessão). Nada disto falha hoje; tudo isto confunde o próximo ciclo. Limpar na consolidação do repositório.

A prioridade nº 3 da lista original ("integrar quarentena e enriquecimento no caminho principal") sobe de âmbito: é integrar as duas metades do pipeline com um contrato de schema, regenerar o adaptador IBKR a partir do funil corrente, e tornar o pipeline consciente do calendário. E1, E2 e E4 bloqueiam qualquer uso não supervisionado.

---

*Ficheiros auditados: finviz_extract.py, validate.py, pipeline.py, pg_fase0.py, fase0_indicadores.py, quarentena.py, ibkr_depth.json, clean_screen.csv, finalists*.csv, pg_*.csv, auditoria-finviz-tickers.md.*
