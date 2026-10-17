"""Funciones del proyecto: carga y limpieza de datos, curvas de declinación (Arps) y evaluación económica.

Las usan el notebook (analisis.ipynb) y el generador del dashboard (construir_web.py),
así los números son los mismos en los dos lugares.
"""
from pathlib import Path

import numpy as np
import pandas as pd

DATOS = Path(__file__).parent / "datos"
BBL_POR_SM3 = 6.2898  # barriles por metro cúbico estándar


# ---------- 1. Carga y limpieza ----------

def cargar_produccion():
    """Producción mensual por campo, en unidades de campo (barriles y miles de barriles por día)."""
    p = pd.read_csv(DATOS / "produccion_mensual.csv")
    p = p.rename(columns={
        "prfInformationCarrier": "campo", "prfYear": "anio", "prfMonth": "mes",
        "prfPrdOilNetMillSm3": "petroleo_msm3", "prfPrdGasNetBillSm3": "gas_bsm3",
        "prfPrdNGLNetMillSm3": "ngl_msm3", "prfPrdCondensateNetMillSm3": "condensado_msm3",
        "prfPrdOeNetMillSm3": "oe_msm3", "prfPrdProducedWaterInFieldMillSm3": "agua_msm3",
    }).drop(columns="prfNpdidInformationCarrier")
    p["campo"] = p["campo"].str.strip().str.upper()
    p["fecha"] = pd.to_datetime(dict(year=p["anio"], month=p["mes"], day=1))
    dias = p["fecha"].dt.days_in_month
    p["petroleo_bbl"] = p["petroleo_msm3"] * 1e6 * BBL_POR_SM3
    p["petroleo_kbd"] = p["petroleo_bbl"] / dias / 1000           # miles de barriles por día
    p["agua_kbd"] = p["agua_msm3"] * 1e6 * BBL_POR_SM3 / dias / 1000
    liquido = p["petroleo_kbd"] + p["agua_kbd"]
    p["corte_agua"] = np.where(liquido > 0, p["agua_kbd"] / liquido, np.nan)  # fracción de agua en el líquido
    return p.sort_values(["campo", "fecha"]).reset_index(drop=True)


def cargar_reservas():
    """Última estimación oficial de reservas de cada campo (MSm³ y millones de barriles)."""
    r = pd.read_csv(DATOS / "reservas.csv")
    r = r.rename(columns={"fldName": "campo", "fldRecoverableOil": "recuperable_msm3",
                          "fldRemainingOil": "remanente_msm3", "fldVersion": "version"})
    r["campo"] = r["campo"].str.strip().str.upper()
    r = r.sort_values("version").groupby("campo").tail(1)
    r["recuperable_mmbbl"] = r["recuperable_msm3"] * BBL_POR_SM3
    r["remanente_mmbbl"] = r["remanente_msm3"] * BBL_POR_SM3
    return r[["campo", "version", "recuperable_msm3", "remanente_msm3", "recuperable_mmbbl", "remanente_mmbbl"]]


def cargar_campos():
    c = pd.read_csv(DATOS / "campos.csv")
    c = c.rename(columns={"fldName": "campo", "cmpLongName": "operador", "fldCurrentActivitySatus": "estado",
                          "fldMainArea": "area", "fldHcType": "tipo", "wlbCompletionDate": "fecha_descubrimiento"})
    c["campo"] = c["campo"].str.strip().str.upper()
    c["anio_descubrimiento"] = pd.to_datetime(c["fecha_descubrimiento"], format="%d.%m.%Y", errors="coerce").dt.year
    return c[["campo", "operador", "estado", "area", "tipo", "anio_descubrimiento"]]


def cargar_brent():
    b = pd.read_csv(DATOS / "brent_mensual.csv", parse_dates=["observation_date"])
    return b.rename(columns={"observation_date": "fecha", "POILBREUSDM": "brent"})


# ---------- 2. Curva de declinación de Arps ----------
# q(t) = qi / (1 + b·Di·t)^(1/b)   (b = 0 es la declinación exponencial: q = qi·e^(-Di·t))
# t en años, Di = declinación inicial anual, b = exponente (0 a 1).

def arps(t, qi, di, b):
    t = np.asarray(t, dtype=float)
    if b < 1e-6:
        return qi * np.exp(-di * t)
    return qi / (1 + b * di * t) ** (1 / b)


def ajustar_arps(t, q):
    """Ajuste por búsqueda en rejilla de b y Di; qi se despeja por mínimos cuadrados en escala logarítmica.
    Devuelve qi, di, b y el R² del ajuste (en escala log)."""
    t, q = np.asarray(t, float), np.asarray(q, float)
    ok = q > 0
    t, lq = t[ok], np.log(q[ok])
    mejor = None
    for b in np.round(np.arange(0, 1.0001, 0.05), 2):
        for di in np.geomspace(0.01, 2.0, 80):
            lf = np.log(arps(t, 1.0, di, b))
            lqi = np.mean(lq - lf)
            sse = np.sum((lq - lqi - lf) ** 2)
            if mejor is None or sse < mejor[0]:
                mejor = (sse, float(np.exp(lqi)), float(di), float(b))
    sse, qi, di, b = mejor
    r2 = 1 - sse / np.sum((lq - lq.mean()) ** 2)
    return {"qi": qi, "di": di, "b": b, "r2": float(r2)}


def pronostico(ajuste, t0, meses=12 * 25, q_limite=0.5):
    """Pronóstico mensual desde t0 (años desde el inicio del ajuste) hasta el límite económico q_limite (kbd)."""
    t = t0 + np.arange(1, meses + 1) / 12
    q = arps(t, ajuste["qi"], ajuste["di"], ajuste["b"])
    return q[q >= q_limite]


# ---------- 3. Evaluación económica simplificada ----------

def vpn(q_kbd, precio, opex, impuesto, tasa):
    """Valor presente neto (millones de USD) de un pronóstico mensual de petróleo.
    Flujo mensual = barriles × (precio − opex) × (1 − impuesto). No incluye inversiones (capex) ni gas."""
    q_kbd = np.asarray(q_kbd, float)
    bbl = q_kbd * 1000 * 30.4375
    flujo = bbl * (precio - opex) * (1 - impuesto) / 1e6
    meses = np.arange(1, len(q_kbd) + 1)
    return float(np.sum(flujo / (1 + tasa) ** (meses / 12)))


def ventana_declinacion(g, meses=120):
    """Elige el tramo a ajustar: desde el pico (media móvil de 3 meses) de los últimos `meses` hasta hoy.
    Si el campo sigue en meseta (últimos 12 meses > 85 % del pico) o hay menos de 24 meses de caída,
    la curva de declinación no aplica todavía."""
    g = g.tail(meses).reset_index(drop=True)
    suave = g["petroleo_kbd"].rolling(3, center=True, min_periods=1).mean()
    pico = int(suave.idxmax())
    tramo = g.iloc[pico:]
    relacion = g["petroleo_kbd"].tail(12).mean() / suave.max()
    if len(tramo) < 24 or relacion > 0.85:
        return None
    return tramo


def calidad(r2):
    return "confiable" if r2 >= 0.6 else "moderado" if r2 >= 0.3 else "poco confiable"
