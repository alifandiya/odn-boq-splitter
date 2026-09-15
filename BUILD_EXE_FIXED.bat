@echo off
setlocal
cd /d "%~dp0"

echo ============================================
echo BUILD EXE FIXED - Kalashnikova BOQ Split
echo ============================================

set PY_CMD=

for %%P in (py -3.14 py -3.13 py -3.12 python) do (
    %%P -c "import sys,platform; print('OK')" >nul 2>&1
    if not errorlevel 1 (
        set PY_CMD=%%P
        goto found
    )
)

:found
if "%PY_CMD%"=="" (
 echo Python tidak ditemukan
 pause
 exit /b 1
)

echo Python: %PY_CMD%

%PY_CMD% -m pip install --upgrade pip
%PY_CMD% -m pip install pandas openpyxl pyinstaller

if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

%PY_CMD% -m PyInstaller ^
 --noconfirm ^
 --clean ^
 --onefile ^
 --windowed ^
 --name Kalashnikova_BOQ_Split_FINAL ^
 --icon app_icon.ico ^
 --add-data "config.json;." ^
 --add-data "material_code_match.txt;." ^
 --add-data "service_code_match.txt;." ^
 --add-data "material_codes_to_delete.txt;." ^
 --add-data "material_codes_to_convert_unit.txt;." ^
 run_app.py

if exist dist\Kalashnikova_BOQ_Split_FINAL.exe (
 echo BUILD BERHASIL
) else (
 echo BUILD GAGAL
)

pause
