README BUILD EXE - Kalashnikova BOQ Split V1

ISI PAKET
- Kalashnikova_BOQ_Split_V1.pyd
- run_app.py
- Kalashnikova_BOQ_Split_V1.spec
- BUILD_EXE.bat
- BUILD_EXE_FORCE_ICON.bat
- BERSIHKAN_CACHE_ICON_WINDOWS.bat
- app_icon.ico
- config.json
- file referensi material dan service

PERSYARATAN
1. Windows 64-bit.
2. Python 3.14 64-bit.
3. Koneksi internet saat pertama kali build, karena pip akan memasang pandas, openpyxl, dan pyinstaller.

CARA BUILD NORMAL
1. Ekstrak ZIP ini ke folder baru.
2. Klik kanan BUILD_EXE.bat.
3. Pilih Run as administrator jika diperlukan.
4. Tunggu sampai selesai.
5. File hasil build berada di:
   dist\Kalashnikova_BOQ_Split_V1.exe

PERBAIKAN ICON PADA VERSI INI
Versi ini sudah memasukkan icon ke tiga tempat:
1. Icon EXE melalui parameter icon di file .spec.
2. Icon runtime melalui data app_icon.ico yang ikut dibundel.
3. Icon window Tkinter melalui patch di run_app.py.

JIKA ICON MASIH TIDAK MUNCUL
Coba urutan ini:
1. Pastikan build dilakukan dari ZIP versi terbaru ini, bukan folder build lama.
2. Hapus folder build dan dist lama, atau biarkan BUILD_EXE.bat menghapusnya otomatis.
3. Jalankan BUILD_EXE.bat.
4. Tutup Windows Explorer yang membuka folder dist.
5. Jalankan BERSIHKAN_CACHE_ICON_WINDOWS.bat.
6. Buka lagi folder dist.
7. Jika masih belum berubah, jalankan BUILD_EXE_FORCE_ICON.bat.

CATATAN WINDOWS ICON CACHE
Kadang EXE sudah benar-benar memakai icon baru, tetapi Windows Explorer tetap menampilkan icon lama karena cache. Ini bukan kegagalan PyInstaller. Biasanya selesai dengan membersihkan cache icon, rename file EXE, atau restart Windows.
