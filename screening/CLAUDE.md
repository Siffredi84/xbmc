# CLAUDE.md — funil de descoberta de small-caps

Contexto para retomar este projecto em Claude Code. Lê isto primeiro, depois `docs/HANDOVER.md` e `docs/fase4-plano-implementacao.md`.

---

## Porque o Claude Code muda o projecto

Três bloqueadores desapareceram só por mudar de ambiente:

| Bloqueador | No chat | No Claude Code |
|---|---|---|
| **C-2 — adaptador IBKR** (risco alto) | ferramentas MCP não chamáveis do Python; vNext em modo degradado permanente com o Yahoo | `ib_insync` + TWS Gateway resolve. **Deixa de ser critério de rejeição** |
| **H-1 — backfill de 181 sessões** (39 min) | contentor apaga-se entre sessões | job local, cache persiste |
| **H-2 — congelar snapshots** | irreprodutível | git / disco |

Também deixa de ser preciso passar chaves em prompts. **As cinco chaves que circularam no chat continuam por rodar — faz isso antes de qualquer coisa e põe as novas em `.env`.**

---

## Estado

```
codigo/     pipeline actual, P1-P5 + N4 + épico D0 completo (D0-1 a D0-4)
vnext/      núcleo E1: estados, contratos, config. Fases A-G por construir
snapshot/   dados de 29-07 e 30-07, congelados com MANIFESTO.json
docs/       auditorias + Fases 0 a 5 do vNext + registo-implementacao.md
tests/      âncoras do snapshot
```

`python3 -m pytest` a partir de `screening/` corre os 85 testes. Nenhum toca na
rede. `python3 snapshot/verifica.py` confirma que o snapshot não mudou — se
falhar, a comparação da Fase 5 deixou de ser reproduzível.

`pg_universe.json.gz` são 71 sessões de OHLCV do universo inteiro (13.479 tickers). Descomprime antes de correr.

**Não está aqui:** as caches brutas (`pg_cache` 111 MB, `edgar_cache` 62 MB, `fh_cache` 7,5 MB). São regeneráveis — o Polygon custa 13 s por sessão.

## Correr o pipeline actual

```bash
cd codigo && pip install -r requirements.txt
export POLYGON_KEY=... FINNHUB_KEY=... FRED_KEY=... MARKETAUX_KEY=... SEC_UA="nome email"
python3 run.py
```

A frio ~17 min (74 chamadas Polygon a 13 s). Com cache quente ~18 s.
**Só produz resultados determinísticos com o mercado fechado.**

---

## Primeiras tarefas, por ordem

**1. Rodar as chaves.** Fora de qualquer prompt. **Continua por fazer** — é a única acção urgente e nenhum trabalho de rede deve começar antes.

**~~2. Git + snapshot congelado.~~** Feito. `snapshot/MANIFESTO.json` + `verifica.py`, com teste de integridade.

**~~3. D0-1 e D0-2.~~** Feitos, com o D0-3 e o D0-4 do mesmo épico. Ver `docs/registo-implementacao.md`.

**4. H-1 — backfill de 181 sessões** (39 min, desatendido). Desbloqueia B-5 e E-2. **Exige `POLYGON_KEY` — bloqueado pela tarefa 1.**

**5. C-2 — adaptador IBKR com `ib_insync`.** Contrato `IBKRSource` já especificado na Fase 4. Precisa de TWS Gateway a correr. **Só recolhe spreads com o mercado aberto** (14:30-21:00 Lisboa) — em pre-market os spreads são artificialmente largos e não servem.

**6. D-1 — acções em circulação da SEC.** Ticket de maior risco: as cinco regras de semântica XBRL estão especificadas (`docs/fase3` §1) e **nenhuma foi validada**. Valida contra os casos conhecidos antes de ligar ao gate.

---

## Números que a implementação tem de reproduzir

Sobre o snapshot de 29-07. Se não baterem, algo mudou que não devia.

| Etapa | Esperado |
|---|---|
| Universo Polygon | 13.479 |
| `type=CS` + bolsa | 5.299 |
| Excluídos por split ≤90 d | 144 |
| Íntegros pós-quarentena | 4.784 |
| Preço $1-7 + volume acções | 860 |
| **+ gate USD >$1M** | **670** |
| Shortlist técnica | **48** |
| Após gates fundamentais | **26** |
| Setups | **2/1/1/4/6/12** |
| Residual | 46% |

**Nota:** a Fase 3 publicou 2/3/2/7/12/22 — está **errado**, corrigido na Fase 5 §0. Os testes de integração da Fase 4 têm de usar 2/1/1/4/6/12.

Casos de regressão: TOP → $78M (Finnhub diz $1.305M). AMIX → $52M (Finnhub diz $2,5M). NKLR → $540M, **excluído**. SNDL → `REVER` (nome desactualizado). Par `BW`/`BBW` resolve correctamente.

---

## O princípio que governa tudo

> **Dados em falta produzem etiqueta, nunca decisão.**

Saiu de seis falhas reais, todas com a mesma forma — uma ausência de dados disfarçada de facto sobre o mundo. Está codificado em quatro sítios e o vNext leva-o a seis estados distintos (`docs/fase3` §2), que **nunca podem ser coagidos uns nos outros**.

**Não relaxes um gate para "arranjar" um resultado estranho.** Todas as vezes que um candidato pareceu errado, a causa foi a fonte e não a calibração.

---

## O que este projecto ainda não sabe

Nenhuma medição feita até agora diz se os candidatos são **bons investimentos**. Tudo o que foi validado é coerência interna, cobertura de dados e explicabilidade.

Promover o vNext com base nos critérios da Fase 5 é uma decisão de engenharia. Para saber se selecciona melhor, é preciso correr os dois pipelines em paralelo **≥20 sessões** e medir retornos a 5, 10 e 20 dias. Isso é trabalho para o Claude Code, e não era possível no chat.
