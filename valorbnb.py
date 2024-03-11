import requests

print("""

              DESENVOLVEDOR: WILLIAN DE OLIVEIRA

""")


def obter_dados_bnb():
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    parameters = {
        'symbol': 'BNB',
        'convert': 'BRL'
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': 'd7d19d39-b71d-4588-86a7-2158f1c58fb9',
    }

    response = requests.get(url, headers=headers, params=parameters)

    if response.status_code == 200:
        dados = response.json()
        return dados
    else:
        print("Erro ao obter dados:", response.text)
        return None

def main():
    dados_bnb = obter_dados_bnb()
    if dados_bnb:
        valor_bnb_brl = dados_bnb['data']['BNB']['quote']['BRL']['price']
        print(f"Valor do Binance Coin (BNB) em BRL: {valor_bnb_brl}")

if __name__ == "__main__":
    main()
