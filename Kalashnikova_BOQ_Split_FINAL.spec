# -*- mode: python ; coding: utf-8 -*-
# Spec relatif, tidak memakai path absolut D:\ sehingga aman dipindah folder.
from pathlib import Path
from PyInstaller.utils.hooks import collect_all

BASE = Path.cwd()
APP_NAME = 'Kalashnikova_BOQ_Split_FINAL'

datas = [
    (str(BASE / 'app_icon.ico'), '.'),
    (str(BASE / 'config.json'), '.'),
    (str(BASE / 'material_code_match.txt'), '.'),
    (str(BASE / 'material_codes_to_convert_unit.txt'), '.'),
    (str(BASE / 'material_codes_to_delete.txt'), '.'),
    (str(BASE / 'service_code_match.txt'), '.'),
]

binaries = [
    (str(BASE / f'{APP_NAME}.pyd'), '.'),
]

hiddenimports = [
    APP_NAME,
    'tkinter',
    'tkinter.ttk',
    'tkinter.filedialog',
    'tkinter.messagebox',
    'openpyxl.cell._writer',
]

for pkg in ('pandas', 'openpyxl'):
    collected_datas, collected_binaries, collected_hiddenimports = collect_all(pkg)
    datas += collected_datas
    binaries += collected_binaries
    hiddenimports += collected_hiddenimports


a = Analysis(
    [str(BASE / 'run_app.py')],
    pathex=[str(BASE)],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name=APP_NAME,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=[str(BASE / 'app_icon.ico')],
)
