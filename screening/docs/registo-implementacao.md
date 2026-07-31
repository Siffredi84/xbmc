# Registo de implementação

Sessão a sessão, o que foi construído e o que ficou por decidir. Complementa o
plano da Fase 4 — o plano diz o que fazer, isto diz o que está feito.

---

## 2026-07-31 — instalação, épico D0, núcleo E1, H-2

**Contexto:** primeira sessão em Claude Code. O projecto passou a viver em
`screening/` dentro do repositório, com git e testes.

### H-2 — snapshot congelado (P0, bloqueava toda a Fase 5)

`snapshot/MANIFESTO.json` regista os 13 ficheiros com SHA-256, tamanho e sessão
de origem. `snapshot/verifica.py` confere; `tests/test_snapshot.py` corre a
verificação em cada `pytest`. Reescrever o manifesto exige `--escrever` e
aparece no diff.

O que isto resolve: as medições de 29-07 e 30-07 deixam de depender de um
contentor que se apaga. O que isto não resolve: as caches brutas (`pg_cache`,
`edgar_cache`, `fh_cache`) continuam fora — são regeneráveis, mas regenerá-las
custa uma corrida a frio.

### Épico D0 — quatro defeitos de robustez

Únicas alterações autorizadas ao pipeline actual durante a migração, porque
afectam os dois pipelines.

| Ticket | Antes | Depois |
|---|---|---|
| D0-1 | `polygon.py` lia `POLYGON_KEY` no import | `_chave()` lê no momento da chamada de rede; `import polygon` sem credenciais funciona |
| D0-2 | `queda_sem_recuperacao(None, x)` → `TypeError` | devolve `None`; o `run.py` passa a ter três filas — reprovado, limpo, **não verificado** |
| D0-3 | `except Exception` no bloco de splits | `except (requests.RequestException, RuntimeError)`; um erro de código volta a rebentar |
| D0-4 | backoff SEC de 5 tentativas, tecto 16 s (31 s no total) | 8 tentativas, tecto 60 s, jitter de 25% — ~3 min de paciência |

**O D0-2 tinha uma segunda metade que o ticket não mencionava.** Devolver
`None` sem mexer no chamador teria partido o `run.py`, onde `~e.queda_sem_recuperacao`
não sobrevive a um `None`. Pior: a correcção óbvia — tratar a ausência como
`False` — seria exactamente a falha que o princípio invariante proíbe, um
52 semanas que o Finnhub não devolveu a disfarçar-se de «não houve colapso».
Os não verificados saem agora em `queda_nao_verificada` no `saida_resumo.json`
e não entram nos finalistas.

### Épico E1 — núcleo de estados e contratos (P0)

`vnext/` é **pacote**, ao contrário de `codigo/` que são módulos soltos. Não é
estilo: os dois pipelines têm `config.py` e o `import config` do pipeline actual
não pode resolver para os limiares do vNext quando ambos correm no mesmo
processo — que é precisamente o que o harness de shadow run da Fase 5 vai fazer.

- **E1-1 `estados.py`** — sete estados (seis além do `OK`), `Resultado`
  imutável com fonte e proveniência obrigatórias, `transita()` como única forma
  de mudar de estado. Só o `OK` é origem de transições; os indeterminados são
  terminais. `bool(Resultado)` levanta.
- **E1-2 `contratos.py`** — seis contratos (A, B, C, D, E, G) validados em
  runtime. Colunas a mais permitidas, colunas em falta nomeadas na mensagem.
- **E1-3 `config.py`** — 37 limiares (14 documento, 13 decisão, 4 medição,
  6 provisório), cada um com `origem` ∈ {documento,
  decisão, medição, provisório}. `gate()` recusa provisórios sem revisão
  marcada; `valor()` não.

85 testes, nenhum toca na rede.

### Verificação da correcção da Fase 5 §0

`snapshot/setups_3007.csv` contém os 48 sobreviventes técnicos com a
classificação. Confirmado contra o ficheiro:

- a distribuição **2/3/2/7/12/22 está correcta para os 48** — o erro da Fase 3
  foi apresentá-la como a taxonomia da população elegível;
- os 14 candidatos nomeados na correcção têm no ficheiro exactamente os setups
  que a Fase 5 lhes atribui;
- os que caem nos gates fundamentais são consistentes com 2/1/1/4/6/12 sobre
  26, e 12/26 = 46,2%;
- **NG e OPK são setup 2 no ficheiro** e caem nos gates fundamentais. É por
  isso que os setups 1 e 2 dão três candidatos e não cinco, e é por isso que a
  restrição 4.3 continua viva.

O total corrigido (26) **não é verificável só com este ficheiro** — exige o
épico D. Fica para os testes de integração.

### Decisões tomadas nesta sessão

1. **Contratos permissivos quanto a colunas extra.** Mitigação explícita do
   risco registado na Fase 4 («schema demasiado rígido trava iteração»).
2. **`OK` no enum de estados**, apesar de a Fase 3 dizer «seis». São seis além
   do `OK`; sem o representar não há como exprimir «verificado e dentro do
   critério».
3. **Uma sequência de registos vazia passa qualquer contrato.** As colunas
   viajam nos registos; sem registos não há schema para verificar, e uma
   corrida de zero candidatos é um resultado legítimo (critério 8). Um
   DataFrame vazio declara colunas e continua a ser verificado.
4. **Elegibilidade e red flag têm a mesma regra** — só `OK` passa. A diferença
   está na razão registada, não no efeito.

### Por decidir — e não é decisão minha

- **A zona morta do `Eco`** (Fase 3 §4, opções (a) e (b)). O `config.py` do
  vNext regista `ECO_ALTO`, `ECO_BAIXO` e `RVOL_SETUP4` como **provisórios com
  revisão a 5 sessões**, o que os deixa utilizáveis como gate mas assinalados.
  Se a decisão for (b) — a zona morta não é setup — os três passam a decisão e
  a nota muda.
- **Rodar as cinco chaves.** Bloqueia H-1, C-2, D-1 e qualquer corrida a frio.

### Estado dos tickets

```
D0-1 ✅  D0-2 ✅  D0-3 ✅  D0-4 ✅
E1-1 ✅  E1-2 ✅  E1-3 ✅
H-2  ✅
H-1  ⛔ bloqueado por credenciais
A-1 … G-4  por fazer
```
