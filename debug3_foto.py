import requests
import base64

TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbXByZXNhIjoiQXltYXIiLCJpYXQiOjE3ODE4Mjg3NTksImV4cCI6MTgxMzM4NjM1OX0.LADrt1sOt9fwmjcBZngGHm1O91b1C_oXOJt7hLWMJus"

r = requests.get(
    "https://apicedula.socket-studio.com/consulta-cedula/consulta/0944238641",
    headers={"Authorization": f"Bearer {TOKEN}", "Accept": "application/json"},
    timeout=15
)
data = r.json()
foto_raw = data.get("foto", "")

# Mostrar los ultimos 200 caracteres del base64 tal cual viene
print("=== ULTIMOS 200 CHARS DEL BASE64 (RAW) ===")
print(repr(foto_raw[-200:]))
print()
print("=== ULTIMOS 50 CHARS (VISIBLE) ===")
print(foto_raw[-50:])
print()

# Verificar si termina en == (padding base64 correcto)
foto_limpia = foto_raw.replace("\\\n","").replace("\n","").replace("\r","").replace(" ","")
print(f"Termina en '==': {foto_limpia.endswith('==')}")
print(f"Termina en '=': {foto_limpia.endswith('=')}")
print(f"Ultimo 10 chars limpio: '{foto_limpia[-10:]}'")

# Probar: el base64 de un JPEG valido deberia terminar en /2Q==
# /9j/ es el inicio de JPEG, /2Q== es un final comun
print(f"Esperado fin JPEG (/2Q==): {foto_limpia[-4:]}")
