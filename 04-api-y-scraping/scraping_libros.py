"""Web scraping ético de books.toscrape.com (sitio creado para practicar scraping):
extrae título, precio, calificación y disponibilidad de varias páginas y los analiza.
Uso: python scraping_libros.py"""
import time
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import requests
from bs4 import BeautifulSoup

AQUI = Path(__file__).parent
BASE = "https://books.toscrape.com/catalogue/page-{}.html"
HEADERS = {"User-Agent": "Mozilla/5.0 (proyecto de portafolio - aprendizaje)"}
ESTRELLAS = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
PAGINAS = 5

filas = []
for pagina in range(1, PAGINAS + 1):
    resp = requests.get(BASE.format(pagina), headers=HEADERS, timeout=15)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    for libro in soup.select("article.product_pod"):              # contenedor que se repite
        filas.append({
            "titulo": libro.select_one("h3 a").get("title"),         # atributo
            "precio_gbp": libro.select_one(".price_color").get_text(strip=True),
            "estrellas": libro.select_one("p.star-rating").get("class")[1],
            "disponible": libro.select_one(".availability").get_text(strip=True),
            "url": "https://books.toscrape.com/catalogue/" + libro.select_one("h3 a").get("href"),
        })
    print(f"Página {pagina}: {len(filas)} libros acumulados")
    time.sleep(1)                                                   # pausa respetuosa

# Limpieza: texto -> números
df = pd.DataFrame(filas)
df["precio_gbp"] = df["precio_gbp"].str.replace(r"[^\d.]", "", regex=True).astype(float)
df["estrellas"] = df["estrellas"].map(ESTRELLAS)
df["disponible"] = df["disponible"].eq("In stock")
df.to_csv(AQUI / "libros.csv", index=False)

# Análisis
por_estrellas = df.groupby("estrellas")["precio_gbp"].agg(libros="count", precio_promedio="mean").round(2)
print("\nTotal:", len(df), "libros | precio promedio £", round(df["precio_gbp"].mean(), 2))
print("\nPor calificación:\n", por_estrellas)
print("\nTop 5 más caros:\n", df.nlargest(5, "precio_gbp")[["titulo", "precio_gbp", "estrellas"]])

ax = por_estrellas["precio_promedio"].plot(kind="bar", color="#E3122F", rot=0, title="Precio promedio por calificación")
ax.set_xlabel("Estrellas"); ax.set_ylabel("£"); plt.tight_layout(); plt.savefig(AQUI / "libros_precio_estrellas.png", dpi=120)
print("\nArchivos: libros.csv, libros_precio_estrellas.png")
