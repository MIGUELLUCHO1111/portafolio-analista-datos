"""Consume la API pública y gratuita Frankfurter (sin clave) para analizar el tipo de cambio USD
en el primer semestre de 2026. Uso: python api_tipo_cambio.py"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import requests

AQUI = Path(__file__).parent
URL = "https://api.frankfurter.app/2026-01-01..2026-06-30"
PARAMS = {"from": "USD", "to": "EUR,MXN"}

# 1) Petición con timeout y control de errores
resp = requests.get(URL, params=PARAMS, timeout=15)
resp.raise_for_status()                      # detiene el script si la API responde 4xx/5xx
data = resp.json()
print("Estado:", resp.status_code, "| base:", data["base"], "| días:", len(data["rates"]))

# 2) JSON anidado -> tabla: {"fecha": {"EUR": x, "MXN": y}} -> filas
df = (pd.DataFrame.from_dict(data["rates"], orient="index")
        .rename_axis("fecha").reset_index())
df["fecha"] = pd.to_datetime(df["fecha"])
df = df[df["fecha"] >= "2026-01-01"]          # la API incluye el último día hábil previo
df.to_csv(AQUI / "tipo_cambio_diario.csv", index=False)

# 3) Análisis: promedio mensual, variación y volatilidad
mensual = df.set_index("fecha").resample("ME").mean().round(4)
mensual.index = mensual.index.strftime("%Y-%m")
resumen = pd.DataFrame({
    "inicio": df.iloc[0, 1:], "fin": df.iloc[-1, 1:],
    "minimo": df.iloc[:, 1:].min(), "maximo": df.iloc[:, 1:].max(),
    "volatilidad_std": df.iloc[:, 1:].std().round(4),
})
resumen["variacion_%"] = ((resumen["fin"] / resumen["inicio"] - 1) * 100).round(2)
print("\nPromedio mensual:\n", mensual, "\n\nResumen del semestre:\n", resumen)
mensual.to_csv(AQUI / "tipo_cambio_mensual.csv")

# 4) Gráfico
fig, ejes = plt.subplots(1, 2, figsize=(11, 4))
for ax, moneda, color in zip(ejes, ["EUR", "MXN"], ["#1E5BFF", "#11A64B"]):
    ax.plot(df["fecha"], df[moneda], color=color)
    ax.set_title(f"USD → {moneda} (diario)"); ax.tick_params(axis="x", rotation=30)
plt.tight_layout(); plt.savefig(AQUI / "tipo_cambio.png", dpi=120)
print("\nArchivos: tipo_cambio_diario.csv, tipo_cambio_mensual.csv, tipo_cambio.png")
