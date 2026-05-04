import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="BEP Kalkulator PKWU", page_icon="📊")

st.title("📊 KALKULATOR BEP PKWU")
st.markdown("### Hitung Break Even Point dengan Mudah")

with st.sidebar:
    st.header("⚙️ INPUT DATA")
    mode = st.radio("Pilih Mode:", ["Mode Cepat", "Mode Detail (Soal Kamu)"])

if mode == "Mode Cepat":
    fc = st.number_input("Fixed Cost (Biaya Tetap)", min_value=0, value=61000, step=1000)
    vc_total = st.number_input("Variable Cost Total", min_value=0, value=247000, step=1000)
    jumlah_unit = st.number_input("Jumlah Unit Produksi", min_value=1, value=25)
    harga = st.number_input("Harga Jual per Unit", min_value=1, value=15000, step=1000)
else:
    st.subheader("📝 Masukkan Pengeluaran Sesuai Soal:")
    galon = st.number_input("Beli galon", value=21000)
    gas = st.number_input("Beli gas", value=23000)
    mie_ayam = st.number_input("Mie + pangsit + ayam filet", value=100000)
    sayur = st.number_input("Sayuran + bumbu + cabai + saus", value=59000)
    belanja = st.number_input("Mie 2kg + sayur + daun bawang", value=44000)
    biaya_print = st.number_input("Print", value=7000)
    bensin = st.number_input("Bensin", value=24000)
    mika = st.number_input("Mika", value=30000)
    jumlah_unit = st.number_input("Jumlah unit yang dihasilkan", value=25)
    harga = st.number_input("Harga jual per unit", value=15000)
    
    vc_total = galon + gas + mie_ayam + sayur + belanja
    fc = biaya_print + bensin + mika
    
    st.info(f"✅ FC (Biaya Tetap): Rp {fc:,.0f} | VC Total: Rp {vc_total:,.0f}")

if vc_total > 0 and jumlah_unit > 0 and harga > 0:
    vc_per_unit = vc_total / jumlah_unit
    margin = harga - vc_per_unit
    
    if margin > 0:
        bep_unit = fc / margin
        bep_rupiah = bep_unit * harga
        
        col1, col2, col3 = st.columns(3)
        col1.metric("🎯 BEP (Unit)", f"{bep_unit:.0f} porsi")
        col2.metric("💰 BEP (Rupiah)", f"Rp {bep_rupiah:,.0f}")
        col3.metric("📈 Margin/Unit", f"Rp {margin:,.0f}")
        
        st.success(f"""
        ### 📌 Analisis:
        - Fixed Cost: Rp {fc:,.0f}
        - VC per unit: Rp {vc_per_unit:,.0f}
        - Harga Jual: Rp {harga:,.0f}
        
        **Kamu perlu menjual {bep_unit:.0f} unit untuk BEP**
        """)
        
        # Tabel
        st.subheader("📊 Tabel Laba/Rugi")
        qty_list = [int(bep_unit*0.5), int(bep_unit), int(bep_unit*1.5), jumlah_unit]
        data = []
        for q in qty_list:
            if q > 0:
                pendapatan = q * harga
                biaya = fc + (q * vc_per_unit)
                laba = pendapatan - biaya
                data.append({"Unit": q, "Pendapatan": f"Rp {pendapatan:,.0f}", "Biaya": f"Rp {biaya:,.0f}", "Laba/Rugi": f"Rp {laba:,.0f}"})
        st.table(data)
        
        # Grafik
        st.subheader("📈 Grafik BEP")
        x = np.arange(0, max(50, int(bep_unit*2)))
        pendapatan_line = x * harga
        biaya_line = fc + (x * vc_per_unit)
        
        fig, ax = plt.subplots(figsize=(10,5))
        ax.plot(x, pendapatan_line, 'g-', linewidth=2, label='Pendapatan')
        ax.plot(x, biaya_line, 'r-', linewidth=2, label='Total Biaya')
        ax.plot(bep_unit, bep_rupiah, 'bo', markersize=8, label=f'BEP ({bep_unit:.0f})')
        ax.fill_between(x, pendapatan_line, biaya_line, where=(pendapatan_line>=biaya_line), color='green', alpha=0.2)
        ax.fill_between(x, pendapatan_line, biaya_line, where=(pendapatan_line<biaya_line), color='red', alpha=0.2)
        ax.axvline(x=bep_unit, color='blue', linestyle='--')
        ax.set_xlabel('Unit Terjual')
        ax.set_ylabel('Rupiah')
        ax.set_title('Grafik Break Even Point')
        ax.legend()
        ax.grid(True, alpha=0.3)
        st.pyplot(fig)
        
        if bep_unit <= jumlah_unit:
            st.balloons()
            st.success(f"✅ Selamat! BEP tercapai dalam 1x produksi. Cukup jual {bep_unit:.0f} dari {jumlah_unit} unit.")
        else:
            st.warning(f"⚠️ Perlu produksi {int(np.ceil(bep_unit/jumlah_unit))}x untuk BEP")
    else:
        st.error("❌ Harga jual harus lebih besar dari biaya variabel per unit")