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

print(f"Largo base64 original: {len(foto_raw)} chars")

# Limpiar
foto_limpia = foto_raw.replace("\n", "").replace("\r", "").replace(" ", "")
print(f"Largo base64 limpio: {len(foto_limpia)} chars")
print(f"Largo % 4 = {len(foto_limpia) % 4} (debe ser 0 para base64 perfecto)")

# Intentar decodificar con validate=False para aceptar datos truncados
try:
    foto_bytes = base64.b64decode(foto_limpia, validate=False)
    print(f"Decodificado con validate=False: {len(foto_bytes)} bytes")
    print(f"Ultimo 4 bytes: {foto_bytes[-4:].hex()}")
    print(f"Termina FFD9: {foto_bytes[-2:].hex() == 'ffd9'}")
except Exception as e:
    print(f"Error: {e}")

# Probar con urlsafe_b64decode
try:
    foto_bytes2 = base64.urlsafe_b64decode(foto_limpia + "==")
    print(f"urlsafe decode: {len(foto_bytes2)} bytes, fin: {foto_bytes2[-2:].hex()}")
except Exception as e:
    print(f"urlsafe error: {e}")

# Ver los ultimos 100 chars del base64 para detectar si esta cortado
print(f"\nUltimos 100 chars del base64:\n{foto_raw[-100:]}")
