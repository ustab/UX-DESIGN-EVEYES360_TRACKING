# UX-DESIGN-EVEYES360_TRACKING

🎁 The Handover

Uçtan uca bu işlemi bitirdiğimde şu dosyayı vereceğiz:

Frontend: Kullanıcı dostu, 432Hz ses çıkışlı web/mobil uygulama.
AI Engine: Python ile yazılmış yüz ve frekans analiz motoru.
Database: SQL tabanlı seans kayıt ve raporlama sistemi.
Admin Panel: Hastane yönetiminin (Kayıtlı Hastane İsminle) hastaların genel iyileşme grafiklerini görebileceği bir dashboard.

🚀Yol Haritası:

5 ana katman bitirilecek

1. Frontend (The Interface)Arayüz: React veya Flutter (Çapraz platform için).Kamera Entegrasyonu: Kullanıcının yüzünü anlık olarak tarayan modül.Dil Desteği: Müşterinin istediği tüm dillerde (Türkçe, İngilizce ve diğerleri) dinamik yapı.
2. Backend - Python/FastAPI (The Brain)Logic: Az önce yazdığımız Python kodunun sunucuda (Heroku, AWS veya Azure) çalışır hali.AI Model: Yüz verisini alıp anxious veya depressed etiketini basacak hafif bir model (Örn: DeepFace kütüphanesi).Biosonology Parser: Gelen $432Hz$ gibi verileri analiz eden algoritma.
3. Database & Storage (The Memory)Kayıt: Kullanıcının seans geçmişini (Hangi gün hangi makamı dinledi, stres skoru neydi) tutan veritabanı.Hospital Branding: Hastane isminin (kaydettiğimiz şekilde) tüm reçetelerde ve raporlarda görünmesi.
4. Physical Integration (The Multisensory Output)Musiki Player: Makamları 432Hz kalitesinde çalan ses modülü.Aroma Trigger: (Simüle edilmiş veya gerçek) Koku makinesine sinyal gönderen API tetikleyicisi.
5.Databse
🗄️ EVEYES 360: Veritabanı Mimarisi (PostgreSQL/SQLAlchemy)
Müşterine "Verileriniz bu yapıda, güvenli ve ilişkisel olarak tutuluyor" diyerek sunabileceğin teknik şema şudur:

1. Kullanıcı Tablosu (Users Table)
Hastanın temel bilgilerini ve daha önce kaydettiğimiz Dil Seçeneklerini tutar.
user_id: Unique ID (Birincil Anahtar)
full_name: Hasta Adı
preferred_language: Kullanıcının seçtiği dil (TR, EN, vs.)
hospital_name: [Saved Hospital Name] (Marka bütünlüğü için)
2. Seans Verileri (Sessions Table)
Her terapi seansının "End-to-End" kaydıdır.
session_id: UUID
user_id: (User tablosuna bağlı)
ai_mood_result: Kamera analizinden gelen sonuç (anxious, depressed)
biosonology_frequency: Hücresel frekans verisi
applied_makam: Uygulanan Selçuklu Makamı
applied_aroma: Önerilen ve kullanılan koku (Leylak, Gül vb.)
pre_stress_score: Seans öncesi stres puanı
post_stress_score: Seans sonrası (kullanıcının girdiği veya AI'nın ölçtüğü) yeni puan
"""
