# Proxy de valor — dados de mercado sistemáticos

## Porquê existe

A regra 4 do arquivo manda registar, em cada corrida, o fecho mais recente de cada
cartão entregue e do benchmark. Feito à mão, falhou duas vezes de maneiras diferentes:

- **05/08/2026:** o preço do Ibiden ficou por obter;
- **antes disso:** o arquivo registou uma divergência de fornecedor (FORM $110,21
  arquivado contra $107,11 numa série posterior) que obrigou à nota *"manter fonte
  consistente daqui em diante"*.

Este coletor é essa consistência: **uma fonte, uma janela, um método**, com o
instrumento resolvido gravado em cada retrato.

## O que mede

Retorno de cada posição **desde a data de entrega/promoção no arquivo** — não desde o
início do ano, não desde uma compra (não há compra: a fronteira descoberta ≠ execução
mantém-se) — contra o seu benchmark na mesma janela. A diferença é o excesso, em
pontos percentuais.

**O que isto não é:** não avalia teses. Um cartão pode cair com a tese intacta. Esta é
**uma** das duas curvas do método; a curva industrial vive nos invalidadores de cada
cartão, que se verificam à mão na Parte A da corrida.

## A guarda de símbolo — e porque existe

Na primeira execução, `SLX` devolveu o **VanEck Steel ETF (NYSE)**. A tese do funil
nuclear referia-se à **Silex Systems (ASX)**, a dona da GLE/PLEF. Um ETF de aço estava
a ser medido como opção de enriquecimento a laser, e o número parecia perfeitamente
plausível (+10,3%).

Por isso `carteira.json` aceita `exchange` e `moeda` por posição, e o coletor **compara
com o que o fornecedor devolveu**: se divergirem, a linha sai marcada `SUSPEITO` em vez
de passar. Posições sem declaração passam sem guarda — o que é honesto, mas é o estado
a evitar em qualquer nome fora dos EUA.

Testado nos quatro casos (correto / moeda divergente / bolsa divergente / não declarado).

## ADRs são proxies, e estão marcados como tal

`IBIDF` (Ibiden) e `SILXY` (Silex) são ADRs de balcão em USD, ambos pouco líquidos —
o SILXY negoceia **centenas de ações por dia**. Servem para medir *direção relativa*.
Não são a cotação oficial, e os valores históricos em ienes do arquivo **não são
comparáveis** com a série do ADR. A ressalva viaja no retrato e é impressa no output.

## Uso

```bash
python3 coletar_precos.py                    # retrato de hoje
python3 coletar_precos.py --desde 2026-07-01 # janela mais larga
```

Fonte primária **Twelve Data** (`TWELVEDATA_API_KEY`), reserva **Polygon**
(`POLYGON_API_KEY`); ambas as chaves já estão no ambiente. O plano gratuito limita a
8 pedidos/minuto, por isso o coletor espaça os pedidos — uma execução completa demora
cerca de 1,5 minutos.

**Yahoo/yfinance foi testado e rejeitado como fonte:** limita por taxa de forma
agressiva e imprevisível (a mesma chamada devolveu dados numa sessão e `429` noutra),
o que é inaceitável para uma série que tem de ser reproduzível.

## Manutenção

`carteira.json` acompanha o arquivo. Quando um cartão morre ou nasce: acrescentar, ou
marcar `"ativo": false` — **nunca apagar**, pela mesma razão que o arquivo não reescreve
histórico.
