import requests
from bs4 import BeautifulSoup
import json

def limpiar_texto(texto):
    if not texto:
        return ""
    return " ".join(texto.split())

def extraer_tabla_por_titulo(soup, titulo):
    tablas = soup.find_all("table")
    for tabla in tablas:
        if tabla.find("td") and titulo in tabla.get_text():
            return tabla.get_text(separator=" ", strip=True)
    return ""

def procesar_materia(nombre, links):
    href = None

    # Priorizar 2025
    for a in links:
        if a.get_text(strip=True) == "2025":
            href = a["href"]
            break

    # Si no buscar 2024
    if not href:
        for a in links:
            if a.get_text(strip=True) == "2024":
                href = a["href"]
                break

    materia_data = {
        "nombre": nombre,
        "objetivos": "",
        "biblio_basica": "",
        "biblio_complementaria": "",
        "url": ""
    }

    if href:
        if not href.startswith("http"):
            href = "http://cargaprogramas.unsl.edu.ar/" + href.lstrip("/")
        materia_data["url"] = href

        prog_resp = requests.get(href)
        if prog_resp.status_code == 200:
            prog_soup = BeautifulSoup(prog_resp.text, "html.parser")
            objetivos = extraer_tabla_por_titulo(prog_soup, "V - Objetivos / Resultados de Aprendizaje")
            biblio_basica = extraer_tabla_por_titulo(prog_soup, "IX - Bibliografía Básica")
            biblio_complementaria = extraer_tabla_por_titulo(prog_soup, "X - Bibliografia Complementaria")

            materia_data["objetivos"] = limpiar_texto(objetivos)
            materia_data["biblio_basica"] = limpiar_texto(biblio_basica)
            materia_data["biblio_complementaria"] = limpiar_texto(biblio_complementaria)

    return materia_data





url_plan = "http://planesestudio.unsl.edu.ar/index.php?action=car_g3&fac=14&car=14008&plan=20/22&version=9&version_id=1276"
resp = requests.get(url_plan)
soup = BeautifulSoup(resp.text, "html.parser")

tablas = soup.find_all("table", class_="tablamat")

print("Tablas encontradas:", len(tablas))  

materias_obligatorias = []
materias_optativas = []

# materias obligatorias 
if len(tablas) > 0:
    for fila in tablas[0].find_all("tr")[1:]:
        cols = fila.find_all("td")
        if len(cols) >= 6:
            nombre = cols[1].get_text(strip=True)
            links = cols[5].find_all("a")
            materias_obligatorias.append(procesar_materia(nombre, links))

# optativas 
for tabla in tablas[1:]:
    for fila in tabla.find_all("tr")[1:]:
        cols = fila.find_all("td")
        if len(cols) >= 6:
            nombre = cols[1].get_text(strip=True)
            links = cols[5].find_all("a")
            materias_optativas.append(procesar_materia(nombre, links))

plan_estudios = {
    "obligatorias": materias_obligatorias,
    "optativas": materias_optativas
}

print(f"Obligatorias: {len(materias_obligatorias)}")
print(f"Optativas: {len(materias_optativas)}")

# Guardar en JSON
with open("materias_info2.json", "w", encoding="utf-8") as f:
    json.dump(plan_estudios, f, ensure_ascii=False, indent=4)

print("Archivo materias.json creado ✅")
