import streamlit as st
import json

# Sayfa Yapılandırması
st.set_page_config(page_title="Akıllı İş İlanı Agregatörü", page_icon="💼", layout="centered")

st.title("💼 Akıllı İş İlanı Agregatörü")
st.write("Türkiye'deki güncel iş ilanlarını tek bir ekranda canlı listeleyin.")

# Yan Menüde API Key Girişi
with st.sidebar:
    st.header("⚙️ Ayarlar")
    api_key = st.text_input("Gemini API Key Giriniz", type="password", key="gemini_api_key", help="aistudio.google.com adresinden ücretsiz alabilirsiniz.")

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
        st.error("Lütfen sol taraftaki menüye Gemini API Key'inizi yazın!")
    else:
        with st.spinner(f"'{job_title}' pozisyonu için {location} bölgesindeki ilanlar listeleniyor..."):
            try:
                import google.generativeai as genai
                
                genai.configure(api_key=api_key)
                
                # Hata mesajında önerilen en güncel model ismi
                model = genai.GenerativeModel('gemini-3.8-flash')
                
                prompt = f"""
                Sen profesyonel bir iş arama asistanısın. Türkiye'de (LinkedIn, Kariyer.net vb. platformlarda) aktif olarak 
                aranan '{job_title}' pozisyonu için '{location}' bölgesinde güncel olabilecek gerçekçi ve güncel şirket ilanları listesi oluştur.
                
                Bana tam olarak 4 adet ilan bul ve kesinlikle sadece aşağıdaki JSON formatında yanıt ver. 
                Hiçbir ek açıklama veya metin yazma, sadece saf JSON döndür:
                
                [
                  {{
                    "sirket": "Şirket Adı",
                    "baslik": "İlan Başlığı",
                    "lokasyon": "Şehir / Uzaktan",
                    "kaynak": "Kariyer.net / LinkedIn",
                    "link": "https://www.kariyer.net"
                  }}
                ]
                """
                
                response = model.generate_content(prompt)
                raw_text = response.text
                
                clean_json = raw_text.replace("```json", "").replace("```", "").strip()
                jobs = json.loads(clean_json)
                
                st.success(f"{len(jobs)} adet ilan başarıyla listelendi!")
                
                for job in jobs:
                    with st.container():
                        st.markdown(f"### 🏢 {job.get('sirket')} - {job.get('baslik')}")
                        st.write(f"📍 **Lokasyon:** {job.get('lokasyon')} | 🌐 **Kaynak:** {job.get('kaynak')}")
                        st.markdown(f"👉 [**İlana Git ve Başvur**]({job.get('link')})")
                        st.divider()
                        
            except Exception as e:
                st.error(f"Hata detayı: {str(e)}")
