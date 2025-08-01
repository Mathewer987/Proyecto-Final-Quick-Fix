from datetime import datetime

# Le pedís al usuario la fecha en formato YYYY-MM-DD
fecha_nacimiento = input("Nacimiento (YYYY-MM-DD): ")

# Convertís a tipo date (sin hora ni zona horaria)
RDBirth = datetime.strptime(fecha_nacimiento, "%Y-%m-%d").date()

print("Fecha registrada:", RDBirth)
