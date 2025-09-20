import requests
from bs4 import BeautifulSoup
import json

URL = "https://www.fica.unsl.edu.ar/index.php/carreras/plan-20-22-ii/"

resp = requests.get(URL)
soup = BeautifulSoup(resp.text, "html.parser")

materias = []

for tabla in soup.find_all("table"):
    for row in tabla.find_all("tr")[1:]:  
        cols = row.find_all("td")
        if len(cols) >= 6:  
            Cod_Materia = cols[0].get_text(strip=True)
            Asignatura = cols[1].get_text(strip=True)
            Cuatrimestre = cols[2].get_text(strip=True)
            BI = cols[3].get_text(strip=True) 
            CHS = cols[4].get_text(strip=True)
            CHT = cols[5].get_text(strip=True) 

            materias.append({
                "Cod_Materia": Cod_Materia,
                "Asignatura": Asignatura,
                "Cuatrimestre": Cuatrimestre,
                "BI": BI,
                "CHS": CHS,
                "CHT": CHT
            })

print(f"Se encontraron {len(materias)} materias.")
if materias:
    print("Ejemplo primera materia:", materias[0])
else:
    print("No se encontraron materias. Revisa el selector o la página.")

# Guardar en JSON
with open("materias.json", "w", encoding="utf-8") as f:
    json.dump(materias, f, ensure_ascii=False, indent=4)

print("Archivo materias.json creado.")

