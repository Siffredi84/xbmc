"""Encadeia o funil completo. Uma execucao = um comando.

    POLYGON_KEY=... FINNHUB_KEY=... python3 run.py

Etapas: universo -> guarda de calendario -> indicadores+quarentena ->
gates tecnicos -> enriquecimento -> gates fundamentais -> identidade ->
encaminhamento. Qualquer etapa que nao consiga decidir com dados fiaveis
etiqueta e segue; so falhas duras interrompem.
"""
import json, os, sys
import pandas as pd
import requests
import config as C
import polygon, fase0, finnhub, identidade, encaminhamento
import fred, continuacao, evento, edgar, descoberta, tripwire


def main():
    for v in ("POLYGON_KEY", "FINNHUB_KEY", "FRED_KEY", "MARKETAUX_KEY"):
        if v not in os.environ:
            sys.exit(f"falta a variavel de ambiente {v}")

    print("[0/11] gate macro FRED")
    regime, stress, macro = fred.avalia()
    print(f"      regime: {regime} (stress {stress}) — {fred.veredicto(regime)}")
    macro.to_csv("saida_macro.csv", index=False)

    print("[1/11] universo Polygon")
    polygon.main() if hasattr(polygon, "main") else None
    u = json.load(open("pg_universe.json"))
    sessao = u.get("ultima_sessao", "desconhecida")
    print(f"      ultima sessao: {sessao}")

    print("[2/11] indicadores, quarentena e gates tecnicos")
    fase0.main()
    s = pd.read_csv("pg_shortlist63.csv")
    print(f"      shortlist: {len(s)}")

    print("[3/11] enriquecimento Finnhub (cache por sessao)")
    precos = dict(zip(s.Ticker, s.Price))
    regs, falhas = finnhub.enriquece(list(s.Ticker), sessao, precos)
    if falhas:
        print(f"      SEM DADOS (nao reprovados, para revisao): {falhas}")
    e = pd.DataFrame(regs).merge(s, on="Ticker")
    e["High52_pct"] = (e.Price / e.High52 - 1) * 100
    e["Low52_pct"] = (e.Price / e.Low52 - 1) * 100
    e["queda_sem_recuperacao"] = [
        finnhub.queda_sem_recuperacao(h, l)
        for h, l in zip(e.High52_pct, e.Low52_pct)
    ]

    print("[4/11] gates fundamentais")
    # D0-2: tres estados, nao dois. None e 'nao verificado' e nao pode entrar
    # nos finalistas por omissao — passa a fila propria, como o resto do funil.
    qsr = e.queda_sem_recuperacao
    fin = e[(e.MCapM.between(C.MCAP_MIN_M, C.MCAP_MAX_M)) &
            (e.High52_pct <= C.HIGH52_MAX_PCT) &
            (qsr == False)].copy()
    queda = list(e[qsr == True].Ticker)
    queda_indet = list(e[qsr.isna()].Ticker)
    if queda_indet:
        print(f"      52 semanas sem dados (nao verificados, nao aprovados): "
              f"{queda_indet}")
    mcap_div = list(e[e.MCapEstado == "DIVERGENTE"].Ticker)
    print(f"      finalistas: {len(fin)}")
    if queda:
        print(f"      excluidos por queda >80% sem recuperacao: {queda}")
    if mcap_div:
        print(f"      market cap divergente >{C.MCAP_DIVERGENCIA_MAX_PCT}%: {mcap_div}")

    print("[5/11] gate de identidade")
    depth = identidade.load_ibkr("ibkr_depth.json")
    sem = identidade.cobertura(fin, depth)
    if sem:
        print(f"      sem cobertura IBKR (vao ao arbitro): {sem}")
    res = identidade.resolve(fin, depth, verbose=False)
    print(f"      {(res.estado == 'OK').sum()} OK, "
          f"{(res.estado == 'REVER').sum()} para revisao")
    fin = fin.merge(res[["Ticker", "estado"]], on="Ticker")

    print("[6/11] encaminhamento")
    fin = encaminhamento.classifica(fin)
    f = encaminhamento.filas(fin)
    for k, v in f.items():
        print(f"      {k}: {len(v)} {v}")

    print("[7/11] fila de continuacao (insiders e diluicao)")
    desde = (pd.Timestamp(sessao) - pd.Timedelta(days=182)).date().isoformat()
    cont = pd.DataFrame(continuacao.analisa(f["continuacao"], sessao, desde, sessao))
    cont.to_csv("saida_continuacao.csv", index=False)
    dil = list(cont[cont.get("risco_diluicao", False) == True].Ticker)
    print(f"      {len(cont)} analisados | com prateleira/ATM activa: {dil}")

    print("[8/11] fila de evento (noticias e sentimento)")
    recente = (pd.Timestamp(sessao) - pd.Timedelta(days=8)).date().isoformat()
    ev = pd.DataFrame(evento.analisa(f["evento"], sessao, recente, sessao))
    ev.to_csv("saida_evento.csv", index=False)
    sem_cob = list(ev[ev.estado == "SEM_COBERTURA"].Ticker)
    print(f"      {len(ev)} analisados | sem cobertura noticiosa: {sem_cob}")

    print("[9/11] red flags e catalisadores (EDGAR)")
    alvo = sorted(set(f["evento"] + f["continuacao"] + f["fila_20f"]))
    d8k = (pd.Timestamp(sessao) - pd.Timedelta(days=90)).date().isoformat()
    dsp = (pd.Timestamp(sessao) -
           pd.Timedelta(days=C.REVERSE_SPLIT_JANELA_DIAS)).date().isoformat()
    try:
        splits = polygon.reverse_splits(dsp, sessao, tickers=alvo)
    except (requests.RequestException, RuntimeError) as exc:
        # D0-3: o except era largo. Um NameError ou um erro de schema no parser
        # de splits ficava indistinguivel de 'o fornecedor nao respondeu' — o
        # funil seguia sem verificacao de splits e nao havia forma de saber
        # porque. Falhas de rede etiquetam; erros de codigo tem de rebentar.
        print(f"      reverse splits SEM DADOS: {str(exc)[:120]}")
        splits = None
    ed = pd.DataFrame(edgar.analisa(alvo, sessao, d8k, dsp,
                                    reverse_splits=splits))
    ed.to_csv("saida_edgar.csv", index=False)
    repr_ = list(ed[ed.get("reprova", False) == True].Ticker)
    rever = list(ed[ed.get("gc_estado", "") == "A_REVER"].Ticker)
    falhou = list(ed[ed.estado != "OK"].Ticker)
    print(f"      REPROVADOS por red flag: {repr_}")
    print(f"      going concern a rever: {rever}")
    if falhou:
        print(f"      sem verificacao (nao aprovados): {falhou}")
    fin["red_flag"] = fin.Ticker.isin(repr_)
    fin["gc"] = fin.Ticker.map(dict(zip(ed.Ticker, ed.get("gc_estado", "")))).fillna("NAO_VERIFICADO")
    nao_us = sorted(set(fin[fin.regime_reporte != "10-Q"].Ticker) |
                    set(fin[fin.get("Pais", "US") != "US"].Ticker))

    print("[10/11] sinais de descoberta precoce")
    aprov = sorted(set(alvo) - set(repr_) - set(falhou))
    ev_art = ev if "n_marketaux" in ev.columns else None
    desc = descoberta.compila(aprov, sessao, u["bars"], insiders=cont, artigos=ev_art)
    desc.to_csv("saida_descoberta.csv", index=False)
    top = desc.head(3)[["Ticker", "n_sinais"]].values.tolist()
    print(f"      mais sinais: {top}")

    print("[11/11] tripwire Finviz")
    tw = tripwire.compara(aprov, C, bars=u["bars"], explicados=nao_us)
    if tw["estado"] == "NAO_COMPARAVEL":
        print(f"      {tw['detalhe']}")
    else:
        print(f"      Finviz {tw['finviz']} vs funil {tw['polygon']}, "
              f"comuns {tw['comuns']} | divergencia inexplicada "
              f"{tw['divergencia_inexplicada']}"
              f"{'  <<< ALARME' if tw['alarme'] else ''}")

    fin = fin.merge(desc[["Ticker", "n_sinais"]], on="Ticker", how="left")
    fin.to_csv("saida_finalistas.csv", index=False)
    json.dump({"sessao": sessao, "regime_macro": regime, "stress_macro": stress,
               "filas": f, "sem_dados": falhas,
               "market_cap_divergente": mcap_div,
               "queda_sem_recuperacao": queda,
               "queda_nao_verificada": queda_indet,
               "rever_identidade": list(res[res.estado == "REVER"].Ticker),
               "risco_diluicao": dil, "sem_cobertura_noticiosa": sem_cob,
               "reprovados_red_flag": repr_, "going_concern_a_rever": rever,
               "sem_verificacao_edgar": falhou,
               "aprovados": sorted(set(alvo) - set(repr_) - set(falhou)),
               "tripwire": tw},
              open("saida_resumo.json", "w"), indent=1)
    print("\nescrito: saida_finalistas.csv, saida_macro.csv, "
          "saida_continuacao.csv, saida_evento.csv, saida_edgar.csv, "
          "saida_resumo.json")


if __name__ == "__main__":
    main()
