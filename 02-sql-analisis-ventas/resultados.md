# Resultados de las consultas

Generado con `python ejecutar.py` sobre `datos/ventas.db`.


## 1. ¿Cuántas ventas, unidades e ingresos hubo en el semestre?

| num_ventas | unidades | ingreso | ticket_promedio |
|---|---|---|---|
| 120 | 462 | 77,355.00 | 644.63 |

## 2. ¿Qué región genera más ingresos y qué participación tiene?

| region | ingreso | participacion_pct |
|---|---|---|
| Norte | 32,580.00 | 42.10 |
| Sur | 27,175.00 | 35.10 |
| Este | 10,510.00 | 13.60 |
| Oeste | 7,090.00 | 9.20 |

## 3. ¿Cómo evolucionan los ingresos mes a mes y cuánto varían?

| mes | ingreso | variacion | variacion_pct | acumulado |
|---|---|---|---|---|
| 01 | 16,085.00 | None | None | 16,085.00 |
| 02 | 11,940.00 | -4,145.00 | -25.80 | 28,025.00 |
| 03 | 16,190.00 | 4,250.00 | 35.60 | 44,215.00 |
| 04 | 12,190.00 | -4,000.00 | -24.70 | 56,405.00 |
| 05 | 12,915.00 | 725.00 | 5.90 | 69,320.00 |
| 06 | 8,035.00 | -4,880.00 | -37.80 | 77,355.00 |

## 4. ¿Qué productos venden más unidades y cuáles generan más margen?

| nombre | categoria | unidades | ingreso | margen | margen_pct |
|---|---|---|---|---|---|
| Silla ergonómica | Oficina | 44 | 11,440.00 | 4,840.00 | 42.30 |
| Impresora láser | Oficina | 52 | 10,920.00 | 3,640.00 | 33.30 |
| Tablet 10 | Electrónica | 30 | 11,400.00 | 3,300.00 | 28.90 |
| Teclado mecánico | Accesorios | 82 | 6,970.00 | 2,870.00 | 41.20 |
| Laptop Pro 14 | Electrónica | 9 | 10,800.00 | 2,700.00 | 25.00 |
| Monitor 27 | Electrónica | 23 | 7,360.00 | 2,530.00 | 34.40 |
| Webcam HD | Accesorios | 90 | 5,400.00 | 2,520.00 | 46.70 |
| Escritorio ajustable | Oficina | 13 | 6,240.00 | 2,340.00 | 37.50 |
| Audífonos BT | Electrónica | 55 | 5,225.00 | 2,200.00 | 42.10 |
| Mouse inalámbrico | Accesorios | 64 | 1,600.00 | 832.00 | 52.00 |

## 5. ¿Qué categoría es más rentable?

| categoria | ingreso | margen | margen_pct |
|---|---|---|---|
| Oficina | 28,600.00 | 10,820.00 | 37.80 |
| Electrónica | 34,785.00 | 10,730.00 | 30.80 |
| Accesorios | 13,970.00 | 6,222.00 | 44.50 |

## 6. ¿Cumplieron los vendedores su meta semestral?

| nombre | region | ventas | ingreso | meta | cumplimiento_pct | ranking |
|---|---|---|---|---|---|---|
| Luis Pérez | Norte | 34 | 23,920.00 | 18,000.00 | 132.90 | 1 |
| Jorge Medina | Sur | 23 | 15,775.00 | 17,000.00 | 92.80 | 2 |
| María Gómez | Sur | 21 | 11,400.00 | 20,000.00 | 57.00 | 3 |
| Carlos Ruiz | Este | 16 | 10,510.00 | 20,000.00 | 52.50 | 4 |
| Ana Torres | Norte | 13 | 8,660.00 | 22,000.00 | 39.40 | 5 |
| Sofía Díaz | Oeste | 13 | 7,090.00 | 21,000.00 | 33.80 | 6 |

## 7. ¿Qué canal (Tienda u Online) aporta más y con qué ticket promedio?

| canal | ventas | ingreso | ticket_promedio |
|---|---|---|---|
| Online | 49 | 30,985.00 | 632.35 |
| Tienda | 71 | 46,370.00 | 653.10 |

## 8. ¿Cuál es el producto líder de cada región?

| region | producto_lider | ingreso |
|---|---|---|
| Sur | Laptop Pro 14 | 6,000.00 |
| Norte | Tablet 10 | 5,700.00 |
| Este | Silla ergonómica | 3,640.00 |
| Oeste | Tablet 10 | 1,900.00 |

## 9. ¿Cuántas ventas son grandes, medianas o pequeñas?

| tamano | ventas | ingreso |
|---|---|---|
| 1. Grande (>= 1000) | 27 | 37,670.00 |
| 2. Mediana (300-999) | 60 | 35,445.00 |
| 3. Pequeña (< 300) | 33 | 4,240.00 |

## 10. ¿Hay productos sin ventas en algún mes? (control de calidad con LEFT JOIN)

| nombre | meses_con_ventas |
|---|---|
| Escritorio ajustable | 4 |
| Silla ergonómica | 4 |
| Laptop Pro 14 | 5 |
| Monitor 27 | 5 |
| Audífonos BT | 6 |
| Impresora láser | 6 |
| Mouse inalámbrico | 6 |
| Tablet 10 | 6 |
| Teclado mecánico | 6 |
| Webcam HD | 6 |
