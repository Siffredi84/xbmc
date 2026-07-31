"""E1-3 — todos os limiares, cada um com origem declarada.

Um numero num gate e uma afirmacao sobre o mundo. A diferenca entre `RSI <= 60`
(esta no documento de criterios) e `Eco >= 1,5` (saiu de duas sessoes de
observacao) e enorme, e no `config.py` actual sao indistinguiveis — a mesma
linha, o mesmo formato, a mesma autoridade aparente.

Aqui cada limiar diz de onde veio. Os classificados como PROVISORIO nao podem
ser usados como gate duro sem revisao marcada (criterio de aceitacao 7 da
Fase 4): `gate("ECO_ALTO")` levanta, `valor("ECO_ALTO")` nao.

Referencia: docs/fase4-plano-implementacao.md §4.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Origem(Enum):
    DOCUMENTO = "documento"    # documento de criterios do utilizador
    DECISAO = "decisao"        # decisao registada, com razao (HANDOVER §8)
    MEDICAO = "medicao"        # derivado de medicao sobre dados reais
    PROVISORIO = "provisorio"  # base insuficiente; usar com revisao marcada

    def __str__(self) -> str:
        return self.value


class LimiarProvisorio(RuntimeError):
    """Um limiar sem base suficiente foi pedido como gate duro."""


@dataclass(frozen=True)
class Limiar:
    nome: str
    valor: float | int | str
    unidade: str
    origem: Origem
    nota: str
    revisao_apos_sessoes: int | None = None

    @property
    def utilizavel_como_gate(self) -> bool:
        return (self.origem is not Origem.PROVISORIO
                or self.revisao_apos_sessoes is not None)


def _l(nome, valor, unidade, origem, nota, revisao=None) -> Limiar:
    return Limiar(nome, valor, unidade, origem, nota, revisao)


LIMIARES: dict[str, Limiar] = {l.nome: l for l in [
    # -- janelas de calculo ---------------------------------------------------
    _l("JANELA_VOLUME", 63, "sessoes", Origem.DECISAO,
       "comparabilidade com Finviz e historico; resiste a contaminacao pelo "
       "proprio pico (HANDOVER §8)"),
    _l("JANELA_RSI", 14, "sessoes", Origem.DOCUMENTO, "RSI(14) do documento"),
    _l("JANELA_RSI_SERIE", 63, "sessoes", Origem.DECISAO,
       "B3: serie fixa em 63 sessoes. O Wilder varia +-5 pontos com o "
       "comprimento da serie; sem fixar, o RSI nao e reproduzivel"),
    _l("JANELA_SMA", 20, "sessoes", Origem.DOCUMENTO, "MA20 do documento"),
    _l("JANELA_RANGE", 252, "sessoes", Origem.DECISAO,
       "B7: range calculado, truncado no ultimo split"),
    _l("JANELA_BREAKOUT", 60, "sessoes", Origem.DECISAO, "F-3, parametro exposto"),

    # -- gates quantitativos (documento) --------------------------------------
    _l("PRECO_MIN", 1.0, "USD", Origem.DOCUMENTO, "criterio 1"),
    _l("PRECO_MAX", 7.0, "USD", Origem.DOCUMENTO,
       "criterio 1; 15x mais massa junto a $1 do que a $7"),
    _l("MCAP_MIN_M", 50.0, "M USD", Origem.DOCUMENTO, "criterio 2"),
    _l("MCAP_MAX_M", 500.0, "M USD", Origem.DOCUMENTO, "criterio 2"),
    _l("VOL_MEDIO_MIN", 100_000, "accoes/dia", Origem.DOCUMENTO,
       "criterio 3; B2a"),
    _l("RELVOL_MIN", 1.2, "x", Origem.DOCUMENTO,
       "criterio 7; corta 88%, mediana do universo e 0,51"),
    _l("RSI_MAX", 60.0, "pontos", Origem.DOCUMENTO,
       "criterio 5, tecto. B5 mantem so o tecto"),
    _l("SMA20_MIN_PCT", -15.0, "%", Origem.DOCUMENTO, "criterio 6"),
    _l("HIGH52_MAX_PCT", -10.0, "%", Origem.DOCUMENTO,
       "criterio 8; corta 3 em 50 — mantido por custo zero, nao por utilidade"),

    # -- gates derivados de medicao -------------------------------------------
    _l("VOL_USD_MIN", 1_000_000, "USD/dia", Origem.MEDICAO,
       "B2b: remove 205 de 860 em 29-07. O T2 mostrou que os sinais dos "
       "removidos sao indistinguiveis (Mann-Whitney p 0,054-0,717) — o gate "
       "separa por liquidez, nao por qualidade"),
    _l("SPLIT_EXCLUSAO_DIAS", 90, "dias", Origem.DECISAO,
       "A3: split <=90 dias exclui. Remove 72 de 932; largura por confirmar"),
    _l("SPLIT_RECENTE_DIAS", 365, "dias", Origem.DECISAO,
       "A3: 90-365 dias marca RECENTE e trunca a janela de range"),
    _l("QUEDA_52S_MAX_PCT", -80.0, "%", Origem.DOCUMENTO, "P4, red flag"),
    _l("RECUPERACAO_52S_MIN_PCT", 15.0, "%", Origem.DOCUMENTO,
       "P4: o qualificador 'sem recuperacao' salva o BYRN (+25,4%)"),
    _l("MCAP_DIVERGENCIA_MAX_PCT", 5.0, "%", Origem.MEDICAO,
       "P2: CRDL divergia 42%, SUPX 38%"),
    _l("FRESHNESS_ACCOES_DIAS", 120, "dias", Origem.DECISAO,
       "D1: facto XBRL mais velho que isto passa a DATA_STALE"),
    _l("QUARENTENA_LIMIAR_FALHAS", 3, "sessoes", Origem.DECISAO,
       "A5; acima da linha de base do mercado"),
    _l("NOME_SIMILARIDADE_MIN", 0.60, "racio", Origem.MEDICAO,
       "C-1: separa o par BW/BBW sem partir o SNDL"),
    _l("C_COMPONENTES_MIN", 2, "componentes", Origem.DECISAO,
       "B8: o sinal C disparava em 17 de 21 com 1 componente — um teste que "
       "81% passam nao distingue"),
    _l("TETO_SHORTLIST", 10, "candidatos", Origem.DOCUMENTO,
       "criterio 13; excedente vai para saida_reserva.csv"),
    _l("BREAKOUT_TOLERANCIA_PCT", 2.0, "%", Origem.DECISAO, "F-3"),

    # -- provisorios: base insuficiente, revisao obrigatoria -------------------
    _l("ECO_ALTO", 1.5, "racio", Origem.PROVISORIO,
       "setups 1, 2 e 5. Derivado de duas sessoes", revisao=5),
    _l("ECO_BAIXO", 1.15, "racio", Origem.PROVISORIO,
       "setup 4. Derivado de duas sessoes; 14 dos 22 residuais caem na zona "
       "morta [1,15; 1,5]", revisao=5),
    _l("RVOL_SETUP4", 2.0, "x", Origem.PROVISORIO,
       "setup 4. Baixar para 1,5 recuperaria 4 residuais — e seria overfitting "
       "pelo mecanismo que a Fase 3 rejeitou", revisao=5),
    _l("SPREAD_MAX_PCT", 2.0, "%", Origem.PROVISORIO,
       "F-2. 17 observacoes de uma unica sessao", revisao=5),
    _l("SPREAD_EXCLUSAO_PCT", 5.0, "%", Origem.PROVISORIO,
       "F-2, exclusao dura. Mesma amostra de 17", revisao=5),
    _l("VOL20D_BANDEIRA", 100.0, "% anualizado", Origem.PROVISORIO,
       "bandeira, nunca gate: BYRN a 171% e diferente de TLRY a 36%",
       revisao=20),

    # -- ritmo e quota (auditoria de 2026-07-22) ------------------------------
    _l("POLYGON_PACE_S", 13.0, "s", Origem.DECISAO, "Stocks Basic: 5/min"),
    _l("FINNHUB_PACE_S", 1.35, "s", Origem.DECISAO, "60/min -> ~44/min efectivo"),
    _l("MARKETAUX_DIA_MAX", 75, "chamadas/dia", Origem.DECISAO,
       "de 100/dia, com reserva de 25%"),
    _l("SEC_TENTATIVAS", 8, "tentativas", Origem.MEDICAO,
       "D0-4: 5 tentativas esgotavam em 31 s e a SEC deu 503 mais tempo"),
]}

#: Universo, por cotacao e nao por domicilio (HANDOVER §8).
TIPO_VALIDO = "CS"
EXCH_POLYGON = frozenset({"XNAS", "XNYS", "XASE"})
EXCH_IBKR = frozenset({"NASDAQ", "NYSE", "AMEX", "ARCA", "BATS", "IEX"})
EXCH_YAHOO = frozenset({"NYQ", "NMS", "NGM", "NCM", "ASE", "PCX", "BTS", "NYS"})


def limiar(nome: str) -> Limiar:
    try:
        return LIMIARES[nome]
    except KeyError:
        raise KeyError(f"limiar desconhecido: {nome!r}. Um numero que governa "
                       "uma decisao vive aqui ou nao existe") from None


def valor(nome: str):
    """Valor sem juizo sobre o uso. Para features, relatorios e bandeiras."""
    return limiar(nome).valor


def gate(nome: str):
    """Valor para uso como gate duro. Levanta se a base for insuficiente."""
    lim = limiar(nome)
    if not lim.utilizavel_como_gate:
        raise LimiarProvisorio(
            f"{nome} e PROVISORIO sem revisao marcada e nao pode ser gate duro: "
            f"{lim.nota}")
    return lim.valor


def provisorios() -> list[Limiar]:
    return [l for l in LIMIARES.values() if l.origem is Origem.PROVISORIO]


def por_origem() -> dict[str, list[str]]:
    """Para `metricas.json`: quantas decisoes assentam em que tipo de base."""
    out: dict[str, list[str]] = {o.value: [] for o in Origem}
    for l in LIMIARES.values():
        out[l.origem.value].append(l.nome)
    return out
