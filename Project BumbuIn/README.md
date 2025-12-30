# Project BumbuIn 🌿

Aplikasi CLI marketplace untuk simulasi jual-beli hasil pertanian.

## Struktur Project
*   `src/`: Source code aplikasi (`main.py`, `database.py`)
*   `data/`: Data CSV (`users.csv`, `products.csv`, dll)

## Cara Menjalankan
1.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
2.  Jalankan aplikasi:
    ```bash
    python src/main.py
    ```

## Fitur
*   **Petani**: Jual barang, update stok, lihat laporan.
*   **Pembeli**: Beli barang, dynamic pricing (diskon untuk industri/warung), keranjang belanja.
*   **Admin**: Manajemen user dan laporan lengkap.
