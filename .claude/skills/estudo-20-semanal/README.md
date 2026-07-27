# Nota sobre esta pasta

Isto **não é código do Kodi**. É uma cópia de segurança, versionada, de um
skill pessoal do Claude Code (`~/.claude/skills/estudo-20-semanal/`), que
de outra forma viveria apenas num container efémero.

Para usar: copiar a pasta `estudo-20-semanal/` para `~/.claude/skills/`,
instalar as dependências e criar o ficheiro de chaves local descrito na
secção *Setup* do [SKILL.md](SKILL.md).

```bash
pip install pandas numpy requests yfinance matplotlib
cd scripts && python3 test_movers_study.py && python3 test_pipeline_offline.py
```

Nenhuma chave de API é guardada aqui — ver *Setup* no SKILL.md.
