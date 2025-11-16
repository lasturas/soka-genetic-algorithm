# Pengujian Penjadwalan Tugas dengan Algoritma Genetika

Repo ini berisi implementasi **Algoritma Genetika** untuk masalah penjadwalan tugas (Task Scheduling) di lingkungan server nyata. Proyek ini dikembangkan untuk keperluan mata kuliah **Strategi Optimasi Komputasi Awan (SOKA)**.

Algoritma ini bertujuan untuk menugaskan serangkaian tugas ke beberapa server dengan spesifikasi berbeda, dengan tujuan utama meminimalkan waktu penyelesaian total (Makespan).

---

## Cara Menjalankan Proyek

Berikut adalah panduan langkah demi langkah untuk menyiapkan dan menjalankan pengujian.

### Tahap 1: Persiapan Awal

1.  **Unduh Proyek**
    Buka terminal atau Command Prompt dan jalankan perintah berikut untuk mengunduh kode dari repositori ini.
    ```bash
    git clone https://github.com/lasturas/soka-genetic-algorithm.git
    ```
    Setelah itu, masuk ke dalam folder proyek yang baru saja diunduh.
    ```bash
    cd soka-genetic-algorithm
    ```

2.  **Instalasi `uv` (Dependency Manager)**
    Proyek ini menggunakan `uv` untuk mengelola library Python. Instal `uv` dengan menjalankan:
    ```bash
    pip install uv
    ```

3.  **Instalasi Semua Library yang Dibutuhkan**
    `uv` akan membaca file `requirements.txt` dan menginstall semua library yang diperlukan secara otomatis. Jalankan perintah:
    ```bash
    uv sync
    ```

4.  **Periksa File Dataset**
    Pastikan file bernama `dataset.txt` sudah ada di dalam folder proyek. File ini berisi daftar "endpoint" (angka 1-10) untuk setiap tugas, di mana setiap angka berada di baris baru. Panjang setiap tugas akan dihitung berdasarkan rumus `endpoint² * 10000`.

    Jika file tersebut belum ada, buatlah secara manual dengan isi file sebagai berikut.
    ```conf
    6
    5
    8
    2
    10
    3
    4
    4
    7
    3
    9
    1
    7
    9
    1
    8
    2
    5
    6
    10
    ```

### Tahap 2: Konfigurasi dan Eksekusi

1.  **Konfigurasi Alamat Server**
    Pastikan file `.env` sudah ada di dalam folder proyek. Jika belum, buat salinan dari `.env.example` dan beri nama `.env`.

    Buka file `.env` tersebut. Di dalamnya terdapat dua set konfigurasi server: satu untuk **pengujian lokal** dan satu lagi untuk **server asli**.
    
    ```conf
    # Local server (untuk uji coba di komputer sendiri)
    # VM1_IP="127.0.0.1"
    # VM2_IP="127.0.0.1"
    # VM3_IP="127.0.0.1"
    # VM4_IP="127.0.0.1"
    
    # Server Asli (Pak Fuad Server)
    VM1_IP="10.15.42.77"
    VM2_IP="10.15.42.78"
    VM3_IP="10.15.42.79"
    VM4_IP="10.15.42.80"
    
    VM_PORT=5000
    ```
    
    *   Untuk **menjalankan di server asli**, pastikan baris `VMx_IP="10.15.42.xx"` **tidak memiliki tanda `#`** di depannya.
    *   Untuk **melakukan uji coba di komputermu sendiri**, berikan tanda `#` di depan IP server asli dan hapus tanda `#` dari IP `127.0.0.1`.

2.  **Hubungkan ke Jaringan**
    Pastikan komputermu terhubung ke jaringan yang dapat mengakses alamat IP server di atas (misalnya, menggunakan **VPN atau Wifi ITS**).

3.  **Jalankan Penjadwalan**
    Eksekusi skrip utama untuk memulai proses penjadwalan dengan Algoritma Genetika dan mengirimkan tugas ke server.
    ```bash
    uv run scheduler.py
    ```

### Tahap 3: Melihat Hasil

Setelah program selesai berjalan, hasil pengujian akan ditampilkan dan disimpan secara otomatis:

*   **Output di Terminal:**
    Terminal akan menampilkan log dari proses Algoritma Genetika, status pengiriman setiap tugas, dan diakhiri dengan rangkuman metrik performa seperti **Makespan**, **Throughput**, **Resource Utilization**, dll.
    <img width="926" height="381" alt="image" src="https://github.com/user-attachments/assets/b12ef617-6731-4fb5-a36f-271c589414fc" />


*   **File `ga_results.csv`:**
    Sebuah file CSV bernama `ga_results.csv` akan dibuat di dalam folder proyek. File ini berisi catatan detail dari setiap tugas yang dieksekusi, termasuk waktu mulai, waktu eksekusi, dan ke server mana ia ditugaskan. Data ini dapat digunakan untuk analisis lebih lanjut.
    <img width="1204" height="583" alt="image" src="https://github.com/user-attachments/assets/9a0686a2-9543-4184-87c4-afea4268c23e" />
