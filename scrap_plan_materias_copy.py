import requests
from bs4 import BeautifulSoup
import json

def extraer_tabla_por_titulo(soup, titulo):
    th = soup.find("th", string=lambda s: s and titulo.lower() in s.lower())
    if th:
        tr = th.find_parent("tr")
        siguiente_tr = tr.find_next_sibling("tr")
        if siguiente_tr:
            contenido = siguiente_tr.get_text(separator="\n", strip=True)
            return contenido
    return ""

def limpiar_texto(texto):
    return texto.replace("\n", " | ").replace("\r", " ").replace("\t", " ").strip()

url = "http://planesestudio.unsl.edu.ar/index.php?action=car_g3&fac=14&car=14008&plan=20/22&version=9&version_id=1276"
resp = requests.get(url)
soup = BeautifulSoup(resp.text, "html.parser")

tablas = soup.find_all("table", class_="tablamat")

materias_info = []

for tabla in tablas:
    filas = tabla.find_all("tr")[1:]
    if len(filas) == 0:
        continue
    for fila in filas:
        cols = fila.find_all("td")
        if len(cols) >= 5:
            nombre = cols[1].get_text(strip=True)
            for a in cols[4].find_all("a"):
                if a.get_text(strip=True) == "2025":
                    href = a["href"]
                    if not href.startswith("http"):
                        href = "http://cargaprogramas.unsl.edu.ar/" + href.lstrip("/")
                    prog_resp = requests.get(href)
                    if prog_resp.status_code == 200:
                        prog_soup = BeautifulSoup(prog_resp.text, "html.parser")
                        objetivos = extraer_tabla_por_titulo(prog_soup, "V - Objetivos / Resultados de Aprendizaje")
                        biblio_basica = extraer_tabla_por_titulo(prog_soup, "IX - Bibliografía Básica")
                        biblio_complementaria = extraer_tabla_por_titulo(prog_soup, "X - Bibliografia Complementaria")
                        materias_info.append({
                            "nombre": nombre,
                            "objetivos": limpiar_texto(objetivos),
                            "biblio_basica": limpiar_texto(biblio_basica),
                            "biblio_complementaria": limpiar_texto(biblio_complementaria),
                            "url": href
                        })
                    else:
                        materias_info.append({
                            "nombre": nombre,
                            "objetivos": "",
                            "biblio_basica": "",
                            "biblio_complementaria": "",
                            "url": href
                        })

# Guardar en JSON
with open("materias_info.json", "w", encoding="utf-8") as f:
    json.dump(materias_info, f, ensure_ascii=False, indent=4)

print(f"Archivo materias_info2.json creado con {len(materias_info)} materias.")

