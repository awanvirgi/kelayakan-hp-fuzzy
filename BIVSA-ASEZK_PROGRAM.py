
# inisiasi library
import skfuzzy as fuz
import numpy as np
import streamlit as st


# fungsi buat inisiasi range dari fungsi keanggotanya
def OurRange(_lo,_hi,_step):
    ourr=np.arange(_lo,_hi,_step)
    return ourr

# menentukan fungsi anggota ini startnya dari segitiga kalau datanya diisi 2 jenis angka kemungkiann itu linear
def MembershipFunc1 (_rule, _our_range): 
    low=fuz.trimf (_our_range, _rule[0])
    middle=fuz.trimf(_our_range, _rule[1]) 
    high=fuz.trimf(_our_range, _rule[2])
    
    return low, middle, high

def MembershipFunc2 (_rule, _our_range): 
    low=fuz.trimf(_our_range, _rule[0])
    high=fuz.trimf(_our_range, _rule[1])
    
    return low,high

# inisiasi fungsi anggota masing masing variabel
xandro = OurRange (9,15,1)
randro = np.array([
[9,9,12],
[11,14,14]])
lo_andro,hi_andro=MembershipFunc2(randro,xandro)

xram = OurRange (2,13,1)
rram = np.array([
[2,2,6],
[4,6,8], 
[6,12,12]])
lo_ram,mi_ram,hi_ram=MembershipFunc1(rram,xram)

xrom = OurRange (16,256,1)
rrom = np.array([
[16,16,64],
[32,64,128], 
[64,256,256]])
lo_rom,mi_rom,hi_rom=MembershipFunc1(rrom,xrom)

xlayar = OurRange (4.7,6.5,0.1)
rlayar = np.array([
[4.7,4.7,5.5],
[5.0,5.5,6.0], 
[5.5,6.5,6.5]])
lo_layar,mi_layar,hi_layar=MembershipFunc1(rlayar,xlayar)

xkondisi = OurRange (0,11,1)
rkondisi = np.array([
[0,0,5],
[0,5,10], 
[5,10,10]])
lo_kondisi,mi_kondisi,hi_kondisi=MembershipFunc1(rkondisi,xkondisi)

xspek = OurRange (0,9,1)
rspek  = np.array([
[0,0,4],
[2,4,6], 
[4,8,8]])
lo_spek,mi_spek,hi_spek=MembershipFunc1(rspek,xspek)

xharga = OurRange (0,10000000,10000)
rharga  = np.array([
[0,0,5000000],
[0,5000000,10000000], 
[5000000,10000000,150000000]])
lo_harga,mi_harga,hi_harga=MembershipFunc1(rharga,xharga)


# nyari derajat pada masing masing himpunan
def MembershipDeg1(_range,_lo,_mi,_hi,_val):
    low=fuz.interp_membership (_range,_lo,_val)
    middle=fuz.interp_membership(_range,_mi,_val)
    high=fuz.interp_membership(_range,_hi, _val)
    return low, middle, high


def MembershipDeg2(_range,_lo,_hi ,_val):
    low=fuz.interp_membership(_range,_lo,_val)
    high=fuz.interp_membership(_range,_hi,_val)
    return low, high


# proses implikasi
def Status1 (_membership,_label0,_label1,_label2):
    status=''
    if _membership[0]>_membership[1] and _membership[0]>_membership[2]:
        status=_label0
    elif _membership[1]>_membership[0] and _membership[1]>_membership[2]:
        status=_label1
    elif _membership[2]>_membership[0] and _membership[2]>_membership[1]:
        status=_label2
    else:
        status=_label2
    return status

def Status2 (_membership,_label0,_label1):
    status=''
    if _membership[0]>_membership[1]:
        status= _label0
    elif _membership[1]>_membership[0]:
        status= _label1
    return status

# proses penghitungan poin spesifikasi
def spekPoin(status):
    poin = 0
    for i in status:
        if i == 'Sedang' or 'Baru':
            poin += 1
        elif i == 'Lebar' or 'Besar' or 'Terbaru':
            poin += 2
    return poin

# tempat buat nyimpen fungsi dari spek
class spesifikasi:
    def __init__(self,andro,ram,rom,layar,jaringan):
        self.andro = float(andro)
        self.ram = float(ram)
        self.rom = float(rom)
        self.layar = float(layar)
        self.jaringan = float(jaringan)
    def Member(self):
        m_andro = MembershipDeg2(xandro,lo_andro,hi_andro,andro)
        m_ram = MembershipDeg1(xram,lo_ram,mi_ram,hi_ram,ram)
        m_rom = MembershipDeg1(xrom,lo_rom,mi_rom,hi_rom,rom)
        m_layar = MembershipDeg1(xlayar,lo_layar,mi_layar,hi_layar,layar)
        m_jaringan = jaringan
        return m_andro,m_ram,m_rom,m_layar,m_jaringan
    def Status(self,m):
        s_andro = Status2(m[0],"Lama","Baru")
        s_ram = Status1(m[1],"Kecil","Sedang","Besar")
        s_rom = Status1(m[2],"Kecil","Sedang","Besar")
        s_layar = Status1(m[3],"Kecil","Sedang","Besar")
        def status_jaringan(m):
            status=''
            if m == 3:
                status='Jadul'
            elif m == 4:
                status='Normal'
            elif m == 5:
                status='Terbaru'
            return status
        s_jaringan = status_jaringan(m[4])
        return s_andro,s_ram,s_rom,s_layar,s_jaringan
    
# menyimpan rule base
def Rulebased(_spek_status,_kondisi_status,_harga_status):
    layak_status=''
    if _spek_status == 'Rendah' and _harga_status != 'Murah' :
        layak_status ='Rendah'
    elif _spek_status == 'Rendah' and _harga_status == 'Murah' and _kondisi_status != 'Bagus':
        layak_status = 'Rendah'
    elif _spek_status == 'Rendah' and _harga_status == 'Murah' and _kondisi_status == 'Bagus':
        layak_status = 'Sedang'
    elif _spek_status == 'Menengah' and _harga_status != 'Murah' and _kondisi_status == 'Buruk':
        layak_status = 'Rendah'
    elif _spek_status == 'Menengah' and _harga_status == 'Murah' and _kondisi_status != 'Bagus':
        layak_status = 'Sedang'
    elif _spek_status == 'Menengah' and _harga_status != 'Murah' and _kondisi_status != 'Buruk':
        layak_status = 'Sedang'
    elif _spek_status == 'Menengah' and _harga_status == 'Murah' and _kondisi_status == 'Bagus':
        layak_status = 'Tinggi'
    elif _spek_status == 'Tinggi' and _harga_status == 'Mahal' and _kondisi_status != 'Bagus':
        layak_status = 'Sedang'
    elif _spek_status == 'Tinggi' and _harga_status != 'Mahal' and _kondisi_status != 'Buruk':
        layak_status = 'Tinggi'
    return layak_status
 
# tampilan interface dengan streamlit       
st.title("Aplikasi Menentukan Kelayakan HP Bekas") #ini buat title
st.header("Spesifikasi Handphone") #ini buat header

# input spesifikasi interface
andro = st.text_input("Masukan Versi Androidnya") 
ram = st.text_input("Masukan Ukuran RAM nya (gb)")
rom = st.text_input("Masukan Ukuran Internal Storagenya (gb)")
layar = st.number_input("Masukan Ukuran Diameter layarnya (inch)",step=0.1)
jaringan = st.selectbox("Masukan Tipe Jaringannya (3/4/5)",(3,4,5))

# bagian untuk kondisi
st.header("Kondisi Handphone")
s_kondisi = [] #buat nyimpen jawaban
p_kondisi = 0 #insiasi awal poin
k_kamera = st.radio("Apakah Kamera berfungsi dengan baik?",('Iya','Tidak'),key = 1) #key disini buat untuk menamai inputan biar beda2
s_kondisi.append(k_kamera) #hasil jawabannya dimasukin ke array s_kondisi
k_koneksi=st.radio("Apakah Konektivitas(Bluetooth,Wifi,Data,Hotspot) berfungsi dengan baik?",('Iya','Tidak'),key = 2)
s_kondisi.append(k_koneksi)
k_layar=st.radio("Apakah Layar tidak pecah dan berfungsi dengan baik?",('Iya','Tidak'),key = 3)
s_kondisi.append(k_layar)
k_sistem=st.radio("Apakah Sistem berfungsi dengan baik?",('Iya','Tidak'),key = 4) #value untuk radionya sudah disetup
s_kondisi.append(k_sistem)
k_port=st.radio("Apakah Lubang Port berfungsi dengan baik?",('Iya','Tidak'),key = 5)
s_kondisi.append(k_port)
k_sensor=st.radio("Apakah Sensor berfungsi dengan baik?",('Iya','Tidak'),key = 6)
s_kondisi.append(k_sensor)
k_tombol=st.radio("Apakah Tombol berfungsi dengan baik?",('Iya','Tidak'),key = 7)
s_kondisi.append(k_tombol)
k_baterai=st.radio("Apakah Baterai berfungsi dengan baik?",('Iya','Tidak'),key = 8)
s_kondisi.append(k_baterai)
k_kinerja=st.radio("Apakah Kinerja handphone Lancar(Tidak Lag)?",('Iya','Tidak'),key = 9)
s_kondisi.append(k_kinerja)
k_suara=st.radio("Apakah Suara bandphone terdengar dengan baik?",('Iya','Tidak'),key = 10)
s_kondisi.append(k_suara)
# ngehitung jumlah Y pada array
for i in s_kondisi:
    if i == 'Iya':
        p_kondisi += 1
# harag handphone
st.header("Harga Handphone")
harga = st.text_input("Masukan Harga Jual Handphone (Rupiah)")


# ini untuk tombol jika tidak ditekan maka dia tidak jalan programnya
if st.button('Analysis'):
    # inisiasi variabel untuk spek
    spek = spesifikasi(andro,ram,rom,layar,jaringan)
    
    # insiasi member spek
    cek_mem = spek.Member()
    # proses implikasi 
    cek_status = spek.Status(cek_mem)
    # masukin ke rulebase
    p_spek = spekPoin(cek_status)
    m_spek = MembershipDeg1(xspek,lo_spek,mi_spek,hi_spek,p_spek)
    s_spek = Status1(m_spek,"Rendah","Menengah","Tinggi")
    
    m_kondisi = MembershipDeg1(xkondisi,lo_kondisi,mi_kondisi,hi_kondisi,p_kondisi)
    s_kondisi = Status1(m_kondisi,"Buruk","Sedang","Bagus")

    harga=float(harga)
    m_harga = MembershipDeg1(xharga,lo_harga,mi_harga,hi_harga,harga)
    s_harga = Status1(m_harga,"Murah","Sedang","Mahal")

    kelayakan = Rulebased(s_spek,s_kondisi,s_harga)

    # nampilin hasil perhitungannya
    st.write("Spesifikasi HP = ",s_spek)
    st.write("Harga HP = ",s_harga)
    st.write("Kondisi HP = ",s_kondisi)
    st.write("Kelayakan HP = ",kelayakan)


















    
        
