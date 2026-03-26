from flask import Flask, render_template, request, redirect, session, url_for, flash
from database import (
    db,                         # import db object dari database.py
    get_user_by_username, get_user_by_id, simpan_user,
    get_semua_paket, get_paket_by_id,
    tambah_paket_db, update_paket_db, hapus_paket_db,
    hitung_total_tarif, hitung_tarif_estimasi,
    isi_data_awal                # import fungsi seed data
)
from validation_registration import (
    validasi_registrasi, validasi_resi
)
import os

app = Flask(__name__)
app.secret_key = "gudang_ekspedisi_2026"

## untuk MySQL (comment jika menggunakan SQLite)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://DB_Admin:CRUDsql@localhost/Tugas_Project'

### Konfigurasi Flask-SQLAlchemy
# Sebelumnya: create_engine() di database.py
# Sekarang  : app.config 
# ============================================================
# app.config['SQLALCHEMY_DATABASE_URI']        = 'sqlite:///db_gudang_ekspedisi.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False   # matikan fitur berat di memory
db.init_app(app)

# with app.app_context(): db.create_all()
with app.app_context():
    db.create_all()
    isi_data_awal()
print("Database siap digunakan.")

# ==============
## Helper
# ==============
KATEGORI_LIST = [
    'Alat Olahraga', 'Kebutuhan Rumah Tangga', 'ATK (Alat Tulis Kantor)',
    'Dokumen', 'Elektronik', 'Pakaian/Tekstil', 'Sparepart'
]
JENIS_LIST = [
    'D&L Reguler', 'D&L Eco (Ekonomis)', 'D&L Super (Kilat)', 'D&L Cargo'
]


## ---- AUTH — Redirect ke login ----
@app.route('/')
def index():
    return redirect(url_for("login"))

## ---- LOGIN ----
@app.route("/login", methods=["GET","POST"])
def login():
    if "user_id" in session:
        return redirect(url_for("dashboard"))

    error = None
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"].strip()

        # User.query.filter_by(username=...).first()
        # = SELECT * FROM users WHERE username = ? LIMIT 1
        user = get_user_by_username(username)

        if user is None:
            error = "Username tidak terdaftar. Silakan registrasi."
        elif user.password != password:
            error = "Password salah."
        else:
            session['user_id']  = user.id
            session['username'] = user.username
            session['nama']     = user.nama
            flash(f"Selamat datang, {user.nama}!", "success")
            return redirect(url_for("dashboard"))

    return render_template("login.html", error=error)

## ---- REGISTER ----
@app.route('/register', methods=["GET","POST"])
def register():
    error     = {}
    form_data = {}
    list_hobi = []

    if request.method == 'POST':
        form_data = request.form.to_dict()
        error, list_hobi = validasi_registrasi(form_data)

        if not error:
            data_user = {
                'username':  form_data['username'].strip(),
                'password':  form_data['password'].strip(),
                'email':     form_data['email'].strip(),
                'nama':      form_data['nama'].strip().title(),
                'gender':    form_data['gender'],
                'usia':      int(form_data['usia']),
                'pekerjaan': form_data['pekerjaan'].strip().title(),
                'hobi':      ','.join(list_hobi),
                'kota':      form_data['kota'].strip().title(),
                'rt':        int(form_data.get('rt', 0) or 0),
                'rw':        int(form_data.get('rw', 0) or 0),
                'zipcode':   int(form_data['zipcode']),
                'lat':       float(form_data.get('lat', 0) or 0),
                'longitude': float(form_data.get('longitude', 0) or 0),
                'nohp':      int(form_data['nohp'])
            }
           
            # setara: INSERT INTO users VALUES (...)
            simpan_user(data_user)
            flash("Registrasi berhasil! Silakan login.", "success")
            return redirect(url_for('login'))

    return render_template("register.html", error=error, form_data=form_data)

# ---- LOGOUT ----
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# ---- DASHBOARD — READ semua paket ----
@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))

    search   = request.args.get('search', '').strip()
    kategori = request.args.get('kategori', '')
    jenis    = request.args.get('jenis', '')

    # Paket.query.all() = SELECT * FROM paket
    pakets      = get_semua_paket(search, kategori, jenis)
    total_tarif = hitung_total_tarif(pakets)
    # db.session.get(User, id) = SELECT * FROM users WHERE id = ?
    user        = get_user_by_id(session['user_id'])

    jml_kilat   = sum(1 for p in pakets if p.jenis_pengiriman == 'D&L Super (Kilat)')
    jml_reguler = sum(1 for p in pakets if p.jenis_pengiriman == 'D&L Reguler')
    jml_ekonomis= sum(1 for p in pakets if p.jenis_pengiriman == 'D&L Eco (Ekonomis)')
    jml_cargo   = sum(1 for p in pakets if p.jenis_pengiriman == 'D&L Cargo')

    return render_template('dashboard.html',
                           pakets=pakets,
                           user=user,
                           total_tarif=total_tarif,
                           jml_kilat=jml_kilat,
                           jml_reguler=jml_reguler,
                           jml_ekonomis=jml_ekonomis,
                           jml_cargo=jml_cargo,
                           kategori_list=KATEGORI_LIST,
                           jenis_list=JENIS_LIST,
                           search=search,
                           kategori_filter=kategori,
                           jenis_filter=jenis)

# ---- CRUD PAKET ----

### CREATE — Tambah paket baru
@app.route("/paket/tambah", methods=["GET", "POST"])
def tambah_paket():
    if "user_id" not in session:
        return redirect(url_for("login"))

    if request.method == "GET":
        return redirect(url_for('dashboard'))

    resi  = request.form.get('resi', '').strip().upper()
    berat = float(request.form.get('berat', 0))
    jenis = request.form.get('jenis_pengiriman', '')

    ok, message = validasi_resi(resi)
    if not ok:
        flash(f"Error Resi: {message}", "error")
        return redirect(url_for('dashboard'))

    tarif, estimasi = hitung_tarif_estimasi(berat, jenis)

    data = {
        'resi':               resi,
        'pengirim':           request.form.get('pengirim', ''),
        'no_hp_pengirim':     request.form.get('no_hp_pengirim', ''),
        'penerima':           request.form.get('penerima', ''),
        'no_hp_penerima':     request.form.get('no_hp_penerima', ''),
        'alamat_tujuan':      request.form.get('alamat_tujuan', ''),
        'kategori':           request.form.get('kategori', ''),
        'berat':              berat,
        'tanggal_pengiriman': request.form.get('tanggal_pengiriman', ''),
        'jenis_pengiriman':   jenis,
        'estimasi':           estimasi,
        'tarif':              tarif
    }
    # Paket object --> db.session.add() --> db.session.commit() --> database
    # setara: INSERT INTO paket VALUES (...)
    tambah_paket_db(data)
    flash(f"Paket {resi} berhasil ditambahkan! Tarif: Rp {tarif:,.0f}", "success")
    return redirect(url_for('dashboard'))


### UPDATE — Edit paket
@app.route("/paket/edit/<int:id>", methods=["GET", "POST"])
def edit_paket(id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    # db.session.get(Paket, id) = SELECT * FROM paket WHERE id = ?
    paket = get_paket_by_id(id)
    if paket is None:
        flash("Paket tidak ditemukan.", "error")
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        berat = float(request.form.get('berat', paket.berat))
        jenis = request.form.get('jenis_pengiriman', paket.jenis_pengiriman)
        tarif, estimasi = hitung_tarif_estimasi(berat, jenis)

        data = {
            'id':                 id,
            'pengirim':           request.form.get('pengirim', paket.pengirim),
            'no_hp_pengirim':     request.form.get('no_hp_pengirim', paket.no_hp_pengirim),
            'penerima':           request.form.get('penerima', paket.penerima),
            'no_hp_penerima':     request.form.get('no_hp_penerima', paket.no_hp_penerima),
            'alamat_tujuan':      request.form.get('alamat_tujuan', paket.alamat_tujuan),
            'kategori':           request.form.get('kategori', paket.kategori),
            'berat':              berat,
            'tanggal_pengiriman': request.form.get('tanggal_pengiriman', paket.tanggal_pengiriman),
            'jenis_pengiriman':   jenis,
            'estimasi':           estimasi,
            'tarif':              tarif
        }
        
        # setara: UPDATE paket SET ... WHERE id = ?
        update_paket_db(data)
        flash(f"Paket {paket.resi} berhasil diupdate!", "success")
        return redirect(url_for('dashboard'))

    return render_template('edit_paket.html', paket=paket,
                           kategori_list=KATEGORI_LIST, jenis_list=JENIS_LIST)


### DELETE — Hapus paket
@app.route("/paket/hapus/<int:id>", methods=["GET", "POST"])
def hapus_paket_route(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    paket = get_paket_by_id(id)
    if paket is None:
        flash("Paket tidak ditemukan.", "error")
        return redirect(url_for('dashboard'))

    resi = paket.resi
    # db.session.delete(object) + commit()
    # setara: DELETE FROM paket WHERE id = ?
    hapus_paket_db(id)
    flash(f"Paket {resi} berhasil dihapus.", "success")
    return redirect(url_for('dashboard'))


# ---- PROFIL USER ----
@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = get_user_by_id(session['user_id'])
    return render_template('profile.html', user=user)


if __name__ == "__main__":
    app.run(debug=True)