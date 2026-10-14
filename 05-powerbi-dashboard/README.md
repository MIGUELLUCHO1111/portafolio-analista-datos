# Proyecto 5 · Dashboard en Power BI

Este proyecto lo construyes tú en **Power BI Desktop** siguiendo la guía. Aquí tienes todo lo necesario:

- `medidas.dax` · todas las medidas listas para copiar
- `tema_galactico.json` · tema de colores personalizado
- Datos: `../datos/ventas.csv`, `productos.csv`, `vendedores.csv`

## Guía paso a paso

### 1. Obtener datos
*Inicio → Obtener datos → Texto o CSV* y carga los tres archivos de `datos/`.

### 2. Limpiar en Power Query (*Transformar datos*)
- Revisa que `fecha` sea tipo **Fecha** y `cantidad` / `precio_unit` sean **Número**.
- Renombra las consultas a `ventas`, `productos`, `vendedores`.
- *Cerrar y aplicar*.

### 3. Modelo estrella (vista **Modelo**)
- `productos[id]` → `ventas[producto_id]` (1 a muchos)
- `vendedores[id]` → `ventas[vendedor_id]` (1 a muchos)
- Crea la tabla `Calendario` (está en `medidas.dax`), márcala como tabla de fechas y relaciona `Calendario[Date]` → `ventas[fecha]`.

### 4. Medidas DAX
*Inicio → Nueva medida* y copia cada medida de `medidas.dax`: Ingresos, Margen %, Ticket Promedio, % del Total, Cumplimiento %, Ingresos Acumulados, Variación vs Mes Anterior %…

### 5. Tema
*Vista → Temas → Examinar temas* y elige `tema_galactico.json`.

### 6. Visuales sugeridos
| Visual | Campos |
|---|---|
| 4 tarjetas | Ingresos, Margen %, Num Ventas, Ticket Promedio |
| Columnas | Eje: region · Valor: Ingresos |
| Línea | Eje: Calendario[Mes] · Valor: Ingresos e Ingresos Mes Anterior |
| Barras | Eje: productos[nombre] · Valor: Margen |
| Tabla | vendedores[nombre], Ingresos, Meta, Cumplimiento %, Estado Meta |
| Segmentadores | region, canal, productos[categoria], Calendario[Mes] |

### 7. Guardar y subir
Guarda como `dashboard_ventas.pbix` en esta carpeta, toma una captura (`captura.png`) y súbelo:

```bash
git add .
git commit -m "Power BI: dashboard de ventas"
git push
```

## Tu turno (retos extra)

1. Agrega formato condicional (verde/rojo) a la columna *Cumplimiento %*.
2. Crea una medida **Top producto** con `TOPN` o `RANKX`.
3. Agrega una página de **detalle** con *Obtener detalles* (drill-through) por vendedor.
4. Pon como título de cada visual la **conclusión**, no solo el nombre del gráfico.

Mientras tanto puedes ver la versión web del dashboard: **[dashboard interactivo](https://miguellucho1111.github.io/portafolio-analista-datos/)**.
