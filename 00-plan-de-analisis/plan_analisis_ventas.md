# Plan de análisis · Ventas enero–junio 2026

## 1. Solicitud original
> “Gerencia quiere saber cómo vamos con las ventas.”

## 2. Preguntas de negocio (SMART)
1. ¿Qué región generó más ingresos entre enero y junio de 2026 y qué participación tiene?
2. ¿Cómo varió el ingreso mes a mes y cuál fue el peor mes?
3. ¿Qué productos y categorías dejan más margen?
4. ¿Qué vendedores cumplieron su meta semestral?
5. ¿Qué canal (Tienda u Online) tiene mejor ticket promedio?

## 3. KPIs y fórmulas
| KPI | Fórmula | Granularidad |
|---|---|---|
| Ingreso | Σ cantidad × precio_unit | por venta, agregable |
| Margen | Σ cantidad × (precio_unit − costo) | por venta |
| Margen % | margen ÷ ingreso | no se promedia; se recalcula |
| Ticket promedio | ingreso ÷ número de ventas | por segmento |
| Cumplimiento | ingreso del vendedor ÷ meta semestral | por vendedor |

## 4. Fuentes de datos
| Fuente | Contenido | Actualización |
|---|---|---|
| `ventas.csv` | 120 transacciones | semanal (ERP) |
| `productos.csv` | catálogo, precio y costo | mensual |
| `vendedores.csv` | vendedor, región y meta | semestral |

## 5. Supuestos
- `precio_unit` es el precio de lista; no hay descuentos.
- La región de la venta es la región del vendedor.
- Las metas están en USD y cubren todo el semestre.

## 6. Controles de calidad
- [x] Sin filas duplicadas
- [x] Sin vacíos en cantidad ni precio
- [x] Todos los `producto_id` existen en productos
- [x] Totales iguales en Excel, SQL y Python ($77.355)

## 7. Entregables
- Reporte en Excel (proyecto 01), consultas SQL (02), notebook (03), dashboard (05 y web)

## 8. Bitácora
| Fecha | Decisión | Motivo |
|---|---|---|
| 2026-07-02 | Usar ingreso, no unidades, como métrica principal | Los productos tienen precios muy distintos |
| 2026-07-03 | Calcular margen % con totales | Promediar porcentajes distorsiona el resultado |
