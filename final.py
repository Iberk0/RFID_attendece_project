import pandas as pd
from datetime import datetime

# Proje dosyasını oku
proje_df = pd.read_excel('proje.xlsx')

# İlgili hücreleri seç
card_ids = proje_df.iloc[7:51, 1].tolist()

# Liste dosyasını oku ve bir matris olarak sakla
liste_matrix = pd.read_excel('liste.xlsx').values

# Eşleşen kartların indexlerini saklamak için bir liste oluştur
matching_cards_index = []

# Kart numaralarını karşılaştır ve eşleşen kartların indexlerini bul
for i, row in enumerate(liste_matrix):
    if row[0] in card_ids:
        matching_cards_index.append(i)

# Eşleşen kartların isim ve soyisim bilgilerini al
matching_names = []
for index in matching_cards_index:
    name = liste_matrix[index, 1]
    surname = liste_matrix[index, 2]
    matching_names.append({'Name': name, 'Surname': surname})

# Tarihi al
date = datetime.now().strftime("%d-%m-%Y")

# Sonuçları bir metin dosyasına yaz
with open(f'{date}_yoklama.txt', 'w') as file:
    
    for name in matching_names:
        file.write(f"{name['Name']} {name['Surname']}\n")
