@echo off
echo =====================================
echo   Preparando entorno virtual Python
echo =====================================

:: Crear entorno virtual (si no existe)
if not exist "venv" (
    python -m venv venv
)

:: Activar entorno virtual
call venv\Scripts\activate

:: Instalar requerimientos
pip install -r requirements.txt

echo =====================================
echo   Entorno listo. ¡Todo instalado!
echo =====================================
pause
