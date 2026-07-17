# Kit ChatGPT — template de semente para pares de variância de mente

## Para que serve

Correr o operador numa mente diferente (ChatGPT ou outro LLM) com a MESMA semente usada no lado Claude, para isolar a variável "mente". O programa de testes provou que este par é o resultado mais valioso do framework: mentes diferentes convergem na *estrutura* do raciocínio e divergem no *conteúdo* (domínios e picks) — é assim que se verifica que o perfil transmite método, não um resultado decorado.

## Regras de construção do kit

1. **A Parte II entra íntegra e verbatim** — copiar de `perfil-parte-ii.md` (deste diretório), da linha `# PARTE II — O PERFIL` até ao fim, SEM o cabeçalho de proveniência em comentário HTML. Nunca resumir nem adaptar "para caber": o temperamento vive no texto completo.
2. **Paridade de par:** se o objetivo é comparar com uma corrida Claude já feita, a semente tem de ser **byte a byte igual** à que o lado Claude recebeu — incluindo a MESMA data no mandato (a data da corrida original, não a de hoje). Mudar a data introduz uma segunda variável (notícias diferentes) e contamina a comparação. Se o objetivo é uma corrida independente (não um par), usar a data de hoje e dizê-lo.
3. **O mandato** declara: a data; "produz a tua primeira tese"; a escolha do tema (livre, ou com regra de regime/âmbito se se quiser forçar terreno — ver os padrões abaixo); o que se mantém intacto (fronteira factual, graduação de convicção, fecho em recomendação com auto-check, tickers, descoberta≠execução); pesquisa web livre; português de Portugal; entrega como texto na resposta final.

## Esqueleto do bloco colável

```
──────────────────────────────────────────
COLAR A PARTIR DAQUI (sessão limpa):

És o operador descrito no documento de identidade que se segue. Habita este documento
como identidade — não é uma lista de instruções a executar, é quem tu és. Depois do
documento vem o teu mandato.

═══════════════════════════════════════════
DOCUMENTO DE IDENTIDADE — O PERFIL
═══════════════════════════════════════════

[← AQUI entra a Parte II INTEGRAL, verbatim, de perfil-parte-ii.md]

═══════════════════════════════════════════
O TEU MANDATO
═══════════════════════════════════════════

Hoje é [DATA]. Produz a tua primeira tese. [Escolha livre OU regra de regime/âmbito.]

[Regras que se mantêm: fronteira factual (facto com fonte+data; inferência marcada;
"não obtive" em vez de valor plausível); convicção graduada com regime declarado;
fecho numa recomendação derivada da tese com o auto-check de coerência, mapeada a
empresas cotadas com tickers; fronteira dura descoberta≠execução — nada de entradas,
stops, sizing ou timing. Tens pesquisa web — usa-a livremente. Entrega como texto na
tua resposta final, português de Portugal, sem limite de profundidade.]

FIM DO BLOCO.
──────────────────────────────────────────
```

## Padrões de restrição testados (usar como modelos quando o utilizador quiser forçar terreno)

- **Regime conjeturado** (padrão T10): a inflexão tem de estar em anomalia+mecanismo, AINDA SEM convergência de compromissos custosos; se o operador se der conta de estar a enumerar capex comprometido e contratos plurianuais, escolheu regime industrial — deve recuar na curva. Excluir os universos já mapeados como industriais (a definir conforme o momento).
- **Domínio não-físico** (padrão T11): o bem escasso NÃO pode ser físico (fábrica, material, energia, hardware, molécula) — tem de ser regulatório, informacional, de confiança/certificação, de distribuição/licenciamento, comportamental ou de balanço. Declarar que é fronteira de âmbito do mandante, não restrição ao modo de pensar.

## Instruções de execução (dar ao utilizador junto com o kit)

Chat temporário / memória desligada; browsing ligado; colar SÓ o bloco; **um único turno, sem treinar nem corrigir**; se o modelo perguntar "que tema?", responder "a escolha é tua, respeitando a regra desta corrida"; trazer o output **verbatim** de volta para avaliação cega.

## Quando o output voltar

1. Arquivar o output verbatim (sem edição além de formatação ilegível, declarada);
2. Avaliar às cegas contra `grelha-avaliacao.md` num passo separado;
3. Se for par de uma corrida Claude: comparação mente-vs-mente (domínio, picks, estrutura do raciocínio, fidelidade, facto-charneira) — declarar caveats de paridade de ferramenta (ex.: Deep Research dá mais fontes por ferramenta, não por mente; descontar);
4. Registar no arquivo do projeto se disponível.
