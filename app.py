from flask import Flask, render_template, request, redirect, url_for, session, make_response, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length, URL
from functools import wraps
from flask_bootstrap import Bootstrap
from sqlalchemy import UniqueConstraint, exc
import os
import datetime
import timeit
import sys
from flask_uploads import UploadSet, configure_uploads, IMAGES, ALL
from flask_migrate import Migrate
from sqlalchemy import func
from flask_cors import CORS
import random
import numpy as np
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tH1Sv3ryd4nger0u$;'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/hospitaldb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['UPLOADED_PHOTOS_DEST'] = 'static/img'
photos = UploadSet('photos', IMAGES, ALL)
configure_uploads(app, photos)
db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
bcrypt = Bcrypt(app)
migrate = Migrate(db,app)
CORS(app)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

class LoginForm(FlaskForm):
    username = StringField('', validators=[InputRequired(), Length(min=5, max=50)], render_kw={'autofocus':True, 'placeholder':'Username'})
    password = PasswordField('', validators=[InputRequired(), Length(min=5, max=100)], render_kw={'autofocus':True, 'placeholder':'Password'})

class CariData(FlaskForm):
    cari = StringField('', validators=[InputRequired(), Length(max=150)], render_kw={'placeholder':'Cari Produk'})

class Login(db.Model):
    __tablename__ = 'login'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80), nullable=False)

    def __init__(self,username,password):
        self.username = username
        self.password = bcrypt.generate_password_hash(password)

    def __repr__(self):
        return '[%s,%s]' % (self.username,self.password)

class Karyawan(db.Model):
    __tablename__ = 'karyawan'
    id = db.Column(db.Integer, primary_key=True)
    tanggal = db.Column(db.DateTime, default=datetime.datetime.now())
    nama = db.Column(db.String(100))
    np = db.Column(db.Integer)
    jabatan = db.Column(db.String(80))
    gaji = db.Column(db.Integer)
    lembur = db.Column(db.Integer)
    kasbon = db.Column(db.Integer)
    iuran = db.Column(db.Integer)
    total = db.Column(db.Integer)
    keterangan = db.Column(db.String(90))

    def __init__(self,nama,np,jabatan,gaji,lembur,kasbon,iuran,total,keterangan):
        self.nama = nama
        self.np = np
        self.jabatan = jabatan
        self.gaji = gaji
        self.lembur = lembur
        self.kasbon = kasbon
        self.iuran = iuran
        self.total = total
        self.keterangan = keterangan

    def __repr__(self):
        return '[%s,%s,%s,%s,%s,%s,%s,%s,%s]' % (self.nama,self.np,self.jabatan,self.gaji,self.lembur,self.kasbon,self.iuran,self.total,self.keterangan)

class Dokter(db.Model):
    __tablename__ = 'dokter'
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100), unique=True)
    alamat = db.Column(db.String(80))
    noHP = db.Column(db.String(80))
    spesialis = db.Column(db.String(80))
    jadwal = db.Column(db.String(180))
    biaya = db.Column(db.Integer)
    keterangan = db.Column(db.String(90))

    def __init__(self,nama,alamat,noHP,spesialis,jadwal,biaya,keterangan):
        self.nama = nama
        self.alamat = alamat
        self.noHP = noHP
        self.spesialis = spesialis
        self.jadwal = jadwal
        self.biaya = biaya
        self.keterangan = keterangan

    def __repr__(self):
        return '[%s,%s,%s,%s,%s,%s,%s]' % (self.nama,self.alamat,self.noHP,self.spesialis,
                                            self.jadwal,self.biaya,self.keterangan)

class Pasien(db.Model):
    __tablename__ = 'pasien'
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100))
    usia = db.Column(db.String(50))
    status = db.Column(db.String(80))
    jenisklm = db.Column(db.String(35))
    alamat = db.Column(db.String(95))
    kamar = db.Column(db.String(60))
    keluhan = db.Column(db.String(55))
    metode = db.Column(db.String(60))
    checkin = db.Column(db.String(80))
    checkout = db.Column(db.String(80))
    keterangan = db.Column(db.String(80))

    def __init__(self,nama,usia,status,jenisklm,alamat,kamar,keluhan,metode,checkin,checkout,keterangan):
        self.nama = nama
        self.usia = usia
        self.status = status
        self.jenisklm = jenisklm
        self.alamat = alamat
        self.kamar = kamar
        self.keluhan = keluhan
        self.metode = metode
        self.checkin = checkin
        self.checkout = checkout
        self.keterangan = keterangan

    def __repr__(self):
        return '[%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s]' % (self.nama,self.usia,self.status,self.jenisklm,self.alamat,self.kamar,self.keluhan,self.metode,self.checkin,self.checkout,self.keterangan)

class Mitra(db.Model):
    __tablename__ = 'mitra'
    id = db.Column(db.Integer, primary_key=True)
    perusahaan = db.Column(db.String(80), unique=True)
    tanggal = db.Column(db.String(80))
    keterangan = db.Column(db.String(90))

    def __init__(self,perusahaan,tanggal,keterangan):
        self.perusahaan = perusahaan
        self.tanggal = tanggal
        self.keterangan = keterangan

    def __repr__(self):
        return '[%s,%s,%s]' % (self.perusahaan,self.tanggal,self.keterangan)

class Obat(db.Model):
    __tablename__ = 'obat'
    id = db.Column(db.Integer, primary_key=True)
    tanggal = db.Column(db.String(70))
    jenisObat = db.Column(db.String(85))
    namaObat = db.Column(db.String(60), nullable=False)
    hBeli = db.Column(db.Integer)
    hJual = db.Column(db.Integer, nullable=False)
    exp = db.Column(db.String(80))
    ready = db.Column(db.String(50))
    satuan = db.Column(db.String(80))
    stok = db.Column(db.Integer)
    total = db.Column(db.Integer)
    sisa = db.Column(db.Integer)

    def __init__(self,tanggal,jenisObat,namaObat,hBeli,hJual,exp,ready,satuan,stok,total,sisa):
        self.tanggal = tanggal
        self.jenisObat = jenisObat
        self.namaObat = namaObat
        self.hBeli = hBeli
        self.hJual = hJual
        self.exp = exp
        self.ready = ready
        self.satuan = satuan
        self.stok = stok
        self.total = total
        self.sisa = sisa
        
    def __repr__(self):
        return '[%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s]' % '{} - {}'.format(self.tanggal,self.jenisObat,self.namaObat,self.hBeli,
                                                                       self.hJual,self.exp,self.ready,self.satuan,self.stok,self.total,self.sisa)

    def as_dict(self):
        return {'nama': self.namaObat, 'harga': self.hJual}

class Pengadaan(db.Model):
    __tablename__ = 'pengadaan'
    id = db.Column(db.Integer, primary_key=True)
    nFaktur = db.Column(db.String(80))
    tgl = db.Column(db.String(100))
    suplier = db.Column(db.String(150))
    noHp = db.Column(db.String(80))
    alamat = db.Column(db.String(120))

    def __init__(self,nFaktur,tgl,suplier,noHp,alamat):
        self.nFaktur = nFaktur
        self.tgl = tgl
        self.suplier = suplier
        self.noHp = noHp
        self.alamat = alamat

    def __repr__(self):
        return "[%s,%s,%s,%s,%s]" % (self.nFaktur,self.tgl,self.suplier,self.noHp,self.alamat)

class Iuran(db.Model):
    __tablename__ = 'iuran'
    id = db.Column(db.Integer, primary_key=True)
    tanggal = db.Column(db.DateTime, default=datetime.datetime.now())
    tagihan = db.Column(db.String(85))
    jumlah = db.Column(db.Integer)
    keterangan = db.Column(db.String(90))

    def __init__(self,tagihan,jumlah,keterangan):
        self.tagihan = tagihan
        self.jumlah = jumlah
        self.keterangan = keterangan

    def __repr__(self):
        return '[%s,%s,%s]' % (self.tagihan,self.jumlah,self.keterangan)

class Pembelanjaan(db.Model):
    __tablename__ = 'pembelanjaan'
    id = db.Column(db.Integer, primary_key=True)
    nBarang = db.Column(db.String(100))
    satuan = db.Column(db.String(80))
    volume = db.Column(db.Integer)
    harga = db.Column(db.Integer)
    total = db.Column(db.Integer)
    tanggal = db.Column(db.String(70))
    keterangan = db.Column(db.String(100))

    def __init__(self,nBarang,satuan,volume,harga,total,tanggal,keterangan):
        self.nBarang = nBarang
        self.satuan = satuan
        self.volume = volume
        self.harga = harga
        self.total = total
        self.tanggal = tanggal
        self.keterangan = keterangan

    def __repr__(self):
        return '[%s,%s,%s,%s,%s,%s,%s]' % (self.nBarang,self.satuan,self.volume,self.harga,self.total,self.tanggal,self.keterangan)

class RekamMedis(db.Model):
    __tablename__ = 'rekammedis'
    id = db.Column(db.Integer, primary_key=True)
    nPasien= db.Column(db.String(100))
    dokter = db.Column(db.String(85))
    keluhan = db.Column(db.String(70))
    diagnosa = db.Column(db.String(80))
    obat = db.Column(db.String(70))
    tindakan = db.Column(db.String(90))
    tanggal = db.Column(db.DateTime, default=datetime.datetime.now())

    def __init__(self,nPasien,dokter,keluhan,diagnosa,obat,tindakan):
        self.nPasien = nPasien
        self.dokter = dokter
        self.keluhan = keluhan
        self.diagnosa = diagnosa
        self.obat = obat
        self.tindakan = tindakan

    def __repr__(self):
        return '[%s,%s,%s,%s,%s,%s]' % (self.nPasien,self.dokter,self.keluhan,self.diagnosa,self.obat,self.tindakan)

class Rontgen(db.Model):
    __tablename__ = 'rontgen'
    id = db.Column(db.Integer, primary_key=True)
    tanggal = db.Column(db.DateTime, default=datetime.datetime.now())
    nDokter = db.Column(db.String(100))
    npasien = db.Column(db.String(100))
    usia = db.Column(db.String(70))
    gender = db.Column(db.String(50))
    diagnosa = db.Column(db.String(90))
    npetugas = db.Column(db.String(100))
    keterangan = db.Column(db.String(80))

    def __init__(self,nDokter,npasien,usia,gender,diagnosa,npetugas,keterangan):
        self.nDokter = nDokter
        self.npasien = npasien
        self.usia = usia
        self.gender = gender
        self.diagnosa = diagnosa
        self.npetugas = npetugas
        self.keterangan = keterangan

    def __repr__(self):
        return '[%s,%s,%s,%s,%s,%s,%s]' % (self.nDokter,self.npasien,self.usia,self.gender,self.diagnosa,self.npetugas,self.keterangan)

class Pendaftaran(db.Model):
    __tablename__ = 'pendaftaran'
    id = db.Column(db.Integer, primary_key=True)
    rm = db.Column(db.String(50))
    nama = db.Column(db.String(100))
    usia = db.Column(db.String(70))
    gender = db.Column(db.String(75))
    status = db.Column(db.String(80))
    golDarah = db.Column(db.String(20))
    ttl = db.Column(db.String(200))
    ktp = db.Column(db.String(100))
    pJawab = db.Column(db.String(70))
    alamat = db.Column(db.String(80))
    kategori = db.Column(db.String(100))
    jenisKmr = db.Column(db.String(100))
    biaya = db.Column(db.Integer)
    metode = db.Column(db.String(80))
    tanggal = db.Column(db.DateTime, default=datetime.datetime.now())
    igd_id = db.Column(db.Integer, db.ForeignKey('igd.id'))

    def __init__(self,rm,nama,usia,gender,status,golDarah,ttl,ktp,pJawab,alamat,kategori,jenisKmr,biaya,metode):
        self.rm = rm
        self.nama = nama
        self.usia = usia
        self.gender = gender
        self.status = status
        self.golDarah = golDarah
        self.ttl = ttl
        self.ktp = ktp
        self.pJawab = pJawab
        self.alamat = alamat
        self.kategori = kategori
        self.jenisKmr = jenisKmr
        self.biaya = biaya
        self.metode = metode

    def __repr__(self):
        return '[%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s]' % (self.rm,self.nama,self.usia,self.gender,self.status,self.golDarah,self.ttl,self.ktp,self.pJawab,
                                                             self.alamat,self.kategori,self.jenisKmr,self.biaya,self.metode)

class Laboratorium(db.Model):
    __tablename__ = 'laboratorium'
    id = db.Column(db.Integer, primary_key=True)
    tanggal = db.Column(db.DateTime, default=datetime.datetime.now())
    nDokter = db.Column(db.String(100))
    nama = db.Column(db.String(100))
    usia = db.Column(db.String(70))
    gender = db.Column(db.String(70))
    status = db.Column(db.String(75))
    golDarah = db.Column(db.String(20))
    keluhan = db.Column(db.String(80))
    hasil = db.Column(db.String(80))

    def __init__(self,nDokter,nama,usia,gender,status,golDarah,keluhan,hasil):
        self.nDokter = nDokter
        self.nama = nama
        self.usia = usia
        self.gender = gender
        self.status = status
        self.golDarah = golDarah
        self.keluhan = keluhan
        self.hasil = hasil

    def __repr__(self):
        return '[%s,%s,%s,%s,%s,%s,%s,%s]' % (self.nDokter,self.nama,self.usia,self.gender,self.status,self.golDarah,self.keluhan,self.hasil)

class Kasir(db.Model):
    __tablename__ = 'kasir'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    item = db.Column(db.Text)
    qty = db.Column(db.Integer)
    price = db.Column(db.Integer)
    total = db.Column(db.Integer)
    obat_id = db.relationship('BayarPasien', backref='kasir', lazy='dynamic')

    def __init__(self,item,qty,price,total):
        self.item = item
        self.qty = qty
        self.price = price
        self.total = total

    def as_dict(self):
        return {'item': self.item, 'qty': self.qty, 'price': self.price, 'total': self.total}

class BayarPasien(db.Model):
    __tablename__ = 'bayarpasien'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    wkt = db.Column(db.DateTime, default=datetime.datetime.now())
    rm = db.Column(db.String(60))
    nama = db.Column(db.String(110))
    dokter = db.Column(db.String(110))
    bDokter = db.Column(db.Integer)
    status = db.Column(db.String(70))
    kasirnya = db.Column(db.Integer, db.ForeignKey('kasir.id'))

    def __init__(self,rm,nama,dokter,bDokter,status):
        self.rm = rm
        self.nama = nama
        self.dokter = dokter
        self.bDokter = bDokter
        self.status = status

    def __repr__(self):
        return '[%s,%s,%s,%s,%s]' % (self.rm,self.nama,self.dokter,self.bDokter,self.status)


class Belanja(db.Model):
    __tablename__ = 'belanja'
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(100))
    price = db.Column(db.Integer)
    qty = db.Column(db.Integer)
    total = db.Column(db.Integer)

    def __init__(self,item,price,qty,total):
        self.item = item
        self.price = price
        self.qty = qty
        self.total = total

    def __repr__(self):
        return '[%s,%s,%s,%s]' % (self.item,self.price,self.qty,self.total)

class IGD(db.Model):
    __tablename__ = 'igd'
    id = db.Column(db.Integer, primary_key=True)
    rm = db.Column(db.String(50))
    nama = db.Column(db.String(100))
    alamat = db.Column(db.String(200))
    usia = db.Column(db.String(80))
    tanggal = db.Column(db.String(120))
    pemFisik = db.Column(db.String(300))
    diagnosa = db.Column(db.String(300))
    tindakan = db.Column(db.String(300))
    resep = db.Column(db.String(400))
    dokter = db.Column(db.String(100))
    biaya = db.Column(db.Integer)
    pendaftar = db.relationship('Pendaftaran', backref='igd', lazy='dynamic')

    def __init__(self,rm,nama,alamat,usia,tanggal,pemFisik,diagnosa,tindakan,resep,dokter,biaya):
        self.rm = rm
        self.nama = nama
        self.usia = usia
        self.alamat = alamat
        self.tanggal = tanggal
        self.pemFisik = pemFisik
        self.diagnosa = diagnosa
        self.tindakan = tindakan
        self.resep = resep
        self.dokter = dokter
        self.biaya = biaya

    def __repr__(self):
        return '[%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s]' % (self.rm,self.nama,self.usia,self.alamat,self.tanggal,self.pemFisik,self.diagnosa,
                                                    self.tindakan,self.resep,self.dokter,self.biaya)

class TebusObat(db.Model):
    __tablename__ = 'tebusobat'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    rm = db.Column(db.String(50))
    nama = db.Column(db.String(100))
    resep = db.Column(db.String(400))
    dokter = db.Column(db.String(100))
    biaya = db.Column(db.Integer)

    def __init__(self,rm,nama,resep,dokter,biaya):
        self.rm = rm
        self.nama = nama
        self.resep = resep
        self.dokter = dokter
        self.biaya = biaya

    def __repr__(self):
        return '[%s,%s,%s,%s,%s]' % (self.rm,self.nama,self.dokter,self.biaya)

class History(db.Model):
    __tablename__= 'history'
    id = db.Column(db.Integer, primary_key=True)
    waktu = db.Column(db.DateTime, default=datetime.datetime.now())
    noreg = db.Column(db.Integer, autoincrement=True)
    rm = db.Column(db.String(90))
    nama = db.Column(db.String(110))
    bDokter = db.Column(db.Integer)
    biaya = db.Column(db.Integer)
    belanjaan = db.Column(db.Text)
    tot_belanjaan = db.Column(db.Integer)
    total = db.Column(db.Integer)

    def __init__(self,rm,nama,bDokter,biaya,belanjaan,tot_belanjaan,total):
        self.rm = rm
        self.nama = nama
        self.bDokter = bDokter
        self.biaya = biaya
        self.belanjaan = belanjaan
        self.tot_belanjaan = tot_belanjaan
        self.total = total

    def as_dict(self):
        return {'rm': self.rm, 'nama': self.nama, 'bDokter': self.bDokter, 'biaya': self.biaya, 'belanjaan': self.belanjaan,
                'tot_belanjaan': self.tot_belanjaan, 'total': self.total}

db.create_all()
    
@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Login.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                session['logged_in'] = True
                return redirect(url_for('dashboard'))
        pesan = "Username atau Password anda salah"
        return render_template('login.html', pesan=pesan, form=form)
    return render_template('login.html', form=form)
    
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    return wrap
               
@app.route('/dashboard')
@is_logged_in
def dashboard():
    row = db.session.query(Dokter).count()
    row2 = db.session.query(Pendaftaran).count()
    #P1
    laba = Pendaftaran.query.all()
    uang = []
    for lb in laba:
        i = lb.biaya
        uang.insert(0,i)
    uang = sum(uang)
    if 10000 <= uang < 100000:
        uang = int(uang)
    elif 100000 <= uang < 1000000:
        uang = int(uang)
    elif uang >= 1000000:
        uang = int(uang)
    elif uang >= 1000000000 or uang == 1000000000:
        uang = int(uang)
    else:
        uang = int(uang)
    ung = int(uang)
    # Kasir
    apt = Kasir.query.all()
    ap = []
    for a in apt:
        i = a.total
        ap.insert(0,i)
    ap = sum(ap)
    total1 = int(ap) + int(ung)
    # Iuran
    I1 = Iuran.query.all()
    b1 = []
    for p in I1:
        i = p.jumlah
        b1.insert(0,i)
    b1 = sum(b1)
    # Pengeluaran
    pmb1 = Pembelanjaan.query.all()
    b2 = []
    for pm in pmb1:
        i = pm.total
        b2.insert(0,i)
    b2 = sum(b2)
    totPeng = int(b1) + int(b2)
    # Pembelanjaan
    count1 = Pembelanjaan.query.all()
    c1 = []
    for co1 in count1:
        i = co1.total
        c1.insert(0,i)
    c1 = sum(c1)
    # Iuran
    count2 = Iuran.query.all()
    c2 = []
    for co2 in count2:
        i = co2.jumlah
        c2.insert(0,i)
    c2 = sum(c2)
    total = int(c1) + int(c2)
    tot = int(total) - int(1000000000)
    # Profit
    obat = Obat.query.all()
    jml = []
    for ob in obat:
        i = ob.total
        jml.insert(0,i)
    jml = sum(jml)
    return render_template('dashboard.html', row=row, row2=row2, ung=ung, ap=ap, total1=total1, totPeng=totPeng, tot=tot, jml=jml)

@app.route('/dokter')
@is_logged_in
def dokter():
    return render_template('dokter.html', containers=Dokter.query.all())

@app.route('/tambahdokter', methods=['GET','POST'])
@is_logged_in
def tambahdokter():
    if request.method == 'POST':
        nama = request.form['nama']
        alamat = request.form['alamat']
        noHP = request.form['nohp']
        spesialis = request.form['spesialis']
        jadwal = request.form['jadwal']
        biaya = request.form['biaya']
        keterangan = request.form['keterangan']
        data = Dokter(nama,alamat,noHP,spesialis,jadwal,biaya,keterangan)
        db.session.add(data)
        db.session.commit()
        return redirect(url_for('dokter'))

@app.route('/editdokter/<id>', methods=['GET','POST'])
@is_logged_in
def editdokter(id):
    data = Dokter.query.filter_by(id=id).first()
    if request.method == 'POST':
        data.nama = request.form['nama']
        data.alamat = request.form['alamat']
        data.noHP = request.form['nohp']
        data.spesialis = request.form['spesialis']
        data.jadwal = request.form['jadwal']
        data.biaya = request.form['biaya']
        data.keterangan = request.form['keterangan']
        db.session.add(data)
        db.session.commit()
        return redirect(url_for('dokter'))
    else:
        return render_template('editdokter.html', data=data)

@app.route('/hapusdokter/<id>', methods=['GET','POST'])
@is_logged_in
def hapusdokter(id):
    data = Dokter.query.filter_by(id=id).first()
    db.session.delete(data)
    db.session.commit()
    return redirect(url_for('dokter'))

@app.route('/pasien')
@is_logged_in
def pasien():
    return render_template('pasien.html', containers=Pasien.query.all())

@app.route('/tambahpasien', methods=['GET','POST'])
@is_logged_in
def tambahpasien():
    if request.method == 'POST':
        nama = request.form['nama']
        usia = request.form['usia']
        status = request.form['status']
        jenisklm = request.form['jenisklm']
        alamat = request.form['alamat']
        kamar = request.form['kamar']
        keluhan = request.form['keluhan']
        metode = request.form['metode']
        checkin = request.form['checkin']
        checkout = request.form['checkout']
        keterangan = request.form['keterangan']
        data = Pasien(nama,usia,status,jenisklm,alamat,kamar,keluhan,metode,checkin,checkout,keterangan)
        db.session.add(data)
        db.session.commit()
        return redirect(url_for('pasien'))

@app.route('/editpasien/<id>', methods=['GET','POST'])
@is_logged_in
def editpasien(id):
    data = Pasien.query.filter_by(id=id).first()
    if request.method == 'POST':
        data.nama = request.form['nama']
        data.usia = request.form['usia']
        data.status = request.form['status']
        data.jenisklm = request.form['jenisklm']
        data.alamat = request.form['alamat']
        data.kamar = request.form['kamar']
        data.keluhan = request.form['keluhan']
        data.metode = request.form['metode']
        data.checkin = request.form['checkin']
        data.checkout = request.form['checkout']
        data.keterangan = request.form['keterangan']
        db.session.add(data)
        db.session.commit()
        return redirect(url_for('pasien'))
    else:
        return render_template('editpasien.html', data=data)

@app.route('/hapuspasien/<id>', methods=['GET','POST'])
@is_logged_in
def hapuspasien(id):
    data = Pasien.query.filter_by(id=id).first()
    db.session.delete(data)
    db.session.commit()
    return redirect(url_for('pasien'))

@app.route('/tindakan')
@is_logged_in
def tindakan():
    return render_template('tindakan.html', containers=Tindakan.query.all())

@app.route('/tambahtindakan', methods=['GET','POST'])
@is_logged_in
def tambahtindakan():
    if request.method == 'POST':
        tindak = request.form['tindak']
        harga = request.form['harga']
        keterangan = request.form['keterangan']
        data = Tindakan(tindak,harga,keterangan)
        db.session.add(data)
        db.session.commit()
        return redirect(url_for('tindakan'))

@app.route('/edittindakan/<id>', methods=['GET','POST'])
@is_logged_in
def edittindakan(id):
    data = Tindakan.query.filter_by(id=id).first()
    if request.method == 'POST':
        data.tindak = request.form['tindak']
        data.harga = request.form['harga']
        data.keterangan = request.form['keterangan']
        db.session.add(data)
        db.session.commit()
        return redirect(url_for('tindakan'))
    else:
        return render_template('/edittindakan.html', data=data)

@app.route('/hapustindakan/<id>', methods=['GET','POST'])
@is_logged_in
def hapustindakan(id):
    data = Tindakan.query.filter_by(id=id).first()
    db.session.delete(data)
    db.session.commit()
    return redirect(url_for('tindakan'))

@app.route('/karyawan')
@is_logged_in
def karyawan():
    return render_template('karyawan.html', container=Karyawan.query.all())

@app.route('/tambahkaryawan', methods=['GET','POST'])
@is_logged_in
def tambahkaryawan():
    if request.method == 'POST':
        nama = request.form['nama']
        np = request.form['np']
        jabatan = request.form['jabatan']
        gaji = request.form['gaji']
        lembur = request.form['lembur']
        kasbon = request.form['kasbon']
        iuran = request.form['iuran']
        lmb = 60000
        count = int(lmb) * int(lembur)
        count2 = int(gaji) + int(count) - int(kasbon)
        total = int(count2) - int(iuran)
        keterangan = request.form['keterangan']
        data = Karyawan(nama,np,jabatan,gaji,lembur,kasbon,iuran,total,keterangan)
        db.session.add(data)
        db.session.commit()
        return redirect(url_for('karyawan'))

@app.route('/editkaryawan/<id>', methods=['GET','POST'])
@is_logged_in
def editkaryawan(id):
    data = Karyawan.query.filter_by(id=id).first()
    if request.method == 'POST':
        data.nama = request.form['nama']
        data.np = request.form['np']
        data.jabatan = request.form['jabatan']
        data.gaji = request.form['gaji']
        data.lembur = request.form['lembur']
        data.kasbon = request.form['kasbon']
        data.iuran = request.form['iuran']
        data.total = request.form['total']
        data.keterangan = request.form['keterangan']
        db.session.add(data)
        db.session.commit()
        return redirect(url_for('karyawan'))
    else:
        return render_template('editkaryawan.html', data=data)

@app.route('/hapuskaryawan/<id>', methods=['GET','POST'])
@is_logged_in
def hapuskaryawan(id):
    data = Karyawan.query.filter_by(id=id).first()
    db.session.delete(data)
    db.session.commit()
    return redirect(url_for('karyawan'))

@app.route('/gudangstok')
@is_logged_in
def obat():
    return render_template('obat.html', container=Obat.query.all())

@app.route('/tambahobat', methods=['GET','POST'])
@is_logged_in
def tambahobat():
    if request.method == 'POST':
        tanggal = request.form['tanggal']
        jenisObat = request.form['jenisobat']
        namaObat = request.form['namaobat']
        hBeli = request.form['hBeli']
        jm1 = 0.40 * int(hBeli)
        hJual = int(jm1) + int(hBeli)
        exp =  request.form['exp']
        ready = request.form['ready']
        satuan = request.form['satuan']
        stok = request.form['stok']
        ksr = Kasir.query.all()
        jm = []
        for k in ksr:
            i = k.qty
            jm.insert(0,i)
        jm = sum(jm)
        total = int(hJual) * int(stok)
        sisa = int(stok) - int(jm)
        data = Obat(tanggal,jenisObat,namaObat,hBeli,hJual,exp,ready,satuan,stok,total,sisa)
        db.session.add(data)
        db.session.commit()
        return redirect(url_for('obat'))

@app.route('/editobat/<id>', methods=['GET','POST'])
@is_logged_in
def editobat(id):
    data = Obat.query.filter_by(id=id).first()
    if request.method == 'POST':
        data.tanggal = request.form['tanggal']
        data.jenisObat = request.form['jenisobat']
        data.namaObat = request.form['namaobat']
        data.hBeli = request.form['hBeli']
        data.hJual = request.form['hJual']
        data.exp =  request.form['exp']
        data.ready = request.form['ready']
        data.satuan = request.form['satuan']
        data.stok = request.form['stok']
        data.sisa = request.form['sisa']
        db.session.add(data)
        db.session.commit()
        return redirect(url_for('obat'))
    else:
        return render_template('editobat.html', data=data)

@app.route('/hapusobat/<id>', methods=['GET','POST'])
@is_logged_in
def hapusobat(id):
    data = Obat.query.filter_by(id=id).first()
    db.session.delete(data)
    db.session.commit()
    return redirect(url_for('obat'))

@app.route('/obatan')
@is_logged_in
def obatan():
    res = Obat.query.all()
    list_obat = [r.as_dict() for r in res]
    return jsonify(list_obat)

@app.route('/transaksiobat')
@is_logged_in
def transaksiobat():
    belanja = Belanja.query.all()
    uang = []
    for gt in belanja:
        i = gt.total
        uang.insert(0,i)
    uang = sum(uang)
    return render_template('klaimobat.html', row=Obat.query.all(), container=TebusObat.query.all(), kasir=Kasir.query.all(), belanja=belanja, uang=uang)

@app.route('/belanja', methods=['GET','POST'])
@is_logged_in
def belanja():
    if request.method == 'POST':
        item = request.form['item']
        price = request.form['price']
        qty = request.form['qty']
        total = int(price) * int(qty)
        data = Belanja(item,price,qty,total)
        db.session.add(data)
        db.session.commit()
        return redirect(url_for('transaksiobat'))

@app.route('/hapusale/<id>', methods=['GET','POST'])
@is_logged_in
def hapusale(id):
    data = Belanja.query.filter_by(id=id).first()
    db.session.delete(data)
    db.session.commit()
    return redirect(url_for('transaksiobat'))

@app.route('/tambahtransaksi', methods=['GET','POST'])
@is_logged_in
def tambahtransaksi():
    if request.method == 'POST':
        rm = request.form['rm']
        nama = request.form['nama']
        dokter = request.form['dokter']
        bDokter = request.form['bDokter']
        status = request.form['status']
        order = Belanja.query.all()
        for itm in order:
            it = itm.item
            qty = itm.qty
            price = itm.price
            total = itm.total
            db.session.add(Kasir(it,qty,price,total))
        data = BayarPasien(rm,nama,dokter,bDokter,status)
        db.session.add(data)
        db.session.commit()
    # Clear data di data Belanja
    db.session.query(Belanja).delete()
    db.session.commit()
    # Redirect Ke Awal
    return redirect(url_for('transaksiobat'))

@app.route('/pengadaan')
@is_logged_in
def pengadaan():
    return render_template('pengadaan.html', cont=Pengadaan.query.all())

@app.route('/tambahpengadaan', methods=['GET','POST'])
@is_logged_in
def tambahpengadaan():
    if request.method == 'POST':
        nFaktur = request.form['nfaktur']
        tgl = request.form['tgl']
        suplier = request.form['suplier']
        nohp = request.form['nohp']
        alamat = request.form['alamat']
        data = Pengadaan(nFaktur,tgl,suplier,nohp,alamat)
        db.session.add(data)
        db.session.commit()
        return redirect(url_for('pengadaan'))

@app.route('/mitra')
@is_logged_in
def mitra():
    return render_template('mitra.html', container=Mitra.query.all())

@app.route('/tambahmitra', methods=['GET','POST'])
@is_logged_in
def tambahmitra():
    if request.method == 'POST':
        perusahaan = request.form['perusahaan']
        tanggal = request.form['tanggal']
        keterangan = request.form['keterangan']
        data = Mitra(perusahaan,tanggal,keterangan)
        db.session.add(data)
        db.session.commit()
        return redirect(url_for('mitra'))

@app.route('/editmitra/<id>', methods=['GET','POST'])
@is_logged_in
def editmitra(id):
    data = Mitra.query.filter_by(id=id).first()
    if request.method == 'POST':
        data.perusahaan = request.form['perusahaan']
        data.tanggal = request.form['tanggal']
        data.keterangan = request.form['keterangan']
        db.session.add(data)
        db.session.commit()
        return redirect(url_for('mitra'))
    else:
        return render_template('editmitra.html', data=data)

@app.route('/hapusmitra/<id>', methods=['GET','POST'])
@is_logged_in
def hapusmitra(id):
    data = Mitra.query.filter_by(id=id).first()
    db.session.delete(data)
    db.session.commit()
    return redirect(url_for('mitra'))

@app.route('/iuran')
@is_logged_in
def iuran():
    return render_template('iuran.html', container=Iuran.query.all())

@app.route('/tambahiuran', methods=['GET','POST'])
@is_logged_in
def tambahiuran():
    if request.method == 'POST':
        tagihan = request.form['tagihan']
        jumlah = request.form['jumlah']
        keterangan = request.form['keterangan']
        data = Iuran(tagihan,jumlah,keterangan)
        db.session.add(data)
        db.session.commit()
        return redirect(url_for('iuran'))

@app.route('/editiuran/<id>', methods=['GET''POST'])
@is_logged_in
def editiuran(id):
    data = Iuran.query.filter_by(id=id).first()
    if request.method == 'POST':
        data.tagihan = request.form['tagihan']
        data.jumlah = request.form['jumlah']
        data.keterangan = request.form['keterangan']
        db.session.add(data)
        db.session.commit()
        return redirect(url_for('iuran'))
    else:
        return render_template('editiuran.html', data=data)

@app.route('/hapusiuran/<id>', methods=['GET','POST'])
@is_logged_in
def hapusiuran(id):
    data = Iuran.query.filter_by(id=id).first()
    db.session.delete(data)
    db.session.commit()
    return redirect(url_for('iuran'))

@app.route('/pembelanjaan')
@is_logged_in
def pembelanjaan():
    return render_template('pembelanjaan.html', container=Pembelanjaan.query.all())

@app.route('/tambahbelanja', methods=['GET','POST'])
@is_logged_in
def tambahbelanja():
    if request.method == 'POST':
        nbarang = request.form['nbarang']
        satuan = request.form['satuan']
        volume = request.form['volume']
        harga = request.form['harga']
        total = int(volume) * int(harga)
        tanggal = request.form['tanggal']
        keterangan = request.form['keterangan']
        data = Pembelanjaan(nbarang,satuan,volume,harga,total,tanggal,keterangan)
        db.session.add(data)
        db.session.commit()
        return redirect(url_for('pembelanjaan'))

@app.route('/editbelanja/<id>', methods=['GET','POST'])
@is_logged_in
def editbelanja(id):
    data = Pembelanjaan.query.filter_by(id=id).first()
    if request.method == 'POST':
        data.nbarang = request.form['nbarang']
        data.satuan = request.form['satuan']
        data.volume = request.form['volume']
        data.harga = request.form['harga']
        data.total = request.form['total']
        data.keterangan = request.form['keterangan']
        db.session.add(data)
        db.session.commit()
        return redirect(url_for('pembelanjaan'))

@app.route('/hapusbelanja/<id>', methods=['GET','POST'])
@is_logged_in
def hapusbelanja(id):
    data = Pembelanjaan.query.filter_by(id=id).first()
    db.session.delete(data)
    db.session.commit()
    return redirect(url_for('pembelanjaan'))

@app.route('/rekammedis')
@is_logged_in
def rekammedis():
    return render_template('rekammedis.html', container=RekamMedis.query.all())

@app.route('/tambahrekammedis', methods=['GET','POST'])
@is_logged_in
def tambahrekammedis():
    if request.method == 'POST':
        npasien = request.form['npasien']
        dokter = request.form['dokter']
        keluhan = request.form['keluhan']
        diagnosa = request.form['diagnosa']
        obat = request.form['obat']
        tindakan = request.form['tindakan']
        data = RekamMedis(npasien,dokter,keluhan,diagnosa,obat,tindakan)
        db.session.add(data)
        db.session.commit()
        return redirect(url_for('rekammedis'))

@app.route('/editrekammedis/<id>', methods=['GET','POST'])
@is_logged_in
def editrekammedis(id):
    data = RekamMedis.query.filter_by(id=id).first()
    if request.method == 'POST':
        data.npasien = request.form['npasien']
        data.dokter = request.form['dokter']
        data.keluhan = request.form['keluhan']
        data.diagnosa = request.form['diagnosa']
        data.obat = request.form['obat']
        data.tindakan = request.form['tindakan']
        db.session.add(data)
        db.session.commit()
        return redirect(url_for('rekammedis'))
    else:
        return render_template('editrekammedis.html', data=data)

@app.route('/hapusrekammedis/<id>', methods=['GET','POST'])
@is_logged_in
def hapusrekammedis(id):
    data = RekamMedis.query.filter_by(id=id).first()
    db.session.delete(data)
    db.session.commit()
    return redirect(url_for('rekammedis'))

@app.route('/rontgen')
@is_logged_in
def rontgen():
    return render_template('rontgen.html', container=Rontgen.query.all())

@app.route('/tambahrontgen', methods=['GET','POST'])
@is_logged_in
def tambahrontgen():
    if request.method == 'POST':
        nDokter = request.form['ndokter']
        npasien = request.form['npasien']
        usia = request.form['usia']
        gender = request.form['gender']
        diagnosa = request.form['diagnosa']
        npetugas = request.form['npetugas']
        keterangan = request.form['keterangan']
        data = Rontgen(nDokter,npasien,usia,gender,diagnosa,npetugas,keterangan)
        db.session.add(data)
        db.session.commit()
        return redirect(url_for('rontgen'))

@app.route('/editrontgen/<id>', methods=['GET','POST'])
@is_logged_in
def editrontgen(id):
    data = Rontgen.query.filter_by(id=id).first()
    if request.method == 'POST':
        data.nDokter = request.form['ndokter']
        data.npasien = request.form['npasien']
        data.usia = request.form['usia']
        data.gender = request.form['gender']
        data.diagnosa = request.form['diagnosa']
        data.npetugas = request.form['npetugas']
        data.keterangan = request.form['keterangan']
        db.session.add(data)
        db.session.commit()
        return redirect(url_for('rontgen'))
    else:
        return render_template('editrontgen.html', data=data)

@app.route('/hapusrontgen/<id>', methods=['GET','POST'])
@is_logged_in
def hapusrontgen(id):
    data = Rontgen.query.filter_by(id=id).first()
    db.session.delete(data)
    db.session.commit()
    return redirect(url_for('rontgen'))

@app.route('/pendaftaran')
@is_logged_in
def pendaftaran():
    form = CariData()
    return render_template('pendaftaran.html', container=Pendaftaran.query.all(), form=form)

@app.route('/tambahpendaftaran', methods=['GET','POST'])
@is_logged_in
def tambahpendaftaran():
    if request.method == 'POST':
        rm = request.form['rm']
        nama = request.form['nama']
        usia = request.form['usia']
        gender = request.form['gender']
        status = request.form['status']
        goldarah = request.form['goldarah']
        ttl = request.form['ttl']
        ktp = request.form['ktp']
        pJawab = request.form['pjawab']
        alamat = request.form['alamat']
        kategori = request.form['kategori']
        jenisKmr = request.form['jeniskmr']
        biaya = request.form['biaya']
        metode = request.form['metode']
        data = Pendaftaran(rm,nama,usia,gender,status,goldarah,ttl,ktp,pJawab,alamat,kategori,jenisKmr,biaya,metode)
        db.session.add(data)
        db.session.commit()
        return redirect(url_for('pendaftaran'))

@app.route('/editpendaftaran/<id>', methods=['GET','POST'])
@is_logged_in
def editpendaftaran(id):
    data = Pendaftaran.query.filter_by(id=id).first()
    if request.method == 'POST':
        data.nama = request.form['nama']
        data.usia = request.form['usia']
        data.gender = request.form['gender']
        data.status = request.form['status']
        data.goldarah = request.form['goldarah']
        data.ttl = request.form['ttl']
        data.ktp = request.form['ktp']
        data.pJawab = request.form['pjawab']
        data.alamat = request.form['alamat']
        data.kategori = request.form['kategori']
        data.jenisKmr = request.form['jeniskmr']
        data.biaya = request.form['biaya']
        data.metode = request.form['metode']
        db.session.add(data)
        db.session.commit()
        return redirect(url_for('pendaftaran'))
    else:
        return render_template('editpendaftaran.html', data=data)

@app.route('/hapuspendaftaran/<id>', methods=['GET','POST'])
@is_logged_in
def hapuspendaftaran(id):
    data = Pendaftaran.query.filter_by(id=id).first()
    db.session.delete(data)
    db.session.commit()
    return redirect(url_for('pendaftaran'))

@app.route('/igd')
@is_logged_in
def igd():
    return render_template('igd.html', container=Pendaftaran.query.filter_by(jenisKmr="IGD").all(), igd=IGD.query.all())

@app.route('/hasilIGD')
@is_logged_in
def dataigd():
    return render_template('dataigd.html', igd=IGD.query.all())

@app.route('/tambahigd', methods=['GET','POST'])
@is_logged_in
def tambahigd():
    if request.method == 'POST':
        rm = request.form['rem']
        nama = request.form['nama']
        alamat = request.form['alamat']
        usia = request.form['usia']
        tanggal = request.form['tanggal']
        pemFisik = request.form['pemfisik']
        diagnosa = request.form['diagnosa']
        tindakan = request.form['tindakan']
        resep = request.form['resep']
        dokter = request.form['dokter']
        biaya = request.form['biaya']
        data = IGD(rm,nama,alamat,usia,tanggal,pemFisik,diagnosa,tindakan,resep,dokter,biaya)
        db.session.add(data)
        db.session.commit()
    if request.method == 'POST':
        rm = request.form['rem']
        nama = request.form['nama']
        resep = request.form['resep']
        dokter = request.form['dokter']
        biaya = request.form['biaya']
        db.session.add(TebusObat(rm,nama,resep,dokter,biaya))
        db.session.commit()
        return redirect(url_for('igd'))

@app.route('/laboratorium')
@is_logged_in
def laboratorium():
    return render_template('laboratorium.html', container=Laboratorium.query.all())

@app.route('/tambahlaboratorium', methods=['GET','POST'])
@is_logged_in
def tambahlaboratorium():
    if request.method == 'POST':
        ndokter = request.form['ndokter']
        nama = request.form['nama']
        usia = request.form['usia']
        gender = request.form['gender']
        status = request.form['status']
        golDarah = request.form['goldarah']
        keluhan = request.form['keluhan']
        hasil = request.form['hasil']
        data = Laboratorium(ndokter,nama,usia,gender,status,golDarah,keluhan,hasil)
        db.session.add(data)
        db.session.commit()
        return redirect(url_for('laboratorium'))

@app.route('/editlaboratorium/<id>', methods=['GET','POST'])
@is_logged_in
def editlaboratorium(id):
    data = Laboratorium.query.filter_by(id=id).first()
    if request.method == 'POST':
        data.ndokter = request.form['ndokter']
        data.nama = request.form['nama']
        data.usia = request.form['usia']
        data.gender = request.form['gender']
        data.status = request.form['status']
        data.golDarah = request.form['goldarah']
        data.keluhan = request.form['keluhan']
        data.hasil = request.form['hasil']
        db.session.add(data)
        db.session.commit()
        return redirect(url_for('laboratorium'))
    else:
        return render_template('editlaboratorium', data=data)

@app.route('/hapuslaboratorium/<id>', methods=['GET','POST'])
@is_logged_in
def hapuslaboratorium(id):
    data = Laboratorium.query.filter_by(id=id).first()
    db.session.delete(data)
    db.session.commit()
    return redirect(url_for('laboratorium'))

@app.route('/search', methods=['GET','POST'])
@is_logged_in
def search():
    form = CariData()
    Cariobt = Obat.query
    if form.validate_on_submit():
        Cariobt = Cariobt.filter(Obat.namaObat.like('%' + form.cari.data + '%'))
    Cariobt = Cariobt.order_by(Obat.namaObat).all()
    return render_template('kasir.html', Cariobt=Cariobt, form=form)

@app.route('/history')
@is_logged_in
def history():
    hitung = Kasir.query.all()
    uang = []
    for ht in hitung:
        i = ht.total
        uang.insert(0,i)
    uang = sum(uang)
    return render_template('history.html', container=Kasir.query.all(), uang=uang)

@app.route('/hapushistory/<id>', methods=['GET','POST'])
@is_logged_in
def hapushistory(id):
    data = Kasir.query.filter_by(id=id).first()
    db.session.delete(data)
    db.session.commit()
    return redirect(url_for('history'))

@app.route('/bayarobat')
@is_logged_in
def bayarobat():
    return render_template('transaksiobat.html', container=Obat.query.all())

@app.route('/bayarpasien')
@is_logged_in
def bayarpasien():
    return render_template('bayarpasien.html', container=BayarPasien.query.all(), pndaftar=Pendaftaran.query.all(),
                           igd=Kasir.query.all())

@app.route('/bpjs1')
@is_logged_in
def bpjs():
    return render_template('bpjs.html', container=Pendaftaran.query.filter_by(metode="BPJS").all())

@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.secret_key = os.urandom(42)
    app.run(debug=True)
    
    

