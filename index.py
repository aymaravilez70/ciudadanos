# -*- coding: utf-8 -*-
import sys
import io
import requests
import base64
import os

# Forzar UTF-8 en la salida de la consola de Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

TOKEN_API = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbXByZXNhIjoiQXltYXIiLCJpYXQiOjE3ODE4Mjg3NTksImV4cCI6MTgxMzM4NjM1OX0.LADrt1sOt9fwmjcBZngGHm1O91b1C_oXOJt7hLWMJus"

CAMPOS_MOSTRAR = {
    "identificacion":    "Cédula",
    "nombres":           "Nombres Completos",
    "nacionalidad":      "Nacionalidad",
    "codigoDactilar":    "Código Dactilar",
    "lugarNacimiento":   "Lugar de Nacimiento",
    "fechaNacimiento":   "Fecha de Nacimiento",
    "estadoCivil":       "Estado Civil",
    "genero":            "Género",
    "sexo":              "Sexo",
    "nombrePadre":       "Nombre del Padre",
    "nombreMadre":       "Nombre de la Madre",
    "instruccion":       "Instrucción",
    "profesion":         "Profesión",
    "calle":             "Dirección/Calle",
    "fechaCedulacion":   "Fecha de Cedulación",
    "condicionCedulado": "Condición de Cedulado",
}


def consultar_por_cedula(cedula):
    """Consulta el perfil ciudadano por número de cédula usando la API."""
    url = f"https://apicedula.socket-studio.com/consulta-cedula/consulta/{cedula}"
    headers = {
        "Authorization": f"Bearer {TOKEN_API}",
        "Accept": "application/json"
    }

    print(f"\n[~] Consultando cédula: {cedula} ...")

    try:
        response = requests.get(url, headers=headers, timeout=15)

        if response.status_code == 200:
            data = response.json()

            # Verificar que realmente se encontraron datos
            if not data.get("nombres"):
                print("[-] No se encontraron datos para esa cédula.")
                return

            print("\n" + "=" * 56)
            print("       PERFIL CIUDADANO — REGISTRO CIVIL ECUADOR")
            print("=" * 56)

            for key, label in CAMPOS_MOSTRAR.items():
                valor = data.get(key, "")
                if valor and str(valor).strip():
                    print(f"  [+] {label:<25} {valor}")
                else:
                    print(f"  [-] {label:<25} No disponible")

            # --- Manejo de la foto ---
            foto_base64 = data.get("foto")
            os.makedirs("img", exist_ok=True)  # crea carpeta img si no existe
            foto_filename = os.path.join("img", f"foto_{cedula}.jpg")

            if foto_base64:
                try:
                    # Limpiar prefijo dataURI si está presente
                    if "," in foto_base64:
                        foto_base64 = foto_base64.split(",")[1]

                    # La API devuelve \n como texto literal (barra+n), no como salto de linea real
                    # Hay que eliminar primero esa secuencia literal, luego whitespace real
                    foto_base64 = (
                        foto_base64
                        .replace("\\n", "")   # elimina literal \n (barra + n como texto)
                        .replace("\n", "")    # elimina saltos de linea reales (por si acaso)
                        .replace("\r", "")    # elimina carriage return
                        .replace(" ", "")     # elimina espacios
                    )

                    foto_bytes = base64.b64decode(foto_base64)
                    with open(foto_filename, "wb") as f:
                        f.write(foto_bytes)

                    foto_path = os.path.abspath(foto_filename)
                    print(f"\n  [+] {'Foto Facial':<25} Guardada → {foto_path}")

                    # Intentar abrir la foto automáticamente
                    try:
                        os.startfile(foto_path)
                        print(f"  [+] Abriendo foto en el visor de imágenes...")
                    except Exception:
                        pass  # En entornos sin GUI se ignora

                except Exception as ex:
                    print(f"\n  [-] {'Foto Facial':<25} Error al decodificar: {ex}")
            else:
                print(f"\n  [-] {'Foto Facial':<25} No disponible en la respuesta")

            print("=" * 56 + "\n")

        elif response.status_code == 401:
            print("[-] Error 401: Token de API no autorizado o inválido.")
        elif response.status_code == 404:
            print("[-] Error 404: Cédula no encontrada.")
        elif response.status_code == 429:
            print("[-] Error 429: Límite de consultas alcanzado. Intenta más tarde.")
        else:
            print(f"[-] Error del servidor. Código: {response.status_code}")
            print(response.text[:300])

    except requests.exceptions.ConnectionError:
        print("[-] Sin conexión. Verifica tu internet.")
    except requests.exceptions.Timeout:
        print("[-] El servidor tardó demasiado en responder.")
    except Exception as e:
        print(f"[-] Error inesperado: {e}")


def menu_principal():
    """Menú interactivo principal."""
    print("\n" + "=" * 56)
    print("    CONSULTA REGISTRO CIVIL — ECUADOR (API Cédula)")
    print("=" * 56)
    print("  [1] Consultar por número de cédula")
    print("  [0] Salir")
    print("=" * 56)

    while True:
        opcion = input("\nElige una opción: ").strip()

        if opcion == "1":
            cedula = input("Ingresa el número de cédula: ").strip()
            if cedula.isdigit() and len(cedula) == 10:
                consultar_por_cedula(cedula)
            else:
                print("[-] Cédula inválida. Debe tener exactamente 10 dígitos numéricos.")

        elif opcion == "0":
            print("\n[~] Saliendo. ¡Hasta luego!\n")
            break

        else:
            print("[-] Opción no válida. Elige 1 o 0.")

        print("\n" + "-" * 56)
        print("  [1] Nueva consulta por cédula")
        print("  [0] Salir")


if __name__ == "__main__":
    menu_principal()