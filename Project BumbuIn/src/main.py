import os
import time
import sys
from tabulate import tabulate
from typing import List, Dict, Any, Optional
import database

def bubble_sort(data: List[Dict], key: str, descending: bool = False) -> List[Dict]:
    """
    Algoritma Bubble Sort untuk mengurutkan daftar produk.
    Kompleksitas: O(n^2) - Cocok untuk pembelajaran.
    """
    n = len(data)
    data_sorted = data.copy() # Agar data asli tidak berubah
    for i in range(n):
        for j in range(0, n - i - 1):
            # Tentukan kondisi swap berdasarkan descending/ascending
            if descending:
                should_swap = data_sorted[j][key] < data_sorted[j + 1][key]
            else:
                should_swap = data_sorted[j][key] > data_sorted[j + 1][key]
            
            if should_swap:
                # Tukar posisi
                data_sorted[j], data_sorted[j + 1] = data_sorted[j + 1], data_sorted[j]
    return data_sorted

def binary_search(data: List[Dict], target_id: str) -> Optional[Dict]:
    # Pastikan data terurut berdasarkan id_barang (konversi ke int untuk perbandingan yang benar)
    # Kita urutkan salinan data agar tidak merusak urutan asli tampilan
    sorted_data = sorted(data, key=lambda x: int(x['id_barang']))
    
    low = 0
    high = len(sorted_data) - 1
    try:
        target_int = int(target_id)
    except ValueError:
        return None
    
    while low <= high:
        mid = (low + high) // 2
        mid_val = int(sorted_data[mid]['id_barang'])
        
        if mid_val == target_int:
            return sorted_data[mid]
        elif mid_val < target_int:
            low = mid + 1
        else:
            high = mid - 1
            
    return None

def tampilkan_stack_riwayat(transaksi_list: List[Dict]):
    # Konsep Stack: LIFO (Last In First Out)
    # Kita gunakan list[::-1] atau reversed() untuk membalik urutan
    stack_tampilan = []
    headers = ["ID Barang", "Nama Barang", "Jumlah", "Harga", "Total", "Penjual"]
    
    # Push data ke stack tampilan (dari belakang ke depan)
    for t in reversed(transaksi_list):
        stack_tampilan.append([
            t['id_barang'],
            t['nama_barang'],
            t['jumlah'],
            f"Rp {t['harga']:,.0f}",
            f"Rp {t['total_harga']:,.0f}",
            t['penjual']
        ])
        
    print(tabulate(stack_tampilan, headers=headers, tablefmt="fancy_grid"))

def clear_screen():
    """Membersihkan layar terminal."""
    os.system('cls' if os.name == 'nt' else 'clear')

def validasi_input_angka(prompt: str) -> float:
    """Meminta input angka valid dari pengguna."""
    while True:
        try:
            nilai = float(input(prompt))
            if nilai < 0:
                print("Angka tidak boleh negatif!")
                continue
            return nilai
        except ValueError:
            print("Masukkan angka yang valid!")

def format_rupiah(nilai: float) -> str:
    """Format angka ke format Rupiah standar."""
    return f"Rp {nilai:,.0f}".replace(",", ".")

def hitung_diskon_pembeli(harga: float, tipe_pembeli: str) -> float:
    """Menghitung harga akhir berdasarkan tipe pembeli (Logika Bisnis)."""
    if tipe_pembeli == 'Pelaku Industri':
        return harga * 0.90  # Diskon 10%
    elif tipe_pembeli == 'Pembeli Warungan':
        return harga * 0.95  # Diskon 5%
    return harga

def login():
    """Menu Login Utama."""
    while True:
        clear_screen()
        print("=== LOGIN BUMBUIN ===")
        print("1. Login")
        print("2. Daftar")
        print("0. Keluar")
        pilihan = input("Pilih menu: ")
        
        if pilihan == "1":
            proses_login()
        elif pilihan == "2":
            proses_daftar()
        elif pilihan == "0":
            print("Sampai Jumpa!")
            sys.exit()
        else:
            input("Pilihan tidak valid. Tekan Enter...")

def proses_login():
    """Proses autentikasi user."""
    clear_screen()
    print("--- Form Login ---")
    username = input("Username: ").strip()
    password = input("Password: ").strip()
    
    # Ambil data dari database (Returns Dict)
    data_user = database.muat_data_pengguna()
    
    # Logika Login Sederhana (Dictionary lookup O(1))
    # Gunakan lower() saat lookup agar case-insensitive
    user = data_user.get(username.lower())
    
    if user and user['password'] == password:
        # Gunakan nama asli dari database untuk greeting
        nama_sesi = user.get('nama_asli', username) 
        tipe = user['tipe_pengguna'].lower()
        
        if tipe == 'admin':
            menu_admin(nama_sesi)
        elif tipe == 'petani':
            menu_petani(nama_sesi)
        elif tipe == 'pembeli':
            menu_pembeli(nama_sesi, user.get('tipe_pembeli'))
        else:
            print("Tipe akun tidak dikenali.")
            input("Enter...")
    else:
        print("Username atau Password salah!")
        input("Tekan Enter untuk mencoba lagi...")

def proses_daftar():
    """Proses registrasi user baru."""
    clear_screen()
    print("--- Daftar Akun Baru ---")
    
    # Validasi Username
    data_user = database.muat_data_pengguna()
    while True:
        username = input("Username baru: ").strip()
        if len(username) < 4:
            print("Username minimal 4 karakter.")
            continue
        # Cek duplikasi secara case-insensitive
        if username.lower() in data_user:
            print("Username sudah dipakai!")
            continue
        break
        
    password = input("Password: ").strip()
    
    print("\nPilih Peran:")
    print("1. Petani")
    print("2. Pembeli")
    peran_input = input("Pilih (1/2): ")
    
    tipe_pengguna = "petani" if peran_input == "1" else "pembeli"
    tipe_pembeli = ""
    
    if tipe_pengguna == "pembeli":
        print("\nTipe Pembeli:")
        print("1. Anak Kosan (Tidak ada diskon)")
        print("2. Pembeli Warungan (Diskon 5%)")
        print("3. Pelaku Industri (Diskon 10%)")
        tipe_input = input("Pilih tipe: ")
        mapping = {"1": "Anak Kosan", "2": "Pembeli Warungan", "3": "Pelaku Industri"}
        tipe_pembeli = mapping.get(tipe_input, "Anak Kosan")
    
    database.simpan_pengguna_baru(username, password, tipe_pengguna, tipe_pembeli)
    print("Pendaftaran Berhasil! Silakan Login.")
    input("Tekan Enter...")

# Menu Admin
def menu_admin(username: str):
    while True:
        clear_screen()
        print(f"Halo, Admin {username}!")
        print("1. Tambah Barang")
        print("2. Lihat Semua Transaksi")
        print("3. Analisis Barang (Fast/Slow Moving)")
        print("4. Lihat Stok Barang")
        print("0. Logout")
        
        pilihan = input("Pilih menu: ")
        
        if pilihan == "1":
            admin_tambah_barang()
        elif pilihan == "2":
            admin_lihat_transaksi()
        elif pilihan == "3":
            admin_analisis_barang()
        elif pilihan == "4":
            tampilkan_daftar_barang(database.muat_data_produk())
            input("Enter untuk kembali...")
        elif pilihan == "0":
            break

def admin_tambah_barang():
    clear_screen()
    print("--- Tambah Barang Baru ---")
    nama = input("Nama Barang: ").strip()
    stok = validasi_input_angka("Stok Awal: ")
    harga = validasi_input_angka("Harga Satuan: ")
    penjual = input("Nama Penjual (Petani): ").strip()
    
    # Generate ID Sederhana (Max ID + 1)
    produk_list = database.muat_data_produk()
    if not produk_list:
        new_id = 1
    else:
        # List comprehension untuk ambil semua ID
        ids = [int(p['id_barang']) for p in produk_list]
        new_id = max(ids) + 1
        
    database.simpan_produk(str(new_id), nama, stok, harga, penjual)
    print(f"Barang berhasil disimpan dengan ID {new_id}")
    input("Enter...")

def admin_lihat_transaksi():
    clear_screen()
    transaksi = database.muat_transaksi()
    if not transaksi:
        print("Belum ada transaksi.")
    else:
        tampilkan_stack_riwayat(transaksi) # Pakai Stack Helper
    input("Enter...")

def admin_analisis_barang():
    clear_screen()
    print("--- Analisis Penjualan ---")
    transaksi = database.muat_transaksi()
    produk = database.muat_data_produk()
    
    # Hitung jumlah terjual per barang manual (Procedural Logic)
    terjual_counter = {} # Dict untuk menghitung
    for t in transaksi:
        nama = t['nama_barang']
        jumlah = t['jumlah']
        if nama in terjual_counter:
            terjual_counter[nama] += jumlah
        else:
            terjual_counter[nama] = jumlah
            
    print("\n[Fast Moving - Terjual > 5]")
    headers = ["Nama Barang", "Total Terjual"]
    fast = [[k, v] for k, v in terjual_counter.items() if v > 5]
    print(tabulate(fast, headers=headers))
    
    print("\n[Slow Moving - Terjual <= 5]")
    slow = [[k, v] for k, v in terjual_counter.items() if v <= 5]
    print(tabulate(slow, headers=headers))
    input("Enter...")

# Menu Pembeli
def menu_pembeli(username: str, tipe_pembeli: str):
    while True:
        clear_screen()
        print(f"Halo, {username} ({tipe_pembeli})")
        print("1. Lihat & Cari Barang")
        print("2. Beli Barang (Masuk Keranjang)")
        print("3. Lihat Keranjang & Checkout")
        print("4. Cek Saldo & Top Up")
        print("5. Riwayat Pembelian")
        print("0. Logout")
        
        pilihan = input("Pilih: ")
        
        if pilihan == "1":
            pembeli_lihat_barang(tipe_pembeli)
        elif pilihan == "2":
            pembeli_beli_barang(username, tipe_pembeli)
        elif pilihan == "3":
            pembeli_checkout(username)
        elif pilihan == "4":
            pembeli_saldo(username)
        elif pilihan == "5":
            pembeli_riwayat(username)
        elif pilihan == "0":
            break

def tampilkan_daftar_barang(data_barang: List[Dict], tipe_pembeli: str = ""):
    """Helper untuk menampilkan tabel barang dengan harga diskon."""
    tabel_view = []
    for p in data_barang:
        harga_asli = p['harga']
        harga_final = hitung_diskon_pembeli(harga_asli, tipe_pembeli)
        
        tabel_view.append([
            p['id_barang'],
            p['nama_barang'],
            p['stok'],
            format_rupiah(harga_asli),
            format_rupiah(harga_final),
            p['penjual']
        ])
    
    print(tabulate(tabel_view, headers=["ID", "Nama", "Stok", "Harga Dasar", "Harga Kamu", "Penjual"], tablefmt="fancy_grid"))

def pembeli_lihat_barang(tipe_pembeli: str):
    clear_screen()
    produk = database.muat_data_produk()
    if not produk:
        print("Barang kosong.")
        input("Enter...")
        return
        
    print("Opsi Pengurutan:")
    print("1. ID (Default)")
    print("2. Harga Termurah (Bubble Sort Ascending)")
    print("3. Harga Termahal (Bubble Sort Descending)")
    sort_opsi = input("Pilih: ")
    
    if sort_opsi == "2":
        produk = bubble_sort(produk, "harga", descending=False)
    elif sort_opsi == "3":
        produk = bubble_sort(produk, "harga", descending=True)
        
    tampilkan_daftar_barang(produk, tipe_pembeli)
    input("Enter...")

def pembeli_beli_barang(username: str, tipe_pembeli: str):
    clear_screen()
    print("--- Beli Barang ---")
    produk = database.muat_data_produk()
    
    # Tampilkan dulu
    tampilkan_daftar_barang(produk, tipe_pembeli)
    
    target_id = input("\nMasukkan ID Barang yang mau dibeli: ").strip()
    
    # Gunakan BINARY SEARCH untuk mencari ID (Algoritma Requirement)
    # Binary search butuh data terurut
    while True:
        target_id_input = input("\nMasukkan ID Barang yang mau dibeli (atau '0' untuk kembali): ").strip()
        if not target_id_input:
            print("ID Barang tidak boleh kosong!")
            continue
        if target_id_input == '0':
            return
        if not target_id_input.isdigit():
             print("ID Barang harus berupa angka!")
             continue
        break

    barang_ditemukan = binary_search(produk, target_id_input)
    
    if barang_ditemukan:
        print(f"\nDitemukan: {barang_ditemukan['nama_barang']}")
        stok_tersedia = barang_ditemukan['stok']
        harga_satuan = hitung_diskon_pembeli(barang_ditemukan['harga'], tipe_pembeli)
        
        jumlah = validasi_input_angka("Mau beli berapa? ")
        
        if jumlah > stok_tersedia:
            print("Stok tidak cukup!")
        else:
            total = jumlah * harga_satuan
            print(f"Total: {format_rupiah(total)}")
            confirm = input("Masukan ke keranjang? (y/n): ")
            if confirm.lower() == 'y':
                database.tambah_ke_keranjang(
                    username, 
                    barang_ditemukan['id_barang'], 
                    barang_ditemukan['nama_barang'], 
                    int(jumlah), 
                    harga_satuan, 
                    total, 
                    barang_ditemukan['penjual']
                )
                print("Berhasil masuk keranjang!")
    else:
        print("ID Barang tidak ditemukan (Binary Search returned None).")
    input("Enter...")

def pembeli_checkout(username: str):
    clear_screen()
    keranjang = database.muat_keranjang(username)
    if not keranjang:
        print("Keranjang kosong.")
        input("Enter...")
        return
        
    total_tagihan = sum(item['total_harga'] for item in keranjang)
    saldo_user = database.ambil_saldo(username)
    
    print("--- Keranjang Belanja ---")
    # Tampilkan keranjang manual
    data_tabel = [[k['nama_barang'], k['jumlah'], format_rupiah(k['total_harga'])] for k in keranjang]
    print(tabulate(data_tabel, headers=["Barang", "Jml", "Total"]))
    
    print(f"\nTotal Tagihan: {format_rupiah(total_tagihan)}")
    print(f"Saldo Kamu : {format_rupiah(saldo_user)}")
    
    if saldo_user < total_tagihan:
        print("Saldo kurang! Silakan Top Up dulu.")
    else:
        konfirmasi = input("Bayar sekarang? (y/n): ")
        if konfirmasi.lower() == 'y':
            try:
                # 1. Kurangi Stok (Validasi stok lagi)
                for item in keranjang:
                    database.update_stok_produk(item['id_barang'], -item['jumlah'])
                
                # 2. Kurangi Saldo
                database.update_saldo(username, -total_tagihan)
                
                # 3. Simpan Transaksi & Bersihkan Keranjang
                database.tambah_transaksi(keranjang)
                database.bersihkan_keranjang(username)
                
                print("Checkout Berhasil! Terima kasih.")
            except ValueError as e:
                print(f"Gagal Checkout: {e}")
                
    input("Enter...")

def pembeli_saldo(username: str):
    clear_screen()
    saldo = database.ambil_saldo(username)
    print(f"Saldo Saat Ini: {format_rupiah(saldo)}")
    print("\n1. Top Up")
    print("0. Kembali")
    pilih = input("Pilih: ")
    if pilih == "1":
        jumlah = validasi_input_angka("Nominal Top Up: ")
        database.update_saldo(username, jumlah)
        print("Top Up Berhasil!")
        input("Enter...")

def pembeli_riwayat(username: str):
    clear_screen()
    transaksi = database.muat_transaksi(username)
    if not transaksi:
        print("Belum ada riwayat.")
    else:
        print("--- Riwayat Belanja (Tumpukan/Stack) ---")
        tampilkan_stack_riwayat(transaksi)
    input("Enter...")

# Menu Petani (Simplified)
def menu_petani(username: str):
    while True:
        clear_screen()
        print(f"Halo, Petani {username}!")
        print("1. Kelola Barang Saya")
        print("0. Logout")
        pilih = input("Pilih: ")
        if pilih == "1":
            # Reuse fungsi admin tp filter by penjual (Untuk simplifikasi kita pakai logic admin tambah barang)
            admin_tambah_barang() 
        elif pilih == "0":
            break

if __name__ == "__main__":
    try:
        login()
    except KeyboardInterrupt:
        print("\nProgram dihentikan.")