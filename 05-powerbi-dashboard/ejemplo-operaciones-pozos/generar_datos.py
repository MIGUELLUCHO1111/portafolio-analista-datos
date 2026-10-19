"""Genera los datos simulados del ejemplo de Power BI: operación de 12 pozos en 3 campos (ene-sep 2026).

Crea las tablas del modelo estrella en datos/ (para cargarlas en Power BI Desktop)
y datos.json, que usa la página web del reporte.
"""
import calendar
import csv
import json
import random
from pathlib import Path

random.seed(2026)
AQUI = Path(__file__).parent
(AQUI / "datos").mkdir(exist_ok=True)

MESES = [f"2026-{m:02d}" for m in range(1, 10)]
BRENT = [74.2, 76.8, 79.1, 77.5, 73.9, 71.2, 72.8, 75.6, 78.3]
DESCUENTO = 4.5  # USD/bbl por calidad y transporte

# pozo, campo, tipo, mes de inicio, tasa inicial bbl/d, declinación mensual, corte de agua inicial, aumento mensual de agua
POZOS = [
    ("AUR-01", "Aurora", "Vertical", 1, 610, 0.010, 0.27, 0.004),
    ("AUR-02", "Aurora", "Horizontal", 1, 655, 0.012, 0.24, 0.005),
    ("AUR-03", "Aurora", "Vertical", 1, 430, 0.020, 0.33, 0.006),
    ("AUR-04", "Aurora", "Desviado", 1, 520, 0.011, 0.29, 0.004),
    ("ORI-01", "Orión", "Vertical", 1, 480, 0.032, 0.46, 0.020),
    ("ORI-02", "Orión", "Vertical", 1, 445, 0.030, 0.49, 0.018),
    ("ORI-03", "Orión", "Desviado", 1, 395, 0.035, 0.52, 0.022),
    ("ORI-04", "Orión", "Vertical", 1, 330, 0.028, 0.44, 0.016),
    ("VEG-01", "Vega", "Horizontal", 1, 360, 0.006, 0.16, 0.002),
    ("VEG-02", "Vega", "Horizontal", 1, 340, 0.006, 0.15, 0.002),
    ("VEG-03", "Vega", "Horizontal", 2, 300, 0.004, 0.14, 0.002),
    ("VEG-04", "Vega", "Horizontal", 3, 380, 0.003, 0.12, 0.002),
]
META_FACTOR = {"Aurora": 1.00, "Orión": 1.02, "Vega": 0.97}

hechos, metas = [], []
for pid, campo, tipo, inicio, q0, dec, wc0, dwc in POZOS:
    for i, mes in enumerate(MESES, start=1):
        if i < inicio:
            continue
        t = i - inicio
        dias_mes = calendar.monthrange(2026, i)[1]
        tasa = q0 * (1 - dec) ** t * random.uniform(0.96, 1.04)
        if pid == "VEG-03" and t == 0 or pid == "VEG-04" and t == 0:
            tasa *= 0.55  # arranque gradual de pozos nuevos
        paro = random.choice([0, 0, 0, 1, 1, 2, 3])
        if pid == "AUR-03" and mes == "2026-04":
            paro = 12  # reacondicionamiento (workover)
        if pid == "AUR-03" and i >= 5:
            tasa *= 1.38  # el workover recupera producción
        if campo == "Orión" and mes == "2026-07":
            paro += 9  # mantenimiento mayor de la estación de flujo
        dias_op = dias_mes - paro
        petroleo = round(tasa * dias_op)
        wc = min(wc0 + dwc * t, 0.85)
        agua = round(petroleo * wc / (1 - wc))
        gas = round(petroleo * random.uniform(0.9, 1.3) / 1000, 2)  # MMscf
        fijo = 62000
        variable = round(5.8 * petroleo)
        manejo_agua = round(1.4 * agua)
        workover = 180000 if pid == "AUR-03" and mes == "2026-04" else 0
        hechos.append(dict(mes=mes, pozo_id=pid, dias_mes=dias_mes, dias_operativos=dias_op,
                           petroleo_bbl=petroleo, agua_bbl=agua, gas_mmscf=gas,
                           opex_fijo_usd=fijo, opex_variable_usd=variable, opex_agua_usd=manejo_agua,
                           opex_workover_usd=workover, opex_usd=fijo + variable + manejo_agua + workover))
        plan = q0 * (1 - dec * 0.8) ** t * META_FACTOR[campo]
        if t == 0 and pid in ("VEG-03", "VEG-04"):
            plan *= 0.6
        metas.append(dict(mes=mes, pozo_id=pid, meta_bbl_d=round(plan)))

pozos = [dict(pozo_id=p[0], campo=p[1], tipo=p[2], inicio=MESES[p[3] - 1]) for p in POZOS]
precios = [dict(mes=m, brent_usd=b, precio_realizado_usd=round(b - DESCUENTO, 2)) for m, b in zip(MESES, BRENT)]


def guardar(nombre, filas):
    with open(AQUI / "datos" / nombre, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(filas[0]))
        w.writeheader()
        w.writerows(filas)


guardar("hecho_produccion.csv", hechos)
guardar("dim_pozo.csv", pozos)
guardar("dim_precio.csv", precios)
guardar("metas.csv", metas)
(AQUI / "datos.json").write_text(json.dumps(dict(hechos=hechos, pozos=pozos, precios=precios, metas=metas),
                                            ensure_ascii=False, separators=(",", ":")), encoding="utf-8")

total = sum(h["petroleo_bbl"] for h in hechos)
print(f"{len(hechos)} filas de producción · {total:,} bbl de petróleo")
