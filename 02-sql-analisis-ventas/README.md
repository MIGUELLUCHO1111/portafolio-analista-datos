# Proyecto 2 · Análisis de ventas con SQL

**Objetivo:** responder 10 preguntas de negocio sobre la base `datos/ventas.db` (SQLite).

## Archivos

- `consultas.sql` · las 10 consultas, comentadas
- `ejecutar.py` · ejecuta todas las consultas y genera el reporte
- `resultados.md` · **[ver los resultados](resultados.md)**

## Preguntas y técnicas

| # | Pregunta | Técnica SQL |
|---|---|---|
| 1 | Ventas, unidades e ingreso del semestre | Agregaciones |
| 2 | Región con más ingreso y su participación | GROUP BY + subconsulta |
| 3 | Evolución mensual y variación | CTE + `LAG` + acumulado con `SUM() OVER` |
| 4 | Productos con más volumen y margen | JOIN + agregaciones |
| 5 | Categoría más rentable | JOIN + GROUP BY |
| 6 | Cumplimiento de metas | CTE + JOIN + `RANK()` |
| 7 | Tienda vs. Online | GROUP BY |
| 8 | Producto líder por región | `RANK() OVER (PARTITION BY ...)` |
| 9 | Tamaño de las ventas | `CASE WHEN` |
| 10 | Control de calidad: productos sin ventas | `LEFT JOIN` |

## Hallazgos

- **Norte 42,1 %** y **Sur 35,1 %** del ingreso.
- Marzo fue el mejor mes (**$16.190**); junio el peor (**−37,8 %** vs. mayo).
- **Silla ergonómica** es el producto con más margen ($4.840); **Webcam HD** el más vendido (90 u.).
- **Accesorios** tiene el mejor margen relativo (**44,5 %**).
- Solo **1 de 6** vendedores cumplió su meta.

## Cómo ejecutar

```bash
python ejecutar.py
```

También puedes abrir `../datos/ventas.db` con **DB Browser for SQLite** y ejecutar cada consulta.

## Tu turno

1. Escribe una consulta con el **ticket promedio por vendedor y canal**.
2. Encuentra los **3 días con más ingresos** del semestre.
3. Calcula la **participación de cada categoría por región** (ventana con `PARTITION BY`).
4. Agrega tus consultas al final de `consultas.sql` con el formato `-- @pregunta 11. ...` y ejecuta `python ejecutar.py`.
5. Sube tus cambios con `git add`, `git commit` y `git push`.
