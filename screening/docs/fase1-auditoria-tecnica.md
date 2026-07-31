# Fase 1 — Auditoria técnica individual

**Data:** 30 de julho de 2026 · **Base:** registo factual da Fase 0 + corridas de 28-07 e 29-07
**Âmbito:** classificação e alteração candidata por critério. Ordenação e dependências ficam para a Fase 2.

## Decisões desbloqueadoras recebidas

| ID | Resolução | Efeito nesta fase |
|---|---|---|
| D1 | Alvo operacional, sem piso, **tecto duro de 10**; menos de 5 exige razão escrita | Critério 13 auditável |
| C2 | **2-3 toques** é a especificação, mas deixa de ser interruptor: contagem vira informação, com tolerância e janela declaradas | Critério 12 auditável |
| C4 | Documento actualizado para **63 sessões**; separar janelas fica PROPOSTA | Critérios 3 e 7 auditáveis |

---

## Critério 1 — Preço $1,00–$7,00

| Campo | Conteúdo |
|---|---|
| **Objectivo original** | Delimitar a faixa de micro/small-cap onde a estratégia opera |
| **Regra actual** | `Price.between(1.0, 7.0)`, inclusivo, sobre o fecho ajustado da última sessão |
| **Tipo de componente** | Hard gate de elegibilidade (construção do universo) |
| **Inputs** | Fecho ajustado da sessão de referência |
| **Fonte actual** | Polygon grouped daily, `adjusted=true` |
| **Evidência** | 8/8 exactos vs Yahoo. 38 excluídos em $0,90-1,00 contra 14 em $7,00-7,10. Na shortlist, 9 entre $1,00-1,50 e 3 entre $6,50-7,00 |
| **Diagnóstico** | O gate funciona e os dados são fiáveis. O que não está tratado é que o limite inferior coincide com o patamar regulatório de delisting da NASDAQ e da NYSE — a densidade junto a $1 não é ruído, é a fronteira de conformidade |
| **Poder discriminatório** | Forte (define o universo) |
| **Qualidade dos dados** | Fiável |
| **Dependências** | Nenhuma. Calculável antes de identidade e corporate actions |
| **Efeito downstream** | Enviesa toda a base para títulos baratos, o que amplifica o defeito do Critério 3 |
| **Estado** | **MANTER + DIVIDIR** |
| **Alteração candidata** | Gate mantido inalterado. Acrescentar **feature** `risco_listagem` ∈ {NENHUM, VIGIAR, ALERTA}: `VIGIAR` se preço < $1,20; `ALERTA` se preço < $1,20 **e** tier ∈ {NasdaqCM, NasdaqGM}. Nunca exclui |
| **Fase de execução** | Universo (gate); enriquecimento (feature, após Critério 4 fornecer o tier) |
| **Dados ausentes** | Preço ausente → o ticker não entra no universo (não é candidato). Tier ausente → `risco_listagem = VIGIAR` no máximo, nunca `ALERTA` |
| **Fonte principal / fallback** | Polygon / Yahoo em caso de divergência >1% |
| **Logging** | `preco_fonte`, `preco_sessao`, `risco_listagem`, `tier_listagem` |
| **Risco** | Falso negativo se a flag for lida como exclusão. Mitigação: nome do campo não contém "excluir" |
| **Teste necessário** | Ablação: distribuição de `risco_listagem` em ≥5 sessões. Verificar contra avisos formais 8-K item 3.01 nos 12 meses seguintes |
| **Critério de aceitação** | A flag não altera a contagem de aprovados em nenhuma sessão. Em ≥3 sessões, `ALERTA` cobre ≥50% dos candidatos que venham a receber item 3.01 |

---

## Critério 2 — Market cap $50M–$500M

| Campo | Conteúdo |
|---|---|
| **Objectivo original** | Restringir a capitalização à faixa onde a ineficiência informacional é maior |
| **Regra actual** | `MCapM = shareOutstanding × preço USD`; gate `between(50, 500)`; Finnhub como comparador; `MCapEstado` ∈ {COERENTE, DIVERGENTE, SEM_COMPARADOR} |
| **Tipo de componente** | Hard gate de elegibilidade + flag de proveniência |
| **Inputs** | Acções em circulação, preço |
| **Fonte actual** | `shareOutstanding` do Finnhub `profile2` |
| **Evidência** | 22/67 (33%) DIVERGENTE. TOP: $78M real vs $1.305M Finnhub. AMIX: $52M vs $2,5M. **NKLR: SEC 110,5M acções vs Finnhub 70,3M — o cálculo dá $344M e o real é $540M, acima do tecto.** Yahoo não devolve market cap para esta população |
| **Diagnóstico** | O P2 corrigiu moeda e valores congelados. **Não corrigiu a fonte das acções**: quando `shareOutstanding` está desactualizado, o cálculo erra na mesma direcção. Uma taxa de divergência de 33% não é ruído — é defeito sistémico da fonte |
| **Poder discriminatório** | Forte (32 de 67) |
| **Qualidade dos dados** | **Condicional** — depende de um campo demonstradamente desactualizado |
| **Dependências** | Preço validado (Critério 1). Deve correr **depois** de corporate actions: um split altera acções em circulação |
| **Efeito downstream** | Erro junto à fronteira inverte a elegibilidade. TOI a 1% do tecto em 28-07 |
| **Estado** | **ALTERAR fonte** (decisão A9, ainda não implementada) |
| **Alteração candidata** | Acções em circulação da SEC XBRL `companyconcept/dei:EntityCommonStockSharesOutstanding`. Regras obrigatórias: (a) usar o facto com `end` mais recente; (b) somar todas as classes distintas do mesmo CIK uma única vez por `end`, nunca acumular `end` diferentes; (c) se houver múltiplos valores no mesmo `end`, usar o do `accn` mais recente; (d) `freshness` máxima 120 dias — acima disso `MCapEstado = DESACTUALIZADO`; (e) fallback Finnhub apenas quando a SEC não devolver facto, com `MCapEstado = FALLBACK` |
| **Fase de execução** | Enriquecimento, após corporate actions |
| **Dados ausentes** | SEC ausente e Finnhub ausente → `DATA_INSUFFICIENT`, candidato para quarentena, **nunca aprovado nem reprovado** |
| **Fonte principal / fallback** | SEC XBRL / Finnhub `profile2` |
| **Logging** | `shares_fonte`, `shares_end`, `shares_accn`, `shares_idade_dias`, `MCapM`, `MCapFinnhubM`, `MCapDivergenciaPct`, `MCapEstado` |
| **Risco** | Emissores estrangeiros (20-F) podem não publicar este facto → aumento de `FALLBACK` na população já frágil. Custo: 1 chamada/candidato, sem chave |
| **Teste necessário** | Ablação de fonte sobre os 22 DIVERGENTE de 29-07: quantos passam a COERENTE. Verificar NKLR passa a $540M e é excluído. Medir taxa de `FALLBACK` por `regime_reporte` |
| **Critério de aceitação** | Taxa de DIVERGENTE < 5% da shortlist. NKLR excluído. Zero candidatos aprovados com `MCapEstado ∈ {DESACTUALIZADO, DATA_INSUFFICIENT}` |

---

## Critério 3 — Volume médio > 100.000 acções

| Campo | Conteúdo |
|---|---|
| **Objectivo original** | Garantir liquidez suficiente para entrar e sair |
| **Regra actual** | `AvgVolN > 100_000`, média de 63 sessões excluindo a corrente |
| **Tipo de componente** | Hard gate de elegibilidade — **incompleto** |
| **Inputs** | Série de volume |
| **Fonte actual** | Polygon |
| **Evidência** | Desvio 0,1% vs Yahoo. **15/67 abaixo de $1M/dia**: JBDI $0,15M, JAGU $0,17M, WIMI $0,22M, USIO $0,26M. CRDL e DCX passam com 5,4× e 5,8× de margem em acções e ficam nos $0,62-0,63M. `MIN_USD_VOL_90D = $1M` declarado no config e nunca aplicado |
| **Diagnóstico** | Medir liquidez em unidades e não em valor premia sistematicamente os títulos mais baratos — e o Critério 1 já enviesa a base para o limite inferior de preço. Os dois defeitos reforçam-se. Um gate que aprova o JBDI a $150k/dia não está a cumprir o seu objectivo declarado |
| **Poder discriminatório** | Moderado em acções; o eixo em valor está inactivo |
| **Qualidade dos dados** | Fiável |
| **Dependências** | Série íntegra (quarentena) e ajustada a splits |
| **Efeito downstream** | Candidatos ilíquidos consomem enriquecimento e quota, e produzem teses inexecutáveis |
| **Estado** | **DIVIDIR** em dois gates independentes |
| **Alteração candidata** | Gate A: `AvgVolShares_63 > 100_000` (inalterado). Gate B: `AvgVolUSD_63 = média(volume × fecho) > $1.000.000`. Ambos duros. Guardar também `MedVolShares_63` (ver Critério 7). **PROPOSTA separada, não implementar nesta fase:** janela curta (20 sessões) para liquidez e longa (63) para anormalidade |
| **Fase de execução** | Universo, imediatamente após o Critério 1 — é o filtro mais barato que evita enriquecimento |
| **Dados ausentes** | Série mais curta que 64 sessões → quarentena `SERIE_CURTA`, não reprovação |
| **Fonte principal / fallback** | Polygon / nenhum (não misturar fontes de volume — ver SUPERSEDED S3) |
| **Logging** | `AvgVolShares_63`, `AvgVolUSD_63`, `MedVolShares_63` |
| **Risco** | Falso negativo em títulos genuinamente investíveis a preço baixo. Medir: 15 removidos em 29-07 (22% da shortlist) |
| **Teste necessário** | Ablação com e sem o Gate B em ≥3 sessões. Confirmar que nenhum candidato removido tinha `RVOL ≥ 3×` **e** compra de insider — se tiver, o limiar de $1M é demasiado alto |
| **Critério de aceitação** | Zero aprovados abaixo de $1M/dia. Redução da shortlist ≤30%. Nenhum candidato com insider P + RVOL≥3 removido |

---

## Critério 4 — NYSE / NASDAQ / AMEX

| Campo | Conteúdo |
|---|---|
| **Objectivo original** | Excluir OTC e pink sheets |
| **Regra actual** | `type == "CS"` **e** `exch ∈ {XNAS, XNYS, XASE}` (P5) |
| **Tipo de componente** | Hard gate de construção do universo |
| **Inputs** | Tipo de instrumento, bolsa primária |
| **Fonte actual** | Polygon `/v3/reference/tickers` |
| **Evidência** | 67/67 validados vs Yahoo. Zero OTC. Distribuição: 28 NasdaqCM, 13 NasdaqGS, 11 NYSE, 10 NasdaqGM, 5 NYSE American. Efeito directo do P5: remove 1 (CBOE) |
| **Diagnóstico** | Gate correcto e agora explícito. O achado é o **tier**: 38 dos 67 nos dois tiers inferiores da NASDAQ, onde os requisitos de manutenção de listagem são mais baixos. O tier não está capturado em lado nenhum |
| **Poder discriminatório** | Nulo como gate (1 em 5.300) — mas é uma garantia estrutural, não um filtro |
| **Qualidade dos dados** | Fiável |
| **Dependências** | Nenhuma |
| **Efeito downstream** | Fornece o `tier_listagem` que o Critério 1 precisa para a flag `ALERTA` |
| **Estado** | **MANTER + acrescentar feature** |
| **Alteração candidata** | Gate inalterado. Extrair `tier_listagem` ∈ {NasdaqGS, NasdaqGM, NasdaqCM, NYSE, NYSEAmerican} como **feature**. Não é gate: não está demonstrado que o tier preveja nada |
| **Fase de execução** | Universo |
| **Dados ausentes** | `exch` ausente → ticker não entra no universo. `tier` ausente → feature `DESCONHECIDO` |
| **Fonte principal / fallback** | Polygon `primary_exchange` / `fullExchangeName` do Yahoo (é este que dá a granularidade CM/GM/GS) |
| **Logging** | `type`, `exch`, `tier_listagem`, `tier_fonte` |
| **Risco** | Nenhum material. Custo: o tier granular exige 1 chamada Yahoo por candidato |
| **Teste necessário** | Verificar em ≥3 sessões que 100% dos candidatos têm `tier_listagem` resolvido |
| **Critério de aceitação** | Zero OTC em qualquer corrida. `tier_listagem` resolvido em ≥95% dos candidatos |

---

## Critério 5 — RSI(14) entre 25 e 60

| Campo | Conteúdo |
|---|---|
| **Objectivo original** | Evitar extremos de sobrecompra |
| **Regra actual** | `RSI.between(25, 60)`, Wilder, semente = média simples das primeiras 14 diferenças, sobre a série disponível |
| **Tipo de componente** | Hard gate declarado bilateral; na prática unilateral |
| **Inputs** | Série de fechos |
| **Fonte actual** | Polygon |
| **Evidência** | 28-07: 19 cortados acima de 60, 2 abaixo de 25. 29-07: **9 acima de 60, 0 abaixo de 25**. Baixar o piso de 25 para 20 não altera a shortlist em nenhuma das sessões. Convergência de Wilder: desvio mediano de 1,9 pontos e máximo de 5,0 entre séries de 30 e 71 sessões |
| **Diagnóstico** | O tecto discrimina; o piso não. Duas sessões não bastam para o declarar inútil, mas bastam para o retirar da categoria de gate activo. Problema separado e mais sério: **a janela do RSI é implícita** — usa toda a série disponível, que hoje são 71 sessões e amanhã serão 72. Com 9 candidatos entre 55 e 65, um desvio de 5 pontos é decisivo |
| **Poder discriminatório** | Tecto: moderado. Piso: **nulo em 2 sessões** |
| **Qualidade dos dados** | Fiável, mas **não reprodutível** por falta de janela fixa |
| **Dependências** | Série íntegra e ajustada |
| **Efeito downstream** | O Sinal B (Critério 9) mede reversão de oversold; o piso do RSI interage com essa população |
| **Estado** | **DIVIDIR + formalizar** |
| **Alteração candidata** | (a) **Fixar a janela em 63 sessões** no `config`, explícita. (b) Tecto `RSI ≤ 60` permanece **gate duro**. (c) Piso passa a **feature** `rsi_zona` ∈ {OVERSOLD (<25), BAIXO (25-40), MEDIO (40-55), ALTO (55-60)} — não exclui. (d) Registar `rsi_janela_sessoes` na saída |
| **Fase de execução** | Indicadores técnicos |
| **Dados ausentes** | Série < 64 sessões → `DATA_INSUFFICIENT`, quarentena |
| **Fonte principal / fallback** | Polygon / nenhum — indicadores derivados nunca vêm de fonte externa |
| **Logging** | `RSI`, `rsi_janela_sessoes`, `rsi_zona` |
| **Risco** | Remover o piso admite candidatos em queda severa. Mitigação: o Critério 6 e o P4 cobrem esse flanco por vias independentes |
| **Teste necessário** | Ablação em ≥5 sessões: contagem de aprovados com piso 25, piso 20 e sem piso. Recalcular o RSI com janela fixa e medir a divergência face ao actual |
| **Critério de aceitação** | Janela fixa produz RSI reprodutível entre corridas (desvio zero para a mesma data). Remover o piso altera a shortlist em ≤5% nas sessões testadas — se alterar mais, o piso volta a gate |

---

## Critério 6 — Preço vs SMA20 > −15%

| Campo | Conteúdo |
|---|---|
| **Objectivo original** | Evitar candidatos demasiado estendidos para baixo |
| **Regra actual** | `(preço / média(20 fechos) − 1) × 100 > −15` |
| **Tipo de componente** | Hard gate unilateral |
| **Inputs** | Série de fechos |
| **Fonte actual** | Polygon |
| **Evidência** | 28-07: corta 28 de 78. 29-07: **corta 32 de 99** — o mais discriminatório do funil. Sensibilidade: −20%→81, −15%→67, −10%→52. Sobreposição com RSI: 14; exclusivos SMA20: 32; exclusivos RSI: 9. **DCX passa a +18,9% com RVOL 18,7× e +71% em três sessões partindo do mínimo de 60 dias. VRRM passa a +20,3% com RVOL 3,8× num título líquido** |
| **Diagnóstico** | O gate funciona e não é redundante. O flanco aberto é o lado de cima: nada trava um candidato que já subiu violentamente. O RSI com tecto em 60 cobre parcialmente, mas o DCX mostra que não cobre — a queda anterior deprime o RSI e o salto não o levanta o suficiente |
| **Poder discriminatório** | **Forte**, e o mais sensível a calibração de todos |
| **Qualidade dos dados** | Fiável |
| **Dependências** | Série íntegra e ajustada |
| **Efeito downstream** | Concentra o Sinal B (ver Critério 9) |
| **Estado** | **MANTER + acrescentar flag** |
| **Alteração candidata** | Gate `> −15%` inalterado. Acrescentar **flag** `extensao` ∈ {NORMAL, ESTENDIDO, SALTO_DE_FUNDO}: `ESTENDIDO` se desvio > +15%; `SALTO_DE_FUNDO` se desvio > +15% **e** preço a menos de 25% do mínimo de 60 sessões. Nunca exclui |
| **Fase de execução** | Indicadores técnicos |
| **Dados ausentes** | Série < 20 sessões → `DATA_INSUFFICIENT` |
| **Fonte principal / fallback** | Polygon / nenhum |
| **Logging** | `SMA20_pct`, `extensao`, `dist_min60_pct` |
| **Risco** | O limiar de +15% e os 25% do mínimo derivam de **dois casos** (DCX, VRRM). Risco de overfitting **médio** — assumido explicitamente. Por isso é flag e não gate |
| **Teste necessário** | Ablação em ≥5 sessões: prevalência de `ESTENDIDO` e `SALTO_DE_FUNDO`. Testar limiares +10/+15/+20/+25%. Verificar se `SALTO_DE_FUNDO` separa consistentemente títulos com máximo de 60 dias >2× o preço actual |
| **Critério de aceitação** | `SALTO_DE_FUNDO` dispara em <5% dos candidatos. Prevalência de `ESTENDIDO` estável (±5pp) entre sessões. Se `SALTO_DE_FUNDO` nunca disparar em 5 sessões, a flag é removida por inutilidade |

---

## Critério 7 — Volume relativo > 1,2×

| Campo | Conteúdo |
|---|---|
| **Objectivo original** | Detectar actividade anormal |
| **Regra actual** | `RVOL = volume_hoje / média(volume das 63 sessões anteriores)`; gate `> 1,2` |
| **Tipo de componente** | Hard gate de elegibilidade |
| **Inputs** | Série de volume |
| **Fonte actual** | Polygon |
| **Evidência** | Reduz 933→122 (29-07) e 940→111 (28-07) — **o gate que define o funil**. Mediana do universo: 0,51 (28-07) e 0,59 (29-07). 26/67 entre 1,2 e 1,5. 23 cumprem RVOL≥2 e **44 tiveram pico ≥2× nos últimos 20 dias**. **AMIX: RVOL 171×, média 63s de 408.244 acções e mediana de 10.814 — divergência de 38×** |
| **Diagnóstico** | Três problemas distintos. (i) A média representa mal séries assimétricas: o AMIX passa também o Critério 3 por causa da mesma média inflacionada. (ii) O denominador exclui a sessão corrente — correcto, mas nunca formalizado. (iii) "Actividade hoje" e "actividade recente" são conceitos diferentes e o gate só mede o primeiro, enquanto o Sinal A do documento mede algo mais próximo do segundo |
| **Poder discriminatório** | **Muito forte** |
| **Qualidade dos dados** | Fiável na medição, **semanticamente frágil** na agregação |
| **Dependências** | Série íntegra, ajustada a splits, **e corporate actions já verificadas** — o AMIX prova que um split recente contamina a interpretação mesmo com volumes ajustados |
| **Efeito downstream** | Determina a composição de tudo a jusante; alimenta o rácio Eco (A4) |
| **Estado** | **MANTER + DIVIDIR + flag** |
| **Alteração candidata** | (a) Gate `RVOL_sessao > 1,2` inalterado, com denominador formalizado como *média das 63 sessões anteriores, excluindo a corrente*. (b) Nova **feature** `RVOL_pico_20 = max(volume das últimas 20 sessões) / média_63` — dá corpo ao Sinal A reformulado (R6). (c) **Flag** `volume_assimetrico` se `média_63 / mediana_63 > 5`. (d) Registar `MedVolShares_63` |
| **Fase de execução** | Indicadores técnicos, **depois** de corporate actions |
| **Dados ausentes** | Série < 64 sessões → `DATA_INSUFFICIENT` |
| **Fonte principal / fallback** | Polygon / nenhum |
| **Logging** | `RVOL_sessao`, `RVOL_pico_20`, `AvgVol_63`, `MedVol_63`, `volume_assimetrico` |
| **Risco** | O limiar de 5× na assimetria vem de **um caso** (R4, risco médio). Por isso é flag. Não alterar o gate de 1,2× sem ablação: é o componente com maior efeito estrutural |
| **Teste necessário** | Ablação em ≥5 sessões: prevalência de `volume_assimetrico` e testar limiares 3×/5×/10×. Medir se `RVOL_pico_20 ≥ 2` reconcilia o Sinal A (44 vs 23 em 29-07). Confirmar que o AMIX é apanhado por `volume_assimetrico` |
| **Critério de aceitação** | `volume_assimetrico` dispara em 3-15% dos candidatos (se <3% é inútil, se >15% não discrimina). AMIX etiquetado. Gate de 1,2× inalterado até haver ≥5 sessões de dados |

---

## Critério 8 — Não estar acima de 90% do máximo de 52 semanas

| Campo | Conteúdo |
|---|---|
| **Objectivo original** | Evitar comprar no topo do range anual |
| **Regra actual** | `High52_pct = (preço / High52 − 1) × 100 ≤ −10` |
| **Tipo de componente** | Hard gate declarado |
| **Inputs** | Máximo de 52 semanas |
| **Fonte actual** | Finnhub `stock/metric` |
| **Evidência** | 28-07: corta 3 de 50. 29-07: **corta 1 de 67 (CCO), e 0 em exclusivo** — não removeu nenhum candidato que já não fosse removido por outro gate. Mediana da shortlist: −54,7% abaixo do máximo. **Dados inválidos:** mínimo do EU ($1,60) **acima** do preço ($1,06); HCTI 1.225 vs 612 no Yahoo (factor 2); BRAI 99 vs 33 (factor 3); YYGH 5.175 vs 3.900. DCX com máximo de $3.408 e preço de $1,08 |
| **Diagnóstico** | Contribuição marginal **zero** em 29-07 e quase zero em 28-07. Os outros gates já garantem que nada está perto do topo. Pior: a fonte é inválida para a população pós-reverse-split, e **o P4 depende exactamente destes dados** — o EU foi excluído com um input impossível. "Ajustado aritmeticamente" não é "válido para o sinal" |
| **Poder discriminatório** | **Nulo** |
| **Qualidade dos dados** | **Inadequada** |
| **Dependências** | Corporate actions — o range só é interpretável relativamente ao último split |
| **Efeito downstream** | Alimenta o P4 (Critério 11), que é uma exclusão estrutural. Um input inválido produz exclusões corretas por acidente |
| **Estado** | **CONVERTER de gate para feature + REPARAR fonte** |
| **Alteração candidata** | (a) Deixa de ser gate: `High52_pct` passa a **feature**. (b) Máximo e mínimo calculados do OHLCV Polygon (`adjusted=true`) sobre 252 sessões, coerente com o resto do funil. (c) **Janela truncada no último corporate action**: se houve split nos 252 dias, o range começa no dia seguinte e `range_janela_sessoes` regista o comprimento efectivo. (d) Se `range_janela_sessoes < 60`, `range_estado = DATA_INSUFFICIENT` e o P4 **não** pode decidir sobre esse candidato |
| **Fase de execução** | Indicadores técnicos, depois de corporate actions |
| **Dados ausentes** | `DATA_INSUFFICIENT` → o P4 não avalia; candidato fica em revisão |
| **Fonte principal / fallback** | Polygon OHLCV calculado / Finnhub `metric` apenas como comparador |
| **Logging** | `High52`, `Low52`, `range_fonte`, `range_janela_sessoes`, `range_truncado_por_split`, `range_estado`, `High52_finnhub`, `range_divergencia_pct` |
| **Risco** | Custo: ~252 sessões em cache, 3,3 h de descarga inicial a 13 s/chamada, depois incremental. Remover o gate admite candidatos perto do máximo — hoje 1 candidato (CCO) |
| **Teste necessário** | Recalcular o range dos 67 candidatos de 29-07 do OHLCV e comparar com o Finnhub. Verificar que o mínimo nunca é superior ao preço. Reavaliar o P4 com os dados corrigidos e comparar a lista de 6 excluídos |
| **Critério de aceitação** | Zero casos de mínimo > preço. Divergência vs Finnhub explicável por split em 100% dos casos. O P4 sobre dados corrigidos produz uma lista de exclusão justificável candidato a candidato |

---

## Critério 9 — Pelo menos um sinal A/B/C

| Campo | Conteúdo |
|---|---|
| **Objectivo original** | Exigir evidência de momentum, reversão ou acumulação |
| **Regra actual** | **Não implementada.** Os oito sub-sinais são calculáveis mas nenhuma regra os exige |
| **Tipo de componente** | Gate declarado no documento; hoje é feature latente |
| **Inputs** | Séries de fecho e volume |
| **Fonte actual** | Polygon |
| **Evidência** | **SOUN aprovado sem nenhum sinal** (29-07); em 28-07 não havia nenhum caso. Sinal B: 21,1% na base pós-preço-volume vs **28,4%** pós-gates; RSI-oversold 4,5%→14,9%; bounce 7,5%→16,4%. Consolidação lateral: 40/67 (60%) em 29-07 e 17/21 (81%) em 28-07. 58/67 com ≥2 sinais; após red flags, ≥2 sinais reduz 27→26 |
| **Diagnóstico** | A regra é barata e agora tem um caso que a justifica. Dois problemas de qualidade: (i) a **consolidação lateral** (amplitude <1,6× em 60 sessões) dispara em 60-81% — um teste que a maioria passa não discrimina, e é a via única de qualificação de vários candidatos; (ii) o critério "≥2 sinais" perdeu poder com base maior (reduz 27→26), pelo que não serve como gate |
| **Poder discriminatório** | `≥1 sinal`: desconhecido (1 caso em 2 sessões). `≥2 sinais`: **fraco** |
| **Qualidade dos dados** | Fiável |
| **Dependências** | Todos os indicadores técnicos. **Confirmado que corre depois dos gates técnicos** (S1 SUPERSEDED) |
| **Efeito downstream** | Alimenta a classificação de setups e a ordenação (Critério 13) |
| **Estado** | **IMPLEMENTAR `≥1` como gate; CONVERTER `≥2` em confirmação** |
| **Alteração candidata** | (a) Gate: `A ∨ B ∨ C` obrigatório. (b) `n_sinais ≥ 2` passa a **nível de confirmação** usado na classificação, não na elegibilidade. (c) **Sinal A reformulado** (R6): `RVOL_pico_20 ≥ 2` em vez de `RVOL_sessao ≥ 2` — reconcilia gate e sinal. (d) Consolidação lateral: **não apertar para 1,3× nesta fase** (R9, overfitting alto); em vez disso, exigir que o Sinal C se qualifique por **≥2 dos 3 componentes** (lateral, higher lows, coiling), o que remove a via única sem escolher um limiar novo |
| **Fase de execução** | Sinais, após todos os gates técnicos |
| **Dados ausentes** | Qualquer sub-sinal não calculável → `False` **e** registo em `sinais_nao_calculaveis`. Se ≥2 dos 3 sinais forem não calculáveis → `DATA_INSUFFICIENT` |
| **Fonte principal / fallback** | Polygon / nenhum |
| **Logging** | oito sub-sinais booleanos, `A`, `B`, `C`, `n_sinais`, `sinais_nao_calculaveis` |
| **Risco** | A alteração (d) é uma regra nova sem evidência directa — mas evita escolher um limiar para produzir prevalência desejada, que era o defeito do R9. Prevalência esperada do C cai; medir |
| **Teste necessário** | Ablação em ≥5 sessões: quantos aprovados perde o gate `≥1`. Prevalência do C com regra actual vs "≥2 componentes". Confirmar que o SOUN é excluído |
| **Critério de aceitação** | SOUN excluído. Gate `≥1` remove 0-10% dos candidatos (se >10%, é gate a sério e exige revisão). Sinal C com prevalência entre 20% e 50% |

---

## Critério 10 — Tier 1 / Tier 2 sectorial

| Campo | Conteúdo |
|---|---|
| **Objectivo original** | Priorizar sectores com maior potencial de re-rating |
| **Regra actual** | Não implementada. `Industria` é recolhida e nunca usada |
| **Tipo de componente** | Filtro de priorização declarado |
| **Inputs** | Classificação sectorial |
| **Fonte actual** | Finnhub `finnhubIndustry` |
| **Evidência** | Biotech/pharma: **67% da shortlist em 28-07, 37% em 29-07**, contra 31% no universo elegível. 23 indústrias distintas em 67 candidatos (29-07). **Software/cibersegurança: zero nas duas sessões. Semicondutores: zero.** Clean energy: 3. Space/aero: 1 (BYRN, que é defesa) |
| **Diagnóstico** | A hipótese de enviesamento estrutural **não se confirmou** (S2 SUPERSEDED) — 67% assentava em 21 observações. Aplicar Tier 1 removeria 39 dos 67 e concentraria a lista em biotech, agravando o que devia corrigir. E dois dos quatro Tier 1 do documento são **inacessíveis por construção**: não existem praticamente empresas de software ou semicondutores nos EUA a $1-7 com $50-500M de capitalização |
| **Poder discriminatório** | Não aplicado. Como filtro, seria **negativo** para o objectivo |
| **Qualidade dos dados** | Fiável, mas taxonomia inadequada ao universo |
| **Dependências** | Enriquecimento Finnhub |
| **Efeito downstream** | Hoje entra na prioridade 1 e 3 do Critério 13 como "sector prioritário" — funciona como proxy parcial de biotech |
| **Estado** | **REMOVER como filtro; MANTER como observabilidade** |
| **Alteração candidata** | (a) Nenhum gate nem filtro sectorial. (b) Métrica de observabilidade por corrida: `concentracao_top_sector_pct` e `n_industrias`. (c) **Flag** `concentracao_elevada` se um único sector >50% da shortlist. (d) Retirar "sector prioritário" das regras de prioridade do Critério 13 até ser demonstrado valor marginal independente. (e) Reavaliar a taxonomia do documento contra o universo realmente elegível |
| **Fase de execução** | Observabilidade, pós-shortlist |
| **Dados ausentes** | `Industria` ausente → `DESCONHECIDO`, conta para `n_industrias` como categoria própria |
| **Fonte principal / fallback** | Finnhub / SIC code da SEC |
| **Logging** | `Industria`, `industria_fonte`, `concentracao_top_sector_pct`, `n_industrias`, `concentracao_elevada` |
| **Risco** | Perde-se a intenção original de priorizar temas. Contra-argumento: a intenção não é satisfazível neste universo |
| **Teste necessário** | Medir `concentracao_top_sector_pct` em ≥5 sessões. Testar se "sector Tier 1" tem valor marginal na ordenação, isolando-o das outras condições |
| **Critério de aceitação** | A métrica existe e é registada. Se em 5 sessões a concentração exceder 50% em ≥3, a hipótese S2 é reaberta |

---

## Critério 11 — Red flags

| Campo | Conteúdo |
|---|---|
| **Objectivo original** | Excluir empresas com risco estrutural incompatível |
| **Regra actual** | 4 de 6 implementadas: delisting (8-K item 3.01), going concern (3 estados), reverse split (P3, Polygon), volume <50k (coberto por gate mais exigente), OTC (coberto pelo Critério 4), queda >80% sem recuperação (P4) |
| **Tipo de componente** | Exclusão estrutural + corporate action (mal posicionada) |
| **Inputs** | Filings SEC, itens de 8-K, registo de splits, range de 52 semanas |
| **Fonte actual** | EDGAR + Polygon splits + Finnhub metric |
| **Evidência** | 3 reprovados de 32: **PYPD** going concern, **NKLR** item 3.01, **AMIX** split 21:1 de 24-06. P4 excluiu 6 (TLRY, BRAI, XXI, HCTI, UPB, EU), dos quais **3 em exclusivo** (EU, TLRY, UPB). ABEO e ACB em `FALHA_REDE`, corretamente não aprovados. **A SEC devolveu 503 e o backoff de 5 tentativas esgotou-se; à mão veio 200 imediato.** O split do AMIX foi detectado na etapa 9, depois de o candidato ter consumido indicadores, enriquecimento Finnhub e chamadas EDGAR |
| **Diagnóstico** | As exclusões funcionam e o fail-closed funciona. Dois defeitos: (i) **posição** — corporate actions são a dependência mais a montante de todo o pipeline (contaminam volume, RSI, range) e correm em último; (ii) **o P4 depende da fonte menos fiável** (Critério 8) e excluiu o EU com um mínimo acima do preço |
| **Poder discriminatório** | Forte |
| **Qualidade dos dados** | Mista: itens de 8-K exactos (código, não texto); going concern robusto após distinguir avaliação de conclusão; range **inadequado** |
| **Dependências** | Identidade resolvida (CIK). Nada mais |
| **Efeito downstream** | Determina os aprovados |
| **Estado** | **MOVER corporate actions + REVALIDAR P4 + completar** |
| **Alteração candidata** | (a) **Reverse splits movidos para a construção do universo**: uma chamada por corrida, sobre o universo inteiro, antes de qualquer indicador. Candidato com split nos últimos 90 dias → excluído; entre 90 e 365 dias → flag `split_recente` e o range é truncado (Critério 8). (b) P4 recalculado sobre o range Polygon; até lá, P4 sobre `range_estado = DATA_INSUFFICIENT` **não decide**. (c) Backoff da SEC: 8 tentativas, até 60 s, com jitter. (d) Formalizar os 6 red flags numa tabela única com `politica_de_falha` explícita por item |
| **Fase de execução** | Corporate actions: universo. Red flags de filings: após shortlist (são caros) |
| **Dados ausentes** | Splits indisponíveis → `VERIFICACAO_INCOMPLETA`, ninguém aprovado (fail-closed, já implementado). EDGAR indisponível → `FALHA_REDE`, não aprovado |
| **Fonte principal / fallback** | Polygon splits / nenhum. EDGAR / nenhum |
| **Logging** | por red flag: `estado`, `fonte`, `data_evento`, `politica_de_falha_aplicada` |
| **Risco** | Excluir por split nos últimos 90 dias é uma regra nova: mede-se quantos remove. Custo de mover splits para o universo: **−1 chamada** (deixa de ser por candidato) |
| **Teste necessário** | Ablação de posição: AMIX é removido antes de consumir enriquecimento? Contar chamadas poupadas. Recalcular P4 com range corrigido e comparar os 6 excluídos. Injectar 503 e confirmar que o backoff resiste |
| **Critério de aceitação** | AMIX excluído na fase de universo. Chamadas Finnhub reduzidas proporcionalmente aos candidatos com split. Zero exclusões do P4 assentes em `range_estado ≠ OK`. 503 simulado não interrompe a corrida |

---

## Critério 12 — Sinais de descoberta precoce

| Campo | Conteúdo |
|---|---|
| **Objectivo original** | Bonus para candidatos ainda não descobertos |
| **Regra actual** | 2 de 5 implementados: insider buying (P1, código P, 30 dias) e proximidade de breakout. Cobertura de analistas devolve `None`. Menções sociais e partnerships sem fonte |
| **Tipo de componente** | Features (bonus declarado) |
| **Inputs** | Form 4, série de fechos, ratings, notícias |
| **Fonte actual** | Finnhub insider-transactions; Polygon OHLCV |
| **Evidência** | **BYRN: 12 compras, 109.137 acções, zero vendas** (e 96.987 em 28-07 — repetido em duas sessões). **HDSN: 7 compras, 834.986 acções, zero vendas.** 23 transacções A/M corretamente ignoradas. **SEER marcado perto de breakout com 4 toques**, quando a especificação diz 2-3. Cobertura de analistas: `None` em 27/27. **24 dos 27 aprovados com zero sinais.** 6 com shelf ou oferta activa |
| **Diagnóstico** | O P1 é a correcção de maior impacto qualitativo: sem ela, PMVP e SIGA apareciam como insiders compradores tendo comprado zero. O breakout tem discrepância entre código (2-8) e especificação (2-3) — resolvida pela decisão C2. Mais candidatos com risco de diluição (6) do que com compra de insider (2) |
| **Poder discriminatório** | Como features: **fraco em cobertura** (2 de 27) — mas isso é informação, não defeito |
| **Qualidade dos dados** | Insiders: condicional (Form 4 é declaração, `change` inclui derivados — mitigado pelo filtro de código). Analistas: **indisponível**. Sociais: indisponível |
| **Dependências** | Identidade resolvida; shortlist definida (são chamadas caras) |
| **Efeito downstream** | Alimenta a ordenação (Critério 13) |
| **Estado** | **MANTER como features + corrigir breakout + formalizar ausências** |
| **Alteração candidata** | (a) Breakout deixa de ser booleano: expor `resistencia`, `toques`, `dist_resistencia_pct`, `toque_tolerancia_pct` (2%) e `resistencia_janela_sessoes` (60), todos declarados no `config`. A condição "2-3 toques" fica registada como **referência da especificação**, não como filtro. (b) `nova_cobertura` permanece `None` — proibido converter em `False`; expor `cobertura_estado = SEM_FONTE`. (c) Menções sociais e PDUFA registados como `SEM_FONTE`, não como ausência de sinal. (d) Manter as quatro features separadas: insider, breakout, cobertura, risco de oferta. Nenhuma agrega em score |
| **Fase de execução** | Enriquecimento pós-shortlist |
| **Dados ausentes** | `SEM_FONTE` distinto de `SEM_SINAL` distinto de `FALHA_REDE`. Nunca colapsar |
| **Fonte principal / fallback** | Finnhub insider / EDGAR Form 4 directo. Analistas: nenhuma |
| **Logging** | `insider_compras_P_30d`, `accoes_compradas_P`, `transaccoes_AM_ignoradas`, `janela_insider_desde`, campos de breakout acima, `cobertura_estado`, `formularios_diluicao` |
| **Risco** | Expor 4 números de breakout em vez de um booleano transfere julgamento para o utilizador. É intencional |
| **Teste necessário** | Verificar em ≥5 sessões que `None` nunca vira `False`. Confirmar que os candidatos com insider P são um subconjunto estável. Medir prevalência de `risco_diluicao` |
| **Critério de aceitação** | Zero ocorrências de `nova_cobertura = False`. Todos os campos de breakout presentes quando `dist_resistencia_pct` é calculável. Prevalência de insider P entre 5% e 30% dos aprovados |

---

## Critério 13 — Selecção final e ordenação

| Campo | Conteúdo |
|---|---|
| **Objectivo original** | Entregar 5-10 candidatos ordenados por prioridade |
| **Regra actual** | Filtro `≥2 sinais`; quatro níveis de prioridade; **desempate por RVOL introduzido em execução e não especificado** |
| **Tipo de componente** | Regra de prioridade + desempate |
| **Inputs** | Sinais A/B/C, tier sectorial, insider, breakout |
| **Fonte actual** | derivada |
| **Evidência** | `≥2 sinais` reduz 27→26. **Ordem original: 12 no escalão 1, zero no 2, zero no 3, 14 no residual.** Ordem invertida: BYRN no 1, SEER no 2, 10 no 3, **14 no residual**. Oito dos dez do escalão 3 são saúde/biotech/pharma. Catalisadores pendentes não implementados |
| **Diagnóstico** | A ordem original colapsa nas duas sessões porque a prioridade 1 ("volume spike + sector prioritário") é a intersecção de duas condições muito comuns. A inversão aumenta a especificidade mas **não corrige a taxonomia**: 14 de 26 continuam sem classificação, e o desempate residual é feito por um critério que ninguém especificou. E "sector prioritário" funciona como proxy de biotech (Critério 10) |
| **Poder discriminatório** | Nulo enquanto taxonomia |
| **Qualidade dos dados** | n/a |
| **Dependências** | Todos os critérios anteriores |
| **Efeito downstream** | É a saída do sistema |
| **Estado** | **TESTAR — não promover R10 nesta fase** |
| **Alteração candidata** | (a) `≥2 sinais` deixa de ser filtro; passa a `nivel_confirmacao` ∈ {1, 2, 3}. (b) **Tecto duro de 10** (decisão D1); se houver mais de 10 elegíveis, o corte é pela ordenação e o excedente vai para `saida_reserva.csv` com a razão. (c) Menos de 5 → campo `razao_lista_curta` obrigatório. (d) Retirar "sector prioritário" das regras de prioridade (Critério 10). (e) **R10 permanece PROPOSTA**: a inversão é testada em shadow run, não promovida — restrição 4.3, o BYRN esteve no topo em ambas as sessões. (f) O desempate por RVOL é **removido** até haver especificação; até lá, empates ficam empatados e a ordem é alfabética, declaradamente arbitrária e assinalada como tal |
| **Fase de execução** | Ordenação, última |
| **Dados ausentes** | Candidato sem features suficientes para classificar → escalão residual com `classificacao_estado = DATA_INSUFFICIENT` |
| **Fonte principal / fallback** | derivada / n/a |
| **Logging** | `escalao`, `regra_aplicada`, `nivel_confirmacao`, `desempate_aplicado`, `razao_lista_curta`, `classificacao_estado` |
| **Risco** | O escalão residual com 54% dos candidatos permanece. Esta fase **não resolve** a taxonomia de setups — isso exige a Fase 3 |
| **Teste necessário** | Shadow run comparando ordem original e invertida em ≥5 sessões, incluindo pelo menos duas sem o BYRN na shortlist. Medir estabilidade do escalão 1 entre sessões consecutivas |
| **Critério de aceitação** | Nenhuma corrida devolve >10 candidatos. Toda a posição na ordem é explicável por uma regra nomeada. Zero desempates não especificados. R10 só é promovida se o escalão 1 for não vazio e ≤3 candidatos em ≥4 das 5 sessões, **e** se pelo menos duas dessas sessões não contiverem o BYRN |

---

## Resumo das classificações

| # | Critério | Estado | Tipo depois da alteração |
|---|---|---|---|
| 1 | Preço | MANTER + DIVIDIR | gate + feature de risco |
| 2 | Market cap | ALTERAR fonte | gate + flag de proveniência |
| 3 | Volume médio | DIVIDIR | dois gates (acções + USD) |
| 4 | Bolsa | MANTER + feature | gate + feature de tier |
| 5 | RSI | DIVIDIR + formalizar | gate (tecto) + feature (zona) |
| 6 | SMA20 | MANTER + flag | gate + flag de extensão |
| 7 | RVOL | MANTER + DIVIDIR + flag | gate + feature de pico + flag |
| 8 | Range 52s | **CONVERTER para feature** + reparar | feature |
| 9 | Sinais A/B/C | **IMPLEMENTAR** | gate (≥1) + confirmação (≥2) |
| 10 | Sector | **REMOVER** filtro | observabilidade |
| 11 | Red flags | MOVER + revalidar | exclusão + corporate action a montante |
| 12 | Descoberta precoce | MANTER + corrigir | features separadas |
| 13 | Selecção | **TESTAR** | prioridade + desempate especificado |

**Contabilidade das alterações:** 1 conversão de gate para feature (8), 1 gate novo implementado (9), 1 gate dividido em dois (3), 1 filtro removido (10), 1 componente movido a montante (11), 1 fonte substituída (2), 1 desempate removido (13). Nenhum limiar de gate existente é alterado nesta fase.

---

## Handoff — Fase 1

**Decisões fechadas nesta fase:** classificação de tipo para os 13 critérios; alteração candidata especificada com condição actual, condição proposta, fase, tratamento de missingness, fonte, fallback, logging e critério de aceitação; três decisões desbloqueadoras aplicadas (D1, C2, C4).

**Evidência utilizada:** exclusivamente o registo factual da Fase 0. Nenhum número novo foi produzido.

**Decisões provisórias:** R10 (inversão de prioridades) mantida como PROPOSTA por força da restrição 4.3. R9 (apertar consolidação lateral) **rejeitada** e substituída por uma regra que não escolhe limiares — exigir ≥2 dos 3 componentes do Sinal C. R4 e R5 aceites apenas como flags, com o risco de overfitting declarado.

**Questões abertas que persistem:** as oito questões de semântica XBRL (L8) continuam a bloquear a implementação do Critério 2; a Fase 1 especificou as regras (a)-(e) mas nenhuma foi validada contra dados reais. O escalão residual do Critério 13 (54%) não é resolúvel sem uma taxonomia de setups, que é matéria da Fase 3.

**Inputs necessários para a Fase 2:** tecto de chamadas por corrida (pergunta 7 da Fase 0) — o Critério 8 propõe 252 sessões de cache e o Critério 2 propõe 1 chamada SEC por candidato; a Fase 2 não pode ordenar por custo sem esse tecto. Política de falha por componente (pergunta 6) — a Fase 1 atribuiu `fail-closed` ou `DATA_INSUFFICIENT` critério a critério, mas essa atribuição precisa de ser ratificada.

**Riscos de avançar:** a Fase 2 vai propor mover o Critério 11 (corporate actions) para o universo e o Critério 8 para depois dele. Ambas as deslocações alteram a base sobre a qual todos os indicadores são calculados — sem teste de ablação, a Fase 2 produz uma ordem plausível mas não demonstrada.

**Condição para iniciar a Fase 2:** ratificação da política de falha e do tecto de chamadas. Sem isso, a Fase 2 pode ser produzida mas as suas conclusões de custo ficam como NÃO RESOLVIDO.
