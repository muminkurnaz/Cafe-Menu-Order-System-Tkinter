import tkinter as tk
from tkinter import messagebox
import csv

class Kullanici:
    def __init__(self, kullanici_adi, sifre):
        self.kullanici_adi = kullanici_adi
        self.sifre = sifre

class CafeUygulamasi:
    def __init__(self, pencere, masa_sayisi=50, menu_dosyasi="menu.csv"):
        self.pencere = pencere
        self.pencere.title("Cafe Ödeme Sistemi")
        self.pencere.configure(bg="Salmon2")  # Arka plan rengi

        # Kullanıcılar ve şifreler
        self.kullanicilar = [
            Kullanici("kullanici1", "sifre1"),
            Kullanici("kullanici2", "sifre2")
        ]

        # Masa sayısını belirle
        self.masa_sayisi = masa_sayisi

        self.urunler = self.menuyu_yukle(menu_dosyasi)

        # Masalara ait siparişleri tutacak sözlük
        self.masa_siparisleri = {masa: {} for masa in range(1, self.masa_sayisi + 1)}

        # Günlük satışları tutacak sözlük
        self.gunluk_satislar = {}

        # Seçilen masa
        self.secilen_masa = None

        # Kullanıcı giriş penceresini göster
        self.kullanici_giris_penceresi()

    def menuyu_yukle(self, dosya):
        urunler = {}
        with open(dosya, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                urunler[row['Ürün']] = float(row['Fiyat'])
        return urunler
         
    def kullanici_giris_penceresi(self):
        self.temizle_pencere()
        self.pencere.configure(bg="Salmon2")  # Arka plan rengi
        
        self.label_kullanici_adi = tk.Label(self.pencere, text="Kullanıcı Adı:", font=("Arial", 12), bg="Salmon2")
        self.label_kullanici_adi.grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.kullanici_adi_entry = tk.Entry(self.pencere, font=("Arial", 12))
        self.kullanici_adi_entry.grid(row=0, column=1, padx=10, pady=5)
        
        self.label_sifre = tk.Label(self.pencere, text="Şifre:", font=("Arial", 12), bg="Salmon2")
        self.label_sifre.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.sifre_entry = tk.Entry(self.pencere, show="*", font=("Arial", 12))
        self.sifre_entry.grid(row=1, column=1, padx=10, pady=5)

        self.giris_button = tk.Button(self.pencere, text="Giriş Yap", font=("Arial", 12), command=self.giris_kontrol, bg="#007BFF", fg="white", relief="raised")
        self.giris_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="we")

    def giris_kontrol(self):
        kullanici_adi = self.kullanici_adi_entry.get()
        sifre = self.sifre_entry.get()

        for kullanici in self.kullanicilar:
            if kullanici.kullanici_adi == kullanici_adi and kullanici.sifre == sifre:
                self.ana_arayuz()
                return

        messagebox.showerror("Hata", "Geçersiz kullanıcı adı veya şifre!")

    def ana_arayuz(self):
        self.temizle_pencere()
        self.pencere.configure(bg="Salmon2")  # Arka plan rengi
        
        self.label_masa_numaralari = tk.Label(self.pencere, text="Masa Numaraları:", font=("Arial", 14, "bold"), bg="Salmon2")
        self.label_masa_numaralari.grid(row=0, column=0, columnspan=5, pady=10)

        # Masa numaraları için düğmeler oluştur
        row = 1
        col = 0
        for masa in range(1, self.masa_sayisi + 1):
            masa_button = tk.Button(self.pencere, text=f"Masa {masa}", font=("Arial", 12), command=lambda m=masa: self.masa_secildi(m), bg="#007BFF", fg="white", relief="raised")
            masa_button.grid(row=row, column=col, padx=5, pady=5, sticky="we")
            col += 1
            if col == 5:
                col = 0
                row += 1

        # Günlük Satışlar Butonu
        self.gunluk_satislar_button = tk.Button(self.pencere, text="Günlük Satışlar", font=("Arial", 12), command=self.gunluk_satislar_penceresi, bg="#E91E63", fg="white", relief="raised")
        self.gunluk_satislar_button.grid(row=row, column=0, columnspan=5, pady=10, sticky="we")

    def masa_arayuz(self):
        self.temizle_pencere()
        self.pencere.configure(bg="Salmon2")  # Arka plan rengi
        
        self.label_masa_numarasi = tk.Label(self.pencere, text=f"Masa {self.secilen_masa}", font=("Arial", 14, "bold"), bg="Salmon2")
        self.label_masa_numarasi.grid(row=0, column=0, columnspan=5, pady=10)

        self.label_siparisler = tk.Label(self.pencere, text="Siparişler:", font=("Arial", 12, "bold"), bg="Salmon2")
        self.label_siparisler.grid(row=1, column=0, columnspan=5)

        self.listebox_siparisler = tk.Listbox(self.pencere, width=50, font=("Arial", 12))
        self.listebox_siparisler.grid(row=2, column=0, columnspan=5)

        self.label_toplam_tutar = tk.Label(self.pencere, text="Toplam Tutar:", font=("Arial", 12, "bold"), bg="Salmon2")
        self.label_toplam_tutar.grid(row=3, column=0, columnspan=2)

        self.toplam_tutar = tk.Label(self.pencere, text="0 TL", font=("Arial", 12), bg="Salmon2")
        self.toplam_tutar.grid(row=3, column=2, columnspan=3)

        # Ürünler için dropdown menü oluştur
        self.label_urun = tk.Label(self.pencere, text="Ürün Seçiniz:", font=("Arial", 12, "bold"), bg="Salmon2")
        self.label_urun.grid(row=4, column=0, columnspan=2)

        self.urun_secim = tk.StringVar()
        self.urun_secim.set(list(self.urunler.keys())[0])  # Başlangıçta ilk ürünü seçili yap
        self.dropdown_urun = tk.OptionMenu(self.pencere, self.urun_secim, *self.urunler.keys())
        self.dropdown_urun.config(font=("Arial", 12))
        self.dropdown_urun.grid(row=4, column=2, columnspan=3)

        self.label_miktar = tk.Label(self.pencere, text="Miktar:", font=("Arial", 12, "bold"), bg="Salmon2")
        self.label_miktar.grid(row=5, column=0, columnspan=2)

        self.miktar_entry = tk.Entry(self.pencere, font=("Arial", 12))
        self.miktar_entry.grid(row=5, column=2, columnspan=3)

        self.ekle_button = tk.Button(self.pencere, text="Sepete Ekle", font=("Arial", 12), command=self.sepete_ekle, bg="#007BFF", fg="white", relief="raised")
        self.ekle_button.grid(row=6, column=0, columnspan=2)

        self.cikar_button = tk.Button(self.pencere, text="Sepetten Çıkar", font=("Arial", 12), command=self.sepetten_cikar, bg="#007BFF", fg="white", relief="raised")
        self.cikar_button.grid(row=6, column=2, columnspan=3)

        self.odeme_button = tk.Button(self.pencere, text="Ödeme Yap", font=("Arial", 12), command=self.odeme_penceresi, bg="#E91E63", fg="white", relief="raised")
        self.odeme_button.grid(row=7, column=0, columnspan=5, pady=10)

        self.geri_button = tk.Button(self.pencere, text="Ana Arayüze Dön", font=("Arial", 12), command=self.ana_arayuza_don, bg="#6C757D", fg="white", relief="raised")
        self.geri_button.grid(row=8, column=0, columnspan=5, pady=10)

        self.guncelle_siparisler()

    def temizle_pencere(self):
        for widget in self.pencere.winfo_children():
            widget.destroy()

    def masa_secildi(self, masa):
        self.secilen_masa = masa
        self.masa_arayuz()

    def sepete_ekle(self):
        urun = self.urun_secim.get()
        miktar = int(self.miktar_entry.get())
        if urun in self.masa_siparisleri[self.secilen_masa]:
            self.masa_siparisleri[self.secilen_masa][urun] += miktar
        else:
            self.masa_siparisleri[self.secilen_masa][urun] = miktar
        self.guncelle_siparisler()

    def sepetten_cikar(self):
        urun = self.urun_secim.get()
        miktar = int(self.miktar_entry.get())
        if urun in self.masa_siparisleri[self.secilen_masa]:
            self.masa_siparisleri[self.secilen_masa][urun] -= miktar
            if self.masa_siparisleri[self.secilen_masa][urun] <= 0:
                del self.masa_siparisleri[self.secilen_masa][urun]
        self.guncelle_siparisler()

    def guncelle_siparisler(self):
        self.listebox_siparisler.delete(0, tk.END)
        for urun, miktar in self.masa_siparisleri[self.secilen_masa].items():
            self.listebox_siparisler.insert(tk.END, f"{urun}: {miktar}")
        toplam_tutar = sum(self.urunler[urun] * miktar for urun, miktar in self.masa_siparisleri[self.secilen_masa].items())
        self.toplam_tutar.config(text=f"{toplam_tutar} TL")

    def odeme_penceresi(self):
        toplam_tutar = sum(self.urunler[urun] * miktar for urun, miktar in self.masa_siparisleri[self.secilen_masa].items())

        odeme_penceresi = tk.Toplevel(self.pencere)
        odeme_penceresi.title("Ödeme Yap")
        odeme_penceresi.configure(bg="Salmon2")  # Arka plan rengi

        # Ödeme yapılan tutarın gösterilmesi
        tk.Label(odeme_penceresi, text=f"Toplam Tutar: {toplam_tutar} TL", font=("Arial", 12), bg="Salmon2").pack()

        # Ödeme seçenekleri için butonlar
        tk.Button(odeme_penceresi, text="Nakit", font=("Arial", 12), command=lambda: self.odeme_tamamlandi(odeme_penceresi, toplam_tutar, "Nakit"), bg="#007BFF", fg="white", relief="raised").pack()
        tk.Button(odeme_penceresi, text="Kart", font=("Arial", 12), command=lambda: self.odeme_tamamlandi(odeme_penceresi, toplam_tutar, "Kart"), bg="#007BFF", fg="white", relief="raised").pack()

    def odeme_tamamlandi(self, pencere, tutar, odeme_yontemi):
        # Günlük satışlara ekle
        for urun, miktar in self.masa_siparisleri[self.secilen_masa].items():
            if urun not in self.gunluk_satislar:
                self.gunluk_satislar[urun] = {'Adet': miktar, 'Tutar': self.urunler[urun] * miktar}
            else:
                self.gunluk_satislar[urun]['Adet'] += miktar
                self.gunluk_satislar[urun]['Tutar'] += self.urunler[urun] * miktar

        messagebox.showinfo("Ödeme Yapıldı", f"Ödeme yapıldı. Ödeme yöntemi: {odeme_yontemi}, Toplam Tutar: {tutar} TL")

        # Masanın siparişlerini temizle
        self.masa_siparisleri[self.secilen_masa] = {}
        self.guncelle_siparisler()

        # Ödeme penceresini kapat
        pencere.destroy()

    def gunluk_satislar_penceresi(self):
        pencere = tk.Toplevel(self.pencere)
        pencere.title("Günlük Satışlar")
        pencere.configure(bg="Salmon2")  # Arka plan rengi

        # Başlık
        tk.Label(pencere, text="Günlük Satışlar", font=("Arial", 16, "bold"), bg="Salmon2").grid(row=0, column=0, columnspan=3, pady=10)

        # Tablo başlıkları
        tk.Label(pencere, text="Ürün", font=("Arial", 14, "bold"), bg="Salmon2").grid(row=1, column=0, padx=10, pady=5)
        tk.Label(pencere, text="Adet", font=("Arial", 14, "bold"), bg="Salmon2").grid(row=1, column=1, padx=10, pady=5)
        tk.Label(pencere, text="Tutar", font=("Arial", 14, "bold"), bg="Salmon2").grid(row=1, column=2, padx=10, pady=5)

        # Günlük satışları listele
        row = 2
        for urun, degerler in self.gunluk_satislar.items():
            tk.Label(pencere, text=urun, font=("Arial", 12), bg="Salmon2").grid(row=row, column=0, padx=10, pady=5)
            tk.Label(pencere, text=degerler['Adet'], font=("Arial", 12), bg="Salmon2").grid(row=row, column=1, padx=10, pady=5)
            tk.Label(pencere, text=f"{degerler['Tutar']} TL", font=("Arial", 12), bg="Salmon2").grid(row=row, column=2, padx=10, pady=5)
            row += 1

        # Toplam Tutar
        toplam_tutar = sum(degerler['Tutar'] for degerler in self.gunluk_satislar.values())
        tk.Label(pencere, text=f"Toplam Tutar: {toplam_tutar} TL", font=("Arial", 14, "bold"), bg="Salmon2").grid(row=row, column=0, columnspan=3, pady=10)

    def ana_arayuza_don(self):
        self.secilen_masa = None
        self.ana_arayuz()

if __name__ == "__main__":
    root = tk.Tk()
    uygulama = CafeUygulamasi(root)
    root.mainloop()