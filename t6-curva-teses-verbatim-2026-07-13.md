# T6 — Curva de degradação: teses verbatim (10 / 5 / 2 / 1 pesquisas)

**Data:** 13/07/2026
**Objeto:** o mesmo tema (CTC / faturação eletrónica obrigatória na Europa), o mesmo perfil (Parte II pós-podas), a mesma data — só o **orçamento de pesquisa** varia. Quatro operadores frios e isolados, correndo em paralelo, cada um sem ver os outros nem o T6 de 3 pesquisas. O patamar de **3 pesquisas** está em `t6-tese-claude-2026-07-13.md`; estes quatro completam a curva.
**Consumo verificado (contador de ferramentas de cada operador):** 10-tier = 10 WebSearch (+1 WebFetch que deu 403, não insistiu); 5-tier = 5; 2-tier = 2; 1-tier = 1. **Todos respeitaram o cap exatamente.**
**A análise da curva está em `t6-curva-degradacao-2026-07-13.md`.** Este ficheiro é só o registo verbatim para avaliação cega.

---
---

# PATAMAR 10 PESQUISAS (verbatim)

Dez pesquisas gastas, WebFetch bloqueado (403 — não insisti). Tenho material suficiente para construir a tese. Segue-se o produto acabado.

## 0. Onde estou no terreno (auto-diagnóstico e regime)

Regime de inflexão: **emergente a industrializar**. Não é conjetura (a Itália corre clearance obrigatório desde 2019 — a prova de conceito existe e é pública); não é ainda plenamente industrial à escala europeia (a vaga de massa é 2026–2030). Estou no ponto exato em que a curva industrial acelera por decreto e a curva de preço ainda reflete a identidade legada das casas-mãe. É este desfasamento que persigo.

## 1. A restrição (o mecanismo)

Durante meio século o IVA europeu foi **autoliquidado e reportado à posteriori**: a empresa emitia a fatura, cobrava o imposto e, semanas ou meses depois, entregava uma declaração agregada. O Estado via a transação tarde, em bruto, e a fenda entre o devido e o cobrado — erro, omissão e sobretudo fraude carrossel/MTIC — drenava uma ordem de grandeza de **~€90–130 mil milhões/ano** (VAT compliance gap; ver nota de fidelidade sobre o número exato).

O modelo **Continuous Transaction Controls (CTC) / clearance obrigatório** inverte a física do problema. A fatura deixa de ser válida quando a empresa a emite: passa a ser válida **quando o Estado — ou um intermediário por ele certificado — a viu e libertou, em tempo quase real, num formato-máquina imposto**. O Estado sai da cadeira de auditor-depois-do-facto e senta-se **dentro do fluxo, como nó obrigatório**. Sem clearance não há fatura legal, não há pagamento, não há dedução de IVA a montante.

A restrição que está a ser esmagada é a **opacidade informacional do reporte periódico**. Mas — e é aqui que a tese vive — fechá-la cria uma restrição *nova* e mais dura: cada empresa em âmbito tem de, num **prazo legal que não controla**, ligar-se a uma **plataforma nacional específica**, num **formato específico**, e libertar **cada fatura** em tempo real. O gargalo desloca-se de "o Estado não vê" para **"27 regimes nacionais de clearance fragmentados"** — e o comércio transfronteiriço tem de os satisfazer a todos ao mesmo tempo, a convergir (ViDA, 2030/2035) mas ainda não convergidos.

Calendário (todos os factos: pesquisa de 17/07/2026):
- **ViDA adotado em 11/03/2025, em vigor 14/04/2025** (Comissão Europeia). A partir de 14/04/2025 os Estados-membros podem **impor faturação eletrónica B2B obrigatória sem derrogação da UE**. Reporte digital transfronteiriço intra-UE (EN 16931) obrigatório desde **1/07/2030**; convergência de todos os sistemas domésticos até **1/01/2035**. A CE estima corte de fraude "até €11 mil milhões/ano" e custos administrativos ">€4,1 mil milhões/ano" (materiais ViDA da CE — nota a condicionalidade "até").
- **Itália:** SdI em clearance desde 2019 (pioneiro; a prova).
- **Alemanha:** receção obrigatória desde jan/2025; emissão >€800K jan/2027; todos jan/2028.
- **Bélgica:** ao vivo desde **1/01/2026** — primeiro país a tornar o **Peppol o canal B2B exclusivo**, sem isenção por dimensão.
- **Polónia (KSeF):** promulgado 27/08/2025; obrigatório **1/02/2026** (>PLN 200m), **1/04/2026** (todos), micro jan/2027.
- **França:** **set/2026** todas recebem + grandes/médias emitem; **set/2027** PME emitem. PDP → **"Plateformes Agréées" (PA)**; **~101 PA certificadas**.

## 2. A transferência de valor — e a França como caso puro

A portagem cobra-se **por transação libertada e por ligação mantida**. Quem opera o **tubo certificado entre o ERP e cada plataforma governamental** cobra uma taxa sobre **cada fatura, para sempre, indexada ao volume** — a **camada de rede de faturação eletrónica**.

**Modo de falha:** o que parte quando o tema cresce é a **interoperabilidade** — 27 sistemas fragmentados + transfronteiriço. Quem vende a solução para o que parte tem a portagem mais defensável. Não é quem calcula o imposto; é quem opera a canalização.

**A França é a demonstração mais pura.** Ao abolir a função de troca do portal público gratuito (PPF) e encaminhar **todo** o tráfego B2B através de **plataformas privadas certificadas (PA/PDP)**, o Estado francês converteu, por decreto, um serviço público numa **rede de portagem privada-regulada** com ~101 operadores certificados.

## 3. Mapa de portagens: funções → empresas cotadas (tickers)

**Função A — Determinação/conteúdo regulatório:** **Thomson Reuters — TRI**; **Vertex — VERX**; **Wolters Kluwer — WKL**. *Sovos — privada (Hg). Não investível.*
**Função B — Conectividade de clearance / a rede certificada (a camada defensável):** **Pagero → dentro da TRI** (90.000 clientes, alcance 14M empresas, 87% receita recorrente; ~USD 800M / SEK 8,1B, jan/2024); **ecosio → dentro da Vertex (VERX)** (até ~$180M, ~$69M upfront, ≈5x receita → ~$14M/ano inferido); **Unifiedpost / Banqup — UPG** (pure-play, turnaround, dívida líquida €29,5m fim 2024, subs +8,2%/transação +9,3%); **TIE Kinetix — TIE** (small-cap, não obtive métricas). *Basware — privada; Comarch — **saiu de bolsa** 03/2025, deixou de ser veículo.*
**Função C — Embebida no ERP:** **SAP — SAP** (Document and Reporting Compliance, clearance nativo no S/4HANA).
**Função D — Distribuição às PME:** **Sage — SGE**; **Wolters Kluwer — WKL**; *Cegid — privada*; **Intuit — INTU** (menos exposta).

TAM direcional (ordem de grandeza): mercado global de e-invoicing **~$18–24B em 2025 → ~$60–70B até 2030–2034, CAGR ~16–20%**.

## 4. As duas curvas

**Curva industrial:** qualificação feita (101 PA; Peppol na Bélgica; KSeF em lei). Adoção→receita com go-lives de massa em 2026. **Sinal custoso:** incumbentes pagaram para possuir a rede antes do volume — TR ~$800M por Pagero, Vertex ~$180M por ecosio.
**Curva de preço:** TRI precificada como "informação legal", VERX como "sales-tax US", SAP como "cloud/IA", WKL como "publicação". **Nenhuma precificada como "operador CTC europeu"** — invisibilidade nominal / opacidade funcional.
**Desfasamento:** industrial sobe em calendário legal fixo; preço reflete o negócio antigo da mãe.

## 5. DECISÃO

A expressão mais pura (rede de clearance certificada, cotada, pure-play) **não é limpa**: os puros saíram de bolsa (Comarch), são privados (Sovos, Basware, Cegid) ou frágeis (Unifiedpost). Digo-o.

**1) Thomson Reuters (TRI) — a melhor expressão solvente.** Detém a maior rede de clearance multi-jurisdição cotada (Pagero) + ONESOURCE. Pagou ~$800M antes da vaga. Mudaria se: volumes da Pagero não escalarem com BE/PL/FR, ou valor migrar para Peppol aberto. **Auto-check:** *a Pagero cobra sobre o MESMO bem escasso? Sim. Limpo.*
**2) Vertex (VERX) — a mesma tese com mais torque.** Pure-play de imposto indireto que comprou a rede (ecosio); menor que a TRI, move mais a agulha. Mudaria se o crescimento ficar preso no sales-tax US. **Auto-check:** *núcleo é determinação (adjacente, não idêntico); coerência depende de acrescer via ecosio + e-invoicing, não sales-tax US. Coerência parcial — assinalada.*
**3) SAP (SAP) — expressão estrutural/embebida (moat, não gatilho).** DRC no S/4HANA; arredondamento no P&L de um título de cloud/IA.
**Menção obrigatória — Unifiedpost/Banqup (UPG):** a portagem pura e não diluída (cotada), mas micro-cap em turnaround, risco de balanço. Nomeio-a e assinalo a fragilidade do chassis — não a coloco no topo por isso, não por falta de pureza.

## 6. Rasto
**(a) Camadas** — *Observado:* ViDA 11/03/2025→14/04/2025→2030→2035; mandatos DE/BE/PL/FR; Pagero (~$800M, 90k/14M, 87%); ecosio (~$180M, ~5x); Comarch delistada 03/2025; Unifiedpost 27/02/2025 (net debt €29,5m). *Inferido:* receita ecosio ~$14M/ano; rede é a portagem defensável. *Convicção:* valor 2026-2030 acresce à rede certificada por transação, salvo comoditização Peppol. *Não obtive:* segmento e-invoicing isolado dentro de TRI/VERX/SAP; métricas TIE; preço/portagem por documento; VAT gap primário (WebFetch 403).
**(b) Falsificadores:** (1) comoditização via Peppol aberto; (2) desintermediação pelo Estado (modelo SdI público); (3) valor não escala com mandatos (volumes Pagero/ecosio/Banqup planos nos FY2026); (4) deslize de mandatos.
**(c) Previsões datadas:** FY2026 → degrau visível de volumes; 1/07/2030 clearance transfronteiriço; 2026-2028 vigiar atos de execução ViDA (interoperabilidade).
**(d) Percurso:** 10 WebSearch (ViDA; França/PA; Vertex/ecosio; TR/Pagero; DE/PL/BE; VAT gap; Comarch→delisting; Unifiedpost→Banqup; SAP DRC/Sovos/Basware; TAM). +1 WebFetch à CE: 403, não insisti.

## 7. Nota de fidelidade
- **Facto-charneira (VAT gap):** ~€90–130 mil milhões/ano — **apoiado apenas em fonte secundária** (VAT Gap 2024, Oxford Economics/CASE para a CE, devolveu €128B / 9,5%). Primário da CE deu **403**. Edições anteriores citaram ~€61–93B, logo o €128B pode ser reexpressão metodológica — **por confirmar**. Direção robusta; valor exato não certificado.
- Poupança de fraude "até €11 mil milhões/ano" — condicional "até" mantida, não achatada.
- **ecosio:** data de fecho ~2024 numa fonte, 8-K Vertex de 03/2025 — não reconciliei a data exata; valor consistente. Não é charneira.
- **Comarch** fora de bolsa desde 03/2025 — descoberta, não suposição.
- Tudo o não obtido nomeado como "não obtive".

---
---

# PATAMAR 5 PESQUISAS (verbatim)

Tenho o suficiente. Encerrei as cinco pesquisas. Antes, o auto-diagnóstico da Secção 8: não pergunto se a hipótese "pode existir" — estou num regime industrial com datas legais fixas; não exijo invisibilidade — mapeio portagens; e nomeio o que não obtive.

## 1. A restrição
O erro comum é "a faturação eletrónica está a crescer". O que se passa é que **o Estado se tornou parte obrigatória dentro de cada transação B2B** — unilateralmente, país a país, com formatos, modelos de clearance e calendários divergentes que só harmonizam em 2035. A restrição dura é jurídica: uma empresa **não pode legalmente emitir, receber ou deduzir IVA** sobre uma fatura que não passe por um canal certificado, estruturado e em tempo real. O bem escasso é **interoperabilidade juridicamente válida sobre uma superfície regulatória fragmentada e em movimento**.

Facto-charneira: o *VAT gap* da UE foi de **€89 mil milhões em 2022**, contra €121 mil milhões em 2018, e a Comissão Europeia (relatório de **18 de dezembro de 2024**) atribui o progresso à "digitalização dos sistemas fiscais, reporte em tempo real e faturação eletrónica" (fonte primária: CE, DG TAXUD). É auto-reforçador: o instrumento funciona, logo os Estados redobram.

**Gargalo a seguir:** à medida que o formato estandardiza (EN 16931, revisão EN 16931-1:2026 do CEN em março/2026), o gargalo desloca-se de "consegues produzir o ficheiro?" para "és um nó *certificado/acreditado* na rede?". A portagem passa a **acreditação + posição de rede**.

## 2. Mecanismo e modo de falha
Mandato → ligação não-opcional → portagem por transação/assinatura. Defensabilidade pelo **modo de falha**: fatura não-validada = IVA não dedutível, coima, tesouraria bloqueada. O fosso tem duas camadas: **conteúdo regulatório sobre 27 regimes divergentes** (opacidade funcional) e **acreditação** (licença de nó certificado).

## 3. Transferência de valor
De cada função AP/AR/fiscalidade para os operadores de plataforma certificada + motor de regras. Fluxo recorrente **fabricado pelo Estado e juridicamente compelido**.

## 4. Calendários
Regime **industrial**. Itália SdI 2019; Alemanha receção jan/2025, emissão faseada 2027-2028; Bélgica e Polónia (KSeF) 2026; **França 1/09/2026** grandes/médias emitem + todas recebem, PME 1/09/2027, canal via **Plateforme Agréée (PA)**, antes PDP (service-public.gouv.fr; Avalara/ecosio). [Inferência, a confirmar: PPF pública reduzida a concentrador — da memória de out/2024, não confirmado nesta corrida.] **ViDA** em vigor 14/04/2025; e-fatura EN 16931 intra-UE 1/07/2030; harmonização doméstica jan/2035. **A harmonização em 2035 significa que a fragmentação — e o valor do nó multi-país — persiste uma década.**

## 5. Duas curvas
**Industrial madura e a acelerar; sinal custoso inequívoco:** TR venceu guerra de licitações contra Vertex e Avalara e pagou **~$800M** pela **Pagero** (fev/2024; comunicado TR); Vertex, após perder, comprou **ecosio** (~$69M upfront + $76M earn-out + $35M ações; Accounting Today/CPA Practice Advisor, ago/2024). PE drenou o resto: **Esker** saiu de bolsa (OPA Bridgepoint/General Atlantic a €262/ação, ~€1,62B, delisting 3/03/2025); Basware (Accel-KKR 2022), Tungsten (Kofax 2022), Generix (Montefiore ~2024), Avalara (Vista 2022), Sovos (Hg), Edicom/Seeburger.
**Preço:** universo cotado a esvaziar-se — **edge: invisibilidade nominal + escassez de veículo.** Quase todas as pure-plays foram privatizadas 2022-2025 enquanto o precipício de 2026 se aproximava.
**Tensão (momentum como saturação vs confirmação):** direção trancada, timing irregular — França deslizou 2024→2026, Polónia deslizou. Vertex na call do 3T2025 sinalizou "contradições na adoção de e-invoicing e timing de migração de ERP para SAP". Digo-o em vez de esconder.

## 6. Funções → cotadas
Motor+reporte no ERP: **SAP** (DRC), **VERX**, **TRI** (ONESOURCE). **Nó certificado (a cabine):** ecosio→**VERX**; Pagero→**TRI**; **Cegedim — CGM**; **Comarch — CMR** (ver ressalva); **TIE Kinetix — TIE**; **Unifiedpost — UPG**. Conteúdo multi-país: Sovos [privado], VERX, TRI, SAP, **Wolters Kluwer — WKL**. Backbone: Peppol (OpenPeppol, sem fins lucrativos; monetiza nos access points).
Ressalva: **não obtive** o estado de cotação da **Comarch** após OPA família+CVC 2024 — incerta. **Avalara** já **não cotada**. **ecosio** descrita como sediada na Alemanha (memória situa-a em Viena) — não fixo o país.

## 7. DECISÃO
**Primária — Vertex (VERX).** Única cotada de dimensão quase-pure-play de tax-tech; com ecosio detém as duas funções (determinação + nó certificado europeu/Peppol). Vende a solução para o modo de falha. Herda escassez de veículo. Ponto na curva: início-industrial no e-invoicing (ecosio ~$10,8M ARR na aquisição; adoção grumosa por confissão da gestão no 3T2025), dentro de $748,4M receita / $671M ARR 2025 (8-K Vertex/SEC; cloud +27,9%). Sinal custoso: pagou pela ecosio dias após perder a guerra de $800M. Mudaria se ARR de e-invoicing não inflectir no ciclo França-2026/ViDA, ou SAP DRC + hyperscalers comoditizarem.
**Auto-check:** *mesmo bem escasso? Sim, mas parcialmente:* Vertex+ecosio cobra o canal+motor+conteúdo, mas **a maioria da receita ainda é sales-tax US, não CTC europeu** — o bem escasso é minoria (em crescimento). **VERX é o melhor proxy cotado, não puro.**
**Secundária — Thomson Reuters (TRI):** a maior cabine já comprometida (Pagero), mas gigante diversificado — portagem diluída e invisível na conta (invisibilidade nominal numa mega-cap).
**A mais pura, e por que não é limpa:** os pure-plays cotados extinguiram-se. Restam **Unifiedpost (UPG)** e **TIE Kinetix (TIE)** — os pure-plays Peppol mais limpos, alavancados à Bélgica-2026, mas a UPG está financeiramente aflita (venda de ativos; **não obtive** a atualização de solvência) e ambas micro-caps com risco de execução. Nomeio-as como a expressão mais pura *e* a menos limpa.

## Rasto
**Camadas** — *Observado:* VAT gap €89B 2022 vs €121B 2018 (CE 18/12/2024); ViDA 14/04/2025→2030→2035; França 1/09/2026 (service-public.gouv.fr; Avalara); Pagero ~$800M por TR batendo Vertex e Avalara (fev/2024); ecosio ~$69M+$76M+$35M (ago/2024); Esker delisted 3/03/2025 a €262/€1,62B; Vertex 2025 receita $748,4M/ARR $671M/cloud $352,9M/ecosio +$10,8M ARR (8-K SEC). *Inferido:* gargalo migra formato→acreditação; fragmentação até 2035 prolonga valor; PPF francesa reduzida a concentrador (memória, não reconfirmado). *Convicção:* esvaziamento do universo cotado + precipício de mandatos → valor de escassez para a única cotada quase-pura (VERX). *Não obtive:* split receita Vertex CTC-EU vs sales-tax US; estado Comarch pós-OPA 2024; solvência Unifiedpost; receita CTC dentro de SAP/WKL; país-sede ecosio.
**Falsificadores:** (1) mandatos-chave 2026 deslizam >12 meses; (2) SAP DRC/hyperscalers absorvem determinação+transmissão; (3) EN 16931 estandardiza depressa demais, dissolve a opacidade funcional; (4) M&A inverte, regressam IPOs de nós CTC.
**Previsões datadas:** até 1/09/2026 degrau de volumes nas PA/Peppol (visível no 2S2026 de ecosio/Vertex, Pagero/TR); até fim 2027 mais uma pure-play sai de bolsa; até 1/07/2030 nó certificado vira infraestrutura não-opcional, fragmentação persiste até 2035.
**Percurso:** 5 WebSearch (espinha ViDA; França 2026/PA; guerra Pagero+ecosio; encolhimento do universo/Esker delisting; VAT gap €89B + estado financeiro dos veículos). Sem WebFetch. **Fronteira dura respeitada.**

---
---

# PATAMAR 2 PESQUISAS (verbatim)

*Ver `scratchpad`/registo — reproduzido na íntegra abaixo.*

Tenho as duas confirmações de que precisava. Encerro a fase de pesquisa (2/2 WebSearch usadas) e entrego a tese.

## 1. A restrição
Não parto de "a faturação eletrónica está a crescer". A restrição real é a **cegueira informacional do Estado sobre a transação individual**. O *VAT gap* da UE ronda ~€90 mil milhões/ano (*número de memória, não confirmado nesta corrida — não é o meu facto-charneira*). O CTC remove a restrição por inserção: nos modelos de clearance a fatura não tem existência legal enquanto não passar pelo sistema do Estado ou intermediário certificado. O bem escasso passa a ser a **validade legal da própria fatura**.

**Facto-charneira (fonte primária — CE, lido via snippet):** ViDA adotado **11/03/2025**, em vigor **14/04/2025** → Estados podem impor e-invoicing B2B **sem derrogação**. A **1/07/2030** e-fatura EN 16931 obrigatória intra-UE B2B; alinhamento até **1/01/2035**.

## 2. Mecanismo
Clearance obrigatório → cada fatura por software/rede conforme. Edge no **modo de falha**: gargalo migra para **interoperabilidade sobre mosaico fragmentado** (~27 regimes: Itália SdI 2019, Polónia KSeF, França PDP, Alemanha receção-primeiro, Bélgica Peppol). **Fragmentação causal** pura. Caixa bloqueada = a portagem inelástica está na **camada de abstração de conformidade multi-jurisdicional**.

## 3. Funções → cotadas
Motor+rede (abstração): **Vertex — VERX** (alta no vetor incremental, base sales-tax US). Rede pura (Pagero) diluída: **Thomson Reuters — TRI**. Clearance no ERP: **SAP** (DRC). Conteúdo fiscal recorrente europeu: **Wolters Kluwer — WKL**. Trust/assinatura (Itália): **Tinexta — TNXT** (mix **não confirmado**). PME: **Sage — SGE** / Xero — XRO. Campeão polaco (KSeF): **Comarch — CMR**.
**Fora do alcance (absorvidos/privados — confirma a tese):** Sovos (Hg), Basware (Accel-KKR), Pagero (→TRI), ecosio (→Vertex), Edicom, Namirial, Seres/Docaposte, Generix, e — creio — Esker (OPA Bridgepoint/General Atlantic ~€262/ação; *não obtido/por confirmar*).

## 4. Duas curvas
**Sinal custoso:** jan/2024 TR pagou **~838 M$** por maioria da Pagero, **cobrindo oferta de ~555 M$ da Vertex** (Vertex 8-K; TR press release); Vertex comprou de imediato a ecosio. Antes, Basware/Sovos a privado. Estratégicos e PE em **guerras de licitação a pagar prémios** pelas cabines.
**Consequência:** a exposição pura foi comprada porque a portagem é real. Edge = ler qual diversificado tem maior pureza/margem incremental.
**Desfasamento:** certeza industrial datada + acesso público a colapsar → a cotada quase-pura sobrevivente herda valor de escassez. Regime **emergente → industrial**.

## 5. DECISÃO
**Primária — Vertex (VERX).** Melhor ajuste ao vetor incremental (ecosio). Sinal custoso: 555 M$ pela Pagero e, perdida, a ecosio. Mudaria se receita europeia de e-invoicing não virar segmento divulgado a acelerar, ou sales-tax US dominar o P&L.
**Auto-check:** *mesmo bem escasso? Parcialmente, e digo-o:* núcleo é sales-tax US (adjacente, distinto); a fatia coerente é a ecosio, real mas não maioritária. **Vertex é a melhor expressão cotada, não pura.** A perfeitamente coerente seria a **Pagero, presa dentro da TRI**. Não troco de tese; reconheço que o veículo mais puro foi retirado do mercado.
**Secundária — TRI** (ativo-rede mais puro, num conglomerado) e **Tinexta — TNXT** (mais direta sobre trust italiano, mas pequena/volátil/mix por confirmar; andaime, não edifício).
**Conclusão:** a expressão mais pura (Sovos/Pagero/Basware) **já não está limpa em bolsa** — comprada porque a portagem é verdadeira. **A indisponibilidade do pure-play é evidência confirmatória, não defeito.**

## Rasto
**Camadas** — *Observado:* ViDA 11/03/2025→14/04/2025→2030→2035; mandatos BE jan, PL fev, GR mar, FR set/2026, DE 2027-2028; TR/Pagero ~838M$ cobrindo Vertex ~555M$ (jan/2024); ecosio→Vertex; Sovos ~6B transações/ano. *Inferido:* fragmentação de 27 regimes é o fosso; M&A confirma a tese. *Não obtido:* delisting da Esker; mix Tinexta/InfoCert; VAT gap atual; economia por transação; split europeu da Vertex. *Não inventei valores.*
**Falsificadores:** (1) adiamento em massa (França>set/2026, Polónia suspende KSeF); (2) Estado desintermedia (portal público gratuito obrigatório); (3) EN 16931+Peppol comoditizam o fosso; (4) sinal custoso reverte (imparidade Pagero/ecosio).
**Previsões:** até fim 2026 França set-2026 + KSeF + Bélgica ao vivo (≥2 deslizes → falsificador #1); 2027 attach SAP DRC+Peppol nos resultados; 2030-07-01 evento terminal de procura; antes de 2027 mais uma pure-play cotada privatizada.
**Percurso:** 2 WebSearch (calendário regulatório → charneira; ações corporativas/veículos → guerra de licitação). Esker/Tinexta/WKL não confirmados nos snippets → conhecimento prévio/por confirmar. Sem WebFetch.

---
---

# PATAMAR 1 PESQUISA (verbatim)

Confirmado o facto-charneira (o calendário). Tenho o que preciso; não gastarei mais pesquisas.

## 0. Regime (não conjeturado)
**Regime industrial**: lei feita, sistemas em produção, go-lives *este semestre*. ViDA adotada **11/03/2025**; França **1/09/2026**; Polónia (KSeF) **1/02/2026** (fontes secundárias). A pergunta é "onde se desloca o gargalo e quem cobra portagem em cada país e entre países?".

## 1. A restrição
O bem escasso **não** é "software de faturação". É **conformidade transfronteiriça em tempo real sobre schemas divergentes**. Três restrições encaixadas: (1) **confiança** — o VAT gap (dezenas de milhares de milhões/ano; **memória/fonte secundária, por confirmar**) força a migração para clearance contínuo; (2) **fragmentação causal** — 27 schemas divergentes (clearance central IT/PL/RO, modelo "Y" com PDP privadas FR, receive-first DE); (3) **capacidade** — ViDA intra-UE B2B **1/07/2030**, harmonização **1/01/2035**: uma década de arbitragem de fragmentação, e depois prémio para quem detiver a rede pan-europeia. **Onde cresce o crescimento:** no **número de ligações país×formato×contraparte**, não no número de emitentes.

## 2. Mecanismo
O momento mais limpo é francês: em **out/2024 o Estado abandonou o portal público gratuito (PPF)** e **obrigou todas as empresas a contratar uma PDP privada certificada** — regulação que transforma uma obrigação legal numa **encomenda privada recorrente e mandatória**, proibindo a alternativa gratuita.

## 3. Mapa de portagens
**Achado central — invisibilidade nominal + mosaico:** os pure-plays foram **consolidados por PE e estratégicos em 2022–2024** enquanto a ViDA cristalizava — compromisso custoso a gritar; e a razão pela qual a expressão cotada é diluída.
Consolidados (o sinal): Avalara (→Vista 2022), Basware (→Accel-KKR 2022), Tungsten (→Kofax 2022), **Pagero (→Thomson Reuters 2024)**, **ecosio (→Vertex 2024)**, Sovos (Hg/TA).
Cotadas que restam: **Determinação:** Vertex — **VERX**; ONESOURCE dentro de **TRI**. **Rede de clearance:** ecosio dentro de **VERX**; Pagero dentro de **TRI**. **ERP:** **SAP** (DRC), **MSFT**, **ORCL**. **Software fiscal PME:** **WKL** (CCH), **Sage — SGE**. **Integrador nacional:** **Comarch — CMR** (exposição polaca pura, mas sob saída de bolsa/privatização CVC+fundadores; *por confirmar, não obtive o desfecho*).

## 4. Duas curvas
**Industrial a inflectir agora:** certificação de PDP/KSeF 2025-2026; volumes a acelerar 2026; onda PME (FR set-2027) multiplica emitentes de milhares para milhões. **Preço desligado:** VERX sobre sales-tax US, TRI sobre Legal/IA. **Desfasamento/edge:** os múltiplos pagos *em privado* pelos pure-plays revelam o valor da portagem pura; os múltiplos públicos não pagam esse prémio por opacidade funcional. Divergência de expectativas.

## 5. DECISÃO
**A expressão mais pura não é comprável — foi privatizada. Isso não anula a tese; é a tese.**
**Primária — Vertex (VERX):** determinação defensável + **opção europeia real via ecosio**, a inflectir 2026-2027. Sinal custoso: pagou pela ecosio (2024). Mudaria se a receita europeia (ecosio) não acelerar 2026-2027. **Auto-check:** *mesmo bem escasso? Parcialmente e honestamente:* ecosio cobra a portagem de conectividade europeia; determinação é adjacente; mas **a maioria da receita é imposto indireto dos EUA** — a Vertex está a *comprar o caminho* para o bem escasso, não é ainda um puro cobrador CTC-UE. Reconheço a impureza.
**Rede pura — TRI:** via Pagero detém a rede (o nó exato), mais ONESOURCE. **Auto-check:** *mesmo bem escasso? Sim no ativo (Pagero é a cabine), não no veículo* — fração pequena de um conglomerado comandado por outra coisa.
**Qualidade europeia — WKL e Sage — SGE:** portagem sobre conformidade em geral, europeia e recorrente, mas fatia CTC diluída; captam o tema, não a inflexão.
**Conclusão:** exigindo pureza absoluta, **nenhum veículo cotado é limpo — e digo-o.** Melhor par: **VERX** (primária) + **TRI** (rede pura diluída). O andaime a deitar fora era "há um pure-play europeu cotado à espera" — não há; o edifício que fica é "a fragmentação 2026-2030 é portagem real, os puros foram comprados, o desfasamento vive na opacidade funcional dos que restam".

## Rasto
**Camadas** — *Observado:* França 1/09/2026 (receção universal + emissão grandes/médias) e PME 1/09/2027, **PPF abandonado out/2024 → PDP obrigatórias** (Forbes/Lasernet/Novutech, nov/2025); Polónia KSeF 1/02/2026 (>200M PLN), todo B2B 1/04/2026, micro 1/01/2027 (CE + VATupdate); ViDA adotada 11/03/2025, intra-UE 1/07/2030, harmonização 1/01/2035; consolidação de pure-plays 2022-2024 (conhecimento próprio, corte jan-2026). *Inferido:* gargalo migra "emitir"→"reconciliar 27 schemas"→(pós-2030)"rede pan-europeia"; opção-CTC não reprecificada. *Convicção:* portagem real e defensável no nó de clearance/rede; impureza dos veículos é estrutural. *Não obtido:* VAT gap atual; desfecho Comarch; peso € da ecosio dentro da Vertex e da Pagero dentro da TRI; se a Alemanha adotará portal público central.
**Facto-charneira:** o calendário legal 2026→2030→2035. **Apoiado apenas em fonte secundária (agregadores + página da CE); por confirmar em fonte primária** (Journal Officiel FR, ustawa KSeF PL, Diretiva ViDA no JO da UE).
**Falsificadores:** (1) derrapagem de calendário (FR adia set-2026; PL suspende KSeF); (2) re-nacionalização (portal público gratuito); (3) comoditização por Peppol (access points a preço de custo); (4) internalização pelos ERPs (DRC incluído no S/4HANA base).
**Previsões:** fim 2026 maior inflexão de ligações/volumes da década (Pagero/TRI, ecosio/VERX, Comarch); 2027 onda PME multiplica emitentes; 1/07/2030 primeira portagem pan-europeia; +1 pure-play privatizado antes de 2030.
**Percurso:** parti do sinal regulatório → li a restrição → recuei à genealogia (Itália SdI 2019) → mapeei funções → **descobri a consolidação dos pure-plays 2022-2024** → conclui que a expressão cotada é diluída → decisão graduada, impureza declarada. Gastei a **única WebSearch** a confirmar o facto-charneira (o calendário), por ser o mais sensível ao tempo dado o corte de conhecimento jan/2026.
**Fronteira dura respeitada.**
