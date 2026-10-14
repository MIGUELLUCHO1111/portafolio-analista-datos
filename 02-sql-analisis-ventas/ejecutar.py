"""Ejecuta cada consulta de consultas.sql sobre ../datos/ventas.db y escribe resultados.md."""
import sqlite3
from pathlib import Path

AQUI = Path(__file__).parent
con = sqlite3.connect(AQUI.parent / "datos" / "ventas.db")

bloques = AQUI.joinpath("consultas.sql").read_text(encoding="utf-8").split("-- @pregunta ")[1:]
salida = ["# Resultados de las consultas\n", "Generado con `python ejecutar.py` sobre `datos/ventas.db`.\n"]

for bloque in bloques:
    pregunta, consulta = bloque.split("\n", 1)
    cur = con.execute(consulta)
    columnas = [c[0] for c in cur.description]
    filas = cur.fetchall()
    salida.append(f"\n## {pregunta.strip()}\n")
    salida.append("| " + " | ".join(columnas) + " |")
    salida.append("|" + "---|" * len(columnas))
    for fila in filas:
        salida.append("| " + " | ".join(f"{v:,.2f}" if isinstance(v, float) else str(v) for v in fila) + " |")

AQUI.joinpath("resultados.md").write_text("\n".join(salida) + "\n", encoding="utf-8")
print(f"{len(bloques)} consultas ejecutadas -> resultados.md")
