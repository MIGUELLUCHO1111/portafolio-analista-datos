"""Simula la llegada de archivos mensuales "sucios" (como en la vida real) en la carpeta entrada/.
Divide ../datos/ventas.csv por mes y agrega problemas típicos: espacios, mayúsculas y un duplicado.
Uso: python preparar_entrada.py"""
import csv
from pathlib import Path

AQUI = Path(__file__).parent
entrada = AQUI / "entrada"
entrada.mkdir(exist_ok=True)

filas = list(csv.DictReader(open(AQUI.parent / "datos" / "ventas.csv", encoding="utf-8")))
por_mes = {}
for i, f in enumerate(filas):
    if i % 7 == 0:
        f["region"] = "  " + f["region"].lower()          # espacios y minúsculas
    if i % 11 == 0:
        f["region"] = f["region"].upper()
    por_mes.setdefault(f["fecha"][:7], []).append(f)
por_mes["2026-03"].append(dict(por_mes["2026-03"][0]))   # un duplicado

for mes, datos in por_mes.items():
    with open(entrada / f"ventas_{mes}.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=datos[0].keys())
        w.writeheader()
        w.writerows(datos)
print(f"{len(por_mes)} archivos mensuales creados en entrada/")
