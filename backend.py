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
import warnings

# Silencia avisos de nomes de colunas do Scikit-Learn
warnings.filterwarnings("ignore", category=UserWarning)

app = Flask(__name__)
CORS(app)

# Lista de ativos padronizada para o HTML
SÍMBOLOS = ["BTCUSDT", "SOLUSDT", "PAXGUSDT"] 
DADOS_APP = {}

def calcular_rsi(series, period=14):
    if len(series) < period: return 50.0
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1+rs)).iloc[-1]

def auto_treinamento():
    print("🔄 Will Tech Solutions: Treinando Modelos de IA...")
    for ativo in SÍMBOLOS:
        try:
            url = f"https://api.binance.com/api/v3/klines?symbol={ativo}&interval=1m&limit=500"
            r = requests.get(url, timeout=10).json()
            df = pd.DataFrame(r, columns=['t','o','h','l','c','v','ct','qv','nt','tb','tq','i'])
            df['close'] = df['close'].astype(float)
            df['high'] = df['high'].astype(float)
            df['low'] = df['low'].astype(float)
            
            # Engenharia de recursos para o LightGBM
            df['rsi_val'] = (df['close'].diff().where(df['close'].diff() > 0, 0)).rolling(14).mean()
            df['volatilidade'] = df['high'] - df['low']
            df['target'] = (df['close'].shift(-5) < df['close']).astype(int)
            df.dropna(inplace=True)

            X = df[['rsi_val', 'volatilidade']]
            y = df['target']
            
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)
            
            train_data = lgb.Dataset(X_scaled, label=y)
            model = lgb.train({'objective': 'binary', 'verbosity': -1}, train_data)
            
            model.save_model(f'model_{ativo}.txt')
            joblib.dump(scaler, f'scaler_{ativo}.pkl')
            print(f"✅ Inteligência de {ativo} atualizada.")
        except Exception as e:
            print(f"❌ Erro ao treinar {ativo}: {e}")

def monitor_mercado():
    global DADOS_APP
    print("📡 Monitoramento em tempo real iniciado...")
    while True:
        for ativo in SÍMBOLOS:
            try:
                # 1. Pega preço atual
                url = f"https://api.binance.com/api/v3/ticker/24hr?symbol={ativo}"
                res = requests.get(url, timeout=5).json()
                
                preco = float(res['lastPrice'])
                variacao = res['priceChangePercent']

                # 2. Faz predição com o modelo salvo
                modelo = lgb.Booster(model_file=f'model_{ativo}.txt')
                scaler = joblib.load(f'scaler_{ativo}.pkl')
                
                # Criando input com nomes de colunas para evitar o erro anterior
                X_input = pd.DataFrame([[50.0, 0.01]], columns=['rsi_val', 'volatilidade'])
                X_scaled = scaler.transform(X_input)
                prob = modelo.predict(X_scaled)[0] * 100

                DADOS_APP[ativo] = {
                    "preco": round(preco, 4) if "USDT" in ativo else preco,
                    "variacao": variacao,
                    "prob": round(prob, 2)
                }
            except:
                continue
        time.sleep(2)

@app.route('/dados')
def enviar_dados():
    return jsonify(DADOS_APP)

if __name__ == "__main__":
    auto_treinamento()
    # Inicia a thread de monitoramento
    t = Thread(target=monitor_mercado)
    t.daemon = True
    t.start()
    
    print("🚀 Servidor da Will Tech Solutions rodando em http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=False)
