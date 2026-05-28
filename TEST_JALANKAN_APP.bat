@echo off
setlocal EnableExtensions EnableDelayedExpansion
cd /d "%~dp0"
set "PY_CMD="

echo ============================================================
echo  TEST JALANKAN APLIKASI DARI SOURCE / PYD
echo ============================================================
echo Test ini wajib memakai Python 3.14 Windows 64-bit karena file .pyd dibuat untuk python314.dll.
echo.

call :detect_python314
if "%PY_CMD%"=="" (
    echo Python 3.14 Windows 64-bit tidak ditemukan.
    pause
    exit /b 1
)

echo Python yang dipakai: %PY_CMD%
%PY_CMD% -m pip install pandas openpyxl >nul
%PY_CMD% "%cd%\run_app.py"
pause
exit /b 0

:detect_python314
if "!PY_CMD!"=="" (
    py -3.14 -c "import platform, sys; assert platform.architecture()[0]=='64bit'; assert sys.version_info[:2] == (3,14)" >nul 2>&1
    if not errorlevel 1 set "PY_CMD=py -3.14"
)
if "!PY_CMD!"=="" (
    python -c "import platform, sys; assert platform.architecture()[0]=='64bit'; assert sys.version_info[:2] == (3,14)" >nul 2>&1
    if not errorlevel 1 set "PY_CMD=python"
)
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
