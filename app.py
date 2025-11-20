from flask import Flask, render_template
import firebase_admin
from firebase_admin import credentials, firestore
import os
import json   # <-- SUPER IMPORTANTE

# Inicializar Firebase
if not firebase_admin._apps:
    if "FIREBASE_CREDENTIALS" in os.environ:
        cred_dict = json.loads(os.environ["FIREBASE_CREDENTIALS"])
        
        # Importante: arreglar saltos de línea
        cred_dict["private_key"] = cred_dict["private_key"].replace("\\n", "\n")

        cred = credentials.Certificate(cred_dict)
    else:
        cred = credentials.Certificate("firebase.json")  # solo local

    firebase_admin.initialize_app(cred)

db = firestore.client()

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "default-secret")


@app.route("/")
def home():
    return render_template("test.html")


@app.route("/ver_clientes")
def ver_clientes():
    docs = db.collection("clientes").get()
    if not docs:
        return "No hay documentos en 'clientes'"
    return "<br>".join([doc.id for doc in docs])


@app.route("/agregar_trabajador")
def agregar_trabajador():
    col = db.collection("trabajadores")
    docs = col.get()
    next_num = len(docs) + 1
    nombre = f"prueba{next_num}"

    col.document(nombre).set({"mensaje": "Documento de prueba creado"})
    return f"Documento creado: {nombre}"


if __name__ == "__main__":
    app.run(debug=True)
