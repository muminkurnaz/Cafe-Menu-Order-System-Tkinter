# Cafe-Menu-Order-System-Tkinter
A graphical user interface application for cafe menu and order management built using Python's Tkinter library.


## How to Create a Menu and Export it as a CSV File

This application allows you to create a menu by entering product names and prices, and then export the menu as a CSV file which can be used within the application.

### Creating the Menu

1. Run the following command to start the menu creation process:
    ```sh
    python create_menu.py
    ```

2. Follow the prompts to enter product names and prices. To finish and save the menu, press 'q'.

### Example Usage

```python
import csv

def menu_olustur():
    menu = []
    while True:
        urun = input("Ürün adını girin (Çıkmak için 'q' tuşuna basın): ")
        if urun.lower() == 'q':
            break
        fiyat = input("Ürün fiyatını girin: ")
        menu.append((urun, fiyat))
    return menu

def csv_olustur(menu, dosya_adi="menu.csv"):
    with open(dosya_adi, mode='w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Ürün', 'Fiyat']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for urun, fiyat in menu:
            writer.writerow({'Ürün': urun, 'Fiyat': fiyat})

if __name__ == "__main__":
    menu = menu_olustur()
    csv_olustur(menu)
    print("CSV dosyası başarıyla oluşturuldu.")
     ```
### Note
The menu_olustur function collects the product names and prices from the user until 'q' is pressed.
The csv_olustur function writes the collected menu data to a CSV file named menu.csv by default.
You can now use the generated menu.csv file in the application for managing orders.

## Screenshots

![menü1](https://github.com/muminkurnaz/Cafe-Menu-Order-System-Tkinter/assets/112796390/ea126c2e-b771-440d-8cdb-87b005f9b790)




## Contributing
Contributions are welcome! Please fork this repository and submit pull requests to contribute to the project.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.

## Contact
For any questions or inquiries, please contact [mmnkrnz@gmail.com.
