from flask import Flask, render_template, redirect, url_for, session, flash, request
import os
import firebase_admin
from firebase_admin import credentials, firestore

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Configuración Firebase
cred = credentials.Certificate("firebase-key.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

ROLES_MAPPING = {
    'cliente': 'clientes',
    'trabajador': 'trabajadores',
    'desempleado': 'desempleados'
}

USER_TYPE_MAPPING = {
    'cliente': '1',
    'trabajador': '2',
    'desempleado': '3'
}

@app.route('/')
def index():
    return render_template('Inicio_de_Sesion.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('username', '').strip().lower()
        password = request.form.get('contra', '').strip()
        role_form = request.form.get('rol', '').strip()

        if not all([email, password, role_form]):
            return render_template('Inicio_de_Sesion.html', 
                                error="Por favor, completá todos los campos.",
                                color="red")

        try:
            firebase_collection = ROLES_MAPPING[role_form]
            users_ref = db.collection(firebase_collection)
            query = users_ref.where("mail", "==", email).where("contra", "==", password).limit(1)
            docs = query.get()

            if docs:
                usuario = docs[0].to_dict()
                session['is_logged_in'] = True
                session['user_name'] = usuario.get('nombre', 'Usuario')
                session['user_type'] = USER_TYPE_MAPPING[role_form]
                return redirect(url_for('home'))
            else:
                return render_template('Inicio_de_Sesion.html',
                                    error="Usuario o contraseña incorrectos.",
                                    color="red")
        except Exception as e:
            print(f"Error: {str(e)}")
            return render_template('Inicio_de_Sesion.html',
                                error="Error en el servidor. Intente nuevamente.",
                                color="red")
    return render_template('Inicio_de_Sesion.html')

@app.route('/home')
def home():
    if not session.get('is_logged_in'):
        return redirect(url_for('login'))
    return render_template('Home.html')

@app.route('/browser')
def browser():
    if not session.get('is_logged_in'):
        flash('Debes iniciar sesión primero', 'warning')
        return redirect(url_for('login'))
    
    if session.get('user_type') != '1':
        flash('Solo los clientes pueden acceder', 'error')
        return redirect(url_for('home'))
    
    # Obtener todos los trabajadores de Firebase
    try:
        trabajadores_ref = db.collection('trabajadores')
        docs = trabajadores_ref.stream()
        
        profesionales = []
        for doc in docs:
            trabajador_data = doc.to_dict()
            trabajador_data['id'] = doc.id  # Agregar el ID del documento
            
            # Obtener especialidades (campos booleanos true)
            especialidades = []
            campos_especialidad = [
                'Albañil', 'Carpintero', 'Cerrajero', 'Electricista', 
                'Fontanero_Plomero', 'Fumigador', 'Gasista_matriculado', 
                'Herrero', 'InstaladorDeRedes_WiFi', 'Instalador_de_aires_acondicionados',
                'Instalador_de_alarmas_cámaras_de_seguridad', 'Jardinero', 
                'LavadoDeAlfombras_cortinas', 'Limpieza_de_tanques_de_agua',
                'Limpieza_de_vidrios_en_altura', 'Mantenimiento_de_piletas',
                'Paisajista', 'Personal_de_limpieza', 'Pintor', 
                'Podador_de_árboles', 'Techista_Impermeabilizador',
                'TécnicoDeComputadoras_laptops', 'TécnicoDeTelevisores_equiposelectrónicos',
                'Técnico_de_celulares', 'Técnico_de_electrodomésticos', 'Técnico_de_impresoras'
            ]
            
            for especialidad in campos_especialidad:
                if trabajador_data.get(especialidad) == True:
                    # Formatear nombres para mejor visualización
                    nombre_bonito = especialidad.replace('_', ' ').title()
                    especialidades.append(nombre_bonito)
            
            # Si no tiene especialidades marcadas, usar "Servicios generales"
            if not especialidades:
                especialidades = ["Servicios generales"]
            
            trabajador_data['especialidades'] = especialidades
            trabajador_data['especialidad_principal'] = especialidades[0] if especialidades else "Servicios generales"
            
            # Asegurar que todos los campos necesarios existan
            if 'nombre' not in trabajador_data:
                trabajador_data['nombre'] = 'Nombre no disponible'
            if 'apellido' not in trabajador_data:
                trabajador_data['apellido'] = ''
            if 'rating' not in trabajador_data:
                trabajador_data['rating'] = 0
            if 'reseñas' not in trabajador_data:
                trabajador_data['reseñas'] = 0
            if 'ubicacion' not in trabajador_data:
                trabajador_data['ubicacion'] = 'Ubicación no disponible'
            if 'precio' not in trabajador_data:
                trabajador_data['precio'] = 'Consultar'
            
            profesionales.append(trabajador_data)
            
    except Exception as e:
        print(f"Error al obtener trabajadores: {str(e)}")
        profesionales = []  # Lista vacía en caso de error
        flash('Error al cargar los profesionales', 'error')
    
    return render_template('Browser.html', profesionales=profesionales)

@app.route('/perfil/<profesional_id>')
def ver_perfil(profesional_id):
    if not session.get('is_logged_in'):
        return redirect(url_for('login'))
    
    try:
        # Obtener datos del profesional específico
        doc_ref = db.collection('trabajadores').document(profesional_id)
        profesional = doc_ref.get()
        
        if profesional.exists:
            profesional_data = profesional.to_dict()
            
            # Procesar especialidades como en la función browser
            especialidades = []
            campos_especialidad = [
                'Albañil', 'Carpintero', 'Cerrajero', 'Electricista', 
                'Fontanero_Plomero', 'Fumigador', 'Gasista_matriculado', 
                'Herrero', 'InstaladorDeRedes_WiFi', 'Instalador_de_aires_acondicionados',
                'Instalador_de_alarmas_cámaras_de_seguridad', 'Jardinero', 
                'LavadoDeAlfombras_cortinas', 'Limpieza_de_tanques_de_agua',
                'Limpieza_de_vidrios_en_altura', 'Mantenimiento_de_piletas',
                'Paisajista', 'Personal_de_limpieza', 'Pintor', 
                'Podador_de_árboles', 'Techista_Impermeabilizador',
                'TécnicoDeComputadoras_laptops', 'TécnicoDeTelevisores_equiposelectrónicos',
                'Técnico_de_celulares', 'Técnico_de_electrodomésticos', 'Técnico_de_impresoras'
            ]
            
            for especialidad in campos_especialidad:
                if profesional_data.get(especialidad) == True:
                    nombre_bonito = especialidad.replace('_', ' ').title()
                    especialidades.append(nombre_bonito)
            
            profesional_data['especialidades'] = especialidades
            profesional_data['especialidad_principal'] = especialidades[0] if especialidades else "Servicios generales"
            
            return render_template('perfil_profesional.html', profesional=profesional_data)
        else:
            flash('Profesional no encontrado', 'error')
            return redirect(url_for('browser'))
            
    except Exception as e:
        print(f"Error: {str(e)}")
        flash('Error al cargar el perfil', 'error')
        return redirect(url_for('browser'))

@app.route('/contratar/<profesional_id>')
def contratar(profesional_id):
    if not session.get('is_logged_in'):
        return redirect(url_for('login'))
    
    if session.get('user_type') != '1':
        flash('Solo los clientes pueden contratar servicios', 'error')
        return redirect(url_for('home'))
    
    try:
        # Obtener datos del profesional
        doc_ref = db.collection('trabajadores').document(profesional_id)
        profesional = doc_ref.get()
        
        if profesional.exists:
            profesional_data = profesional.to_dict()
            return render_template('contratar.html', profesional=profesional_data)
        else:
            flash('Profesional no encontrado', 'error')
            return redirect(url_for('browser'))
            
    except Exception as e:
        print(f"Error: {str(e)}")
        flash('Error al cargar la página de contratación', 'error')
        return redirect(url_for('browser'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)