# Post-Mortem — Discovery de 20/10/2025 (framework v1)

**Data do relatório:** 11/07/2026
**Objeto:** Sessão real de Discovery corrida a 20/10/2025 com o framework v1 (JSON original, pré-auditorias v4/v5): identificação de temas → screening do Tema 1 (Advanced Packaging/Hybrid Bonding) → deep-dive de 7 critérios sobre ONTO → ranking final AMKR (8,76) > ONTO (8,62) > ASMPT (8,58) > FORM (8,24) → plano de execução com gatilhos concretos.
**Âmbito:** (1) auditoria de conformidade da sessão; (2) auditoria da camada macro/não-técnica e da sua influência nas escolhas; (3) post-mortem dos tickers até 11/07/2026 com simulação dos planos; (4) counterfactual do pipeline v2 no mesmo dia; (5) parecer final.
**Autor:** Claude (Fable 5, sessão Claude Code)

**Legenda de proveniência dos números** (obrigatória — ver nota de dados no fim):
- **[V]** verificado por pesquisa (fonte no anexo)
- **[D]** derivado aritmeticamente de valores verificados
- **[A]** aproximado (reconstruído de fontes parciais/conhecimento de treino; erro possível)
- **[?]** não obtível nesta sessão

---

## 0. Resumo executivo

**A sessão de 20/10/2025 acertou espetacularmente na seleção e falhou na arquitetura de execução.** Os quatro nomes qualificados fizeram, do gatilho até 11/07/2026: **AMKR +176%, FORM +174%, ONTO +129%, ASMPT ~+118%** — todos acima do benchmark SOXX (~+101% [A]). O tema (Advanced Packaging/Hybrid Bonding) estava certo, cedo, e com catalisadores factualmente corretos — a camada macro foi verificada nesta auditoria e passa quase toda [V].

**Mas o processo que produziu essa seleção violou o seu próprio contrato**, e a execução planeada teria capturado uma fração ínfima do movimento: o plano punha o trader posicionado **à frente de três eventos de earnings** que ele próprio nunca calendarizou (AMKR 27/10, FORM 29/10, ONTO 06/11), com stops de ~3,5% em nomes que corrigiram >10% em novembro/2025. Na simulação, o trade de ONTO termina em **-1R** (stopado na correção de novembro, antes de a ação fazer +129%) e o de AMKR realiza **+2R a +4R** de um movimento que foi de **+50R** em potência.

**A conclusão mais importante desta auditoria não é "v1 mau, v2 bom":** com os parâmetros default, o v2 só teria negociado ONTO (o pior dos quatro) — o gate de dollar volume ($100M) excluía AMKR, FORM e ASMPT. O v2 teria sido mais seguro, mais repetível e mais honesto — e teria feito menos dinheiro neste episódio. As recomendações de calibração daí resultantes estão na secção 5.

---

## 1. Auditoria de conformidade — a sessão vs o próprio v1

A sessão respeitou a camada de comunicação do v1 (PT-PT, tom, pausas obrigatórias, ~3.200 caracteres reportados por critério) e a mecânica de screening declarada. As violações estão na camada de decisão — e são exatamente as que as auditorias v4/v5 previram em abstrato:

| # | Facto na sessão | Regra violada | Gravidade |
|---|---|---|---|
| 1 | O Step 4 atribui scores a AMKR (8,76), ASMPT (8,58) e FORM (8,24) declaradamente **"estimadas para os peers"** — nenhum dos três passou pelos 7 critérios | "tolerancia_imprecisao: zero" | **Crítica** |
| 2 | O **#1 do ranking (AMKR) nunca foi analisado** — a única ação com deep-dive completo (ONTO) ficou em 2º; a recomendação final ("prioridade de execução: AMKR → ONTO") assenta no nome menos estudado | Todo o step_3 do pipeline | **Crítica** |
| 3 | Notas 0-10 atribuídas aos critérios 2-7 sem rubrica — o v1 só define `scoring_rubric` para o critério 1 (finding 3.2 da v4, confirmado em produção) | `step_4_final_scoring` sem base | Alta |
| 4 | Nenhuma verificação de regime de mercado em toda a sessão — 10 dias depois do tariff-shock de 10/10/2025 (S&P -2,7%, pior dia em 6 meses [V]) | Critério inexistente no v1 (finding 3.9 da v4) | Alta |
| 5 | O plano de execução final **não calendariza earnings**: AMKR reportava a 27/10 (5.ª sessão após o Discovery), FORM a 29/10, ONTO a 06/11 [V] — e o próprio critério 4 da sessão tinha inventado a regra "Nunca estejas a 1% fully loaded à frente de earnings". A regra foi escrita e depois ignorada pelo plano | Autocontradição interna | **Crítica** |
| 6 | "hoje o fluxo já ia em ~520k **a meio da sessão** (Lisboa 21:24)" — 21:24 de Lisboa = 16:24 ET, **24 minutos após o fecho** de NY. A leitura de volume que sustenta o critério 7 foi feita com a sessão encerrada e interpretada como parcial | Rigor factual ("zero imprecisão") | Média |
| 7 | Duplicação integral do plano A-B-C/RVOL nos critérios 3, 6 e 7 (~60% do texto dos três critérios é o mesmo conteúdo reformatado) — finding 4.3 da v4 em produção | "nunca_incluir: frases repetitivas" | Média |
| 8 | Comandos prometem "9 critérios"; a sessão executa 7 | `sistema_identity.mission` | Baixa (fóssil conhecido) |

**O que a sessão fez bem (para registo):** a aritmética do score composto da ONTO está certa (verificada: 7,8×20+8,5×15+8,8×10+9,0×15+9,0×20+8,8×10+8,7×10 = 8,615 ≈ 8,62); o screening aplicou os filtros com honestidade (BESI excluída por volume apesar de ser "o name estratégico", CAMT e KLIC para watchlist com razões explícitas); as pausas interativas foram respeitadas; e várias invenções fora de spec eram melhorias reais (teto de 2-3% de risco por tema, "stop de tempo", cenário de event risk) — o executor a corrigir o framework em curso, sem contrato para isso.

**A anatomia do score 8,62 da ONTO** merece um parágrafo próprio, porque expõe o defeito estrutural do scoring do v1: dos 7 critérios, **apenas 2 (C1 momentum: 7,8; C2 gráficos: 8,5) mediram a ação**. Os outros 5 — escalonamento (8,8), risco (9,0), tema (9,0), timing (8,8), volume (8,7) — avaliaram **a qualidade do plano da própria sessão e da narrativa do tema**, não o instrumento. 65% do peso do score foi o sistema a dar nota ao seu próprio trabalho de casa. E o único critério verdadeiramente medido sobre a ação — o momentum, com a âncora de 12 meses a -36% — foi a **nota mais baixa** das sete, diluída pelas autoavaliações de 8,7-9,0. Um sistema de gates binários teria dito simplesmente: "momentum de 12M em contra-tendência; ou entra pela regra de 1-3 meses ou não entra" — sem média que o mascarasse.

---

## 2. Auditoria da camada macro/não-técnica

### 2.1 Verificação factual — a macro estava certa

Todos os catalisadores centrais citados no Step 1/critério 5 foram verificados nesta auditoria:

| Afirmação da sessão | Estado | Facto verificado |
|---|---|---|
| Kinex (AMAT+Besi), sistema integrado D2W hybrid bonding, "últimos 30 dias" | **[V]** | Anunciado a 07/10/2025; 5 anos de desenvolvimento; já em adoção por clientes logic/memory/OSAT |
| AMAT comprou 9% da BESI "em abril" | **[V]** | Abril/2025 |
| SK hynix: HBM4 pronto para produção em massa, setembro | **[V]** | Anúncio de setembro/2025 |
| CHIPS NAPMP — apoio público a advanced packaging | **[V]** | $1,4B em final awards (jan/2025): $300M substratos (Absolics, AMAT, ASU) + $1,1B Natcast/PPF |
| Amkor: campus de $7B no Arizona | **[V]** | Expansão anunciada em 2025; em maio/2026 confirmou-se program win da AMD associado à tese Arizona |
| Oppenheimer sobe PT da ONTO para $180 (14/10) | **[V]** | 14/10/2025, Edward Yang, $130→$180, Outperform |
| Ajuste do acordo Semilab (10/10) | **[V]** | Amendment datado de 09/10/2025 (-$50M, ~-10%, exclui EIR); a aquisição fechou a 17/11/2025 por $432M |
| BESI earnings call 23/10 (CET 16:00) | **[V]** (fonte secundária) | Q3 2025 da BESI reportado a 23/10/2025 |
| TSMC a acelerar advanced packaging nos EUA | **[V]** | Plano de 2025 inclui instalações de AP no Arizona |

A profundidade era real: datas certas à precisão do dia, números certos, e a cadeia causal (HBM4 → hybrid bonding → metrologia/OSAT) tecnicamente sólida. **Não foi confabulação — foi research genuíno e atual.** Os temas 2 e 3 (Grid & Power, Liquid Cooling) não foram auditados em detalhe por não terem gerado trades, mas as afirmações amostradas (S&P/451 +22%, défice de transformadores Wood Mackenzie, OCP Summit 13-16/10) são consistentes com o registo público da época.

### 2.2 A influência estrutural — o que a macro realmente decidiu

Aqui está o ponto que o pedido desta auditoria levanta, e a resposta é desconfortável para ambas as versões do framework:

1. **A macro determinou 100% do universo.** Nenhum dos 4 tickers entrou por um scan de preço: entraram porque a narrativa (hybrid bonding) os nomeou, e a técnica limitou-se a ordenar dentro dessa lista de 7 nomes. A ONTO — com 12 meses a -36% — nunca sairia de um scan de líderes; entrou porque a tese técnica ("metrologia é o gargalo do HBM4") a nomeou.

2. **Mas o sinal já estava nos preços — a macro foi confirmatória, não generativa.** Este é o teste decisivo, e é possível fazê-lo com os números da própria sessão: a 20/10/2025, o scan bottom-up do v2 (top performers 3 meses) apanhava **AMKR +50,3%, ONTO +40,6%, ASMPT +35-39%, CAMT +33%** — quatro nomes do mesmo sub-setor, todos a bater o SOXX (+20,99%), em simultâneo. É exatamente a definição de "tema qualificado" do passo 1 do v2 (≥3 títulos do mesmo grupo). **O tema Advanced Packaging era detetável por agregação de scans, sem ler um único press release.** O research macro (excelente) chegou à mesma lista que meia hora de screening — o que confirma empiricamente a decisão da v5 (ponto 7.9) de absorver o critério 5 no pipeline.

3. **O que a macro acrescentou de facto:** (a) convicção — que se traduziu em prioridade de execução e no peso 20 do critério 5 a empurrar o score; (b) a ONTO, que o scan de líderes puro teria tratado com desconfiança (12M negativo) — e que foi precisamente **o pior dos 4 nomes** no post-mortem (+129% vs +174-176% dos outros); (c) risco de ancoragem: 5 dos 7 critérios da ONTO citam os mesmos 3 catalisadores (Kinex, HBM4, NAPMP) como reforço — a narrativa contaminou critérios supostamente técnicos.

**Veredito da camada macro:** profundidade real, factualidade quase perfeita, e contributo marginal para a seleção — o preço já dizia o mesmo. O custo dela não foi estar errada: foi (i) custar peso de scoring que mascarou o único sinal técnico fraco (C1 da ONTO), e (ii) não ser reproduzível — research desta qualidade não é garantido em cada sessão, enquanto um scan é.

---

## 3. Post-mortem dos tickers (20/10/2025 → 11/07/2026)

### 3.1 O que aconteceu — cronologia verificada

**Curto prazo (as 4 semanas críticas):**

- **20/10 (seg):** Discovery. AMKR HOD 32,70; ONTO ~135,7 (dados da sessão).
- **21-24/10:** AMKR sobe para ~$33,2 [D — derivado de "+14% na semana" para 37,84] → **o buy-stop de 32,75 disparou antes dos earnings**, deixando o plano v1 posicionado à frente do evento que não tinha calendarizado.
- **27/10 (seg):** AMKR reporta Q3: $1,99B (+31% seq), EPS 0,51 vs 0,43 esperado, acima do topo do guidance [V]. Na semana seguinte ao anúncio a ação sobe **+14% para $37,84** [V].
- **29/10 (qua):** FORM reporta Q3: beat de 32% no EPS, guidance acima; "shares rise" [V]. O gatilho 44,35 dispara nesta janela [A].
- **06/11 (qui):** ONTO reporta Q3: EPS 0,92 vs 0,89, receita $218,2M **abaixo** do consenso; guidance Q4 forte ($250-265M, +15-21% seq) [V]. Fecho pré-reação ≈ $139,9 [D] — ou seja, **o gatilho 139,10 tinha disparado antes dos earnings** e o plano estava posicionado.
- **07/11 (sex):** ONTO **-2,95% para $135,76**, "further declines in after-hours" [V]. O stop de 134,60 fica a $1,16 de distância.
- **10-21/11:** Correção do setor: a 20/11 o SOX cai **-3,35% num dia**, Nasdaq -1,44%; NVDA devolve o pop pós-earnings; 45% dos gestores (BofA survey) apontam "AI bubble" como maior tail risk; LRCX -10% na semana [V]. Neste ambiente, a probabilidade de a ONTO (fechada a 135,76 a 07/11) não ter tocado 134,60 é negligenciável → **stop executado, -1R** [inferido — ver nota de dados].
- **Dez/2025:** recuperação. ONTO negoceia a $168,37 a 10/12 e ~$160 a 11/12 [V] — +24% acima do stop que acabara de executar.

**Longo prazo (o que o tema fez):**

| Ticker | Gatilho v1 (out/2025) | 11/07/2026 | Variação | Marcos |
|---|---|---|---|---|
| **AMKR** | 32,75 | **90,46** [V] | **+176%** | ATH $83,30 a 12/06/2026 e de novo em julho; catalisadores 2026: Q1 recorde, primeiro Investor Day em ~20 anos (21/05, alvo $11B receita/EPS >$5 em 2030), program win da AMD no Arizona [V]; +304% em 12 meses [V] |
| **FORM** | 44,35 | **121,42** [V] | **+174%** | ~$60,6 no fim de 2025 [D — YTD 2026 +100,49%]; ATH $160,27 a 30/06/2026; -17,7% na semana antes de 11/07 [V]; promovida ao Russell 1000 em jun/2026 [V] |
| **ONTO** | 139,10 | **318,45** [V] | **+129%** | ~$135,76 a 07/11 [V]; $168,37 a 10/12 [V]; pico de $386,46 no 1S2026 [V]; +183,6% em 12 meses [V]; Oppenheimer subiu o PT para $450 em 2026 [V] |
| **ASMPT** | ~HKD 86 [D — do market cap citado na sessão] | **HKD 187,90** [V] | **~+118%** | 52w: 59,60–244,40 [V]; Q1 2026: receita +32% YoY, bookings +71,6% [V] — a tese TCB/HB confirmou-se operacionalmente |
| **SOXX** (benchmark) | ~290 [A] | **584** [V] | **~+101%** | 2025: +40,7% no ano [V]; crash de -10% num dia a 05/06/2026 (miss da Broadcom, ~$1,3 biliões de market cap apagados no setor) [V]; recuperação parcial |

**Todos os quatro nomes bateram o benchmark.** A seleção — incluindo a ordenação AMKR #1 feita sem análise — foi vindicada pelo mercado. Nota de simetria: o setor também demonstrou em 05-06/2026 exatamente o risco de correlação que a sessão tinha intuído ("um air-pocket setorial pode afundar todos no mesmo dia").

### 3.2 Simulação dos planos — o que o trader teria realmente ganho

**Trade ONTO segundo o plano v1** (tal como escrito na sessão):
- Entrada A a 139,10 (algures entre 21/10 e 06/11); risco/ação $4,50.
- A ação nunca correu +6-8% antes dos earnings (máximo pré-evento ≈ 140-141 [A]) → sem parcial, sem B provável, stop original intacto.
- Posição atravessa os earnings de 06/11 (violação da regra do próprio critério 4 da sessão).
- 07/11: -2,95%; correção de 10-21/11: stop a 134,60 executado → **resultado: -1R** (-$1.000 numa conta de $100k). A ação fez +129% nos 8 meses seguintes sem o trader.

**Trade ONTO segundo as regras v2** (mesmo dia, mesmos dados):
- A regra de earnings ("sem parcial vendida + almofada, não atravessa o evento") força a saída até 05-06/11 a ~139-140 → **scratch (~0R a +0,2R)**.
- Reentrada apenas em novo setup completo (a base de dezembro, ~$160-168) — o v2 não garante apanhar o movimento, mas evita a perda e a ferida psicológica, e deixa o candidato vivo na watchlist.

**Trade AMKR segundo o plano v1:**
- Entrada A a 32,75 entre 21-24/10 [D]; risco/ação $1,15; earnings 5 sessões depois, não calendarizados.
- Gap pós-earnings: +14% na semana → $37,84 = **+4,4R em potência**.
- O plano do Step 4 marcava alvos de gestão em **1,5R (34,48) e 2R (35,05)** — parciais tomadas nesses níveis realizam +1,5 a +2R sobre grande parte da posição; o remanescente com trailing 10-20DMA é provavelmente fechado na correção de novembro perto de breakeven-a-+2R [A].
- **Resultado realista: +2R a +4R realizados.** O movimento completo até julho/2026 foi de **+50R em potência** (57,71/1,15). O plano capturou 4-8% dele.
- Nota crítica: o resultado positivo dependeu de um gap de earnings favorável **que o plano não sabia que ia atravessar**. Com um miss, o gap contra teria saltado o stop de 31,60 — a perda não estava limitada a 1R; o sizing "1% de risco" era uma ficção na presença do evento.

**Trade AMKR segundo as regras v2:**
- Entrada a 21-24/10 **bloqueada** (earnings a <5 sessões, sem almofada).
- 28/10 é um **Episodic Pivot de manual**: gap forte com beat-and-raise, primeiro dia da reavaliação → entrada legítima no ORH do dia 28 (~$35-36 [A]), stop no low do dia. O v2 não perde o nome — ganha-o **depois** do evento, com o risco verdadeiramente limitado. Com saída faseada (1/3-1/2 a 2-3R) + trailing MA20 + reforços nos setups seguintes (dez/2025, fev/2026, maio/2026), a regra de "reforço só em novo setup" é o único mecanismo em qualquer das versões capaz de transformar +176% de movimento em dígitos duplos de R realizados.

**FORM (v1 "defensivo"):** gatilho 44,35 disparado na janela dos earnings de 29/10 [A]; a ação fecha o ano a ~$60,6 [D] → +6R em potência já em dezembro; ~+44R até ao pico de junho/2026. O nome com o gatilho mais "defensivo" foi o segundo melhor. **No v2, nunca teria sido negociado** (ver secção 4).

**Balanço da carteira v1 tal como planeada** (risk budget 50/50 AMKR+ONTO): ~+2R a +4R na AMKR, -1R na ONTO → **líquido: +1R a +3R** num episódio em que o cabaz escolhido fez +149% em média. A seleção gerou o alpha; a arquitetura de execução (stops de 3,5% ao estilo swing apertado, sem gestão de eventos, sem mecanismo de reentrada) devolveu-o quase todo.

---

## 4. Counterfactual — o pipeline v2 a 20/10/2025

**Passo 0 — Filtro de mercado (gate global, aplica-se antes de qualquer ticker):** **GO marginal [A]**. Seis sessões após o -2,7% de 10/10, as MA10 de QQQ/SPY tinham sido puxadas para junto das MA20; com os fechos reconstruídos a diferença está dentro da margem de erro. Uma implementação estrita podia ter dito NO-GO a 20/10 e GO na semana seguinte — em qualquer dos casos, o v2 teria *sabido* que operava num regime frágil, coisa que a sessão v1 nunca verificou.

**Passo 1 — deteção de tema (gate global):** ✅ tema qualificado — AMKR, ONTO, ASMPT e CAMT apareciam simultaneamente no scan de 3 meses do mesmo grupo: o tema era detetável bottom-up (ver 2.2).

Gates por ticker:

| Gate v2 | AMKR | ONTO | ASMPT | FORM |
|---|---|---|---|---|
| **Passo 1 — Scan 1/3/6m top 1-2%** | ✅ +50,3% 3m | ✅ +40,6% 3m | ✅ +35-39% 3m | ⚠️ +25,5% — acima do setor mas provavelmente fora do top 1-2% |
| **Passo 2 — Liderança** (30-100%+ em 1-3m; > MA10/MA20) | ✅ máximos novos | ⚠️ +40%/3m mas 12m -36% e a negociar ~3,6% abaixo do máximo do mês [A] | ✅ | ⚠️ |
| **Passo 3 — Dollar volume ≥ $100M** | ❌ ~2,46M × $32,5 ≈ **$80M** | ✅ ~1,43M × $135,7 ≈ **$194M** | ❌ ~3,5M × HKD86 ≈ **US$38M** | ❌ ~0,91M × $44 ≈ **$40M** |
| **Passo 4 — stop_distance ≤ 1×ADR** | ✅ risco 3,5% ≈ ADR [A] | ✅ risco 3,2% ≈ 0,8-0,9×ADR [A] | n/a | ✅ risco 6,0%… ❌ >1×ADR se ADR ~4% [A] |
| **Passo 6 — Regra de earnings** | ❌ evento a 5 sessões → entrada pré-27/10 bloqueada; **EP legítimo a 28/10** | ❌ atravessar 06/11 bloqueado → scratch em vez de -1R | (results 28/10 [A]) | ❌ evento a 7 sessões |
| **Resultado v2** | Não entra a 32,75; entra como EP a 28/10 | Entra; sai antes de earnings ~0R; reentra no setup de dez. | Não entra (liquidez) | Não entra (liquidez + RS) |

**A leitura honesta desta tabela tem dois gumes:**

1. **O v2 teria feito tudo o que promete:** nenhuma posição à frente de earnings, nenhum score estimado, nenhum peso narrativo, deteção do tema por scan (sem depender de research de qualidade excecional), e a AMKR capturada da forma metodologicamente correta — como Episodic Pivot pós-evento, com risco real ≤1R.

2. **E, com os defaults atuais, teria negociado apenas 1 dos 4 vencedores — precisamente o pior (ONTO, +129%).** O gate de $100M de dollar volume — calibrado para a escala de conta do próprio Kullamägi — exclui AMKR ($80M), FORM ($40M) e ASMPT ($38M), que fizeram +174-176%. Para uma conta retail, o parâmetro está demasiado apertado: a liquidez necessária para executar $2-20k sem mover o book é ordens de grandeza menor.

**Recomendações de calibração resultantes (a aplicar ao `kristjan-discovery-system-v2.json`):**
1. **`dollar_volume_min_usd` deve escalar com a conta** — p.ex. `max($20M, 200 × posição_máxima_em_$)` em vez do default fixo de $100M; manter $100M apenas como default para contas institucionais. (O caso AMKR/FORM é a prova empírica.)
2. **Adicionar ao passo 5/6 um campo obrigatório `proximos_earnings`** (data + nº de sessões) — a falha mais grave da sessão auditada não foi conceptual, foi de *checklist*: a regra existia e não havia campo que obrigasse a preenchê-la.
3. **Passo 0 com histerese**: em regime marginal (|MA10-MA20| < 0,3% [convenção a calibrar]), permitir watchlist + EPs mas bloquear breakouts — teria refletido corretamente o estado real do mercado a 20/10/2025 (recuperação pós-choque, confirmada na semana seguinte).
4. **Formalizar a reentrada**: o caso ONTO (-1R em novembro, +129% depois) mostra que o valor do método está menos no primeiro trade e mais na disciplina de voltar ao candidato quando forma novo setup. O v2 já tem a regra ("reforço só em novo setup") — falta um mecanismo de watchlist pós-stop que a torne operativa.

---

## 5. Parecer final — a abordagem de então vs a de agora

**O que este episódio prova sobre o v1:** a sessão de 20/10/2025 é o melhor caso possível do v1 — research macro de qualidade genuína, screening honesto, tema certo, nomes certos, timing decente — e ainda assim o processo entregou +1R a +3R de um cabaz que fez +149%, deixou -1R no único nome analisado a fundo, e esteve exposto a três eventos binários sem o saber. As falhas não foram de inteligência; foram as falhas *estruturais* que as auditorias v4/v5 identificaram no papel: scoring que se auto-avalia, ausência de gestão de eventos no plano executável, ausência de filtro de regime, stops de swing curto colados a movimentos de tese longa, e "zero imprecisão" declarada sobre scores confessadamente estimados.

**O que este episódio prova sobre o v2:** as regras teriam funcionado como desenhadas — ONTO scratch em vez de -1R, AMKR como EP pós-earnings em vez de roleta pré-earnings, tema detetado por scan em vez de depender de research de elite. Mas o episódio também expõe o preço da disciplina com parâmetros mal calibrados: o gate de liquidez institucional custava 3 dos 4 vencedores. **Um framework não é validado por ser mais restritivo; é validado por a restrição comprar algo** — aqui, comprou controlo de risco real (a AMKR podia ter falhado os earnings) ao custo de amplitude de universo que é corrigível por calibração, e essa correção está agora especificada (secção 4).

**Sobre a camada macro, a resposta direta à pergunta desta auditoria:** a profundidade macro era real e verificou-se quase na íntegra — mas o seu papel causal na seleção foi menor do que parece. Os quatro tickers estavam todos no top de performers de 3 meses do próprio sub-setor à data; o scan bottom-up do v2 tê-los-ia agrupado como tema qualificado sem um único press release. O que a macro acrescentou foi convicção (que o scoring transformou em peso, mascarando o sinal técnico fraco da ONTO) e um nome de turnaround (ONTO — o pior dos quatro). A decisão do v2 de substituir a camada macro pela agregação de scans não perde o que gerou o alpha deste episódio; perde uma fonte de convicção não reproduzível — e é exatamente essa troca (narrativa por processo) que separa as duas versões.

**Uma última observação sobre sorte e processo.** O ranking pôs em #1, sem análise nenhuma, o nome que fez +176% com um beat de earnings seis sessões depois. Se os earnings da AMKR tivessem falhado, esta mesma transcrição seria hoje a prova de acusação contra estimar scores e atravessar eventos às cegas. Avaliar o processo pelo resultado deste episódio seria repetir o erro que o método de Kullamägi existe para evitar: com ~25-30% de win rate, qualquer sistema vive de sobreviver aos maus desfechos, não de ser julgado nos bons.

---

## Nota de dados e limitações

- O ambiente desta sessão bloqueia (política de egress) as fontes diretas de OHLCV (stooq, Yahoo Finance API, stockanalysis, macrotrends) — testado incluindo com headers de browser; o bloqueio é no gateway, anterior ao site. Toda a reconstrução assenta em pesquisa web dirigida (excertos indexados) + derivações aritméticas.
- Consequências concretas: o dia exato do disparo dos gatilhos (AMKR 21-24/10; ONTO 21/10-06/11; FORM ~29-31/10) e os mínimos exatos de novembro/2025 não foram obtidos à precisão do tick. A conclusão "stop da ONTO executado em novembro" é inferência de alta confiança (fecho a $1,16 do stop a 07/11 + SOX -3,35% só no dia 20/11), não observação direta.
- **Para elevar a simulação a exatidão de tick**: (a) adicionar `stooq.com` ou `stockanalysis.com` à network policy do environment em claude.ai/code, ou (b) carregar CSVs OHLCV (broker/TradingView) na conversa — refaço as tabelas de simulação com dados exatos e recalculo os R.
- Nenhuma parte deste documento é aconselhamento financeiro; é uma auditoria retrospetiva de processo.

## Anexo — Fontes principais desta auditoria

- [Amkor 8-K Q3 2025 (27/10/2025)](https://www.sec.gov/Archives/edgar/data/1047127/000104712725000187/amkr9302025erex-991.htm) · [Amkor ATH e catalisadores 2026 — TIKR](https://www.tikr.com/blog/amkor-technology-stock-rises-to-an-all-time-high-can-it-keep-going) · [Investing.com — AMKR ATH $79,49](https://www.investing.com/news/company-news/amkor-technology-stock-hits-alltime-high-at-7949-usd-93CH-4724536)
- [Onto Innovation — resultados Q3 2025 (06/11/2025)](https://investors.ontoinnovation.com/news/news-details/2025/Onto-Innovation-Reports-2025-Third-Quarter-Results/default.aspx) · [Investing.com — "beats EPS, stock dips" (-2,95% → $135,76)](https://www.investing.com/news/transcripts/earnings-call-transcript-onto-innovation-q3-2025-beats-eps-stock-dips-93CH-4340558) · [ts2.tech — ONTO a 11/12/2025 (~$160; $168,37 a 10/12)](https://ts2.tech/en/onto-innovation-onto-stock-on-december-11-2025-latest-price-q3-earnings-semilab-deal-and-2026-forecasts/) · [Semilab: fecho da aquisição 17/11/2025 — StockTitan](https://www.stocktitan.net/sec-filings/ONTO/8-k-onto-innovation-inc-reports-material-event-8cdcd0ee7be2.html) · [Oppenheimer $130→$180 (14/10/2025)](https://www.investing.com/news/analyst-ratings/onto-innovation-stock-price-target-raised-by-oppenheimer-to-180-93CH-4286277) · [Oppenheimer $370→$450 (2026) — MarketScreener](https://www.marketscreener.com/news/oppenheimer-adjusts-onto-innovation-price-target-to-450-from-370-maintains-outperform-rating-ce7f5cd3dc8ef72d)
- [FormFactor — resultados Q3 2025 (29/10/2025)](https://www.globenewswire.com/news-release/2025/10/29/3176831/0/en/FormFactor-Inc-Reports-2025-Third-Quarter-Results.html) · [FORM: preço atual, ATH 30/06/2026, -17,7%/semana — WallStreetZen/StockAnalysis](https://stockanalysis.com/stocks/form/) · [Russell shift — Simply Wall St](https://simplywall.st/stocks/us/semiconductors/nasdaq-form/formfactor/news/formfactor-form-could-be-18-undervalued-on-russell-index-shi)
- [ASMPT — cotação 0522.HK](https://finance.yahoo.com/quote/0522.HK/) · [ASMPT Q1 2026 (+32% receita, +71,6% bookings)](https://www.asmpt.com/en/investor-relations/news-events/asmpt-announces-2026-first-quarter-results/)
- [SOXX — cotação atual](https://finance.yahoo.com/quote/SOXX/) · [SOXX fact sheet (2025: +40,7%)](https://www.ishares.com/us/literature/fact-sheet/soxx-ishares-semiconductor-etf-fund-fact-sheet-en-us.pdf) · [Crash de 05/06/2026 (Broadcom; SOXX -10%)](https://intellectia.ai/blog/semiconductor-stocks-selloff-june-2026)
- [Tariff-shock 10/10/2025 (S&P -2,7%, $2T) — Fortune](https://fortune.com/2025/10/10/trump-2-percent-sp-500-china-tariffs-rare-earths-metals/) · [CNBC](https://www.cnbc.com/2025/10/11/trump-post-costs-stocks-2-trillion-in-single-day.html) · [Correção de 20/11/2025 (SOX -3,35%; BofA "AI bubble" 45%)](https://markets.financialcontent.com/wral/article/tokenring-2025-11-20-tech-and-semiconductor-stocks-face-headwinds-as-ai-bubble-fears-mount-amid-economic-uncertainty)
- [Kinex — anúncio AMAT (07/10/2025)](https://www.globenewswire.com/news-release/2025/10/07/3162509/0/en/Applied-Materials-Unveils-Next-Gen-Chipmaking-Products-to-Supercharge-AI-Performance.html) · [EE Times — AMAT/Besi D2W HVM](https://www.eetimes.com/applied-materials-besi-push-die-to-wafer-hybrid-bonding-toward-high-volume-manufacturing/)
- [NAPMP $1,4B final awards (jan/2025) — NIST](https://www.nist.gov/news-events/news/2025/01/us-department-commerce-announces-14-billion-final-awards-support-next)

---

*Fim do post-mortem. Este documento fecha o ciclo iniciado no handoff v4: especificação (v4) → verificação (v5) → reescrita (v2 JSON) → validação empírica contra uma execução real (este relatório).*
