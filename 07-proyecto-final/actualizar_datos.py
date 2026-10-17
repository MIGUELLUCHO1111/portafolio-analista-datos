"""Descarga los datos oficiales más recientes a datos/. Uso: python actualizar_datos.py

Fuentes (datos abiertos, se actualizan cada mes):
- Sodir (Dirección Noruega de Costa Afuera), FactPages: producción mensual, reservas y campos.
  Licencia: Norwegian Licence for Open Government Data (NLOD).
- FRED (Banco de la Reserva Federal de St. Louis): precio mensual del Brent, serie POILBREUSDM.
"""
from datetime import date
from pathlib import Path
from urllib.request import urlopen

AQUI = Path(__file__).parent
DATOS = AQUI / "datos"
SODIR = ("https://factpages.sodir.no/public?/Factpages/external/tableview/{}"
         "&rs:Command=Render&rc:Toolbar=false&rc:Parameters=f&IpAddress=not_used"
         "&CultureCode=en&rs:Format=CSV&Top100=false")
FUENTES = {
    "produccion_mensual.csv": SODIR.format("field_production_monthly"),
    "reservas.csv": SODIR.format("field_reserves"),
    "campos.csv": SODIR.format("field"),
    "brent_mensual.csv": "https://fred.stlouisfed.org/graph/fredgraph.csv?id=POILBREUSDM",
}

DATOS.mkdir(exist_ok=True)
for nombre, url in FUENTES.items():
    contenido = urlopen(url, timeout=120).read().decode("utf-8-sig")
    (DATOS / nombre).write_text(contenido, encoding="utf-8")
    print(f"{nombre}: {len(contenido.splitlines()) - 1} filas")

(DATOS / "FUENTES.md").write_text(
    f"# Fuentes de los datos\n\nDescargados el {date.today():%d/%m/%Y} con `actualizar_datos.py`.\n\n"
    "| Archivo | Fuente | Contenido |\n|---|---|---|\n"
    "| `produccion_mensual.csv` | [Sodir FactPages](https://factpages.sodir.no) · licencia NLOD | Producción mensual neta por campo desde 1971 (petróleo, gas, NGL, condensado y agua) |\n"
    "| `reservas.csv` | Sodir FactPages | Reservas recuperables y remanentes por campo (estimación oficial) |\n"
    "| `campos.csv` | Sodir FactPages | Operador, estado, área y tipo de hidrocarburo de cada campo |\n"
    "| `brent_mensual.csv` | [FRED, serie POILBREUSDM](https://fred.stlouisfed.org/series/POILBREUSDM) | Precio promedio mensual del Brent (USD/bbl) |\n\n"
    "Unidades de Sodir: millones de metros cúbicos estándar (MSm³). 1 Sm³ = 6,2898 barriles.\n",
    encoding="utf-8")
print("Listo: datos/FUENTES.md")
