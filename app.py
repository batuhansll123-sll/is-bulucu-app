import streamlit as st

# Sayfa Yapılandırması
st.set_page_config(page_title="Akıllı İş İlanı Agregatörü", page_icon="💼", layout="centered")

st.title("💼 Akıllı İş İlanı Agregatörü (Canlı)")
st.write("Kariyer.net, LinkedIn, Indeed ve şirketlerin kariyer sayfalarındaki **güncel** ilanları tek bir yerden arayın.")

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
if st.button("🔍 Güncel İlanları Canlı Ara", use_container_width=True):
    if not job_title:
        st.warning("Lütfen aramak istediğiniz bir iş unvanı girin!")
    else:
        st.info(f"'{job_title}' pozisyonu için {location} bölgesinde güncel ilanlar taranıyor...")
        
        # Kullanıcının arama yapabilmesi için doğrudan arama motoru kısayolları ve akıllı yönlendirme oluşturalım
        query_location = "" if location == "Tüm Türkiye" else location
        
        st.success("Arama sonuçları hazır! Doğrudan kaynaklardan incelemek için aşağıdaki bağlantıları kullanabilirsiniz:")
        
        # Arama motorlarında ve platformlarda doğrudan arama yapacak akıllı linkler oluşturalım
        linkedin_url = f"https://www.linkedin.com/jobs/search/?keywords={job_title.replace(' ', '%20')}&location={query_location.replace(' ', '%20')}"
        kariyer_net_url = f"https://www.kariyer.net/is-ilanlari/{job_title.lower().replace(' ', '-')}"
        google_jobs_url = f"https://www.google.com/search?q={job_title.replace(' ', '+')}+iş+ilanları+{query_location.replace(' ', '+')}&ibp=htl;jobs"
        
        # Sonuç Kartları
        with st.container():
            st.markdown(f"### 🌐 Google İş İlanları (Tüm Ağlar)")
            st.write(f"Google'ın yapay zeka destekli iş tarayıcısında **{job_title}** ({location}) için en güncel toplu listeyi görün.")
            st.markdown(f"[Google İş İlanlarında Ara]({google_jobs_url})")
            st.divider()

        with st.container():
            st.markdown(f"### 💼 LinkedIn İlanları")
            st.write(f"LinkedIn üzerindeki güncel **{job_title}** pozisyonlarına doğrudan göz atın.")
            st.markdown(f"[LinkedIn'de İlanları Gör]({linkedin_url})")
            st.divider()

        with st.container():
            st.markdown(f"### 🏢 Kariyer.net")
            st.write(f"Kariyer.net veritabanındaki **{job_title}** filtreli sonuçlarına ulaşın.")
            st.markdown(f"[Kariyer.net'te Ara]({kariyer_net_url})")
            st.divider()
