# vNext — núcleo E1

Pipeline novo, construído **lado a lado** com `codigo/`. O pipeline actual não
se toca: sem ele intacto não há shadow run, e sem shadow run não há Fase 5.
As três excepções autorizadas (D0-1, D0-2, D0-3, mais o D0-4 do mesmo épico)
estão aplicadas em `codigo/` porque são defeitos que afectam os dois.

## O que já existe

| Módulo | Ticket | Papel |
|---|---|---|
| `estados.py` | E1-1 | os sete estados, `Resultado`, transições proibidas, `avalia()` |
| `contratos.py` | E1-2 | schema de entrada/saída por fase, validado em runtime |
| `config.py` | E1-3 | limiares com `origem` declarada e gates provisórios bloqueados |

Nada mais. As fases A a G do plano ainda não têm código.

## As três regras que este núcleo impõe

**1. Um estado nunca vira outro.** `TRANSICOES_PERMITIDAS` só admite o `OK`
como origem — é o único estado que carrega um valor verificado. Um
indeterminado é terminal: o que falta não passa a existir porque uma etapa a
jusante lhe mudou o nome.

```python
Resultado.ausente("finnhub", "profile2 vazio").transita(
    Estado.FORA_DO_CRITERIO, "B2b")   # CoercaoProibida
```

**2. `Resultado` não tem valor de verdade.** `bool(r)` levanta. Um
`if resultado:` leria «não verificado» como «falso», que é a forma exacta das
seis falhas que originaram o princípio invariante.

**3. Um limiar provisório não é gate duro.** `valor("ECO_ALTO")` devolve 1,5
para uso como feature; `gate("ECO_ALTO")` levanta se não houver revisão
marcada. Critério de aceitação 7 da Fase 4, imposto pelo código e não pela
disciplina de quem escreve.

## Papéis e o que bloqueia

`avalia(resultado, papel)` responde a «este resultado bloqueia o candidato?»:

| Papel | OK | `FORA_DO_CRITERIO` | indeterminado |
|---|---|---|---|
| `ELEGIBILIDADE` | passa | bloqueia | **bloqueia** |
| `RED_FLAG` | passa | bloqueia | **bloqueia** |
| `FEATURE` | passa | passa | passa, com etiqueta |

É a tabela da Fase 3 §2 («red flag: bloqueia · feature: passa com etiqueta») e
o critério de aceitação 3 («zero aprovados com `DATA_*` num gate de
elegibilidade») no mesmo sítio.

## Contratos

Colunas a mais são permitidas — é a mitigação deliberada do risco «schema
demasiado rígido trava iteração» registado na Fase 4. O contrato diz o que a
fase seguinte tem direito a ler, não tudo o que a anterior pode escrever.
Colunas em falta são nomeadas na mensagem de erro.

```python
from vnext.contratos import UNIVERSO
UNIVERSO.valida(df)   # ContratoViolado: coluna(s) em falta: split_estado
```

## Correr os testes

```bash
cd screening && python3 -m pytest        # 85 testes, sem rede
```

## Nota sobre «seis estados»

A Fase 3 fala em seis estados e a tabela lista sete linhas. São seis **além do
`OK`** — `OK` está no enum por ser o único que autoriza uma decisão positiva e
por isso tem de ser representável. `test_estados.py` fixa as duas leituras.
