@echo off
setlocal
cd /d "%~dp0"

set "APP_NAME=Kalashnikova_BOQ_Split_V1"
set "SPEC_FILE=%cd%\Kalashnikova_BOQ_Split_V1.spec"
set "ICON_FILE=%cd%\app_icon.ico"

echo ============================================================
echo  BUILD EXE - Kalashnikova BOQ Split V1
echo ============================================================
echo.
echo Catatan penting:
echo - File .pyd ini dibuat untuk Python 3.14 64-bit.
echo - Build harus dijalankan di Windows 64-bit.
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

py -3.14 -c "import sys; import platform; print(sys.version); print(platform.architecture()[0]); assert platform.architecture()[0]=='64bit'" >nul 2>nul
if errorlevel 1 (
    echo Python 3.14 64-bit tidak ditemukan.
    echo Silakan install Python 3.14 64-bit, lalu centang Add Python to PATH.
    echo Setelah itu jalankan ulang BUILD_EXE.bat ini.
    echo.
    pause
    exit /b 1
)

echo [1/5] Update pip...
py -3.14 -m pip install --upgrade pip
if errorlevel 1 goto gagal

echo.
echo [2/5] Install dependency aplikasi dan builder...
py -3.14 -m pip install pandas openpyxl pyinstaller
if errorlevel 1 goto gagal

echo.
echo [3/5] Bersihkan folder build lama...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist "%APP_NAME%.exe" del /f /q "%APP_NAME%.exe"

echo.
echo [4/5] Membuat EXE dengan icon tertanam...
py -3.14 -m PyInstaller --clean --noconfirm "%SPEC_FILE%"
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
echo Pastikan Python 3.14 64-bit, pandas, openpyxl, pyinstaller,
echo dan file app_icon.ico tersedia satu folder dengan file build.
echo.
pause
exit /b 1
