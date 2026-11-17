import streamlit as st
import pandas as pd
import plotly.express as px

# Konfigurasi Halaman Web
st.set_page_config(page_title="Dashboard Keuangan Pribadi", page_icon="💰", layout="wide")

st.title("📊 Dashboard Keuangan Otomatis")
st.markdown("Pantau arus kas masuk dan keluar secara interaktif langsung dari VS Code.")

# Membaca Data CSV
@st.cache_data
def load_data():
    df = pd.read_csv("transaksi_mentah.csv")
    df["Tanggal"] = pd.to_datetime(df["Tanggal"])
    return df

df = load_data()

# Sidebar Filter
st.sidebar.header("🔍 Filter Data")
kategori_pilihan = st.sidebar.multiselect(
    "Pilih Kategori Transaksi:",
    options=df["Kategori"].unique(),
    default=df["Kategori"].unique()
)

df_filtered = df[df["Kategori"].isin(kategori_pilihan)]

# Hitung Metrik Utama
total_pemasukan = df_filtered[df_filtered["Jumlah"] > 0]["Jumlah"].sum()
total_pengeluaran = abs(df_filtered[df_filtered["Jumlah"] < 0]["Jumlah"].sum())
sisa_saldo = total_pemasukan - total_pengeluaran

col1, col2, col3 = st.columns(3)
col1.metric("Total Pemasukan", f"Rp {total_pemasukan:,.0f}")
col2.metric("Total Pengeluaran", f"Rp {total_pengeluaran:,.0f}")
col3.metric("Sisa Saldo", f"Rp {sisa_saldo:,.0f}")

st.markdown("---")

# Grafik Interaktif
col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.subheader("Porsi Pengeluaran per Kategori")
    df_pengeluaran = df_filtered[df_filtered["Jumlah"] < 0].copy()
    df_pengeluaran["Jumlah_Absen"] = df_pengeluaran["Jumlah"].abs()

    if not df_pengeluaran.empty:
        fig_pie = px.pie(df_pengeluaran, names="Kategori", values="Jumlah_Absen", hole=0.4)
        st.plotly_chart(fig_pie, use_container_width=True)
    else:
        st.info("Tidak ada data pengeluaran.")

with col_chart2:
    st.subheader("Arus Kas per Tanggal")
    fig_bar = px.bar(df_filtered, x="Tanggal", y="Jumlah", color="Kategori")
    st.plotly_chart(fig_bar, use_container_width=True)

# Tabel Data
st.subheader("📋 Rincian Data Transaksi")
st.dataframe(df_filtered, use_container_width=True)