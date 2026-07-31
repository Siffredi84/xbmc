# Auditoria das correções P1–P5

**Data:** 29 de julho de 2026 · **Base:** `screening-projeto-atualizado.tar`
**Método:** diff contra a versão anterior, leitura do código, execução da suite, e testes de comportamento com os casos reais e com casos-limite.

---

## Veredicto

**As cinco correções estão implementadas e fazem o que dizem.** Reproduzi a validação declarada: compila limpo, 6 testes passam, 21 asserções, sem rede, com stubs. Confirmei cada uma por comportamento e não por leitura.

Duas implementações vão além do que eu tinha pedido, e uma delas corrige um bug meu que eu não tinha detectado. Encontrei três defeitos novos, todos menores, e um problema de ordenação que afecta a validação de regressão prevista para a próxima corrida.

---

## P1 — Insider buying · **conforme, com uma decisão implícita não documentada**

Filtra `transactionCode == "P"`, janela de 30 dias vinda de `config.INSIDER_JANELA_DIAS`, e conta `A`/`M` separadamente em `transaccoes_nao_abertas_ignoradas` — o que preserva a informação em vez de a deitar fora. Bom.

**Foi mais longe do que eu tinha pedido, e a decisão é defensável mas não está registada.** As vendas passaram a contar apenas `transactionCode == "S"`; e o `descoberta.py` deixou de usar `saldo_insider`, passando a usar `accoes_compradas > 0`, com o comentário: *"uma venda não apaga o facto verificável de que houve uma compra P"*.

Concordo com a mudança — é o que resolve o caso TOI. Mas altera a semântica do sinal: deixou de ser "os insiders estão líquidos compradores" e passou a ser "houve pelo menos uma compra de mercado nos últimos 30 dias". São afirmações diferentes e a segunda é mais fraca. Deve ficar na secção 8 do handover como decisão tomada, não enterrada num comentário.

**Nota:** o `saldo_insider` sobrevive na saída mas já não alimenta nenhuma decisão. Ou se documenta como informativo, ou se remove.

## P2 — Market cap · **conforme, e apanhou um bug meu**

`calcula_market_cap()` usa `shareOutstanding × preço USD` como canónico, mantém o valor do Finnhub como comparador, e devolve `MCapEstado` ∈ {COERENTE, DIVERGENTE, SEM_COMPARADOR}. O `run.py` filtra por `MCapM` e reporta `market_cap_divergente` no resumo. Correcto.

**O achado que não era meu para reclamar:** a chave da cache do Finnhub não incluía os parâmetros do pedido. Só o endpoint e o símbolo. Consequência — uma resposta de insiders a 6 meses seria reutilizada num pedido a 30 dias, e o P1 devolveria dados da janela errada sem qualquer sinal. A correcção acrescenta um hash SHA-256 dos parâmetros ao nome do ficheiro.

Este bug estava no código que eu escrevi e passou-me na auditoria anterior. Teria silenciosamente anulado o P1.

## P3 — Reverse split · **conforme, com ressalva de robustez**

Passou para `polygon.reverse_splits()`, com paginação, janela de 365 dias no `config`, e detecção por dois caminhos — o campo `type == "reverse_split"` e a razão `split_from > split_to` — o que protege contra a mudança de esquema da API.

O contrato de falha está bem desenhado: `reverse_splits=None` produz `estado = "VERIFICACAO_INCOMPLETA"`, e o `run.py` exclui dos aprovados tudo o que não tenha `estado == "OK"`. Verifiquei os dois lados. Fiel ao princípio invariante.

**Ressalva:** o `except Exception` no `run.py` engole qualquer falha, incluindo um erro de programação. Nesse caso o pipeline não pára — degrada para "ninguém verificado" e exclui os 21 candidatos em bloco. É seguro, mas seria indistinguível de um dia sem splits. Apertar para as excepções de rede esperadas.

## P4 — Queda >80% sem recuperação · **conforme nos casos reais, frágil nos limites**

Testei com os cinco casos que produziram a especificação:

| Ticker | Máx. | Mín. | Resultado | Esperado |
|---|---|---|---|---|
| SUPX | −91,4% | +6,1% | exclui | ✅ |
| TLRY | −82,6% | +6,1% | exclui | ✅ |
| BYRN | −87,0% | +25,4% | mantém | ✅ |
| SIGA | −65,3% | +11,0% | mantém | ✅ |
| MIST | −65,0% | +7,0% | mantém | ✅ |

Fronteiras coerentes: `(-80,0 ; 15,0)` não exclui, `(-80,1 ; 14,9)` exclui.

**Defeito:** `queda_sem_recuperacao(None, 10.0)` levanta `TypeError`. Rebenta o pipeline em vez de etiquetar — exactamente o comportamento que o princípio invariante proíbe.

Na prática é inalcançável hoje, porque `enriquece()` já manda para `falhas` qualquer ticker sem `High52` ou `Low52`. Mas a protecção passou a depender de um invariante mantido noutro módulo, e ninguém o escreveu em lado nenhum. Devolver `None` (→ etiqueta) em vez de rebentar custa duas linhas.

## P5 — Filtro de bolsa · **conforme**

`fase0.py` verifica `type == C.TIPO_VALIDO` **e** `exch in C.EXCH_POLYGON`. O `TIPO_VALIDO` que estava definido e não usado ficou ligado. A garantia deixou de depender do comportamento implícito do endpoint.

---

## Defeitos novos

**N1 — `polygon.py` lê a chave no import.** `KEY = os.environ["POLYGON_KEY"]` está ao nível do módulo: `import polygon` rebenta sem credenciais. Os outros três módulos (`finnhub`, `fred`, `evento`) lêem dentro da função e comportam-se bem. Efeito prático: não se consegue inspeccionar, testar ou fazer lint do módulo sem exportar uma chave falsa — e a suite atual só passa porque define uma. Mover para dentro de `_get()`.

**N2 — `except Exception` demasiado largo** no bloco de splits do `run.py` (ver P3).

**N3 — `queda_sem_recuperacao` rebenta com `None`** (ver P4).

## Problema de ordenação que afecta a regressão prevista

O gate de queda corre na etapa 4 (posição 1765 do `run.py`); o EDGAR corre na etapa 9 (posição 4422). **O TLRY é excluído por queda sem recuperação antes de chegar ao teste de reverse split.**

Ambos os red flags o apanham, portanto o resultado final está certo. Mas o passo 3 da secção 12 do handover pede para confirmar que "o reverse split de TLRY é reconhecido" — e numa corrida normal ele **não aparece** na saída do EDGAR, porque já saiu do conjunto. A verificação tem de ser feita isoladamente, chamando `polygon.reverse_splits()` sobre o ticker, ou reordenando os gates.

Sem isto, o verificador vai concluir que o P3 falhou quando não falhou.

## Sugestão para o próximo passo

A suite de 6 testes cobre a lógica pura. **Nenhuma corrida live foi feita** — e o handover é honesto quanto a isso. Antes de correr a frio com chaves novas, sugiro:

1. Corrigir N1 (permite testar sem credenciais).
2. Corrigir N3 (duas linhas, restaura o invariante).
3. Ajustar o passo 3 da secção 12 para verificar o reverse split do TLRY isoladamente.
4. Só então a corrida a frio, pós-fecho.

Os números de regressão a esperar, dos testes desta sessão: insiders com compra P a 30 dias apenas **BYRN, ANIX, TOI**; exclusão por queda de **SUPX e TLRY**; **BYRN preservado**; **CRDL e SUPX** com `MCapEstado = DIVERGENTE`.
