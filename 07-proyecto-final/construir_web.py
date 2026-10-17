"""Genera docs/petroleo_datos.js (datos del dashboard petrolero) a partir de datos/*.csv.
Uso: python construir_web.py   (después de python actualizar_datos.py, si quieres datos nuevos)"""
import json
from pathlib import Path

import pandas as pd

import petro as P

AQUI = Path(__file__).parent
DESTINO = AQUI.parent / "docs" / "petroleo_datos.js"

prod, res, campos, brent = P.cargar_produccion(), P.cargar_reservas(), P.cargar_campos(), P.cargar_brent()
ultimo = prod["fecha"].max()

# Serie nacional mensual
nac = prod.groupby("fecha").agg(petroleo=("petroleo_kbd", "sum"), agua=("agua_kbd", "sum"),
                                gas=("gas_bsm3", "sum")).reset_index()
nac = nac.merge(brent, on="fecha", how="left")
NAC = {
    "ini": nac["fecha"].iloc[0].strftime("%Y-%m"),
    "petroleo": nac["petroleo"].round(1).tolist(),
    "corte": (nac["agua"] / (nac["agua"] + nac["petroleo"])).round(3).tolist(),
    "gas": nac["gas"].round(3).tolist(),
    "brent": [None if pd.isna(x) else round(x, 2) for x in nac["brent"]],
}

# Un registro por campo con producción de petróleo
info = campos.set_index("campo").to_dict("index")
rese = res.set_index("campo").to_dict("index")
CAMPOS = []
for nombre, g in prod.groupby("campo"):
    if g["petroleo_msm3"].sum() <= 0:
        continue
    g = g.set_index("fecha").reindex(pd.date_range(g["fecha"].min(), g["fecha"].max(), freq="MS"))
    i, r = info.get(nombre, {}), rese.get(nombre, {})
    CAMPOS.append({
        "n": nombre.title(),
        "op": i.get("operador") or "—", "est": i.get("estado") or "—", "area": i.get("area") or "—",
        "tipo": i.get("tipo") or "—",
        "desc": None if pd.isna(i.get("anio_descubrimiento", float("nan"))) else int(i["anio_descubrimiento"]),
        "rec": round(r.get("recuperable_mmbbl", 0) or 0, 1), "rem": round(r.get("remanente_mmbbl", 0) or 0, 1),
        "acum": round(g["petroleo_bbl"].sum() / 1e6, 1),
        "ini": g.index[0].strftime("%Y-%m"),
        "o": g["petroleo_kbd"].fillna(0).round(2).tolist(),
        "w": [None if pd.isna(x) else round(x, 3) for x in g["corte_agua"]],
    })
for c in CAMPOS:
    meses_fin = (ultimo.year - int(c["ini"][:4])) * 12 + ultimo.month - int(c["ini"][5:]) + 1
    c["actual"] = round(sum(c["o"][-12:]) / 12, 1) if meses_fin == len(c["o"]) else 0.0
CAMPOS.sort(key=lambda c: (-c["actual"], -c["acum"]))

META = {"actualizado": ultimo.strftime("%Y-%m"), "campos": len(CAMPOS),
        "rem_total": round(res.loc[res["recuperable_mmbbl"] > 0, "remanente_mmbbl"].sum(), 1),
        "brent_12m": round(brent[brent["fecha"] > brent["fecha"].max() - pd.DateOffset(months=12)]["brent"].mean(), 2)}

DESTINO.write_text(
    "// Generado por 07-proyecto-final/construir_web.py · Fuentes: Sodir FactPages (NLOD) y FRED\n"
    f"const META = {json.dumps(META, ensure_ascii=False)};\n"
    f"const NAC = {json.dumps(NAC)};\n"
    f"const CAMPOS = {json.dumps(CAMPOS, ensure_ascii=False)};\n", encoding="utf-8")
print(f"{DESTINO.name}: {len(CAMPOS)} campos, datos hasta {META['actualizado']}, {DESTINO.stat().st_size / 1024:.0f} KB")
