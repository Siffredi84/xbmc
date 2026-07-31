"""E1-2 — testes dos contratos por fase.

Teste de aceitacao da Fase 4: "validacao de contrato falha com mensagem que
nomeia a coluna em falta".
"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from vnext.contratos import (CONTRATOS, SHORTLIST, UNIVERSO, Coluna, Contrato,
                       ContratoViolado, intervalo, um_de)


def _universo(**alt):
    base = {"Ticker": "BYRN", "type": "CS", "exch": "XNAS", "nome": "Byrna",
            "split_estado": "SEM_SPLIT", "split_ultima_data": None,
            "serie_estado": "OK", "sessoes_em_falta": 0}
    base.update(alt)
    return base


class TestMensagens(unittest.TestCase):
    def test_coluna_em_falta_e_nomeada(self):
        r = _universo()
        del r["split_estado"]
        with self.assertRaises(ContratoViolado) as ctx:
            UNIVERSO.valida([r])
        self.assertIn("split_estado", str(ctx.exception))
        self.assertIn("A/universo", str(ctx.exception))

    def test_varias_colunas_em_falta_sao_todas_nomeadas(self):
        r = _universo()
        del r["split_estado"], r["serie_estado"]
        with self.assertRaises(ContratoViolado) as ctx:
            UNIVERSO.valida([r])
        self.assertIn("split_estado", str(ctx.exception))
        self.assertIn("serie_estado", str(ctx.exception))

    def test_valor_fora_do_dominio_nomeia_coluna_e_ticker(self):
        with self.assertRaises(ContratoViolado) as ctx:
            UNIVERSO.valida([_universo(exch="OTC")])
        self.assertIn("exch", str(ctx.exception))
        self.assertIn("BYRN", str(ctx.exception))

    def test_tipo_errado_e_apanhado(self):
        with self.assertRaises(ContratoViolado) as ctx:
            UNIVERSO.valida([_universo(sessoes_em_falta="dois")])
        self.assertIn("sessoes_em_falta", str(ctx.exception))


class TestPolitica(unittest.TestCase):
    def test_colunas_a_mais_sao_permitidas(self):
        # Mitigacao do risco 'schema rigido trava iteracao': o contrato diz o
        # que a fase seguinte tem direito a ler, nao tudo o que a anterior
        # escreve.
        UNIVERSO.valida([_universo(experiencia_nova=1.0)])

    def test_opcional_pode_ser_none(self):
        UNIVERSO.valida([_universo(split_ultima_data=None)])

    def test_obrigatoria_nao_pode_ser_none(self):
        with self.assertRaises(ContratoViolado):
            UNIVERSO.valida([_universo(serie_estado=None)])

    def test_devolve_os_dados_para_encadear(self):
        dados = [_universo()]
        self.assertIs(UNIVERSO.valida(dados), dados)

    def test_chave_repetida_levanta(self):
        with self.assertRaises(ContratoViolado) as ctx:
            UNIVERSO.valida([_universo(), _universo()])
        self.assertIn("Ticker", str(ctx.exception))

    def test_vazio_e_valido(self):
        # Uma corrida de zero candidatos e um resultado, nao um erro
        # (criterio de aceitacao 8). Sem registos nao ha colunas para verificar.
        UNIVERSO.valida([])

    def test_dataframe_vazio_continua_a_declarar_colunas(self):
        pd = __import__("pandas")
        UNIVERSO.valida(pd.DataFrame(columns=UNIVERSO.nomes))
        with self.assertRaises(ContratoViolado) as ctx:
            UNIVERSO.valida(pd.DataFrame(columns=["Ticker"]))
        self.assertIn("split_estado", str(ctx.exception))

    def test_booleano_nao_passa_por_numero(self):
        c = Contrato("t", [Coluna("Ticker", str), Coluna("n", int)])
        with self.assertRaises(ContratoViolado):
            c.valida([{"Ticker": "X", "n": True}])


class TestPandas(unittest.TestCase):
    def test_dataframe_aceite(self):
        pd = __import__("pandas")
        df = pd.DataFrame([_universo(), _universo(Ticker="HDSN")])
        self.assertIs(UNIVERSO.valida(df), df)

    def test_dataframe_sem_coluna_nomeia_a_coluna(self):
        pd = __import__("pandas")
        df = pd.DataFrame([_universo()]).drop(columns=["nome"])
        with self.assertRaises(ContratoViolado) as ctx:
            UNIVERSO.valida(df)
        self.assertIn("nome", str(ctx.exception))


class TestContratosDeclarados(unittest.TestCase):
    def test_todas_as_fases_tem_chave_presente(self):
        for nome, c in CONTRATOS.items():
            self.assertIn(c.chave, c.nomes, nome)

    def test_shortlist_exige_o_desempate_da_ordenacao(self):
        # Fase 3 §5: AvgVolUSD_63 e o desempate declarado. Se desaparecer do
        # contrato, a ordenacao passa a ter empates implicitos.
        self.assertIn("AvgVolUSD_63", SHORTLIST.nomes)

    def test_rsi_fora_de_0_100_e_recusado(self):
        base = {"Ticker": "X", "Price": 3.0, "AvgVolShares_63": 2e5,
                "AvgVolUSD_63": 1.2e6, "RSI": 145.0, "SMA20_pct": -3.0,
                "RVOL": 1.4, "RVOL_pico_20": 2.2, "Eco": 1.6,
                "range_estado": "OK", "sinal_A": True, "sinal_B": False,
                "sinal_C": False, "n_sinais": 1}
        with self.assertRaises(ContratoViolado) as ctx:
            SHORTLIST.valida([base])
        self.assertIn("RSI", str(ctx.exception))
        base["RSI"] = 45.0
        SHORTLIST.valida([base])

    def test_range_estado_usa_o_vocabulario_dos_estados(self):
        col = next(c for c in SHORTLIST.colunas if c.nome == "range_estado")
        self.assertTrue(col.dominio >= {"OK", "DATA_INVALID", "NETWORK_FAILURE"})


class TestPredicados(unittest.TestCase):
    def test_intervalo_e_um_de(self):
        self.assertTrue(intervalo(1, 7)(3))
        self.assertFalse(intervalo(1, 7)(7.5))
        self.assertIn("CS", um_de("CS"))


if __name__ == "__main__":
    unittest.main()
