# app.py
from flask import Flask, render_template, request, jsonify
from pago import generar_enlace_pago, generar_qr

app = Flask(__name__)

@app.route("/pagos")
def pagina_pagos():
    return render_template("pagos.html")


@app.route("/crear-pago")
def crear_pago():

    link = generar_enlace_pago(
        monto=100,
        descripcion="Servicio Quick-Fix",
        referencia="orden_0001"
    )

    # Generar QR
    qr_path = "static/qr.png"
    generar_qr(link["init_point"], qr_path)

    return render_template(
        "resultado_pago.html",
        link=link["init_point"],
        qr_file="/" + qr_path
    )


# --- Rutas de retorno ---
@app.route("/mp/success")
def pago_exitoso():
    return render_template("success.html")


@app.route("/mp/failure")
def pago_fallido():
    return render_template("failure.html")


@app.route("/mp/pending")
def pago_pendiente():
    return render_template("pending.html")


# --- Webhook ---
@app.route("/webhooks/mercadopago", methods=["POST"])
def mp_webhook():
    print("🔔 WEBHOOK RECIBIDO 🔔")
    print(request.json)
    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    app.run(debug=True)
