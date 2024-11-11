# app.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

st.title("Analisis Data Kualitas Udara di Beijing")
st.write(
    """
Aplikasi ini menyediakan antarmuka untuk menganalisis dan memvisualisasikan data polusi udara dari berbagai stasiun pengukuran di Beijing.
"""
)

#----------------------------------load data : open folder
def load_data(folder_path):
    data_frames = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            file_path = os.path.join(folder_path, filename)
            df = pd.read_csv(file_path)
            data_frames.append(df)
    return pd.concat(data_frames, ignore_index=True)

folder_path = 'D:/Puji Ayu-Dicoding/Air-quality-dataset/PRSA_Data_20130301-20170228/'  # Sesuaikan dengan lokasi folder
data = load_data(folder_path)
st.write("Data Kualitas Udara:", data.head())


data['datetime'] = pd.to_datetime(data[['year', 'month', 'day', 'hour']])
data.fillna(data.mean(numeric_only=True), inplace=True)


#---------------------------------- polutan
pollutant = st.selectbox("Pilih Polutan:", ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3'])

#---------------------------------- Plot tren waktu untuk polutan
st.write(f"Tren Konsentrasi {pollutant} dari Waktu ke Waktu")
fig, ax = plt.subplots()
ax.plot(data['datetime'], data[pollutant], color='blue', linewidth=0.5)
ax.set_xlabel('Tanggal')
ax.set_ylabel(f'{pollutant} (µg/m³)')
ax.set_title(f'Tren {pollutant} di Beijing')
st.pyplot(fig)


#---------------------------------- faktor meteorologi
meteorology = st.selectbox("Pilih Faktor Meteorologi:", ['TEMP', 'PRES', 'WSPM', 'RAIN'])

#---------------------------------- Visualisasi korelasi
st.write(f"Korelasi antara {pollutant} dan {meteorology}")
fig, ax = plt.subplots()
sns.scatterplot(x=data[meteorology], y=data[pollutant], ax=ax)
ax.set_xlabel(meteorology)
ax.set_ylabel(pollutant)
ax.set_title(f"Korelasi antara {pollutant} dan {meteorology}")
st.pyplot(fig)


#---------------------------------- stasiun pengukuran
station = st.selectbox("Pilih Stasiun Pengukuran:", data['station'].unique())

# Filter data berdasarkan stasiun
station_data = data[data['station'] == station]

#---------------------------------- Plot distribusi
st.write(f"Distribusi {pollutant} di Stasiun {station}")
fig, ax = plt.subplots()
sns.histplot(station_data[pollutant], bins=30, kde=True, ax=ax, color='green')
ax.set_xlabel(pollutant)
ax.set_ylabel('Frekuensi')
ax.set_title(f"Distribusi {pollutant} di Stasiun {station}")
st.pyplot(fig)
