"""E1-3 — testes dos limiares com origem declarada.

Criterio de aceitacao 7 da Fase 4: "cada limiar tem origem declarada; nenhum
classificado como provisorio e usado como gate duro sem revisao marcada".
"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from vnext import config
from vnext.config import (LIMIARES, Limiar, LimiarProvisorio, Origem, gate, limiar,
                    por_origem, provisorios, valor)


class TestOrigemDeclarada(unittest.TestCase):
    def test_todos_tem_origem_unidade_e_nota(self):
        for nome, l in LIMIARES.items():
            self.assertIsInstance(l.origem, Origem, nome)
            self.assertTrue(l.unidade.strip(), nome)
            self.assertTrue(l.nota.strip(), f"{nome} sem justificacao")

    def test_nome_do_registo_bate_com_o_limiar(self):
        for nome, l in LIMIARES.items():
            self.assertEqual(nome, l.nome)

    def test_limiar_desconhecido_levanta(self):
        with self.assertRaises(KeyError):
            limiar("RSI_MIN")   # removido: B5 mantem so o tecto


class TestProvisorios(unittest.TestCase):
    def test_provisorio_sem_revisao_nao_e_gate(self):
        falso = Limiar("TESTE", 1.0, "x", Origem.PROVISORIO, "sem base")
        self.assertFalse(falso.utilizavel_como_gate)

    def test_provisorios_declarados_tem_revisao_marcada(self):
        for l in provisorios():
            self.assertIsNotNone(l.revisao_apos_sessoes,
                                 f"{l.nome} provisorio sem revisao marcada")

    def test_gate_levanta_para_provisorio_sem_revisao(self):
        original = LIMIARES["SPREAD_MAX_PCT"]
        LIMIARES["SPREAD_MAX_PCT"] = Limiar(
            "SPREAD_MAX_PCT", 2.0, "%", Origem.PROVISORIO, "17 observacoes")
        try:
            with self.assertRaises(LimiarProvisorio):
                gate("SPREAD_MAX_PCT")
            self.assertEqual(valor("SPREAD_MAX_PCT"), 2.0)  # feature: permitido
        finally:
            LIMIARES["SPREAD_MAX_PCT"] = original

    def test_gate_permitido_com_revisao_marcada(self):
        self.assertEqual(gate("SPREAD_MAX_PCT"), 2.0)
        self.assertEqual(limiar("SPREAD_MAX_PCT").revisao_apos_sessoes, 5)

    def test_limiares_do_documento_sao_gates(self):
        for nome in ("PRECO_MIN", "PRECO_MAX", "MCAP_MIN_M", "MCAP_MAX_M",
                     "VOL_MEDIO_MIN", "RELVOL_MIN", "RSI_MAX", "SMA20_MIN_PCT"):
            gate(nome)


class TestValoresMedidos(unittest.TestCase):
    def test_valores_que_a_implementacao_tem_de_reproduzir(self):
        self.assertEqual(valor("PRECO_MIN"), 1.0)
        self.assertEqual(valor("PRECO_MAX"), 7.0)
        self.assertEqual(valor("VOL_MEDIO_MIN"), 100_000)
        self.assertEqual(valor("VOL_USD_MIN"), 1_000_000)
        self.assertEqual(valor("JANELA_VOLUME"), 63)
        self.assertEqual(valor("JANELA_RSI_SERIE"), 63)
        self.assertEqual(valor("SPLIT_EXCLUSAO_DIAS"), 90)
        self.assertEqual(valor("C_COMPONENTES_MIN"), 2)
        self.assertEqual(valor("TETO_SHORTLIST"), 10)

    def test_gate_usd_e_medicao_e_nao_documento(self):
        # B2b nao esta no documento de criterios: saiu da medicao dos spreads.
        self.assertIs(limiar("VOL_USD_MIN").origem, Origem.MEDICAO)

    def test_limiares_da_taxonomia_sao_provisorios(self):
        # Duas sessoes nao sao base para um gate de classificacao.
        for nome in ("ECO_ALTO", "ECO_BAIXO", "RVOL_SETUP4"):
            self.assertIs(limiar(nome).origem, Origem.PROVISORIO, nome)


class TestUniverso(unittest.TestCase):
    def test_bolsas_explicitas(self):
        # P5: o filtro de bolsa passa a ser regra nossa, nao propriedade do
        # endpoint do Polygon.
        self.assertEqual(config.EXCH_POLYGON, {"XNAS", "XNYS", "XASE"})
        self.assertEqual(config.TIPO_VALIDO, "CS")


class TestObservabilidade(unittest.TestCase):
    def test_por_origem_cobre_tudo(self):
        mapa = por_origem()
        self.assertEqual(sum(len(v) for v in mapa.values()), len(LIMIARES))
        self.assertEqual(set(mapa), {o.value for o in Origem})


if __name__ == "__main__":
    unittest.main()
