import requests
import base64
import os

TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbXByZXNhIjoiQXltYXIiLCJpYXQiOjE3ODE4Mjg3NTksImV4cCI6MTgxMzM4NjM1OX0.LADrt1sOt9fwmjcBZngGHm1O91b1C_oXOJt7hLWMJus"

r = requests.get(
    "https://apicedula.socket-studio.com/consulta-cedula/consulta/0944238641",
    headers={"Authorization": f"Bearer {TOKEN}", "Accept": "application/json"},
    timeout=15
)
data = r.json()
foto_raw = data.get("foto", "")

print(f"Largo del base64: {len(foto_raw)} chars")
print(f"Contiene coma (dataURI): {',' in foto_raw}")
print(f"Primeros 80 chars: {foto_raw[:80]}")
print(f"Ultimos 20 chars: {foto_raw[-20:]}")

# Decodificar
if "," in foto_raw:
    foto_raw = foto_raw.split(",")[1]

foto_bytes = base64.b64decode(foto_raw + "==")
print(f"Bytes totales: {len(foto_bytes)}")
print(f"Primeros 12 bytes (hex): {foto_bytes[:12].hex()}")
print(f"Ultimos 4 bytes (hex): {foto_bytes[-4:].hex()}")

# JPEG valido: empieza FFD8, termina FFD9
empieza_bien = foto_bytes[:2].hex() == "ffd8"
termina_bien = foto_bytes[-2:].hex() == "ffd9"
print(f"Empieza FFD8 (inicio JPEG valido): {empieza_bien}")
print(f"Termina FFD9 (fin JPEG valido): {termina_bien}")

# Guardar para verificar
with open("foto_debug_0944238641.jpg", "wb") as f:
    f.write(foto_bytes)
print(f"Guardado como foto_debug_0944238641.jpg ({len(foto_bytes)} bytes)")

# Verificar el archivo existente (el viejo)
if os.path.exists("foto_0944238641.jpg"):
    old_size = os.path.getsize("foto_0944238641.jpg")
    print(f"Archivo antiguo foto_0944238641.jpg: {old_size} bytes")
    with open("foto_0944238641.jpg", "rb") as f:
        old_bytes = f.read()
    print(f"Primeros bytes del archivo antiguo: {old_bytes[:12].hex()}")
    print(f"Ultimos bytes del archivo antiguo: {old_bytes[-4:].hex()}")
    print(f"Son identicos: {old_bytes == foto_bytes}")
