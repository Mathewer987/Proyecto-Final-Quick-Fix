# pago.py
import mercadopago
import qrcode

# ACCESS TOKEN DE TU CUENTA
sdk = mercadopago.SDK(
    "APP_USR-3383294953183085-113019-5f3a0d5372ba9908be3745d8ed4db19c-224566475"
)


def generar_enlace_pago(monto, descripcion, referencia):

    request = {
        "items": [
            {
                "title": descripcion,
                "quantity": 1,
                "currency_id": "ARS",
                "unit_price": float(monto),
            }
        ],

        "external_reference": referencia,

        "back_urls": {
            "success": "http://127.0.0.1:5000/mp/success",
            "failure": "http://127.0.0.1:5000/mp/failure",
            "pending": "http://127.0.0.1:5000/mp/pending",
        },

        #"auto_return": "approved",

        # Webhook local
        "notification_url": None,
    }

    response = sdk.preference().create(request)

    print("\n=== RESPUESTA MP ===")
    print(response)
    print("====================\n")

    data = response.get("response", {})

    if "init_point" not in data:
        raise Exception(f"Error al crear preferencia: {data}")

    return {
        "id": data["id"],
        "init_point": data["init_point"],
        "sandbox": data["sandbox_init_point"],
    }


def generar_qr(link, archivo="static/qr_pago.png"):
    img = qrcode.make(link)
    img.save(archivo)
    return archivo

