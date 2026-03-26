from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    # merepresentasikan tabel 'user' dalam database
    __tablename__ = 'users'

    id         = db.Column(db.Integer, primary_key=True)
    username   = db.Column(db.String(50),  unique=True, nullable=False)
    password   = db.Column(db.String(100), nullable=False)
    email      = db.Column(db.String(100), unique=True, nullable=False)
    nama       = db.Column(db.String(100))
    gender     = db.Column(db.String(10))
    usia       = db.Column(db.Integer)
    pekerjaan  = db.Column(db.String(100))
    hobi       = db.Column(db.String(200))
    kota       = db.Column(db.String(100))
    rt         = db.Column(db.Integer)
    rw         = db.Column(db.Integer)
    zipcode    = db.Column(db.Integer)
    lat        = db.Column(db.Float)
    longitude  = db.Column(db.Float)
    nohp       = db.Column(db.BigInteger)

class Paket(db.Model):
    # merepresentasikan tabel 'paket' dalam database
    __tablename__ = 'paket'

    id                 = db.Column(db.Integer,  primary_key=True)
    resi               = db.Column(db.String(10),  unique=True, nullable=False)
    pengirim           = db.Column(db.String(100))
    no_hp_pengirim     = db.Column(db.String(20))
    penerima           = db.Column(db.String(100))
    no_hp_penerima     = db.Column(db.String(20))
    alamat_tujuan      = db.Column(db.String(200))
    kategori           = db.Column(db.String(50))
    berat              = db.Column(db.Float)
    tanggal_pengiriman = db.Column(db.String(20))
    jenis_pengiriman   = db.Column(db.String(50))
    estimasi           = db.Column(db.String(30))
    tarif              = db.Column(db.Float)

# ============================================================
# ISI DATA AWAL (seed data)
# ============================================================
def isi_data_awal():
    # Cek apakah data sudah ada
    # User.query.all() = SELECT * FROM users
    if User.query.count() == 0:
        users = [
            User(username='admin123', password='Admin@123', email='admin@mail.com',
                 nama='Admin Utama',    gender='Male',   usia=30, pekerjaan='Manager',
                 hobi='Membaca,Traveling,Fotografi', kota='Jakarta',
                 rt=5,  rw=10, zipcode=12345, lat=-6.2088,  longitude=106.8456, nohp=81234567890),

            User(username='dea2026',  password='Dea#2026',   email='dea@gmail.com',
                 nama='Dea Trishnanti', gender='Female', usia=25, pekerjaan='Staff Gudang',
                 hobi='Memasak,Menyanyi,Berkebun', kota='Bandung',
                 rt=3,  rw=8,  zipcode=40123, lat=-6.9175,  longitude=107.6191, nohp=85678901234),

            User(username='lauzia99', password='Lauzia@99',  email='lauzia@yahoo.com',
                 nama='Lauzia Fadhila', gender='Female', usia=23, pekerjaan='Admin',
                 hobi='Olahraga,Menggambar,Menulis', kota='Surabaya',
                 rt=7,  rw=12, zipcode=60271, lat=-7.2575,  longitude=112.7521, nohp=87654321098),

            User(username='user456',  password='User@456',   email='user@hotmail.com',
                 nama='Budi Santoso',  gender='Male',   usia=28, pekerjaan='Kurir',
                 hobi='Masak,Membaca,Coding', kota='Yogyakarta',
                 rt=2,  rw=6,  zipcode=55281, lat=-7.7956,  longitude=110.3695, nohp=89012345678),
        ]
        # db.session.add_all() = INSERT INTO users VALUES (...)
        db.session.add_all(users)
        db.session.commit()

    if Paket.query.count() == 0:
        pakets = [
            Paket(resi='EXP001', pengirim='Ahmad Wijaya',  no_hp_pengirim='081234567890',
                  penerima='Siti Rahayu',  no_hp_penerima='085678901234',
                  alamat_tujuan='Jl. Merdeka No. 10, Jakarta Pusat',
                  kategori='Elektronik',      berat=2.5, tanggal_pengiriman='15-02-2026',
                  jenis_pengiriman='D&L Super (Kilat)', estimasi='1-2 hari',   tarif=37500),

            Paket(resi='EXP002', pengirim='Budi Santoso',  no_hp_pengirim='082345678901',
                  penerima='Ani Kusuma',   no_hp_penerima='087654321098',
                  alamat_tujuan='Jl. Sudirman No. 25, Bandung',
                  kategori='Pakaian/Tekstil', berat=1.2, tanggal_pengiriman='14-02-2026',
                  jenis_pengiriman='D&L Reguler',        estimasi='2-5 hari',  tarif=12000),

            Paket(resi='EXP003', pengirim='Dewi Lestari',  no_hp_pengirim='089012345678',
                  penerima='Rudi Hartono', no_hp_penerima='081234567890',
                  alamat_tujuan='Jl. Gatot Subroto No. 50, Surabaya',
                  kategori='Dokumen',         berat=0.5, tanggal_pengiriman='16-02-2026',
                  jenis_pengiriman='D&L Super (Kilat)', estimasi='1-2 hari',   tarif=7500),
        ]
        # db.session.add_all() = INSERT INTO paket VALUES (...)
        db.session.add_all(pakets)
        db.session.commit()


# ============================================================
# HELPER — hitung tarif & estimasi berdasarkan berat + jenis
# ============================================================
def hitung_tarif_estimasi(berat, jenis):
    tabel = {
        'D&L Reguler':        (10000, '2-5 hari'),
        'D&L Eco (Ekonomis)': (7000,  '3-7 hari'),
        'D&L Super (Kilat)':  (15000, '1-2 hari'),
        'D&L Cargo':          (8000,  'Sesuai jadwal'),
    }
    tarif_per_kg, estimasi = tabel.get(jenis, (10000, '2-5 hari'))
    return berat * tarif_per_kg, estimasi


# ============================================================
# FUNGSI USERS — READ
# ============================================================
def get_user_by_username(username):
    # User.query = SELECT * FROM users
    # .filter_by() = WHERE username = ?
    return User.query.filter_by(username=username).first()


def get_user_by_id(id):
    # .get(id) = SELECT * FROM users WHERE id = ?
    return db.session.get(User, id)


def cek_username_ada(username):
    return User.query.filter_by(username=username).first() is not None


def cek_email_ada(email):
    return User.query.filter_by(email=email).first() is not None


def simpan_user(data):
    # setara: INSERT INTO users VALUES (...)
    user_baru = User(
        username  = data['username'],
        password  = data['password'],
        email     = data['email'],
        nama      = data['nama'],
        gender    = data['gender'],
        usia      = data['usia'],
        pekerjaan = data['pekerjaan'],
        hobi      = data['hobi'],
        kota      = data['kota'],
        rt        = data['rt'],
        rw        = data['rw'],
        zipcode   = data['zipcode'],
        lat       = data['lat'],
        longitude = data['longitude'],
        nohp      = data['nohp']
    )
    
    db.session.add(user_baru)
    db.session.commit()


# ============================================================
# FUNGSI PAKET — CRUD
# ============================================================
def get_semua_paket(search='', kategori='', jenis=''):
    # Paket.query = SELECT * FROM paket
    # .filter() = WHERE ...
    query = Paket.query

    if search:
        # LIKE '%...%' untuk pencarian sebagian teks
        query = query.filter(
            db.or_(
                Paket.resi.like(f'%{search}%'),
                Paket.pengirim.like(f'%{search}%'),
                Paket.penerima.like(f'%{search}%')
            )
        )
    if kategori:
        query = query.filter_by(kategori=kategori)
    if jenis:
        query = query.filter_by(jenis_pengiriman=jenis)

    return query.all()


def get_paket_by_id(id):
    # .get(id) = SELECT * FROM paket WHERE id = ?
    return db.session.get(Paket, id)


def cek_resi_ada(resi, exclude_id=None):
    query = Paket.query.filter_by(resi=resi)
    if exclude_id:
        query = query.filter(Paket.id != exclude_id)
    return query.first() is not None


def tambah_paket_db(data):
    # setara: INSERT INTO paket VALUES (...)
    paket_baru = Paket(
        resi               = data['resi'],
        pengirim           = data['pengirim'],
        no_hp_pengirim     = data['no_hp_pengirim'],
        penerima           = data['penerima'],
        no_hp_penerima     = data['no_hp_penerima'],
        alamat_tujuan      = data['alamat_tujuan'],
        kategori           = data['kategori'],
        berat              = data['berat'],
        tanggal_pengiriman = data['tanggal_pengiriman'],
        jenis_pengiriman   = data['jenis_pengiriman'],
        estimasi           = data['estimasi'],
        tarif              = data['tarif']
    )

    db.session.add(paket_baru)
    db.session.commit()


def update_paket_db(data):
    # setara: UPDATE paket SET ... WHERE id = ?
    paket = db.session.get(Paket, data['id'])
    paket.pengirim           = data['pengirim']
    paket.no_hp_pengirim     = data['no_hp_pengirim']
    paket.penerima           = data['penerima']
    paket.no_hp_penerima     = data['no_hp_penerima']
    paket.alamat_tujuan      = data['alamat_tujuan']
    paket.kategori           = data['kategori']
    paket.berat              = data['berat']
    paket.tanggal_pengiriman = data['tanggal_pengiriman']
    paket.jenis_pengiriman   = data['jenis_pengiriman']
    paket.estimasi           = data['estimasi']
    paket.tarif              = data['tarif']
    # tidak perlu db.session.add() lagi karena object sudah ada di session
    db.session.commit()


def hapus_paket_db(id):
    # setara: DELETE FROM paket WHERE id = ?
    paket = db.session.get(Paket, id)
    db.session.delete(paket)
    db.session.commit()


def hitung_total_tarif(pakets):
    total = 0
    for p in pakets:
        total += p.tarif
    return total    