# Portafolio · Analista de Datos

Proyectos prácticos de análisis de datos: de los datos crudos a decisiones de negocio.
Cada proyecto responde preguntas reales con la herramienta adecuada y documenta los hallazgos.

**[Ver el dashboard interactivo](https://miguellucho1111.github.io/portafolio-analista-datos/)** · Construido con HTML, JavaScript y Chart.js, publicado con GitHub Pages.

## Proyectos

| # | Proyecto | Herramientas | Qué demuestra |
|---|---|---|---|
| 1 | [Reporte de ventas en Excel](01-excel-reporte-ventas/) | Excel | Tablas, BUSCARV, SUMAR.SI.CONJUNTO, SI anidado, formato condicional, gráficos |
| 2 | [Análisis de ventas con SQL](02-sql-analisis-ventas/) | SQL (SQLite) | JOIN, GROUP BY, HAVING, CASE, CTE y funciones de ventana para 10 preguntas de negocio |
| 3 | [Análisis exploratorio con Python](03-python-analisis-ventas/) | Python, pandas, matplotlib, Jupyter | Limpieza, merge, groupby, pivot_table, gráficos y exportación a Excel |
| 4 | [APIs y Web Scraping](04-api-y-scraping/) | requests, BeautifulSoup, pandas | Consumo de una API pública, scraping ético con paginación y análisis |
| 5 | [Dashboard en Power BI](05-powerbi-dashboard/) | Power BI, DAX, Power Query | Modelo estrella, medidas DAX, CALCULATE, inteligencia de tiempo, tema personalizado |
| ★ | [Dashboard web interactivo](docs/) | HTML, JavaScript, Chart.js | Filtros, filtro cruzado y KPIs publicados en la web |

## Los datos

`datos/` contiene una base de ventas de una distribuidora de tecnología y oficina (enero–junio 2026):

- `ventas.csv` · 120 ventas (fecha, vendedor, producto, región, canal, cantidad, precio)
- `productos.csv` · 10 productos con categoría, precio y costo
- `vendedores.csv` · 6 vendedores con región y meta semestral
- `ventas.db` · las mismas tablas en SQLite

## Hallazgos principales

1. **Norte (42 %) y Sur (35 %) concentran el 77 % del ingreso**; Este y Oeste tienen margen para crecer.
2. **Junio cayó 38 % frente a mayo**, el peor mes del semestre.
3. **Accesorios tiene el mejor margen (44,5 %)** aunque menor ingreso.
4. **Solo 1 de 6 vendedores superó su meta** (Luis Pérez, 133 %); las metas parecen desalineadas por región.

## Cómo ejecutar

```bash
git clone https://github.com/MIGUELLUCHO1111/portafolio-analista-datos.git
cd portafolio-analista-datos
pip install pandas matplotlib openpyxl requests beautifulsoup4 jupyter
```

Luego entra a cada carpeta y sigue su README.

## Aprendiendo haciendo

Cada proyecto incluye una sección **Tu turno** con tareas para ampliarlo. Al completarlas:

```bash
git add .
git commit -m "Describe lo que agregaste"
git push
```

---
Proyectos creados como parte de mi ruta de aprendizaje en el *Laboratorio del Analista de Datos*.
