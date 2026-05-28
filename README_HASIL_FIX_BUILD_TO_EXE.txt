README HASIL FIX BUILD TO EXE
Kalashnikova BOQ Split FINAL

Status perbaikan paket:
1. File run_app.py yang sebelumnya tidak ada sudah ditambahkan kembali.
2. BUILD_EXE.bat sudah diperbaiki agar wajib memakai Python 3.14 Windows 64-bit.
3. Alasan wajib Python 3.14: file Kalashnikova_BOQ_Split_FINAL.pyd terhubung ke python314.dll.
4. BUILD_EXE.bat sudah memasukkan file .pyd, icon, config, dan mapping text ke dalam EXE.
5. File .spec sudah diganti menjadi path relatif, tidak lagi memakai path absolut D:\.

Cara build di Windows:
1. Extract ZIP ini ke folder biasa, misalnya Desktop atau D:\Project.
2. Pastikan Python 3.14 Windows 64-bit sudah terpasang.
3. Jalankan TEST_JALANKAN_APP.bat terlebih dahulu.
4. Jika aplikasi terbuka, tutup aplikasi.
5. Jalankan BUILD_EXE.bat.
6. Hasil EXE ada di folder:
   dist\Kalashnikova_BOQ_Split_FINAL.exe

Catatan:
- Jangan jalankan build dengan Python 3.12 atau 3.13 karena file .pyd ini dibuat untuk python314.dll.
- Jika gagal, buka build_error_log.txt lalu kirim 60-80 baris paling bawah untuk dibaca.
