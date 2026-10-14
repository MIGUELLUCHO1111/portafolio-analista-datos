# Proyecto 06 · Automatización de reportes e IA responsable

**Problema:** cada mes llegan archivos de ventas y alguien los une, limpia y resume a mano.
**Solución:** un proceso automático que se ejecuta solo y deja el reporte listo.

## Flujo
```
entrada/ventas_*.csv  →  consolidar  →  limpiar  →  validar  →  calcular KPIs  →  salida/reporte_ventas_FECHA.xlsx
                                                                                      └→ registro.log
```

## Archivos
| Archivo | Para qué |
|---|---|
| `preparar_entrada.py` | Simula archivos mensuales con problemas reales (espacios, mayúsculas, duplicados) |
| `automatizar_reporte.py` | El proceso automático: carga, limpia, valida y genera el Excel |
| `ejecutar_reporte.bat` | Lanzador para el Programador de tareas |
| [`programar_tarea.md`](programar_tarea.md) | Cómo programarlo cada lunes a las 8:00 (gratis) |
| [`prompts_analista.md`](prompts_analista.md) | 10 prompts profesionales para usar IA en el trabajo |

## Cómo ejecutar
```bash
python preparar_entrada.py
python automatizar_reporte.py
```

## Buenas prácticas aplicadas
- **Validación antes de reportar:** si los datos vienen mal, el proceso se detiene y lo registra.
- **Registro (`registro.log`):** cada ejecución deja constancia de qué hizo o por qué falló.
- **Rutas relativas:** funciona en cualquier computadora.
- **Herramientas sin costo:** Python y el Programador de tareas de Windows.

## Tu turno
1. Ejecuta los dos scripts y abre el reporte en `salida/`.
2. Programa la tarea semanal siguiendo `programar_tarea.md`.
3. Agrega una validación nueva: que no haya fechas fuera de 2026.
4. Agrega una hoja **Vendedores** al reporte con el cumplimiento de meta.
5. Usa 3 prompts de la biblioteca con el Tutor IA y guarda en `mis_prompts.md` cuál funcionó mejor y por qué.
6. Sube tus cambios con `git add`, `git commit` y `git push`.
