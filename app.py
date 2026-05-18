import streamlit as st
import pandas as pd

# =========================
# KONFIGURASI HALAMAN
# =========================

st.set_page_config(
    page_title="SmartActuary",
    page_icon="💰",
    layout="wide"
)

# =========================
# CUSTOM CSS
# =========================

st.markdown("""
<style>

/* BACKGROUND UTAMA */
.main {
    background-color: #f4f7fb;
}

/* JARAK ATAS */
.block-container {
    padding-top: 2rem;
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background-color: #2563eb;
}

section[data-testid="stSidebar"] * {
    color: white;
}

/* JUDUL */
h1 {
    color: #1e3a8a;
    font-weight: bold;
}

h2, h3 {
    color: #2563eb;
}

/* CARD */
.card {
    background-color: white;
    padding: 25px;
    border-radius: 18px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.08);
    margin-bottom: 20px;
    color: #0f172a;
    border-left: 6px solid #2563eb;
}

/* BUTTON */
.stButton>button {
    background: #2563eb;
    color: white;
    border-radius: 12px;
    border: none;
    padding: 12px 25px;
    font-size: 16px;
    font-weight: bold;
    width: 100%;
}

.stButton>button:hover {
    background: #1d4ed8;
}

/* METRIC */
[data-testid="metric-container"] {
    background-color: white;
    border: 1px solid #dbeafe;
    padding: 15px;
    border-radius: 15px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}

/* DATAFRAME */
[data-testid="stDataFrame"] {
    background-color: white;
    border-radius: 15px;
    padding: 10px;
}

/* INFO BOX */
.stAlert {
    border-radius: 12px;
}

/* SUCCESS BOX */
.stSuccess {
    background-color: #dbeafe;
    color: #1e3a8a;
}

/* INPUT */
.stNumberInput input {
    border-radius: 10px;
}

/* RADIO MENU */
.stRadio label {
    font-size: 16px;
}

</style>
""", unsafe_allow_html=True)

# =========================
# SIDEBAR
# =========================

st.sidebar.title("SmartActuary")

menu = st.sidebar.radio(
    "",
    [
        "Dashboard",
        "Simulator Pinjaman",
        "Dana Pensiun",
    ]
)

# =========================
# DASHBOARD
# =========================

if menu == "Dashboard":

    st.title("SMARTACTUARY")

    st.markdown("""
    <div class="card">
    <p>
    SmartActuary merupakan aplikasi simulasi matematika
    aktuaria berbasis Python dan Streamlit. 
    SmartActuary membantu pengguna melakukan simulasi
    pinjaman, tabel amortisasi, dan dana pensiun
    secara mudah dan interaktif.
    </p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)

    c1.success("Simulasi Pinjaman")
    c2.success("Tabel Amortisasi")
    c3.success("Dana Pensiun")

# =========================
# SIMULATOR PINJAMAN
# =========================

elif menu == "Simulator Pinjaman":

    st.title("Simulator Pinjaman & Tabel Amortisasi")

    st.markdown("""
    <div class="card">
    Masukkan data berikut untuk menghitung cicilan
    dan tabel amortisasi.
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:

        pinjaman = st.text_input(
            "Jumlah Pinjaman (Rp)",
            placeholder="Contoh: 20.000.000"
        )

        bunga = st.text_input(
            "Bunga per Tahun (%)",
            placeholder="Masukkan Bunga"
        )

    with col2:

        tahun = st.text_input(
            "Lama Pinjaman (Tahun)",
            placeholder=" Masukkan Tahun"
        )

    st.markdown("---")

    if st.button("Hitung Pinjaman"):

        i = float(bunga.replace(",", ".")) / 100
        n = int(tahun)
        P = int(pinjaman.replace(".",""))

        # Rumus Anuitas
        an = (1 - (1 + i) ** (-n)) / i
        R = P / an

        total_bayar = R * n
        total_bunga = total_bayar - P

        st.success(
            f"Cicilan per Tahun: Rp {R:,.0f}"
        )

        st.markdown("---")

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "Cicilan / Tahun",
            f"Rp {R:,.0f}"
        )

        c2.metric(
            "Total Pembayaran",
            f"Rp {total_bayar:,.0f}"
        )

        c3.metric(
            "Total Bunga",
            f"Rp {total_bunga:,.0f}"
        )

        st.markdown("---")

        # TABEL AMORTISASI

        data = []

        sisa_utang = P

        for t in range(1, n + 1):

            bunga_tahun = sisa_utang * i

            pokok = R - bunga_tahun

            sisa_utang -= pokok

            if sisa_utang < 0:
                sisa_utang = 0

            data.append({
                "Tahun": t,
                "Cicilan": round(R),
                "Bunga": round(bunga_tahun),
                "Pokok": round(pokok),
                "Sisa Utang": round(sisa_utang)
            })

        df = pd.DataFrame(data)

        st.write("### Tabel Amortisasi")

        st.dataframe(df)

        st.write("### Grafik Sisa Utang")

        grafik_df = pd.DataFrame({
            "Tahun": df["Tahun"],
            "Sisa Utang": df["Sisa Utang"]
        })

        st.line_chart(
            grafik_df.set_index("Tahun")
        )

        st.info("""
        Grafik menunjukkan penurunan sisa utang
        setiap tahun setelah dilakukan pembayaran cicilan.
        """)

# =========================
# DANA PENSIUN
# =========================

elif menu == "Dana Pensiun":

    st.title("Simulasi Dana Pensiun")

    st.markdown("""
    <div class="card">
    Masukkan data untuk menghitung
    estimasi dana pensiun berdasarkan
    tabungan tahunan dan bunga.
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:

        tabungan = st.text_input(
            "Tabungan per Tahun (Rp)",
            placeholder="Contoh: 10.000.000"
        )

        bunga_pensiun = st.text_input(
            "Bunga per Tahun (%)",
            placeholder="Masukkan Bunga"
        )

    with col2:

        usia_sekarang = st.text_input(
            "Usia Sekarang",
            placeholder="Masukkan Usia"
        )

        usia_pensiun = st.text_input(
            "Usia Pensiun",
            placeholder="Masukkan Usia"
        )

    st.markdown("---")

    if st.button("Hitung Dana Pensiun"):

        if (
            tabungan == "" or
            bunga_pensiun == ""
        ):

            st.warning(
                "Masukkan semua data terlebih dahulu."
            )

        else:

            tabungan_bersih = int(
                tabungan.replace(".", "")
            )

            i = float(
                bunga_pensiun.replace(",", ".")
            ) / 100

            usia_awal = int(usia_sekarang)
            usia_akhir= int(usia_pensiun)
            n = usia_akhir-usia_awal

            hasil = tabungan_bersih * (
                ((1 + i) ** n - 1) / i
            )

            st.success(
                f"Total Dana Pensiun: Rp {hasil:,.0f}"
            )

            st.markdown("---")

            c1, c2, c3 = st.columns(3)

            c1.metric(
                "Usia Sekarang",
                f"{usia_awal} Tahun"
            )

            c2.metric(
                "Usia Pensiun",
                f"{usia_akhir} Tahun"
            )

            c3.metric(
                "Lama Menabung",
                f"{n} Tahun"
            )

            # DATA GRAFIK

            tahun_list = []

            dana_list = []

            for t in range(1, n + 1):

                dana = tabungan_bersih * (
                    (((1 + i) ** t) - 1) / i
                )

                tahun_list.append(t)

                dana_list.append(dana)

            grafik = pd.DataFrame({
                "Tahun": tahun_list,
                "Dana Pensiun": dana_list
            })

            st.write("### Grafik Pertumbuhan Dana")

            st.line_chart(
                grafik.set_index("Tahun")
            )

            st.info("""
            Grafik menunjukkan pertumbuhan
            dana pensiun dari tahun ke tahun.Semakin lama periode menabung,
            maka total dana yang terkumpul
            akan semakin besar.
            """)