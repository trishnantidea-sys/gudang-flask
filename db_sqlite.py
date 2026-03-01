# koneksi + buat tabel SQLite otomatis

import mysql.connector
import sqlite3

def get_conection():
    conn = mysql.connector.connect(**{
        "user": os.getenv('DB_USER'),
        "password": os.getenv('DB_PASSWORD'),
        "host": os.getenv('DB_HOST'),
        "database": os.getenv('DB_SCHEMA'),
    })

    return conn

def get_connection():
    conn = sqlite3.connect("db_gudang_ekspedisi.db")
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXIST users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        userid TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        nama TEXT, gender TEXT, usia INTEGER,
        pekerjaan TEXT, hobi TEXT, kota TEXT,
        rt INTEGER, rw INTEGER, zipcode INTEGER,
        lat REAL, longitude REAL, nohp INTEGER
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS paket (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        resi TEXT UNIQUE NOT NULL,
        pengirim TEXT, no_hp_pengirim TEXT,
        penerima TEXT, no_hp_penerima TEXT,
        alamat_tujuan TEXT, kategori TEXT,
        berat REAL, tanggal_pengiriman DATETIME,
        jenis_pengiriman TEXT, estimasi DATETIME, 
        tarif INTEGER, created_date DATETIME, 
        created_by INTEGER
    )''')

    conn.commit()
    conn.close()