APLIKASI EXCEL CONVERTER APD ABD MULTIBAHASA

Fitur utama:
1. Dropdown bahasa: English, Indonesia, dan 中文.
2. Teks Cina tidak tampil permanen. Teks Cina hanya tampil ketika bahasa 中文 dipilih.
3. Dropdown tipe file: APD atau ABD.
4. Dropdown worksheet target otomatis membaca sheet dari file Excel yang diupload.
5. Nama file Material dan Service dibuat otomatis, tetapi bisa diedit.
6. Tombol Mulai Konversi untuk menghasilkan file Material dan Service saja.

Cara menjalankan:
1. Extract ZIP.
2. Jalankan INSTALL_REQUIREMENTS.bat satu kali.
3. Jalankan JALANKAN_APLIKASI.bat untuk membuka aplikasi.
4. Pilih bahasa dari dropdown di kanan atas aplikasi.

Catatan:
Jangan menjalankan file .py secara terpisah di luar folder aplikasi, karena aplikasi membutuhkan config.json dan file mapping .txt dalam folder yang sama.

Update terbaru:
Aplikasi sekarang memakai openpyxl untuk membuat output Excel, sehingga tidak lagi bergantung pada modul xlsxwriter.


CATATAN FORMAT OUTPUT:
Versi ini menghasilkan file output sederhana yang mengikuti contoh upload: 1 sheet bernama Sheet1, header bold dengan border, tanpa warna header, tanpa autofilter/freeze pane, dan tanpa salinan Sheet2.


UPDATE OUTPUT TERBARU:
Aplikasi tidak lagi membuat folder _last_backup, tidak lagi menyediakan tombol Undo, dan tidak lagi membuat file Unmatched. Output yang dibuat hanya dua file Excel, yaitu Material dan Service, langsung pada folder tujuan yang dipilih.

UPDATE DINAMIS BOQ:
Pada versi ini, isi output tidak dikunci dari contoh file tertentu. Data output Material dan Service mengikuti sheet BOQ yang dipilih pada dropdown worksheet target.

Kolom yang dibaca dari BOQ input:
- No Material atau Koreksi No Material untuk kode material/service.
- Description/Item untuk deskripsi item.
- Unit untuk satuan.
- Material Qty dan Service Qty untuk kuantitas.
- Remarks untuk penanda Material, Service, atau Material & Service.

Catatan teknis:
File mapping .txt tetap dipakai sebagai fallback dan aturan khusus service split, misalnya kode service tambahan dengan suffix tertentu. Namun prioritas utama output material tetap dari BOQ yang diinput.

UPDATE LEMBAR KERJA TARGET:
Dropdown Lembar Kerja Target sekarang menjadi sumber utama pemrosesan. Jika user memilih BoQ Roll Out ODN, ABD BoQ RO ODN, PO, kode material, atau sheet lain yang memiliki struktur BOQ, aplikasi akan memproses sheet yang dipilih tersebut.

Aturan APD/ABD:
- Jika sheet memiliki beberapa blok qty seperti As Plan, As Build, dan Defiasi, maka APD mengambil blok As Plan dan ABD mengambil blok As Build.
- Jika sheet hanya memiliki satu pasangan Material Qty dan Service Qty, maka pasangan qty itu langsung dipakai sesuai sheet yang dipilih.
- Mengganti tipe APD/ABD tidak lagi menimpa pilihan manual pada dropdown Lembar Kerja Target.
