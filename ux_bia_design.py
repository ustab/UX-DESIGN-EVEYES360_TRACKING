import math
import json
import os
import datetime
from typing import Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, func, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
# --- 1. VERİTABANI AYARLARI ---
# SQLite kullanarak 'eveyes360.db' adında bir dosya oluşturur.
DATABASE_URL = "sqlite:///./eveyes360.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) # Düzeltildi: bind=engine aktif edildi
Base = declarative_base()

# --- 3. API TANIMLAMALARI ---
app = FastAPI(title="EVEYES 360 Professional API")
core = EVEYES360_Biosonology(hospital_name="Şehir Hastanesi")
# --- 4. API ENDPOINT (ANA GİRİŞ) ---
app = FastAPI() 
@app.post("/api/v1/analyze-condition")
# --- 3. API MODELLEMESİ ---
app = FastAPI(title="EVEYES 360 Professional API")
# --- 4. API ENDPOINT'LERİ ---
@app.post("/api/v1/analyze")
async def perform_analysis(req: AnalysisRequest):
    db = SessionLocal()
    final_stress = 0

class TherapySession(Base):
    __tablename__ = "therapy_sessions"
    id = Column(Integer, primary_key=True, index=True)
    patient_name = Column(String)
    ai_mood = Column(String)
    phase_angle = Column(Float)
    selected_makam = Column(String)
    scent = Column(String)
    created_at = Column(DateTime, default=func.now()) # Sunucu saatini otomatik alır
    
Base.metadata.create_all(bind=engine)    

class EVEYES360_Biosonology:
    def __init__(self, hospital_name):
        self.hospital_name = hospital_name
        self.article = "Biyosonoloji ve Selçuklu tıbbı üzerine makale..."

    def calculate_phase_angle(self, resistance: float, reactance: float):
        # Biyosonoloji Temelli Faz Açısı Formülü
        pa = math.degrees(math.atan(reactance / resistance))
        return round(pa, 2)
    
    def get_scientific_article(self, lang="tr"):
        articles = {
            "tr": "Hücreler ses dalgalarına mekanik tepkiler verir. Selçuklu dönemi şifahanelerinde "
                  "uygulanan müzikoterapi, bu biyolojik akordu (Faz Açısı dengesini) düzeltmeyi hedefler.",
            "en": "Cells respond mechanically to sound waves. Seljuk-era music therapy aims to "
                  "restore this biological harmony and balance the Phase Angle."
        }
        return articles.get(lang, articles["en"])

class TherapySession(Base):
    __tablename__ = "therapy_sessions"
    __table_args__ = {'extend_existing': True} 
    patient_name = Column(String)
    #id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    ai_mood = Column(String)  # AI'nın yüz analiz sonucu
    frequency = Column(Float) # Biosonology verisi
    selected_makam = Column(String) # Seçilen şifa makamı
    scent = Column(String) # Eşleşen koku
    stress_reduction_rate = Column(Float) # Başarı oranı
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
     
    # Fonksiyonu şöyle tanımla:
    def EVEYES360_Therapy(system_object):
    # ... rapor yazdırma kodları ...
        secim = input("\n👉 Bilimsel dayanakları okumak ister misiniz? (E/H): ").upper()
        if secim == "E":
        # Burada 'my_app' yerine 'system_object' kullanıyoruz
            print(system_object.get_scientific_article(lang="tr"))

    # Sistemi Test Edelim
    eveyes = EVEYES360_Biosonology("NIZAMIYE HOSPITAL")
    SETTINGS_FILE = 'settings.json'
    def save_settings(hospital, doctor, contact):
        data = {"hospital": hospital, "doctor": doctor, "contact": contact}
        with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
                 json.dump(data, f, ensure_ascii=False, indent=4)
    def load_settings():
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
            
class EVEYES360_Engine:
    def __init__(self, hospital_name: str):
        self.hospital_name = hospital_name
    def analyze_bia(self, resistance: float, reactance: float):
       #pa = math.degrees(math.atan(reactance / resistance)) 
        pa= core.analyze_bia(req_resistance, req_reactance) 
        if pa < 5.0:
           status = "Yüksek Ödem Riski / Hücresel Zayıflık"
           suggested_key = "hicaz_desc" # Selçuklu tıbbına göre ödem atıcı makam 
           print(f"Biyosonolojik Tespit: Hücresel titreşim zayıf (Faz Açısı: {pa_degeri}°)")

        else:
           recete = self.makam_rehberi["genel_denge"]
           print(f"Biyosonolojik Tespit: Hücresel titreşim normal (Faz Açısı: {pa_degeri}°)")

 # --- DOĞRU SIRALAMA ---

# 1. Sınıf Tanımı (En başta ve en solda olmalı)

class EVEYES360_Engine:
    def __init__(self, hospital_name):
        self.hospital_name = hospital_name
        core = EVEYES360_Engine(hospital_name="NIZAMIYE HOSPITAL")  
   
    def analyze_bia(self, resistance: float, reactance: float):
        import math
        pa = math.degrees(math.atan(reactance / resistance))
        return round(pa, 2)

class Patient:
    def __init__(self, tckn, name, reason):
        self.tckn = tckn
        self.name = name
        self.reason = reason

# --- 2. ANALİZ MODELLERİ ---
class AnalysisRequest(BaseModel):
    patient_name: str
    resistance: float
    reactance: float
    facial_mood: Optional[str] = "neutral"
    lang: str = "tr"
# --- 3. CORE LOGIC (Biyosonoloji & Selçuklu Tıbbı) ---

def get_therapy_logic(pa: float, mood: str):
    """Biyosonoloji verilerini Selçuklu makam terapisiyle eşleştirir."""
    if pa < 5.0 or mood in ["anxious", "sad"]:
        return {
            "makam": "Hicaz", 
            "scent": "Gül Yağı", 
            "note": "Hücresel ödem tespiti. Hicaz makamı ve Gül aroması ile dengeleme önerilir."
        }
    return {
        "makam": "Rast", 
        "scent": "Sandal Ağacı", 
        "note": "Hücresel vibrasyon stabil. Rast makamı ile zindelik desteklenir."
    }

async def analyze_condition(req: AnalysisRequest):
    engine_logic = EVEYES360_Engine()
# BIA Analizi

    pa = core.analyze_bia(req.resistance, req.reactance)
    
    # Diyelim ki BIA ölçümü 4.2 çıktı (Düşük/Ödemli)

    # Terapi Karar Mekanizması
    if pa < 5.0 or req.facial_mood in ["anxious", "depressed"]:
        makam, scent = "Hicaz", "Gül Yağı"
        status = "Kritik (Ödem / Düşük Titreşim)"
        desc = "Hicaz makamı ve Gül yağı ile hücresel boşaltım ve sakinleşme önerilir."
    else:
        makam, scent = "Rast", "Sandal Ağacı"
        status = "Stabil (Hücresel Denge)"
        desc = "Rast makamı ve Sandal ağacı ile canlılık ve neşe desteklenir."
   
    therapy = core.therapy_db[res_key]
    selected_makam = therapy["makam"]
    scent = therapy["scent"]
    therapy = get_therapy_logic(pa, req.facial_mood)
    db = SessionLocal()
    try:
        new_log = TherapyLog(
            patient_name=req.patient_name,
            phase_angle=pa,
            suggested_makam=makam,
            scent=scent,
            status=status
        )
        db.add(new_log)
        db.commit()
    except Exception as e:
        db.rollback()
        return {"error": "Veritabanı hatası", "detail": str(e)}
    finally:
        db.close()
    # DB Kayıt
    db = SessionLocal()
    new_log = TherapyLog(patient_name=req.patient_name, phase_angle=pa, suggested_makam=makam)
    db.add(new_log)
    db.commit()
    return {
        "hospital": "EVEYES 360",
        "patient": req.patient_name,
        "analysis": {
            "phase_angle": pa,
            "condition_status": status
        },
        "therapy_plan": {
            "maqam": makam,
            "aroma": scent,
            "clinical_note": desc
        },
        "scientific_insight": engine_logic.get_scientific_article(req.lang)
    }


class AnalysisRequest(BaseModel):
    patient_name: str
    resistance: float
    reactance: float
    facial_mood: Optional[str] = "neutral"
    lang: str = "tr"
    
    # 1. AI Yüz Analizi Mantığı
    if req.facial_mood == "anxious":
        final_stress = 85
    elif req.facial_mood == "depressed":
        final_stress = 90

    # 2. Kullanıcı Beyanı (Manuel giriş varsa AI verisini günceller)
    # Not: Request modelinizde manual_mood_score olduğunu varsayıyoruz
    if hasattr(req, 'manual_mood_score') and req.manual_mood_score is not None:
        final_stress = req.manual_mood_score

    # 3. Biyosonoloji Hesaplaması (Faz Açısı)
    pa = round(math.degrees(math.atan(req.reactance / req.resistance)), 2)

    # 4. Karar Mekanizması (Selçuklu Tıbbı & Biyosonoloji)
    # Stres yüksekse veya Faz Açısı düşükse (hücresel ödem) Hicaz önerilir
    if final_stress > 75 or pa < 5.0:
        therapy = {
            "makam": "Hicaz",
            "scent": "Gül Yağı",
            "info": "Yüksek stres/ödem saptandı. Hicaz makamı ile dengeleme başlatıldı."
        }
    else:
        therapy = {
            "makam": "Rast",
            "scent": "Sandal Ağacı",
            "info": "Hücresel vibrasyon stabil. Rast makamı ile zindelik veriliyor."
        }

    # 5. Veritabanına Kaydet (Hata Kontrollü)
    try:
        new_session = TherapySession(
            patient_name=req.patient_name,
            ai_mood=req.facial_mood,
            phase_angle=pa,
            selected_makam=therapy["makam"],
            scent=therapy["scent"]
        )
        db.add(new_session)
        db.commit()
        db.refresh(new_session)
    except Exception as e:
        db.rollback()
        return {"status": "error", "message": f"DB Hatası: {str(e)}"}
    finally:
        db.close()

    # 6. EN SON RETURN (Tüm işlemler bittikten sonra)
    return {
        "status": "success",
        "data": {
            "patient": req.patient_name,
            "phase_angle": pa,
            "final_stress_score": final_stress,
            "therapy": therapy,
            "scientific_article": core.get_scientific_article(req.lang)
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



class EVEYES360_System:
    def __init__(self, hospital_name="EVEYES 360 Center"):# Eğer parantez içinde isim varsa onu sil, boş kalsın
        # 1. Önce ayarları dosyadan yüklemeyi dene    
        self.status_db = {
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
            },
            "kritik": {
            "tr": "Kritik (Ödem Saptandı)",
            "en": "Critical (Edema Detected)",
            "ar": "حرج (تم اكتشاف وذمة)",
            "ru": "Критический (Обнаружен отек)"},
            "normal": {
            "tr": "Normal (Hücresel Denge)",
            "en": "Normal (Cellular Balance)",
            "ar": "طبيعي (التوازن الخلوي)",
            "ru": "Нормальный (Клеточное равновесие)" }}
       
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
    
    def get_scientific_article(self, lang="tr"):
        file_name = {"tr":"Biyosonoloji, hücrelerin ses vibrasyonuna verdiği mekanik tepkileri inceler. Selçuklu döneminde Gevher Nesibe gibi şifahanelerde uygulanan müzikoterapi, bu hücresel akordu düzeltmeyi hedefler",
        "en": "Biosonology examines mechanical responses of cells to sound vibrations. Seljuk-era music therapy aims to restore this cellular harmony" }

        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_name = os.path.join(current_dir, f"makale_{lang}.txt")
    
        if os.path.exists(file_name):
             with open(file_name, "r", encoding="utf-8") as f:
                return f.read()
                
        else:
            # Eğer dosya yoksa kullanıcıyı bilgilendiren kısa bir özet dönelim
            if lang == "tr":
                return f"❌ HATA: {file_name} dosyası bulunamadı!"    
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

# --- 5. ÇALIŞTIRMA TALİMATI ---
if __name__ == "__main__":
    import uvicorn
    print("EVEYES 360 Sistemi Başlatılıyor...")
    # Bu satır API'yi 8000 portunda ayağa kaldırır
    uvicorn.run(app, host="127.0.0.1", port=8000)
