# Corrida do Motor de Inflexões — 17/07/2026 (T1, ponto de dados #2)

**Comando executado:** `corrida_semanal` do `inflection-discovery-engine.json`
**Data de referência:** 17/07/2026 (última sessão de mercado apurada: 16/07/2026)
**Corrida anterior:** 11/07/2026 (ponto de dados #1). Intervalo: 6 dias.
**Modo:** manual (a automação semanal continua bloqueada — ver nota no fim).

**Restrições declaradas (regra de honestidade nº 2 do motor):** evidência por excertos de WebSearch (WebFetch bloqueado). Classes de emissor 6 (talento) e 7 (infraestrutura física) não pesquisáveis com fiabilidade — NÃO OBTÍVEL, nunca estimadas. Contexto de mercado: pullback setorial a 16/07/2026 (SOXX −4,5% no dia) — registado como contexto, não é gate.

**Disclaimer:** output de research/watchlist. Não é aconselhamento financeiro. Sem níveis de entrada, stops ou sizing.

---

## PARTE A — Ações pendentes do arquivo (tratadas primeiro)

### A.1 — Desbloqueio do cartão Ibiden (2.ª e última tentativa) → ✅ SUCESSO

- **Ação:** confirmar a data de resultados trimestrais no IR da Ibiden. 1.ª tentativa falhou a 11/07; à 2.ª falha, o cartão morria.
- **Resultado:** **data confirmada — 04/08/2026** (próximos resultados; Investing.com, apurado 17/07/2026). O padrão histórico (Q1 FY a ~1 de agosto; FY2026 foi 01/08/2025) corrobora.
- **Efeito:** o cartão Ibiden (4062.T) **sai de RETIDO → ENTREGUE**. Passa a ter calendário e entra no acompanhamento como cartão pleno da etapa 2 (substrato ABF).
- *Nota de método:* o mecanismo do cartão retido funcionou como desenhado — não se entregou um cartão sem calendário, e o desbloqueio aconteceu por confirmação real de fonte, não por data inventada. Primeira validação forward do mecanismo retido→entregue.

### A.2 — Verificação de invalidadores dos cartões entregues (FORM, TER)

**FORM (FormFactor):** nenhum invalidador disparou.
- Invalidador (1) insourcing do teste fotónico pelas foundries: **sem evidência**.
- Invalidador (2) esvaziamento da parceria Advantest: **sem evidência** — e, pelo contrário, surgiu um **sinal custoso reforçador** que o cartão #1 não tinha registado: **a FormFactor adquiriu a Keystone Photonics (15/12/2025)**, "pioneira em optical probing para teste wafer de silicon photonics e CPO" (GlobeNewswire/FormFactor, 15/12/2025). É um compromisso custoso (aquisição) sobre a *exata* portagem da tese — reforça a perna-produto e a defensabilidade, não a enfraquece.
- Invalidadores (3) 2 trimestres pós-COUPE sem receita SiPh e (4) rampa CPO adiada 2028+: **prematuros** — earnings a 29/07/2026 ainda não ocorreram; reavaliar no pós-resultados.
- **Estado FORM: mantém-se ENTREGUE / qualificado, com sinal reforçador registado.**

**TER (Teradyne):** nenhum invalidador disparou.
- Invalidador (1) integração Quantifi falhada: **sem evidência** — Quantifi descrita como integrada e a acelerar a posição em teste de SiPh.
- Invalidador (2) ficonTEC capturada por rival: **sem evidência**.
- Invalidador (3) segmento robótico a deteriorar-se e a dominar a narrativa: **não disparou, e no sentido oposto** — a robótica surge como *driver de crescimento* (plano de registo de um grande cliente, esperado como motor de crescimento no 2S2026), não como deterioração. O invalidador vigiava a robótica-como-lastro; observa-se robótica-como-motor.
- *Ressalva de fidelidade:* apareceu um título "Teradyne (TER) Stock Moves −13,63%" sem data confirmável no excerto — **não contado** (pode ser reação a resultados passados; a apurar na próxima corrida). O fecho de 16/07 foi $321,99, sem sinal de queda dessa ordem nessa sessão.
- **Estado TER: mantém-se ENTREGUE / qualificado (ressalva de pureza inalterada).**

### A.3 — Tema CPO: prazo de reavaliação do gradiente

- Prazo **até 05/09/2026** (marcador TRANSICAO_2_PARA_3) — **ainda não vencido** (faltam ~7 semanas). Sem ação obrigatória esta semana.
- *Observação de deriva:* a pesquisa de gargalos desta semana (Moody's: escassez de substrato PCB/ABF a limitar entregas de chips até 2027; CoWoS esgotado; 2nm booked até 2027) mantém a sub-camada substrato no discurso especializado. Ainda **não** encontrada cobertura generalista dedicada nem ETF da etapa 2/6 → gradiente ainda 1-2. A vigiar no prazo formal.

### A.4 — Proxy de valor (medição a partir desta corrida, #2)

| Instrumento | Fecho 16/07/2026 | Baseline 10/07/2026 | Δ desde baseline | Fonte |
|---|---|---|---|---|
| FORM | **$110,21** (−4,84% no dia) | $121,42 | **−9,23%** | Yahoo/stockanalysis, 16/07 |
| TER | **$321,99** (1.º registo) | — (não registado no #1) | — | Yahoo, 16/07 |
| SOXX (benchmark) | **$530,50** | $584 | **−9,16%** | Investing/iShares, 16/07 |

**Leitura (com honestidade de amostra):** em 6 dias, o cabaz de cartões (FORM) moveu-se **essencialmente em linha com o setor** (FORM −9,23% vs SOXX −9,16%) — não há sinal idiossincrático, e o movimento é um pullback setorial de risco (SOXX −4,5% a 16/07), não um evento específico dos nomes. **6 dias não têm significado de tese** — é apenas o arranque formal da série do proxy; o valor acumula-se ao longo de meses.

---

## PARTE B — Descoberta (fases 1-5, varrimento de novas hipóteses)

**Resultado da fase 1-4: NENHUM tema novo cruzou a fasquia esta semana.** Os sinais frescos mais fortes reforçam temas já classificados, não abrem um novo:

| Sinal fresco (17/07/2026) | Nível/emissor | Onde encaixa | Veredito |
|---|---|---|---|
| Moody's: escassez de substrato PCB/ABF pode limitar entregas de chips até 2027; constrangimento a migrar de fab para materiais a montante | L3, analista/agência | **Reforça a perna Ibiden/ABF** (tema CPO, já qualificado) | Não é tema novo — corrobora um cartão vivo |
| CoWoS esgotado; 2nm booked até 2027; HBM3E alocado; 6 fabs TSMC lotadas (lead times 78-104 semanas) | L4, TSMC/OSATs | Advanced packaging (tema **maduro** de out/2025) + reforça procura a jusante do CPO | Maduro / reforço |
| Siemens Energy backlog recorde €154B, book-to-bill 1,72; Grid Technologies b2b 1,90; GE Vernova 100 GW de backlog de turbinas (Q1 2026) | L5, produtores | Grid/equipamento elétrico pesado (tema **maduro**, H1) | Maduro — falha o gate de invisibilidade |
| Forgent Power Solutions: bookings $867M, book-to-bill 2,3×, backlog recorde $1,98B | L4, produtor | Grid (mesma família madura) — nome menos coberto, mas sub-camada já retail | Maduro; não abre pure-play com edge |

**Por que não se força um tema:** o motor é um gate, não um gerador de novidade obrigatória. Numa janela de 6 dias, o resultado honesto é que a paisagem de inflexões não mudou materialmente; os grandes atractores de sinal custoso (energia/rede, packaging) ou já estão seguidos (CPO) ou já estão maduros (grid, humanoides). Qualificar um tema maduro só para "ter output" seria teatro — precisamente o que o motor deve recusar.

**Observação longitudinal (para as métricas): "maduro" (cobertura) ≠ pico industrial.** O tema grid foi classificado maduro a 11/07 (~9 meses de cobertura desde out/2025), mas a curva **industrial** continua a subir (Siemens Energy b2b 1,72; GEV backlog a caminho de 110 GW no fim do ano). Confirma a tese das duas curvas: a curva de cobertura/preço satura *antes* de a curva industrial atingir o pico. O edge informacional morre, o supersiclo industrial continua. Dado útil para calibrar o que "maduro" significa (perda de edge, não fim da procura).

---

## PARTE C — Estados atualizados, calendário e métricas

### Estados dos temas (pós-corrida #2)

| Tema | Estado | Mudança nesta corrida |
|---|---|---|
| Industrialização do CPO | **qualificado** | Sem mudança de estado; perna ABF reforçada (Moody's); cartão Ibiden desbloqueado |
| SRM / energéticos | **qualificado (sem cartão)** | Sem mudança; sem IPO do universo privado observado |
| Atuadores de humanoides | **maduro** | Sem mudança |
| Equipamento elétrico pesado | **maduro** | Sem mudança de estado; nota: curva industrial ainda a subir (b2b 1,72/GEV 100GW) |

### Cartões (pós-corrida #2)

| Ticker | Etapa | Estado | Calendário | Nota |
|---|---|---|---|---|
| FORM | Teste eletro-ótico WL | **entregue / qualificado** | Earnings 29/07/2026 | + sinal reforçador Keystone (15/12/2025) |
| TER | Teste eletro-ótico WL (par) | **entregue / qualificado** | Earnings 28/07/2026 AC | Robótica = motor, não lastro |
| **Ibiden (4062.T)** | Substrato ABF | **entregue / qualificado** (era RETIDO) | **Resultados 04/08/2026 [confirmado]** | Desbloqueado à 2.ª tentativa |

### Calendário consolidado

| Data | Evento | Relevância |
|---|---|---|
| 28/07/2026 | TER Q2 (after close) | Cartão entregue — 1.º teste de invalidadores forward |
| 29/07/2026 | FORM Q2 | Cartão entregue — idem |
| 04/08/2026 | **Ibiden resultados [confirmado]** | Cartão entregue (recém-desbloqueado) |
| 17 ou 24/08/2026 | FN Q4 FY26 (confirmar) | Etapa 5 CPO (sem cartão) |
| até 05/09/2026 | Reavaliação gradiente CPO | Prazo TRANSICAO_2_PARA_3 |

### Métricas do motor (atualizadas)

| Métrica | Valor | Nota |
|---|---|---|
| Lead time inflexão→mainstream | ~6-9 meses (2 obs. retroativas) | Inalterado; refinamento: "mainstream" = perda de edge de cobertura, ≠ pico industrial (grid ainda a subir industrialmente) |
| Honestidade preditiva dos invalidadores | ainda sem tese morta; **1.º ciclo de verificação forward limpo** (0 disparos em FORM/TER a 17/07) | Primeiro ponto forward: nenhum invalidador falso, nenhum disparo real |
| Mecanismo retido→entregue | **1.ª validação forward** (Ibiden desbloqueado à 2.ª tentativa por fonte real) | O mecanismo do cartão retido funciona no tempo |
| Proxy de valor | FORM $110,21 · TER $321,99 · SOXX $530,50 (16/07) | Cabaz em linha com benchmark em 6 dias (sem significado de tese ainda) |

---

## Nota sobre a automação (transparência)

Esta corrida foi disparada **manualmente** a pedido. A tentativa de ativar a Routine semanal automática (sábados 10:00 UTC, sessão nova por disparo) voltou a falhar a 17/07/2026 com "MCP tool call requires approval" — a superfície de sessão atual (móvel/web) não consegue apresentar o carimbo de aprovação que o servidor de agendamento exige. A automação fica pendente de ativação a partir de uma interface de computador (app/IDE/Routines no browser) com a especificação já registada no arquivo. Até lá, o modo manual mantém a série viva; este arquivo garante a continuidade.

---

## Fontes principais desta corrida

- [Ibiden IR](https://www.ibiden.com/ir/) · [Ibiden earnings 04/08/2026 — Investing.com](https://www.investing.com/equities/ibiden-co-ltd-earnings)
- [FormFactor adquire Keystone Photonics (15/12/2025) — GlobeNewswire](https://www.globenewswire.com/news-release/2025/12/15/3205831/0/en/FormFactor-Expands-Silicon-Photonics-Test-Capabilities-With-Acquisition-of-Keystone-Photonics.html) · [FormFactor investors](https://investors.formfactor.com/news-releases/news-release-details/formfactor-expands-silicon-photonics-test-capabilities/)
- [Teradyne/Quantifi Photonics — Teradyne IR](https://investors.teradyne.com/news-events/press-releases/detail/10/teradyne-to-acquire-quantifi-photonics) · [TER Q2 2025 call transcript — Motley Fool](https://www.fool.com/earnings/call-transcripts/2026/04/28/teradyne-ter-q2-2025-earnings-call-transcript/)
- [FORM cotação — stockanalysis](https://stockanalysis.com/stocks/form/) · [TER cotação — Yahoo](https://finance.yahoo.com/quote/TER/) · [SOXX — iShares](https://www.ishares.com/us/products/239705/ishares-phlx-semiconductor-etf)
- [Moody's — semicondutores 2026, gargalos da cadeia](https://www.moodys.com/web/en/us/insights/corporations/semiconductors-in-2026-why-supply-chains-are-a-major-bottleneck.html) · [AtlasPCB — Moody's substrato PCB até 2027](https://www.atlaspcb.com/news/news-moodys-semiconductor-supply-chain-pcb-substrate-shortage-2027/) · [FusionWW — CoWoS/HBM/2-3nm até 2027](https://info.fusionww.com/blog/inside-the-ai-bottleneck-cowos-hbm-and-2-3nm-capacity-constraints-through-2027)
- [Siemens Energy — ordens recorde FY2026](https://finance.yahoo.com/sectors/energy/articles/siemens-energy-raises-fy2026-outlook-065132768.html) · [Green Stocks Research — grid hardware](https://greenstocksresearch.com/grid-hardware-stocks/)

---

*Fim da corrida #2. Mudanças materiais: cartão Ibiden desbloqueado (RETIDO→ENTREGUE, 04/08/2026); 1.º ciclo de verificação forward de invalidadores limpo (FORM/TER, 0 disparos) + sinal reforçador Keystone para FORM; nenhum tema novo qualificado; proxy de valor iniciado. Insight: "maduro" (cobertura) ≠ pico industrial.*
