@echo off
setlocal enabledelayedexpansion
echo ======================================================
echo   Preparando la creacion del ejecutable (PyInstaller)
echo ======================================================
echo.

:: Verificar si Python esta instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python no esta instalado o no esta en el PATH.
    pause
    exit /b
)

echo [1/4] Limpiando archivos temporales anteriores...
if exist build rd /s /q build
if exist dist rd /s /q dist
if exist *.spec del /q *.spec

echo [2/4] Instalando dependencias (Flask, Pillow, PyInstaller)...
pip install --quiet flask pillow pyinstaller

echo [3/4] Creando el ejecutable...
echo Esto puede tardar un par de minutos...
echo.

:: El comando de PyInstaller optimizado para Windows
:: Se usan comillas dobles y punto y coma para los datos
pyinstaller --noconfirm --onefile --windowed ^
    --add-data "templates;templates" ^
    --add-data "static;static" ^
    --icon=NONE ^
    --name "ConvertidorWebP" ^
    app.py

echo.
if %errorlevel% equ 0 (
    echo [4/4] ¡EXITO!
    echo.
    echo El archivo "ConvertidorWebP.exe" se encuentra en la carpeta "dist".
    echo Puedes copiarlo a tu escritorio o pasarselo a quien quieras.
) else (
    echo [ERROR] Hubo un problema al crear el ejecutable.
    echo Revisa si tienes algun programa antivirus bloqueando PyInstaller.
)

echo.
pause
