"""Inserta datos.json en la plantilla y publica el reporte en docs/ejemplo-powerbi/ (GitHub Pages)."""
import sys
from pathlib import Path

AQUI = Path(__file__).parent
plantilla = (AQUI / "plantilla.html").read_text(encoding="utf-8")
datos = (AQUI / "datos.json").read_text(encoding="utf-8")
cuerpo = plantilla.replace("/*__DATOS__*/null", datos)

destino = AQUI.parent.parent / "docs" / "ejemplo-powerbi" / "index.html"
destino.parent.mkdir(parents=True, exist_ok=True)
destino.write_text('<!doctype html>\n<html lang="es">\n<head>\n<meta charset="utf-8">\n'
                   '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
                   + cuerpo + "\n</html>\n", encoding="utf-8")
print("Página web:", destino)

# Opcional: versión sin encabezado HTML (para publicarla como Artifact)
if len(sys.argv) > 1:
    Path(sys.argv[1]).write_text(cuerpo, encoding="utf-8")
    print("Versión fragmento:", sys.argv[1])
