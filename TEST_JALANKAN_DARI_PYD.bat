@echo off
cd /d "%~dp0"
py -3.14 run_app.py
if errorlevel 1 (
  echo.
  echo Aplikasi gagal dibuka dari .pyd.
  echo Pastikan Python 3.14 64-bit sudah terinstall dan dependency sudah dipasang:
  echo py -3.14 -m pip install pandas openpyxl
  echo.
  pause
)
