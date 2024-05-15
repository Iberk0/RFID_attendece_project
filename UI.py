import os
import streamlit as st
from datetime import datetime
import time
import pandas as pd
def excel_oku():
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

    yoklama_klasoru = "yoklamalar"
    if not os.path.exists(yoklama_klasoru):
        os.makedirs(yoklama_klasoru)
    # Sonuçları bir metin dosyasına yaz
    with open(f'{yoklama_klasoru}/{date}_yoklama.txt', 'w',encoding='utf-8') as file:
        
        for name in matching_names:
            file.write(f"{name['Name']} {name['Surname']}\n")


# Anlık tarihi al ve date adlı bir değişkene koy
date = datetime.now().strftime("%d-%m-%Y")

# txt dosyasını oku ve içeriği listeye aktar
def read_attendance_list():
    attendance_list = []
    try:
        with open(f'yoklamalar/{date}_yoklama.txt', 'r', encoding='utf-8') as file:
            for line in file:
                attendance_list.append(line.strip())
    except FileNotFoundError:
        st.error("Dosya yok")
    return attendance_list


# Streamlit web arayüzü
def main():

    ders_adi_input = st.empty()
    ders_adi = ders_adi_input.text_input("Ders adı giriniz:")
   
    if ders_adi: 
        ders_adi_input.write("Başlamak için açılacak excel dosyasında 'Data Streamer' sekmesinden cihazı bağlayın ve veri akışını başlatın")
        time.sleep(5)
        os.system(f'start "" "proje.xlsx"')   
        ders_adi_input.empty()
        st.title("Yoklama Listesi")
        st.markdown("Onur Alp Gündüz ve Kerim Ayberk Çıtak tarafından yapıldı")
        st.markdown("---")
        
        st.header(f"{ders_adi} Dersinin {date} Tarihindeki Yoklama Listesi")
        
        # Yazının altında öğrenci adları
        
        
        # Yoklama listesini oku
        attendance_list = read_attendance_list()
        
        # Yoklama listesini göster
        if attendance_list:
            st.write("Yoklama Listesi:")
            for item in attendance_list:
                st.write(item)
        else:
            st.warning("Yoklama listesi boş.")
        
        # Yenileme butonu
        if st.button("Yenilemek için tıklayın"):
            excel_oku()
            attendance_list = read_attendance_list()
        

if __name__ == "__main__":
    main()
