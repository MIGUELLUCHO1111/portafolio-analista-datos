# Programar el reporte para que se ejecute solo

El **Programador de tareas** viene gratis con Windows.

## Opción 1 · Con ventanas
1. Inicio → escribe **Programador de tareas** → ábrelo.
2. Panel derecho → **Crear tarea básica**.
3. Nombre: `Reporte de ventas semanal` → Siguiente.
4. Desencadenador: **Semanalmente** → lunes, 8:00 a. m.
5. Acción: **Iniciar un programa**.
6. Programa: la ruta completa de `ejecutar_reporte.bat`, por ejemplo
   `C:\Users\TU_USUARIO\Documents\portafolio-analista-datos\06-automatizacion-ia\ejecutar_reporte.bat`
7. Finalizar. Para probarla: clic derecho sobre la tarea → **Ejecutar**.

## Opción 2 · Con un comando (PowerShell)
```powershell
schtasks /Create /TN "Reporte de ventas semanal" /SC WEEKLY /D MON /ST 08:00 `
  /TR "\"$env:USERPROFILE\Documents\portafolio-analista-datos\06-automatizacion-ia\ejecutar_reporte.bat\""
```

Para borrarla: `schtasks /Delete /TN "Reporte de ventas semanal" /F`

## Cómo saber si funcionó
- Aparece un archivo nuevo en `salida/` con la fecha del día.
- `registro.log` tiene una línea `Reporte generado`. Si algo falla, ahí verás el error.
