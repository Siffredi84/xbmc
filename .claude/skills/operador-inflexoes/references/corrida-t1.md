# Corrida T1 — procedimento da corrida semanal do Motor de Inflexões

A corrida T1 é o teste longitudinal do framework: a única medição que compara as teses com a realidade no tempo. Cada corrida é um ponto de dados numa série que **não pode partir-se** — por isso o procedimento começa sempre por ler o estado anterior e termina sempre por persistir o novo. A definição canónica das fases e gates está em `motor-engine.json` (neste diretório); este ficheiro é o procedimento operacional.

## Localização do estado

O estado vivo está no repo do projeto: branch `claude/handoff-audit-0w2a31` de `siffredi84/xbmc`, ficheiros `arquivo-inflexoes.md` (o diário imutável) e `corrida-inflexoes-AAAA-MM-DD.md` (uma por corrida). Se o repo não estiver disponível na sessão, pede ao utilizador acesso ou entrega o output como ficheiros locais com aviso claro de que a série canónica vive no repo.

## Sequência

**0. Preparar.** `git fetch` + checkout do branch. Confirmar que `arquivo-inflexoes.md` e o motor estão presentes. Nunca trabalhar de memória quando o arquivo está disponível.

**1. Ler o estado.** Ler `arquivo-inflexoes.md` na íntegra e a corrida anterior: que temas estão vivos e em que estado (qualificado / maduro / morto), que cartões existem (entregues / retidos), que prazos de reavaliação e ações de desbloqueio estão pendentes, que invalidadores há para verificar, qual o baseline do proxy de valor.

**2. Tratar PRIMEIRO as ações pendentes.** Antes de qualquer descoberta nova:
- prazos de reavaliação vencidos (ex.: marcadores de transição de gradiente) — reavaliar e registar;
- ações de desbloqueio de cartões retidos — tentar; **regra das 2 falhas: à segunda tentativa falhada de desbloqueio, o cartão morre** (registado, nunca apagado);
- verificação dos invalidadores de cada cartão entregue — para cada um, registar "disparou" ou "não disparou" com a evidência; um sinal *reforçador* novo também se regista;
- calendário de eventos (earnings, etc.) — confirmar datas, notar as que se aproximam;
- proxy de valor — registar o fecho mais recente disponível de cada cartão entregue e do benchmark.

**3. Descoberta (fases 0-5 do motor).** Correr as fases com pesquisa web live, orçamento ~10-15 WebSearch (WebFetch pode estar bloqueado no gateway — se der 403, não insistir). As regras de honestidade do motor não são opcionais, porque o valor da série está na sua auditabilidade:
- cada sinal contado carrega **fonte + data**;
- o que não se obteve declara-se **"NÃO OBTÍVEL"** — nunca se preenche com um valor plausível;
- sinais de nível **L1 nunca contam** (guidance, price targets, artigos de opinião);
- um **cartão sem calendário** de eventos confirmado fica **RETIDO** com uma ação de desbloqueio nomeada — nunca se inventa uma data para o entregar;
- **nenhum tema novo qualificado é um resultado válido** — o motor é um gate, não um gerador de novidade obrigatória; qualificar um tema maduro só para "ter output" é teatro.

**4. Persistir.** Gravar `corrida-inflexoes-AAAA-MM-DD.md` (data de hoje) com: restrições declaradas, Parte A (ações pendentes tratadas), Parte B (descoberta), Parte C (estados atualizados + calendário + métricas), fontes. Atualizar `arquivo-inflexoes.md` respeitando as suas regras: **acrescentar, nunca reescrever histórico**; transições de estado com justificação datada; tentativas de desbloqueio registadas uma a uma. Commit com mensagem descritiva + push ao branch (retry com recuo exponencial em falha de rede).

**5. Reportar.** No fim, resumir ao utilizador APENAS as mudanças de estado materiais: teses que avançaram/caíram, invalidadores que dispararam, cartões novos/mortos/desbloqueados, transições de regime. Não narrar passos rotineiros.

## Formato de referência

As corridas #1 (`corrida-inflexoes-2026-07-11.md`) e #2 (`corrida-inflexoes-2026-07-17.md`) no repo são o padrão de formato — em caso de dúvida sobre estrutura ou nível de detalhe, imitar a #2.

## Disclaimer obrigatório

Todo o output de corrida inclui: research/watchlist, não é aconselhamento financeiro; sem níveis de entrada, stops ou sizing (fronteira descoberta ≠ execução).
