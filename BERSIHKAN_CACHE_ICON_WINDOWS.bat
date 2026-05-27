@echo off
echo ============================================================
echo  Bersihkan cache icon Windows Explorer
echo ============================================================
echo.
echo Script ini hanya membersihkan cache tampilan icon.
echo Tidak mengubah file aplikasi.
echo Explorer akan restart sebentar.
echo.
pause

taskkill /f /im explorer.exe >nul 2>nul
ie4uinit.exe -ClearIconCache >nul 2>nul
ie4uinit.exe -show >nul 2>nul

del /a /q "%localappdata%\IconCache.db" >nul 2>nul
del /a /f /q "%localappdata%\Microsoft\Windows\Explorer\iconcache*" >nul 2>nul

start explorer.exe

echo.
echo Cache icon sudah dibersihkan.
echo Buka ulang folder dist dan cek icon EXE.
echo.
pause
