import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load Data
def load_data():
    df_aotizhongxin = pd.read_csv("dashboard/PRSA_Data_Aotizhongxin_20130301-20170228.csv")
    df_changping = pd.read_csv("dashboard/PRSA_Data_Changping_20130301-20170228.csv")
    
    # Gabungkan dataset
    df = pd.concat([df_aotizhongxin, df_changping])
    
    # Isi missing values
    df_numeric = ["PM2.5", "PM10", "SO2", "NO2", "CO", "O3", "TEMP", "PRES", "DEWP", "RAIN", "WSPM"]
    df[df_numeric] = df[df_numeric].fillna(df[df_numeric].median())
    df["wd"] = df["wd"].fillna(df["wd"].mode()[0])
    
    return df

df = load_data()

# Sidebar
st.sidebar.title("Air Quality Dashboard")
st.sidebar.write("Analisis polusi udara di Aotizhongxin & Changping")

# 1️⃣ Ringkasan Data
st.title("📊 Air Quality Dashboard")
st.write("Dashboard ini menampilkan analisis kualitas udara berdasarkan data polusi di Aotizhongxin dan Changping.")

st.header("Ringkasan Data")

st.subheader("Perbandingan Konsentrasi Polutan")
df_pollutan = df.groupby("station")[["PM2.5", "PM10", "SO2", "NO2", "CO", "O3"]].mean()
st.dataframe(df_pollutan)

st.subheader("Tren PM2.5 dari Tahun ke Tahun")
df_pm25 = df.groupby(["year", "station"])["PM2.5"].mean().unstack()
df_pm25

st.header("Visualization & Explanatory Analysis")
col1, col2 = st.columns(2)
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📌 Perbandingan Konsentrasi Polutan")
    fig, ax = plt.subplots(figsize=(8, 5))
    df_pollutan.T.plot(kind="bar", ax=ax, colormap="coolwarm")
    ax.set_title("Rata-rata Konsentrasi Polutan di Aotizhongxin vs Changping", fontsize=14)
    ax.set_xlabel("Jenis Polutan", fontsize = 12)
    ax.set_ylabel("Konsentrasi Rata-rata (µg/m³ atau ppb)", fontsize = 12)
    ax.legend(title="Station")
    ax.grid(True, linestyle="--", alpha=0.7)
    st.pyplot(fig)

with col2:

    st.subheader("📉 Tren PM2.5 dari Tahun ke Tahun")

    fig, ax = plt.subplots(figsize=(8, 5))
    df_pm25.plot(kind="line", ax=ax, colormap="coolwarm")
    ax.set_title("Perubahan Rata - Rata PM2.5 per Tahun", fontsize=14)
    ax.set_xlabel("Tahun")
    ax.set_ylabel("Rata - rata PM2.5 (µg/m³)")
    ax.legend(["Aotizhongxin", "Changping"])
    ax.grid(True, linestyle="--", alpha=0.7)
    st.pyplot(fig)

with st.expander("Explanation Perbandingan Polutan di Aotizhongxin vs Changping"):
    st.write("""Aotizhongxin memiliki polusi lebih tinggi dibanding Chanping untuk semua polutan. 
PM10 dan PM2.5 tetap yang dominan di kedua lokasi. CO adalah outlier.""")
    
with st.expander("Explanation Perbandingan Polutan di Aotizhongxin vs Changping"):
    st.write("""Polusi udara di dua kota cenderung memiliki tren yang mirip pada kenaikan dan penurunannya. 
PM2.5 turun dari 2014 ke 2016, tetapi mengalami kenaikan yang signifikan pada tahun 2017. Aotizhongxin selalu lebih tinggi dibanding Changping, yang berarti lebih berpolusi.""")
    
st.header("Kesimpulan")
st.markdown('<div style="text-align: justify;">Aotizhongxin memiliki polusi lebih tinggi dibanding Changping untuk semua jenis polutan, PM2.5 dan PM10 adalah polutan yang dominan di dua tempat tersebut. Polusi udara memiliki kenaikan dan penurunan yang cenderung sama, turun pada 2016 dan naik signifikan pada 2017. perbedaannya adalah Aotizhongxin selalu lebih berpolusi daripada Changping</div>', unsafe_allow_html=True)
