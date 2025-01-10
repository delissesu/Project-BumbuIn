import time
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import pandas as pd
import os
import csv
from tabulate import tabulate as tb


"""
CATATAN MAS FANA:
admin ditetepin jd 1
data pengguna selalu disimpen ben penak
harganya di markup
id automate
"""
data_semua_pengguna = "Project BumbuIn\\CSV\\Data Pengguna\\data_semuapengguna.csv"
barang_file = "Project BumbuIn\\data_barang.csv"
riwayat_file = "Project BumbuIn\\Transaksi.csv"
saldo_file = "Project BumbuIn\\saldo_pengguna.csv"
keranjang_beli = "Project BumbuIn\\keranjang.csv"
data_pengguna = {}


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')
    
def load_data_pengguna():
    global data_pengguna
    data_pengguna.clear()
    if not os.path.exists(data_semua_pengguna):
        with open(data_semua_pengguna, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Username", "Password", "Tipe Pengguna", "Tipe Pembeli"])
        return
    with open(data_semua_pengguna,'r') as file:
        baca_csv = csv.reader(file)
        next(baca_csv) 
        for baris in baca_csv:
            if len(baris) >= 2:
                username = baris[0]
                password = baris[1]
                tipe_pengguna = baris[2] if len(baris) > 2 else ""
                tipe_pembeli = baris[3] if len(baris) > 3 else ""
                if tipe_pengguna and tipe_pembeli:
                    data_pengguna[username] = {
                        "password" : password,
                        "tipe_pengguna" : tipe_pengguna,
                        "tipe_pembeli" : tipe_pembeli
                    }
                elif tipe_pengguna:
                    data_pengguna[username] = {
                        "password" : password,
                        "tipe_pengguna" : tipe_pengguna
                    }
                else:
                    data_pengguna[username] = password
        
def cek_data_pengguna():
    if not data_pengguna:
        print("Belum ada pengguna yang terdaftar")
        return pd.DataFrame()
    else:
        df = pd.DataFrame.from_dict(data_pengguna, orient="index")
        df.index.name = "Username"
        df.reset_index(inplace=True)
        return df
    
def validasi_username(data_pengguna):
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
    load_data_pengguna()
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
                    
                    data_pengguna[username] = {
                        "password" : password,
                        "tipe_pengguna" : "pembeli",
                        "tipe_pembeli" : tipe_pembeli
                    }
                elif tipe_user == "1":
                    data_pengguna[username] = {
                        "password" : password,
                        "tipe_pengguna" : "petani"
                    }
            except Exception as e:
                print(f"Terjadi kesalahan: {e}")
                input("Tekan enter untuk mencoba lagi...")
                continue
            with open(data_semua_pengguna, 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([
                    username,
                    password,
                    data_pengguna[username].get("tipe_pengguna", ""),
                    data_pengguna[username].get("tipe_pembeli", "")
                ])
            print(f"Halo {username}! Kamu terdaftar sebagai {data_pengguna[username].get('tipe_pengguna', '')}")
            return
        
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
        if not os.path.exists(barang_file):
            print("File data barang tidak ditemukan.")
            return
        data_barang = pd.read_csv(barang_file, dtype={'id_barang': str})
        if data_barang.empty:
            print("\nBelum ada barang yang dijual.")
        else:
            pengguna_df = pd.read_csv(data_semua_pengguna)
            if username not in pengguna_df['Username'].values:
                print("Username tidak ditemukan dalam daftar pengguna.")
                return
            tipe_pembeli = pengguna_df.loc[ pengguna_df['Username'] == username, 'Tipe Pembeli'].values[0]
            if tipe_pembeli == 'Pelaku Industri':
                data_barang['Harga_tersedia'] = data_barang['harga'] * 0.9
            elif tipe_pembeli == 'Pembeli Warungan':
                data_barang['Harga_tersedia'] = data_barang['harga'] * 0.95
            elif tipe_pembeli == 'Anak Kosan':
                data_barang['Harga_tersedia'] = data_barang['harga']
            else:
                print("\nTipe pembeli tidak dikenali.")
                return
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
        if not os.path.exists(barang_file):
            print("File data barang tidak ditemukan.")
            return
        data_barang = pd.read_csv(barang_file, dtype={'id_barang': str})
        pengguna_df = pd.read_csv(data_semua_pengguna)
        if username not in pengguna_df['Username'].values:
            print("Username tidak ditemukan dalam daftar pengguna.")
            return
        tipe_pembeli = pengguna_df.loc[pengguna_df['Username'] == username, 'Tipe Pembeli'].values[0]
        if tipe_pembeli == 'Pelaku Industri':
            data_barang['Harga_tersedia'] = data_barang['harga'] * 0.9
        elif tipe_pembeli == 'Pembeli Warungan':
            data_barang['Harga_tersedia'] = data_barang['harga'] * 0.95
        elif tipe_pembeli == 'Anak Kosan':
            data_barang['Harga_tersedia'] = data_barang['harga']
        else:
            print("\nTipe pembeli tidak dikenali.")
            return
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
        Penjual = barang_dipilih['Penjual'].values[0] 
        total_harga = harga * jumlah
        data_barang.loc[data_barang['id_barang'] == id_barang, 'Stok'] -= jumlah
        data_barang.to_csv(barang_file, index=False)
        keranjang_data = pd.DataFrame({
            'username': [username],
            'id_barang': [id_barang],
            'nama_barang': [barang_dipilih['nama_barang'].values[0]],
            'jumlah': [jumlah],
            'harga': [harga],
            'total_harga': [total_harga],
            'Penjual': [Penjual]  
        })
        try:
            keranjang = pd.read_csv(keranjang_beli)
            if 'username' not in keranjang.columns:
                keranjang['username'] = ''
            keranjang = pd.concat([keranjang, keranjang_data], ignore_index=True)
        except FileNotFoundError:
            keranjang = keranjang_data
        keranjang.to_csv(keranjang_beli, index=False)
        print("\nTransaksi berhasil dimasukkan ke keranjang!")
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

    input("\nTekan enter untuk kembali ke menu utama...")


def lihat_keranjang(username):
    try:
        if not os.path.exists("Project BumbuIn\\keranjang.csv"):
            print(f"File keranjang tidak ditemukan.")
            return
        keranjang = pd.read_csv("Project BumbuIn\\keranjang.csv")        
        if 'username' not in keranjang.columns:
            print("\nMana usernamenya?")
            return
        keranjang_user = keranjang[keranjang['username'] == username] 
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
    except pd.errors.EmptyDataError:
        print("\nKeranjang Anda kosong.")
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
    input("\nTekan enter untuk kembali.")


def checkout(username):
    try:
        keranjang_beli= "Project BumbuIn\\keranjang.csv"
        data_barang_file = "Project BumbuIn\\data_barang.csv"
        saldo_pengguna_file = "Project BumbuIn\\saldo_pengguna.csv"
        riwayat_file = "Project BumbuIn\\Transaksi.csv"
        transaksi_file = "Project BumbuIn\\Transaksi.csv"
        keranjang = pd.read_csv(keranjang_beli)
        keranjang.columns = [col.strip() for col in keranjang.columns]
        keranjang['username'] = keranjang['username'].str.replace(r"['\"]", '', regex=True).str.strip()
        keranjang_pengguna = keranjang[keranjang['username'].str.upper() == username.upper()]
        if keranjang_pengguna.empty:
            input(f"Wah, keranjang kak {username} masih kosong! Yuk, tambah barang dulu!")
            return
        barang = pd.read_csv(data_barang_file)
        saldo_pengguna = pd.read_csv(saldo_pengguna_file)
        total_harga = keranjang_pengguna['total_harga'].sum()
        saldo_pengguna['Username'] = saldo_pengguna['Username'].str.strip().str.upper()
        saldo_sekarang = saldo_pengguna.loc[saldo_pengguna['Username'] == username.upper(), 'Saldo'].values[0]
        if saldo_sekarang < total_harga:
            print("Saldo tidak cukup untuk melakukan checkout. Silakan isi saldo terlebih dahulu.")
            return

        saldo_pengguna.loc[saldo_pengguna['Username'] == username.upper(), 'Saldo'] = saldo_sekarang - total_harga
        saldo_pengguna.to_csv(saldo_pengguna_file, index=False)
        for _, item in keranjang_pengguna.iterrows():
            id_barang = item['id_barang']
            jumlah_beli = item['jumlah']
            barang.loc[barang['id_barang'] == id_barang, 'Stok'] -= jumlah_beli
        barang.to_csv(data_barang_file, index=False)
        if os.path.exists(riwayat_file):
            riwayat_pengguna = pd.read_csv(riwayat_file)
        else:
            riwayat_pengguna = pd.DataFrame()
        riwayat_baru = pd.DataFrame({
            "username": keranjang_pengguna['username'],
            "id_barang": keranjang_pengguna['id_barang'],
            "nama_barang": keranjang_pengguna['nama_barang'],
            "harga": keranjang_pengguna['harga'],
            "jumlah": keranjang_pengguna['jumlah'],
            "total_harga": keranjang_pengguna['total_harga'],
            "Penjual": keranjang_pengguna['Penjual']
        })
        riwayat_pengguna = pd.concat([riwayat_pengguna, riwayat_baru], ignore_index=True)
        riwayat_pengguna.to_csv(riwayat_file, index=False)
        if os.path.exists(transaksi_file):
            transaksi = pd.read_csv(transaksi_file)
        else:
            transaksi = pd.DataFrame()
        transaksi = pd.concat([transaksi, keranjang_pengguna[["username", "id_barang", "nama_barang", "jumlah", "harga", "total_harga", "Penjual"]]], ignore_index=True)
        transaksi.to_csv(transaksi_file, index=False)

        keranjang = keranjang[keranjang['username'].str.upper() != username.upper()]
        keranjang.to_csv(keranjang_beli, index=False)
        saldo_akhir = saldo_pengguna.loc[saldo_pengguna['Username'] == username.upper(), 'Saldo'].values[0]
        print(f"\nCheckout berhasil! Saldo akhir Anda adalah: Rp.{saldo_akhir:,.2f}".replace(",", "."))

    except Exception as error:
        print(f"Terjadi kesalahan: {error}")

    input("Tekan enter untuk kembali ke menu utama...")

def riwayat_pembelian(username):
    try:
        riwayat = pd.read_csv("Project BumbuIn\\Transaksi.csv", dtype=str)
        transaksi = riwayat[riwayat['username'] == username]
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
        with open(saldo_file, mode="r") as file:
            reader = csv.reader(file)
            data = list(reader)
        if len(data) > 1:
            header = data[0]
            isi_data = data[1:]
        else:
            header = ["Username", "Saldo"]
            isi_data = []
        username = username.strip().upper()
        ditemukan = False
        for row in isi_data:
            if row[0].strip().upper() == username:
                row[1] = str(float(row[1]) + jumlah_topup)
                ditemukan = True
                break
        if not ditemukan:
            isi_data.append([username, str(jumlah_topup)])
        with open(saldo_file, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(header)
            writer.writerows(isi_data)
        print("Saldo berhasil ditambahkan!")
        input("Tekan Enter untuk kembali ke menu utama...")
    except ValueError:
        print("Masukkan jumlah saldo yang valid!")

def cek_saldo(username):
    df = pd.read_csv(saldo_file)
    df["Username"] = df["Username"].str.strip().str.title()
    username = username.strip().title()
    if username in df["Username"].values:
        saldo = df.loc[df["Username"] == username, "Saldo"].values[0]
        print(f"Halo Kak! Saldo Kak {username} saat ini: Rp.{saldo:,.2f}".replace(",", "."))
    else:
        print("Saldo Anda saat ini: Rp 0")
    input("Tekan Enter untuk kembali ke menu utama...")


def menu_admin(username):
    data_barang = baca_data_barang(barang_file)
    penjualan = baca_riwayat_penjualan(riwayat_file)
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
            lihat_barang(barang_file)
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
    username = validasi_username(data_pengguna)
    if username:
        password = validasi_password()
        tipe_pengguna = input("Masukkan tipe pengguna (admin/petani/pembeli): ").strip().lower()
        tipe_pembeli = ""
        if tipe_pengguna == "pembeli":
            tipe_pembeli = input("Masukkan tipe pembeli: ").strip().title()
        
        data_pengguna[username] = {
            "password": password,
            "tipe_pengguna": tipe_pengguna,
            "tipe_pembeli": tipe_pembeli
        }
        simpan_data_pengguna()
        print(f"\nPengguna {username} berhasil ditambahkan.")
    input("\nTekan enter untuk kembali ke menu admin...")

def lihat_pengguna():
    df_pengguna = cek_data_pengguna()
    if not df_pengguna.empty:
        print(tb(df_pengguna, headers=['Username', 'Password', 'Tipe Pengguna', 'Tipe Pembeli'], tablefmt="fancy_grid", showindex=False))
    input("\nTekan enter untuk kembali ke menu admin...")
    
def perbarui_pengguna():
    print("\n=== Perbarui Pengguna ===")
    username = input("Masukkan username yang ingin diperbarui: ").strip().title()
    if username in data_pengguna:
        print(f"\nInformasi saat ini untuk {username}: {data_pengguna[username]}")
        pilihan = input("Apa yang ingin diperbarui? (password/tipe pengguna/tipe pembeli): ").strip().lower()
        if pilihan == "password":
            data_pengguna[username]["password"] = validasi_password()
        elif pilihan == "tipe pengguna":
            data_pengguna[username]["tipe_pengguna"] = input("Masukkan tipe pengguna baru: ").strip().lower()
        elif pilihan == "tipe pembeli":
            if data_pengguna[username]["tipe_pengguna"] == "pembeli":
                data_pengguna[username]["tipe_pembeli"] = input("Masukkan tipe pembeli baru: ").strip().lower()
            else:
                print("Pengguna bukan tipe pembeli.")
        else:
            print("Pilihan tidak valid.")
        simpan_data_pengguna()
        print(f"\nPengguna {username} berhasil diperbarui.")
    else:
        print("Username tidak ditemukan.")
    input("\nTekan enter untuk kembali ke menu admin...")

def hapus_pengguna():
    username = input("Masukkan username yang ingin dihapus: ").strip().title()
    if username in data_pengguna:
        konfirmasi = input(f"Apakah Anda yakin ingin menghapus pengguna {username}? (y/n): ").strip().lower()
        if konfirmasi == 'y':
            del data_pengguna[username]
            simpan_data_pengguna()
            print(f"\nPengguna {username} berhasil dihapus.")
        else:
            print("Penghapusan dibatalkan.")
    else:
        print("Username tidak ditemukan.")
    input("\nTekan enter untuk kembali ke menu admin...")

def simpan_data_pengguna():
    with open(data_semua_pengguna, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Username", "Password", "Tipe Pengguna", "Tipe Pembeli"])
        for username, info in data_pengguna.items():
            writer.writerow([
                username, 
                info["password"], 
                info.get("tipe_pengguna", ""), 
                info.get("tipe_pembeli", "")
            ])

def lupa_password(username):
    
    if username in data_pengguna:
        password = data_pengguna[username]["password"] if isinstance(data_pengguna[username], dict) else data_pengguna[username]
        print(f"Password untuk username '{username}' adalah: {password}")
    else:
        print("Username tidak ditemukan!")
    input("Tekan enter untuk kembali...")
def pilih_username():
    try:
        keranjang = pd.read_csv("Project BumbuIn\\keranjang.csv", dtype=str)
        riwayat = pd.read_csv("Project BumbuIn\\Transaksi.csv", dtype=str)
        usernames_keranjang = keranjang['username'].unique()
        usernames_riwayat = riwayat['username'].unique()
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
    
def baca_data_barang(barang_file):
    data_barang = {}
    with open(barang_file, mode="r") as file:
        reader = csv.reader(file)
        next(reader)  
        for row in reader:
            if len(row) != 6:
                print(f"Baris tidak valid (terlalu banyak/kekurangan kolom): {row}")
                continue
            id_barang, nama_barang, stok, harga, Penjual, harga_tersedia  = row
            data_barang[nama_barang] = {
                "id_barang": id_barang,
                "stok": int(float(stok)),
                "harga": int(float(harga)),
                "harga_tersedia": harga_tersedia
            }
    return data_barang

def baca_riwayat_penjualan(riwayat_file):
    try:
        penjualan = {}
        with open(riwayat_file, mode='r') as file:
            reader = csv.reader(file)
            header = next(reader)
            for row in reader:
                if not row:
                    continue
                if len(row) != 7:
                    print(f"Baris tidak valid (kolom kurang): {row}")
                    continue
                username, id_barang, nama_barang, jumlah, harga, total_harga, Penjual = row
                try:
                    harga = float(harga)
                except ValueError:
                    print(f"Nilai harga tidak valid: {harga}")
                    continue
                jumlah = 1 
                total_harga = harga * jumlah
                if nama_barang in penjualan:
                    penjualan[nama_barang] += jumlah
                else:
                    penjualan[nama_barang] = jumlah
        return penjualan
    except Exception as e:
        print(f"Terjadi kesalahan saat membaca riwayat penjualan: {e}")
        return {}
    
def lihat_barang(barang_file):
    try:
        data_barang = pd.read_csv(barang_file)
        data_barang.columns = [col.strip() for col in data_barang.columns]
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
    except FileNotFoundError:
        print(f"File '{barang_file}' tidak ditemukan. Pastikan path file sudah benar.")
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
        try:
            baca_tambah_barang = pd.read_csv(
                "Project BumbuIn\\data_barang.csv",
                dtype={'id_barang': str, 'Stok': float, 'harga': float}
            )
        except FileNotFoundError:
            baca_tambah_barang = pd.DataFrame(columns=['id_barang', 'nama_barang', 'Stok', 'harga','Penjual'])
            
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
        while True:
            clear()
            stok = validasi_angka("Masukkan Jumlah Barang: ")
            if stok:
                break
            else:
                input("Jumlah barang tidak boleh kosong! Tekan Enter untuk mencoba lagi...")
        while True:
            clear()
            harga = validasi_angka("Masukkan Harga Barang: ")
            if harga:
                break
            else:
                input("Harga barang tidak boleh kosong! Tekan Enter untuk mencoba lagi...")
        Penjual =validasi_huruf("Masukkan Nama Petani: ").strip().title()
        df_baca_tambah_barang = pd.DataFrame({
            'id_barang': [str(id_barang)],
            'nama_barang': [nama_barang],
            'Stok': [float(stok)],
            'harga': [float(harga)],
            'Penjual':[Penjual]
        })
        baca_tambah_barang = pd.concat([baca_tambah_barang, df_baca_tambah_barang], ignore_index=True)
        baca_tambah_barang.to_csv("Project BumbuIn\\data_barang.csv", index=False)
        print("Barang berhasil ditambahkan.")
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

def hapus_barang():
    try:
        df = pd.read_csv(barang_file, dtype={'id_barang': str, 'Stok': float, 'harga': float})    
        if df.empty:
            print("Belum ada barang yang dijual.")
            return
        print(tb(df[["id_barang", "nama_barang", "Stok", "harga"]], headers=["ID Barang", "Nama Barang", "Stok", "Harga"], tablefmt="fancy_grid", showindex=False))
        id_barang = validasi_angka("Masukkan ID Barang yang ingin dihapus: ")
        id_barang = str(int(id_barang))
        if id_barang in df["id_barang"].values:
            df = df[df["id_barang"] != id_barang]
            df = df.reset_index(drop=True)
            df["id_barang"] = range(1, len(df) + 1)
            df.to_csv(barang_file, index=False)
            input("Barang berhasil dihapus dan ID barang telah diperbarui.")
        else:
            print("ID Barang tidak ditemukan.")
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")


def edit_barang(username):
    try:
        df = pd.read_csv(barang_file, dtype={'id_barang': str, 'Stok': float, 'harga': float})
    except FileNotFoundError:
        print("File data barang tidak ditemukan.")
        return
    if df.empty:
        print("Belum ada barang yang dijual.")
        return
    try:
        print(tb(df[['id_barang', 'nama_barang', 'Stok', 'harga','Penjual']], headers=["ID Barang", "Nama Barang", "Stok", "Harga","Penjual"], tablefmt="fancy_grid", showindex=False))
        id_barang = validasi_angka("Masukkan ID Barang yang ingin diubah: ")
        if str(int(id_barang)) in df["id_barang"].values:
            while True:
                nama_barang = validasi_huruf("Masukkan Nama Barang baru: ")
                if nama_barang:
                    break
                else:
                    print("Nama barang tidak boleh kosong!")
            stok = validasi_angka("Masukkan Stok baru: ")
            harga = validasi_angka("Masukkan Harga baru: ")
            Penjual = validasi_huruf("Masukkan Nama Petani: ").strip().title()
            df.loc[df["id_barang"] == str(int(id_barang)), ["nama_barang", "Stok", "harga","Penjual"]] = [nama_barang, float(stok), float(harga),Penjual]
            df.to_csv(barang_file, index=False)
            print("Barang berhasil diubah.")
        else:
            print("ID Barang tidak ditemukan.")
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

def lihat_riwayat_transaksi(username):
    try:
        riwayat_transaksi = pd.read_csv("Project BumbuIn\\Transaksi.csv")
        if 'Penjual' not in riwayat_transaksi.columns:
            print("\nKolom 'penjual' tidak ditemukan dalam Transaksi.csv.")
            return
        riwayat_transaksi['Penjual'] = riwayat_transaksi['Penjual'].str.strip().str.lower()
        username = username.strip().lower()
        riwayat_user = riwayat_transaksi[riwayat_transaksi['Penjual'] == username]
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
        barang_file = "Project BumbuIn\\data_barang.csv"
        if not os.path.exists(barang_file):
            print("\nFile data barang tidak ditemukan.")
            return
        data_barang = pd.read_csv(barang_file)
        if 'Penjual' not in data_barang.columns:
            print("\nKolom 'Penjual' tidak ditemukan dalam data barang.")
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
    load_data_pengguna()
    kesalahan_login = 0  
    while True:
        clear()
        if not data_pengguna:
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
        
        if username in data_pengguna:
            cek_password = data_pengguna[username]["password"] if isinstance(data_pengguna[username], dict) else data_pengguna[username]
            if cek_password == password:
                kesalahan_login = 0  
                if isinstance(data_pengguna[username], dict):
                    tipe_pengguna = data_pengguna[username].get("tipe_pengguna", "")
                    
                    if tipe_pengguna == "admin":
                        menu_admin(username)
                    elif tipe_pengguna == "petani":
                        menu_petani(username)
                    elif tipe_pengguna == "pembeli":
                        tipe_pembeli = data_pengguna[username].get("tipe_pembeli", "")
                        menu_pembeli(username, tipe_pembeli)
                    else:
                        print("Tipe pengguna yang kamu pilih tidak ada!")
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
                input("Tekan enter untuk kembali...")
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