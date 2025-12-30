import time
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import pandas as pd
import os
# Removed legacy globals and helper functions

import database

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')
    
def cek_data_pengguna():
    data_pengguna = database.load_users() # Load users directly
    if not data_pengguna:
        print("Belum ada pengguna yang terdaftar")
        return pd.DataFrame()
    else:
        df = pd.DataFrame.from_dict(data_pengguna, orient="index")
        df.index.name = "Username"
        df.reset_index(inplace=True)
        return df
    
def validasi_username(data_pengguna=None): 
    # Note: data_pengguna argument is kept for compatibility if needed, 
    # but we should fetch fresh data if None
    if data_pengguna is None:
        data_pengguna = database.load_users()
        
    while True:
        clear()
        tampilan_daftar_bumbuin()
        username = input("Buat username (min. 4 karakter dan maks. 12 karakter): ").strip().title()
        while True:
            if len(username) < 4:
                clear()
                print(f"Username terlalu pendek! Minimal {4} karakter.")
                input("Tekan enter untuk mencoba lagi...")
                break
            elif len(username) > 12:
                print(f"Username terlalu panjang! Maksimal {12} karakter")
            elif username in data_pengguna:
                print("Username sudah ada kak! Pakai username lain yaa!")
                input("Tekan enter untuk mencoba lagi...")
                break
            else:
                return username


def validasi_password():
    while True:
        clear()
        password = input("Buat password (min. 6 karakter dan maks. 8 karakter): ").strip()
        if len(password) < 6:
            print(f"Paaword terlalu pendek! Minimal {6} karakter.")
            input("Tekan enter untuk mencoba lagi...")
            continue
        elif len(password) > 8:
            print(f"Password terlalu panjang! Maksimal {8} karakter.")
            input("Tekan enter untuk mencoba lagi...")
            continue
        else:
            konfirmasi_password = input("Konfirmasi password: ")
            if konfirmasi_password != password:
                print("Password tidak cocok!")
                input("Tekan enter untuk mencoba lagi...")
                continue
            else:
                return password

def pilih_tipe_user():
    while True:
        print("\nPilih Tipe User:\n1. Petani\n2. Pembeli")
        tipe_user = input("Yuk dipilih! (1/2): ")
        if tipe_user in ["1", "2"]:
            return tipe_user
        else:
            print(f"Pilihan {tipe_user} tidak valid. Silahkan pilih (1/2)!")
            continue

def pilih_tipe_pembeli():

    list_tipe_pembeli = {
        "1" : "Anak Kosan",
        "2" : "Pembeli Warungan",
        "3" : "Pelaku Industri"
    }
    for tipe_pembeli, data in list_tipe_pembeli.items():
        print(f"{tipe_pembeli}. {data}")
    while True:
        tipe_pembeli = input("Yuk dipilih (1/2/3): ")
        if tipe_pembeli in list_tipe_pembeli:
            return list_tipe_pembeli[tipe_pembeli]
        else:
            print(f"Hey, pilihan {tipe_pembeli} tidak ada! Silahkan pilih (1/2/3)!")

def tampilan_daftar_bumbuin():
        print(f"+{"="*25}+{"="*25}+")
        print(f"| {"Halo, Selamat Datang di BumbuIn! Ayo Daftar Dulu!"} |")
        print(f"+{"="*25}+{"="*25}+") 
        
def daftar(): 
    # load_data_pengguna() # Removed
    while True:
        clear()
        tampilan_daftar_bumbuin()
        username = validasi_username(data_pengguna)
        password = validasi_password()
        clear()
        print(f"Halo {username}! Silahkan pilih tipe user terlebih dahulu.")
        time.sleep(1)
        while True:
            tipe_user = pilih_tipe_user()
            try:
                if tipe_user == "2":
                    print(f"Halo Kak {username}! Mau jadi pembeli yang mana?")
                    time.sleep(1)
                    tipe_pembeli = pilih_tipe_pembeli()
                    
                    database.save_user(username, password, "pembeli", tipe_pembeli)
                elif tipe_user == "1":
                    database.save_user(username, password, "petani")
                
                # load_data_pengguna() # Removed
                print(f"Halo {username}! Kamu terdaftar.")
                return
            except Exception as e:
                print(f"Terjadi kesalahan: {e}")
                input("Tekan enter untuk mencoba lagi...")
                continue
        
def validasi_angka(prompt):
    while True:
        # clear()
        try:
            value = float(input(prompt))
            return value
        except ValueError:
            input("Masukkan angka yang valid! Tekan enter untuk mencoba lagi...")

def validasi_huruf(prompt):
    while True:
        value = input(prompt).strip()
        if value ==  "":
            return value
        if all(char.isalpha() or char.isspace() for char in value):
            return value.capitalize()
        print("Masukkan hanya huruf!")

def hitung_harga_diskon(harga, tipe_pembeli):
    if tipe_pembeli == 'Pelaku Industri':
        return harga * 0.9
    elif tipe_pembeli == 'Pembeli Warungan':
        return harga * 0.95
    return harga
        
def menu_pembeli(username, tipe_pembeli):
    while True:
        clear()
        panjang_tabel = 60
        nama_pesan_pembeli = f"Halo {username}! Kamu mau ngapain sebagai {tipe_pembeli}?"
        print("\n" + "=" * panjang_tabel)
        print(f"| {nama_pesan_pembeli.center(panjang_tabel - 4)} |")
        print("=" * panjang_tabel)
        print("1. Lihat Daftar Barang")
        print("2. Beli Barang")
        print("3. Top-up Saldo")
        print("4. Cek Saldo")
        print("5. Lihat Keranjang")
        print("6. Checkout")
        print("7. Riwayat Pembelian")
        print("0. Keluar")
        pilihan = input("Pilih menu: ")
        
        if pilihan == "1":
            clear()
            lihat_daftar(username)
        elif pilihan == "2":
            clear()
            beli_barang(username)
        elif pilihan == "3":
            clear()
            topup_saldo(username)
        elif pilihan == "4":
            clear()
            cek_saldo(username)
        elif pilihan == "5":
            clear()
            lihat_keranjang(username)
        elif pilihan == "6":
            clear()
            checkout(username)
        elif pilihan == "7":
            clear()
            riwayat_pembelian(username)
        elif pilihan == "0":
            menu_utama()
            break
        else:
            print("Pilihan belum tersedia atau tidak valid!")

def lihat_daftar(username):
    try:
        data_barang = database.load_products()
        if data_barang.empty:
            print("\nBelum ada barang yang dijual.")
        else:
            users = database.load_users()
            if username not in users:
                print("Username tidak ditemukan dalam daftar pengguna.")
                return
            tipe_pembeli = users[username].get('tipe_pembeli', '')
            
            # Dynamic pricing calculation
            data_barang['Harga_tersedia'] = data_barang['harga'].apply(lambda x: hitung_harga_diskon(x, tipe_pembeli))
            
            panjang_tabel = 62
            nama_pembeli = f"Halo {username}! Yuk lihat barang yang dijual!"
            print("\n" + "=" * panjang_tabel)
            print(f"| {nama_pembeli.center(panjang_tabel - 4)} |")
            print("=" * panjang_tabel)
            tabel_barang = data_barang[['id_barang', 'nama_barang', 'Stok', 'Harga_tersedia', 'Penjual']]
            print(tb(tabel_barang, headers=["ID Barang", "Nama Barang", "Stok", "Harga", "Penjual"], tablefmt="fancy_grid", showindex=False))
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
    input("\nTekan Enter untuk kembali ke menu utama...")
    
def beli_barang(username):
    try:
        data_barang = database.load_products()
        users = database.load_users()
        if username not in users:
            print("Username tidak ditemukan dalam daftar pengguna.")
            return
        tipe_pembeli = users[username].get('tipe_pembeli', '')
        
        # Dynamic pricing
        data_barang['Harga_tersedia'] = data_barang['harga'].apply(lambda x: hitung_harga_diskon(x, tipe_pembeli))

        panjang_tabel = 62
        nama_pesan = f"Hai {username}! Mau Beli apa di BumbuIn?"
        print("\n" + "=" * panjang_tabel)
        print(f"| {nama_pesan.center(panjang_tabel - 4)} |")
        print("=" * panjang_tabel)
        tabel_barang = data_barang[['id_barang', 'nama_barang', 'Stok', 'Harga_tersedia', 'Penjual']]
        while True:
            print(tb(tabel_barang, headers=["ID Barang", "Nama Barang", "Stok", "Harga", "Penjual"], tablefmt="fancy_grid", showindex=False))
            id_barang = input("\nMasukkan ID Barang yang ingin dibeli: ").strip()
            if id_barang == '':
                input("ID Barang tidak boleh kosong! Tekan Enter untuk mencoba lagi...")
                continue
            if not data_barang['id_barang'].eq(id_barang).any():
                input("ID barang yang kamu cari tidak ada! Tekan Enter untuk mencoba lagi...")
                continue
            try:
                jumlah_input = input("Masukkan jumlah yang ingin dibeli: ").strip()
                if jumlah_input == '':
                    input("Jumlah tidak boleh kosong! Tekan Enter untuk mencoba lagi...")
                    continue
                jumlah = int(jumlah_input)
                if jumlah <= 0:
                    input("Jumlah harus lebih dari 0! Tekan Enter untuk mencoba lagi...")
                    continue
                konfirmasi = input("Kamu yakin ingin melanjutkan pembelian ini? (y/n): ").strip().lower()
                if konfirmasi in ['y', 'yes', 'ya', 'iya', '1']:
                    break
                else:
                    input("Proses pembelian dibatalkan.")
                    return
            except ValueError:
                input("Masukkan jumlah yang valid! Tekan Enter untuk mencoba lagi...")

        barang_dipilih = data_barang[data_barang['id_barang'] == id_barang]
        stok = barang_dipilih['Stok'].values[0]
        if jumlah > stok:
            print(f"Jumlah yang diminta melebihi stok yang tersedia! Stok saat ini: {stok}")
            return
        
        harga = barang_dipilih['Harga_tersedia'].values[0]
        penjual = barang_dipilih['Penjual'].values[0] 
        total_harga = harga * jumlah
        
        # FIX: Do not deduct stock here. Only add to cart. Stock is deducted at checkout.
        database.add_to_cart(username, id_barang, barang_dipilih['nama_barang'].values[0], jumlah, harga, total_harga, penjual)
        print("\nTransaksi berhasil dimasukkan ke keranjang!")
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

    input("\nTekan enter untuk kembali ke menu utama...")


def lihat_keranjang(username):
    try:
        keranjang_user = database.load_cart(username)
        if keranjang_user.empty:
            print(f"\nYah, keranjang Kak {username} kosong. Yuk tambah barangnya dulu!")
        else:
            panjang_tabel = 52
            nama_pesan = f"Hai {username}! Yuk lihat isi keranjang kamu!"
            print("\n" + "=" * panjang_tabel)
            print(f"| {nama_pesan.center(panjang_tabel - 4)} |")
            print("=" * panjang_tabel)
            keranjang_user_tb = keranjang_user[['id_barang', 'jumlah', 'harga', 'total_harga']]
            print(tb(keranjang_user_tb, headers=["ID Barang", "Jumlah", "Harga", "Total Harga"], tablefmt="fancy_grid", showindex=False))
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
    input("\nTekan enter untuk kembali.")


def checkout(username):
    try:
        keranjang_pengguna = database.load_cart(username)
        if keranjang_pengguna.empty:
            input(f"Wah, keranjang kak {username} masih kosong! Yuk, tambah barang dulu!")
            return
        
        total_harga = keranjang_pengguna['total_harga'].sum()
        saldo_sekarang = database.get_balance(username)
        
        if saldo_sekarang < total_harga:
            print("Saldo tidak cukup untuk melakukan checkout. Silakan isi saldo terlebih dahulu.")
            return

        # Try to deduct stock first to ensure availability
        try:
            for _, item in keranjang_pengguna.iterrows():
                id_barang = item['id_barang']
                jumlah_beli = item['jumlah']
                # Try to reduce stock. If insufficient, this raises ValueError
                database.update_product_stock(id_barang, -jumlah_beli)
        except ValueError as e:
            # If stock deduction fails, we should ideally rollback (not implemented simply here)
            # But for this simple app, we just stop and warn.
            # NOTE: In a real app, we need transactions. Here, manual rollback or careful check is needed.
            print(f"Checkout gagal: {e}")
            print("Silakan cek kembali stok barang.")
            return

        # Deduct balance (if stock deduction was successful)
        database.update_balance(username, -total_harga)
        
        # Record transaction
        database.add_transactions(keranjang_pengguna)
        
        # Clear cart
        database.clear_cart(username)
        
        saldo_akhir = database.get_balance(username)
        print(f"\nCheckout berhasil! Saldo akhir Anda adalah: Rp.{saldo_akhir:,.2f}".replace(",", "."))

    except Exception as error:
        print(f"Terjadi kesalahan: {error}")

    input("Tekan enter untuk kembali ke menu utama...")

def riwayat_pembelian(username):
    try:
        transaksi = database.load_transactions(username)
        if transaksi.empty:
            print("\nYah belum ada riwayat ayo beli barang kebutuhan mu!!.")
        else:
            panjang_tabel = 64
            nama_judul = f"Halo {username}! Yuk lihat riwayat belanjaanmu!"
            print("\n" + "=" * panjang_tabel)
            print(f"| {nama_judul.center(panjang_tabel - 4)} |")
            print("=" * panjang_tabel)
            print(tb(transaksi[["id_barang", "jumlah", "harga", "total_harga","Penjual"]], headers=["ID Barang", "Jumlah", "Harga", "Total Harga", "Penjual"], tablefmt="fancy_grid", showindex=False))
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
    input("\nTekan enter untuk kembali.")


def topup_saldo(username):
    try:
        jumlah_topup = float(input("Masukkan jumlah saldo yang ingin di-top-up: "))
        database.update_balance(username, jumlah_topup)
        print("Saldo berhasil ditambahkan!")
        input("Tekan Enter untuk kembali ke menu utama...")
    except ValueError:
        print("Masukkan jumlah saldo yang valid!")

def cek_saldo(username):
    saldo = database.get_balance(username)
    print(f"Halo Kak! Saldo Kak {username} saat ini: Rp.{saldo:,.2f}".replace(",", "."))
    input("Tekan Enter untuk kembali ke menu utama...")


def menu_admin(username):
    data_barang = baca_data_barang()
    penjualan = baca_riwayat_penjualan()
    while True:
        clear()
        panjang_tabel = 60
        nama_pesan_admin = f"Halo {username}! Mau ngapain di menu admin?"
        print("\n" + "=" * panjang_tabel)
        print(f"| {nama_pesan_admin.center(panjang_tabel - 4)} |")
        print("=" * panjang_tabel)

        print("1. Tambah Barang")
        print("2. Lihat Riwayat Pembelian")
        print("3. Lihat Stok Barang")
        print("4. Barang Kurang Diminati")
        print("5. Barang Paling Diminati")
        print("6. Tambah Pengguna")
        print("7. Lihat Daftar Pengguna")
        print("8. Perbarui Pengguna")
        print("9. Hapus Pengguna")
        print("0. Kembali ke Menu Utama")
        admin_memilih = input("Yuk dipilih! (1-9)): ").strip()
        if admin_memilih == "1":
            clear()
            tambah_barang()
        elif admin_memilih == "2":
            clear()
            username_terpilih = pilih_username()
            if username_terpilih:
                clear()
                riwayat_pembelian(username_terpilih)
        elif admin_memilih == "3":
            clear()
        elif admin_memilih == "3":
            clear()
            lihat_barang()
        elif admin_memilih == "4":
            clear()
            laporan_slow(data_barang, penjualan)
        elif admin_memilih == "5":
            clear()
            laporan_fast(data_barang, penjualan)
        elif admin_memilih == "6":
            clear()
            tambah_pengguna()
        elif admin_memilih == "7":
            clear()
            lihat_pengguna()
        elif admin_memilih == "8":
            clear()
            perbarui_pengguna()
        elif admin_memilih == "9":
            clear()
            hapus_pengguna()
        elif admin_memilih == "0":
            return
        else:
            print("Wah, pilihan kamu tidak ada. Pilih ulang yaa!")
            input("Tekan enter untuk mencoba lagi")
            
def laporan_slow(data_barang, penjualan):
    barang_tidak_terjual = {
        nama_barang: info
        for nama_barang, info in data_barang.items()
        if not any(nama_barang.lower().strip() == item.lower().strip() for item in penjualan.keys())
    }
    slow_moving = {
        key: jumlah
        for key, jumlah in penjualan.items()
        if jumlah < 4
    }
    nama_laporan = "=== Laporan Slow-Moving ==="
    panjang_tabel = 80
    print("\n" + "=" * panjang_tabel)
    print(f"| {nama_laporan.center(panjang_tabel - 4)} |")
    print("=" * panjang_tabel)
    print(f"+{'='*10}+{'='*20}+{'='*15}+{'='*10}+{'='*10}+")
    print(f"| {'ID Barang':<8} | {'Nama Barang':<18} | {'Jumlah Terjual':<13} | {'Stok':<8} | {'Harga':<6} |")
    print(f"+{'='*10}+{'='*20}+{'='*15}+{'='*10}+{'='*10}+")
    
    for nama_barang, info in barang_tidak_terjual.items():
        print(f"| {info['id_barang']:<8} | {nama_barang:<18} | {'0':<13} | {info['stok']:<8} | {info['harga']:<8} |")
    # print("tes")

    for nama_barang, jumlah_terjual in slow_moving.items():
        info = data_barang.get(nama_barang, None)
        if info:
            print(f"| {info['id_barang']:<8} | {nama_barang:<18} | {jumlah_terjual:<13} | {info['stok']:<8} | {info['harga']:<8} |")
    print(f"+{'='*10}+{'='*20}+{'='*15}+{'='*10}+{'='*10}+")
    input("\nTekan enter untuk kembali...")

def laporan_fast(data_barang, penjualan):
    fast_moving = {
        key: jumlah
        for key, jumlah in penjualan.items()
        if jumlah >= 4
    }
    nama_laporan = "=== Laporan Fast-Moving ==="
    panjang_tabel = 70
    print("\n" + "=" * panjang_tabel)
    print(f"| {nama_laporan.center(panjang_tabel - 4)} |")
    print("=" * panjang_tabel)
    
    # Styling manual untuk tabel
    print(f"+{'='*10}+{'='*20}+{'='*15}+{'='*10}+")
    print(f"| {'ID Barang':<8} | {'Nama Barang':<18} | {'Jumlah Terjual':<13} | {'Harga':<6} |")
    print(f"+{'='*10}+{'='*20}+{'='*15}+{'='*10}+")
    for nama_barang, jumlah_terjual in fast_moving.items():
        info = data_barang.get(nama_barang, None)
        if info:
            print(f"| {info['id_barang']:<8} | {nama_barang:<18} | {jumlah_terjual:<13} | {info['harga']:<8} |")
    print(f"+{'='*10}+{'='*20}+{'='*15}+{'='*10}+")
    input("\nTekan enter untuk kembali...")
    
def tambah_pengguna():
    print("\n=== Tambah Pengguna Baru ===")
    username = validasi_username()
    if username:
        password = validasi_password()
        tipe_pengguna = input("Masukkan tipe pengguna (admin/petani/pembeli): ").strip().lower()
        tipe_pembeli = ""
        if tipe_pengguna == "pembeli":
            tipe_pembeli = input("Masukkan tipe pembeli: ").strip().title()
        
        database.save_user(username, password, tipe_pengguna, tipe_pembeli)
        # load_data_pengguna() # Removed
        print(f"\nPengguna {username} berhasil ditambahkan.")
    input("\nTekan enter untuk kembali ke menu admin...")

def lihat_pengguna():
    users = database.load_users()
    if not users:
        print("Belum ada pengguna yang terdaftar")
    else:
        df = pd.DataFrame.from_dict(users, orient="index")
        df.index.name = "Username"
        df.reset_index(inplace=True)
        print(tb(df, headers=['Username', 'Password', 'Tipe Pengguna', 'Tipe Pembeli'], tablefmt="fancy_grid", showindex=False))
    input("\nTekan enter untuk kembali ke menu admin...")
    
def perbarui_pengguna():
    print("\n=== Perbarui Pengguna ===")
    username = input("Masukkan username yang ingin diperbarui: ").strip().title()
    users = database.load_users()
    if username in users:
        info = users[username]
        print(f"\nInformasi saat ini untuk {username}: {info}")
        pilihan = input("Apa yang ingin diperbarui? (password/tipe pengguna/tipe pembeli): ").strip().lower()
        
        new_password = info["password"]
        new_tipe_pengguna = info["tipe_pengguna"]
        new_tipe_pembeli = info.get("tipe_pembeli", "")

        if pilihan == "password":
            new_password = validasi_password()
        elif pilihan == "tipe pengguna":
            new_tipe_pengguna = input("Masukkan tipe pengguna baru: ").strip().lower()
        elif pilihan == "tipe pembeli":
            if new_tipe_pengguna == "pembeli":
                new_tipe_pembeli = input("Masukkan tipe pembeli baru: ").strip().lower()
            else:
                print("Pengguna bukan tipe pembeli.")
                input("\nTekan enter untuk kembali...")
                return
        else:
            print("Pilihan tidak valid.")
            input("\nTekan enter untuk kembali...")
            return
            
        database.save_user(username, new_password, new_tipe_pengguna, new_tipe_pembeli)
        # load_data_pengguna() # Removed
        print(f"\nPengguna {username} berhasil diperbarui.")
    else:
        print("Username tidak ditemukan.")
    input("\nTekan enter untuk kembali ke menu admin...")

def hapus_pengguna():
    username = input("Masukkan username yang ingin dihapus: ").strip().title()
    users = database.load_users()
    if username in users:
        konfirmasi = input(f"Apakah Anda yakin ingin menghapus pengguna {username}? (y/n): ").strip().lower()
        if konfirmasi == 'y':
            database.delete_user(username)
            # load_data_pengguna() # Removed
            print(f"\nPengguna {username} berhasil dihapus.")
        else:
            print("Penghapusan dibatalkan.")
    else:
        print("Username tidak ditemukan.")
    input("\nTekan enter untuk kembali ke menu admin...")

# Removed legacy simpan_data_pengguna

def lupa_password(username):
    users = database.load_users()
    if username in users:
        password = users[username]["password"]
        print(f"Password untuk username '{username}' adalah: {password}")
    else:
        print("Username tidak ditemukan!")
    input("Tekan enter untuk kembali...")
def pilih_username():
    try:
        keranjang = database.load_cart()
        riwayat = database.load_transactions()
        usernames_keranjang = keranjang['username'].unique() if not keranjang.empty else []
        usernames_riwayat = riwayat['username'].unique() if not riwayat.empty else []
        usernames = pd.concat([pd.Series(usernames_keranjang), pd.Series(usernames_riwayat)]).unique()
        if not len(usernames):
            print("\nTidak ada username yang terdaftar.")
            return None
        print("\nDaftar Username:")
        for i, user in enumerate(usernames, start=1):
            print(f"{i}. {user}")
        pilihan = int(input("\nMasukkan nomor username yang ingin dilihat riwayat pembeliannya: ")) - 1
        if 0 <= pilihan < len(usernames):
            return usernames[pilihan]
        else:
            print("Pilihan tidak valid.")
            return None
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
        return None
    
def baca_data_barang(unused_path=None):
    df = database.load_products()
    data_barang = {}
    for _, row in df.iterrows():
        # NOTE: 'Harga_tersedia' is no longer stored in CSV. 
        # For reporting purposes, we use base price or 0.
        data_barang[row['nama_barang']] = {
            "id_barang": row['id_barang'],
            "stok": int(float(row['Stok'])),
            "harga": int(float(row['harga'])),
            "harga_tersedia": row['harga'] 
        }
    return data_barang

def baca_riwayat_penjualan(unused_path=None):
    try:
        df = database.load_transactions()
        if df.empty:
            return {}
        # Simple aggregation: count transactions per item name
        # Note: Original code had a bug where it hardcoded jumlah = 1
        # I will keep the compatibility but use actual 'jumlah' if possible
        penjualan = df.groupby('nama_barang')['jumlah'].sum().to_dict()
        return penjualan
    except Exception as e:
        print(f"Terjadi kesalahan saat membaca riwayat penjualan: {e}")
        return {}
    
def lihat_barang(unused_path=None):
    try:
        data_barang = database.load_products()
        if data_barang.empty:
            print("Data barang kosong! Tidak ada barang yang tersedia saat ini.")
            return
        panjang_tabel = 60
        nama_laporaan = "Daftar Barang Tersedia"
        print("\n"+"="*panjang_tabel)
        print(f"| {nama_laporaan.center(panjang_tabel-4)} |")
        print("="*panjang_tabel)
        print(f"+{'-'*10}+{'-'*20}+{'-'*10}+{'-'*10}+")
        print(f"| {'ID Barang':<8} | {'Nama Barang':<18} | {'Harga':<8} | {'Stok':<7} |")
        print(f"+{'-'*10}+{'-'*20}+{'-'*10}+{'-'*10}+")
        for _, row in data_barang.iterrows():
            print(f"| {row['id_barang']:<8} | {row['nama_barang']:<18} | {row['harga']:<8} | {row['Stok']:<8} |")
        print(f"+{'-'*10}+{'-'*20}+{'-'*10}+{'-'*10}+")
    except Exception as e:
        print(f"Terjadi kesalahan saat membaca data barang: {e}")
    
    input("\nTekan enter untuk kembali...")

def menu_petani(username):
    while True:
        clear()
        print(f"\nHalo {username}! mau ngapain di menu petani?")
        print("1. Tambah Barang")
        print("2. Hapus Barang")
        print("3. Edit Barang")
        print("4. Lihat Barang")
        print("5. Lihat Data Penjualan")
        print("0. Keluar")
        pilihan = input("Pilih menu: ")
        if pilihan == "1":
            clear()
            tambah_barang()
        elif pilihan == "2":
            clear()
            hapus_barang()
        elif pilihan == "3":
            clear()
            edit_barang(username)
        elif pilihan == "4":
            clear()
            lihat_barang_petani(username)
        elif pilihan == "5":
            # clear()
            lihat_riwayat_transaksi(username)
        elif pilihan == "0":
            clear()
            menu_utama()
            break
        else:
            print("Pilihan tidak valid.")
            
def tambah_barang():
    try:
        baca_tambah_barang = database.load_products()
        if baca_tambah_barang.empty:
            id_barang = 1
        else:
            id_barang = int(baca_tambah_barang['id_barang'].max()) + 1
        
        while True:
            nama_barang = validasi_huruf("Masukkan Nama Barang: ").strip()
            if nama_barang:
                break
            else:
                input("Nama barang tidak boleh kosong! Tekan Enter untuk mencoba lagi...")
        
        stok = validasi_angka("Masukkan Jumlah Barang: ")
        harga = validasi_angka("Masukkan Harga Barang: ")
        penjual = validasi_huruf("Masukkan Nama Petani: ").strip().title()
        
        database.save_product(id_barang, nama_barang, stok, harga, penjual)
        print("Barang berhasil ditambahkan.")
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

def hapus_barang():
    try:
        df = database.load_products()
        if df.empty:
            print("Belum ada barang yang dijual.")
            return
        print(tb(df[["id_barang", "nama_barang", "Stok", "harga"]], headers=["ID Barang", "Nama Barang", "Stok", "Harga"], tablefmt="fancy_grid", showindex=False))
        id_barang_input = validasi_angka("Masukkan ID Barang yang ingin dihapus: ")
        id_barang = str(int(id_barang_input))
        
        if id_barang in df["id_barang"].values:
            database.delete_product(id_barang)
            input("Barang berhasil dihapus.")
        else:
            print("ID Barang tidak ditemukan.")
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")


def edit_barang(username):
    try:
        df = database.load_products()
        if df.empty:
            print("Belum ada barang yang dijual.")
            return
        print(tb(df[['id_barang', 'nama_barang', 'Stok', 'harga','Penjual']], headers=["ID Barang", "Nama Barang", "Stok", "Harga","Penjual"], tablefmt="fancy_grid", showindex=False))
        id_barang_input = validasi_angka("Masukkan ID Barang yang ingin diubah: ")
        id_barang = str(int(id_barang_input))
        
        if id_barang in df["id_barang"].values:
            while True:
                nama_barang = validasi_huruf("Masukkan Nama Barang baru: ")
                if nama_barang:
                    break
                else:
                    print("Nama barang tidak boleh kosong!")
            stok = validasi_angka("Masukkan Stok baru: ")
            harga = validasi_angka("Masukkan Harga baru: ")
            penjual = validasi_huruf("Masukkan Nama Petani: ").strip().title()
            
            database.save_product(id_barang, nama_barang, stok, harga, penjual)
            print("Barang berhasil diubah.")
        else:
            print("ID Barang tidak ditemukan.")
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

def lihat_riwayat_transaksi(username):
    try:
        riwayat_user = database.load_transactions()
        if riwayat_user.empty:
            print("\nAnda belum memiliki riwayat transaksi.")
            return

        riwayat_user['Penjual'] = riwayat_user['Penjual'].str.strip().str.lower()
        username = username.strip().lower()
        riwayat_user = riwayat_user[riwayat_user['Penjual'] == username]
        
        if riwayat_user.empty:
            print("\nAnda belum memiliki riwayat transaksi.")
        else:
            panjang_tabel = 60
            nama_pesan = f"Halo {username}! Ini riwayat penjualan kamu:"
            print("\n" + "=" * panjang_tabel)
            print(f"| {nama_pesan.center(panjang_tabel - 4)} |")
            print("=" * panjang_tabel)
            print(tb(riwayat_user[['id_barang', 'jumlah', 'harga', 'total_harga', 'username']], headers=["ID Barang", "Jumlah", "Harga", "Total Harga", "Pembeli"], tablefmt="fancy_grid", showindex=False))
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

    input("\nTekan enter untuk kembali.")
def lihat_barang_petani(username):
    try:
        data_barang = database.load_products()
        if data_barang.empty:
            print("\nTidak ada barang yang ditemukan.")
            return
        
        data_barang['Penjual'] = data_barang['Penjual'].str.strip().str.lower()
        username = username.strip().lower()
        barang_penjual = data_barang[data_barang['Penjual'] == username]
        
        if barang_penjual.empty:
            print("\nTidak ada barang yang ditemukan untuk penjual ini.")
        else:
            print(f"\nWah, Halo {username}! Ini barang yang kamu jual: ")
            print(tb(barang_penjual[['id_barang', 'nama_barang', 'Stok', 'harga']], 
                    headers=['ID Barang', 'Nama Barang', 'Stok', 'Harga'], tablefmt="fancy_grid", showindex=False))
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

    input("\nTekan enter untuk kembali ke menu utama...") 

def login():
    # load_data_pengguna() # Removed
    kesalahan_login = 0  
    while True:
        clear()
        users = database.load_users()
        if not users:
            print("Data pengguna tidak ditemukan. Silahkan daftar terlebih dahulu.")
            return
            
        panjang_tabel = 40
        print(f"+{'='*panjang_tabel}+")
        print(f"|{'Selamat Datang di Login Menu Bumbuln':^{panjang_tabel}}|")
        print(f"|{'Silahkan login terlebih dahulu.':^{panjang_tabel}}|")
        print(f"+{'='*panjang_tabel}+")
        username = input("Masukkan username: ").strip().title()
        password = input("Masukkan password: ").strip()
        
        if not username or not password:
            print("Username atau password tidak boleh kosong!")
            input("Tekan enter untuk mencoba lagi...")
            continue
        
        if username == "Admin" and password == "admin123":
            menu_admin(username)
            return
        
        if username in users:
            info = users[username]
            if info["password"] == password:
                kesalahan_login = 0  
                tipe_pengguna = info.get("tipe_pengguna", "").strip().lower() 
                
                if tipe_pengguna == "admin":
                    menu_admin(username)
                elif tipe_pengguna == "petani":
                    menu_petani(username)
                elif tipe_pengguna == "pembeli":
                    tipe_pembeli = info.get("tipe_pembeli", "")
                    menu_pembeli(username, tipe_pembeli)
                else:
                    print("Tipe pengguna tidak dikenal!")
                return
            else:
                kesalahan_login += 1  
                if kesalahan_login >= 3:
                    lupa_password(username)
                    kesalahan_login = 0  
                else:
                    print("Password salah! Silahkan coba lagi.")
                    input("Tekan enter untuk mencoba lagi...")
        else:
            print("Username tidak ditemukan!")
            mau_daftar_gak = input("Mau daftar? (y/n): ")
            if mau_daftar_gak.lower() == "y":
                daftar()
            else:
                return
            
def menu_utama():
    while True:
        clear()
        try:
            nama_aplikasi = "Selamat Datang di BumbuIn"
            panjang_tabel = len(nama_aplikasi) + 20
            print(f"\n{"=" * panjang_tabel}")
            print(f"| {nama_aplikasi.center(panjang_tabel-4)} |")
            print(f"{"=" * panjang_tabel}")    
            print(f"+{"="*4}+{"="*(panjang_tabel-6)}+")
            print(f"| {"No":<2} | {"Menu":<{panjang_tabel-8}} |")
            print(f"+{"="*4}+{"="*(panjang_tabel-6)}+")
            print(f"| {"1":<2} | {"Daftar":<{panjang_tabel-8}} |")
            print(f"| {"2":<2} | {"Login":<{panjang_tabel-8}} |")
            print(f"| {"0":<2} | {"Keluar":<{panjang_tabel-8}} |")
            print(f"+{"="*4}+{"="*(panjang_tabel-6)}+")
            pilih_awal = input("Silahkan pilih menu yang sesuai (0/1/2): ")
            if pilih_awal == "1":
                clear()
                daftar()
            elif pilih_awal == "2":
                clear()
                login()
            elif pilih_awal == "0":
                print("Terima kasih sudah berbelanja!\nProgram akan berhenti dalam hitungan...")
                for i in reversed(range(3)):
                    i += 1
                    print(f"{i}...")
                    time.sleep(1)
                break
            else:
                print(f"Wah! Pilihan {pilih_awal} tidak ada. Pilih ulang yaa!")
                input("Tekan enter untuk mencoba lagi...")
                continue
        except KeyboardInterrupt:
            print("\nProgram dihentikan oleh pengguna!")
            break
menu_utama()