# Ejemplo de Power BI · Operaciones de pozos

Muestra de cómo se ve un reporte de Power BI terminado, con un tema del sector petrolero: **12 pozos en 3 campos (Aurora, Orión y Vega), de enero a septiembre de 2026**.

**Ver el reporte interactivo:** https://miguellucho1111.github.io/portafolio-analista-datos/ejemplo-powerbi/

> Los datos son **simulados** con fines de aprendizaje. No representan ningún activo real.

## Qué tiene el reporte
| Página | Visuales | Qué responde |
|---|---|---|
| Resumen | 5 tarjetas KPI, columnas apiladas con línea de plan, ranking de pozos, narrativa automática, días de paro | ¿Cumplimos el plan? ¿Qué pozos producen más? |
| Pozos | Matriz con formato condicional y subtotales, dispersión corte de agua vs costo | ¿Qué pozos están en problemas y por qué? |
| Economía | Tarjetas, precio vs costo por barril, margen por campo, cascada de ingresos a margen | ¿Cuánto ganamos por barril y en qué se va el costo? |
| Modelo y DAX | Modelo estrella y las 13 medidas con su valor en vivo | ¿Cómo está construido? |

Como en Power BI, tiene **segmentadores** (campo y meses), **filtro cruzado** (clic en un pozo o en un mes filtra todo) e **información sobre herramientas** al pasar el mouse. Cada visual tiene el botón **ƒx DAX** con las medidas que usa.

## Historia que cuentan los datos
- **Orión** va por debajo del plan: su corte de agua sube cada mes y su costo por barril es el más alto.
- En **julio** hubo un mantenimiento mayor en la estación de Orión: es el mes con más días de paro.
- El **workover de AUR-03** en abril costó US$ 180.000, pero subió su tasa cerca de un 40 %.
- **Vega** crece porque entraron dos pozos nuevos (VEG-03 en febrero y VEG-04 en marzo).

## Archivos
| Archivo | Para qué |
|---|---|
| `datos/hecho_produccion.csv` | Tabla de hechos: producción, agua, gas, días y costos por pozo y mes |
| `datos/dim_pozo.csv` | Dimensión de pozos: campo, tipo y fecha de inicio |
| `datos/dim_precio.csv` | Precio Brent y precio realizado por mes |
| `datos/metas.csv` | Plan de producción (bbl/d) por pozo y mes |
| `medidas.dax` | Las 13 medidas del reporte |
| `generar_datos.py` | Crea los datos simulados |
| `plantilla.html` · `construir_web.py` | Generan la página web del reporte |

## Tu turno: constrúyelo en Power BI Desktop
1. *Obtener datos → Texto o CSV* y carga los 4 archivos de `datos/`.
2. En Power Query, convierte `mes` a tipo **Fecha** y revisa que los números sean numéricos.
3. Crea la tabla `Calendario` (está en `medidas.dax`) y márcala como tabla de fechas.
4. En la vista Modelo, relaciona `Dim_Pozo[pozo_id]`, `Dim_Precio[mes]` y `Calendario[Date]` con la tabla de hechos.
5. Crea las medidas de `medidas.dax`, en orden.
6. Reproduce los visuales de la página Resumen y aplica `../tema_galactico.json`.
7. Guarda `operaciones_pozos.pbix` aquí, toma una captura y súbela con `git add`, `git commit` y `git push`.

Consejo del mentor: compara cada tarjeta de tu .pbix con la página web. Si los números no coinciden, revisa primero las relaciones del modelo, que es donde suelen estar los errores.
