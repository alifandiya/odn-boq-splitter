# odn-boq-splitter
Aplikasi ini membaca file Excel BOQ mentah yang kompleks dengan banyak kolom, sel gabungan, dan header bersusun, lalu mengekstrak data kuantitas material serta layanan (service). Outputnya adalah dua file Excel terpisah (Material &amp; Service) dengan format simpel (satu sheet, tanpa warna/filter) yang siap diunggah ke ERP atau sistem manajemen proyek.


# ⚡ KALASHNIKOVA BOQ SPLITTER

![Python Version](https://img.shields.io/badge/python-3.8%20%7C%203.9%20%7C%203.10%20%7C%203.11-blue?style=for-the-badge&logo=python)
![Dependencies](https://img.shields.io/badge/dependencies-pandas%20%7C%20openpyxl-green?style=for-the-badge&logo=pypi)
![UI Language](https://img.shields.io/badge/UI--Language-ID%20%7C%20EN%20%7C%20ZH-orange?style=for-the-badge)
![Industry](https://img.shields.io/badge/Industry-Telecommunication%20%2F%20FTTH-red?style=for-the-badge)

Aplikasi berbasis GUI Python yang dirancang khusus untuk mengotomatisasi pemisahan file *Bill of Quantities* (BOQ) telekomunikasi yang kompleks menjadi format **Material** dan **Service** yang bersih. Siap *upload* langsung ke sistem ERP/manajemen proyek.

---

Kalashnikova BOQ Splitter & Converter (V1)
Kalashnikova BOQ Splitter & Converter V1 adalah aplikasi desktop berbasis GUI yang dirancang khusus untuk mempercepat alur kerja administrasi teknik, otomatisasi pemisahan, sekaligus standardisasi data Bill of Quantities (BOQ). Perangkat lunak ini ditujukan untuk para insinyur, drafter, dan profesional di bidang telekomunikasi (khususnya pada proyek pembangunan jaringan FTTH/ODN dengan default pabrikan FiberHome).

Aplikasi ini menyatukan proses pemetaan kolom dinamis dan logika penyaringan data ke dalam satu ekosistem user-friendly, sehingga menghilangkan proses pemisahan manual yang melelahkan dalam memilah item Material, komponen Service (Layanan), konversi satuan, hingga kalkulasi otomatis perizinan lingkungan.

🚀 Fitur Utama
Advanced BOQ Splitter: Otomatis memisahkan file Excel BOQ mentah yang kompleks menjadi dua file output terpisah (Material dan Service) dengan format bersih (plain text, tanpa modifikasi gaya bawaan/warna) yang siap diunggah langsung ke sistem ERP pelanggan.
Multilingual GUI: Antarmuka grafis interaktif mendefinisikan kenyamanan pengguna dengan dukungan tiga bahasa (Indonesia, Inggris, dan Mandarin) yang dapat dialihkan secara dinamis dari panel utama.
Dynamic Mapping & Smart Filtering: Sistem secara otomatis mendeteksi baris header menggunakan alias berbasis konfigurasi JSON (tahan terhadap pergeseran kolom) serta menyaring material secara otomatis (blacklist), mengubah satuan kabel secara presisi (Meter ke KM), dan menambahkan baris perizinan RT/RW (Community Permit) berdasarkan kuantitas Home Pass.
Flexible Document Modes (APD & ABD): Mendukung pengolahan dokumen terintegrasi baik untuk tahap perencanaan (APD - As Plan Design) maupun tahap realisasi lapangan (ABD - As Build Design) hanya dengan sekali klik dropdown lembar kerja target.

🔥 Fitur Unggulan

🌐 Trilingual Interface: Ganti bahasa GUI secara instan antara Indonesia, English, dan Mandarin (中文) langsung dari dropdown.

🛡️ Zero-Rigid Structure: Bebas dari error kolom geser! Sistem memindai posisi kolom menggunakan alias teks secara dinamis.

📐 Smart Unit Scaling: Otomatis mengubah satuan kabel serat optik tertentu dari Meter (m) ke Kilometer (KM) demi akurasi input sistem.

🏡 Auto Community Permit (Opsional): Jika diaktifkan, skrip akan menembak baris baru berisi data perizinan RT/RW (Home Pass) secara otomatis berdasarkan sel referensi.

📁 Bedah Struktur Proyek
├── Kalashnikova_BOQ_Split_V1.py           # Kode utama aplikasi (GUI Tkinter)
├── config.json                            # Remote control aplikasi (Alias & Konfigurasi)
├── material_code_match.txt                # Database fallback deskripsi kode material
├── service_code_match.txt                 # Database fallback deskripsi kode service
├── material_codes_to_delete.txt           # Blacklist item yang akan otomatis dibuang
├── material_codes_to_convert_unit.txt     # Target item untuk konversi satuan (m -> KM)
├── requirements.txt                       # Library Python yang dibutuhkan
├── INSTALL_REQUIREMENTS.bat               # Installer dependensi (Sekali klik)
└── JALANKAN_APLIKASI.bat                  # Launcher aplikasi Windows (Sekali klik)

🛠️ Teknologi yang Digunakan
Aplikasi ini dibangun menggunakan ekosistem Python modern yang dioptimalkan untuk performa manipulasi data struktural tingkat tinggi, memanfaatkan beberapa pustaka powerhouse berikut:
Python 3.x: Menggunakan runtime Python untuk efisiensi eksekusi data dan kestabilan antarmuka grafis.
Pandas: Digunakan di balik layar untuk menangani manipulasi struktur data tabel, pemisahan baris berbasis kondisi, dan pemrosesan array data BOQ berskala besar secara instan.
Openpyxl Engine: Digunakan sebagai mesin penulis dokumen Excel keluaran demi menjamin hasil akhir berupa spreadsheet yang bersih, akurat, dan kompatibel dengan template upload sistem.
Tkinter Engine: Menghadirkan tampilan panel kontrol, dropdown sheet dinamis, dan baris status pemrosesan yang responsif serta bebas dari dependensi eksternal yang berat.

💻 Cara Penggunaan
1. **Unduh Aplikasi**: Masuk ke tab [Releases]([https://github.com/alifandiya/odn-boq-splitter/releases/tag/odn_boq_splitter]) di repositori ini dan unduh semua file source code.
Instal Dependensi: Cukup klik dua kali pada file BUILD_EXE.bat. untuk memasang modul pustaka yang dibutuhkan secara otomatis.
Jalankan Aplikasi: Klik dua kali pada file JALANKAN_APLIKASI.bat untuk membuka antarmuka grafis aplikasi.
Pilih Parameter & File: Pilih bahasa yang diinginkan, tentukan jenis dokumen (APD/ABD), unggah file Excel BOQ input, lalu pilih lembar kerja target dari dropdown yang muncul.
Mulai Konversi: Klik tombol Mulai Konversi untuk mengekstrak data. Hasil akhir berupa file Material dan Service akan langsung digenerate pada folder tujuan yang telah ditentukan.

📋 Persyaratan Sistem
Sistem Operasi: Windows 10 / Windows 11 (64-bit).
Prasyarat Perangkat Lunak: Python 3.x terinstal di sistem dan terdaftar dalam Environment Path.
Folder kerja harus tetap mempertahankan kesatuan file skrip bersama dengan file konfigurasi (config.json) serta file aturan pemetaan teks (.txt).

🤝 Kontribusi
Kontribusi selalu terbuka! Jika Anda menemukan bug, memiliki ide penyesuaian untuk format vendor/pabrikan lain, atau ingin mengoptimalkan algoritma pemetaan kolom ini:
Fork repositori ini.
Buat feature branch baru (git checkout -b fitur-keren-anda).
Lakukan commit perubahan Anda (git commit -m 'Menambahkan fitur keren').
Push ke branch tersebut (git push origin fitur-keren-anda).
Buat sebuah Pull Request.

## 📄 Lisensi

Proyek ini dilisensikan di bawah [MIT License](LICENSE) – Anda bebas menggunakannya untuk kebutuhan personal maupun komersial.



## 🗺️ Alur Kerja Aplikasi (Data Pipeline)

Berikut adalah gambaran bagaimana aplikasi memproses data secara dinamis dari file mentah Anda:

```text
   [ File BOQ Mentah (.xlsx) ]
                │
                ▼
   ┌─────────────────────────────┐
   │ Dynamic Column Identifier   │ ◄─── (Membaca alias dari config.json)
   └────────────┬────────────────┘
                │
                ├────────────────────────┐
                ▼                        ▼
       [ Mode APD (As Plan) ]   [ Mode ABD (As Build) ]
                │                        │
                └───────────┬────────────┘
                            │
                            ▼
   ┌─────────────────────────────┐
   │  Unit Converter & Filter    │ ◄─── (Konversi m -> KM & Filter Blacklist)
   └────────────┬────────────────┘
                │
        ┌───────┴───────┐
        ▼               ▼
   [ Material Qty ]  [ Service Qty ]
        │               │
        ▼               ▼
 📦 File Material  🛠️ File Service
 (Format Clean)    (+ RT/RW Permit Opsional)
 
