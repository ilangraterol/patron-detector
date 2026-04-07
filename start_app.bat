@echo off
title BTC Pattern Detector

echo.
echo ====================================================================
echo  BTC Pattern Detector - Iniciando aplicacion...
echo ====================================================================
echo.

echo [1/3] Cerrando instancias previas de Python en puerto 5000...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :5000 ^| findstr LISTENING') do (
    taskkill /F /PID %%a >nul 2>&1
)

echo [2/3] Iniciando servidor Flask...
cd /d "%~dp0btc_pattern_app"
start "BTC Pattern Detector" cmd /k "venv\Scripts\python.exe main.py"

echo [3/3] Abriendo navegador...
timeout /t 5 /nobreak >nul
start http://localhost:5000

echo.
echo ====================================================================
echo  Aplicacion iniciada exitosamente!
echo  Abre http://localhost:5000 si no se abrio automaticamente
echo ====================================================================
echo.
pause