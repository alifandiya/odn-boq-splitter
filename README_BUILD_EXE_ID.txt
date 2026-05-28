README BUILD EXE - Kalashnikova BOQ Split FINAL

ISI PAKET
- Kalashnikova_BOQ_Split_FINAL.py
- run_app.py
- Kalashnikova_BOQ_Split_FINAL.spec
- BUILD_EXE.bat
- BUILD_EXE_FORCE_ICON.bat
- TEST_JALANKAN_APP.bat
- JALANKAN_EXE_SETELAH_BUILD.bat
- BERSIHKAN_CACHE_ICON_WINDOWS.bat
- app_icon.ico
- config.json
- file referensi material dan service

PERBAIKAN FINAL
1. Steel clamp tetap masuk ke output ABD Material meskipun No Material di BOQ utama terbaca kosong, NaN, atau #N/A.
2. Fallback kode material sekarang mencari ke material_code_match.txt terlebih dahulu, lalu ke service_code_match.txt.
3. Mapping Steel clamp juga ditambahkan ke material_code_match.txt sebagai pengaman.
4. Build EXE tidak lagi bergantung pada file .pyd, sehingga tidak terkunci hanya pada Python 3.14.

PERSYARATAN
1. Windows 64-bit.
2. Python 3.12, 3.13, atau 3.14 64-bit.
3. Koneksi internet saat pertama kali build, karena pip akan memasang pandas, openpyxl, dan pyinstaller.

CARA BUILD NORMAL
1. Ekstrak ZIP ini ke folder baru.
2. Klik kanan BUILD_EXE.bat.
3. Pilih Run as administrator jika diperlukan.
4. Tunggu sampai selesai.
5. File hasil build berada di:
   dist\Kalashnikova_BOQ_Split_FINAL.exe

CARA TEST SEBELUM BUILD
1. Jalankan TEST_JALANKAN_APP.bat.
2. Jika aplikasi terbuka, berarti source dan dependency sudah siap.

JIKA ICON MASIH TIDAK MUNCUL
Coba urutan ini:
1. Pastikan build dilakukan dari ZIP versi terbaru ini, bukan folder build lama.
2. Hapus folder build dan dist lama, atau biarkan BUILD_EXE.bat menghapusnya otomatis.
3. Jalankan BUILD_EXE.bat.
4. Tutup Windows Explorer yang membuka folder dist.
5. Jalankan BERSIHKAN_CACHE_ICON_WINDOWS.bat.
6. Buka lagi folder dist.
7. Jika masih belum berubah, jalankan BUILD_EXE_FORCE_ICON.bat.

CATATAN
Windows kadang masih menampilkan icon lama karena cache. Itu bukan berarti build gagal. Biasanya selesai dengan membersihkan cache icon, rename file EXE, atau restart Windows.
