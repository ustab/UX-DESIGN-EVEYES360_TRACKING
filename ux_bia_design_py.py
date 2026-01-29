import streamlit as st
import pandas as pd # Verileri tablo yapmak için

# --- 1. AYARLAR VE TASARIM ---
st.set_page_config(page_title="EVEYES 360 - NUC Accreditation", layout="wide")

# CSS Düzenlemesi (Koyu Mavi ve Profesyonel Görünüm)
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stMetric { background-color: #ffffff; padding: 20px; border-radius: 15px; border: 1px solid #3498db; box-shadow: 2px 2px 10px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

import os
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()
# Frontend'den gelecek veri yapısı (Data Schema)
class HealthData(BaseModel):
    frequency: float
    facialMood: Optional[str] = None
    manualMoodScore: Optional[int] = None

@app.post("/api/v1/analyze-condition")
async def analyze_condition(data: HealthData):
    final_stress = 0

    # 1. AI Yüz Analizi Mantığı
    if data.facialMood == "anxious":
        final_stress = 85
    elif data.facialMood == "depressed":
        final_stress = 90

    # 2. Kullanıcı Beyanı (Manuel giriş varsa AI verisini günceller/geçer)
    if data.manualMoodScore is not None:
        final_stress = data.manualMoodScore

    # 3. Musiki Engine: Karar Mekanizması
    result = {
        "makam": "Rast",
        "scent": "Rose",
        "instruction": "Standard balance mode activated."
    }

    if final_stress > 75:
        result = {
            "makam": "Saba",
            "scent": "Lilac",
            "instruction": "High stress/anxiety detected. Activating Saba Makamı & Lilac."
        }
    elif data.frequency < 432:
        result = {
            "makam": "Rehavi",
            "scent": "Sandalwood",
            "instruction": "Low energy detected. Rehavi Makamı will restore focus."
        }

    return {"status": "success", "data": result}

from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

class TherapySession(Base):
    __tablename__ = "therapy_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    ai_mood = Column(String)  # AI'nın yüz analiz sonucu
    frequency = Column(Float) # Biosonology verisi
    selected_makam = Column(String) # Seçilen şifa makamı
    scent = Column(String) # Eşleşen koku
    stress_reduction_rate = Column(Float) # Başarı oranı
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

# Müşteriye sunarken: "Her seans milisaniyelik hassasiyetle kaydedilir."

{
  "hospital_name": "Şehir Hastanesi",
  "patient_data": "Hasta Verileri",
  "bia_analysis": "BIA Analizi (Ödem Durumu)",
  "therapy_suggestion": "Önerilen Makam ve Koku"
}

# Tüm dilleri kapsayan veri yapısı
translations = {
    "tr": {
        "welcome": "Hoş geldiniz",
        "phase_angle": "Faz Açısı",
        "biosonology": "Biyosonoloji",
        "seljuk_therapy": "Selçuklu Müzik Terapi"
    },
    "en": {
        "welcome": "Welcome",
        "phase_angle": "Phase Angle",
        "biosonology": "Biosonology",
        "seljuk_therapy": "Seljuk Music Psychotherapy"
    },
    "ar": {
        "welcome": "مرحباً",
        "phase_angle": "زاوية الطور",
        "biosonology": "علم البيوسونولوجيا",
        "seljuk_therapy": "العلاج بالموسيقى في العصر السلجوقي"
    }
}

# Kullanıcının seçtiği dil (Dinamik olarak değişebilir)
current_lang = "tr"

def get_translation(key):
    """
    Belirtilen anahtarın çevirisini döndürür.
    Eğer dil veya anahtar bulunamazsa, hata vermek yerine anahtarın adını döndürür.
    """
    return translations.get(current_lang, {}).get(key, key)

# Kullanım Örnekleri
print(f"Başlık: {get_translation('welcome')}")
print(f"Teknik Terim: {get_translation('phase_angle')}")

import json

# Bu yapı veritabanından (PostgreSQL/JSONB) çekilmiş gibi simüle edilmiştir
therapy_data = {
    "hicaz_desc": {
        "tr": "Hicaz makamı ödem atar ve boşaltım sistemini dengeler.",
        "en": "Hicaz maqam reduces edema and balances the excretory system.",
        "ru": "Хиджаз макам уменьшает отеки и балансирует выделительную систему.",
        "ar": "مقام الحجاز يقلل من الوذمة ويوازن الجهاز الإخراجي."
    },
    "lavender_oil": {
        "tr": "Lavanta yağı kortizolü düşürerek hücresel ödemi azaltır.",
        "en": "Lavender oil reduces cellular edema by lowering cortisol.",
        "ar": "زيت اللافندر يقلل من الوذمة الخلوية عن طريق خفض الكورتيزول."
    }
}

def get_description(data_key, lang="tr"):
    # İlgili anahtarın seçilen dildeki karşılığını döner, yoksa anahtarın kendisini döner
    try:
        return therapy_data[data_key].get(lang, therapy_data[data_key]["en"])
    except KeyError:
        return "Data not found."

# Kullanım örneği
selected_lang = "tr" # Bu değer kullanıcı arayüzünden dinamik gelecek
print(f"EVEYES 360 Terapi Notu: {get_description('hicaz_desc', selected_lang)}")

import math
import json
import os
SETTINGS_FILE = 'settings.json'

def save_settings(hospital, doctor, contact):
    data = {"hospital": hospital, "doctor": doctor, "contact": contact}
    with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

def analyze_bia(resistance, reactance):
    """
    BIA verilerini analiz eder ve Faz Açısını hesaplar.
    Düşük Faz Açısı hücresel bozulma ve ödem işaretidir.
    """
    # Faz Açısı Hesaplama (Radyan -> Derece dönüşümü ile)
    phase_angle = math.degrees(math.atan(reactance / resistance))

    # Analiz sonuçları
    status = ""
    suggested_key = ""

    if phase_angle < 5.0:
        status = "Yüksek Ödem Riski / Hücresel Zayıflık"
        suggested_key = "hicaz_desc" # Selçuklu tıbbına göre ödem atıcı makam
    else:
        status = "Sağlıklı Hücre Bütünlüğü"
        suggested_key = "rast_desc"

    return round(phase_angle, 2), status, suggested_key

# Örnek Test: Rezistans=450, Reaktans=35 olan bir hasta için
pa, durum, tavsiye_anahtari = analyze_bia(450, 35)

print(f"Faz Açısı: {pa}°")
print(f"Durum: {durum}")
print(f"Reçete: {get_description(tavsiye_anahtari, 'tr')}")

import math
class Patient:
    def __init__(self, tckn, name, reason):
        self.tckn = tckn
        self.name = name
        self.reason = reason

class EVEYES360_System:
    def __init__(self):  # Eğer parantez içinde isim varsa onu sil, boş kalsın
        # 1. Önce ayarları dosyadan yüklemeyi dene
        self.status_db = {
    "kritik": {
        "tr": "Kritik (Ödem Saptandı)",
        "en": "Critical (Edema Detected)",
        "ar": "حرج (تم اكتشاف وذمة)",
        "ru": "Критический (Обнаружен отек)"
    },
    "normal": {
        "tr": "Normal (Hücresel Denge)",
        "en": "Normal (Cellular Balance)",
        "ar": "طبيعي (التوازن الخلوي)",
        "ru": "Нормальный (Клеточное равновесие)"
    }}
        settings = load_settings()
        
        if settings:
            # Eğer settings.json varsa ismi oradan al
            self.hospital_name = settings['hospital']
            self.doctor = settings['doctor']
            self.contact = settings['contact']
        else:
            # Eğer dosya yoksa varsayılan bir isim ata
            self.hospital_name = "EVEYES 360 Merkezi"
            self.doctor = "Bilinmiyor"
            self.contact = "-"
            
        # Buraya kendi therapy_db sözlüğünü eklemeyi unutma
        # DOĞRU YAZIM (Dictionary):
        self.therapy_db = {
        "hicaz_desc": {  # Burası iki nokta olmalı, virgül değil!
        "tr": "Hicaz makamı: Ödem atar.",
        "en": "Hicaz maqam: Reduces edema."
    },
        "rast_desc": {
        "tr": "Rast makamı: Neşe verir.",
        "en": "Rast maqam: Gives joy."
    } }
       
        
    """def __init__(self, hospital_name):
        self.hospital_name = hospital_name  # Kaydedilen hastane adı
        self.therapy_db = {
            "hicaz_desc": {
                "tr": "Hicaz makamı: Ödem atar, dinlendirir.",
                "en": "Hicaz maqam: Reduces edema, relaxes.",
                "ar": "مقام الحجاز: يقلل الوذمة، يريح."
            },
            "rast_desc": {
                "tr": "Rast makamı: Kemik sağlığı ve neşe verir.",
                "en": "Rast maqam: Bone health and joy.",
                "ar": "مقام الرست: صحة العظام والبهجة."
            }
        }"""

    def calculate_phase_angle(self, resistance, reactance):
        # Bilimsel Faz Açısı Formülü: arctan(Xc/R) * (180/pi)
        pa = math.degrees(math.atan(reactance / resistance))
        return round(pa, 2)

    def generate_report(self, patient, resistance, reactance, lang="tr"):
        # 1. Hesaplamayı yapıyoruz
        pa = self.calculate_phase_angle(resistance, reactance)
        
        # 2. Terminale anlık çıktı veriyoruz (Takip nedenini buraya ekledik)
        print(f"HASTA: {patient.name}")
        print(f"TAKİP NEDENİ: {patient.reason}") 
        
        # Önce hangi anahtarları (key) kullanacağımızı belirliyoruz
        if pa < 5.0:
            recete_key = "hicaz_desc"
            status_key = "kritik" if pa < 5.0 else "normal"
        else:
            recete_key = "rast_desc"
            status_key = "normal"

        # ŞİMDİ SİHİR BURADA: Mesajları sözlükten (DB) tek seferde çekiyoruz
        # Bu satırlar sayesinde 100 dil bile olsa kod değişmez!
        durum = self.status_db[status_key].get(lang, self.status_db[status_key]["en"])
        terapi = self.therapy_db[recete_key].get(lang, self.therapy_db[recete_key]["en"])

        # 4. Tüm veriyi bir sözlükte topluyoruz (Rapor çıktısı için)
        report = {
            "hospital": self.hospital_name,
            "patient": patient.name,    # patient_name yerine patient.name yaptık
            "reason": patient.reason,   # Takip nedenini rapora ekledik
            "phase_angle": pa,
            "status": durum,
            "therapy": self.therapy_db[recete_key].get(lang, self.therapy_db[recete_key]["en"])}
        return report
    
# 1. Hastane adını sisteme kaydediyoruz
my_app = EVEYES360_System()

# 2. Yeni bir hasta verisi geldiğini varsayalım (BIA ölçümü: R=500, Xc=30)
# Şimdi bu paketi (yeni_hasta) fonksiyona gönderiyoruz
yeni_hasta = Patient("12345678901", "Ahmet Yılmaz", "Kalp Yetmezliği - Ödem Takibi")
patient_report = my_app.generate_report(yeni_hasta, 500, 30, lang="tr")

# 3. Sonucu yazdıralım
print(f"--- {patient_report['hospital']} RAPORU ---")
print(f"Hasta: {patient_report['patient']}")
print(f"Takip Nedeni: {patient_report['reason']}") # Bunu eklemeyi unutma
print(f"BIA Faz Açısı: {patient_report['phase_angle']}°")
print(f"Teşhis: {patient_report['status']}")
print(f"Önerilen Tedavi: {patient_report['therapy']}")

import math

class EVEYES360_Biosonology:
    def __init__(self, hospital_name):
        self.hospital_name = hospital_name
        # Mood bozuklukları ve BIA verilerine göre makam eşleşmeleri
        self.makam_rehberi = {
            "düsükh_faz_acisi": {
                "makam": "Hicaz",
                "etki": "Ödem atıcı ve idrar yolları üzerinde etkili. Biosonology verisine göre hücre dışı suyun atılmasını destekler.",
                "mood": "Anksiyete azaltıcı"
            },
            "yuksek_stres": {
                "makam": "Neva",
                "etki": "Gevşetici ve yatıştırıcı. Ruhsal dengeyi sağlar.",
                "mood": "Depresyon ve keder karşıtı"
            },
            "genel_denge": {
                "makam": "Rast",
                "etki": "Kemik ve kas sağlığı. Hücresel canlılığı (vibrasyon) artırır.",
                "mood": "Neşe ve huzur verici"
            }
        }

    def analiz_et(self, pa_degeri, mood_notu=""):
        """
        BIA Faz Açısı ve hastanın mood durumuna göre reçete yazar.
        """
        print(f"\n--- {self.hospital_name} ANALİZ RAPORU ---")
        
        if pa_degeri < 5.0:
            recete = self.makam_rehberi["düsükh_faz_acisi"]
            print(f"Biyosonolojik Tespit: Hücresel titreşim zayıf (Faz Açısı: {pa_degeri}°)")
            print(f"Klinik Durum: Ödem ve düşük hücresel enerji.")
        else:
            recete = self.makam_rehberi["genel_denge"]
            print(f"Biyosonolojik Tespit: Hücresel titreşim normal (Faz Açısı: {pa_degeri}°)")

        print(f"Önerilen Makam: {recete['makam']}")
        print(f"Psikolojik Etki: {recete['mood']}")
        print(f"Açıklama: {recete['etki']}")
     
    # Fonksiyonu şöyle tanımla:
    def EVEYES360_Therapy(system_object):
    # ... rapor yazdırma kodları ...
        secim = input("\n👉 Bilimsel dayanakları okumak ister misiniz? (E/H): ").upper()
        if secim == "E":
        # Burada 'my_app' yerine 'system_object' kullanıyoruz
            print(system_object.get_scientific_article(lang="tr"))

# Sistemi Test Edelim
eveyes = EVEYES360_Biosonology("NIZAMIYE HOSPITAL")

# Diyelim ki BIA ölçümü 4.2 çıktı (Düşük/Ödemli)
eveyes.analiz_et(4.2)

class EVEYES360_Therapy:
    def __init__(self, hospital_name):
        self.hospital_name = hospital_name
        # Musiki, Koku ve Biyosonolojik Etki Matrisi
        self.therapy_matrix = {
            "odem_yuksek": {
                "makam": "Hicaz",
                "koku": "Gül ve Sandal Ağacı",
                "etki": "Diüretik (ödem atıcı) ve vazodilatör etki. Hücre dışı sıvıyı dengeler.",
                "mood": "Anksiyete ve gerginliği azaltır."
            },
            "stres_depresyon": {
                "makam": "Neva",
                "koku": "Lavanta ve Yasemin",
                "etki": "Kortizol baskılayıcı. Hücre zarını strese karşı korur (BIA Faz Açısını stabilize eder).",
                "mood": "Melankoli ve kederi dağıtır."
            },
            "enerji_dusuk": {
                "makam": "Rast",
                "koku": "Buhur ve Ud",
                "etki": "Hücresel vibrasyonu artırır. Kemik-kas sistemini uyarır.",
                "mood": "Yaşama sevinci ve zindelik verir."
            }
        }
        
        
    # 2. Kullanıcıya sor
    secim = input("\n👉 Bilimsel dayanakları ve akademik makaleyi okumak ister misiniz? (E/H): ").upper()

    if secim == "E":
        print("\n" + "="*70)
        print(f"\n{my_app.quick_info['tr']}")
        print("EVEYES 360 - AKADEMİK YAYIN")
        print("="*70)
    # Daha önce yazdığımız dosyadan okuma fonksiyonu:
        print(my_app.get_scientific_article(lang="tr"))
    else:
        print("\nSağlıklı günler dileriz!")
        
        
    def recete_olustur(self, faz_acisi, mood_notu=""):
        
        self.scientific_insight = {
            "tr": {
            "title": "BİLİMSEL DİPNOT: BİYOSONOLOJİ VE SELÇUKLU TIBBI",
            "content": "BURAYA KONTENT GELECEK Hücreler ses dalgalarına mekanik tepkiler verir. Biyosonoloji, hücresel vibrasyonun BIA değerleriyle (Faz Açısı) doğrudan ilişkili olduğunu savunur. Selçuklu döneminde Gevher Nesibe gibi şifahanelerde kullanılan müzikoterapi (Hicaz, Rast vb.) ve aromaterapi, bu biyolojik akordu düzeltmeyi amaçlar." },
            "en": {
            "title": "SCIENTIFIC INSIGHT: BIOSONOLOGY AND SELJUK MEDICINE",
            "content": "Cells respond mechanically to sound waves. Biosonology suggests that cellular vibration is directly linked to BIA values. Music therapy (Maqams) and aromatherapy used in Seljuk-era hospitals like Gevher Nesibe aim to restore this biological harmony."}}
        
        print(f"\n--- {self.hospital_name} REÇETE SİSTEMİ ---")
        
        # Karar mekanizması
        if faz_acisi < 5.0:
            key = "odem_yuksek"
        elif "uzgun" in mood_notu.lower() or "stres" in mood_notu.lower():
            key = "stres_depresyon"
        else:
            key = "enerji_dusuk"
            
        recete = self.therapy_matrix[key]
        
        print(f"Hücresel Durum: {'Kritik (Ödem)' if key == 'odem_yuksek' else 'Stabil'}")
        print(f"Dinletilecek Makam: {recete['makam']}")
        print(f"Uygulanacak Koku: {recete['koku']}")
        print(f"Biyolojik Etki: {recete['etki']}")
        print(f"Ruhsal Etki: {recete['mood']}")

    def generate_report(self, patient, r, xc, lang="tr"):
        # ... rapor kodları ...
        return report

    # EVEYES360_System sınıfının içindeki fonksiyonu şu şekilde güncelle:
    def get_scientific_article(self, lang="tr"):
        import os
    # Dosyanın tam yolunu belirleyelim
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_name = os.path.join(current_dir, f"makale_{lang}.txt")
    
        if os.path.exists(file_name):
             with open(file_name, "r", encoding="utf-8") as f:
                return f.read()
                
        else:
            # Eğer dosya yoksa kullanıcıyı bilgilendiren kısa bir özet dönelim
            if lang == "tr":
                return f"❌ HATA: {file_name} dosyası bulunamadı!"

    
    def EVEYES360_Therapy(system_object):
    # Burada raporu oluşturup yazdırdığın kodlar olmalı
    # Örnek kullanım:
        yeni_hasta = Patient("12345678901", "Ahmet Yılmaz", "Kalp Yetmezliği")
        report = system_object.generate_report(yeni_hasta, 500, 30, lang="tr")
    
        print(f"--- {report['hospital']} ANALİZ RAPORU ---")
        print(f"Biyosonolojik Tespit: {report['status']}")
    # ... diğer print satırların ...
    # Fonksiyonu şöyle çağır:
    # 1. Önce sistemi başlat
    my_app = EVEYES360_System()

    # 2. Sonra fonksiyonu çalıştır (NameError almamak için tanım yukarıda olmalı)
    EVEYES360_Therapy(my_app)
    # İŞTE BURADA SORUYU SORUYORUZ:
    secim = input("\n👉 Bilimsel dayanakları ve akademik makaleyi okumak ister misiniz? (E/H): ").upper()
    
    if secim == "E":
        print("\n" + "="*70)
        # Sınıfın içindeki o meşhur fonksiyonu çağırıyoruz
        print(system_object.get_scientific_article(lang="tr"))
        print("="*70)

# Test Edelim
terapi_merkezi = EVEYES360_Therapy("NIZAMIYE HOSPITAL")

# Örnek: Faz açısı 4.8 olan ve anksiyete yaşayan bir hasta
terapi_merkezi.recete_olustur(4.8, "Hasta kendini çok gergin ve huzursuz hissediyor.")

