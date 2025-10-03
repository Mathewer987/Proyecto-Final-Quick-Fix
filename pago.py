import mercadopago
import qrcode
from io import BytesIO
import base64
import time
import json
from datetime import datetime

class MercadoPagoQR:
    def __init__(self, access_token):
        """
        Inicializa la conexión con Mercado Pago
        """
        self.sdk = mercadopago.SDK(access_token)
    
    def crear_pago_qr(self, monto, descripcion, email_comprador, external_reference=None):
        """
        Crea un pago con QR code
        """
        try:
            # Crear preferencia de pago
            preference_data = {
                "items": [
                    {
                        "title": descripcion,
                        "quantity": 1,
                        "unit_price": float(monto),
                        "currency_id": "ARS"  # Puedes cambiar la moneda según tu país
                    }
                ],
                "payer": {
                    "email": email_comprador
                },
                "payment_methods": {
                    "excluded_payment_types": [
                        {"id": "credit_card"},
                        {"id": "debit_card"},
                        {"id": "ticket"}
                    ],
                    "default_payment_method_id": "pix",  # Para Brasil usar "pix"
                    "installments": 1,
                    "default_installments": 1
                },
                "notification_url": "https://tu-dominio.com/webhook",  # Configura tu webhook
                "back_urls": {
                    "success": "https://tu-dominio.com/success",
                    "failure": "https://tu-dominio.com/failure",
                    "pending": "https://tu-dominio.com/pending"
                },
                "auto_return": "approved",
                "external_reference": external_reference or f"ref_{datetime.now().timestamp()}"
            }

            # Crear la preferencia
            preference_response = self.sdk.preference().create(preference_data)
            
            if preference_response["status"] != 201:
                return {
                    "success": False,
                    "error": f"Error API: {preference_response.get('response', {}).get('message', 'Unknown error')}"
                }
            
            preference = preference_response["response"]
            
            # Obtener QR code (para Pix en Brasil) o punto de pago
            qr_code = preference.get("qr_code", "")
            
            # Para transferencias en Argentina, usar init_point
            if not qr_code:
                qr_code = preference.get("init_point", "")
            
            payment_id = preference.get("id", "")
            
            return {
                "success": True,
                "qr_code": qr_code,
                "payment_id": payment_id,
                "init_point": preference.get("init_point", ""),
                "sandbox_init_point": preference.get("sandbox_init_point", ""),
                "preference": preference
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def generar_imagen_qr(self, qr_data):
        """
        Genera una imagen del QR code
        """
        try:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(qr_data)
            qr.make(fit=True)
            
            img = qr.make_image(fill_color="black", back_color="white")
            
            # Guardar en buffer
            buffer = BytesIO()
            img.save(buffer, format="PNG")
            buffer.seek(0)
            
            # Convertir a base64 para mostrar en web
            img_str = base64.b64encode(buffer.getvalue()).decode()
            
            return f"data:image/png;base64,{img_str}"
            
        except Exception as e:
            print(f"Error generando QR: {e}")
            return None
    
    def verificar_estado_pago(self, payment_id):
        """
        Verifica el estado de un pago
        """
        try:
            payment_response = self.sdk.payment().get(payment_id)
            
            if payment_response["status"] != 200:
                return {
                    "success": False,
                    "error": f"Error al obtener pago: {payment_response}"
                }
            
            payment = payment_response["response"]
            
            estado = payment.get("status", "pending")
            monto = payment.get("transaction_amount", 0)
            
            return {
                "success": True,
                "estado": estado,
                "monto": monto,
                "detalles": payment
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def buscar_pagos_por_referencia(self, external_reference):
        """
        Busca pagos por referencia externa
        """
        try:
            filters = {
                "external_reference": external_reference
            }
            
            search_response = self.sdk.payment().search(filters=filters)
            
            if search_response["status"] != 200:
                return {
                    "success": False,
                    "error": f"Error en búsqueda: {search_response}"
                }
            
            return {
                "success": True,
                "pagos": search_response["response"]["results"]
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

# Ejemplo de uso
if __name__ == "__main__":
    # Configura tu access token
    ACCESS_TOKEN = "APP_USR-XXXXXXXXXXXX-XXXXXXXXXXXX"
    
    mp = MercadoPagoQR(ACCESS_TOKEN)
    
    # Ejemplo de creación de pago
    resultado = mp.crear_pago_qr(
        monto=1500.00,
        descripcion="Servicio de Plomería",
        email_comprador="cliente@ejemplo.com"
    )
    
    if resultado["success"]:
        print("Pago creado:", resultado["payment_id"])
        qr_image = mp.generar_imagen_qr(resultado["qr_code"])
        print("QR generado correctamente")
    else:
        print("Error:", resultado["error"])