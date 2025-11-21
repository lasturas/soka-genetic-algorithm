# Pengujian Penjadwalan Tugas Cloud dengan Algoritma Genetika

## Tentang Proyek

Repositori ini adalah implementasi dari **Algoritma Genetika (GA)** yang diterapkan untuk menyelesaikan masalah penjadwalan tugas (*Task Scheduling*) di lingkungan server cloud Departemen Teknologi Informasi ITS. Tujuan utama dari proyek ini adalah untuk menemukan jadwal penugasan tugas yang paling optimal ke sekumpulan server dengan spesifikasi yang berbeda.

---

## Algoritma yang Digunakan: Genetic Algorithm (GA)

Algoritma Genetika adalah sebuah **algoritma metaheuristik** yang termasuk dalam keluarga besar **Algoritma Evolusioner (*Evolutionary Algorithm*)**. Logika dasarnya terinspirasi dari teori **evolusi biologis dan seleksi alam** oleh Charles Darwin.

### Cara Kerja Algoritma

Alih-alih mencari solusi secara langsung, GA bekerja dengan cara "menumbuhkan" solusi terbaik melalui proses evolusi selama beberapa generasi. Alur kerjanya adalah sebagai berikut:

1.  **Populasi Awal:** Algoritma dimulai dengan membuat sekumpulan solusi jadwal yang sepenuhnya acak. Setiap solusi ini disebut **individu** atau **kromosom**.
2.  **Evaluasi Fitness:** Setiap individu (jadwal) dinilai kualitasnya menggunakan sebuah **fungsi fitness**. Dalam proyek ini, fitness dihitung berdasarkan kombinasi dari **Makespan** dan **Imbalance Degree (keseimbangan beban)**. Solusi dengan nilai fitness terendah dianggap yang terbaik, karena semakin kecil nilai fitnessnya maka
   - Meminimalkan total waktu penyelesaian (Makespan).
   - Meminimalkan ketidakseimbangan beban antar server (Imbalance Degree).
3.  **Seleksi:** Individu-individu dengan fitness terbaik dipilih untuk menjadi "orang tua" bagi generasi berikutnya. Proses ini meniru "survival of the fittest". Metode yang digunakan di sini adalah **Seleksi Turnamen**.
4.  **Crossover (Pindah Silang):** Dua "orang tua" yang terpilih akan menggabungkan "DNA" (resep jadwal) mereka untuk menciptakan solusi "anak" yang baru. Diharapkan anak ini mewarisi sifat-sifat baik dari kedua orang tuanya.
5.  **Mutasi:** Ada peluang kecil bagi setiap "anak" untuk mengalami perubahan acak pada jadwalnya. Mutasi penting untuk menjaga keragaman dan menemukan solusi-solusi baru yang tidak terduga.

Proses ini (evaluasi, seleksi, crossover, mutasi) diulang selama ratusan **generasi**, di mana setiap generasi baru diharapkan menjadi lebih "unggul" atau lebih optimal daripada generasi sebelumnya.

---

## Pengujian Teknis

### Skenario Pengujian

Pengujian dilakukan dengan mengirimkan serangkaian tugas (didefinisikan dalam `dataset.txt`) ke empat server dengan spesifikasi yang berbeda:

| Server | CPU Cores | RAM (GB) | Alamat IP |
| :--- | :--- | :--- | :--- |
| VM1 | 1 | 1 | `10.15.42.77` |
| VM2 | 2 | 2 | `10.15.42.78` |
| VM3 | 4 | 4 | `10.15.42.79` |
| VM4 | 8 | 4 | `10.15.42.80` |

Panjang setiap tugas dihitung berdasarkan rumus `endpoint² * 10000`, di mana `endpoint` adalah nilai yang diambil dari `dataset.txt`.

### Cara Menjalankan Proyek

Berikut adalah panduan langkah demi langkah untuk menyiapkan dan menjalankan pengujian.

#### Tahap 1: Persiapan Awal

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
    Pastikan file bernama `dataset.txt` sudah ada di dalam folder proyek. Jika belum ada, buatlah secara manual dan isi dengan daftar "endpoint" (angka 1-10) untuk setiap tugas.

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

#### Tahap 2: Konfigurasi dan Eksekusi

1.  **Konfigurasi Alamat Server**
    Pastikan file `.env` sudah ada di dalam folder proyek. Jika belum, buat salinan dari `.env.example` dan beri nama `.env`. File ini berisi dua set konfigurasi:
    *   **Server Asli:** Untuk pengujian di server yang telah ditentukan.

2.  **Hubungkan ke Jaringan**
    Pastikan komputermu terhubung ke jaringan yang dapat mengakses alamat IP tersebut, menggunakan **VPN atau Wifi ITS**.

3.  **Jalankan Penjadwalan**
    Eksekusi skrip utama untuk memulai proses.
    ```bash
    uv run scheduler.py
    ```

### Tahap 3: Output Hasil

Setelah program selesai berjalan, hasil pengujian akan ditampilkan dan disimpan secara otomatis:

*   **Output di Terminal:**
    Terminal akan menampilkan log dari proses Algoritma Genetika, status pengiriman setiap tugas, dan diakhiri dengan rangkuman metrik performa seperti **Makespan**, **Throughput**, **Resource Utilization**, dll.  
    <img width="926" height="381" alt="image" src="https://github.com/user-attachments/assets/b12ef617-6731-4fb5-a36f-271c589414fc" />


*   **File `ga_results.csv`:**
    Sebuah file CSV bernama `ga_results.csv` akan dibuat di dalam folder proyek. File ini berisi catatan detail dari setiap tugas yang dieksekusi, termasuk waktu mulai, waktu eksekusi, dan ke server mana ia ditugaskan. Data ini dapat digunakan untuk analisis lebih lanjut.  
    <img width="1204" height="583" alt="image" src="https://github.com/user-attachments/assets/9a0686a2-9543-4184-87c4-afea4268c23e" />
















