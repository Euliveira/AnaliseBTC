import requests

print("""
      
                     DESENVOLVEDOR: WILLIAN DE OLIVEIRA
      """)

API_KEY = "d7d19d39-b71d-4588-86a7-2158f1c58fb9" 

def get_bitcoin_price():
    url = f"https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?id=1"  # URL para obter o preço do Bitcoin em USD
    headers = {
        'X-CMC_PRO_API_KEY': API_KEY,
        'Accept': 'application/json'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        bitcoin_price = data['data']['1']['quote']['USD']['price']
        return bitcoin_price
    else:
        print("Erro ao recuperar o preço do Bitcoin.")
        return None

# Exemplo de uso
bitcoin_price = get_bitcoin_price()
if bitcoin_price:
    print("Preço do Bitcoin (BTC/USD):", bitcoin_price)
else:
    print("Não foi possível obter o preço do Bitcoin.")
