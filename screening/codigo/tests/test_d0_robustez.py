"""Testes de aceitacao do epico D0 — defeitos de robustez.

Referencia: docs/fase4-plano-implementacao.md, epico D0. Sao os quatro
defeitos que afectam o pipeline actual e o vNext em simultaneo, e por isso as
unicas alteracoes autorizadas ao pipeline actual durante a migracao.

Nenhum destes testes toca na rede.
"""
import ast
import os
import subprocess
import sys
import types
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import edgar
import finnhub


class TestD01ChaveNoImport(unittest.TestCase):
    """D0-1: `import polygon` sem credenciais nao pode levantar."""

    def _corre(self, codigo, com_chave):
        env = {k: v for k, v in os.environ.items() if k != "POLYGON_KEY"}
        if com_chave:
            env["POLYGON_KEY"] = "teste"
        return subprocess.run([sys.executable, "-c", codigo], cwd=str(ROOT),
                              env=env, capture_output=True, text=True)

    def test_import_sem_chave_nao_levanta(self):
        r = self._corre("import polygon; print('ok')", com_chave=False)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("ok", r.stdout)

    def test_funcoes_locais_utilizaveis_sem_chave(self):
        # A razao de ser do ticket: sem isto, nada a jusante era testavel.
        r = self._corre("import polygon; print(polygon.ultima_sessao_esperada())",
                        com_chave=False)
        self.assertEqual(r.returncode, 0, r.stderr)

    def test_chave_em_falta_falha_no_momento_da_chamada(self):
        r = self._corre(
            "import polygon\n"
            "try:\n"
            "    polygon._chave()\n"
            "except RuntimeError as e:\n"
            "    print('RUNTIME', e)\n",
            com_chave=False)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("RUNTIME", r.stdout)
        self.assertIn("POLYGON_KEY", r.stdout)

    def test_chave_lida_do_ambiente_quando_existe(self):
        r = self._corre("import polygon; print(polygon._chave())", com_chave=True)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("teste", r.stdout)


class TestD02QuedaSemRecuperacao(unittest.TestCase):
    """D0-2: dado em falta produz etiqueta (None), nunca uma decisao."""

    def test_ausencia_devolve_none(self):
        self.assertIsNone(finnhub.queda_sem_recuperacao(None, 10))
        self.assertIsNone(finnhub.queda_sem_recuperacao(-91.4, None))
        self.assertIsNone(finnhub.queda_sem_recuperacao(None, None))

    def test_nan_e_ausencia_nao_valor(self):
        self.assertIsNone(finnhub.queda_sem_recuperacao(float("nan"), 6.1))
        self.assertIsNone(finnhub.queda_sem_recuperacao(-91.4, float("nan")))

    def test_casos_medidos_mantem_se(self):
        # Os tres casos do P4 no handover. A correccao nao pode mexer neles.
        self.assertTrue(finnhub.queda_sem_recuperacao(-91.4, 6.1))    # SUPX
        self.assertTrue(finnhub.queda_sem_recuperacao(-82.6, 6.1))    # TLRY
        self.assertFalse(finnhub.queda_sem_recuperacao(-87.0, 25.4))  # BYRN
        self.assertFalse(finnhub.queda_sem_recuperacao(-79.9, 1.0))

    def test_none_nao_e_falso(self):
        # A distincao que o ticket protege: 'nao verificado' nao pode ser lido
        # como 'limpo' por um `if` distraido.
        self.assertIsNot(finnhub.queda_sem_recuperacao(None, 10), False)


class TestD02Chamador(unittest.TestCase):
    """O None tem de sobreviver ao filtro do run.py: nem aprovado, nem
    reprovado — fila propria."""

    def test_tres_filas_disjuntas(self):
        pd = __import__("pandas")
        e = pd.DataFrame({
            "Ticker": ["SUPX", "BYRN", "SEMDADOS"],
            "queda_sem_recuperacao": [True, False, None],
        })
        qsr = e.queda_sem_recuperacao
        aprovaveis = list(e[qsr == False].Ticker)
        excluidos = list(e[qsr == True].Ticker)
        indeterminados = list(e[qsr.isna()].Ticker)
        self.assertEqual(aprovaveis, ["BYRN"])
        self.assertEqual(excluidos, ["SUPX"])
        self.assertEqual(indeterminados, ["SEMDADOS"])
        self.assertEqual(len(aprovaveis) + len(excluidos) + len(indeterminados),
                         len(e))


class _Resposta:
    def __init__(self, status, texto=""):
        self.status_code = status
        self.text = texto


class TestD04BackoffSEC(unittest.TestCase):
    """D0-4: 503 repetido nao pode interromper a corrida antes de 8 tentativas."""

    def setUp(self):
        self._get, self._sleep = edgar._S.get, edgar.time.sleep
        self.esperas = []
        edgar.time.sleep = self.esperas.append

    def tearDown(self):
        edgar._S.get, edgar.time.sleep = self._get, self._sleep

    def _sequencia(self, respostas):
        it = iter(respostas)
        chamadas = []

        def falso_get(url, **kw):
            chamadas.append(url)
            return next(it)

        edgar._S.get = falso_get
        return chamadas

    def test_seis_503_consecutivos_nao_interrompem(self):
        chamadas = self._sequencia([_Resposta(503)] * 6 + [_Resposta(200, "conteudo")])
        self.assertEqual(edgar._get("https://exemplo/x"), "conteudo")
        self.assertEqual(len(chamadas), 7)

    def test_oito_tentativas_antes_de_desistir(self):
        chamadas = self._sequencia([_Resposta(503)] * edgar.TENTATIVAS)
        with self.assertRaises(edgar.FalhaRede):
            edgar._get("https://exemplo/x")
        self.assertEqual(len(chamadas), edgar.TENTATIVAS)

    def test_falha_de_rede_nunca_vira_ausencia(self):
        # FalhaRede != None. A confusao entre as duas custou 17 empresas
        # marcadas como 'sem registos na SEC' que existiam.
        self._sequencia([_Resposta(503)] * edgar.TENTATIVAS)
        with self.assertRaises(edgar.FalhaRede):
            edgar._get("https://exemplo/x")

    def test_404_continua_a_ser_ausencia(self):
        self._sequencia([_Resposta(404)])
        self.assertIsNone(edgar._get("https://exemplo/x"))

    def test_backoff_com_tecto_e_jitter(self):
        self._sequencia([_Resposta(503)] * edgar.TENTATIVAS)
        with self.assertRaises(edgar.FalhaRede):
            edgar._get("https://exemplo/x")
        recuos = [s for s in self.esperas if s != edgar.PACE]
        self.assertEqual(len(recuos), edgar.TENTATIVAS)
        tecto = edgar.BACKOFF_MAX_S * (1 + edgar.JITTER)
        self.assertTrue(all(0 < s <= tecto for s in recuos), recuos)
        # jitter: nao ha duas esperas identicas para o mesmo expoente
        self.assertNotEqual(recuos[-1], recuos[-2])
        self.assertGreater(sum(recuos), 60)   # paciencia real, nao 31 s


class TestD03ExceptRestrito(unittest.TestCase):
    """D0-3: o bloco de splits so pode apanhar falhas de rede. Um erro de
    codigo tem de rebentar, nao virar 'dia sem splits'."""

    def _handlers_do_bloco_de_splits(self):
        arvore = ast.parse((ROOT / "run.py").read_text(encoding="utf-8"))
        for no in ast.walk(arvore):
            if isinstance(no, ast.Try) and "reverse_splits" in ast.dump(no.body[0]):
                return no.handlers
        self.fail("bloco try dos reverse splits nao encontrado em run.py")

    def test_nao_apanha_exception_generica(self):
        nomes = []
        for h in self._handlers_do_bloco_de_splits():
            alvo = h.type
            partes = alvo.elts if isinstance(alvo, ast.Tuple) else [alvo]
            nomes += [ast.unparse(p) for p in partes]
        self.assertNotIn("Exception", nomes)
        self.assertNotIn("BaseException", nomes)
        self.assertIn("requests.RequestException", nomes)


if __name__ == "__main__":
    unittest.main()
