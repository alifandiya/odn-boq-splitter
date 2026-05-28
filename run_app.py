# Launcher Kalashnikova BOQ Split FINAL
# File ini sengaja dibuat sebagai entry point PyInstaller.
# Modul utama aplikasi sudah dikompilasi menjadi Kalashnikova_BOQ_Split_FINAL.pyd.

import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
RESOURCE_DIR = Path(getattr(sys, "_MEIPASS", BASE_DIR))
ICON_FILE = RESOURCE_DIR / "app_icon.ico"

if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))
if str(RESOURCE_DIR) not in sys.path:
    sys.path.insert(0, str(RESOURCE_DIR))


def _set_windows_app_id():
    """Agar icon aplikasi muncul benar di taskbar Windows."""
    if sys.platform != "win32":
        return
    try:
        import ctypes
        app_id = "Kalashnikova.BOQSplit.Final"
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
    except Exception:
        pass


def _patch_tkinter_icon():
    """Pasang app_icon.ico otomatis untuk window Tk dan Toplevel."""
    try:
        import tkinter as tk
    except Exception:
        return

    if not ICON_FILE.exists():
        return

    original_tk_init = tk.Tk.__init__
    original_toplevel_init = tk.Toplevel.__init__

    def patched_tk_init(self, *args, **kwargs):
        original_tk_init(self, *args, **kwargs)
        try:
            self.iconbitmap(str(ICON_FILE))
            self.wm_iconbitmap(str(ICON_FILE))
        except Exception:
            pass

    def patched_toplevel_init(self, *args, **kwargs):
        original_toplevel_init(self, *args, **kwargs)
        try:
            self.iconbitmap(str(ICON_FILE))
            self.wm_iconbitmap(str(ICON_FILE))
        except Exception:
            pass

    tk.Tk.__init__ = patched_tk_init
    tk.Toplevel.__init__ = patched_toplevel_init


_set_windows_app_id()
_patch_tkinter_icon()

try:
    import Kalashnikova_BOQ_Split_FINAL as app
except Exception as exc:
    raise SystemExit(
        "Gagal memuat modul Kalashnikova_BOQ_Split_FINAL.pyd.\n"
        "Pastikan file aplikasi berada satu folder dengan launcher.\n"
        f"Detail: {exc}"
    )

if __name__ == "__main__":
    app.main()
