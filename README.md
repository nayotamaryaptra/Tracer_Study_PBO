# 🎓 Sistem Informasi Tracer Study

Aplikasi berbasis web untuk melacak jejak karir alumni, survei pekerjaan, dan feedback kurikulum universitas. Dibangun menggunakan **Django Framework** dengan tampilan modern (Glassmorphism UI).

![Tracer Study Dashboard](https://img.shields.io/badge/Status-Completed-success) ![Python](https://img.shields.io/badge/Python-3.10%2B-blue) ![Django](https://img.shields.io/badge/Django-5.0-green)

## 🌟 Fitur Utama

### 1. 👥 Manajemen Alumni (Admin)
* **CRUD Alumni:** Input data lengkap dengan foto profil otomatis (inisial).
* **Chained Dropdown:** Pilihan Prodi otomatis menyesuaikan Fakultas yang dipilih.
* **Auto User:** Akun login alumni dibuat otomatis saat data diinput.

### 2. 💼 Tracer Survey (Mahasiswa)
* Input riwayat pekerjaan (Perusahaan, Gaji, Posisi).
* Status "Bekerja" otomatis terupdate di profil jika sudah mengisi survei.
* Visualisasi badge kesesuaian bidang studi.

### 3. 📊 Dashboard Statistik & Laporan (Admin)
* **Grafik Interaktif:** Tren Keterserapan Lulusan (Line Chart) & Relevansi Studi (Polar Chart).
* **Ranking Gaji:** Top Program Studi dengan gaji tertinggi.
* **Export PDF Premium:** Laporan eksekutif siap cetak dengan ringkasan angka & grafik visual.

### 4. 💬 Feedback Kurikulum
* Alumni dapat memberikan masukan mata kuliah.
* Admin dapat memonitor feedback per prodi.

---

## 🚀 Cara Install & Menjalankan (Step-by-Step)

Ikuti langkah ini satu per satu. Pastikan **Python** dan **Git** sudah terinstall di komputermu.

### 1. Clone Repository
Download project ini ke komputermu.
```bash
git clone [MASUKKAN_LINK_GITHUB_KAMU_DISINI]
cd [NAMA_FOLDER_PROJECT]
```

### 2. Buat Virtual Environment
Supaya library tidak bentrok dengan project lain, buat lingkungan virtual.

Untuk Windows:
```bash
python -m venv Env
.venv\Scripts\activate
```
(Jika muncul error "Script is disabled", jalankan: Set-ExecutionPolicy RemoteSigned -Scope Process)

### 3. Install Dependencies
Install semua library yang dibutuhkan (Django, ReportLab, Crispy Forms, dll).
```bash
pip install -r requirements.txt
```
*(Jika tidak ada file requirements.txt, install manual: pip install Django django-crispy-forms crispy-bootstrap5 reportlab)

### 4. Setup Database
Kita perlu menyiapkan database dan tabel-tabelnya.
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Isi Data Master (Otomatis)
Project ini punya fitur Auto Seeding untuk mengisi Fakultas & Prodi UNNES secara otomatis tanpa perlu ketik manual.
```bash
python manage.py seed_fakultas_prodi
```

### 6. Buat Akun Admin (Superuser)
Buat akun untuk login ke halaman Admin/Dashboard.
```bash
python manage.py createsuperuser
```
(Masukkan Username, Email, dan Password sesuai keinginanmu)

### 7. Jalankan Server
Nyalakan aplikasi.
```bash
python manage.py runserver
```
Buka browser dan akses: http://127.0.0.1:8000

🔑 Informasi Login
1. Login sebagai Admin
Gunakan akun Superuser yang baru saja kamu buat di langkah nomor 6.

Akses: Semua Menu (Alumni, Statistik, Survey, Feedback).

2. Login sebagai Alumni (Simulasi)
Untuk mencoba fitur Mahasiswa, kamu harus membuat data alumni dulu lewat Admin.

Login Admin -> Menu Alumni -> Tambah Alumni.

Isi Nama, NIM, Email, dll.

Logout Admin.

Login kembali menggunakan:

Username: (Email yang didaftarkan saat tambah alumni)

Password: (NIM alumni tersebut)

🛠️ Tech Stack
Backend: Django 5, SQLite

Frontend: Bootstrap 5, Bootswatch Zephyr (Theme), Bootstrap Icons

Charts: Chart.js (Line, Polar Area, Doughnut)

PDF Engine: ReportLab