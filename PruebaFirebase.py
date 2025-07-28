import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("firebase-key.json")
firebase_admin.initialize_app(cred)

db = firestore.client()


def obtener_datos_cliente(cliente_id):

    doc_ref = db.collection("clientes").document(cliente_id)
    doc = doc_ref.get()
    if doc.exists:
        datos = doc.to_dict()

        nombre = datos.get("nombre")
       
        print(f"Nombre: {nombre}")
        
        return datos  
    else:
        print(f"No existe el cliente con ID: {cliente_id}")
        return None


obtener_datos_cliente("mateoaguero31@gmail.com")

