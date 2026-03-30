@echo off
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

echo [1/3] Instalando dependencias necesarias...
pip install -r requirements.txt

echo.
echo [2/3] Creando el ejecutable...
echo Esto puede tardar un par de minutos...
echo.

:: El comando de PyInstaller
:: --noconfirm: Sobreescribe si ya existe la carpeta dist
:: --onefile: Crea un solo archivo .exe
:: --windowed: No abre una consola de comandos al ejecutarlo
:: --add-data: Incluye las carpetas necesarias (formato carpeta_origen;carpeta_destino)
:: --name: Nombre del archivo final
pyinstaller --noconfirm --onefile --windowed ^
    --add-data "templates;templates" ^
    --add-data "static;static" ^
    --name "ConvertidorWebP" ^
    app.py

echo.
if %errorlevel% equ 0 (
    echo [3/3] ¡EXITO!
    echo.
    echo El archivo "ConvertidorWebP.exe" se encuentra en la carpeta "dist".
    echo Puedes copiarlo a tu escritorio o pasarselo a quien quieras.
) else (
    echo [ERROR] Hubo un problema al crear el ejecutable.
)

echo.
pause
