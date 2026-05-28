@echo off
setlocal EnableExtensions EnableDelayedExpansion
cd /d "%~dp0"

set "APP_NAME=Kalashnikova_BOQ_Split_FINAL_NO_ICON"
set "LOG_FILE=%cd%\build_error_log_no_icon.txt"
set "PY_CMD="

echo ============================================================
echo  BUILD EXE TANPA ICON - MODE DARURAT
echo ============================================================
echo Gunakan ini hanya jika BUILD_EXE.bat gagal karena masalah icon.
echo.

echo BUILD LOG TANPA ICON - %DATE% %TIME% > "%LOG_FILE%"

call :detect_python
if "%PY_CMD%"=="" (
    echo Python 64-bit tidak ditemukan.
    pause
    exit /b 1
)

echo Python yang dipakai: %PY_CMD%
%PY_CMD% -m pip install --upgrade pip >> "%LOG_FILE%" 2>&1
if errorlevel 1 goto gagal
%PY_CMD% -m pip install pandas openpyxl pyinstaller >> "%LOG_FILE%" 2>&1
if errorlevel 1 goto gagal

if exist build rmdir /s /q build >> "%LOG_FILE%" 2>&1
if exist dist rmdir /s /q dist >> "%LOG_FILE%" 2>&1
if exist "%APP_NAME%.spec" del /f /q "%APP_NAME%.spec" >> "%LOG_FILE%" 2>&1

%PY_CMD% -m PyInstaller --clean --noconfirm --onefile --windowed --name "%APP_NAME%" ^
  --add-data "%cd%\app_icon.ico;." ^
  --add-data "%cd%\config.json;." ^
  --add-data "%cd%\material_code_match.txt;." ^
  --add-data "%cd%\material_codes_to_convert_unit.txt;." ^
  --add-data "%cd%\material_codes_to_delete.txt;." ^
  --add-data "%cd%\service_code_match.txt;." ^
  --hidden-import tkinter ^
  --hidden-import tkinter.ttk ^
  --hidden-import tkinter.filedialog ^
  --hidden-import tkinter.messagebox ^
  --hidden-import openpyxl.cell._writer ^
  --collect-all pandas ^
  --collect-all openpyxl ^
  "%cd%\run_app.py" >> "%LOG_FILE%" 2>&1
if errorlevel 1 goto gagal

if not exist "dist\%APP_NAME%.exe" goto gagal

echo.
echo SELESAI. File EXE ada di:
echo %cd%\dist\%APP_NAME%.exe
echo.
pause
exit /b 0

:gagal
echo.
echo BUILD TANPA ICON GAGAL.
echo Lihat log: %LOG_FILE%
powershell -NoProfile -ExecutionPolicy Bypass -Command "if (Test-Path '%LOG_FILE%') { Get-Content '%LOG_FILE%' -Tail 60 }"
echo.
pause
exit /b 1

:detect_python
for %%V in (3.14 3.13 3.12 3.11) do (
    if "!PY_CMD!"=="" (
        py -%%V -c "import platform; assert platform.architecture()[0]=='64bit'" >nul 2>&1
        if not errorlevel 1 set "PY_CMD=py -%%V"
    )
)
if "!PY_CMD!"=="" (
    python -c "import platform; assert platform.architecture()[0]=='64bit'" >nul 2>&1
    if not errorlevel 1 set "PY_CMD=python"
)
if "!PY_CMD!"=="" (
    for %%P in (
        "C:\Language Programming\Python\Python314\python.exe"
        "C:\Language Programming\Python\Python313\python.exe"
        "C:\Language Programming\Python\Python312\python.exe"
        "C:\Language Programming\Python\Python311\python.exe"
        "C:\Python314\python.exe"
        "C:\Python313\python.exe"
        "C:\Python312\python.exe"
        "C:\Python311\python.exe"
    ) do (
        if "!PY_CMD!"=="" if exist "%%~P" (
            "%%~P" -c "import platform; assert platform.architecture()[0]=='64bit'" >nul 2>&1
            if not errorlevel 1 set "PY_CMD=\"%%~P\""
        )
    )
)
exit /b 0
