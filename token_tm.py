import requests

token = input("Digite o token do seu bot Telegram: ").strip()

url = f"https://api.telegram.org/bot{token}/getUpdates"
resp = requests.get(url, timeout=10).json()

if not resp.get("ok"):
    print("Erro ao acessar a API do Telegram")
    print(resp)
    exit()

if not resp.get("result"):
    print("Nenhuma mensagem encontrada.")
    print("👉 Abra o Telegram, vá até o bot e envie /start ou qualquer mensagem.")
    exit()

print("\nChats encontrados:\n")

for update in resp["result"]:
    # Prioridade para mensagens normais
    if "message" in update:
        chat = update["message"]["chat"]
    elif "channel_post" in update:
        chat = update["channel_post"]["chat"]
    else:
        continue

    print("Chat ID:", chat["id"])
    print("Tipo:", chat["type"])
    print("Nome:", chat.get("first_name") or chat.get("title", "Desconhecido"))
    print("-" * 40)
