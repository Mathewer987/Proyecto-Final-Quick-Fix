from flask import Flask, render_template, jsonify
import firebase_admin
from firebase_admin import credentials, firestore
import os
import json

# Inicializar Firebase con variables separadas
def init_firebase():
    if not firebase_admin._apps:
        try:
            print("🔧 Inicializando Firebase con variables separadas...")
            
            # Verificar que tenemos todas las variables necesarias
            required_vars = ['FIREBASE_TYPE', 'FIREBASE_PROJECT_ID', 'FIREBASE_PRIVATE_KEY', 'FIREBASE_CLIENT_EMAIL']
            missing_vars = [var for var in required_vars if var not in os.environ]
            
            if missing_vars:
                raise Exception(f"Faltan variables de entorno: {missing_vars}")
            
            # Crear diccionario de credenciales
            cred_dict = {
                "type": os.environ["FIREBASE_TYPE"],
                "project_id": os.environ["FIREBASE_PROJECT_ID"],
                "private_key_id": os.environ.get("FIREBASE_PRIVATE_KEY_ID", ""),
                "private_key": os.environ["FIREBASE_PRIVATE_KEY"].replace("\\n", "\n"),
                "client_email": os.environ["FIREBASE_CLIENT_EMAIL"],
                "client_id": os.environ.get("FIREBASE_CLIENT_ID", ""),
                "auth_uri": os.environ.get("FIREBASE_AUTH_URI", "https://accounts.google.com/o/oauth2/auth"),
                "token_uri": os.environ.get("FIREBASE_TOKEN_URI", "https://oauth2.googleapis.com/token"),
                "auth_provider_x509_cert_url": os.environ.get("FIREBASE_AUTH_PROVIDER_CERT_URL", "https://www.googleapis.com/oauth2/v1/certs"),
                "client_x509_cert_url": os.environ.get("FIREBASE_CLIENT_CERT_URL", ""),
                "universe_domain": os.environ.get("FIREBASE_UNIVERSE_DOMAIN", "googleapis.com")
            }
            
            # Limpiar campos vacíos
            cred_dict = {k: v for k, v in cred_dict.items() if v}
            
            print(f"✅ Credenciales preparadas para: {cred_dict['client_email']}")
            
            cred = credentials.Certificate(cred_dict)
            firebase_admin.initialize_app(cred)
            print("✅ Firebase inicializado correctamente")
            
        except Exception as e:
            print(f"❌ Error inicializando Firebase: {e}")
            raise

init_firebase()
db = firestore.client()

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "default-secret")

@app.route("/")
def home():
    return render_template("test.html")

@app.route("/ver_clientes")
def ver_clientes():
    try:
        docs = db.collection("clientes").get()
        if not docs:
            return "No hay documentos en 'clientes'"
        
        clientes = []
        for doc in docs:
            clientes.append(f"{doc.id}: {doc.to_dict()}")
        
        return "<br>".join(clientes)
    
    except Exception as e:
        return f"Error accediendo a clientes: {str(e)}"

@app.route("/agregar_trabajador")
def agregar_trabajador():
    try:
        col = db.collection("trabajadores")
        docs = col.get()
        next_num = len(docs) + 1
        nombre = f"prueba{next_num}"

        col.document(nombre).set({
            "mensaje": "Documento de prueba creado",
            "timestamp": firestore.SERVER_TIMESTAMP
        })
        
        return f"✅ Documento creado: {nombre}"
    
    except Exception as e:
        return f"❌ Error creando documento: {str(e)}"

@app.route("/debug")
def debug():
    """Endpoint para debuggear la configuración"""
    firebase_vars = {}
    for key, value in os.environ.items():
        if 'FIREBASE' in key:
            if 'PRIVATE_KEY' in key:
                firebase_vars[key] = {
                    "length": len(value),
                    "starts_with": value[:50] + "..." if len(value) > 50 else value
                }
            else:
                firebase_vars[key] = value
    
    # Verificar variables requeridas
    required_vars = ['FIREBASE_TYPE', 'FIREBASE_PROJECT_ID', 'FIREBASE_PRIVATE_KEY', 'FIREBASE_CLIENT_EMAIL']
    vars_status = {var: var in os.environ for var in required_vars}
    
    return jsonify({
        "firebase_vars": firebase_vars,
        "required_vars_status": vars_status,
        "firebase_initialized": len(firebase_admin._apps) > 0,
        "missing_vars": [var for var in required_vars if var not in os.environ]
    })

@app.route("/health")
def health_check():
    """Health check para verificar que todo funciona"""
    try:
        # Probar conexión a Firestore
        test_ref = db.collection("health_check").document("test")
        test_ref.set({"timestamp": firestore.SERVER_TIMESTAMP})
        test_data = test_ref.get().to_dict()
        
        return jsonify({
            "status": "healthy",
            "firebase": "connected",
            "timestamp": "ok",
            "database": "working"
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "firebase": "disconnected",
            "error": str(e)
        }), 500

if __name__ == "__main__":
    app.run(debug=True)