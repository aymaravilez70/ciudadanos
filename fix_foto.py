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

# El API retorna \n (literal backslash+n, no newline real) como separador de linea
# En Python, esto aparece como '\\n' en repr() — hay que eliminar la barra y la n
# Primero eliminar secuencias literales '\n' (backslash-n como texto)
foto_limpia = foto_raw.replace("\\n", "")  # elimina la secuencia \n literal
# Luego eliminar whitespace real
foto_limpia = foto_limpia.replace("\n", "").replace("\r", "").replace(" ", "")

print(f"Largo limpio: {len(foto_limpia)}")
print(f"Ultimos 10: '{foto_limpia[-10:]}'")
print(f"Termina '2Q==': {foto_limpia.endswith('2Q==')}")

foto_bytes = base64.b64decode(foto_limpia)
inicio_ok = foto_bytes[:2].hex() == "ffd8"
fin_ok = foto_bytes[-2:].hex() == "ffd9"

print(f"Bytes: {len(foto_bytes)}")
print(f"Inicio FFD8: {inicio_ok}")
print(f"Fin    FFD9: {fin_ok}")

if inicio_ok and fin_ok:
    with open("foto_0944238641.jpg", "wb") as f:
        f.write(foto_bytes)
    ruta = os.path.abspath("foto_0944238641.jpg")
    print(f"JPEG VALIDO! Guardado en: {ruta}")
    os.startfile(ruta)
else:
    print(f"AUN CORRUPTO. Fin: {foto_bytes[-4:].hex()}")
