import streamlit as st
import json

# Sayfa Yapılandırması
st.set_page_config(page_title="Akıllı İş İlanı Agregatörü", page_icon="💼", layout="centered")

st.title("💼 Akıllı İş İlanı Agregatörü")
st.write("Türkiye'deki güncel iş ilanlarını tek bir ekranda canlı listeleyin.")

# Yan Menüde API Key Girişi
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
        with st.spinner(f"'{job_title}' pozisyonu için {location} bölgesindeki güncel ilanlar taranıyor..."):
            try:
                import google.generativeai as genai
                
                # Gemini yapılandırması
                genai.configure(api_key=api_key)
                
                # Google Search grounding destekli model (Canlı arama için en güncel yöntem)
                model = genai.GenerativeModel(
                    model_name='gemini-1.5-flash',
                    tools='default_api' # Web araması ve araç kullanımı için
                )
                
                prompt = f"""
                Türkiye'deki kariyer platformlarında (LinkedIn, Kariyer.net, İŞKUR ve şirket kariyer sayfalarında) 
                '{job_title}' pozisyonu için '{location}' bölgesindeki **GÜNCEL AKTİF İLANLARI** ara.
                
                Bana gerçek ve aktif ilanlar bul ve kesinlikle sadece aşağıdaki JSON formatında yanıt ver. 
                Hiçbir ek açıklama, giriş veya çıkış metni yazma. Sadece saf JSON dizisi döndür:
                
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
                
                response = model.generate_content(prompt)
                raw_text = response.text
                
                # JSON temizliği
                clean_json = raw_text.replace("```json", "").replace("```", "").strip()
                jobs = json.loads(clean_json)
                
                st.success(f"{len(jobs)} adet güncel ilan başarıyla bulundu!")
                
                # İlanları Kart Şeklinde Ekrana Basma
                for job in jobs:
                    with st.container():
                        st.markdown(f"### 🏢 {job.get('sirket')} - {job.get('baslik')}")
                        st.write(f"📍 **Lokasyon:** {job.get('lokasyon')} | 🌐 **Kaynak:** {job.get('kaynak')}")
                        st.markdown(f"👉 [**İlana Git ve Başvur**]({job.get('link')})")
                        st.divider()
                        
            except Exception as e:
                st.error(f"Bir hata oluştu: {str(e)}")
                st.info("Lütfen API anahtarınızın doğru olduğundan emin olun ve tekrar deneyin.")
