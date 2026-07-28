# Nota sobre esta pasta

Isto **não é código do Kodi**. É uma cópia de segurança, versionada, de um
skill pessoal do Claude Code (`~/.claude/skills/estudo-20-semanal/`), que
de outra forma viveria apenas num container efémero.

Para usar: copiar a pasta `estudo-20-semanal/` para `~/.agents/skills/`
(Codex) ou `~/.claude/skills/` (Claude Code), instalar as dependências e
exportar as variáveis de ambiente descritas na secção *Setup* do
[SKILL.md](SKILL.md). Nunca guardar chaves no repositório.

```bash
pip install pandas numpy requests yfinance matplotlib
cd scripts && python3 test_movers_study.py && python3 test_pipeline_offline.py
```

Discovery recomendado: `--provider auto --security-database /caminho/market.sqlite3`.
Se Polygon grouped não estiver incluído no plano, o motor cai para Yahoo e
marca o resultado como provisório; `--alpha-k-repo` reconcilia os movers de
maior amplitude em Polygon + Twelve Data.
