# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all

datas = [('D:\\Alif Data\\Alif File\\PROJECT PYTHON\\COMPLETED\\BOQ SPLIT UP BASED ON MATERIAL AND SERVICE\\DRAFT FOR PUBLIC RELEASE\\app_icon.ico', '.'), ('D:\\Alif Data\\Alif File\\PROJECT PYTHON\\COMPLETED\\BOQ SPLIT UP BASED ON MATERIAL AND SERVICE\\DRAFT FOR PUBLIC RELEASE\\config.json', '.'), ('D:\\Alif Data\\Alif File\\PROJECT PYTHON\\COMPLETED\\BOQ SPLIT UP BASED ON MATERIAL AND SERVICE\\DRAFT FOR PUBLIC RELEASE\\material_code_match.txt', '.'), ('D:\\Alif Data\\Alif File\\PROJECT PYTHON\\COMPLETED\\BOQ SPLIT UP BASED ON MATERIAL AND SERVICE\\DRAFT FOR PUBLIC RELEASE\\material_codes_to_convert_unit.txt', '.'), ('D:\\Alif Data\\Alif File\\PROJECT PYTHON\\COMPLETED\\BOQ SPLIT UP BASED ON MATERIAL AND SERVICE\\DRAFT FOR PUBLIC RELEASE\\material_codes_to_delete.txt', '.'), ('D:\\Alif Data\\Alif File\\PROJECT PYTHON\\COMPLETED\\BOQ SPLIT UP BASED ON MATERIAL AND SERVICE\\DRAFT FOR PUBLIC RELEASE\\service_code_match.txt', '.')]
binaries = [('D:\\Alif Data\\Alif File\\PROJECT PYTHON\\COMPLETED\\BOQ SPLIT UP BASED ON MATERIAL AND SERVICE\\DRAFT FOR PUBLIC RELEASE\\Kalashnikova_BOQ_Split_FINAL.pyd', '.')]
hiddenimports = ['Kalashnikova_BOQ_Split_FINAL', 'tkinter', 'tkinter.ttk', 'tkinter.filedialog', 'tkinter.messagebox', 'openpyxl.cell._writer']
tmp_ret = collect_all('pandas')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('openpyxl')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]


a = Analysis(
    ['D:\\Alif Data\\Alif File\\PROJECT PYTHON\\COMPLETED\\BOQ SPLIT UP BASED ON MATERIAL AND SERVICE\\DRAFT FOR PUBLIC RELEASE\\run_app.py'],
    pathex=[],
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
    name='Kalashnikova_BOQ_Split_FINAL',
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
    icon=['D:\\Alif Data\\Alif File\\PROJECT PYTHON\\COMPLETED\\BOQ SPLIT UP BASED ON MATERIAL AND SERVICE\\DRAFT FOR PUBLIC RELEASE\\app_icon.ico'],
)
