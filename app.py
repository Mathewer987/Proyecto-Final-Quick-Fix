from flask import Flask, render_template
import firebase_admin
from firebase_admin import credentials, firestore
import os

# Inicializar Firebase
if not firebase_admin._apps:
    if "FIREBASE_CREDENTIALS" in os.environ:
        cred_dict = json.loads(os.environ["FIREBASE_CREDENTIALS"])
        cred_dict["private_key"] = cred_dict["private_key"].replace("\\n", "\n")
        cred = credentials.Certificate(cred_dict)
    else:
        cred = credentials.Certificate("firebase.json")  # Solo para pruebas locales
    
    firebase_admin.initialize_app(cred)

db = firestore.client()

app = Flask(__name__)


# RUTA PRINCIPAL: muestra el HTML
@app.route("/")
def home():
    return render_template("test.html")


# BOTÓN 1 → obtener clientes
@app.route("/ver_clientes")
def ver_clientes():
    docs = db.collection("clientes").get()
    nombres = [doc.id for doc in docs]
    return f"Documentos en 'clientes': <br>{'<br>'.join(nombres)}"


# BOTÓN 2 → agregar trabajador prueba1, prueba2, prueba3
@app.route("/agregar_trabajador")
def agregar_trabajador():
    col = db.collection("trabajadores")
    
    # detectar el próximo número
    docs = col.get()
    next_num = len(docs) + 1  # simple pero funciona
    
    nombre_doc = f"prueba{next_num}"
    
    col.document(nombre_doc).set({
        "mensaje": "Documento de prueba creado correctamente"
    })
    
    return f"Se creó el documento: {nombre_doc}"
    

if __name__ == "__main__":
    app.run(debug=True)
