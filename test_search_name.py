import requests
from bs4 import BeautifulSoup

def test_name():
    url = "https://servicios.educacion.gob.ec/titulacion25-web/faces/paginas/consulta-titulos-refrendados.xhtml"
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    }
    session = requests.Session()
    r = session.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    
    view_state = soup.find("input", {"name": "javax.faces.ViewState"})["value"]
    img_src = soup.find("img", {"id": "formBusqueda:capimg"})["src"]
    
    r_cap = session.get("https://servicios.educacion.gob.ec" + img_src, headers=headers)
    with open("cap_name.jpg", "wb") as f:
        f.write(r_cap.content)
    
    print("[+] Downloaded cap_name.jpg")
    cap_val = input("Enter captcha: ")
    
    payload = {
        "formBusqueda": "formBusqueda",
        "formBusqueda:selecItem": "2", # 2 is for names
        "formBusqueda:cedula": "TAGLE VICTOR",
        "formBusqueda:captcha": cap_val,
        "formBusqueda:clBuscar": "Consultar",
        "javax.faces.ViewState": view_state
    }
    
    r_post = session.post(url, data=payload, headers=headers)
    soup_res = BeautifulSoup(r_post.text, 'html.parser')
    open("res_name.html", "w", encoding="utf-8").write(r_post.text)
    
    # Try finding tables or list of names
    print("--- Searching for tables ---")
    for t in soup_res.find_all("table"):
        if t.get("id") and "tabla" in t.get("id"):
            print(f"Table ID: {t.get('id')}")
            for tr in t.find_all("tr"):
                print([td.text.strip() for td in tr.find_all("td") if td.text.strip()])

if __name__ == "__main__":
    test_name()
