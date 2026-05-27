# -*- mode: python ; coding: utf-8 -*-
# Spec PyInstaller untuk Kalashnikova BOQ Split V1.
# Perbaikan icon:
# 1. Path icon dibuat absolut dari lokasi file .spec.
# 2. app_icon.ico ikut dimasukkan ke datas agar icon window Tkinter bisa dipakai saat runtime.

from pathlib import Path
from PyInstaller.utils.hooks import collect_submodules, collect_data_files

PROJECT_DIR = Path(SPECPATH) if 'SPECPATH' in globals() else Path.cwd()
ICON_FILE = PROJECT_DIR / 'app_icon.ico'

binaries = [
    (str(PROJECT_DIR / 'Kalashnikova_BOQ_Split_V1.pyd'), '.'),
]

datas = [
    (str(PROJECT_DIR / 'app_icon.ico'), '.'),
    (str(PROJECT_DIR / 'config.json'), '.'),
    (str(PROJECT_DIR / 'material_code_match.txt'), '.'),
    (str(PROJECT_DIR / 'material_codes_to_convert_unit.txt'), '.'),
    (str(PROJECT_DIR / 'material_codes_to_delete.txt'), '.'),
    (str(PROJECT_DIR / 'service_code_match.txt'), '.'),
]

hiddenimports = []
hiddenimports += collect_submodules('pandas')
hiddenimports += collect_submodules('openpyxl')
hiddenimports += [
    'tkinter',
    'tkinter.ttk',
    'tkinter.filedialog',
    'tkinter.messagebox',
]

datas += collect_data_files('pandas')
datas += collect_data_files('openpyxl')


a = Analysis(
    [str(PROJECT_DIR / 'run_app.py')],
    pathex=[str(PROJECT_DIR)],
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
    name='Kalashnikova_BOQ_Split_V1',
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
    icon=str(ICON_FILE),
)
