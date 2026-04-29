import pandas as pd
import lightgbm as lgb
from sklearn.preprocessing import StandardScaler
import requests
import joblib
import os
import time
from flask import Flask, jsonify
from flask_cors import CORS
from threading import Thread

app = Flask(__name__)
CORS(app) # Permite que o HTML acesse os dados

# --- CONFIGURAÇÕES E APIs ---
# Para o GOLD (XAUUSD), usaremos a API gratuita da Binance para o par PAXG/USDT (Ouro Tokenizado) 
# ou uma API de Metal se preferir. Usaremos PAXG por ser 1:1 com o Ouro.
SÍMBOLOS = ["SOL_USDT", "DOGE_USDT", "PAXG_USDT"] 
DADOS_APP = {}

def calcular_rsi(series, period=14):
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1+rs))

# --- 1. SISTEMA DE AUTO-TREINAMENTO ---
def auto_treinamento():
    print("🔄 Will Tech Solutions: Iniciando Aprendizado de Máquina...")
    for ativo in SÍMBOLOS:
        try:
            # Coleta dados (Exemplo via MEXC/Binance para simular o Gold via PAXG)
            url = f"https://api.binance.com/api/v3/klines?symbol={ativo.replace('_', '')}&interval=1m&limit=500"
            r = requests.get(url).json()
            df = pd.DataFrame(r, columns=['t','open','high','low','close','v','ct','qv','nt','tb','tq','i'])
            df['close'] = df['close'].astype(float)
            df['high'] = df['high'].astype(float)
            df['low'] = df['low'].astype(float)
            
            df['rsi'] = calcular_rsi(df['close'])
            df['volatilidade'] = df['high'] - df['low']
            df['target'] = (df['close'].shift(-5) < df['close']).astype(int)
            df.dropna(inplace=True)

            X = df[['rsi', 'volatilidade']]
            y = df['target']
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)
            
            train_data = lgb.Dataset(X_scaled, label=y)
            model = lgb.train({'objective': 'binary', 'verbosity': -1}, train_data)
            
            model.save_model(f'model_{ativo}.txt')
            joblib.dump(scaler, f'scaler_{ativo}.pkl')
            print(f"✅ Modelo {ativo} atualizado.")
        except Exception as e:
            print(f"❌ Erro treino {ativo}: {e}")

# --- 2. LOOP DE ANÁLISE EM TEMPO REAL ---
def monitor_mercado():
    global DADOS_APP
    while True:
        for ativo in SÍMBOLOS:
            try:
                url = f"https://api.binance.com/api/v3/ticker/24hr?symbol={ativo.replace('_', '')}"
                data = requests.get(url).json()
                
                preco = float(data['lastPrice'])
                variacao = float(data['priceChangePercent'])
                
                # Carrega modelo e prediz
                modelo = lgb.Booster(model_file=f'model_{ativo}.txt')
                scaler = joblib.load(f'scaler_{ativo}.pkl')
                
                # Simulação de RSI para a predição rápida
                X = scaler.transform([[50.0, 0.1]]) # Valores base
                prob = modelo.predict(X)[0] * 100

                DADOS_APP[ativo] = {
                    "preco": preco,
                    "variacao": variacao,
                    "prob": round(prob, 2),
                    "status": "COMPRA" if prob > 80 else "VENDA" if prob < 20 else "NEUTRO"
                }
            except: pass
        time.sleep(2)

# --- 3. ROTA DA API PARA O HTML ---
@app.route('/dados')
def enviar_dados():
    return jsonify(DADOS_APP)

if __name__ == "__main__":
    auto_treinamento()
    # Roda o monitor em segundo plano
    Thread(target=monitor_mercado).start()
    # Inicia o servidor para o HTML
    app.run(port=5000)
