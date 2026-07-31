"""E1-1 — os estados do funil e o objecto que os transporta.

Existe uma so razao para este modulo: **dados em falta produzem etiqueta, nunca
decisao**. O pipeline actual codifica esse principio em quatro sitios, cada um
a sua maneira, com tres estados de missingness. Aqui sao seis (sete contando o
OK) e sao objectos, nao strings — porque uma string deixa-se comparar, somar e
converter em silencio, e foi assim que se perderam empresas.

O que este modulo proibe, e porque:

* `bool(Resultado)` levanta. Um `if resultado:` leria 'nao verificado' como
  'falso' — a forma exacta das seis falhas que originaram o principio.
* `Resultado(None, OK, ...)` levanta. OK significa verificado; sem valor nao
  ha verificacao.
* `DATA_INSUFFICIENT -> FORA_DO_CRITERIO` levanta. E a coercao central: uma
  ausencia de fonte a apresentar-se como ausencia de sinal.

Referencia: docs/fase3-especificacao-vnext.md §2.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
from enum import Enum
from typing import Any


class Estado(Enum):
    """Sete valores: um verificado, um decidido, cinco indeterminados.

    A Fase 3 fala em 'seis estados' — sao os seis que nao sao OK. OK esta na
    lista por ser o unico que autoriza uma decisao positiva, e por isso tem de
    ser representavel.
    """

    OK = "OK"                                # verificado e dentro do criterio
    FORA_DO_CRITERIO = "FORA_DO_CRITERIO"    # verificado e fora
    DATA_INSUFFICIENT = "DATA_INSUFFICIENT"  # dado ausente
    DATA_INVALID = "DATA_INVALID"            # presente e impossivel
    DATA_STALE = "DATA_STALE"                # valido mas fora da freshness
    SOURCE_DISAGREE = "SOURCE_DISAGREE"      # fontes divergem acima do limiar
    NETWORK_FAILURE = "NETWORK_FAILURE"      # falha de rede apos backoff

    def __str__(self) -> str:
        return self.value


#: Estados que autorizam uma decisao. Tudo o resto e indeterminado e vai para
#: uma fila, nunca para a lista de aprovados.
DECIDIVEIS = frozenset({Estado.OK, Estado.FORA_DO_CRITERIO})

#: Os cinco indeterminados. Distintos entre si por construcao: colapsa-los foi
#: precisamente o erro que este modelo existe para impedir.
INDETERMINADOS = frozenset(set(Estado) - DECIDIVEIS)

#: Estados em que nao ha valor nenhum para transportar. Nao ha resposta e nao
#: ha dado; um valor aqui seria inventado.
SEM_VALOR = frozenset({Estado.DATA_INSUFFICIENT, Estado.NETWORK_FAILURE})

#: Transicoes legitimas. So o OK e origem: e o unico estado que carrega um
#: valor verificado, e portanto o unico sobre o qual outra regra pode
#: pronunciar-se depois. Um indeterminado e terminal — o que falta nao passa a
#: existir por uma etapa a jusante lhe mudar o nome.
TRANSICOES_PERMITIDAS: dict[Estado, frozenset[Estado]] = {
    Estado.OK: frozenset({
        Estado.FORA_DO_CRITERIO,   # um gate avaliou o valor verificado
        Estado.DATA_STALE,         # verificacao de freshness a jusante
        Estado.DATA_INVALID,       # verificacao de plausibilidade a jusante
        Estado.SOURCE_DISAGREE,    # segunda fonte contradisse a primeira
    }),
    Estado.FORA_DO_CRITERIO: frozenset(),
    Estado.DATA_INSUFFICIENT: frozenset(),
    Estado.DATA_INVALID: frozenset(),
    Estado.DATA_STALE: frozenset(),
    Estado.SOURCE_DISAGREE: frozenset(),
    Estado.NETWORK_FAILURE: frozenset(),
}


class CoercaoProibida(TypeError):
    """Tentativa de converter um estado noutro, ou de o ler como booleano."""


class Papel(Enum):
    """Para que serve o campo. Determina o efeito de um indeterminado."""

    ELEGIBILIDADE = "elegibilidade"  # decide se o candidato entra
    RED_FLAG = "red_flag"            # decide se o candidato e reprovado
    FEATURE = "feature"              # descreve; nunca exclui


@dataclass(frozen=True)
class Decisao:
    """Resposta a 'este resultado bloqueia o candidato?', com a razao."""

    bloqueia: bool
    razao: str
    estado: Estado


@dataclass(frozen=True)
class Resultado:
    """Um valor, o seu estado, quem o produziu e como.

    `fonte` e o fornecedor (`polygon`, `sec`, `ibkr`, `local`). `proveniencia`
    e a regra que o produziu, em texto legivel — e o que permite responder
    'porque e que este candidato esta nesta posicao' sem ler codigo.
    """

    valor: Any
    estado: Estado
    fonte: str
    proveniencia: str

    def __post_init__(self) -> None:
        if not isinstance(self.estado, Estado):
            raise CoercaoProibida(
                f"estado tem de ser Estado, nao {type(self.estado).__name__}: "
                f"{self.estado!r}")
        if not (isinstance(self.fonte, str) and self.fonte.strip()):
            raise ValueError("fonte obrigatoria: sem ela nao ha auditoria")
        if not (isinstance(self.proveniencia, str) and self.proveniencia.strip()):
            raise ValueError("proveniencia obrigatoria: sem ela nao ha "
                             "explicacao da posicao")
        if self.estado in SEM_VALOR and self.valor is not None:
            raise CoercaoProibida(
                f"{self.estado} nao pode transportar valor ({self.valor!r}): "
                "nao houve dado nenhum")
        if self.estado is Estado.OK and self.valor is None:
            raise CoercaoProibida(
                "OK sem valor e uma ausencia disfarcada de verificacao; "
                "usa DATA_INSUFFICIENT")

    # -- construtores nomeados ------------------------------------------------
    @classmethod
    def ok(cls, valor, fonte, proveniencia) -> "Resultado":
        return cls(valor, Estado.OK, fonte, proveniencia)

    @classmethod
    def fora(cls, valor, fonte, proveniencia) -> "Resultado":
        return cls(valor, Estado.FORA_DO_CRITERIO, fonte, proveniencia)

    @classmethod
    def ausente(cls, fonte, proveniencia) -> "Resultado":
        return cls(None, Estado.DATA_INSUFFICIENT, fonte, proveniencia)

    @classmethod
    def invalido(cls, valor, fonte, proveniencia) -> "Resultado":
        return cls(valor, Estado.DATA_INVALID, fonte, proveniencia)

    @classmethod
    def velho(cls, valor, fonte, proveniencia) -> "Resultado":
        return cls(valor, Estado.DATA_STALE, fonte, proveniencia)

    @classmethod
    def divergente(cls, valor, fonte, proveniencia) -> "Resultado":
        return cls(valor, Estado.SOURCE_DISAGREE, fonte, proveniencia)

    @classmethod
    def falha_rede(cls, fonte, proveniencia) -> "Resultado":
        return cls(None, Estado.NETWORK_FAILURE, fonte, proveniencia)

    # -- guardas --------------------------------------------------------------
    def __bool__(self):
        raise CoercaoProibida(
            f"Resultado({self.estado}) nao tem valor de verdade: usa .decidivel "
            "ou .estado. Um `if resultado:` leria indeterminado como falso, que "
            "e a falha que este modelo existe para impedir")

    @property
    def decidivel(self) -> bool:
        """Ha base para decidir? Nao confundir com 'passou'."""
        return self.estado in DECIDIVEIS

    @property
    def indeterminado(self) -> bool:
        return self.estado in INDETERMINADOS

    def exige(self):
        """Devolve o valor ou levanta. Para quando o chamador ja verificou o
        estado e quer falhar alto se estiver enganado."""
        if self.estado is not Estado.OK:
            raise CoercaoProibida(
                f"valor exigido a um resultado {self.estado} "
                f"({self.fonte}: {self.proveniencia})")
        return self.valor

    # -- transicoes -----------------------------------------------------------
    def transita(self, novo: Estado, regra: str) -> "Resultado":
        """Unica forma de mudar de estado. A regra fica na proveniencia."""
        if not isinstance(novo, Estado):
            raise CoercaoProibida(f"estado de destino invalido: {novo!r}")
        if not (isinstance(regra, str) and regra.strip()):
            raise ValueError("transicao sem regra nomeada nao e auditavel")
        if novo is self.estado:
            return self
        permitidas = TRANSICOES_PERMITIDAS[self.estado]
        if novo not in permitidas:
            raise CoercaoProibida(
                f"coercao proibida {self.estado} -> {novo} (regra {regra!r}). "
                f"Permitidas a partir de {self.estado}: "
                f"{sorted(e.value for e in permitidas) or 'nenhuma (terminal)'}")
        valor = None if novo in SEM_VALOR else self.valor
        return replace(self, valor=valor, estado=novo,
                       proveniencia=f"{self.proveniencia} -> {regra}")


def avalia(resultado: Resultado, papel: Papel) -> Decisao:
    """Efeito de um resultado sobre o candidato, dado o papel do campo.

    Elegibilidade e red flag exigem OK: sao os dois sitios onde um
    indeterminado nao pode passar (criterio de aceitacao 3 da Fase 4). Uma
    feature nunca exclui — descreve, e leva a etiqueta consigo.
    """
    if not isinstance(papel, Papel):
        raise TypeError(f"papel invalido: {papel!r}")
    e = resultado.estado
    if papel is Papel.FEATURE:
        return Decisao(False, f"feature com estado {e}", e)
    if e is Estado.OK:
        return Decisao(False, "verificado e dentro do criterio", e)
    if e is Estado.FORA_DO_CRITERIO:
        return Decisao(True, f"{papel.value}: verificado e fora do criterio", e)
    return Decisao(True, f"{papel.value} com {e}: nao verificado, nao aprovado", e)


def conta_estados(resultados) -> dict[str, int]:
    """Contagem por estado, para `metricas.json` (missingness por campo)."""
    contas = {e.value: 0 for e in Estado}
    for r in resultados:
        contas[r.estado.value] += 1
    return contas
