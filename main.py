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

app.run(debug=True)