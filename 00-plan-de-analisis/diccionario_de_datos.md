# Diccionario de datos

## ventas.csv · tabla de hechos (una fila = una venta)
| Columna | Tipo | Descripción | Ejemplo |
|---|---|---|---|
| id | entero | Identificador único de la venta (llave primaria) | 1 |
| fecha | fecha (AAAA-MM-DD) | Día de la venta | 2026-01-01 |
| vendedor_id | entero | Llave foránea → vendedores.id | 2 |
| producto_id | entero | Llave foránea → productos.id | 102 |
| region | texto | Región del vendedor: Norte, Sur, Este, Oeste | Norte |
| canal | texto | Tienda u Online | Tienda |
| cantidad | entero | Unidades vendidas | 3 |
| precio_unit | decimal (USD) | Precio de lista por unidad | 320 |

## productos.csv · dimensión
| Columna | Tipo | Descripción |
|---|---|---|
| id | entero | Llave primaria |
| nombre | texto | Nombre del producto |
| categoria | texto | Electrónica, Accesorios u Oficina |
| precio | decimal (USD) | Precio de lista |
| costo | decimal (USD) | Costo unitario |

## vendedores.csv · dimensión
| Columna | Tipo | Descripción |
|---|---|---|
| id | entero | Llave primaria |
| nombre | texto | Nombre del vendedor |
| region | texto | Región asignada |
| meta | decimal (USD) | Meta de ingresos del semestre |
