import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style("whitegrid")

st.set_page_config(page_title="Analisis Gojek - TAM", layout="wide")
st.title("📊 Analisis Kemudahan & Kepercayaan Pengguna Aplikasi Gojek")
st.caption("Kelompok 1_PDRL — Technology Acceptance Model (TAM)")

# ======================
# 1. UPLOAD FILE CSV
# ======================
uploaded_file = st.file_uploader("Upload dataset CSV hasil kuesioner", type=["csv"])

if uploaded_file is None:
    st.info("Silakan upload file CSV dataset untuk melihat analisis.")
    st.stop()

df = pd.read_csv(uploaded_file)

# Filter hanya responden valid (pengguna Gojek, usia >=18)
kolom_filter = 'Apakah Anda pengguna Gojek dan berusia minimal 18 tahun?  '
if kolom_filter in df.columns:
    df = df[df[kolom_filter] == 'Ya'].copy()

cols = df.columns.tolist()

# ======================
# 2. MAPPING KOLOM PER VARIABEL
# ======================
kinerja_cols     = cols[9:14]
kemudahan_cols   = cols[14:19]
kepercayaan_cols = cols[19:24]
niatpakai_cols   = cols[24:29]

variabel_kolom = {
    "Kinerja": kinerja_cols,
    "Kemudahan": kemudahan_cols,
    "Kepercayaan": kepercayaan_cols,
    "Niat_Pakai": niatpakai_cols,
}
label_tampil = {"Kinerja": "Kinerja", "Kemudahan": "Kemudahan",
                "Kepercayaan": "Kepercayaan", "Niat_Pakai": "Niat Pakai"}

for var, kolom in variabel_kolom.items():
    df[f"Skor_{var}"] = df[kolom].astype(float).mean(axis=1)

rata_rata = df[[f"Skor_{v}" for v in variabel_kolom]].mean()

st.success(f"Jumlah responden valid: {len(df)}")

# ======================
# 3. METRIC RINGKASAN
# ======================
col1, col2, col3, col4 = st.columns(4)
col1.metric("Kinerja", f"{rata_rata['Skor_Kinerja']:.2f} / 5")
col2.metric("Kemudahan", f"{rata_rata['Skor_Kemudahan']:.2f} / 5")
col3.metric("Kepercayaan", f"{rata_rata['Skor_Kepercayaan']:.2f} / 5")
col4.metric("Niat Pakai", f"{rata_rata['Skor_Niat_Pakai']:.2f} / 5")

st.divider()

# ======================
# 4. CHART SUMMARY
# ======================
st.subheader("Rata-rata Skor Variabel Penelitian")
fig1, ax1 = plt.subplots(figsize=(8, 5))
warna = ["#2e7d32", "#c5e1a5", "#8bc34a", "#ffd54f"]
bars = ax1.bar(label_tampil.values(), rata_rata.values, color=warna)
ax1.set_ylim(0, 5)
ax1.set_ylabel("Rata-rata Skor")
for bar, val in zip(bars, rata_rata.values):
    ax1.text(bar.get_x() + bar.get_width()/2, val + 0.05, f"{val:.2f}", ha="center", fontweight="bold")
st.pyplot(fig1)

st.divider()

# ======================
# 5. DISTRIBUSI JAWABAN (interaktif - pilih variabel)
# ======================
st.subheader("Distribusi Jawaban per Variabel")
variabel_pilihan = st.selectbox("Pilih variabel:", list(variabel_kolom.keys()),
                                  format_func=lambda x: label_tampil[x])

skor_bulat = df[f"Skor_{variabel_pilihan}"].round().clip(1, 5).astype(int)
counts = skor_bulat.value_counts().reindex([1, 2, 3, 4, 5], fill_value=0)

fig2, ax2 = plt.subplots(figsize=(8, 5))
bars2 = ax2.bar(counts.index, counts.values, color="#4caf50", edgecolor="#2e7d32")
ax2.set_xlabel("Skor (1-5)")
ax2.set_ylabel("Jumlah Responden")
ax2.set_xticks([1, 2, 3, 4, 5])
for bar in bars2:
    h = bar.get_height()
    if h > 0:
        ax2.text(bar.get_x() + bar.get_width()/2, h + 0.3, int(h), ha="center")
st.pyplot(fig2)

st.divider()

# ======================
# 6. PROFIL RESPONDEN
# ======================
st.subheader("Profil Responden")
c1, c2, c3 = st.columns(3)

with c1:
    if 'Usia' in df.columns:
        fig3, ax3 = plt.subplots()
        usia_counts = df['Usia'].value_counts()
        ax3.pie(usia_counts.values, labels=usia_counts.index, autopct="%1.1f%%",
                colors=["#2e7d32", "#8bc34a", "#c8e6c9"])
        ax3.set_title("Generasi")
        st.pyplot(fig3)

with c2:
    if 'Jenis kelamin' in df.columns:
        fig4, ax4 = plt.subplots()
        gender_counts = df['Jenis kelamin'].value_counts()
        ax4.pie(gender_counts.values, labels=gender_counts.index, autopct="%1.1f%%",
                colors=["#66bb6a", "#dcedc8"])
        ax4.set_title("Jenis Kelamin")
        st.pyplot(fig4)

with c3:
    if 'Layanan Paling Sering' in df.columns:
        fig5, ax5 = plt.subplots()
        layanan_counts = df['Layanan Paling Sering'].value_counts()
        ax5.pie(layanan_counts.values, labels=layanan_counts.index, autopct="%1.1f%%",
                colors=["#1b5e20", "#4caf50", "#a5d6a7", "#e8f5e9"])
        ax5.set_title("Layanan Tersering")
        st.pyplot(fig5)
