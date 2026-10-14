"""Reporte automático de ventas.
Lee todos los archivos entrada/ventas_*.csv, los consolida, limpia y valida, calcula KPIs
y genera salida/reporte_ventas_AAAA-MM-DD.xlsx. Registra cada ejecución en registro.log.
Pensado para ejecutarse solo con el Programador de tareas de Windows.
Uso: python automatizar_reporte.py"""
import logging
from datetime import date
from pathlib import Path

import pandas as pd

AQUI = Path(__file__).parent
ENTRADA, SALIDA = AQUI / "entrada", AQUI / "salida"
SALIDA.mkdir(exist_ok=True)
logging.basicConfig(filename=AQUI / "registro.log", level=logging.INFO,
                    format="%(asctime)s | %(levelname)s | %(message)s", encoding="utf-8")


def cargar() -> pd.DataFrame:
    archivos = sorted(ENTRADA.glob("ventas_*.csv"))
    if not archivos:
        raise FileNotFoundError("No hay archivos en entrada/. Ejecuta primero preparar_entrada.py")
    logging.info("Archivos encontrados: %s", ", ".join(a.name for a in archivos))
    return pd.concat([pd.read_csv(a, parse_dates=["fecha"]) for a in archivos], ignore_index=True)


def limpiar(df: pd.DataFrame) -> pd.DataFrame:
    antes = len(df)
    df["region"] = df["region"].str.strip().str.title()
    df = df.drop_duplicates()
    logging.info("Limpieza: %d filas -> %d (duplicados eliminados: %d)", antes, len(df), antes - len(df))
    return df


def validar(df: pd.DataFrame) -> None:
    problemas = []
    if df[["cantidad", "precio_unit"]].isna().any().any():
        problemas.append("hay cantidades o precios vacíos")
    if (df["cantidad"] <= 0).any():
        problemas.append("hay cantidades menores o iguales a cero")
    regiones = set(df["region"]) - {"Norte", "Sur", "Este", "Oeste"}
    if regiones:
        problemas.append(f"regiones desconocidas: {regiones}")
    if problemas:
        raise ValueError("Validación fallida: " + "; ".join(problemas))
    logging.info("Validación correcta")


def reporte(df: pd.DataFrame) -> Path:
    productos = pd.read_csv(AQUI.parent / "datos" / "productos.csv").rename(columns={"id": "producto_id", "nombre": "producto"})
    df = df.merge(productos[["producto_id", "producto", "categoria", "costo"]], on="producto_id")
    df["ingreso"] = df["cantidad"] * df["precio_unit"]
    df["margen"] = df["cantidad"] * (df["precio_unit"] - df["costo"])
    kpis = pd.Series({
        "Ingreso total": df["ingreso"].sum(),
        "Margen %": round(df["margen"].sum() / df["ingreso"].sum() * 100, 1),
        "Ventas": len(df),
        "Ticket promedio": round(df["ingreso"].mean(), 2),
    }, name="valor")
    mensual = df.groupby(df["fecha"].dt.to_period("M").astype(str))["ingreso"].sum()
    region = df.groupby("region")["ingreso"].sum().sort_values(ascending=False)
    producto = df.groupby("producto")[["ingreso", "margen"]].sum().sort_values("margen", ascending=False)

    destino = SALIDA / f"reporte_ventas_{date.today():%Y-%m-%d}.xlsx"
    with pd.ExcelWriter(destino) as xls:
        kpis.to_frame().to_excel(xls, sheet_name="KPIs")
        mensual.to_frame().to_excel(xls, sheet_name="Mensual")
        region.to_frame().to_excel(xls, sheet_name="Region")
        producto.to_excel(xls, sheet_name="Productos")
        df.to_excel(xls, sheet_name="Datos", index=False)
    logging.info("Reporte generado: %s | ingreso total %.2f", destino.name, kpis["Ingreso total"])
    return destino


if __name__ == "__main__":
    try:
        df = limpiar(cargar())
        validar(df)
        archivo = reporte(df)
        print(f"Reporte listo: {archivo}")
    except Exception as error:                      # el error queda registrado para revisarlo
        logging.error("Falló la ejecución: %s", error)
        print(f"Error: {error}. Revisa registro.log")
        raise SystemExit(1)
