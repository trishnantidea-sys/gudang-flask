# koneksi + buat tabel SQLite otomatis

import mysql.connector

def get_conection():
    conn = mysql.connector.connect(
        host="localhost",
        user="DB_Admin",
        password="CRUDsql",
        database="Tugas_Project"
    )
    return conn

import sqlite3

def get_connection():
    conn = sqlite3.connect("Tugas_Project.db")
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXIST user (
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
        berat REAL, tanggal_pengiriman TEXT,
        jenis_pengiriman TEXT, estimasi TEXT, tarif INTEGER
    )''')

    conn.commit()
    conn.close()