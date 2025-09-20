import json
import pandas as pd
from unidecode import unidecode

# Función para normalizar nombres
def normalizar(texto):
    return unidecode(texto.strip().lower().replace("\xa0", " "))

# ===============================
# CARGAR JSONS
# ===============================

# Materias obligatorias
with open("materias.json", "r", encoding="utf-8") as f:
    materias = [m for m in json.load(f) if m.get("Asignatura")]

# Materias optativas
with open("materias_opt.json", "r", encoding="utf-8") as f:
    materias_opt = json.load(f)

# Si materias_opt es un dict, extraer la lista bajo la clave correcta
if isinstance(materias_opt, dict):
    materias_opt = materias_opt.get("optativas", [])

# Filtrar filas vacías
materias_opt = [m for m in materias_opt if m.get("Asignatura")]

# Materias info detallada
with open("materias_info.json", "r", encoding="utf-8") as f:
    materias_info = json.load(f)

# Crear diccionario de info detallada con nombres normalizados
info_dict = {normalizar(m["nombre"]): m for m in materias_info}

# ===============================
# FUSIONAR
# ===============================
fusionadas = []

# Materias obligatorias
for m in materias:
    nombre_norm = normalizar(m["Asignatura"])
    detalle = info_dict.get(nombre_norm, {})
    fusionadas.append({
        "Cod_Materia": m.get("Cod_Materia", ""),
        "Asignatura": m.get("Asignatura", ""),
        "Cuatrimestre": m.get("Cuatrimestre", ""),
        "BI": m.get("BI", ""),
        "CHS": m.get("CHS", ""),
        "CHT": m.get("CHT", ""),
        "Tipo": "obligatoria",
        "Objetivos": detalle.get("objetivos", ""),
        "Biblio_Basica": detalle.get("biblio_basica", ""),
        "Biblio_Complementaria": detalle.get("biblio_complementaria", ""),
        "URL": detalle.get("url", "")
    })

# Materias optativas
for m in materias_opt:
    nombre_norm = normalizar(m["Asignatura"])
    detalle = info_dict.get(nombre_norm, {})
    fusionadas.append({
        "Cod_Materia": m.get("Cod_Materia", ""),
        "Asignatura": m.get("Asignatura", ""),
        "Cuatrimestre": m.get("Cuatrimestre", ""),
        "BI": m.get("BI", ""),
        "CHS": m.get("CHS", ""),
        "CHT": m.get("CHT", ""),
        "Tipo": "optativa",
        "Objetivos": detalle.get("objetivos", ""),
        "Biblio_Basica": detalle.get("biblio_basica", ""),
        "Biblio_Complementaria": detalle.get("biblio_complementaria", ""),
        "URL": detalle.get("url", "")
    })

# ===============================
# GUARDAR RESULTADOS
# ===============================
with open("materias_fusionadas.json", "w", encoding="utf-8") as f:
    json.dump(fusionadas, f, ensure_ascii=False, indent=2)

# También generar CSV
pd.DataFrame(fusionadas).to_csv("materias_fusionadas.csv", index=False, encoding="utf-8")

print(f"Fusion terminado. Se crearon {len(fusionadas)} materias en materias_fusionadas.json y materias_fusionadas.csv ✅")