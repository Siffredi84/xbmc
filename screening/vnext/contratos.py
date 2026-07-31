"""E1-2 — contratos de entrada e saida por fase, validados em runtime.

O funil actual passa DataFrames entre etapas e descobre uma coluna em falta
tres etapas a jusante, sob a forma de um KeyError ou — pior — de um NaN que
atravessa um filtro em silencio. Um contrato transforma isso numa falha com
nome, no sitio onde a coluna devia ter sido produzida.

Risco reconhecido na Fase 4: um schema demasiado rigido trava a iteracao. A
mitigacao esta no desenho — **colunas a mais sao permitidas**. O contrato diz o
que a fase seguinte tem direito a ler, nao tudo o que a anterior pode escrever.

Referencia: docs/fase3-especificacao-vnext.md §1.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Iterable, Sequence

from vnext.estados import Estado

MAX_EXEMPLOS = 5


class ContratoViolado(ValueError):
    """Dados nao cumprem o contrato. A mensagem nomeia sempre a coluna."""


@dataclass(frozen=True)
class Coluna:
    nome: str
    tipo: type | tuple[type, ...] | None = None
    obrigatoria: bool = True
    dominio: Callable[[Any], bool] | frozenset | None = None
    nota: str = ""

    def aceita(self, v) -> bool:
        if v is None:
            return not self.obrigatoria
        if self.tipo is not None and not isinstance(v, self.tipo):
            # bool e subclasse de int em Python; um True num campo numerico e
            # quase sempre um bug de construcao, nao um 1.
            return False
        if isinstance(v, bool) and self.tipo in (int, float, (int, float)):
            return False
        if self.dominio is None:
            return True
        if isinstance(self.dominio, frozenset):
            return v in self.dominio
        return bool(self.dominio(v))


@dataclass(frozen=True)
class Contrato:
    nome: str
    colunas: Sequence[Coluna]
    chave: str = "Ticker"
    nota: str = ""

    @property
    def nomes(self) -> list[str]:
        return [c.nome for c in self.colunas]

    def valida(self, dados, *, amostra: int | None = None):
        """Valida e devolve os dados intactos, para encadear.

        Aceita DataFrame do pandas ou sequencia de dicionarios — os testes
        unitarios nao precisam de pandas para exercitar um contrato.
        """
        registos, colunas = _normaliza(dados)
        if colunas is None:
            # Sequencia de registos vazia: as colunas viajam nos registos, e
            # nao ha registos. Nao ha schema para verificar e uma corrida de
            # zero candidatos e um resultado legitimo (criterio 8). Um
            # DataFrame vazio ja declara colunas e continua a ser verificado.
            return dados

        em_falta = [n for n in self.nomes
                    if n not in colunas and _obrigatoria(self, n)]
        if em_falta:
            raise ContratoViolado(
                f"contrato {self.nome}: coluna(s) em falta: "
                f"{', '.join(sorted(em_falta))}. "
                f"Presentes: {', '.join(sorted(colunas)) or '(nenhuma)'}")

        if self.chave and self.chave not in colunas:
            raise ContratoViolado(
                f"contrato {self.nome}: chave {self.chave!r} ausente")

        alvo = registos if amostra is None else registos[:amostra]
        problemas: list[str] = []
        for col in self.colunas:
            if col.nome not in colunas:
                continue
            maus = [(_id(r, self.chave), r.get(col.nome))
                    for r in alvo if not col.aceita(r.get(col.nome))]
            if maus:
                exemplos = ", ".join(f"{t}={v!r}" for t, v in maus[:MAX_EXEMPLOS])
                problemas.append(
                    f"{col.nome}: {len(maus)} valor(es) fora do contrato "
                    f"[{exemplos}]" + (f" — {col.nota}" if col.nota else ""))
        if problemas:
            raise ContratoViolado(
                f"contrato {self.nome}: " + " | ".join(problemas))

        if self.chave:
            vistos, repetidos = set(), set()
            for r in registos:
                k = r.get(self.chave)
                (repetidos if k in vistos else vistos).add(k)
            if repetidos:
                raise ContratoViolado(
                    f"contrato {self.nome}: {self.chave} repetido: "
                    f"{sorted(repetidos)[:MAX_EXEMPLOS]}")
        return dados


def _obrigatoria(contrato: Contrato, nome: str) -> bool:
    return next(c.obrigatoria for c in contrato.colunas if c.nome == nome)


def _id(registo, chave):
    return registo.get(chave, "?") if chave else "?"


def _normaliza(dados) -> tuple[list[dict], set[str] | None]:
    """(registos, colunas). Colunas a None significa 'indeterminavel'."""
    if hasattr(dados, "columns") and hasattr(dados, "to_dict"):
        return list(dados.to_dict("records")), set(map(str, dados.columns))
    if isinstance(dados, Iterable):
        registos = list(dados)
        if not registos:
            return [], None
        if not all(isinstance(r, dict) for r in registos):
            raise ContratoViolado("dados tem de ser DataFrame ou sequencia de "
                                  "dicionarios")
        colunas: set[str] = set()
        for r in registos:
            colunas |= set(r)
        return registos, colunas
    raise ContratoViolado(f"tipo de dados nao suportado: {type(dados).__name__}")


# -- predicados reutilizaveis -------------------------------------------------
def intervalo(minimo, maximo):
    return lambda v: minimo <= v <= maximo


def positivo(v) -> bool:
    return v > 0


def um_de(*valores):
    return frozenset(valores)


ESTADOS = frozenset(e.value for e in Estado)

# -- contratos por fase -------------------------------------------------------
# FASE A — universo. Saida de `vnext/universo.py`.
UNIVERSO = Contrato("A/universo", [
    Coluna("Ticker", str),
    Coluna("type", str, dominio=um_de("CS")),
    Coluna("exch", str, dominio=um_de("XNAS", "XNYS", "XASE")),
    Coluna("nome", str),
    Coluna("split_estado", str,
           dominio=um_de("SEM_SPLIT", "RECENTE", "EXCLUIDO_SPLIT_RECENTE"),
           nota="A3 e a raiz contaminante: sem splits verificados nenhum "
                "indicador a jusante e interpretavel"),
    Coluna("split_ultima_data", str, obrigatoria=False),
    Coluna("serie_estado", str,
           dominio=um_de("OK", "INTERRUPCAO", "SERIE_CURTA", "ILIQUIDEZ")),
    Coluna("sessoes_em_falta", int, dominio=lambda v: v >= 0),
])

# FASE B — gates tecnicos. Saida de `vnext/gates.py`.
SHORTLIST = Contrato("B/shortlist", [
    Coluna("Ticker", str),
    Coluna("Price", float, dominio=positivo),
    Coluna("AvgVolShares_63", float, dominio=lambda v: v >= 0),
    Coluna("AvgVolUSD_63", float, dominio=lambda v: v >= 0,
           nota="desempate declarado da ordenacao (Fase 3 §5)"),
    Coluna("RSI", float, dominio=intervalo(0, 100)),
    Coluna("SMA20_pct", float),
    Coluna("RVOL", float, dominio=lambda v: v >= 0),
    Coluna("RVOL_pico_20", float, dominio=lambda v: v >= 0),
    Coluna("Eco", float, dominio=lambda v: v >= 0),
    Coluna("range_estado", str, dominio=ESTADOS,
           nota="B7 e feature, nao gate; o P4 nao decide se isto nao for OK"),
    Coluna("sinal_A", bool),
    Coluna("sinal_B", bool),
    Coluna("sinal_C", bool),
    Coluna("n_sinais", int, dominio=intervalo(0, 3)),
    Coluna("rsi_zona", str, obrigatoria=False),
])

# FASE C — identidade.
IDENTIDADE = Contrato("C/identidade", [
    Coluna("Ticker", str),
    Coluna("conid", (int, str), obrigatoria=False),
    Coluna("cik", (int, str), obrigatoria=False),
    Coluna("tier_listagem", str, obrigatoria=False),
    Coluna("identidade_estado", str, dominio=um_de("OK", "REVER", "FAIL")),
])

# FASE D — fundamentais.
FUNDAMENTAIS = Contrato("D/fundamentais", [
    Coluna("Ticker", str),
    Coluna("accoes_em_circulacao", float, obrigatoria=False, dominio=positivo),
    Coluna("accoes_estado", str, dominio=ESTADOS),
    Coluna("MCapM", float, obrigatoria=False, dominio=positivo),
    Coluna("MCapEstado", str, dominio=ESTADOS),
    Coluna("regime_reporte", str, obrigatoria=False,
           dominio=um_de("10-Q", "20-F")),
])

# FASE E — red flags.
REDFLAGS = Contrato("E/redflags", [
    Coluna("Ticker", str),
    Coluna("gc_estado", str,
           dominio=um_de("CONFIRMADO", "ALIVIADO", "A_REVER", "NAO_APLICAVEL")),
    Coluna("delisting", bool, obrigatoria=False),
    Coluna("queda_sem_recuperacao", bool, obrigatoria=False,
           nota="None e 'nao verificado' e nao pode virar False (D0-2)"),
    Coluna("redflag_estado", str, dominio=ESTADOS),
    Coluna("reprova", bool),
])

# FASE G — classificacao e ordenacao.
CLASSIFICACAO = Contrato("G/classificacao", [
    Coluna("Ticker", str),
    Coluna("setup", int, dominio=um_de(1, 2, 3, 4, 5, 9)),
    Coluna("setup_nome", str),
    Coluna("posicao", int, dominio=positivo),
    Coluna("razao_posicao", str,
           nota="criterio de aceitacao 6: zero desempates implicitos"),
    Coluna("desempate_aplicado", str, obrigatoria=False),
])

CONTRATOS: dict[str, Contrato] = {c.nome: c for c in [
    UNIVERSO, SHORTLIST, IDENTIDADE, FUNDAMENTAIS, REDFLAGS, CLASSIFICACAO]}
