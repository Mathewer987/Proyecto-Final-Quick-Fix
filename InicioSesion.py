from flask import Flask, render_template, request
import firebase_admin
from firebase_admin import credentials, firestore

app = Flask(__name__)

# Inicializar Firebase
cred = credentials.Certificate("firebase-key.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

@app.route('/')
def index():
    return render_template('inicio_sesion.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['username']  # acá usás email
    password = request.form['password']
    role = request.form['role']  # 'clientes', 'desempleados' o 'trabajadores'

    try:
        # Buscar documento por ID (email) en la colección según rol
        doc_ref = db.collection(role).document(email)
        doc = doc_ref.get()
        if doc.exists:
            usuario = doc.to_dict()
            if usuario.get('contra') == password:
                return render_template('Inicio_de_Sesion.html', success=f"¡Bienvenido, {usuario.get('nombre')}!")
            else:
                return render_template('Inicio_de_Sesion.html', error="Contraseña incorrecta.")
        else:
            return render_template('Inicio_de_Sesion.html', error="Usuario no encontrado.")
    except Exception as e:
        return render_template('Inicio_de_Sesion.html', error=f"Error: {str(e)}")

if __name__ == '__main__':
    app.run(debug=True)
