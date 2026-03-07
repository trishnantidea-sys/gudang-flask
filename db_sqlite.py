import sqlite3

# Database SQLite initialization
DB_NAME = "db_gudang_ekspedisi.db"

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # Create users table
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        nama TEXT, 
        gender TEXT CHECK(gender IN ('male', 'female')), 
        usia INTEGER,
        pekerjaan TEXT, 
        hobi TEXT, 
        kota TEXT,
        rt INTEGER, 
        rw INTEGER, 
        zipcode INTEGER,
        lat REAL, 
        longitude REAL, 
        nohp TEXT
    )''')

    # Create paket table
    cursor.execute('''CREATE TABLE IF NOT EXISTS paket (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        resi TEXT UNIQUE NOT NULL,
        pengirim TEXT, 
        no_hp_pengirim TEXT,
        penerima TEXT, 
        no_hp_penerima TEXT,
        alamat_tujuan TEXT, 
        kategori TEXT CHECK(kategori IN ('Alat Olahraga', 'Kebutuhan Rumah Tangga', 'ATK', 'Dokumen', 'Elektronik', 'Pakaian/Tekstil', 'Sparepart')),
        berat REAL, 
        tanggal_pengiriman DATETIME,
        jenis_pengiriman TEXT CHECK(jenis_pengiriman IN ('Reguler', 'Eco', 'Kilat', 'Kargo')), 
        estimasi DATETIME, 
        tarif INTEGER, 
        created_date DATETIME, 
        created_by INTEGER
    )''')

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database SQLite initialized successfully.")