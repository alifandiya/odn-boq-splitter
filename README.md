# odn-boq-splitter
Aplikasi ini membaca file Excel BOQ mentah yang kompleks dengan banyak kolom, sel gabungan, dan header bersusun, lalu mengekstrak data kuantitas material serta layanan (service). Outputnya adalah dua file Excel terpisah (Material &amp; Service) dengan format simpel (satu sheet, tanpa warna/filter) yang siap diunggah ke ERP atau sistem manajemen proyek.

# ⚡ FTTH BOQ Splitter & Converter Wizard

![Python Version](https://img.shields.io/badge/python-3.8%20%7C%203.9%20%7C%203.10%20%7C%203.11-blue?style=for-the-badge&logo=python)
![Dependencies](https://img.shields.io/badge/dependencies-pandas%20%7C%20openpyxl-green?style=for-the-badge&logo=pypi)
![UI Language](https://img.shields.io/badge/UI--Language-ID%20%7C%20EN%20%7C%20ZH-orange?style=for-the-badge)
![Industry](https://img.shields.io/badge/Industry-Telecommunication%20%2F%20FTTH-red?style=for-the-badge)

Aplikasi berbasis GUI Python yang dirancang khusus untuk mengotomatisasi pemisahan file *Bill of Quantities* (BOQ) telekomunikasi yang kompleks menjadi format **Material** dan **Service** yang bersih. Siap *upload* langsung ke sistem ERP/manajemen proyek.

---

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
 
