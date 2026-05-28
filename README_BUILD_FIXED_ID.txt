README BUILD FIXED - Kalashnikova BOQ Split FINAL

Masalah sebelumnya:
BUILD_EXE.bat menampilkan pesan umum "BUILD GAGAL ATAU EXE TIDAK TERBENTUK", tetapi penyebab asli tertutup di bagian atas jendela CMD.

Perbaikan versi ini:
1. BUILD_EXE.bat tidak lagi bergantung pada file .spec.
2. Script otomatis mencari Python 64-bit dari:
   - py -3.14
   - py -3.13
   - py -3.12
   - py -3.11
   - python dari PATH
   - C:\Language Programming\Python\Python314\python.exe
   - C:\Language Programming\Python\Python313\python.exe
   - C:\Language Programming\Python\Python312\python.exe
   - C:\Language Programming\Python\Python311\python.exe
3. Error asli disimpan di build_error_log.txt.
4. Jika masalah berasal dari icon, tersedia BUILD_EXE_TANPA_ICON.bat sebagai mode darurat.

Cara pakai:
1. Extract ZIP ini.
2. Masuk ke folder hasil extract.
3. Jalankan TEST_JALANKAN_APP.bat terlebih dahulu.
4. Jika aplikasi terbuka, tutup aplikasi.
5. Jalankan BUILD_EXE.bat.
6. Hasil EXE ada di folder dist.

Jika masih gagal:
1. Buka file build_error_log.txt.
2. Copy 30-60 baris paling bawah.
3. Kirimkan ke ChatGPT agar error spesifiknya bisa dibaca.

Catatan Steel clamp:
Versi ini tetap membawa fix Steel clamp. Jika No Material di BOQ utama berisi #N/A, aplikasi akan fallback ke mapping sehingga Steel clamp tetap masuk ke file Material.
