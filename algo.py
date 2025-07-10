especializaciones = {
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
    11: "Instalador de alarmas / cámaras de seguridad",
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

def mostrar_especializaciones():
    print("\n🔧 Reparaciones y mantenimiento del hogar")
    for i in range(1, 12):
        print(f"{i}. {especializaciones[i]}")
    
    print("\n🧼 Limpieza y mantenimiento")
    for i in range(12, 17):
        print(f"{i}. {especializaciones[i]}")
    
    print("\n🌳 Jardinería y exteriores")
    for i in range(17, 21):
        print(f"{i}. {especializaciones[i]}")
    
    print("\n🛠️ Servicios técnicos")
    for i in range(21, 27):
        print(f"{i}. {especializaciones[i]}")
    
    print("\n27. Otro")

def main():
    mostrar_especializaciones()
    
    entrada = input("\nElegí tu especialización/es (en caso de ser más de una, separalas con coma): ")
    seleccion = entrada.split(",")
    
    especializaciones_asignadas = []
    otros_trabajos = []

    for item in seleccion:
        try:
            numero = int(item.strip())
            if numero == 27:
                otros = input("📝 Ingresá el/los otro/s trabajo/s (separados por coma en caso de ser más de uno): ")
                otros_trabajos += [x.strip() for x in otros.split(",") if x.strip()]
            elif numero in especializaciones:
                especializaciones_asignadas.append(especializaciones[numero])
            else:
                print(f"❗ Opción inválida: {numero}")
        except ValueError:
            print(f"❗ Entrada no válida: {item}")

    resultado = especializaciones_asignadas + otros_trabajos

    if resultado:
        print("\n✅ Elegiste:")
        for esp in resultado:
            print("•", esp)
    else:
        print("\n⚠️ No asignaste ninguna especialización.")


