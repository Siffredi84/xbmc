"""H-2 — o snapshot congelado e o que dele se pode afirmar.

Dois tipos de teste, e a diferenca importa:

* **Integridade** — os ficheiros conferem com o manifesto. Se falhar, a
  comparacao A vs B da Fase 5 deixou de ser reproduzivel.
* **Ancoras** — os numeros que os testes de integracao da Fase 4 vao assertar
  saem mesmo destes ficheiros, e nao de uma transcricao a mao.
"""
import csv
import sys
import unittest
from collections import Counter
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
SNAPSHOT = RAIZ / "snapshot"
sys.path.insert(0, str(SNAPSHOT))

import verifica


def _le(nome):
    with open(SNAPSHOT / nome, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


class TestIntegridade(unittest.TestCase):
    def test_snapshot_confere_com_o_manifesto(self):
        ok, problemas = verifica.verifica()
        self.assertTrue(ok, "\n".join(problemas))

    def test_manifesto_cobre_as_duas_sessoes(self):
        import json
        m = json.loads((SNAPSHOT / "MANIFESTO.json").read_text())["ficheiros"]
        sessoes = {v["sessao"] for v in m.values()}
        self.assertIn("2026-07-29", sessoes)
        self.assertIn("2026-07-30", sessoes)


class TestAncorasDaTaxonomia(unittest.TestCase):
    """Fase 5 §0 — a correccao aos numeros da Fase 3.

    A Fase 3 classificou os 48 sobreviventes dos gates tecnicos sem lhes
    aplicar os gates fundamentais. `setups_3007.csv` e essa corrida: contem os
    48 e a distribuicao errada. A correccao (26 candidatos, 2/1/1/4/6/12) so e
    verificavel aqui na parte que o ficheiro suporta — os tickers nomeados.
    O total corrigido exige o epico D e fica para os testes de integracao.
    """

    SOBREVIVENTES = {
        "1_ACUMULACAO_INFORMADA": ["BYRN", "HDSN"],
        "2_REVERSAO_CONFIRMADA": ["SIGA"],
        "3_BASE_A_TESTAR_RESISTENCIA": ["SEER"],
        "4_EVENTO_UNICO": ["EPRX", "GAU", "TLRY", "UROY"],
        "5_CONTINUACAO_DE_EVENTO": ["ABEO", "AVIR", "DMAC", "ENGS", "NKLR",
                                    "SNDL"],
    }

    def setUp(self):
        self.linhas = _le("setups_3007.csv")
        self.setup = {l["Ticker"]: l["setup"] for l in self.linhas}

    def test_ficheiro_tem_os_48_sobreviventes_tecnicos(self):
        self.assertEqual(len(self.linhas), 48)

    def test_distribuicao_por_medir_e_a_da_fase_3(self):
        # 2/3/2/7/12/22 esta correcto *para os 48*. O erro da Fase 3 foi
        # apresentar isto como a taxonomia da populacao elegivel.
        c = Counter(l["setup"] for l in self.linhas)
        self.assertEqual(
            [c["1_ACUMULACAO_INFORMADA"], c["2_REVERSAO_CONFIRMADA"],
             c["3_BASE_A_TESTAR_RESISTENCIA"], c["4_EVENTO_UNICO"],
             c["5_CONTINUACAO_DE_EVENTO"], c["9_NAO_CLASSIFICADO"]],
            [2, 3, 2, 7, 12, 22])

    def test_tickers_nomeados_na_correccao_batem(self):
        for setup, tickers in self.SOBREVIVENTES.items():
            for t in tickers:
                self.assertEqual(self.setup.get(t), setup, t)

    def test_correccao_soma_14_classificados_em_26(self):
        # 2+1+1+4+6 = 14 classificados, 12 residuais, 26 elegiveis, 46%.
        classificados = sum(len(v) for v in self.SOBREVIVENTES.values())
        self.assertEqual(classificados, 14)
        self.assertEqual(26 - classificados, 12)
        self.assertAlmostEqual(12 / 26 * 100, 46.2, places=1)

    def test_restricao_4_3_continua_viva(self):
        # Fase 5 §0: os setups 1 e 2 dao tres candidatos, nao cinco — e dois
        # deles sao o mesmo par. NG e OPK caem nos gates fundamentais.
        s12 = (self.SOBREVIVENTES["1_ACUMULACAO_INFORMADA"] +
               self.SOBREVIVENTES["2_REVERSAO_CONFIRMADA"])
        self.assertEqual(sorted(s12), ["BYRN", "HDSN", "SIGA"])
        for caido in ("NG", "OPK"):
            self.assertEqual(self.setup.get(caido), "2_REVERSAO_CONFIRMADA")


class TestAncorasDoFunil(unittest.TestCase):
    def test_universo_diagnostico(self):
        # 5.288 linhas de diagnostico para 5.299 CS+bolsa: a diferenca sao os
        # tickers sem barras na janela. Fixado para que uma mudanca de fonte
        # nao passe despercebida.
        self.assertEqual(len(_le("pg_universo_diag.csv")), 5288)

    def test_spreads_medidos_com_mercado_aberto(self):
        # A base do limiar de 2% do F-2: 17 observacoes de uma sessao.
        linhas = _le("spreads_3007.csv")
        self.assertEqual(len(linhas), 17)
        self.assertIn("NRXS", {l["Ticker"] for l in linhas})

    def test_perfil_t2_dos_removidos_pelo_gate_usd(self):
        removidos = {l["Ticker"] for l in _le("t2_rem_perfil.csv")}
        # Os sete que so o pipeline A aprova (Fase 5 §2).
        for t in ("USIO", "INVE", "BTMD", "CRDL", "DTI", "NRXS", "TOP"):
            self.assertIn(t, removidos)


if __name__ == "__main__":
    unittest.main()
