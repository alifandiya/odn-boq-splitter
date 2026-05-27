@echo off
setlocal
cd /d "%~dp0"

set "APP_NAME=Kalashnikova_BOQ_Split_V1"
set "ICON_FILE=%cd%\app_icon.ico"

echo ============================================================
echo  BUILD EXE FORCE ICON - Tanpa memakai file .spec
echo ============================================================
echo.
echo Gunakan file ini hanya jika BUILD_EXE.bat masih menampilkan icon default.
echo.

if not exist "%ICON_FILE%" (
    echo ERROR: File app_icon.ico tidak ditemukan.
    pause
    exit /b 1
)

py -3.14 -c "import platform; assert platform.architecture()[0]=='64bit'" >nul 2>nul
if errorlevel 1 (
    echo Python 3.14 64-bit tidak ditemukan.
    pause
    exit /b 1
)

echo [1/4] Install dependency...
py -3.14 -m pip install --upgrade pip
py -3.14 -m pip install pandas openpyxl pyinstaller
if errorlevel 1 goto gagal

echo.
echo [2/4] Bersihkan folder build lama...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist "%APP_NAME%.spec" del /f /q "%APP_NAME%.spec"

echo.
echo [3/4] Membuat EXE dengan parameter --icon langsung...
py -3.14 -m PyInstaller --clean --noconfirm --onefile --windowed --name "%APP_NAME%" --icon "%ICON_FILE%" ^
  --add-binary "%cd%\Kalashnikova_BOQ_Split_V1.pyd;." ^
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
  --collect-all pandas ^
  --collect-all openpyxl ^
  "%cd%\run_app.py"
if errorlevel 1 goto gagal

echo.
echo [4/4] Cek hasil build...
if not exist "dist\%APP_NAME%.exe" goto gagal

echo.
echo Selesai. File EXE ada di:
echo %cd%\dist\%APP_NAME%.exe
echo.
pause
exit /b 0

:gagal
echo.
echo BUILD FORCE ICON GAGAL. Cek pesan error di atas.
echo.
pause
exit /b 1
