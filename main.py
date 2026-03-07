from flask import Flask, jsonify, request, render_template, redirect, url_for
import hashlib
import datetime
from db_sqlite import get_connection, init_db

app = Flask(__name__)

# Initialize SQLite DB (Create tables if they don't exist)
init_db()

@app.route('/')
def root():
    return render_template('login.html')

@app.route('/login-page')
def login_page():
    return render_template('login.html')

@app.route('/register-page')
def register_page():
    return render_template('register.html')


@app.route('/login', methods=['POST'])
def login():
    # Ambil data dari form HTML
    email = request.form.get("email")
    password = request.form.get("password")

    password_hash = hashlib.md5(password.encode()).hexdigest()

    conn = get_connection()
    cursor = conn.cursor()

    query_check = "SELECT id, nama FROM users WHERE email=? AND password=?"
    cursor.execute(query_check, (email, password_hash))
    row = cursor.fetchone()
    conn.close()

    if row is not None:
        # Jika berhasil, pindah ke halaman paket
        return redirect(url_for('paket_page'))
    else:
        # Jika gagal, tampilkan pesan sederhana
        return "Email atau password salah! <a href='/login-page'>Kembali</a>"

@app.route('/register', methods=['POST'])
def registrasi():
    # Ambil data dari form HTML sesuai field di DB
    username = request.form.get("username")
    password = request.form.get("password")
    email = request.form.get("email")
    nama = request.form.get("nama")
    gender = request.form.get("gender")
    usia = request.form.get("usia")
    pekerjaan = request.form.get("pekerjaan")
    hobi = request.form.get("hobi")
    kota = request.form.get("kota")
    rt = request.form.get("rt")
    rw = request.form.get("rw")
    zipcode = request.form.get("zipcode")
    lat = request.form.get("lat")
    longitude = request.form.get("longitude")
    nohp = request.form.get("nohp")

    password_hash = hashlib.md5(password.encode()).hexdigest()

    conn = get_connection()
    cursor = conn.cursor()

    # Cek apakah username sudah ada
    query_check_user = "SELECT id FROM users WHERE username=?"
    cursor.execute(query_check_user, (username,))
    if cursor.fetchone():
        conn.close()
        return "Username sudah ada! <a href='/register-page'>Kembali</a>"

    # Cek apakah email sudah ada
    query_check_email = "SELECT id FROM users WHERE email=?"
    cursor.execute(query_check_email, (email,))
    if cursor.fetchone():
        conn.close()
        return "Email sudah ada! <a href='/register-page'>Kembali</a>"

    # Simpan data baru (Urutan sesuai gambar DB)
    query_insert = """
        INSERT INTO users (username, password, email, nama, gender, usia, pekerjaan, hobi, kota, rt, rw, zipcode, lat, longitude, nohp)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    
    # Konversi tipe data agar sesuai DB (INTEGER untuk rt/rw/usia, REAL untuk lat/long)
    cursor.execute(query_insert, (
        username, 
        password_hash, 
        email, 
        nama, 
        gender, 
        int(usia) if usia else 0, 
        pekerjaan, 
        hobi, 
        kota, 
        int(rt) if rt else 0, 
        int(rw) if rw else 0, 
        int(zipcode) if zipcode else 0, 
        float(lat) if lat else 0.0, 
        float(longitude) if longitude else 0.0, 
        nohp
    ))
    
    conn.commit()
    conn.close()

    return "Registrasi berhasil! <a href='/login-page'>Silakan Login</a>"

@app.route('/paket', methods=['GET'])
def get_paket():
    conn = get_connection()
    cursor = conn.cursor()
    query_select = "SELECT * FROM paket ORDER BY id DESC"
    cursor.execute(query_select)
    rows = cursor.fetchall()
    conn.close()
    return jsonify(rows)

@app.route('/paket-page')
def paket_page():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM paket ORDER BY id DESC")
    daftar_paket = cursor.fetchall()
    conn.close()
    return render_template('paket.html', paket=daftar_paket)

@app.route('/tambah-paket-page')
def tambah_paket_page():
    return render_template('tambah_paket.html')

@app.route('/tambah-paket', methods=['POST'])
def tambah_paket():
    resi = request.form.get("resi")
    pengirim = request.form.get("pengirim")
    no_hp_pengirim = request.form.get("no_hp_pengirim")
    penerima = request.form.get("penerima")
    no_hp_penerima = request.form.get("no_hp_penerima")
    alamat = request.form.get("alamat_tujuan")
    kategori = request.form.get("kategori")
    berat = request.form.get("berat")
    tanggal = request.form.get("tanggal_pengiriman")
    jenis = request.form.get("jenis_pengiriman")
    
    # Perhitungan Otomatis
    berat_val = float(berat) if berat else 0
    if jenis == 'Reguler':
        tarif = int(berat_val * 10000)
        days = 5
    elif jenis == 'Eco':
        tarif = int(berat_val * 7000)
        days = 7
    elif jenis == 'Kilat':
        tarif = int(berat_val * 15000)
        days = 2
    elif jenis == 'Kargo':
        tarif = int(berat_val * 8000)
        days = 7
    else:
        tarif = 0
        days = 0

    estimasi = ""
    if tanggal:
        dt_kirim = datetime.datetime.strptime(tanggal, '%Y-%m-%d')
        estimasi = dt_kirim + datetime.timedelta(days=days)

    created_date = datetime.datetime.now()

    conn = get_connection()
    cursor = conn.cursor()
    query = """INSERT INTO paket 
               (resi, pengirim, no_hp_pengirim, penerima, no_hp_penerima, alamat_tujuan, kategori, berat, tanggal_pengiriman, jenis_pengiriman, estimasi, tarif, created_date)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
    cursor.execute(query, (resi, pengirim, no_hp_pengirim, penerima, no_hp_penerima, alamat, kategori, berat_val, tanggal, jenis, estimasi, tarif, created_date))
    conn.commit()
    conn.close()
    return redirect(url_for('paket_page'))

@app.route('/edit-paket-page/<int:id>')
def edit_paket_page(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM paket WHERE id=?", (id,))
    data = cursor.fetchone()
    conn.close()
    return render_template('edit_paket.html', data=data)

@app.route('/edit-paket/<int:id>', methods=['POST'])
def edit_paket(id):
    resi = request.form.get("resi")
    pengirim = request.form.get("pengirim")
    no_hp_pengirim = request.form.get("no_hp_pengirim")
    penerima = request.form.get("penerima")
    no_hp_penerima = request.form.get("no_hp_penerima")
    alamat = request.form.get("alamat_tujuan")
    kategori = request.form.get("kategori")
    berat = request.form.get("berat")
    tanggal = request.form.get("tanggal_pengiriman")
    jenis = request.form.get("jenis_pengiriman")

    # Perhitungan Otomatis
    berat_val = float(berat) if berat else 0
    if jenis == 'Reguler':
        tarif = int(berat_val * 10000)
        days = 5
    elif jenis == 'Eco':
        tarif = int(berat_val * 7000)
        days = 7
    elif jenis == 'Kilat':
        tarif = int(berat_val * 15000)
        days = 2
    elif jenis == 'Kargo':
        tarif = int(berat_val * 8000)
        days = 7
    else:
        tarif = 0
        days = 0

    estimasi = ""
    if tanggal:
        dt_kirim = datetime.datetime.strptime(tanggal, '%Y-%m-%d')
        estimasi = dt_kirim + datetime.timedelta(days=days)

    conn = get_connection()
    cursor = conn.cursor()
    query = """UPDATE paket SET 
               resi=?, pengirim=?, no_hp_pengirim=?, penerima=?, no_hp_penerima=?, alamat_tujuan=?, kategori=?, berat=?, tanggal_pengiriman=?, jenis_pengiriman=?, estimasi=?, tarif=?
               WHERE id=?"""
    cursor.execute(query, (resi, pengirim, no_hp_pengirim, penerima, no_hp_penerima, alamat, kategori, berat_val, tanggal, jenis, estimasi, tarif, id))
    conn.commit()
    conn.close()
    return redirect(url_for('paket_page'))

@app.route('/hapus-paket/<int:id>')
def hapus_paket(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM paket WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('paket_page'))

app.run(debug=True, port=5001)