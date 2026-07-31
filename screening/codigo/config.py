"""Ponto unico de verdade para limiares e parametros.

Nada de numeros magicos espalhados pelos modulos: se um valor governa uma
decisao do funil, vive aqui e e discutivel a olho nu.
"""

# --- janela de calculo -------------------------------------------------------
JANELA_VOLUME = 63        # sessoes de mercado para a media de volume (3 meses)
JANELA_TENDENCIA = 20     # sessoes para o racio de tendencia (20/63)
JANELA_RSI = 14
JANELA_SMA = 20
BUFFER_DIAS_UTEIS = 1.12  # margem para feriados ao pedir dias ao Polygon

# --- gates quantitativos (documento de criterios) ----------------------------
PRECO_MIN, PRECO_MAX = 1.0, 7.0
MCAP_MIN_M, MCAP_MAX_M = 50.0, 500.0      # em milhoes de USD
MCAP_DIVERGENCIA_MAX_PCT = 5.0             # fonte vs shares outstanding × preco
VOL_MEDIO_MIN = 100_000                    # shares/dia

# --- gates tecnicos ----------------------------------------------------------
RELVOL_MIN = 1.2
RSI_MIN, RSI_MAX = 25.0, 60.0
SMA20_MIN_PCT = -15.0
HIGH52_MAX_PCT = -10.0                     # nao estar a menos de 10% do maximo
QUEDA_52S_MAX_PCT = -80.0                  # red flag: colapso anual
RECUPERACAO_52S_MIN_PCT = 15.0             # salva quem ja recuperou do minimo

# --- encaminhamento evento vs continuacao ------------------------------------
ECO_CORTE = 1.5           # pico relvol 20d / relvol hoje
VOL20D_BANDEIRA = 100.0   # volatilidade anualizada acima da qual se assinala
INSIDER_JANELA_DIAS = 30  # compras em mercado aberto, como no documento
REVERSE_SPLIT_JANELA_DIAS = 365

# --- integridade de serie ----------------------------------------------------
QUARENTENA_LIMIAR_FALHAS = 3
QUARENTENA_RUN_HALT = 3

# --- identidade --------------------------------------------------------------
NOME_SIMILARIDADE_MIN = 0.60
SPREAD_MAX_PCT = 2.0
USD_VOL_90D_MIN = 1_000_000

# --- rate limits (auditoria alpha-k-data-pipeline, 2026-07-22) ---------------
# Reserva de 20-25% da capacidade curta; sem retry em respostas de quota.
POLYGON_PACE_S = 13.0     # Stocks Basic: 5/min
FINNHUB_PACE_S = 1.35     # 60/min observado -> ~44/min efetivo
MARKETAUX_DIA_MAX = 75    # de 100/dia, com reserva
TWELVEDATA_PACE_S = 8.0   # 8 creditos/min

# --- universo ----------------------------------------------------------------
TIPO_VALIDO = "CS"                         # common stock: exclui ETF/fundos/units
EXCH_POLYGON = {"XNAS", "XNYS", "XASE"}    # NASDAQ, NYSE, NYSE American
EXCH_IBKR = {"NASDAQ", "NYSE", "AMEX", "ARCA", "BATS", "IEX"}
EXCH_YAHOO = {"NYQ", "NMS", "NGM", "NCM", "ASE", "PCX", "BTS", "NYS"}
