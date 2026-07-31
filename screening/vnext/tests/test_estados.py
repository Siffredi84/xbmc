"""E1-1 — testes das transicoes proibidas.

Teste de aceitacao da Fase 4: "unitario sobre cada transicao proibida
(`SEM_FONTE -> SEM_SINAL` levanta)". SEM_FONTE e DATA_INSUFFICIENT; SEM_SINAL e
FORA_DO_CRITERIO — 'verificado e fora' e a unica forma legitima de dizer que
nao ha sinal.
"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from vnext.estados import (DECIDIVEIS, INDETERMINADOS, SEM_VALOR,
                     TRANSICOES_PERMITIDAS, CoercaoProibida, Decisao, Estado,
                     Papel, Resultado, avalia, conta_estados)


class TestEstados(unittest.TestCase):
    def test_seis_estados_alem_do_ok(self):
        self.assertEqual(len(Estado), 7)
        self.assertEqual(len(set(Estado) - {Estado.OK}), 6)

    def test_decidiveis_e_indeterminados_particionam(self):
        self.assertEqual(DECIDIVEIS | INDETERMINADOS, set(Estado))
        self.assertFalse(DECIDIVEIS & INDETERMINADOS)
        self.assertEqual(len(INDETERMINADOS), 5)


class TestResultado(unittest.TestCase):
    def test_construcao_minima(self):
        r = Resultado.ok(3.2, "polygon", "B1 preco no intervalo")
        self.assertEqual(r.valor, 3.2)
        self.assertIs(r.estado, Estado.OK)
        self.assertTrue(r.decidivel)
        self.assertFalse(r.indeterminado)

    def test_booleano_levanta(self):
        # A falha original: `if resultado:` a ler ausencia como falso.
        r = Resultado.ausente("finnhub", "52 semanas nao devolvido")
        with self.assertRaises(CoercaoProibida):
            bool(r)
        with self.assertRaises(CoercaoProibida):
            if r:  # noqa: SIM103
                pass

    def test_ok_sem_valor_levanta(self):
        with self.assertRaises(CoercaoProibida):
            Resultado.ok(None, "sec", "accoes em circulacao")

    def test_estados_sem_valor_nao_transportam_valor(self):
        for estado in SEM_VALOR:
            with self.assertRaises(CoercaoProibida):
                Resultado(1, estado, "edgar", "x")

    def test_fonte_e_proveniencia_obrigatorias(self):
        with self.assertRaises(ValueError):
            Resultado.ok(1, "", "regra")
        with self.assertRaises(ValueError):
            Resultado.ok(1, "polygon", "  ")

    def test_estado_tem_de_ser_enum(self):
        with self.assertRaises(CoercaoProibida):
            Resultado(1, "OK", "polygon", "regra")

    def test_exige_so_devolve_com_ok(self):
        self.assertEqual(Resultado.ok(7, "sec", "d1").exige(), 7)
        for r in [Resultado.ausente("sec", "d1"),
                  Resultado.velho(7, "sec", "d1"),
                  Resultado.fora(7, "sec", "d1")]:
            with self.assertRaises(CoercaoProibida):
                r.exige()

    def test_imutavel(self):
        r = Resultado.ok(1, "polygon", "regra")
        with self.assertRaises(Exception):
            r.valor = 2


class TestTransicoes(unittest.TestCase):
    def test_sem_fonte_para_sem_sinal_levanta(self):
        r = Resultado.ausente("finnhub", "profile2 vazio")
        with self.assertRaises(CoercaoProibida) as ctx:
            r.transita(Estado.FORA_DO_CRITERIO, "B2b volume USD")
        self.assertIn("DATA_INSUFFICIENT", str(ctx.exception))
        self.assertIn("FORA_DO_CRITERIO", str(ctx.exception))

    def test_indeterminados_sao_terminais(self):
        origem = {
            Estado.DATA_INSUFFICIENT: Resultado.ausente("f", "p"),
            Estado.NETWORK_FAILURE: Resultado.falha_rede("edgar", "503"),
            Estado.DATA_INVALID: Resultado.invalido(1, "finnhub", "min > preco"),
            Estado.DATA_STALE: Resultado.velho(1, "sec", "end a 400 dias"),
            Estado.SOURCE_DISAGREE: Resultado.divergente(1, "ibkr", "vs yahoo"),
            Estado.FORA_DO_CRITERIO: Resultado.fora(1, "polygon", "B1"),
        }
        for estado, r in origem.items():
            self.assertEqual(TRANSICOES_PERMITIDAS[estado], frozenset())
            for destino in set(Estado) - {estado}:
                with self.assertRaises(CoercaoProibida, msg=f"{estado}->{destino}"):
                    r.transita(destino, "regra qualquer")

    def test_ok_transita_para_as_quatro_permitidas(self):
        r = Resultado.ok(-85.0, "polygon", "B7 range calculado")
        for destino in (Estado.FORA_DO_CRITERIO, Estado.DATA_STALE,
                        Estado.DATA_INVALID, Estado.SOURCE_DISAGREE):
            novo = r.transita(destino, "regra X")
            self.assertIs(novo.estado, destino)
            self.assertEqual(novo.valor, -85.0)
            self.assertIn("regra X", novo.proveniencia)
            self.assertIn("B7 range calculado", novo.proveniencia)

    def test_ok_nao_transita_para_ausencias(self):
        r = Resultado.ok(1, "polygon", "regra")
        for destino in (Estado.DATA_INSUFFICIENT, Estado.NETWORK_FAILURE):
            with self.assertRaises(CoercaoProibida):
                r.transita(destino, "regra")

    def test_transicao_exige_regra_nomeada(self):
        r = Resultado.ok(1, "polygon", "regra")
        with self.assertRaises(ValueError):
            r.transita(Estado.FORA_DO_CRITERIO, "")

    def test_transicao_para_o_mesmo_estado_e_identidade(self):
        r = Resultado.ok(1, "polygon", "regra")
        self.assertIs(r.transita(Estado.OK, "reavaliacao"), r)

    def test_original_nao_muda(self):
        r = Resultado.ok(1, "polygon", "B1")
        r.transita(Estado.FORA_DO_CRITERIO, "B2b")
        self.assertIs(r.estado, Estado.OK)


class TestAvalia(unittest.TestCase):
    def test_elegibilidade_so_passa_com_ok(self):
        # Criterio de aceitacao 3: zero aprovados com DATA_* num gate de
        # elegibilidade.
        self.assertFalse(avalia(Resultado.ok(1, "f", "p"),
                                Papel.ELEGIBILIDADE).bloqueia)
        for r in [Resultado.ausente("f", "p"),
                  Resultado.invalido(1, "f", "p"),
                  Resultado.velho(1, "f", "p"),
                  Resultado.divergente(1, "f", "p"),
                  Resultado.falha_rede("f", "p"),
                  Resultado.fora(1, "f", "p")]:
            self.assertTrue(avalia(r, Papel.ELEGIBILIDADE).bloqueia, r.estado)

    def test_red_flag_bloqueia_com_falha_de_rede(self):
        d = avalia(Resultado.falha_rede("edgar", "503 apos 8"), Papel.RED_FLAG)
        self.assertTrue(d.bloqueia)
        self.assertIn("NETWORK_FAILURE", d.razao)

    def test_feature_nunca_bloqueia(self):
        for r in [Resultado.falha_rede("ibkr", "sem TWS"),
                  Resultado.ausente("nenhuma", "cobertura de analistas"),
                  Resultado.fora(1, "f", "p")]:
            d = avalia(r, Papel.FEATURE)
            self.assertFalse(d.bloqueia)
            self.assertIsInstance(d, Decisao)

    def test_papel_invalido_levanta(self):
        with self.assertRaises(TypeError):
            avalia(Resultado.ok(1, "f", "p"), "elegibilidade")


class TestMetricas(unittest.TestCase):
    def test_conta_estados_cobre_os_sete(self):
        c = conta_estados([Resultado.ok(1, "f", "p"),
                           Resultado.ok(2, "f", "p"),
                           Resultado.falha_rede("f", "p")])
        self.assertEqual(c["OK"], 2)
        self.assertEqual(c["NETWORK_FAILURE"], 1)
        self.assertEqual(c["DATA_STALE"], 0)
        self.assertEqual(len(c), 7)


if __name__ == "__main__":
    unittest.main()
