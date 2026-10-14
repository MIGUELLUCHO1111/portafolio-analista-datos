@echo off
REM Ejecuta el reporte automático. Úsalo en el Programador de tareas de Windows.
cd /d "%~dp0"
python automatizar_reporte.py
