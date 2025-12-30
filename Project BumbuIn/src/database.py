import pandas as pd
import os

# Define base paths
# Define base paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_DIR = os.path.join(BASE_DIR, "data")
USER_DATA_DIR = CSV_DIR # Simplified

USERS_FILE = os.path.join(CSV_DIR, "users.csv")
PRODUCTS_FILE = os.path.join(CSV_DIR, "products.csv")
TRANSACTIONS_FILE = os.path.join(CSV_DIR, "transactions.csv")
BALANCE_FILE = os.path.join(CSV_DIR, "balances.csv")
CART_FILE = os.path.join(CSV_DIR, "cart.csv")

def ensure_dirs():
    """Ensure that all necessary directories exist."""
    os.makedirs(USER_DATA_DIR, exist_ok=True)

def init_csv_files():
    """Initialize CSV files with headers if they don't exist."""
    ensure_dirs()
    if not os.path.exists(USERS_FILE):
        pd.DataFrame(columns=["Username", "Password", "Tipe Pengguna", "Tipe Pembeli"]).to_csv(USERS_FILE, index=False)
    if not os.path.exists(PRODUCTS_FILE):
        pd.DataFrame(columns=['id_barang', 'nama_barang', 'Stok', 'harga', 'Penjual']).to_csv(PRODUCTS_FILE, index=False)
    if not os.path.exists(TRANSACTIONS_FILE):
        pd.DataFrame(columns=["username", "id_barang", "nama_barang", "jumlah", "harga", "total_harga", "Penjual"]).to_csv(TRANSACTIONS_FILE, index=False)
    if not os.path.exists(BALANCE_FILE):
        pd.DataFrame(columns=["Username", "Saldo"]).to_csv(BALANCE_FILE, index=False)
    if not os.path.exists(CART_FILE):
        pd.DataFrame(columns=["username", "id_barang", "nama_barang", "jumlah", "harga", "total_harga", "Penjual"]).to_csv(CART_FILE, index=False)

# --- User Management ---
def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    df = pd.read_csv(USERS_FILE)
    users = {}
    for _, row in df.iterrows():
        users[row['Username']] = {
            "password": str(row['Password']),
            "tipe_pengguna": str(row['Tipe Pengguna']),
            "tipe_pembeli": str(row['Tipe Pembeli']) if pd.notna(row['Tipe Pembeli']) else ""
        }
    return users

def save_user(username, password, tipe_pengguna, tipe_pembeli=""):
    df = pd.read_csv(USERS_FILE)
    new_user = pd.DataFrame([{
        "Username": username,
        "Password": password,
        "Tipe Pengguna": tipe_pengguna,
        "Tipe Pembeli": tipe_pembeli
    }])
    df = pd.concat([df[df['Username'] != username], new_user], ignore_index=True)
    df.to_csv(USERS_FILE, index=False)

def delete_user(username):
    df = pd.read_csv(USERS_FILE)
    df = df[df['Username'] != username]
    df.to_csv(USERS_FILE, index=False)

# --- Product Management ---
def load_products():
    if not os.path.exists(PRODUCTS_FILE):
        return pd.DataFrame()
    df = pd.read_csv(PRODUCTS_FILE, dtype={'id_barang': str})
    # Clean up redundant column if it exists
    if 'Harga_tersedia' in df.columns:
        df = df.drop(columns=['Harga_tersedia'])
    return df

def save_product(id_barang, nama_barang, stok, harga, penjual):
    df = load_products()
    if float(stok) < 0:
        raise ValueError("Stok tidak boleh negatif")
        
    new_product = pd.DataFrame([{
        'id_barang': str(id_barang),
        'nama_barang': nama_barang,
        'Stok': float(stok),
        'harga': float(harga),
        'Penjual': penjual
    }])
    df = pd.concat([df[df['id_barang'] != str(id_barang)], new_product], ignore_index=True)
    df.to_csv(PRODUCTS_FILE, index=False)

def update_product_stock(id_barang, delta):
    """
    Update stock for a product.
    delta can be positive (add stock) or negative (reduce stock).
    Raises ValueError if resulting stock would be negative.
    """
    df = load_products()
    id_barang = str(id_barang)
    if id_barang not in df['id_barang'].values:
        raise ValueError(f"Barang dengan ID {id_barang} tidak ditemukan")
    
    current_stock = df.loc[df['id_barang'] == id_barang, 'Stok'].values[0]
    new_stock = current_stock + delta
    
    if new_stock < 0:
        raise ValueError(f"Stok tidak cukup! Stok saat ini: {current_stock}, diminta: {abs(delta)}")
        
    df.loc[df['id_barang'] == id_barang, 'Stok'] = new_stock
    df.to_csv(PRODUCTS_FILE, index=False)

def delete_product(id_barang):
    df = load_products()
    df = df[df['id_barang'] != str(id_barang)]
    df.to_csv(PRODUCTS_FILE, index=False)

# --- Balance Management ---
def load_balances():
    if not os.path.exists(BALANCE_FILE):
        return pd.DataFrame(columns=["Username", "Saldo"])
    df = pd.read_csv(BALANCE_FILE)
    # Deduplicate on load: keep the last entry for each user
    df["Username"] = df["Username"].str.strip().str.upper()
    df = df.drop_duplicates(subset=["Username"], keep='last')
    return df

def get_balance(username):
    df = load_balances()
    username = username.strip().upper()
    user_balance = df[df['Username'] == username]
    if not user_balance.empty:
        return float(user_balance['Saldo'].values[0])
    return 0.0

def update_balance(username, amount, absolute=False):
    df = load_balances()
    username = username.strip().upper()
    if absolute:
        new_balance = float(amount)
    else:
        current = get_balance(username)
        new_balance = current + float(amount)
    
    new_data = pd.DataFrame([{"Username": username, "Saldo": new_balance}])
    df = pd.concat([df[df['Username'] != username], new_data], ignore_index=True)
    df.to_csv(BALANCE_FILE, index=False)

# --- Transaction & Cart ---
def load_cart(username=None):
    if not os.path.exists(CART_FILE):
        return pd.DataFrame()
    df = pd.read_csv(CART_FILE)
    if username:
        return df[df['username'].str.upper() == username.upper()]
    return df

def add_to_cart(username, id_barang, nama_barang, jumlah, harga, total_harga, penjual):
    df = load_cart()
    new_item = pd.DataFrame([{
        'username': username,
        'id_barang': str(id_barang),
        'nama_barang': nama_barang,
        'jumlah': int(jumlah),
        'harga': float(harga),
        'total_harga': float(total_harga),
        'Penjual': penjual
    }])
    df = pd.concat([df, new_item], ignore_index=True)
    df.to_csv(CART_FILE, index=False)

def clear_cart(username):
    df = load_cart()
    df = df[df['username'].str.upper() != username.upper()]
    df.to_csv(CART_FILE, index=False)

def load_transactions(username=None):
    if not os.path.exists(TRANSACTIONS_FILE):
        return pd.DataFrame()
    df = pd.read_csv(TRANSACTIONS_FILE)
    if username:
        return df[df['username'].str.upper() == username.upper()]
    return df

def add_transactions(df_new):
    if not os.path.exists(TRANSACTIONS_FILE):
        df_new.to_csv(TRANSACTIONS_FILE, index=False)
    else:
        df = pd.read_csv(TRANSACTIONS_FILE)
        df = pd.concat([df, df_new], ignore_index=True)
        df.to_csv(TRANSACTIONS_FILE, index=False)

# Initialize files on import
init_csv_files()
