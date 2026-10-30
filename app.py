import streamlit as st
import json

# Web Sayfası Başlığı ve Tasarımı
st.set_page_config(page_title="Tüm İlanlar Tek Çatıda", page_icon="💼", layout="centered")

st.title("💼 Akıllı İş İlanı Agregatörü")
st.write("Kariyer.net, LinkedIn, Indeed ve Şirketlerin kendi kariyer sayfalarındaki **güncel** ilanları tek bir yerden arayın.")

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
if st.button("🔍 Güncel İlanları Bul", use_container_width=True):
    if not job_title:
        st.warning("Lütfen bir iş unvanı girin!")
    else:
        st.info(f"'{job_title}' pozisyonu için {location} bölgesinde güncel ilanlar taranıyor...")
        
        # ARKA PLAN AI MANTIĞI:
        # Burada seçilen title ve location bilgisi, arka planda Gemini API / Google Search API'ye gönderilir.
        # Örnek Arama Promptu: 
        # "Son 7 günde yayınlanmış '{job_title}' ilanlarını LinkedIn, Kariyer.net ve şirket kariyer sitelerinden bul, bana JSON getir."
        
        # MOCK/ÖRNEK GÖSTERİM (Sistemin Çalışma Mantığını Ekranda Görmek İçin)
        st.success("Taramalar tamamlandı! Bulunan güncel ilanlar:")
        
        # Örnek İlan Kartı 1
        with st.container():
            st.markdown(f"### 🏢 Huawei - {job_title}")
            st.write(f"**Lokasyon:** {location} | **Kaynak:** Huawei Kariyer Sayfası (ATS)")
            st.markdown("[İlana Git ve Başvur](https://huawei.com/careers)")
            st.divider()

        # Örnek İlan Kartı 2
        with st.container():
            st.markdown(f"### 🏢 Trendyol - Senior / Mid {job_title}")
            st.write(f"**Lokasyon:** {location} | **Kaynak:** LinkedIn")
            st.markdown("[İlana Git ve Başvur](https://linkedin.com)")
            st.divider()
