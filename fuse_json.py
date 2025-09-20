import json
import pandas as pd
from unidecode import unidecode

# Función para normalizar nombres
def normalizar(texto):
    return unidecode(texto.strip().lower().replace("\xa0", " "))

# Cargar JSONs
with open("materias.json", "r", encoding="utf-8") as f:
    materias = json.load(f)

with open("materias_info.json", "r", encoding="utf-8") as f:
    materias_info = json.load(f)

# Crear diccionario de info detallada con nombres normalizados
info_dict = {normalizar(m["nombre"]): m for m in materias_info}

fusionadas = []
for m in materias:
    nombre_norm = normalizar(m["Asignatura"])
    if nombre_norm in info_dict:
        detalle = info_dict[nombre_norm]
        fusionadas.append({
            "Cod_Materia": m["Cod_Materia"],
            "Asignatura": m["Asignatura"],  # guardo el original, con acento
            "Cuatrimestre": m["Cuatrimestre"],
            "BI": m["BI"],
            "CHS": m["CHS"],
            "CHT": m["CHT"],
            "Objetivos": detalle.get("objetivos", ""),
            "Biblio_Basica": detalle.get("biblio_basica", ""),
            "Biblio_Complementaria": detalle.get("biblio_complementaria", ""),
            "URL": detalle.get("url", "")
        })
    else:
        # Si no hay detalle, guardo solo lo básico
        fusionadas.append(m)

# Guardar resultados
with open("materias_fusionadas.json", "w", encoding="utf-8") as f:
    json.dump(fusionadas, f, ensure_ascii=False, indent=2)

pd.DataFrame(fusionadas).to_csv("materias_fusionadas.csv", index=False, encoding="utf-8")

print("Fusion terminado. Se crearon materias_fusionadas.json y materias_fusionadas.csv")

