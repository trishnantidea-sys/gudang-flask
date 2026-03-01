from flask import Flask, jsonify, request
import mysql.connector
import hashlib
from dotenv import load_dotenv
import os

app = Flask(__name__)

# Load environment variables from the .env file (if present)
load_dotenv()

conn = mysql.connector.connect(**{
    "user": os.getenv('DB_USER'),
    "password": os.getenv('DB_PASSWORD'),
    "host": os.getenv('DB_HOST'),
    "database": os.getenv('DB_SCHEMA'),
})
cursor = conn.cursor()

@app.route('/')
def root():
    response = {
        "message" : "gudang-flask API",
        "status" : 200,
        "data" : []
    }

    return jsonify(response)

@app.route('/login', methods=['POST'])
def login():
    # ambil JSON dari body POST
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    password_hash = hashlib.md5(password.encode()).hexdigest()

    query_check = "SELECT id, nama FROM users WHERE email=%s AND password=%s"
    cursor.execute(query_check, (email, password_hash))
    row = cursor.fetchone()

    data = []
    if row is not None:
        id, nama = row

        message = "Success"
        status_code = 200
        data.append({
            "id": id,
            "email": email,
            "nama": nama
        })
    else:
        message = "Unauthorized"
        status_code = 401
    
    return jsonify({
        "message" : message,
        "status" : status_code,
        "data" : data
    })

@app.route('/register', methods=['POST'])
def registrasi():

    data = request.json
    username = data.get("username")
    email = data.get("email")
    nama = data.get("nama")
    gender=data.get("gender")
    usia=data.get("usia")
    pekerjaan=data.get("pekerjaan")
    hobi=data.get("hobi")
    kota=data.get("kota")
    rt=data.get("rt")
    rw=data.get("rw")
    kode_pos=data.get("kode_pos")
    longitude=data.get("longitude")
    latitude=data.get("latitude")
    no_hp=data.get("no_hp")

    password = data.get("password")
    password_hash = hashlib.md5(password.encode()).hexdigest()

    query_check = f"SELECT id FROM users WHERE username='{username}'"
    cursor.execute(query_check)
    existing = cursor.fetchone()

    if existing:
        return jsonify({
            "message": "Username sudah ada",
            "status": 409,
            "data": []
        }), 409

    query_check = f"SELECT id FROM users WHERE email='{email}'"
    cursor.execute(query_check)
    existing = cursor.fetchone()

    if existing:
        return jsonify({
            "message": "Email sudah ada",
            "status": 409,
            "data": []
        }), 409

    query_insert = f"""
        INSERT INTO users (username, password, email, nama, gender, usia, pekerjaan, hobi, kota, rt, rw, kode_pos, longitude, latitude, no_hp)
        VALUES ('{username}', '{password_hash}', '{email}', '{nama}', '{gender}', {usia}, '{pekerjaan}', '{hobi}', '{kota}', {rt}, {rw}, {kode_pos}, {longitude}, {latitude}, '{no_hp}')
    """

    print(query_insert)

    cursor.execute(query_insert)
    conn.commit()

    return jsonify({
        "message": "Registrasi berhasil",
        "status": 201,
        "data": [
            {
                "username":username,
                "email":email
            }
        ]
    }), 201

@app.route('/paket', methods=['GET'])
def get_paket():
    query_select = "SELECT * FROM paket ORDER BY created_date DESC"
    cursor.execute(query_select)
    rows = cursor.fetchall()

    data = []
    for row in rows:
        if row[7] == "elec":
            cat = "Elektronik"
        elif row[7] == "doc":
            cat = "Dokumen"
        elif row[7] == "sparepart":
            cat = "Sparepart"
        elif row[7] == "textil":
            cat = "Tekstil"

        if row[10] == "reg":
            pengiriman = "D&L Reguler"
        elif row[10] == "eco":
            pengiriman = "D&L Eco (Ekonomis)"
        elif row[10] == "kilat":
            pengiriman = "D&L Super (Kilat)"
        elif row[10] == "kargo":
            pengiriman = "D&L Cargo"

        data.append({
            "id":row[0],
            "resi":row[1],
            "pengirim":row[2],
            "no_hp_pengirim":row[3],
            "penerima":row[4],
            "no_hp_penerima":row[5],
            "alamat_tujuan":row[6],
            "kategori":cat,
            "berat":row[8],
            "tanggal_pengiriman":row[9],
            "jenis_pengiriman":pengiriman,
            "estimasi":row[11],
            "tarif":row[12],
            "created_date":row[13],
            "created_by":row[14],
        })

    return jsonify({
        "message" : "Success",
        "status" : 200,
        "data" : data
    })


app.run(debug=True)