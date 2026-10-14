-- =====================================================================
-- Proyecto 2 · Análisis de ventas con SQL (SQLite)
-- Base: ../datos/ventas.db  ·  Tablas: ventas, productos, vendedores
-- Cada bloque responde una pregunta de negocio. El script ejecutar.py
-- corre todas las consultas y genera resultados.md
-- =====================================================================

-- @pregunta 1. ¿Cuántas ventas, unidades e ingresos hubo en el semestre?
SELECT COUNT(*)                          AS num_ventas,
       SUM(cantidad)                     AS unidades,
       SUM(cantidad * precio_unit)       AS ingreso,
       ROUND(AVG(cantidad * precio_unit), 2) AS ticket_promedio
FROM ventas;

-- @pregunta 2. ¿Qué región genera más ingresos y qué participación tiene?
SELECT region,
       SUM(cantidad * precio_unit) AS ingreso,
       ROUND(100.0 * SUM(cantidad * precio_unit) / (SELECT SUM(cantidad * precio_unit) FROM ventas), 1) AS participacion_pct
FROM ventas
GROUP BY region
ORDER BY ingreso DESC;

-- @pregunta 3. ¿Cómo evolucionan los ingresos mes a mes y cuánto varían?
WITH mensual AS (
    SELECT strftime('%m', fecha) AS mes, SUM(cantidad * precio_unit) AS ingreso
    FROM ventas
    GROUP BY mes
)
SELECT mes,
       ingreso,
       ingreso - LAG(ingreso) OVER (ORDER BY mes) AS variacion,
       ROUND(100.0 * (ingreso - LAG(ingreso) OVER (ORDER BY mes)) / LAG(ingreso) OVER (ORDER BY mes), 1) AS variacion_pct,
       SUM(ingreso) OVER (ORDER BY mes) AS acumulado
FROM mensual
ORDER BY mes;

-- @pregunta 4. ¿Qué productos venden más unidades y cuáles generan más margen?
SELECT p.nombre,
       p.categoria,
       SUM(s.cantidad)                            AS unidades,
       SUM(s.cantidad * s.precio_unit)            AS ingreso,
       SUM(s.cantidad * (s.precio_unit - p.costo)) AS margen,
       ROUND(100.0 * SUM(s.cantidad * (s.precio_unit - p.costo)) / SUM(s.cantidad * s.precio_unit), 1) AS margen_pct
FROM ventas s
JOIN productos p ON p.id = s.producto_id
GROUP BY p.nombre, p.categoria
ORDER BY margen DESC;

-- @pregunta 5. ¿Qué categoría es más rentable?
SELECT p.categoria,
       SUM(s.cantidad * s.precio_unit)             AS ingreso,
       SUM(s.cantidad * (s.precio_unit - p.costo))  AS margen,
       ROUND(100.0 * SUM(s.cantidad * (s.precio_unit - p.costo)) / SUM(s.cantidad * s.precio_unit), 1) AS margen_pct
FROM ventas s
JOIN productos p ON p.id = s.producto_id
GROUP BY p.categoria
ORDER BY margen DESC;

-- @pregunta 6. ¿Cumplieron los vendedores su meta semestral?
WITH por_vendedor AS (
    SELECT vendedor_id, SUM(cantidad * precio_unit) AS ingreso, COUNT(*) AS ventas
    FROM ventas
    GROUP BY vendedor_id
)
SELECT v.nombre,
       v.region,
       pv.ventas,
       pv.ingreso,
       v.meta,
       ROUND(100.0 * pv.ingreso / v.meta, 1) AS cumplimiento_pct,
       RANK() OVER (ORDER BY pv.ingreso DESC) AS ranking
FROM por_vendedor pv
JOIN vendedores v ON v.id = pv.vendedor_id
ORDER BY ranking;

-- @pregunta 7. ¿Qué canal (Tienda u Online) aporta más y con qué ticket promedio?
SELECT canal,
       COUNT(*)                              AS ventas,
       SUM(cantidad * precio_unit)           AS ingreso,
       ROUND(AVG(cantidad * precio_unit), 2) AS ticket_promedio
FROM ventas
GROUP BY canal;

-- @pregunta 8. ¿Cuál es el producto líder de cada región?
WITH ranking AS (
    SELECT s.region, p.nombre, SUM(s.cantidad * s.precio_unit) AS ingreso,
           RANK() OVER (PARTITION BY s.region ORDER BY SUM(s.cantidad * s.precio_unit) DESC) AS pos
    FROM ventas s
    JOIN productos p ON p.id = s.producto_id
    GROUP BY s.region, p.nombre
)
SELECT region, nombre AS producto_lider, ingreso
FROM ranking
WHERE pos = 1
ORDER BY ingreso DESC;

-- @pregunta 9. ¿Cuántas ventas son grandes, medianas o pequeñas?
SELECT CASE
           WHEN cantidad * precio_unit >= 1000 THEN '1. Grande (>= 1000)'
           WHEN cantidad * precio_unit >= 300  THEN '2. Mediana (300-999)'
           ELSE '3. Pequeña (< 300)'
       END AS tamano,
       COUNT(*) AS ventas,
       SUM(cantidad * precio_unit) AS ingreso
FROM ventas
GROUP BY tamano
ORDER BY tamano;

-- @pregunta 10. ¿Hay productos sin ventas en algún mes? (control de calidad con LEFT JOIN)
SELECT p.nombre, COUNT(DISTINCT strftime('%m', s.fecha)) AS meses_con_ventas
FROM productos p
LEFT JOIN ventas s ON s.producto_id = p.id
GROUP BY p.nombre
ORDER BY meses_con_ventas;
