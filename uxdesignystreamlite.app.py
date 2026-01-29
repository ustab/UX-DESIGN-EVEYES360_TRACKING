import streamlit as st
import math
import json
import os

# --- 1. AYARLAR VE TASARIM ---
st.set_page_config(page_title="EVEYES 360", layout="wide")

# CSS - Hastane Teması
st.markdown("""
    <style>
    .stMetric { background-color: #ffffff; padding: 20px; border-radius: 15px; border: 1px solid #3498db; }
    .report-box { background-color: #e3f2fd; padding: 20px; border-radius: 10px; border-left: 5px solid #1565c0; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. VERİ VE DİL DESTEĞİ ---
translations = {
    "tr": {
        "welcome": "EVEYES 360 Analiz Paneli",
        "hospital_label": "Hastane Adı",
        "patient_name": "Hasta Adı",
        "calc_btn": "Analiz Et ve Reçete Oluştur",
        "article_btn": "Bilimsel Makaleyi Oku",
        "phase_angle": "Faz Açısı",
        "scientific_note": "Biyosonoloji ve Selçuklu Tıbbı Notu"
    },
    "en": {
        "welcome": "EVEYES 360 Analysis Panel",
        "hospital_label": "Hospital Name",
        "patient_name": "Patient Name",
        "calc_btn": "Analyze & Generate Prescription",
        "article_btn": "Read Scientific Article",
        "phase_angle": "Phase Angle",
        "scientific_note": "Biosonology and Seljuk Medicine Note"
    }
}

# Dil Seçimi
lang_choice = st.sidebar.selectbox("Language / Dil", ["tr", "en", "ar", "ru"])
t = translations.get(lang_choice, translations["en"])

# --- 3. MANTIK SINIFLARI ---
class EVEYES360_Engine:
    def calculate_phase_angle(self, resistance, reactance):
        pa = math.degrees(math.atan(reactance / resistance))
        return round(pa, 2)

    def get_therapy(self, pa, mood):
        if pa < 5.0:
            return {
                "makam": "Hicaz",
                "koku": "Gül / Sandal Ağacı",
                "etki": "Hücre dışı ödem atıcı, diüretik etki.",
                "detay": "Selçuklu döneminde ödemli hastalar için Hicaz makamı tercih edilirdi."
            }
        else:
            return {
                "makam": "Rast",
                "koku": "Ud / Buhur",
                "etki": "Kemik sağlığı ve zindelik.",
                "detay": "Rast makamı hücresel vibrasyonu stabilize eder."
            }

# --- 4. STREAMLIT ARAYÜZÜ ---
st.title(f"🏥 {t['welcome']}")

col1, col2 = st.columns(2)

with col1:
    hosp_name = st.text_input(t["hospital_label"], value="NIZAMIYE HOSPITAL")
    p_name = st.text_input(t["patient_name"], value="Ahmet Yılmaz")
    reason = st.text_area("Takip Nedeni / Reason")

with col2:
    res = st.number_input("Resistance (Ω)", value=500)
    reac = st.number_input("Reactance (Xc)", value=30)
    mood = st.selectbox("Mood / Ruh Hali", ["Stabil", "Anxious (Anksiyete)", "Depressed (Depresif)"])

engine = EVEYES360_Engine()

if st.button(t["calc_btn"]):
    pa_result = engine.calculate_phase_angle(res, reac)
    therapy = engine.get_therapy(pa_result, mood)
    
    st.divider()
    
    # Metrikler
    m1, m2, m3 = st.columns(3)
    m1.metric(t["phase_angle"], f"{pa_result}°")
    m2.metric("Önerilen Makam", therapy["makam"])
    m3.metric("Önerilen Koku", therapy["koku"])
    
    # Rapor Alanı
    st.markdown(f"""
    <div class="report-box">
        <h3>{hosp_name} - Analiz Raporu</h3>
        <p><b>Hasta:</b> {p_name}</p>
        <p><b>Biyosonolojik Tespit:</b> {therapy['etki']}</p>
        <p><b>Akademik Not:</b> {therapy['detay']}</p>
    </div>
    """, unsafe_allow_html=True)

# --- 5. MAKALE BÖLÜMÜ ---
st.sidebar.divider()
if st.sidebar.button(t["article_btn"]):
    st.subheader(t["scientific_note"])
    # Burada makale_tr.txt dosyasını okuma simülasyonu
    st.write("""
    **Hücreler ses dalgalarına mekanik tepkiler verir.** Biyosonoloji, hücresel vibrasyonun BIA değerleriyle doğrudan ilişkili olduğunu savunur. 
    Selçuklu döneminde Gevher Nesibe gibi şifahanelerde kullanılan müzikoterapi, 
    bu biyolojik akordu düzeltmeyi amaçlar.
    """)
