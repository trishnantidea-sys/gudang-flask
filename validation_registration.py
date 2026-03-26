# Validasi email, username, password, dan form registrasi
# ============================================================

from database import cek_username_ada, cek_email_ada, cek_resi_ada


# ============================================================
# VALIDASI EMAIL
# ============================================================
def validasi_email(Email):
    if Email.count("@") != 1:
        return False, "Format Email salah (harus memiliki '@')"

    bagian = Email.split("@")
    User   = bagian[0]
    sisa   = bagian[1]

    if User == "":
        return False, "Format Username tidak boleh kosong"

    if not User[0].isalnum():
        return False, "Format Username harus diawali huruf atau angka"

    i = 0
    while i < len(User):
        char = User[i]
        if not (char.isalnum() or char == '_' or char == '.'):
            return False, "Format Username mengandung karakter tidak valid"
        i += 1

    if sisa.count(".") < 1:
        return False, "Format Email harus memiliki ekstensi"

    if sisa.count(".") > 2:
        return False, "Format Ekstensi maksimal 2 dot"

    parts    = sisa.split(".")
    Hosting  = parts[0]
    Ekstensi = parts[1:]

    if Hosting == "":
        return False, "Format Hosting tidak boleh kosong"

    i = 0
    while i < len(Hosting):
        if not Hosting[i].isalnum():
            return False, "Format Hosting hanya boleh huruf dan angka"
        i += 1

    idx = 0
    while idx < len(Ekstensi):
        ext = Ekstensi[idx]
        if ext == "":
            return False, "Format Ekstensi belum dimasukkan"
        if not ext.isalpha():
            return False, "Format Ekstensi hanya boleh huruf"
        if len(ext) > 5:
            return False, "Format Ekstensi maksimal 5 karakter"
        idx += 1

    return True, "Email valid"


# ============================================================
# VALIDASI USERNAME
# ============================================================
def validasi_username(username):
    jumlah_huruf = 0
    jumlah_angka = 0
    i = 0
    while i < len(username):
        if username[i].isalpha():
            jumlah_huruf += 1
        if username[i].isdigit():
            jumlah_angka += 1
        i += 1

    if jumlah_huruf == 0 or jumlah_angka == 0:
        return False, "Username harus kombinasi huruf dan angka"

    if not username.isalnum():
        return False, "Username tidak boleh mengandung karakter lain"

    if len(username) < 6 or len(username) > 20:
        return False, "Username harus terdiri dari 6-20 karakter"

    if cek_username_ada(username):
        return False, "Username sudah terdaftar. Gunakan Username yang berbeda."

    return True, "OK"


# ============================================================
# VALIDASI PASSWORD
# ============================================================
def validasi_password(password):
    if len(password) < 8:
        return False, "Password minimal 8 karakter"

    jumlah_huruf_besar     = 0
    jumlah_huruf_kecil     = 0
    jumlah_angka           = 0
    jumlah_karakter_khusus = 0
    char_khusus = "/.,@#$%"

    i = 0
    while i < len(password):
        char = password[i]
        if char.isupper():
            jumlah_huruf_besar += 1
        elif char.islower():
            jumlah_huruf_kecil += 1
        elif char.isdigit():
            jumlah_angka += 1
        elif char in char_khusus:
            jumlah_karakter_khusus += 1
        i += 1

    if not (jumlah_huruf_besar > 0 and jumlah_huruf_kecil > 0
            and jumlah_angka > 0 and jumlah_karakter_khusus > 0):
        return False, "Password harus kombinasi huruf besar, huruf kecil, angka, dan karakter khusus (/.,@#$%)"

    return True, "OK"


# ============================================================
# VALIDASI FORM REGISTRASI — kembalikan dict error
# ============================================================
def validasi_registrasi(form_data):
    error     = {}
    list_hobi = []

    # Username
    ok, msg = validasi_username(form_data.get('username', '').strip())
    if not ok:
        error['username'] = msg

    # Password
    ok, msg = validasi_password(form_data.get('password', '').strip())
    if not ok:
        error['password'] = msg

    # Email
    ok, msg = validasi_email(form_data.get('email', '').strip())
    if not ok:
        error['email'] = msg
    elif cek_email_ada(form_data.get('email', '').strip()):
        error['email'] = "Email sudah terdaftar."

    # Nama
    Nama = form_data.get('nama', '').strip()
    if not Nama.replace(" ", "").isalpha():
        error['nama'] = "Nama hanya boleh mengandung huruf"

    # Gender
    Gender = form_data.get('gender', '')
    if Gender not in ["Male", "Female"]:
        error['gender'] = "Jenis Kelamin tidak valid. Pilih 'Male' atau 'Female'"

    # Usia
    Usia = form_data.get('usia', '')
    if not Usia.isdigit():
        error['usia'] = "Usia harus berupa angka"
    elif not (17 <= int(Usia) <= 80):
        error['usia'] = "Usia harus antara 17-80 tahun"

    # Pekerjaan
    Pekerjaan = form_data.get('pekerjaan', '').strip()
    if not Pekerjaan.replace(" ", "").isalpha():
        error['pekerjaan'] = "Pekerjaan hanya boleh mengandung huruf"

    # Hobi
    hobi_str      = form_data.get('hobi', '')
    list_hobi_raw = hobi_str.replace(" ", "").split(",")
    list_hobi     = [h.strip() for h in list_hobi_raw if h.strip()]
    if len(list_hobi) < 3:
        error['hobi'] = "Isi hobi minimal 3 (pisahkan dengan koma)"
    elif not all(h.isalpha() for h in list_hobi):
        error['hobi'] = "Hobi hanya boleh mengandung huruf"

    # Kota
    NamaKota = form_data.get('kota', '').strip()
    if not NamaKota.replace(" ", "").isalpha():
        error['kota'] = "Nama Kota hanya boleh huruf"

    # RT
    RT = form_data.get('rt', '')
    if not RT.isdigit():
        error['rt'] = "RT harus berupa angka"

    # RW
    RW = form_data.get('rw', '')
    if not RW.isdigit():
        error['rw'] = "RW harus berupa angka"

    # Zipcode
    ZipCode = form_data.get('zipcode', '')
    if len(ZipCode) != 5 or not ZipCode.isdigit():
        error['zipcode'] = "Zip Code harus 5 digit angka"

    # Lat
    try:
        float(form_data.get('lat', ''))
    except:
        error['lat'] = "Latitude harus berupa angka desimal (contoh: -6.9175)"

    # Longitude
    try:
        float(form_data.get('longitude', ''))
    except:
        error['longitude'] = "Longitude harus berupa angka desimal (contoh: 107.6191)"

    # No HP
    NoHp = form_data.get('nohp', '')
    if len(NoHp) < 11 or len(NoHp) > 13 or not NoHp.isdigit():
        error['nohp'] = "No HP harus 11-13 digit angka"

    return error, list_hobi


# ============================================================
# VALIDASI RESI PAKET
# ============================================================
def validasi_resi(resi, exclude_id=None):
    if len(resi) != 6:
        return False, "Resi harus terdiri dari 6 karakter (contoh: EXP001)"
    if not resi.startswith("EXP"):
        return False, "Resi harus dimulai dengan 'EXP' (huruf kapital)"

    angka_bagian = resi[3:]
    i = 0
    while i < len(angka_bagian):
        if not angka_bagian[i].isdigit():
            return False, "3 karakter setelah 'EXP' harus berupa angka (contoh: EXP001)"
        i += 1

    if cek_resi_ada(resi, exclude_id):
        return False, "Nomor resi sudah terdaftar. Gunakan resi yang berbeda."

    return True, "Resi valid"