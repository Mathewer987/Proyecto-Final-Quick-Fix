# pago.py
import mercadopago
import qrcode
import base64
from io import BytesIO

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
            "success": "https://tu-dominio.vercel.app/mp/success",
            "failure": "https://tu-dominio.vercel.app/mp/failure",
            "pending": "https://tu-dominio.vercel.app/mp/pending",
        },
        "notification_url": None,
    }
    
    response = sdk.preference().create(request)
    data = response.get("response", {})
    
    if "init_point" not in data:
        raise Exception(f"Error al crear preferencia: {data}")
    
    return {
        "id": data["id"],
        "init_point": data["init_point"],
        "sandbox": data["sandbox_init_point"],
    }

def generar_qr_base64(link):
    """Generar QR en memoria y devolver como base64"""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(link)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    
    return f"data:image/png;base64,{img_str}"