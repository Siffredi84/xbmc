"""Gate macro FRED — regime de risco antes de olhar para candidatos.

Small-caps a $1-7 sao o extremo da curva de risco: quando as condicoes
financeiras apertam, e a primeira classe a ser vendida e a ultima a recuperar.
Correr o funil sem saber em que regime estamos e trabalhar as cegas.

Os limiares nao sao inventados: cada serie e posicionada no seu proprio
percentil historico de 5 anos. "Spreads altos" passa a significar "altos face
a esta serie", nao face a um numero escolhido a olho.
"""
import json, os, time
import numpy as np
import pandas as pd
import requests

BASE = "https://api.stlouisfed.org/fred/series/observations"
CACHE = "fred_cache"
_S = requests.Session()

# serie -> (nome legivel, direcao de risco: +1 se subir = pior)
SERIES = {
    "BAMLH0A0HYM2": ("Spread high-yield (OAS)", +1),
    "NFCI":         ("Condicoes financeiras (Chicago Fed)", +1),
    "VIXCLS":       ("VIX", +1),
    "T10Y2Y":       ("Inclinacao 10a-2a", -1),
    "UNRATE":       ("Desemprego", +1),
}


def _serie(sid, desde="2016-01-01"):
    """Cache em disco + retry. O FRED devolve 503 esporadicos; sem retry, o
    gate macro derruba o pipeline inteiro por um soluco de rede."""
    os.makedirs(CACHE, exist_ok=True)
    cp = f"{CACHE}/{sid}_{desde}.json"
    if os.path.exists(cp):
        obs = json.load(open(cp))
    else:
        obs = None
        for tent in range(4):
            r = _S.get(BASE, params={"series_id": sid,
                                     "api_key": os.environ["FRED_KEY"],
                                     "file_type": "json",
                                     "observation_start": desde}, timeout=30)
            if r.status_code == 200:
                obs = r.json().get("observations", [])
                json.dump(obs, open(cp, "w"))
                break
            time.sleep(2 * (tent + 1))
        if obs is None:
            raise RuntimeError(f"FRED indisponivel para {sid}")
    d = pd.DataFrame(obs)
    d = d[d.value != "."]
    d["value"] = d.value.astype(float)
    d["date"] = pd.to_datetime(d.date)
    return d.set_index("date").value.sort_index()


def avalia(desde="2016-01-01"):
    linhas = []
    for sid, (nome, direcao) in SERIES.items():
        s = _serie(sid, desde)
        recente = s.tail(1260)                      # ~5 anos uteis
        atual = float(s.iloc[-1])
        pct = float((recente < atual).mean())       # percentil na propria historia
        # tendencia: variacao face a mediana das ultimas 60 observacoes
        tend = atual - float(s.tail(60).median())
        linhas.append({"serie": sid, "nome": nome, "valor": atual,
                       "percentil_5a": round(pct, 2),
                       "tendencia": round(tend, 3),
                       "stress": round(pct if direcao > 0 else 1 - pct, 2),
                       "data": s.index[-1].date().isoformat()})
        time.sleep(0.2)
    d = pd.DataFrame(linhas)
    stress = float(d.stress.mean())
    regime = ("RISK_OFF" if stress >= 0.70 else
              "NEUTRO" if stress >= 0.40 else "RISK_ON")
    return regime, round(stress, 2), d


def veredicto(regime):
    """O gate informa e dimensiona; nao bloqueia sozinho. Bloquear o funil
    inteiro por um indice composto seria substituir julgamento por um numero."""
    return {
        "RISK_ON":  "condicoes favoraveis a small-caps; funil normal",
        "NEUTRO":   "condicoes mistas; exigir catalisador mais forte por candidato",
        "RISK_OFF": "condicoes adversas; reduzir tamanho e exigir tese excepcional",
    }[regime]
