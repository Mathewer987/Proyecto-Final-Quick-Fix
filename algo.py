import requests

ACCESS_TOKEN = "APP_USR-3383294953183085-113019-5f3a0d5372ba9908be3745d8ed4db19c-224566475"

url = "https://api.mercadopago.com/pos"

data = {
    "name": "CAJA001",
    "category": 621102,  # kioscos, comercios pequeños (funciona)
    "store_id": "1234"   # cualquiera, no importa
}

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {ACCESS_TOKEN}"
}

resp = requests.post(url, json=data, headers=headers)

print(resp.status_code)
print(resp.json())
