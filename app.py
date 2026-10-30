import streamlit as st
import json
import requests

# Sayfa Yapılandırması
st.set_page_config(page_title="Akıllı İş İlanı Agregatörü", page_icon="💼", layout="centered")

st.title("💼 Akıllı İş İlanı Agregatörü")
st.write("Türkiye'deki güncel iş ilanlarını tek bir ekranda canlı listeleyin.")

# Yan Menüde API Key Girişi (Güvenli Kullanım İçin)
with st.sidebar:
    st.header("⚙️ Ayarlar")
    api_key = st.text_input("Gemini API Key Giriniz", type="password", help="aistudio.google.com adresinden ücretsiz alabilirsiniz.")

# Kullanıcı Girdi Alanları
col1, col2 = st.columns(2)

with col1:
    job_title = st.text_input("İş Unvanı (Title)", placeholder="Örn: E-Ticaret Uzman Yardımcısı")

with col2:
    location = st.selectbox(
        "Şehir / Lokasyon",
        ["Tüm Türkiye", "İstanbul", "Ankara", "İzmir", "Uzaktan (Remote)"]
    )

# Arama Butonu
if st.button("🔍 Güncel İlanları Canlı Listele", use_container_width=True):
    if not job_title:
        st.warning("Lütfen bir iş unvanı girin!")
    elif not api_key:
        st.error("Lütfen sol taraftaki menüden Gemini API Key'inizi girin!")
    else:
        st.info(f"'{job_title}' pozisyonu için {location} bölgesindeki canlı ilanlar taranıyor...")
        
        # Yapay zekaya canlı arama talimatı veriyoruz
        prompt = f"""
        Sen bir iş ilanı arama uzmanısın. Türkiye'deki kariyer sitelerinde (LinkedIn, Kariyer.net, İŞKUR ve şirket kariyer sayfalarında) 
        '{job_title}' pozisyonu için '{location}' bölgesindeki **GÜNCEL AKTİF İLANLARI** ara.
        
        Bana tam olarak 4 adet gerçek/aktif ilan bul ve aşağıdaki JSON formatında yanıt ver. Başka hiçbir açıklama yazma.
        
        [
          {{
            "sirket": "Şirket Adı",
            "baslik": "İlan Başlığı",
            "lokasyon": "Şehir / Uzaktan",
            "kaynak": "Platform / Şirket Sitesi",
            "link": "Doğrudan Başvuru veya İlan Linki"
          }}
        ]
        """
        
        try:
            # Google Gemini API Çağrısı (Google Search Destekli)
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
            headers = {'Content-Type': 'application/json'}
            payload = {
                "contents": [{"parts": [{"text": prompt}]}],
                "tools": [{"google_search": {}}] # Canlı web araması yapması için
            }
            
            response = requests.post(url, headers=headers, json=payload)
            result = response.json()
            
            # Gelen AI Yanıtını Ayrıştırma
            raw_text = result['candidates'][0]['content']['parts'][0]['text']
            # JSON kısmını temizleme
            clean_json = raw_text.replace("```json", "").replace("```", "").strip()
            jobs = json.loads(clean_json)
            
            st.success(f"{len(jobs)} adet güncel ilan bulundu!")
            
            # İlanları Kart Şeklinde Ekrana Basma
            for job in jobs:
                with st.container():
                    st.markdown(f"### 🏢 {job.get('sirket')} - {job.get('baslik')}")
                    st.write(f"📍 **Lokasyon:** {job.get('lokasyon')} | 🌐 **Kaynak:** {job.get('kaynak')}")
                    st.markdown(f"👉 [**İlana Git ve Başvur**]({job.get('link')})")
                    st.divider()
                    
        except Exception as e:
            st.error("İlanlar çekilirken bir sorun oluştu. API anahtarınızı veya sorgunuzu kontrol edip tekrar deneyin.")
