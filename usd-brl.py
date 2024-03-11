import requests

print("""

                DESENVOLVEDOR: WILLIAN DE OLIVEIRA

""")
def obter_dados_usdt():
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    parameters = {
        'symbol': 'USDT',
        'convert': 'BRL'  # Você pode ajustar a moeda de conversão conforme necessário
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': 'd7d19d39-b71d-4588-86a7-2158f1c58fb9',  # Substitua pelo sua chave de API válida
    }

    response = requests.get(url, headers=headers, params=parameters)

    if response.status_code == 200:
        dados = response.json()
        return dados
    else:
        print("Erro ao obter dados:", response.text)
        return None

def main():
    dados_usdt = obter_dados_usdt()
    if dados_usdt:
        valor_usdt_brl = dados_usdt['data']['USDT']['quote']['BRL']['price']
        print(f"Valor do USDT em BRL: {valor_usdt_brl}")

if __name__ == "__main__":
    main()
