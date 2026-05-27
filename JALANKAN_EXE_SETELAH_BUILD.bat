@echo off
cd /d "%~dp0"
if exist "dist\Kalashnikova_BOQ_Split_V1.exe" (
    start "" "dist\Kalashnikova_BOQ_Split_V1.exe"
) else (
    echo File EXE belum ada.
    echo Jalankan BUILD_EXE.bat terlebih dahulu.
    pause
)
