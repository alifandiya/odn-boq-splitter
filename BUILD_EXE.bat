@echo off
setlocal EnableExtensions EnableDelayedExpansion
cd /d "%~dp0"

set "APP_NAME=Kalashnikova_BOQ_Split_FINAL"
set "ICON_FILE=%cd%\app_icon.ico"
set "LOG_FILE=%cd%\build_error_log.txt"
set "PY_CMD="

cls
echo ============================================================
echo  BUILD EXE - KALASHNIKOVA BOQ SPLIT FINAL
echo ============================================================
echo.
echo Catatan penting:
echo - File aplikasi utama adalah .pyd yang dikompilasi untuk Python 3.14 64-bit.
echo - Karena itu build WAJIB memakai Python 3.14 Windows 64-bit.
echo - Hasil akhir ada di folder dist.
echo.

echo BUILD LOG - %DATE% %TIME% > "%LOG_FILE%"
echo Folder build: %cd% >> "%LOG_FILE%"
echo. >> "%LOG_FILE%"

if not exist "%ICON_FILE%" (
    echo ERROR: app_icon.ico tidak ditemukan.
    echo ERROR: app_icon.ico tidak ditemukan. >> "%LOG_FILE%"
    pause
    exit /b 1
)

if not exist "%cd%\run_app.py" (
    echo ERROR: run_app.py tidak ditemukan.
    echo ERROR: run_app.py tidak ditemukan. >> "%LOG_FILE%"
    pause
    exit /b 1
)

if not exist "%cd%\%APP_NAME%.pyd" (
    echo ERROR: %APP_NAME%.pyd tidak ditemukan.
    echo ERROR: %APP_NAME%.pyd tidak ditemukan. >> "%LOG_FILE%"
    pause
    exit /b 1
)

call :detect_python314
if "%PY_CMD%"=="" (
    echo Python 3.14 Windows 64-bit tidak ditemukan.
    echo Python 3.14 Windows 64-bit tidak ditemukan. >> "%LOG_FILE%"
    echo.
    echo Solusi:
    echo 1. Install Python 3.14 64-bit.
    echo 2. Centang Add Python to PATH saat install.
    echo 3. Jalankan ulang BUILD_EXE.bat.
    echo.
    pause
    exit /b 1
)

echo Python yang dipakai: %PY_CMD%
echo Python yang dipakai: %PY_CMD% >> "%LOG_FILE%"
%PY_CMD% -c "import sys, platform; print(sys.executable); print(sys.version); print(platform.architecture()[0])" >> "%LOG_FILE%" 2>&1
%PY_CMD% -c "import sys, platform; print('Executable:', sys.executable); print('Version:', sys.version); print('Arch:', platform.architecture()[0])"
echo.

echo [1/7] Update pip...
%PY_CMD% -m pip install --upgrade pip >> "%LOG_FILE%" 2>&1
if errorlevel 1 goto gagal

echo [2/7] Install dependency aplikasi dan builder...
%PY_CMD% -m pip install --upgrade pandas openpyxl pyinstaller >> "%LOG_FILE%" 2>&1
if errorlevel 1 goto gagal

echo [3/7] Test import dependency...
%PY_CMD% -c "import pandas, openpyxl, PyInstaller; print('Dependency OK')" >> "%LOG_FILE%" 2>&1
if errorlevel 1 goto gagal

echo [4/7] Test import modul aplikasi .pyd...
%PY_CMD% -c "import Kalashnikova_BOQ_Split_FINAL as app; print('APP MODULE OK:', app.__name__)" >> "%LOG_FILE%" 2>&1
if errorlevel 1 goto gagal

echo [5/7] Bersihkan folder build lama...
if exist build rmdir /s /q build >> "%LOG_FILE%" 2>&1
if exist dist rmdir /s /q dist >> "%LOG_FILE%" 2>&1
if exist "%APP_NAME%.spec" del /f /q "%APP_NAME%.spec" >> "%LOG_FILE%" 2>&1

echo [6/7] Membuat EXE onefile dengan PyInstaller...
%PY_CMD% -m PyInstaller --clean --noconfirm --onefile --windowed --noupx --name "%APP_NAME%" --icon "%ICON_FILE%" ^
  --add-data "%cd%\app_icon.ico;." ^
  --add-data "%cd%\config.json;." ^
  --add-data "%cd%\material_code_match.txt;." ^
  --add-data "%cd%\material_codes_to_convert_unit.txt;." ^
  --add-data "%cd%\material_codes_to_delete.txt;." ^
  --add-data "%cd%\service_code_match.txt;." ^
  --add-binary "%cd%\%APP_NAME%.pyd;." ^
  --hidden-import "%APP_NAME%" ^
  --hidden-import tkinter ^
  --hidden-import tkinter.ttk ^
  --hidden-import tkinter.filedialog ^
  --hidden-import tkinter.messagebox ^
  --hidden-import openpyxl.cell._writer ^
  --collect-all pandas ^
  --collect-all openpyxl ^
  "%cd%\run_app.py" >> "%LOG_FILE%" 2>&1
if errorlevel 1 goto gagal

echo [7/7] Cek hasil build...
if not exist "dist\%APP_NAME%.exe" goto gagal

echo.
echo ============================================================
echo  BUILD SELESAI
echo ============================================================
echo File EXE berada di:
echo %cd%\dist\%APP_NAME%.exe
echo.
echo Log build tersimpan di:
echo %LOG_FILE%
echo.
echo Silakan jalankan:
echo dist\%APP_NAME%.exe
echo.
pause
exit /b 0

:gagal
echo.
echo ============================================================
echo  BUILD GAGAL ATAU EXE TIDAK TERBENTUK
echo ============================================================
echo Error asli sudah disimpan di:
echo %LOG_FILE%
echo.
echo ===== POTONGAN LOG TERAKHIR =====
powershell -NoProfile -ExecutionPolicy Bypass -Command "if (Test-Path '%LOG_FILE%') { Get-Content '%LOG_FILE%' -Tail 80 }"
echo =================================
echo.
pause
exit /b 1

:detect_python314
rem 1) Python launcher resmi
if "!PY_CMD!"=="" (
    py -3.14 -c "import platform, sys; assert platform.architecture()[0]=='64bit'; assert sys.version_info[:2] == (3,14)" >nul 2>&1
    if not errorlevel 1 set "PY_CMD=py -3.14"
)

rem 2) Python dari PATH, tapi harus benar-benar 3.14 64-bit
if "!PY_CMD!"=="" (
    python -c "import platform, sys; assert platform.architecture()[0]=='64bit'; assert sys.version_info[:2] == (3,14)" >nul 2>&1
    if not errorlevel 1 set "PY_CMD=python"
)

rem 3) Lokasi custom yang sering dipakai
if "!PY_CMD!"=="" (
    for %%P in (
        "C:\Language Programming\Python\Python314\python.exe"
        "C:\Users\user\AppData\Local\Python\pythoncore-3.14-64\python.exe"
        "C:\Python314\python.exe"
    ) do (
        if "!PY_CMD!"=="" if exist "%%~P" (
            "%%~P" -c "import platform, sys; assert platform.architecture()[0]=='64bit'; assert sys.version_info[:2] == (3,14)" >nul 2>&1
            if not errorlevel 1 set "PY_CMD=\"%%~P\""
        )
    )
)
exit /b 0
