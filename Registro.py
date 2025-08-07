import tkinter as tk
from tkinter import filedialog
import webbrowser
import threading
import os
import time
import unidecode
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore
import http.server
import socketserver
import pytz

cred = credentials.Certificate("firebase-key.json")
firebase_admin.initialize_app(cred)

db = firestore.client()



ruta_html = "C:\\Users\\HOME\\Documents\\QuickFix\\maps.html"

root = tk.Tk()
root.withdraw()  # Oculta la ventana principal

# Función para seleccionar un archivo PDF
def seleccionar_pdf():
    return filedialog.askopenfilename(
        title="Seleccionar tu CV en formato PDF",
        filetypes=[("Archivos PDF", "*.pdf")]
    )

    


Devuelta = None

print("¿Qué querés hacer?")
print("1. Ingresar")
print("2. Registrarte")

opcion = input("Elegí una opción (1 o 2): ")

if opcion == "1":

    print("¿Cual es tu profesion?")
    print("1. Trabajador")
    print("2. Cliente")
    print("3. Desempleado")

    profesion = input("Elegí una opción (1, 2 o 3): ")
    
    if profesion == "1":

        mail = input("Ingresá tu mail: ")
        contraseña = input("Ingresá tu contraseña: ")

        trabajadores_ref = db.collection("trabajadores")
        query = (
            trabajadores_ref
            .where("mail", "==", mail)
            .where("contra", "==", contraseña)
            .limit(1)
            .stream()
        )
        
        usuario = None
        for doc in query:
            usuario = doc.to_dict()
            break  

        if usuario:
            nombre = usuario.get("nombre", "usuario")  
            print("✅ Inicio de sesión exitoso. ¡Bienvenido,", nombre + "!")
        else:
            print("❌ Datos incorrectos. Por favor, intentá nuevamente.")  


    
    elif profesion == "2":
        mail = input("Ingresá tu mail: ")
        contraseña = input("Ingresá tu contraseña: ")
        
        clientes_ref = db.collection("clientes")
        query = (
            clientes_ref
            .where("mail", "==", mail)
            .where("contra", "==", contraseña)
            .limit(1)
            .stream()
        )
        
        usuario = None
        for doc in query:
            usuario = doc.to_dict()
            break  
       

        if usuario:
            nombre = usuario.get("nombre", "usuario")  
            print("✅ Inicio de sesión exitoso. ¡Bienvenido,", nombre + "!")

            Cmail = mail

            print("¿Q queres hacer ahora?")
            print("1. Solicitar CV de trabajador")
            print("2. Contratar a un trabajador para un trabajo")

            QHacer = input("Elegí una opción (1 o 2): ")
            if QHacer == "1": #modifcar para firestore
                MailTra = input("Ingresá el mail del trabajador: ")

                cursor.execute('SELECT "CV" FROM trabajador WHERE "Mail" = %s', (MailTra,))
                CVA = cursor.fetchone()

                if CVA and CVA[0]:
                    rutaCVR = "CV_" + MailTra.replace("@", "_at_").replace(".", "_") + ".pdf"
                    with open(rutaCVR, "wb") as f:
                        f.write(CVA[0])
                    print(f"✅ CV recuperado y guardado como '{rutaCVR}'.")
                    
                    webbrowser.open(rutaCVR)
            
            
            elif QHacer == "2":
                 especializaciones_legibles = {
            1: "Fontanero / Plomero",
            2: "Electricista",
            3: "Gasista matriculado",
            4: "Albañil",
            5: "Carpintero",
            6: "Pintor",
            7: "Herrero",
            8: "Techista / Impermeabilizador",
            9: "Cerrajero",
            10: "Instalador de aires acondicionados",
            11: "Instalador de alarmas/cámaras de seguridad",
            12: "Personal de limpieza",
            13: "Limpieza de tanques de agua",
            14: "Limpieza de vidrios en altura",
            15: "Lavado de alfombras / cortinas",
            16: "Fumigador",
            17: "Jardinero",
            18: "Podador de árboles",
            19: "Mantenimiento de piletas",
            20: "Paisajista",
            21: "Técnico de electrodomésticos",
            22: "Técnico de celulares",
            23: "Técnico de computadoras / laptops",
            24: "Técnico de televisores / equipos electrónicos",
            25: "Técnico de impresoras",
            26: "Instalador de redes / WiFi",
            27: "Otro"
            }
                 
            especializaciones_firestore = {
                1: "Fontanero_Plomero",
                2: "Electricista",
                3: "Gasista_matriculado",
                4: "Albanil",
                5: "Carpintero",
                6: "Pintor",
                7: "Herrero",
                8: "Techista_Impermeabilizador",
                9: "Cerrajero",
                10: "Instalador_de_aires_acondicionados",
                11: "Instalador_de_alarmas_camáras_de_seguridad",
                12: "Personal_de_limpieza",
                13: "Limpieza_de_tanques_de_agua",
                14: "Limpieza_de_vidrios_en_altura",
                15: "LavadoDeAlfombras_cortinas",
                16: "Fumigador",
                17: "Jardinero",
                18: "Podador_de_árboles",
                19: "Mantenimiento_de_piletas",
                20: "Paisajista",
                21: "Técnico_de_electrodomésticos",
                22: "Técnico_celulares",
                23: "TécnicoDeComputadoras_laptops",
                24: "TécnicoDeTelevisores_equiposelectrónicos",
                25: "Técnico_de_impresoras",
                26: "InstaladorDeRedes_WiFi",
                27: "Otro"
}
            if QHacer == "2":
                print("\n🔧 Reparaciones y mantenimiento del hogar")
                for i in range(1, 12):
                    print(f"{i}. {especializaciones_legibles[i]}")
    
                print("\n🧼 Limpieza y mantenimiento")
                for i in range(12, 17):
                   print(f"{i}. {especializaciones_legibles[i]}")
    
                print("\n🌳 Jardinería y exteriores")
                for i in range(17, 21):
                    print(f"{i}. {especializaciones_legibles[i]}")

                print("\n🛠️ Servicios técnicos")
                for i in range(21, 27):
                    print(f"{i}. {especializaciones_legibles[i]}")

                print("\n27. Otro")

                try:
                    Laburo = int(input("\n¿Qué tipo de laburo necesitás hecho (ingresá el número)? "))
                    LaburoPosta_legible = especializaciones_legibles[Laburo]
                    LaburoPosta_firestore = especializaciones_firestore[Laburo]

                    campo_especializacion = LaburoPosta_firestore
                    
                    trabajadores_ref = db.collection("trabajadores").where(campo_especializacion, "==", True)
                    resultados = trabajadores_ref.stream()

                    lista_mails = []

                    for doc in resultados:
                        data = doc.to_dict()
                        if "mail" in data:
                            if data.get("AyudarAOtros") == True:
                                lista_mails.append(data["mail"])

                    if lista_mails:
                        print("\n📧 Trabajadores disponibles:\n")
                        for i, mail in enumerate(lista_mails, start=1):
                            print(f"{i}. {mail}")
                    else:
                        print("No se encontraron trabajadores con esa especialización.")

                except Exception as e:
                    print("Ocurrió un error:", e)

                Tmail = input("A cual te gustaria contratar (ingresar el mail del trabajador)?:")
                
                trabajador_docs = list(db.collection("trabajadores").where("mail", "==", Tmail).stream())

                while not trabajador_docs:
                    print("❌ El mail no existe. Ingresá otro mail:")
                    Tmail = input("Mail: ")
                    trabajador_docs = list(db.collection("trabajadores").where("mail", "==", Tmail).stream())

                print("✅ Contrataste a " + Tmail + " para que te haga un trabajo de " + LaburoPosta_legible)

                Costo = None  
                argentina = pytz.timezone("America/Argentina/Buenos_Aires")
                ahora = datetime.now(argentina)
                Finalizado = False

                try:
                    db.collection("historialTC").document(Tmail + " - " + Cmail).set({
                        "Tmail": Tmail,
                        "Cmail": Cmail,
                        "Costo": Costo,
                        "Trabajo": LaburoPosta_legible,
                        "HorarioContratacion": ahora,
                        "Finalizado": Finalizado
                    })
                    print("📝 Contratación registrada en el historial.")
                except Exception as e:
                    print("❌ Error al guardar en Firestore:", e)
                


        else:
            print("❌ Datos incorrectos. Por favor, intentá nuevamente.")

    elif profesion == "3":
        mail = input("Ingresá tu mail: ")
        contraseña = input("Ingresá tu contraseña: ")

        desempleados_ref = db.collection("desempleados")
        query = (
            desempleados_ref
            .where("mail", "==", mail)
            .where("contra", "==", contraseña)
            .limit(1)
            .stream()
        )
        
        usuario = None
        for doc in query:
            usuario = doc.to_dict()
            break  

        if usuario:
            nombre = usuario.get("nombre", "usuario")  
            print("✅ Inicio de sesión exitoso. ¡Bienvenido,", nombre + "!")
        
            DMail = mail

            print("¿Q queres hacer ahora?")
            print("1. Solicitar mentoria a un trabajador")

            QHacer = input("Elegí una opción (1 o 2): ")

            argentina = pytz.timezone("America/Argentina/Buenos_Aires")
            ahora = datetime.now(argentina)
            
            especializaciones_legibles = {
            1: "Fontanero / Plomero",
            2: "Electricista",
            3: "Gasista matriculado",
            4: "Albañil",
            5: "Carpintero",
            6: "Pintor",
            7: "Herrero",
            8: "Techista / Impermeabilizador",
            9: "Cerrajero",
            10: "Instalador de aires acondicionados",
            11: "Instalador de alarmas/cámaras de seguridad",
            12: "Personal de limpieza",
            13: "Limpieza de tanques de agua",
            14: "Limpieza de vidrios en altura",
            15: "Lavado de alfombras / cortinas",
            16: "Fumigador",
            17: "Jardinero",
            18: "Podador de árboles",
            19: "Mantenimiento de piletas",
            20: "Paisajista",
            21: "Técnico de electrodomésticos",
            22: "Técnico de celulares",
            23: "Técnico de computadoras / laptops",
            24: "Técnico de televisores / equipos electrónicos",
            25: "Técnico de impresoras",
            26: "Instalador de redes / WiFi",
            27: "Otro"
            }
                 
            especializaciones_firestore = {
                1: "Fontanero_Plomero",
                2: "Electricista",
                3: "Gasista_matriculado",
                4: "Albanil",
                5: "Carpintero",
                6: "Pintor",
                7: "Herrero",
                8: "Techista_Impermeabilizador",
                9: "Cerrajero",
                10: "Instalador_de_aires_acondicionados",
                11: "Instalador_de_alarmas_camáras_de_seguridad",
                12: "Personal_de_limpieza",
                13: "Limpieza_de_tanques_de_agua",
                14: "Limpieza_de_vidrios_en_altura",
                15: "LavadoDeAlfombras_cortinas",
                16: "Fumigador",
                17: "Jardinero",
                18: "Podador_de_árboles",
                19: "Mantenimiento_de_piletas",
                20: "Paisajista",
                21: "Técnico_de_electrodomésticos",
                22: "Técnico_celulares",
                23: "TécnicoDeComputadoras_laptops",
                24: "TécnicoDeTelevisores_equiposelectrónicos",
                25: "Técnico_de_impresoras",
                26: "InstaladorDeRedes_WiFi",
                27: "Otro"
            }
            
            if QHacer == "1":
                print("\n🔧 Reparaciones y mantenimiento del hogar")
                for i in range(1, 12):
                    print(f"{i}. {especializaciones_legibles[i]}")
    
                print("\n🧼 Limpieza y mantenimiento")
                for i in range(12, 17):
                   print(f"{i}. {especializaciones_legibles[i]}")
    
                print("\n🌳 Jardinería y exteriores")
                for i in range(17, 21):
                    print(f"{i}. {especializaciones_legibles[i]}")

                print("\n🛠️ Servicios técnicos")
                for i in range(21, 27):
                    print(f"{i}. {especializaciones_legibles[i]}")

                print("\n27. Otro")

                

                try:
                    Laburo = int(input("\n¿Qué tipo de laburo queres tener (ingresá el número)? "))
                    LaburoPosta_legible = especializaciones_legibles[Laburo]
                    LaburoPosta_firestore = especializaciones_firestore[Laburo]

                    campo_especializacion = LaburoPosta_firestore
                    
                    trabajadores_ref = db.collection("trabajadores").where(campo_especializacion, "==", True)
                    resultados = trabajadores_ref.stream()

                    lista_mails = []

                    for doc in resultados:
                        data = doc.to_dict()
                        if "mail" in data:
                            lista_mails.append(data["mail"])

                    if lista_mails:
                        print("\n📧 Trabajadores disponibles:\n")
                        for i, mail in enumerate(lista_mails, start=1):
                            print(f"{i}. {mail}")
                    else:
                        print("No se encontraron trabajadores con esa especialización dispuestos a enseñar.")

                except Exception as e:
                    print("Ocurrió un error:", e)

                Tmail = input("A cual te gustaria contratar (ingresar el mail del trabajador)?:")
                
                trabajador_docs = list(db.collection("trabajadores").where("mail", "==", Tmail).stream())

                while not trabajador_docs:
                    print("❌ El mail no existe. Ingresá otro mail:")
                    Tmail = input("Mail: ")
                    trabajador_docs = list(db.collection("trabajadores").where("mail", "==", Tmail).stream())

                print("✅ Contrataste a " + Tmail + " para que te enseñe a como ser un " + LaburoPosta_legible)


                Costo = None

                try:
                    db.collection("historialTD").document(Tmail + " - " + DMail).set({
                        "Tmail": Tmail,
                        "Dmail": DMail,
                        "Costo": Costo,
                        "Trabajo": LaburoPosta_legible,
                        "HorarioContratacion": ahora,
                    })
                    print("📝 Contratación registrada en el historial.")
                except Exception as e:
                    print("❌ Error al guardar en Firestore:", e)