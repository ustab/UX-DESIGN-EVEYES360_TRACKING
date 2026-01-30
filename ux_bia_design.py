import math
import json
import os
import datetime
import uvicorn
from typing import Optional, List
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
        "seljuk_therapy": "العلاج بالموسيقى في العصر السلجوقي"
    }
}

current_lang = "tr" # Bu değer ileride arayüzden (frontend) gelecek

def get_translation(key, lang=None):
    """Sistem genelinde kullanılacak çeviri motoru."""
    target_lang = lang or current_lang
    return translations.get(target_lang, {}).get(key, key)
# Kullanım Örnekleri
print(f"Başlık: {get_translation('welcome')}")
print(f"Teknik Terim: {get_translation('phase_angle')}")

class TherapySession(Base):
    """Her terapi seansının veritabanındaki kalıcı kaydı."""
    __tablename__ = "therapy_sessions"
    id = Column(Integer, primary_key=True, index=True)
    patient_name = Column(String)
    ai_mood = Column(String)
    phase_angle = Column(Float)
    selected_makam = Column(String)
    scent = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

Base.metadata.create_all(bind=engine)   

# --- 2. ANALİZ MODELLERİ ---
class AnalysisRequest(BaseModel):
    patient_name: str
    resistance: float
    reactance: float
    facial_mood: str
    phase_angle: float
    manual_mood_score:Optional[float] = "neutral"
    lang: str = "tr"
  
    def EVEYES360_Rapor_Olustur(req):
    # 1. Stres Mantığı
        final_stress = 50 
        if req.facial_mood == "anxious":
            final_stress = 90
    
    # Manuel giriş varsa otomatiği ez
        if req.manual_mood_score is not None:
            final_stress = req.manual_mood_score
           # 2. Yazdırma Kısmı (Hatanın Çözüldüğü Yer)
            print("\n" + "="*40)
            print("--- NIZAMIYE HOSPITAL ANALİZ RAPORU ---")
            print(f"Hasta Durumu: {req.facial_mood}")
            print(f"Biyosonolojik Faz Açısı: {req.phase_angle}")
            print(f"Hesaplanan Stres Puanı: {final_stress}")
            print("="*40)
    # 3. Selçuklu ve Biyosonoloji Makale Bağlantısı
        if final_stress >= 80 or req.phase_angle < 5.0:
            print("\n[TERAPİ ÖNERİSİ]: Selçuklu Dönemi 'Rehavi' Makamı.")
            print("[AKADEMİK NOT]: Biyosonoloji; sesin hücre iyon kanallarına etkisini inceler.")
        else:
            print("\n[TERAPİ ÖNERİSİ]: 'Rast' Makamı ile dengeleme.")


    # --- ÇALIŞTIRMA KOMUTLARI ---
    # Örnek bir veri oluşturup fonksiyonu çağırıyoruz


if __name__ == "__main__":
    # Pydantic artık bu 5 veriyi de zorunlu kılıyor:
    test_verisi = AnalysisRequest(
        patient_name="Ahmet Yılmaz",  # Eksik olan 1
        resistance=500.0,            # Eksik olan 2
        reactance=30.0,              # Eksik olan 3
        facial_mood="anxious", 
        phase_angle=4.8
    )
    EVEYES360_Rapor_Olustur(test_verisi)

    def calculate_final_stress(self):
        # Varsayılan değer
        final_stress = 50 

        # 1. Yüz ifadesine göre kontrol
        if self.facial_mood == "anxious":
           final_stress = 85

        elif self.facial_mood == "depressed":
           final_stress = 90
        
        # 2. Manuel müdahale kontrolü (Senin eklemek istediğin kısım)
        elif self.manual_mood_score is not None:
            final_stress = self.manual_mood_score
            
        return final_stress
        # SONUÇ VE TERAPİ PLANI
    print(f"\n--- NIZAMIYE HOSPITAL ANALİZ RAPORU ---")
    print(f"Biyosonolojik Faz Açısı: {self.phase_angle}")
    print(f"Hesaplanan Stres Puanı: {final_stress}")

    # Selçuklu ve Biyosonoloji Entegrasyonu
    if final_stress >= 80 or req.phase_angle < 5.0:
        print("\n[TERAPİ ÖNERİSİ]: Selçuklu Dönemi 'Rehavi' Makamı.")
        print("[BİLİMSEL DAYANAK]: Biyosonoloji verileri hücre içi düşük enerji tespit etti.")
        print("[AKADEMİK NOT]: Ses frekansları hücre zarındaki iyon kanallarını stimüle eder.")
    else:
        print("\n[TERAPİ ÖNERİSİ]: 'Rast' Makamı ile genel dengeleme.")
class EVEYES360_Engine:
    """Biyosonoloji ve Selçuklu Tıbbı kararlarını veren beyin."""
    def __init__(self, hospital_name="EVEYES 360 Center"):
        self.hospital_name = hospital_name
        self.settings_file = 'settings.json'
        self._load_hospital_settings()

    def _load_hospital_settings(self):
        """Hastanenin adını ve doktor bilgilerini kalıcı hafızadan yükler."""
        if os.path.exists(self.settings_file):
            with open(self.settings_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.hospital_name = data.get("hospital", self.hospital_name)

        else:
            # Eğer dosya yoksa varsayılan bir isim ata
            self.hospital_name = "EVEYES 360 Merkezi"
            self.doctor = "Bilinmiyor"
            self.contact = "-"

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
    def analyze_stress(self, req):
        """
        Sistemden gelen otomatik stres verisini kontrol eder, 
        eğer manuel bir giriş varsa onu önceliklendirir.
        """
        # Varsayılan olarak sistem bir değer hesaplar (Örn: 50)
        final_stress = 50 
        if hasattr(req, 'manual_mood_score') and req.manual_mood_score is not None:
            # Eğer uzman/doktor müdahale ettiyse o puanı kullan
            final_stress = req.manual_mood_score  
        return final_stress
    def calculate_phase_angle(self, resistance: float, reactance: float) -> float:
        """Hücresel vibrasyonu ölçen Faz Açısı formülü: arctan(Xc/R) * (180/pi)"""
        # Formül: $$ \phi = \arctan\left(\frac{X_c}{R}\right) \times \frac{180}{\pi} $$
        pa = math.degrees(math.atan(reactance / resistance))
        return round(pa, 2)      
    def get_scientific_article(self, lang="tr"):
        articles = {
            "tr": "Hücreler ses dalgalarına mekanik tepkiler verir. Selçuklu dönemi şifahanelerinde (Gevher Nesibe gibi) "
                  "uygulanan müzikoterapi, bu biyolojik akordu (Faz Açısı dengesini) düzeltmeyi hedefler.",
            "en": "Cells respond mechanically to sound waves. Seljuk-era music therapy (e.g., Gevher Nesibe) "
                  "aims to restore this biological harmony and balance the Phase Angle.",
            "ar": "تستجيب الخلايا ميكانيكيًا للموجات الصوتية. يهدف العلاج بالموسيقى في العصر السلجوقي إلى استعادة هذا التناغم البيولوجي.",
            "ru": "Клетки механически реагируют на звуковые волны. Сельджукская музыкотерапия направлена на восстановление этой гармонии."
        }
        return articles.get(lang, articles["en"])
    
    def get_therapy_logic(self, pa: float, mood: str, stress_score: Optional[int] = None):
        """Selçuklu tıbbına göre makam ve koku eşleştirmesi yapar."""
        final_stress = stress_score if stress_score else (85 if mood in ["anxious", "sad"] else 50)
        
        # Kritik eşik: Faz açısı 5.0'ın altı hücresel ödem/zayıflık işaretidir.
        if pa < 5.0 or final_stress > 75:
            return {
                "makam": "Hicaz",
                "scent": "Gül Yağı",
                "status": "Kritik (Hücresel Ödem/Yüksek Stres)",
                "note": "Hicaz makamı ödem atar ve boşaltım sistemini dengeler."
            }
        else:
            return {
                "makam": "Rast",
                "scent": "Sandal Ağacı",
                "status": "Stabil (Hücresel Denge)",
                "note": "Rast makamı kemik/kas sağlığı ve zindelik sağlar."
            }


    def recete_olustur(self, faz_acisi, mood_notu=""):
        self.scientific_insight = {
            "tr": {
            "title": "BİLİMSEL DİPNOT: BİYOSONOLOJİ VE SELÇUKLU TIBBI",
            "content": "BURAYA KONTENT GELECEK Hücreler ses dalgalarına mekanik tepkiler verir. Biyosonoloji, hücresel vibrasyonun BIA değerleriyle (Faz Açısı) doğrudan ilişkili olduğunu savunur. Selçuklu döneminde Gevher Nesibe gibi şifahanelerde kullanılan müzikoterapi (Hicaz, Rast vb.) ve aromaterapi, bu biyolojik akordu düzeltmeyi amaçlar." },
            "en": {
            "title": "SCIENTIFIC INSIGHT: BIOSONOLOGY AND SELJUK MEDICINE",
            "content": "Cells respond mechanically to sound waves. Biosonology suggests that cellular vibration is directly linked to BIA values. Music therapy (Maqams) and aromatherapy used in Seljuk-era hospitals like Gevher Nesibe aim to restore this biological harmony."}}
        
        print(f"\n--- {self.hospital_name} REÇETE SİSTEMİ ---")
    

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

    def generate_report(self, patient, r, xc, lang="tr"):
        # ... rapor kodları ...
        return report
    
class EVEYES360_Biosonology:
    def __init__(self, hospital_name):
        self.hospital_name = hospital_name
        self.article = "Biyosonoloji ve Selçuklu tıbbı üzerine makale..."
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
class EVEYES360_Therapy:
    def __init__(self, hospital_name):
        self.hospital = hospital_name

    def recete_olustur(self, faz_acisi, sikayet, manual_mood_score=None):
        # 1. Manuel Mood Kontrolü (Kodun eksik olan kısmı burası)
        # Eğer dışarıdan bir puan (0-100 arası) girilirse onu kullan, yoksa 50 varsay
        final_stress = manual_mood_score if manual_mood_score is not None else 50

        print(f"\n--- {self.hospital} TEDAVİ PLANI ---")
        print(f"Biyosonolojik Veri (Faz Açısı): {faz_acisi}")
        print(f"Hasta Durumu: {sikayet}")
        
        # Selçuklu Dönemi ve Biyosonoloji Bağlantısı
        if faz_acisi < 5.0 or final_stress > 70:
            print("Tespit: Hücre içi enerji düşük ve stres seviyesi yüksek.")
            print("Öneri: Selçuklu tıbbına uygun 'Rehavi' makamı ile terapi.")
            print("Bilimsel Not: Ses frekansları hücre zarındaki iyon kanallarını aktive eder.")
        else:
            print("Durum: Stabil. 'Rast' makamı ile genel dengeleme önerilir.")

        secim = input("\n👉 Bilimsel dayanakları okumak ister misiniz? (E/H): ").upper()
        if secim == "E":
        # Burada 'my_app' yerine 'system_object' kullanıyoruz
            print(system_object.get_scientific_article(lang="tr"))
        # --- Test Edelim ---
        terapi_merkezi = EVEYES360_Therapy("NIZAMIYE HOSPITAL")

        # Örnek 1: Sadece şikayet ile (Manuel puan yok)
        terapi_merkezi.recete_olustur(4.8, "Hasta kendini çok gergin ve huzursuz hissediyor.")

        # Örnek 2: Manuel puan ile (Puan: 85 - Çok yüksek stres)
        terapi_merkezi.recete_olustur(5.2, "Halsizlik", manual_mood_score=85)

    SETTINGS_FILE = 'settings.json'
    def save_settings(hospital, doctor, contact):
        data = {"hospital": hospital, "doctor": doctor, "contact": contact}
        with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
                 json.dump(data, f, ensure_ascii=False, indent=4)
    def load_settings():
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
            
    def analyze_bia(self, resistance: float, reactance: float):
        import math
        pa = math.degrees(math.atan(reactance / resistance))
        return round(pa, 2)

class Patient:
    def __init__(self, tckn, name, reason):
        self.tckn = tckn
        self.name = name
        self.reason = reason

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
    
# --- 4. API VE UYGULAMA MERKEZİ (Başhekimlik) ---
app = FastAPI(title="EVEYES 360 Professional API")
engine_core = EVEYES360_Engine()
@app.post("/api/v1/analyze")  
async def analyze_condition(self: AnalysisRequest):
        db = SessionLocal()

    #  Terapi Karar Mekanizması
        if pa < 5.0 or final_stress > 75: # (#req.facial_mood in ["anxious", "depressed"]:)
            makam, scent = "Hicaz", "Gül Yağı"
            status = "Kritik (Ödem / Düşük Titreşim)"
            desc = "Yüksek stres/ödem saptandı.  Hicaz makamı ve Gül yağı ile hücresel boşaltım ve sakinleşme önerilir."
    
        else:
            therapy = {
        "hicaz_desc": {
        "tr": "Hicaz makamı ödem atar ve boşaltım sistemini dengeler.",
        "en": "Hicaz maqam reduces edema and balances the excretory system.",
        "ru": "Хиджаз макам уменьшает отеки и балансирует выделительную систему.",
        "ar": "مقام الحجاز يقلل من الوذمة ويوازن الجهاز الإخراجي." },
        "lavender_oil": {
        "tr": "Lavanta yağı kortizolü düşürerek hücresel ödemi azaltır.",
        "en": "Lavender oil reduces cellular edema by lowering cortisol.",
        "ar": "زيت اللافندر يقلل من الوذمة الخلوية عن طريق خفض الكورتيزول."}}
    
             # 4. ADIM: Veritabanına (SessionLocal üzerinden) kaydetme
        try:
            new_session = TherapySession(
            patient_name=req.patient_name,
            ai_mood=self.facial_mood,
            phase_angle=pa,
            selected_makam=therapy["makam"], # Burada kullanıyoruz
            scent=therapy["scent"]                 # Burada kullanıyoruz
        )
        
            db.add(new_session)
            db.commit() # Değişiklikleri kaydet
            db.refresh(new_session) # Kaydedilen verinin ID'sini geri al
         
            # 5. ADIM: Sonucu kullanıcıya (ekrana) gönder
            return {
                "status": "success",
                "data": {
                "patient": self.patient_name,
                "phase_angle": pa,
                "therapy": {
                    "makam": selected_makam,
                    "scent": scent,
                    "note": clinical_note
                },
                 "scientific_insight": engine_core.get_scientific_article(self.lang)
            }
        }

        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Sistem Hatası: {str(e)}")
        finally:
            db.close()

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

def get_description(data_key, lang="tr"):
         # İlgili anahtarın seçilen dildeki karşılığını döner, yoksa anahtarın kendisini döner
         try:
            return therapy_data[data_key].get(lang, therapy_data[data_key]["en"])
         except KeyError:
            return "Data not found."  
# --- 5. SİSTEMİ ÇALIŞTIRMA ---


def EVEYES360_Therapy(system_object):
    # 1. Raporu oluşturma ve yazdırma kısmı (Zaten yazmıştık)
        yeni_hasta = Patient("12345678901", "Ahmet Yılmaz", "Kalp Yetmezliği - Ödem Takibi")
        report = system_object.generate_report(yeni_hasta, 500, 30, lang="tr")
        print(f"--- {report['hospital']} ANALİZ RAPORU ---")
        print(f"Hasta: {report['patient']}")
        print(f"Teşhis: {report['status']}")
        print(f"Önerilen Tedavi: {report['therapy']}")
        print(f"Takip Nedeni: {patient_report['reason']}") # Bunu eklemeyi unutma
        print(f"BIA Faz Açısı: {patient_report['phase_angle']}°")
       
     # 2. BURAYA YAPIŞTIR: (Kullanıcıya makaleyi soran kısım)
        secim = input("\n👉 Bilimsel dayanakları ve akademik makaleyi okumak ister misiniz? (E/H): ").upper()
        if secim == "E":
            print("\n" + "="*70)
            print(system_object.get_scientific_article(lang="tr"))
            print("="*70)
        else:
            print("\nSağlıklı günler dileriz!")
        
       
    # 2. Kullanıcıya sor
        secim = input("\n👉 Bilimsel dayanakları ve akademik makaleyi okumak ister misiniz? (E/H): ").upper()
        if secim == "E":
            print("\n" + "="*70)
            print(f"\n{my_app.quick_info['tr']}")
            print("EVEYES 360 - AKADEMİK YAYIN")
            print("="*70)
            print(my_app.get_scientific_article(lang="tr"))
        else:
            print("\nSağlıklı günler dileriz!")
        my_app = EVEYES360_System()
        if __name__ == "__main__":
            ornek_veri = AnalysisRequest(
            facial_mood="anxious", 
            phase_angle=4.8, 
            manual_mood_score=None # Buraya rakam girersen otomatik veriyi ezer
    )
            print("✨ EVEYES 360 Sistemi Başlatılıyor...")
            print("🔗 API Dokümantasyonu için: http://127.0.0.1:8000/docs")
            uvicorn.run(app, host="127.0.0.1", port=8000)

    # Fonksiyonu bu veriyle çağırıyoruz
            EVEYES360_Analiz_Sistemi(ornek_veri)














# 1. ÖNCE SINIF (Bina Planı)
class AnalysisRequest(BaseModel):
    patient_name: str
    resistance: float
    reactance: float
    facial_mood: str
    phase_angle: float
    manual_mood_score: Optional[float] = None

# 2. SONRA FONKSİYON (İşçi - Bunu mutlaka 'if __name__' kısmından yukarıya koy)
def EVEYES360_Rapor_Olustur(req):
    final_stress = 50 
    if req.facial_mood == "anxious":
        final_stress = 90
    
    if req.manual_mood_score is not None:
        final_stress = req.manual_mood_score

    print("\n" + "="*40)
    print("--- NIZAMIYE HOSPITAL ANALİZ RAPORU ---")
    print(f"Hasta: {req.patient_name}")
    print(f"Biyosonolojik Faz Açısı: {req.phase_angle}")
    print(f"Stres Puanı: {final_stress}")
    print("="*40)
    
    # Selçuklu ve Biyosonoloji akademik notu
    if final_stress >= 80 or req.phase_angle < 5.0:
        print("\n[TERAPİ]: Selçuklu Rehavi Makamı önerilir.")
        print("[NOT]: Biyosonoloji; sesin hücre iyon kanallarına etkisini doğrular.")

# 3. EN SON ÇALIŞTIRMA (Tetikleyici - Her zaman en dipte olmalı)
if __name__ == "__main__":
    test_verisi = AnalysisRequest(
        patient_name="Ahmet Yılmaz",
        resistance=500.0,
        reactance=30.0,
        facial_mood="anxious", 
        phase_angle=4.8
    )
    # Python artık bu ismi yukarıda tanıdığı için hata vermeyecek
    EVEYES360_Rapor_Olustur(test_verisi)
