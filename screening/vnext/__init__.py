"""Pipeline vNext — construido lado a lado com `codigo/`, que nao se toca.

Pacote (e nao modulos soltos como em `codigo/`) por uma razao pratica: os dois
pipelines tem `config.py` e o `import config` do pipeline actual nao pode
resolver para os limiares do vNext quando os dois estao no mesmo processo, como
acontece no harness de shadow run da Fase 5.
"""
