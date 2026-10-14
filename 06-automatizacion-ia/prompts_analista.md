# Biblioteca de prompts para analistas de datos

Estructura de cada prompt: **Rol + Contexto + Tarea + Formato + Restricciones + Verificación**.
Antes de usarlos: no pegues datos confidenciales o personales; usa solo herramientas de IA aprobadas por tu empresa y **verifica siempre** el resultado.

## 1. Escribir una consulta SQL
> Actúa como analista experto en SQL. Tengo estas tablas en SQLite: `ventas(id, fecha, vendedor_id, producto_id, region, canal, cantidad, precio_unit)` y `productos(id, nombre, categoria, precio, costo)`. Escribe una consulta que calcule el margen por categoría y región del primer trimestre de 2026, ordenada de mayor a menor. Devuelve solo el código con comentarios en español. Al final explica en dos líneas los supuestos que hiciste.

## 2. Explicar un error
> Actúa como tutor de Python. Este código da el error `KeyError: 'Region'`: [pega el código]. Explícame la causa en lenguaje sencillo, dime en qué línea está y cómo corregirlo. No reescribas todo el código.

## 3. Fórmula de Excel
> Actúa como experto en Excel en español (separador ;). En la columna B tengo la región y en la F el total. Necesito una fórmula que sume el total del Norte solo para ventas mayores a 500. Dame la fórmula, explica cada argumento y un caso para comprobarla a mano.

## 4. Medida DAX
> Actúa como experto en Power BI. Tengo la medida `[Ingresos]` y una tabla `Calendario[Date]` relacionada con `ventas[fecha]`. Escribe una medida que calcule la variación % frente al mes anterior. Usa VAR/RETURN y DIVIDE. Explica qué hace cada línea.

## 5. Plan de limpieza
> Actúa como analista de datos. Te muestro las primeras 10 filas de un CSV (datos anonimizados): [pega]. Lista los problemas de calidad que ves y propón los pasos de limpieza en pandas, en orden, con el código de cada paso.

## 6. Interpretar resultados
> Actúa como jefe de analítica. Estos son los resultados de mi análisis: [pega tabla]. Redacta 3 hallazgos y 1 recomendación para gerencia, en máximo 120 palabras, sin inventar datos que no estén en la tabla.

## 7. Elegir un gráfico
> Quiero mostrar [qué quieres comunicar] con estos datos: [columnas]. Recomiéndame el tipo de gráfico, por qué, y cómo titularlo con la conclusión.

## 8. Documentar un proceso
> Actúa como redactor técnico. Este es mi script: [pega]. Escribe un README en español con: objetivo, requisitos, cómo ejecutarlo, qué archivos genera y cómo saber si falló.

## 9. Revisar mi código
> Revisa este código de Python como un analista senior: [pega]. Señala errores, riesgos y mejoras de legibilidad, en una tabla con línea, problema y sugerencia. No lo reescribas completo.

## 10. Preparar una entrevista
> Hazme una pregunta de entrevista para Analista de Datos Junior sobre [tema]. Espera mi respuesta, califícala del 1 al 10 y dime cómo mejorarla.
