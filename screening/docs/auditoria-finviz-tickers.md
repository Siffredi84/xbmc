# Auditoria: tickers adulterados na extração do Finviz

**Data:** 29 de julho de 2026
**Veredicto:** o Finviz **não** publicou dados errados. O defeito é do parser — meu, e também da biblioteca Python mais usada para este fim.

---

## 1. Causa raiz — **confirmada**, confiança ~99%

Na célula do ticker, o Finviz renderiza um *placeholder* de logótipo que contém a **inicial do ticker** como fallback visual:

```html
<td data-boxover-ticker="ABOS" data-boxover-company="Acumen Pharmaceuticals Inc">
  <a class="company-ticker" style="--logo-url: url('https://logo.finviz.com/ABOS.svg')">
    <img src="https://logo.finviz.com/ABOS.svg" alt="ABOS logo" />
    <span>A</span>          <!-- ← inicial de fallback do logótipo -->
  </a>
  <a class="tab-link">ABOS</a>
</td>
```

`pandas.read_html` extrai **todo** o texto da `<td>` e concatena:
`"A"` + `"ABOS"` = **`AABOS`**.

Isto explica cada observação:

| Observação | Explicação |
|---|---|
| Duplicação da 1.ª letra | O `<span>` contém exatamente a inicial do ticker |
| 100% dos 178 símbolos afetados | Todas as linhas têm placeholder de logótipo |
| Nomes de empresa **corretos** | A coluna Company não tem `<span>` extra |
| Preços, RSI, volumes corretos | Idem — só a coluna Ticker é composta |
| `BBW → Babcock & Wilcox @ $8.83` | O ticker real é `BW`; **$8.83 é o preço correto de BW** |

O `BBW` foi um **falso positivo do meu diagnóstico**: colidiu por acaso com Build-A-Bear, um ticker real diferente. Foi essa colisão que me levou à conclusão errada de que os dados eram sintéticos.

### Hipóteses testadas e **eliminadas**
HTML/CSV incorreto do Finviz · página anti-bot ou CAPTCHA · alteração da estrutura da tabela · desalinhamento de colunas · transformação incorreta no DataFrame · bug de encoding ou serialização · adulteração pelo ambiente ou proxy · erro pós-extração.

**Evidência decisiva:** o HTML bruto (`v111.html`, 209 KB, guardado antes de qualquer processamento) contém `ABOS` em quatro sítios independentes — `href="stock?t=ABOS"`, `data-boxover-ticker="ABOS"`, `alt="ABOS logo"`, `logo.finviz.com/ABOS.svg`. A string `AABOS` **não existe no HTML**. Só aparece no DataFrame.

### Ponto exato de introdução do erro
```
HTTP bruto  →  HTML guardado  →  [pandas.read_html]  →  DataFrame
   ABOS ✅        ABOS ✅          ← AQUI              AABOS ❌
```

---

## 2. O mesmo bug afeta a biblioteca mais popular — **confirmado por teste direto**

Instalei e corri `finvizfinance` **1.3.0** (a mais mantida do ecossistema, [lit26/finvizfinance](https://github.com/lit26/finvizfinance)):

```
Ticker  Company                              Price
AAACI   Armada Acquisition Corp III          9.98   ← real: AACI
AAACO   Abony Acquisition Corp I             9.94   ← real: AACO
AAAME   Atlantic American Corp               1.60   ← real: AAME
AAARD   Aardvark Therapeutics Inc            6.42   ← real: AARD
AABAT   American Battery Technology Company  2.18   ← real: ABAT
AABOS   Acumen Pharmaceuticals Inc           2.28   ← real: ABOS
```

`AAME → AAAME` prova que a inicial é **prefixada incondicionalmente**, e não uma duplicação condicional.

**Não encontrei nenhum relato público deste padrão exato** (PyPI, GitHub issues, Stack Overflow, Reddit, Substack, fóruns). O `release.md` do finvizfinance regista várias correções genéricas de *"table parsing due to finviz side change"* (issue #84), mas nada sobre contaminação da coluna Ticker. Declaro-o explicitamente: **ausência de registo público, não ausência do problema.** A explicação mais provável é que o placeholder de logótipo é uma adição recente ao HTML do Finviz e que a maioria dos utilizadores destas bibliotecas trabalha com large-caps reconhecíveis, onde `AAAPL` salta à vista de imediato.

---

## 3. Comparação de métodos de extração

| Método | Oficial | Técnica | Bug do logótipo | Manutenção | Risco |
|---|---|---|---|---|---|
| `pandas.read_html` (o meu original) | — | scraping | **Sim** | n/a | frágil a qualquer mudança de HTML |
| `finvizfinance` 1.3.0 | Não | scraping + bs4 | **Sim (testado)** | ativa | herda o bug; abstrai o erro para longe do utilizador |
| `mariostoev/finviz` | Não | scraping | não testado | esporádica | provável mesmo bug |
| Finviz Elite `export.ashx` | **Sim** | CSV oficial | **Não** — CSV não tem HTML | n/a | **$39,50/mês**; testado: devolve página de upsell no plano gratuito |
| **Parser por atributo (recomendado)** | — | scraping + bs4 | **Não** | própria | ~40 linhas, sem dependências novas |

**Recomendação: não adotar biblioteca.** Nenhuma resolve o problema e todas afastam-te do HTML, onde o erro nasce. Popularidade não é fiabilidade — o teste acima é a prova.

Nota sobre termos de utilização: o Finviz não oferece API pública gratuita e o scraping vive numa zona cinzenta contratual. O `export.ashx` do Elite é o único caminho contratualmente limpo para volume. Vale considerar se isto passar a ser infraestrutura permanente.

---

## 4. Correção aplicada

### Correção mínima (uma linha de princípio)
**O ticker nunca vem do texto da célula.** Vem de `data-boxover-ticker`, com fallback para o `href="stock?t=..."`.

### Alternativa estrutural (implementada em `finviz_extract.py`)
Substituí `pandas.read_html` por um parser dedicado que:
- seleciona `table.screener_table` e lê cabeçalhos dos `<th>`;
- usa `find_all("td", recursive=False)` para não capturar tabelas aninhadas;
- lê ticker **e** nome da empresa dos atributos `data-boxover-*`;
- **aborta** se o número de células divergir do número de cabeçalhos.

Regra explicitamente **rejeitada**: remover a primeira letra quando as duas primeiras coincidem. Destruiria `AAPL`, `AAL`, `AAME`, `BBW`, `CCL`, `MMM`, `SSNC`, `TTD`. A correção nunca infere — lê a fonte certa.

---

## 5. Validação de identidade e gate fail-closed

`validate.py` confirma, por ticker, contra o Yahoo Finance: **símbolo + nome da empresa (fuzzy ≥ 0,60) + exchange US + preço dentro de 15%**. Se a taxa de validação não for 100%, levanta `IdentityError` e o pipeline **para**.

### Teste de regressão — 12/12 OK
Inclui as armadilhas: `AAPL` e `AAL` (dupla inicial legítima), `BW` **e** `BBW` (o par que causou o diagnóstico errado).

```
OK  AAPL  Apple Inc. @ NMS $340.08          OK  AI    C3.ai, Inc. @ NYQ $8.90
OK  AAL   American Airlines @ NMS $15.36    OK  SIGA  SIGA Technologies @ NGM $3.34
OK  BW    Babcock & Wilcox @ NYQ $8.83      OK  PACB  Pacific Biosciences @ NMS $1.39
OK  BBW   Build-A-Bear Workshop @ NYQ $35.31 OK  MBI  MBIA Inc. @ NYQ $5.46
OK  ABOS  Acumen Pharmaceuticals @ NMS $2.28 OK  BYRN Byrna Technologies @ NCM $3.97
OK  ACDC  ProFrac Holding Corp @ NMS $3.71   OK  XPOF Xponential Fitness @ NYQ $6.74
```

O gate apanhou um falso positivo próprio na primeira passagem — `Prelude Therapeutics Inc` vs `Prelude Therapeutics Incorporated` (similaridade 0,52). Corrigido acrescentando `incorporated` à lista de stopwords. **19/19 finalistas validados.**

---

## 6. Resultado do framework, agora com dados corretos

Universo: 946 → gates quantitativos: **77** → gates técnicos: **19** → validação de identidade: **19/19**.

Dados do fecho de terça, 28 de julho (mercado US fechado às 08:00 de Lisboa). Ficheiros: `clean_screen.csv` (178 linhas completas), `finalists.csv` (19).

Nota sobre a composição: `EAD` e `TSI` são *closed-end funds* e `ACGC` é um SPAC — o framework pede ações, pelo que devem sair antes da análise de fases 2-6.

---

## Factos, hipóteses e inferências

**Factos confirmados**
- O HTML bruto do Finviz contém os tickers corretos.
- `pandas.read_html` produz o ticker corrompido a partir desse HTML correto.
- O `<span>` com a inicial do logótipo está presente em todas as linhas afetadas.
- `finvizfinance` 1.3.0 reproduz o mesmo defeito (testado hoje).
- Os 19 finalistas passam validação cruzada de identidade contra o Yahoo.
- `sh_price_1to7` e `ta_rsi_os60` são silenciosamente ignorados pelo Finviz — só ranges pré-definidos são aceites.

**Inferências (alta confiança)**
- O placeholder de logótipo é uma adição relativamente recente ao HTML do Finviz.
- Qualquer pipeline que leia o ticker por texto de célula está afetado neste momento.

**Hipóteses (por verificar)**
- `mariostoev/finviz` sofrerá do mesmo problema — não testado.
- A ausência de relatos públicos deve-se ao viés de large-caps nos utilizadores destas bibliotecas.

**Não verificável neste momento**
- Data exata em que o Finviz introduziu o placeholder.
- Se o placeholder aparece em todas as vistas e locales.

---

## Fontes

- [finvizfinance — documentação](https://finvizfinance.readthedocs.io/en/latest/screener.html) e [release.md](https://github.com/lit26/finvizfinance/blob/master/release.md) — consultadas 29/07/2026
- [mariostoev/finviz — API não oficial](https://github.com/mariostoev/finviz) — consultada 29/07/2026
- [Finviz — screener e rodapé com opção Export CSV (Elite)](https://finviz.com/screener) — consultado 29/07/2026
- Evidência primária: `v111.html` e restantes capturas HTML, mais os testes reproduzíveis em `finviz_extract.py` e `validate.py`
