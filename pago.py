import requests
import qrcode

# -----------------------------------
# CONFIGURACIÓN
# -----------------------------------
ACCESS_TOKEN = "APP_USR-3383294953183085-113019-5f3a0d5372ba9908be3745d8ed4db19c-224566475"  
USER_ID = "224566475"                    # tu collector_id
POS_ID = "QuickFixMP"                  # el mismo que en el curl

URL = f"https://api.mercadopago.com/instore/orders/qr/seller/collectors/{USER_ID}/pos/{POS_ID}/qrs"

# -----------------------------------
# CUERPO DEL QR TRAMA (igual al curl)
# -----------------------------------
body = {
    "external_reference": "reference_12345",
    "title": "Product order",
    "description": "Purchase description.",
    "notification_url": "https://www.yourserver.com/notifications",
    "total_amount": 100,
    "items": [
        {
            "sku_number": "A123K9191938",
            "category": "marketplace",
            "title": "Point Mini",
            "description": "This is the Point Mini",
            "unit_price": 40,
            "quantity": 1,
            "unit_measure": "unit",
            "total_amount": 40
        }
    ],
    "sponsor": {
        "id": 662208785
    },
    "cash_out": {
        "amount": 0
    }
}

# -----------------------------------
# HEADERS (igual que el curl)
# -----------------------------------
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {ACCESS_TOKEN}"
}

# -----------------------------------
# PASO 1: Enviar POST para crear el QR TRAMA
# -----------------------------------
response = requests.post(URL, json=body, headers=headers)

print("STATUS CODE:", response.status_code)
print("RESPUESTA:", response.json())

if response.status_code != 201:
    print("❌ Error al crear QR trama")
    exit()

# -----------------------------------
# PASO 2: Obtener el qr_data
# -----------------------------------
qr_data = response.json().get("qr_data")

if not qr_data:
    print("❌ No vino qr_data en la respuesta.")
    exit()

print("\nQR DATA:")
print(qr_data)

# -----------------------------------
# PASO 3: Generar el QR como imagen PNG
# -----------------------------------
qr_img = qrcode.make(qr_data)
qr_img.save("qr_trama.png")

print("\n✔ QR GENERADO: qr_trama.png")
