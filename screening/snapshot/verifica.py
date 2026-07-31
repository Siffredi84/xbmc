"""H-2 — congelar o snapshot: manifesto de hashes e verificacao.

O snapshot de 29-07 e 30-07 e a ancora de reprodutibilidade de toda a Fase 5.
Se um destes ficheiros mudar sem que ninguem repare, a divergencia medida entre
os pipelines A e B passa a medir outra coisa e nada o assinala.

    python3 snapshot/verifica.py            # verifica contra o manifesto
    python3 snapshot/verifica.py --escrever # (re)cria o manifesto

Reescrever o manifesto e uma decisao deliberada e tem de aparecer no diff do
git como tal. O modo por omissao nunca escreve.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
MANIFESTO = RAIZ / "MANIFESTO.json"
IGNORAR = {"MANIFESTO.json", "verifica.py", "__pycache__"}

#: A que sessao pertence cada ficheiro. O sufixo do nome e a fonte de verdade;
#: o que nao tem sufixo cobre as duas e fica marcado como tal.
SESSOES = {"2907": "2026-07-29", "3007": "2026-07-30"}


def sessao_de(nome: str) -> str:
    for sufixo, data in SESSOES.items():
        if sufixo in nome:
            return data
    return "2026-07-29+30"


def sha256(caminho: Path) -> str:
    h = hashlib.sha256()
    with open(caminho, "rb") as f:
        for bloco in iter(lambda: f.read(1 << 20), b""):
            h.update(bloco)
    return h.hexdigest()


def ficheiros() -> list[Path]:
    return sorted(p for p in RAIZ.rglob("*")
                  if p.is_file() and not any(x in p.parts for x in IGNORAR)
                  and p.name not in IGNORAR)


def constroi() -> dict:
    return {
        "descricao": "Snapshot congelado das sessoes de 29 e 30 de julho de "
                     "2026. Base da comparacao A vs B da Fase 5.",
        "regra": "Imutavel. Alterar um ficheiro invalida a Fase 5 inteira; "
                 "uma sessao nova entra como ficheiro novo, nunca por cima.",
        "ficheiros": {
            str(p.relative_to(RAIZ)): {
                "sha256": sha256(p),
                "bytes": p.stat().st_size,
                "sessao": sessao_de(p.name),
            } for p in ficheiros()
        },
    }


def verifica() -> tuple[bool, list[str]]:
    """(ok, problemas). Nao levanta: o chamador decide o que fazer."""
    if not MANIFESTO.exists():
        return False, [f"manifesto ausente: {MANIFESTO.name}"]
    esperado = json.loads(MANIFESTO.read_text())["ficheiros"]
    presentes = {str(p.relative_to(RAIZ)): p for p in ficheiros()}
    problemas = []
    for nome, meta in sorted(esperado.items()):
        p = presentes.pop(nome, None)
        if p is None:
            problemas.append(f"AUSENTE   {nome}")
            continue
        real = sha256(p)
        if real != meta["sha256"]:
            problemas.append(
                f"ALTERADO  {nome}: {meta['sha256'][:12]} -> {real[:12]}")
    for nome in sorted(presentes):
        problemas.append(f"NOVO      {nome} (nao esta no manifesto)")
    return not problemas, problemas


def main(argv: list[str]) -> int:
    if "--escrever" in argv:
        MANIFESTO.write_text(json.dumps(constroi(), indent=1) + "\n")
        n = len(json.loads(MANIFESTO.read_text())["ficheiros"])
        print(f"manifesto escrito: {n} ficheiros")
        return 0
    ok, problemas = verifica()
    if ok:
        n = len(json.loads(MANIFESTO.read_text())["ficheiros"])
        print(f"snapshot integro: {n} ficheiros conferem com o manifesto")
        return 0
    print("SNAPSHOT ALTERADO — a Fase 5 nao e reproduzivel neste estado:")
    for p in problemas:
        print("  " + p)
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
