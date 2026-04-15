import pandas as pd
import lightgbm as lgb
from sklearn.preprocessing import StandardScaler
import requests
import joblib
import os

# FunÃ§Ã£o necessÃ¡ria para o cÃ¡lculo do RSI que o LightGBM vai aprender
def calcular_rsi(series, period=14):
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1+rs))

def auto_treinamento(ativo):
    print(f"ðŸ”„ Iniciando auto-treinamento para {ativo}...")
    
    # 1. Coleta automÃ¡tica (2000 velas de 1min)
    # Na MEXC Futuros o sÃ­mbolo usa underline: SOL_USDT
    url = f"https://contract.mexc.com/api/v1/contract/kline/{ativo}?interval=Min1"
    
    try:
        response = requests.get(url, timeout=15)
        dados = response.json()['data']
        
        # Converter os dados para DataFrame e garantir que sÃ£o nÃºmeros
        df = pd.DataFrame({
            'close': [float(x) for x in dados['close']],
            'high': [float(x) for x in dados['high']],
            'low': [float(x) for x in dados['low']]
        })
        
        # 2. Engenharia de Recursos
        df['rsi'] = calcular_rsi(df['close']) 
        df['volatilidade'] = df['high'] - df['low']
        # Alvo: Prever se o preÃ§o vai cair (1) ou nÃ£o (0) nos prÃ³ximos 5 min
        df['target'] = (df['close'].shift(-5) < df['close']).astype(int) 
        
        df.dropna(inplace=True)
        
        # 3. Treinamento
        X = df[['rsi', 'volatilidade']]
        y = df['target']
        
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        train_data = lgb.Dataset(X_scaled, label=y)
        params = {
            'objective': 'binary',
            'metric': 'binary_logloss',
            'boosting_type': 'gbdt',
            'verbosity': -1
        }
        
        model = lgb.train(params, train_data, num_boost_round=100)
        
        # 4. Salva os arquivos no diretÃ³rio atual
        model.save_model(f'model_{ativo}.txt')
        joblib.dump(scaler, f'scaler_{ativo}.pkl')
        
        print(f"âœ… Arquivos gerados: model_{ativo}.txt e scaler_{ativo}.pkl")
        
    except Exception as e:
        print(f"âŒ Erro ao processar {ativo}: {e}")

# --- COMANDO DE EXECUÃ‡ÃƒO (O que faltava) ---
if __name__ == "__main__":
    # Treina para os dois ativos que vocÃª quer operar
    auto_treinamento("SOL_USDT")
    auto_treinamento("DOGE_USDT")
    print("\nðŸš€ Tudo pronto para o Alfabot operar!")
