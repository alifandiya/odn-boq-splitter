@echo off
setlocal
cd /d "%~dp0"

set "APP_NAME=Kalashnikova_BOQ_Split_FINAL"
set "SPEC_FILE=%cd%\Kalashnikova_BOQ_Split_FINAL.spec"
set "ICON_FILE=%cd%\app_icon.ico"
set "PY_CMD="

echo ============================================================
echo  BUILD EXE - Kalashnikova BOQ Split FINAL
echo ============================================================
echo.
echo Catatan penting:
echo - Versi FINAL ini memakai source Python, bukan .pyd.
echo - Build dapat memakai Python 3.12/3.13/3.14 64-bit.
echo - Icon EXE dan icon window memakai app_icon.ico.
echo - Hasil akhir ada di folder dist.
echo.

if not exist "%ICON_FILE%" (
    echo ERROR: File app_icon.ico tidak ditemukan.
    echo Pastikan app_icon.ico berada satu folder dengan BUILD_EXE.bat.
    echo.
    pause
    exit /b 1
)

py -3.12 -c "import platform; assert platform.architecture()[0]=='64bit'" >nul 2>nul
if not errorlevel 1 set "PY_CMD=py -3.12"

if "%PY_CMD%"=="" (
    py -3.13 -c "import platform; assert platform.architecture()[0]=='64bit'" >nul 2>nul
    if not errorlevel 1 set "PY_CMD=py -3.13"
)

if "%PY_CMD%"=="" (
    py -3.14 -c "import platform; assert platform.architecture()[0]=='64bit'" >nul 2>nul
    if not errorlevel 1 set "PY_CMD=py -3.14"
)

if "%PY_CMD%"=="" (
    python -c "import platform; assert platform.architecture()[0]=='64bit'" >nul 2>nul
    if not errorlevel 1 set "PY_CMD=python"
)

if "%PY_CMD%"=="" (
    echo Python 64-bit tidak ditemukan.
    echo Install Python 3.12 64-bit atau 3.13/3.14 64-bit, lalu centang Add Python to PATH.
    echo Setelah itu jalankan ulang BUILD_EXE.bat ini.
    echo.
    pause
    exit /b 1
)

echo Python yang dipakai: %PY_CMD%
%PY_CMD% -c "import sys; print(sys.version)"
echo.

echo [1/5] Update pip...
%PY_CMD% -m pip install --upgrade pip
if errorlevel 1 goto gagal

echo.
echo [2/5] Install dependency aplikasi dan builder...
%PY_CMD% -m pip install pandas openpyxl pyinstaller
if errorlevel 1 goto gagal

echo.
echo [3/5] Bersihkan folder build lama...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist "%APP_NAME%.exe" del /f /q "%APP_NAME%.exe"

echo.
echo [4/5] Membuat EXE dengan icon tertanam...
%PY_CMD% -m PyInstaller --clean --noconfirm "%SPEC_FILE%"
if errorlevel 1 goto gagal

echo.
echo [5/5] Cek hasil build...
if not exist "dist\%APP_NAME%.exe" goto gagal

echo.
echo ============================================================
echo  SELESAI
echo ============================================================
echo File EXE berada di:
echo %cd%\dist\%APP_NAME%.exe
echo.
echo Jika icon masih belum berubah di Windows Explorer:
echo 1. Tutup folder Explorer yang sedang membuka dist.
echo 2. Jalankan BERSIHKAN_CACHE_ICON_WINDOWS.bat.
echo 3. Atau rename EXE menjadi nama baru, misalnya %APP_NAME%_ICON.exe.
echo.
pause
exit /b 0

:gagal
echo.
echo ============================================================
echo  BUILD GAGAL ATAU EXE TIDAK TERBENTUK
echo ============================================================
echo Cek pesan error di atas.
echo Pastikan Python 64-bit, pandas, openpyxl, pyinstaller,
echo dan file app_icon.ico tersedia satu folder dengan file build.
echo.
pause
exit /b 1
