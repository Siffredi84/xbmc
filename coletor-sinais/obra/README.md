# Classe 7 — obra física (fila de interconexão elétrica)

## O sinal

Um projeto industrial pede ligação à rede **anos antes** de haver obra, encomendas ou
notícias. É um compromisso administrativo datado e público — sinal L2 na hierarquia do
motor ("permits obtidos").

**Mede-se energia FIRME** (gás, nuclear, geotérmica, carvão): é o que serve carga 24/7.
Solar e eólica não sinalizam procura industrial contínua da mesma forma.

**O sinal é a derivada**, não o nível: uma duplicação semestral numa região.

## Validação

`teste-retroativo-sinais-precoces-2026-08-06.md` — a fila virou no 1.º semestre de
2024; o operador só detetou o tema em outubro de 2025. **~18 meses de antecedência.**

## Estado atual (06/08/2026)

O coletor deteta sozinho três duplicações: 2022-S1, **2024-S1** (a que o teste
retroativo tinha encontrado à mão) e **2025-S1**. E mostra que a aceleração *continua*:
79,7 → 91,1 GW nos dois últimos semestres. MISO domina (+30,3 GW em 4 semestres);
PJM, a "data center alley", quase não aparece.

## Limitação decisiva: latência

O ficheiro do LBNL é **anual**. Isso reduz a antecedência prática de ~18 para ~5 meses.

Para latência **mensal** são precisas as filas dos ISOs — e todas exigem **registo
gratuito**, que esta sessão não pode fazer:

| Fonte | O que falta |
|---|---|
| **EIA** (`api.eia.gov`) | chave gratuita em eia.gov/opendata — **a mais fácil e valiosa** |
| **PJM** (`api.pjm.com`) | subscrição gratuita em pjm.com (o DataMiner web é uma app, não uma API) |
| ERCOT, CAISO | registo / parsing de relatórios |
| `interconnection.fyi` | aplicação web, sem API pública documentada |

Quando houver chaves, acrescentam-se como fontes adicionais — a métrica e a estrutura
do snapshot não mudam.

## Uso

```bash
python3 coletar_obra.py              # análise do ficheiro local
python3 coletar_obra.py --download   # buscar edição nova ao LBNL
```

**Nota de acesso:** as páginas do LBNL têm proteção Cloudflare (403), mas os ficheiros
em `/sites/default/files/` não. O script usa o caminho direto. Quando sair a edição de
2027, o URL segue o mesmo padrão.

O `.xlsx` (15 MB) não é versionado — o script descarrega-o quando falta.
