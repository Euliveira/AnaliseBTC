import requests
import time
import hmac
import hashlib
import os
import pandas as pd
import lightgbm as lgb
import joblib
from sklearn.preprocessing import StandardScaler
from datetime import datetime
import pytz
from config_client import TOKEN_TELEGRAM, CHAT_ID

# --- CONFIGURAÇÕES ---
fuso_sp = pytz.timezone('America/Sao_Paulo')

# Endpoints
URL_BINANCE = 'https://api.binance.com/api/v3'
URL_MEXC = 'https://contract.mexc.com/api/v1/contract'

def enviar_telegram(mensagem):
    url = f"https://api.telegram.org/bot{TOKEN_TELEGRAM}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": mensagem, "parse_mode": "Markdown"}
    try:
        requests.post(url, json=payload, timeout=5)
    except:
        pass

def calcular_rsi(series, period=14):
    if len(series) < period + 1: return 50.0
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return float(100 - (100 / (1 + rs)).iloc[-1])

# --- EXIBIÇÃO VERTICAL PERFEITA ---
def exibir_painel(ativo, valor, rsi, prob, status, fonte):
    os.system('clear')
    agora = datetime.now(fuso_sp).strftime('%d/%m/%Y %H:%M:%S')
    tendencia = "QUEDA (SHORT) 🧊" if rsi > 50 else "ALTA (LONG) 🔥"
    
    print("\033[1;32m🚀 Sistema Will Tech Solutions | Inteligência Artificial\033[0m")
    print(f"🕒 Horário (SP): {agora} | Fonte: {fonte}")
    print("-" * 45)
    print(f"📊 ATIVO:     {ativo}")
    print(f"💰 VALOR:     ${valor:.4f}")
    print(f"📈 TENDÊNCIA: {tendencia}")
    print(f"🧬 RSI:       {rsi:.2f}")
    print(f"🧠 IA CONF.:  {prob:.2f}%")
    print(f"📡 STATUS:    {status}")
    print("-" * 45)
    print("Monitorando mercado e aplicando dados históricos...")

def alertar_entrada(ativo, direcao, prob, entrada):
    tp = entrada * 0.995 if "VENDA" in direcao else entrada * 1.005
    sl = entrada * 1.003 if "VENDA" in direcao else entrada * 0.997
    
    msg = (
        f"Alfabot - SNIPER:\n"
        f"🚨 *SINAL DE ENTRADA CONFIRMADO*\n\n"
        f"💰 Ativo: {ativo}\n"
        f"Direção: {direcao}\n"
        f"🎯 Probabilidade IA: {prob:.2f}%\n\n"
        f"📊 DADOS TÉCNICOS:\n"
        f"📍 Entrada: {entrada:.4f}\n"
        f"✅ Take Profit: {tp:.4f}\n"
        f"❌ Stop Loss: {sl:.4f}\n\n"
        f"🚀 *Willian Oliveira | Tecnologia e IA*"
    )
    print("\a")
    enviar_telegram(msg)
    time.sleep(5)

# --- ANALISADOR COM CARREGAMENTO DE MODELO ANTERIOR ---
def analisar_sniper(ativo, modo):
    try:
        # 1. Pega os dados atuais da BINANCE ou MEXC
        if modo == '1':
            url = f"{URL_BINANCE}/klines?symbol={ativo}&interval=1m&limit=100"
            r = requests.get(url, timeout=10).json()
            fechamentos = pd.Series([float(f[4]) for f in r])
            volatilidade = float(r[-1][2]) - float(r[-1][3])
            fonte = "BINANCE (SINAIS)"
        else:
            ativo_mexc = ativo.replace("USDT", "_USDT")
            url = f"{URL_MEXC}/kline/{ativo_mexc}?interval=Min1"
            r = requests.get(url, timeout=10).json()['data']
            fechamentos = pd.Series([float(x) for x in r['close']])
            volatilidade = float(r['high'][-1]) - float(r['low'][-1])
            fonte = "MEXC (AUTOMAÇÃO)"

        valor_atual = fechamentos.iloc[-1]
        rsi_atual = calcular_rsi(fechamentos)
        
        # 2. CARREGA O CONHECIMENTO PRÉVIO (A inteligência que já está baixada)
        probabilidade = 50.0
        try:
            # O código busca exatamente os nomes de arquivos do seu treinamento
            nome_base = ativo.replace("USDT", "_USDT")
            modelo = lgb.Booster(model_file=f'model_{nome_base}.txt')
            scaler = joblib.load(f'scaler_{nome_base}.pkl')
            
            # Aplica o Scikit-learn (Sklearn) para preparar os dados atuais
            X = scaler.transform([[rsi_atual, volatilidade]])
            probabilidade = modelo.predict(X)[0] * 100
        except:
            pass # Se não achar o arquivo, o painel mostra 50%

        # 3. Decisão baseada no Aprendizado + RSI
        status = "\033[1;33mAGUARDANDO OPORTUNIDADE...\033[0m"
        
        if rsi_atual >= 65 and probabilidade > 85:
            status = "\033[1;31mVENDA (SHORT) SUGERIDA!\033[0m"
            exibir_painel(ativo, valor_atual, rsi_atual, probabilidade, status, fonte)
            alertar_entrada(ativo, "VENDA (SHORT)", probabilidade, valor_atual)
        elif rsi_atual <= 35 and probabilidade > 85:
            status = "\033[1;32mCOMPRA (LONG) SUGERIDA!\033[0m"
            exibir_painel(ativo, valor_atual, rsi_atual, probabilidade, status, fonte)
            alertar_entrada(ativo, "COMPRA (LONG)", probabilidade, valor_atual)
        else:
            exibir_painel(ativo, valor_atual, rsi_atual, probabilidade, status, fonte)

    except Exception as e:
        print(f"Erro no processamento: {e}")

# --- MENU ---
os.system('clear')
print("\033[1;34m================================================")
print("      WILL TECH SOLUTIONS - SNIPER v3.2")
print("================================================\033[0m")
print("1 - 📊 SINAIS VIA BINANCE (SOLUSDT)")
print("2 - 📊 SINAIS VIA BINANCE (DOGEUSDT)")
print("3 - 🤖 OPERAÇÃO VIA MEXC")
print("0 - SAIR")
op = input("\nEscolha: ")

if op in ['1', '2', '3']:
    par = "DOGEUSDT" if op == '2' else "SOLUSDT"
    modo_exec = '1' if op in ['1', '2'] else '2'
    try:
        while True:
            analisar_sniper(par, modo_exec)
            time.sleep(2)
    except KeyboardInterrupt:
        print("\nFinalizado.")
