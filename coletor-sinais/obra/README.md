# Classe 7 — obra física (geradores planeados + fila de interconexão)

## O sinal

Um projeto industrial pede ligação à rede e regista o gerador que vai construir **anos
antes** de haver obra, encomendas ou notícias. É um compromisso administrativo datado,
público e **assinado por uma entidade com nome** — sinal L2/L3 na hierarquia do motor
("permits obtidos"). Não é opinião nem guidance: custa dinheiro e expõe quem o faz.

**Mede-se energia FIRME** (gás, nuclear, geotérmica, carvão): é o que serve carga 24/7.
Solar e eólica não sinalizam procura industrial contínua da mesma forma.

**O sinal é a derivada e a difusão**, nunca o nível:

1. que região (autoridade de balanço) ganhou GW firmes planeados desde o retrato anterior;
2. que **entidades** aparecem pela primeira vez — a mesma lógica das 3-8 empresas
   distintas do coletor de vocabulário, aplicada a betão e turbinas;
3. que capacidade passou a **cancelada/adiada** — o falsificador, o sinal de reversão.

## Validação

`teste-retroativo-sinais-precoces-2026-08-06.md` — a fila virou no 1.º semestre de
2024; o operador só detetou o tema em outubro de 2025. **~18 meses de antecedência.**

## Duas fontes, dois papéis

| | **EIA-860M** (primária) | **LBNL** (secundária) |
|---|---|---|
| Frequência | **mensal** | anual |
| Latência | ~1-2 meses | ~5 meses |
| Cobertura | geradores planeados/cancelados | fila de interconexão completa (38k pedidos) |
| História | 2023-01 em diante (42 meses) | desde 2000 |
| Nomeia a empresa | **sim** (`Entity Name`) | não |
| Papel | **deteção** | história profunda e contexto |

A latência era a limitação declarada da versão anterior deste coletor — o LBNL anual
reduzia a antecedência prática de ~18 para ~5 meses. O EIA-860M resolve-a: é mensal e,
por ser publicado em arquivo, **a série histórica inteira estava disponível de
imediato** — não foi preciso esperar meses a acumular retratos.

### Nota sobre a API do EIA (testado, não serve para isto)

`api.eia.gov/v2/electricity/operating-generator-capacity` só expõe estados **operáveis**
(`OP`, `OS`, `SB`, `OA`) na faceta `status`. Não tem geradores planeados. A chave
`EIA_API_KEY` está no ambiente e funciona, mas o sinal precoce vive no Excel mensal, não
na API. O coletor usa o Excel; não precisa de chave.

## Uso

```bash
python3 coletar_obra.py                 # último mês + derivadas a 1/3/12 meses
python3 coletar_obra.py --backfill      # constrói a série mensal toda (2023-01 -> hoje)
python3 coletar_obra.py --mes 2025-06   # um mês específico
python3 coletar_obra.py --lbnl          # história profunda (fila LBNL, semestral)
```

Cada mês demora ~20 s (descarrega 13 MB, agrega, **descarta o xlsx**). Só os retratos
JSON (~6 KB cada) ficam versionados, em `snapshots/`.

**Nota de acesso:** o mês corrente vive em `/xls/`, os anteriores em `/archive/xls/`; o
script tenta os dois e valida o `Content-Type` — um pedido a um mês inexistente é
**redirecionado para a homepage do EIA com HTTP 200**, pelo que verificar só o código de
estado dá falsos positivos (67.094 bytes de HTML disfarçados de sucesso). As páginas do
LBNL têm Cloudflare (403), mas os ficheiros em `/sites/default/files/` não.

O `.xlsx` do LBNL (15 MB) não é versionado — o script descarrega-o quando falta.

## Ganhos de latência ainda por explorar

| Fonte | O que falta |
|---|---|
| **PJM** (`api.pjm.com`) | subscrição gratuita em pjm.com (o DataMiner web é uma app, não uma API) |
| ERCOT, CAISO | registo / parsing de relatórios |
| `interconnection.fyi` | aplicação web, sem API pública documentada |

As filas dos ISOs atualizam mais vezes do que o EIA-860M, mas o salto grande — de anual
para mensal — já está feito. Acrescentar um ISO é ganho incremental, não estrutural.
