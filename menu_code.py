import csv

def menu_olustur():
    try:
        with open("menu.csv", mode='r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            menu = [(row['Ürün'], row['Fiyat']) for row in reader]
    except FileNotFoundError:
        menu = []

    return menu

def menu_goster(menu):
    print("Mevcut Menü:")
    for index, (urun, fiyat) in enumerate(menu, start=1):
        print(f"{index}. {urun}: {fiyat}")

def menu_ekle(menu):
    urun = input("Eklemek istediğiniz ürünün adını girin: ")
    fiyat = input("Eklemek istediğiniz ürünün fiyatını girin: ")
    menu.append((urun, fiyat))
    print("Ürün başarıyla eklendi.")

def menu_sil(menu):
    menu_goster(menu)
    try:
        secim = int(input("Silmek istediğiniz ürünün numarasını girin: "))
        if secim < 1 or secim > len(menu):
            print("Geçersiz bir seçim yaptınız. Lütfen menüdeki bir numara girin.")
            return
        del menu[secim - 1]
        print("Ürün başarıyla silindi.")
    except ValueError:
        print("Geçersiz bir seçim yaptınız. Lütfen bir numara girin.")

def menu_duzenle(menu):
    menu_goster(menu)
    try:
        secim = int(input("Düzenlemek istediğiniz ürünün numarasını girin: "))
        if secim < 1 or secim > len(menu):
            print("Geçersiz bir seçim yaptınız. Lütfen menüdeki bir numara girin.")
            return
        yeni_urun = input("Yeni ürün adını girin: ")
        yeni_fiyat = input("Yeni ürün fiyatını girin: ")
        menu[secim - 1] = (yeni_urun, yeni_fiyat)
        print("Ürün başarıyla güncellendi.")
    except ValueError:
        print("Geçersiz bir seçim yaptınız. Lütfen bir numara girin.")

def csv_olustur(menu, dosya_adi="menu.csv"):
    with open(dosya_adi, mode='w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Ürün', 'Fiyat']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for urun, fiyat in menu:
            writer.writerow({'Ürün': urun, 'Fiyat': fiyat})

if __name__ == "__main__":
    menu = menu_olustur()
    while True:
        print("\nMenü Yönetimi:")
        print("1. Mevcut Menüyü Görüntüle")
        print("2. Menüye Ürün Ekle")
        print("3. Menüden Ürün Sil")
        print("4. Menüdeki Ürünleri Düzenle")
        print("5. Çıkış")
        secim = input("Yapmak istediğiniz işlemi seçin: ")

        if secim == '1':
            menu_goster(menu)
        elif secim == '2':
            menu_ekle(menu)
        elif secim == '3':
            menu_sil(menu)
        elif secim == '4':
            menu_duzenle(menu)
        elif secim == '5':
            csv_olustur(menu)
            print("CSV dosyası menü başarıyla güncellendi.")
            break
        else:
            print("Geçersiz bir seçim yaptınız. Lütfen tekrar deneyiniz.")