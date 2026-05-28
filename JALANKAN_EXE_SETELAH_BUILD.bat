@echo off
cd /d "%~dp0"
if exist "dist\Kalashnikova_BOQ_Split_FINAL.exe" (
  start "" "dist\Kalashnikova_BOQ_Split_FINAL.exe"
) else (
  echo EXE belum ditemukan. Jalankan BUILD_EXE.bat terlebih dahulu.
  pause
)
