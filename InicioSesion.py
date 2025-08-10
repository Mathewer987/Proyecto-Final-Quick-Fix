from flask import Flask, render_template, request
import os
import firebase_admin
from firebase_admin import credentials, firestore

app = Flask(__name__, template_folder=os.path.abspath(os.path.dirname(__file__)))

# Inicializar Firebase
cred = credentials.Certificate("firebase-key.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

ALLOWED_ROLES = {'clientes', 'trabajadores', 'desempleados'}

@app.route('/')
def index():
    return render_template('Inicio_de_Sesion.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('username', '').strip()
    password = request.form.get('contra', '').strip()  # fijate que en el HTML el name es 'contra'
    role = request.form.get('rol', '').strip()  # el name en radio buttons es 'rol'

    if role not in ALLOWED_ROLES:
        return render_template('Inicio_de_Sesion.html', error="Rol inválido.", color="red")

    if not email or not password:
        return render_template('Inicio_de_Sesion.html', error="Por favor, completá todos los campos.", color="red")

    try:
        # Hacer query filtrando por mail y contra
        users_ref = db.collection(role)
        query = users_ref.where("mail", "==", email).where("contra", "==", password).limit(1).stream()
        usuario = None
        for doc in query:
            usuario = doc.to_dict()
            break

        if usuario:
            nombre = usuario.get('nombre', 'Usuario')
            return render_template('Inicio_de_Sesion.html', success=f"¡Bienvenido, {nombre}!", color="green")
        else:
            return render_template('Inicio_de_Sesion.html', error="Usuario o contraseña incorrectos.", color="red")
    except Exception as e:
        return render_template('Inicio_de_Sesion.html', error=f"Error: {str(e)}", color="red")

if __name__ == '__main__':
    app.run(debug=True)
