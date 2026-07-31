"""Fila de continuacao: quem esta a acumular, e nao sera isto diluicao?

A pergunta de falsificacao deste grupo nao e "o que aconteceu" — se houvesse
noticia, seria evento. E "quem esta do outro lado da compra". Volume elevado e
sustentado num micro-cap tanto pode ser acumulacao informada como uma empresa
a vender accoes proprias ao mercado atraves de um programa ATM.
"""
import datetime as dt
import config
import finnhub

# S-3/S-1/424B* = prateleira e ofertas ao mercado: diluicao a serio.
# S-8 = planos de accoes para empregados: rotina, nao e o mesmo risco.
# Juntar os dois faria um S-8 inofensivo parecer um programa ATM.
FORMS_DILUICAO = ("S-3", "S-1", "424B5", "424B3")
FORMS_EMPREGADOS = ("S-8",)


def _na_janela(tx, desde, ate):
    data = tx.get("transactionDate") or tx.get("filingDate")
    if not isinstance(data, str):
        return False
    data = data[:10]
    return desde <= data <= ate


def analisa(tickers, sessao, desde, ate):
    """Analisa compras abertas nos ultimos 30 dias e filings desde ``desde``.

    O intervalo longo continua a ser usado para S-3/S-1/424B*. Para insiders,
    o criterio original pede 30 dias e apenas codigo P (compra no mercado).
    Atribuicoes (A) e exercicios (M) ficam explicitamente ignorados.
    """
    desde_insider = (
        dt.date.fromisoformat(ate) - dt.timedelta(days=config.INSIDER_JANELA_DIAS)
    ).isoformat()
    out = []
    for t in tickers:
        ins = finnhub._get("stock/insider-transactions", sessao, symbol=t,
                           **{"from": desde_insider, "to": ate})
        fil = finnhub._get("stock/filings", sessao, symbol=t,
                           **{"from": desde, "to": ate})
        if ins is None or fil is None:
            out.append({"Ticker": t, "estado": "SEM_DADOS"})
            continue
        tx = ins.get("data", []) if isinstance(ins, dict) else []
        compras = [x for x in tx if _na_janela(x, desde_insider, ate)
                   and str(x.get("transactionCode", "")).upper() == "P"
                   and (x.get("change") or 0) > 0]
        vendas = [x for x in tx if _na_janela(x, desde_insider, ate)
                  and str(x.get("transactionCode", "")).upper() == "S"
                  and (x.get("change") or 0) < 0]
        abertas = {id(x) for x in compras + vendas}
        ignoradas = [x for x in tx if id(x) not in abertas]
        n_compra = sum(x.get("change", 0) for x in compras)
        n_venda = -sum(x.get("change", 0) for x in vendas)
        forms = [f.get("form") for f in (fil or []) if isinstance(f, dict)]
        dil = sorted({f for f in forms if f and f.startswith(FORMS_DILUICAO)})
        emp = sorted({f for f in forms if f and f.startswith(FORMS_EMPREGADOS)})
        out.append({
            "Ticker": t, "estado": "OK",
            "insider_compras": len(compras), "insider_vendas": len(vendas),
            "accoes_compradas": int(n_compra), "accoes_vendidas": int(n_venda),
            "saldo_insider": int(n_compra - n_venda),
            "transaccoes_nao_abertas_ignoradas": len(ignoradas),
            "janela_insider_desde": desde_insider,
            "formularios_diluicao": ",".join(dil) or "-",
            "risco_diluicao": bool(dil),
            "planos_empregados": ",".join(emp) or "-",
        })
    return out
