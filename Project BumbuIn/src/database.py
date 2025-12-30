import csv
import os
from typing import List, Dict, Any, Union

# Kita menggunakan path absolut agar tidak bingung saat dijalankan dari folder mana saja
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FOLDER_DATA = os.path.join(BASE_DIR, "data")


FILE_PENGGUNA = os.path.join(FOLDER_DATA, "users.csv")
FILE_PRODUK = os.path.join(FOLDER_DATA, "products.csv")
FILE_TRANSAKSI = os.path.join(FOLDER_DATA, "transactions.csv")
FILE_SALDO = os.path.join(FOLDER_DATA, "balances.csv")
FILE_KERANJANG = os.path.join(FOLDER_DATA, "cart.csv")

def inisialisasi_file_csv():
    """
    Membuat folder data dan file CSV kosong jika belum ada.
    Ini penting agar program tidak error saat pertama kali dijalankan.
    """
    os.makedirs(FOLDER_DATA, exist_ok=True)
    
    # Daftar file dan header kolomnya
    daftar_file = {
        FILE_PENGGUNA: ["username", "password", "tipe_pengguna", "tipe_pembeli"],
        FILE_PRODUK: ["id_barang", "nama_barang", "stok", "harga", "penjual"],
        FILE_TRANSAKSI: ["username", "id_barang", "nama_barang", "jumlah", "harga", "total_harga", "penjual"],
        FILE_SALDO: ["username", "saldo"],
        FILE_KERANJANG: ["username", "id_barang", "nama_barang", "jumlah", "harga", "total_harga", "penjual"]
    }

    for path_file, header in daftar_file.items():
        if not os.path.exists(path_file):
            with open(path_file, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(header)
            print(f"[INFO] File dibuat: {path_file}")

def muat_csv(path_file: str) -> List[Dict[str, str]]:
    """
    Membaca file CSV dan mengembalikannya sebagai List of Dictionaries.
    Contoh output: [{'nama': 'Budi', 'umur': '10'}, ...]
    """
    data = []
    if os.path.exists(path_file):
        with open(path_file, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for baris in reader:
                data.append(dict(baris))
    return data

def simpan_csv(path_file: str, data: List[Dict[str, Any]], fieldnames: List[str]):
    """
    Menyimpan List of Dictionaries kembali ke file CSV.
    Ini akan menimpa (overwrite) isi file lama dengan data baru.
    """
    with open(path_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

def tambah_ke_csv(path_file: str, data_baru: Dict[str, Any], fieldnames: List[str]):
    """
    Menambahkan satu baris data baru ke file CSV (Append).
    """
    with open(path_file, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        # Jika file kosong (size 0), tulis header dulu
        if os.path.getsize(path_file) == 0:
            writer.writeheader()
        writer.writerow(data_baru)

# Manajemen Pengguna (User Management)
def muat_data_pengguna() -> Dict[str, Dict[str, str]]:
    """
    Mengambil data pengguna dan mengubahnya menjadi Dictionary agar mudah dicari.
    Format: {'username': {'password': '...', 'tipe': '...'}}
    """
    daftar_pengguna = muat_csv(FILE_PENGGUNA)
    data_dict = {}
    for pengguna in daftar_pengguna:
        # Normalisasi key agar konsisten (huruf kecil semua untuk key internal)
        username = pengguna.get("username") or pengguna.get("Username")
        if username:
            username = username.strip() # Case sensitive username preservation
        # Mapping nama kolom csv lama ke nama internal baru jika perlu
        # Kita asumsikan CSV sudah bersih, tapi untuk jaga-jaga:
        password = pengguna.get("password") or pengguna.get("Password")
        tipe = pengguna.get("tipe_pengguna") or pengguna.get("Tipe Pengguna")
        pembeli = pengguna.get("tipe_pembeli") or pengguna.get("Tipe Pembeli")
        
        if username:
            data_dict[username] = {
                "password": str(password),
                "tipe_pengguna": str(tipe),
                "tipe_pembeli": str(pembeli) if pembeli else ""
            }
    return data_dict

def simpan_pengguna_baru(username: str, password: str, tipe_pengguna: str, tipe_pembeli: str = ""):
    """Menyimpan pengguna baru ke database."""
    # Cek duplikasi dilakukan di main.py, di sini langsung simpan
    data_baru = {
        "username": username,
        "password": password,
        "tipe_pengguna": tipe_pengguna,
        "tipe_pembeli": tipe_pembeli
    }
    tambah_ke_csv(FILE_PENGGUNA, data_baru, ["username", "password", "tipe_pengguna", "tipe_pembeli"])

def perbarui_pengguna(username_target: str, data_baru: Dict[str, str]):
    """Memperbarui data pengguna yang sudah ada."""
    semua_pengguna = muat_csv(FILE_PENGGUNA)
    for pengguna in semua_pengguna:
        if pengguna["username"] == username_target:
            pengguna.update(data_baru)
    
    # Simpan ulang semua
    simpan_csv(FILE_PENGGUNA, semua_pengguna, ["username", "password", "tipe_pengguna", "tipe_pembeli"])

def hapus_pengguna(username_target: str):
    """Menghapus pengguna dari database."""
    semua_pengguna = muat_csv(FILE_PENGGUNA)
    # Filter: Ambil semua KECUALI yang username-nya target
    pengguna_sisa = [p for p in semua_pengguna if p["username"] != username_target]
    simpan_csv(FILE_PENGGUNA, pengguna_sisa, ["username", "password", "tipe_pengguna", "tipe_pembeli"])

# Manajemen Produk (Product Management)
def muat_data_produk() -> List[Dict[str, Any]]:
    """Mengambil semua data produk."""
    produk = muat_csv(FILE_PRODUK)
    # Konversi tipe data angka (karena CSV selalu string)
    for p in produk:
        # Handle kolom lama vs baru
        id_barang = p.get("id_barang")
        nama = p.get("nama_barang")
        stok = p.get("stok") or p.get("Stok")
        harga = p.get("harga")
        penjual = p.get("penjual") or p.get("Penjual")
        
        p["id_barang"] = str(id_barang)
        p["nama_barang"] = str(nama)
        p["stok"] = float(stok) if stok else 0.0
        p["harga"] = float(harga) if harga else 0.0
        p["penjual"] = str(penjual)
    return produk

def simpan_produk(id_barang: str, nama_barang: str, stok: float, harga: float, penjual: str):
    """Menambah atau Memperbarui produk."""
    if stok < 0:
        raise ValueError("Stok tidak boleh negatif")

    semua_produk = muat_data_produk()
    
    # Cek apakah produk sudah ada (Update)
    ditemukan = False
    for p in semua_produk:
        if p["id_barang"] == str(id_barang):
            p["nama_barang"] = nama_barang
            p["stok"] = stok
            p["harga"] = harga
            p["penjual"] = penjual
            ditemukan = True
            break
    
    # Jika tidak ada, tambah baru (Insert)
    if not ditemukan:
        semua_produk.append({
            "id_barang": str(id_barang),
            "nama_barang": nama_barang,
            "stok": stok,
            "harga": harga,
            "penjual": penjual
        })
    
    simpan_csv(FILE_PRODUK, semua_produk, ["id_barang", "nama_barang", "stok", "harga", "penjual"])

def hapus_produk(id_barang: str):
    """Menghapus produk berdasarkan ID."""
    semua_produk = muat_data_produk()
    produk_sisa = [p for p in semua_produk if p["id_barang"] != str(id_barang)]
    simpan_csv(FILE_PRODUK, produk_sisa, ["id_barang", "nama_barang", "stok", "harga", "penjual"])

def update_stok_produk(id_barang: str, perubahan: float):
    """
    Mengupdate stok. 
    perubahan positif = nambah stok
    perubahan negatif = kurangi stok (misal dibeli)
    """
    semua_produk = muat_data_produk()
    ditemukan = False
    for p in semua_produk:
        if p["id_barang"] == str(id_barang):
            stok_baru = p["stok"] + perubahan
            if stok_baru < 0:
                raise ValueError(f"Stok tidak cukup! Sisa: {p['stok']}, Diminta: {abs(perubahan)}")
            p["stok"] = stok_baru
            ditemukan = True
            break
    
    if ditemukan:
        simpan_csv(FILE_PRODUK, semua_produk, ["id_barang", "nama_barang", "stok", "harga", "penjual"])
    else:
        raise ValueError(f"Barang ID {id_barang} tidak ditemukan")


# Manajemen Saldo & Transaksi
def ambil_saldo(username: str) -> float:
    """Mendapatkan saldo terakhir pengguna."""
    data_saldo = muat_csv(FILE_SALDO)
    # Cari entri terakhir untuk username ini (karena kita append terus)
    # Cara paling mudah: loop dari belakang atau filter lalu ambil terakhir
    # Kita pakai cara filter
    milik_user = [s for s in data_saldo if s.get("username", "").upper() == username.upper()]
    if milik_user:
        return float(milik_user[-1]["saldo"])
    return 0.0

def update_saldo(username: str, jumlah: float):
    """Menambah atau mengurangi saldo (log saldo baru)."""
    saldo_sekarang = ambil_saldo(username)
    saldo_baru = saldo_sekarang + jumlah
    
    # Kita simpan row baru (history style) 
    # atau bisa juga overwrite satu baris per user agar file tidak bengkak
    # Untuk project ini, kita overwrite saja agar rapi (sesuai refactor sebelumnya)
    
    semua_saldo = muat_csv(FILE_SALDO)
    # Hapus data lama user ini
    sisa_saldo = [s for s in semua_saldo if s.get("username", "").upper() != username.upper()]
    
    # Tambah data baru
    sisa_saldo.append({"username": username, "saldo": saldo_baru})
    
    simpan_csv(FILE_SALDO, sisa_saldo, ["username", "saldo"])

def muat_keranjang(username: str = None) -> List[Dict[str, Any]]:
    """Memuat data keranjang belanja."""
    semua_keranjang = muat_csv(FILE_KERANJANG)
    
    # Konversi tipe data
    hasil = []
    for item in semua_keranjang:
        item["jumlah"] = int(item["jumlah"])
        item["harga"] = float(item["harga"])
        item["total_harga"] = float(item["total_harga"])
        
        if username:
            if item["username"].upper() == username.upper():
                hasil.append(item)
        else:
            hasil.append(item)
    return hasil

def tambah_ke_keranjang(username, id_barang, nama_barang, jumlah, harga, total_harga, penjual):
    """Menambah barang ke keranjang."""
    item = {
        "username": username,
        "id_barang": id_barang,
        "nama_barang": nama_barang,
        "jumlah": jumlah,
        "harga": harga,
        "total_harga": total_harga,
        "penjual": penjual
    }
    tambah_ke_csv(FILE_KERANJANG, item, ["username", "id_barang", "nama_barang", "jumlah", "harga", "total_harga", "penjual"])

def bersihkan_keranjang(username: str):
    """Menghapus isi keranjang milik username tertentu."""
    semua = muat_csv(FILE_KERANJANG)
    sisa = [item for item in semua if item["username"].upper() != username.upper()]
    simpan_csv(FILE_KERANJANG, sisa, ["username", "id_barang", "nama_barang", "jumlah", "harga", "total_harga", "penjual"])

def muat_transaksi(username: str = None) -> List[Dict[str, Any]]:
    """Memuat riwayat transaksi."""
    transaksi = muat_csv(FILE_TRANSAKSI)
    
    hasil = []
    for t in transaksi:
        t["jumlah"] = int(t["jumlah"])
        t["harga"] = float(t["harga"])
        t["total_harga"] = float(t["total_harga"])
        
        if username:
            if t["username"].upper() == username.upper():
                hasil.append(t)
        else:
            hasil.append(t)
    return hasil

def tambah_transaksi(daftar_item: List[Dict[str, Any]]):
    """Memindahkan item dari keranjang ke riwayat transaksi."""
    # Pastikan format sesuai header
    for item in daftar_item:
        # Kita hanya ambil kolom yang relevan
        transaksi_baru = {
            "username": item["username"],
            "id_barang": item["id_barang"],
            "nama_barang": item["nama_barang"],
            "jumlah": item["jumlah"],
            "harga": item["harga"],
            "total_harga": item["total_harga"],
            "penjual": item["penjual"]
        }
        tambah_ke_csv(FILE_TRANSAKSI, transaksi_baru, ["username", "id_barang", "nama_barang", "jumlah", "harga", "total_harga", "penjual"])

# Inisialisasi saat modul diimpor
inisialisasi_file_csv()
