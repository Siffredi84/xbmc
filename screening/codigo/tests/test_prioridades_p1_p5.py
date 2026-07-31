import os
import sys
import types
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
os.environ.setdefault("POLYGON_KEY", "teste")


try:
    import requests  # noqa: F401
except ModuleNotFoundError:
    class _SessaoSemRede:
        def __init__(self):
            self.headers = {}

        def get(self, *args, **kwargs):
            raise AssertionError("teste unitario tentou aceder a rede")

    sys.modules["requests"] = types.SimpleNamespace(
        Session=_SessaoSemRede,
        get=lambda *a, **k: (_ for _ in ()).throw(
            AssertionError("teste unitario tentou aceder a rede")
        ),
    )

import continuacao
import edgar
import fase0
import finnhub
import polygon


class PrioridadesP1P5Test(unittest.TestCase):
    def test_p1_so_compra_aberta_e_janela_30_dias(self):
        chamadas = []

        def fake_get(path, sessao, **params):
            chamadas.append((path, params))
            if path == "stock/insider-transactions":
                return {"data": [
                    {"transactionCode": "P", "change": 100,
                     "transactionDate": "2026-07-10"},
                    {"transactionCode": "S", "change": -40,
                     "transactionDate": "2026-07-11"},
                    {"transactionCode": "A", "change": 1000,
                     "transactionDate": "2026-07-12"},
                    {"transactionCode": "M", "change": 500,
                     "transactionDate": "2026-07-13"},
                    {"transactionCode": "P", "change": 900,
                     "transactionDate": "2026-05-01"},
                ]}
            return []

        with patch.object(continuacao.finnhub, "_get", side_effect=fake_get):
            r = continuacao.analisa(
                ["TEST"], "2026-07-28", "2026-01-28", "2026-07-28"
            )[0]

        insider = next(p for path, p in chamadas
                       if path == "stock/insider-transactions")
        self.assertEqual(insider["from"], "2026-06-28")
        self.assertEqual(r["accoes_compradas"], 100)
        self.assertEqual(r["accoes_vendidas"], 40)
        self.assertEqual(r["saldo_insider"], 60)
        self.assertEqual(r["transaccoes_nao_abertas_ignoradas"], 3)

    def test_p2_market_cap_calculado_e_divergencia_etiquetada(self):
        respostas = {
            "stock/profile2": {
                "marketCapitalization": 140,
                "shareOutstanding": 100,
                "country": "US",
                "finnhubIndustry": "Technology",
            },
            "stock/metric": {
                "metric": {"52WeekHigh": 5, "52WeekLow": 0.8}
            },
            "stock/filings": [{"form": "10-Q"}],
        }
        with patch.object(finnhub, "_get",
                          side_effect=lambda path, sessao, **p: respostas[path]):
            regs, falhas = finnhub.enriquece(
                ["TEST"], "2026-07-28", {"TEST": 1.0}
            )

        self.assertEqual(falhas, [])
        self.assertEqual(regs[0]["MCapM"], 100)
        self.assertAlmostEqual(regs[0]["MCapDivergenciaPct"], 40)
        self.assertEqual(regs[0]["MCapEstado"], "DIVERGENTE")
        self.assertEqual(regs[0]["Low52"], 0.8)

    def test_p3_polygon_filtra_reverse_split_pela_razao(self):
        resposta = {
            "results": [
                {"ticker": "TLRY", "execution_date": "2026-06-01",
                 "split_from": 10, "split_to": 1},
                {"ticker": "TEST", "execution_date": "2026-05-01",
                 "split_from": 1, "split_to": 4},
            ]
        }
        with patch.object(polygon, "_get", return_value=resposta):
            r = polygon.reverse_splits(
                "2025-07-28", "2026-07-28", tickers=["TLRY", "TEST"]
            )
        self.assertIn("TLRY", r)
        self.assertNotIn("TEST", r)

    def test_p3_reverse_split_reprova_e_falha_de_fonte_nao_aprova(self):
        sub = {"filings": {"recent": {}}}
        gc = {"gc_estado": "SEM_SINAL", "gc_form": "10-Q",
              "gc_data": "2026-05-01", "gc_excerto": "-"}
        mocks = [
            patch.object(edgar, "mapa_cik", return_value={"TLRY": "1"}),
            patch.object(edgar, "submissoes", return_value=sub),
            patch.object(edgar, "going_concern", return_value=gc),
            patch.object(edgar, "eventos", return_value=(set(), [])),
        ]
        for m in mocks:
            m.start()
            self.addCleanup(m.stop)

        evento = {"TLRY": [{"execution_date": "2026-06-01",
                            "split_from": 10, "split_to": 1}]}
        confirmado = edgar.analisa(
            ["TLRY"], "2026-07-28", "2026-04-01", "2025-07-28", evento
        )[0]
        incompleto = edgar.analisa(
            ["TLRY"], "2026-07-28", "2026-04-01", "2025-07-28", None
        )[0]
        self.assertTrue(confirmado["reprova"])
        self.assertEqual(confirmado["reverse_split"], "2026-06-01")
        self.assertEqual(incompleto["estado"], "VERIFICACAO_INCOMPLETA")

    def test_p4_queda_sem_recuperacao(self):
        self.assertTrue(finnhub.queda_sem_recuperacao(-91.4, 6.1))
        self.assertFalse(finnhub.queda_sem_recuperacao(-87.0, 25.4))
        self.assertFalse(finnhub.queda_sem_recuperacao(-79.9, 1.0))

    def test_p5_tipo_e_bolsa_sao_explicitos(self):
        self.assertTrue(fase0.universo_valido({"type": "CS", "exch": "XNAS"}))
        self.assertFalse(fase0.universo_valido({"type": "CS", "exch": "OTCM"}))
        self.assertFalse(fase0.universo_valido({"type": "ETF", "exch": "XNAS"}))


if __name__ == "__main__":
    unittest.main()
