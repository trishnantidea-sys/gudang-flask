from flask import Flask, jsonify, request
# from flask import Flask, render_template, request, redirect, session, url_for, flash
# from db_sqlite import get_connection, init_db
# import datetime
import mysql.connector
import hashlib
from dotenv import load_dotenv
import os

app = Flask(__name__)
# app.secret_key = "gudang123"
# init_db()


# Load environment variables from the .env file (if present)
load_dotenv()

conn = mysql.connector.connect(**{
    "user": os.getenv('DB_USER'),
    "password": os.getenv('DB_PASSWORD'),
    "host": os.getenv('DB_HOST'),
    "database": os.getenv('DB_SCHEMA'),
})
cursor = conn.cursor()

## helper
# def hitung_tarif(berat, jenis):
#     tarif_map = {
#         "D&L Reguler": 10000,
#         "D&L Eco (Ekonomis)": 7000,
#         "D&L Super (Kilat)": 15000,
#         "D&L Cargo": 8000,
#     }
#     return berat * tarif_map.get(jenis, 10000)

# def estimasi_map(jenis):
#     est = {
#         "D&L Reguler": "2-5 hari",
#         "D&L Eco (Ekonomis)": "3-7 hari",
#         "D&L Super (Kilat)": "1-2 hari",
#         "D&L Cargo": "Sesuai jadwal",
#     }
#     return est.get(jenis, "-")



@app.route('/')
def root():
    response = {
        "message" : "gudang-flask API",
        "status" : 200,
        "data" : []
    }

    return jsonify(response)

# auth
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

    query_check = f"SELECT id FROM users WHERE username=%s"
    cursor.execute(query_check, (username,))
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

# @app.route("/logout")
# def logout():
#     session.clear()
#     return redirect(url_for("login"))

## dashboard
# @app.route("/dashboard")
# def dashboard():
#     if "user_id" not in session:
#         return redirect(url_for("login"))

#     conn = get_connection()
#     cur = conn.cursor()
#     cur.execute("SELECT * FROM paket ORDER BY id DESC")
#     paket = cur.fetchall()
#     cur.execute("SELECT COUNT(*) as total FROM paket")
#     total = cur.fetchone()["total"]
#     cur.execute("SELECT SUM(tarif) as total_tarif FROM paket")
#     total_tarif = cur.fetchone()["total_tarif"] or 0
#     conn.close()

#     return render_template("dashboard.html",
#                            paket=paket,
#                            total=total,
#                            total_tarif=total_tarif)

## CRUD Paket
# @app.route("/paket/tambah", methods=["GET", "POST"])
# def tambah_paket():
#     if "user_id" not in session:
#         return redirect(url_for("login"))

#     if request.method == "POST":
#         resi             = request.form["resi"].strip().upper()
#         pengirim         = request.form["pengirim"].strip()
#         no_hp_pengirim   = request.form["no_hp_pengirim"].strip()
#         penerima         = request.form["penerima"].strip()
#         no_hp_penerima   = request.form["no_hp_penerima"].strip()
#         alamat_tujuan    = request.form["alamat_tujuan"].strip()
#         kategori         = request.form["kategori"]
#         berat            = float(request.form["berat"])
#         tgl_pengiriman   = request.form["tanggal_pengiriman"]
#         jenis_pengiriman = request.form["jenis_pengiriman"]
#         estimasi         = estimasi_map(jenis_pengiriman)
#         tarif            = hitung_tarif(berat, jenis_pengiriman)

#         conn = get_connection()
#         cur = conn.cursor()
#         try:
#             cur.execute('''
#                 INSERT INTO paket (resi, pengirim, no_hp_pengirim, penerima, no_hp_penerima,
#                 alamat_tujuan, kategori, berat, tanggal_pengiriman, jenis_pengiriman, estimasi, tarif)
#                 VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
#             ''', (resi, pengirim, no_hp_pengirim, penerima, no_hp_penerima,
#                   alamat_tujuan, kategori, berat, tgl_pengiriman, jenis_pengiriman, estimasi, tarif))
#             conn.commit()
#             flash(f"Paket {resi} berhasil ditambahkan!", "success")
#             return redirect(url_for("dashboard"))
#         except:
#             flash("Resi sudah terdaftar!", "error")
#         finally:
#             conn.close()

#     return render_template("form_paket.html", mode="tambah", paket=None)


# @app.route("/paket/edit/<int:id>", methods=["GET", "POST"])
# def edit_paket(id):
#     if "user_id" not in session:
#         return redirect(url_for("login"))

#     conn = get_connection()
#     cur = conn.cursor()

#     if request.method == "POST":
#         pengirim         = request.form["pengirim"].strip()
#         no_hp_pengirim   = request.form["no_hp_pengirim"].strip()
#         penerima         = request.form["penerima"].strip()
#         no_hp_penerima   = request.form["no_hp_penerima"].strip()
#         alamat_tujuan    = request.form["alamat_tujuan"].strip()
#         kategori         = request.form["kategori"]
#         berat            = float(request.form["berat"])
#         tgl_pengiriman   = request.form["tanggal_pengiriman"]
#         jenis_pengiriman = request.form["jenis_pengiriman"]
#         estimasi         = estimasi_map(jenis_pengiriman)
#         tarif            = hitung_tarif(berat, jenis_pengiriman)

#         cur.execute('''
#             UPDATE paket SET pengirim=?, no_hp_pengirim=?, penerima=?, no_hp_penerima=?,
#             alamat_tujuan=?, kategori=?, berat=?, tanggal_pengiriman=?,
#             jenis_pengiriman=?, estimasi=?, tarif=?
#             WHERE id=?
#         ''', (pengirim, no_hp_pengirim, penerima, no_hp_penerima,
#               alamat_tujuan, kategori, berat, tgl_pengiriman,
#               jenis_pengiriman, estimasi, tarif, id))
#         conn.commit()
#         conn.close()
#         flash("Data paket berhasil diupdate!", "success")
#         return redirect(url_for("dashboard"))

#     cur.execute("SELECT * FROM paket WHERE id=?", (id,))
#     paket = cur.fetchone()
#     conn.close()
#     return render_template("form_paket.html", mode="edit", paket=paket)

app.run(debug=True)