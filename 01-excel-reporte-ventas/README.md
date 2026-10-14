# Proyecto 1 · Reporte de ventas en Excel

**Pregunta:** ¿cuánto vendimos, con qué margen, qué región lidera y qué vendedores cumplieron su meta?

## Archivo

`reporte_ventas.xlsx` (ábrelo en Excel; todas las cifras se calculan con fórmulas):

| Hoja | Contenido |
|---|---|
| **Resumen** | KPIs, ingreso por región con participación, cumplimiento de metas y gráfico |
| **Datos** | 120 ventas en formato Tabla con columnas calculadas |
| **Productos / Vendedores** | Tablas de búsqueda |
| **Tu turno** | Tareas para practicar |

## Fórmulas que se usan

| Fórmula | Dónde | Para qué |
|---|---|---|
| `=BUSCARV(E2;Productos!$A$2:$D$11;2;FALSO)` | Datos[Categoría] | Traer la categoría del producto |
| `=F2*G2` | Datos[Total] | Ingreso de cada venta |
| `=SI(J2>=1000;"Grande";SI(J2>=300;"Mediana";"Pequeña"))` | Datos[Tamaño] | Clasificar ventas |
| `=SUMAR.SI(Datos!B:B;D4;Datos!J:J)` | Resumen | Ingreso por región |
| `=E4/$B$4` | Resumen | Participación (referencia absoluta) |
| `=CONTAR.SI.CONJUNTO(...;"Online")` | Resumen | Ventas online por región |
| `=SUMAR.SI.CONJUNTO(...)` | Resumen | Ingreso por vendedor |
| `=SI.ERROR(B14/C14;0)` | Resumen | Cumplimiento sin errores |

Además: formato condicional (barras de datos y semáforo de metas), paneles inmovilizados y gráfico de columnas.

## Resultados

- Ingreso total **$77.355** · Margen **35,9 %** · Ticket promedio **$644,63**
- Norte aporta el **42,1 %** del ingreso
- Solo **Luis Pérez** superó su meta (**132,9 %**)

## Cómo se construyó

`construir_excel.py` genera el libro con `openpyxl` a partir de `../datos`. Para regenerarlo:

```bash
python construir_excel.py
```

## Tu turno

1. Convierte el número de mes en nombre con `=TEXTO(A2;"mmmm")`.
2. Crea una **tabla dinámica**: Producto en filas, Canal en columnas, Total en valores.
3. Agrega una **segmentación** por Región.
4. Calcula el ingreso de *Laptop Pro 14* en el Norte con `SUMAR.SI.CONJUNTO`.
5. Usa `BUSCARX` para traer la región de cada vendedor.
6. Crea un gráfico de líneas con el ingreso mensual.
7. Guarda y sube tus cambios: `git add . && git commit -m "Excel: tabla dinámica" && git push`
