import pandas as pd
import lightgbm as lgb
from sklearn.preprocessing import StandardScaler
import requests
import joblib
import os
import time
from flask import Flask, jsonify, send_from_directory # ADICIONADO AQUI
from flask_cors import CORS
from threading import Thread
import warnings

warnings.filterwarnings("ignore")

app = Flask(__name__)
CORS(app)

SÍMBOLOS = ["BTCUSDT", "SOLUSDT", "PAXGUSDT"] 
DADOS_APP = {}

def auto_treinamento():
    print("🔄 Will Tech Solutions: Iniciando Treinamento Sniper...")
    for ativo in SÍMBOLOS:
        try:
            url = f"https://api.binance.com/api/v3/klines?symbol={ativo}&interval=1m&limit=500"
            resp = requests.get(url, timeout=10)
            dados_brutos = resp.json()
            df = pd.DataFrame(dados_brutos)
            df = df[[2, 3, 4]] 
            df.columns = ['high', 'low', 'close']
            df = df.astype(float)
            df['rsi'] = (df['close'].diff().where(df['close'].diff() > 0, 0)).rolling(14).mean()
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
            print(f"✅ Inteligência {ativo} GERADA com sucesso.")
        except Exception as e:
            print(f"❌ Falha crítica no ativo {ativo}: {e}")

def monitor_mercado():
    global DADOS_APP
    print("📡 Monitorando mercado em tempo real...")
    while True:
        for ativo in SÍMBOLOS:
            try:
                url_ticker = f"https://api.binance.com/api/v3/ticker/24hr?symbol={ativo}"
                data = requests.get(url_ticker, timeout=5).json()
                preco = float(data['lastPrice'])
                variacao = data['priceChangePercent']
                if os.path.exists(f'model_{ativo}.txt'):
                    modelo = lgb.Booster(model_file=f'model_{ativo}.txt')
                    scaler = joblib.load(f'scaler_{ativo}.pkl')
                    X_input = pd.DataFrame([[50.0, 0.01]], columns=['rsi', 'volatilidade'])
                    X_scaled = scaler.transform(X_input)
                    prob = modelo.predict(X_scaled)[0] * 100
                else:
                    prob = 50.0
                DADOS_APP[ativo] = {
                    "preco": round(preco, 2),
                    "variacao": variacao,
                    "prob": round(prob, 2)
                }
            except:
                continue
        time.sleep(2)

# --- AS DUAS ROTAS QUE VOCÊ PRECISA ---

@app.route('/') # Rota da Interface
def serve_index():
    # Isso busca o arquivo index.html na mesma pasta do script
    return send_from_directory(os.getcwd(), 'index.html')

@app.route('/dados') # Rota dos Números
def enviar_dados():
    return jsonify(DADOS_APP)

if __name__ == "__main__":
    auto_treinamento()
    t = Thread(target=monitor_mercado)
    t.daemon = True
    t.start()
    print("🚀 Sistema Will Tech Solutions ONLINE!")
    app.run(host='0.0.0.0', port=5000)
