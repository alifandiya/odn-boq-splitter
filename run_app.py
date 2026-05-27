# Launcher untuk menjalankan modul Cython (.pyd) Kalashnikova BOQ Split.
# File ini dibuat kecil agar logic utama tetap berada di .pyd.
# Perbaikan icon:
# - app_icon.ico dipakai untuk icon EXE melalui file .spec.
# - Tkinter.Tk dipatch agar window aplikasi juga memakai app_icon.ico.
# - AppUserModelID Windows diset agar taskbar tidak memakai icon default Python/Tk.

import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
RESOURCE_DIR = Path(getattr(sys, '_MEIPASS', BASE_DIR))
ICON_FILE = RESOURCE_DIR / 'app_icon.ico'

if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))
if str(RESOURCE_DIR) not in sys.path:
    sys.path.insert(0, str(RESOURCE_DIR))


def _set_windows_app_id():
    if sys.platform != 'win32':
        return
    try:
        import ctypes
        app_id = 'Kalashnikova.BOQSplit.V1'
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
    except Exception:
        pass


def _patch_tkinter_icon():
    try:
        import tkinter as tk
    except Exception:
        return

    if not ICON_FILE.exists():
        return

    original_tk_init = tk.Tk.__init__

    def patched_tk_init(self, *args, **kwargs):
        original_tk_init(self, *args, **kwargs)
        try:
            self.iconbitmap(default=str(ICON_FILE))
        except Exception:
            try:
                self.wm_iconbitmap(str(ICON_FILE))
            except Exception:
                pass

    tk.Tk.__init__ = patched_tk_init

    original_toplevel_init = tk.Toplevel.__init__

    def patched_toplevel_init(self, *args, **kwargs):
        original_toplevel_init(self, *args, **kwargs)
        try:
            self.iconbitmap(default=str(ICON_FILE))
        except Exception:
            try:
                self.wm_iconbitmap(str(ICON_FILE))
            except Exception:
                pass

    tk.Toplevel.__init__ = patched_toplevel_init


_set_windows_app_id()
_patch_tkinter_icon()

try:
    import Kalashnikova_BOQ_Split_V1 as app
except Exception as exc:
    raise SystemExit(
        'Gagal memuat modul Kalashnikova_BOQ_Split_V1.pyd.\n'
        'Pastikan memakai Python 3.14 64-bit dan file .pyd berada satu folder dengan launcher.\n'
        f'Detail: {exc}'
    )

if __name__ == '__main__':
    app.main()
