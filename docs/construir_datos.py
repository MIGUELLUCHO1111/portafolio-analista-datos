"""Genera docs/datos.js (datos del dashboard) a partir de ../datos/*.csv. Uso: python construir_datos.py"""
import csv
import json
from pathlib import Path

AQUI = Path(__file__).parent
DATOS = AQUI.parent / "datos"
leer = lambda n: list(csv.DictReader(open(DATOS / f"{n}.csv", encoding="utf-8")))
P = {p["id"]: p for p in leer("productos")}
V = {v["id"]: v for v in leer("vendedores")}
MESES = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]

filas = []
for s in leer("ventas"):
    p, v = P[s["producto_id"]], V[s["vendedor_id"]]
    cant, precio = int(s["cantidad"]), float(s["precio_unit"])
    filas.append({
        "fecha": s["fecha"], "mes": MESES[int(s["fecha"][5:7]) - 1], "mesNum": int(s["fecha"][5:7]),
        "region": s["region"], "canal": s["canal"], "vendedor": v["nombre"], "producto": p["nombre"],
        "categoria": p["categoria"], "cantidad": cant, "ingreso": cant * precio,
        "margen": cant * (precio - float(p["costo"])),
    })
metas = {v["nombre"]: float(v["meta"]) for v in V.values()}
AQUI.joinpath("datos.js").write_text(
    "// Generado por construir_datos.py\nconst VENTAS = " + json.dumps(filas, ensure_ascii=False) +
    ";\nconst METAS = " + json.dumps(metas, ensure_ascii=False) + ";\n", encoding="utf-8")
print(f"datos.js: {len(filas)} ventas")
