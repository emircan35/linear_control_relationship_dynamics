# -*- coding: utf-8 -*-
"""
Created on Wed Dec 10 20:48:14 2025

@author: user
"""
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import requests
from streamlit_lottie import st_lottie
from streamlit_extras.let_it_rain import rain

# --- SAYFA AYARLARI ---
st.set_page_config(
    page_title="İlişki Dinamikleri Analizi",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="❤️"
)

# --- 🎨 ÖZEL TASARIM (CSS) ---
# Burası siteni "Mühendis İşi"nden çıkarıp "Romantik ve Şık" hale getirir.
def local_css():
    st.markdown("""
    <style>
    /* Ana Arka Plan: Yumuşak Pembe Degrade */
    .stApp {
        background: linear-gradient(to bottom right, #fff0f5, #ffe4e1);
    }
    
    /* Başlık Stili */
    h1 {
        color: #C71585 !important;
        font-family: 'Helvetica Neue', sans-serif;
        text-shadow: 1px 1px 2px #ffb6c1;
    }
    
    /* Alt Başlıklar */
    h2, h3, h4 {
        color: #db7093 !important;
    }
    
    /* Slider (Kaydırma Çubuğu) Rengi */
    div.stSlider > div[data-baseweb="slider"] > div > div > div[role="slider"]{
        background-color: #C71585;
        box-shadow: rgb(14 38 74 / 20%) 0px 0px 0px 1px;
    }
    div.stSlider > div[data-baseweb="slider"] > div > div {
        background: linear-gradient(to right, #ffb6c1 0%, #C71585 100%);
    }

    /* Buton Tasarımı - Normal */
    div.stButton > button {
        background-color: #C71585;
        color: white;
        border-radius: 20px;
        border: none;
        padding: 10px 24px;
        font-weight: bold;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* Buton Tasarımı - Hover (Üzerine Gelince) */
    div.stButton > button:hover {
        background-color: #ff69b4;
        color: white;
        transform: translateY(-2px);
        box-shadow: 0 6px 8px rgba(0,0,0,0.15);
    }

    /* Expander (Açılır Kutular) */
    .streamlit-expanderHeader {
        background-color: #fff;
        border-radius: 10px;
        color: #C71585;
        font-weight: 600;
    }
    
    /* Sidebar (Yan Panel) */
    section[data-testid="stSidebar"] {
        background-color: #fff5f8;
        border-right: 1px solid #ffccd5;
    }
    
    /* Metrik Kutuları */
    div[data-testid="stMetricValue"] {
        color: #C71585;
    }
    </style>
    """, unsafe_allow_html=True)

local_css()

# --- ❤️ ANİMASYON FONKSİYONU ---
def load_lottieurl(url):
    try:
        r = requests.get(url)
        if r.status_code != 200: return None
        return r.json()
    except: return None

# Sayfa açılınca kalp yağsın
try:
    rain(emoji="❤️", font_size=18, falling_speed=4, animation_length=1)
except: pass

# Hareketli Kalp Animasyonu (Lottie)
lottie_heart = load_lottieurl("https://lottie.host/4b85776d-1763-4556-981f-368615024773/9Z6w5L8x5K.json")


# --- SORU LİSTESİ ---
QUESTIONS = [
    "1. Tartışmalarımız kötüye gittiğinde birimiz özür dilerse konu kapanır.",
    "2. Zor zamanlarda bile farklılıklarımızı görmezden gelebileceğimizi biliyorum.",
    "3. Gerektiğinde tartışmalarımızı baştan alıp düzeltebiliriz.",
    "4. Eşimle bir konuyu tartışırken ona ulaşmak (iletişim kurmak) eninde sonunda işe yarar.",
    "5. Eşimle geçirdiğim zaman benim için özeldir.",
    "6. Evde partner olarak baş başa vaktimiz olmaz. (Ters)",
    "7. Biz bir aileden ziyade, aynı evi paylaşan iki yabancı gibiyiz. (Ters)",
    "8. Tatillerimizi eşimle geçirmekten keyif alırım.",
    "9. Eşimle seyahat etmekten keyif alırım.",
    "10. Çoğu hedefimiz eşimle ortaktır.",
    "11. Geleceğe baktığımda, eşimle uyum içinde olduğumuzu görüyorum.",
    "12. Eşimle kişisel özgürlük konusunda benzer değerlere sahibiz.",
    "13. Eşimle benzer eğlence anlayışına sahibiz.",
    "14. İnsanlar (çocuklar, arkadaşlar vb.) hakkındaki hedeflerimizin çoğu aynıdır.",
    "15. Eşimle hayallerimiz benzer ve uyumludur.",
    "16. Sevginin ne olması gerektiği konusunda eşimle uyumluyuz.",
    "17. Eşimle hayatta mutlu olmakla ilgili aynı görüşleri paylaşırız.",
    "18. Evliliğin nasıl olması gerektiği konusunda benzer fikirlere sahibiz.",
    "19. Evlilikte rollerin nasıl olması gerektiği konusunda benzer fikirlere sahibiz.",
    "20. Güven konusunda benzer değerlere sahibiz.",
    "21. Eşimin tam olarak nelerden hoşlandığını bilirim.",
    "22. Eşim hasta olduğunda nasıl ilgilenilmek istediğini bilirim.",
    "23. Eşimin en sevdiği yemeği bilirim.",
    "24. Eşimin hayatında ne tür streslerle karşı karşıya olduğunu söyleyebilirim.",
    "25. Eşimin iç dünyası hakkında bilgi sahibiyim.",
    "26. Eşimin temel kaygılarını bilirim.",
    "27. Eşimin şu anki stres kaynaklarının neler olduğunu biliyorum.",
    "28. Eşimin umutlarını ve dileklerini biliyorum.",
    "29. Eşimi çok iyi tanırım.",
    "30. Eşimin arkadaşlarını ve sosyal ilişkilerini bilirim.",
    "31. Eşimle tartışırken kendimi agresif hissederim.",
    "32. Tartışırken genellikle 'sen hep böylesin' veya 'sen asla yapmazsın' gibi ifadeler kullanırım.",
    "33. Tartışmalarımız sırasında olumsuz ifadeler kullanabilirim.",
    "34. Tartışmalarımız sırasında kırıcı ifadeler kullanabilirim.",
    "35. Tartışırken hakaret edebilirim.",
    "36. Tartışırken aşağılayıcı olabilirim.",
    "37. Eşimle tartışmalarımız sakin geçmez.",
    "38. Eşimin konuları açma tarzından nefret ederim.",
    "39. Kavgalar genellikle aniden patlak verir.",
    "40. Daha ne olduğunu anlamadan kavgaya başlarız.",
    "41. Eşimle bir şey hakkında konuşurken sakinliğim aniden bozulur.",
    "42. Tartışırken sadece ortamdan çıkar giderim ve tek kelime etmem.",
    "43. Genellikle ortamı biraz sakinleştirmek için sessiz kalırım.",
    "44. Bazen evden bir süreliğine ayrılmanın iyi olacağını düşünürüm.",
    "45. Eşimle tartışmaktansa sessiz kalmayı tercih ederim.",
    "46. Tartışmada haklı olsam bile karşı tarafı üzmemek için susarım.",
    "47. Tartışırken öfkemi kontrol edememekten korktuğum için sessiz kalırım.",
    "48. Tartışmalarımızda kendimi haklı hissederim.",
    "49. Suçlandığım şeylerle hiçbir ilgim yok.",
    "50. Aslında suçlandığım konularda suçlu olan ben değilim.",
    "51. Evdeki sorunlarda hatalı olan ben değilim.",
    "52. Eşime yetersizliğini söylemekten çekinmem.",
    "53. Tartışırken eşime yetersiz olduğu konuları hatırlatırım.",
    "54. Eşime beceriksizliğini söylemekten korkmam."
]

# --- SABİT AĞIRLIKLAR (MATLAB Kodundan) ---
# Excel okumaya gerek yok, modelin matematiksel sabitleri:
W_FIXED = {
    'A': 0.1724, 'B': 0.1498, 'C': 0.1228,
    'D': 0.1596, 'E': 0.1974, 'F': 0.0923, 'G': 0.1057
}

# Grupların Soru İndeksleri
GROUPS_IDX = {
    'A': list(range(9, 20)), 'B': list(range(4, 9)), 'C': list(range(20, 30)),
    'D': list(range(0, 4)),  'E': list(range(30, 41)), 'F': list(range(41, 47)),
    'G': list(range(47, 54))
}

# --- SIDEBAR (YAN PANEL) ---
if 'answers' not in st.session_state:
    st.session_state.answers = np.zeros(54)

def randomize(): st.session_state.answers = np.random.randint(0, 5, 54)
def reset(): st.session_state.answers = np.zeros(54)

with st.sidebar:
    st.markdown("### ⚙️ Kontrol Paneli")
    col1, col2 = st.columns(2)
    with col1: st.button("🎲 Rastgele", on_click=randomize, use_container_width=True)
    with col2: st.button("↺ Sıfırla", on_click=reset, use_container_width=True)
    
    st.markdown("---")
    st.info("Soruları **0 (Asla)** ile **4 (Her Zaman)** arasında içtenlikle puanlayın.")
    st.caption("Geliştiren: İlişki Mühendisliği Ekibi")

# --- ANA EKRAN BAŞLIK ---
col_anim, col_title = st.columns([1, 4])

with col_anim:
    if lottie_heart:
        st_lottie(lottie_heart, height=120, key="heart")
    else:
        st.markdown("# ❤️")

with col_title:
    st.title("İlişki Dinamikleri Analizi")
    st.markdown("Kontrol Teorisi ile ilişkinizin **duygusal modelini** çıkarın.")

st.divider()

# --- ANKET FORMU ---
with st.form("survey_form"):
    st.markdown("#### 📝 Lütfen Soruları Cevaplayın")
    
    sections = [
        ("💕 1. Uyum ve Çatışma Çözümü", 0, 9),
        ("🎯 2. Ortak Hedefler ve Değerler", 9, 20),
        ("🧠 3. Partneri Tanıma ve İlgi", 20, 30),
        ("⚡ 4. Negatif Davranışlar ve Çatışma", 30, 41),
        ("🛡️ 5. Kaçınma ve Savunma", 41, 54)
    ]
    
    for title, start, end in sections:
        with st.expander(title, expanded=(start==0)):
            for i in range(start, end):
                st.session_state.answers[i] = st.slider(
                    QUESTIONS[i], 0, 4, int(st.session_state.answers[i]), key=f"q_{i}"
                )
    
    st.markdown("###")
    submitted = st.form_submit_button("🚀 ANALİZİ BAŞLAT", type="primary", use_container_width=True)

# --- ANALİZ MOTORU (MATLAB MANTIĞI) ---
if submitted:
    st.divider()
    
    # Tekrar yağmur efekti
    try: rain(emoji="❤️", font_size=20, falling_speed=5, animation_length=2)
    except: pass

    with st.spinner('Veriler 5. Derece Sistem Modeline işleniyor...'):
        # 1. Normalizasyon
        Qn = st.session_state.answers / 4.0
        
        # 2. Grup Skorları
        scores = {key: np.mean(Qn[idxs]) for key, idxs in GROUPS_IDX.items()}
        An, Bn, Cn = scores['A'], scores['B'], scores['C']
        Dn, En, Fn, Gn = scores['D'], scores['E'], scores['F'], scores['G']
        
        # 3. Parametreler (Hardcoded Weights)
        w = W_FIXED
        
        # MATLAB: conf_raw = (wE*En + ... ) - (...)
        conf_raw = (w['E']*En + w['G']*Gn + w['F']*Fn) - (w['D']*Dn + w['A']*An + 0.5*w['B']*Bn)
        calm_raw = (w['D']*Dn + w['A']*An + 0.5*w['B']*Bn) - (w['E']*En + w['G']*Gn)
        
        scale = 0.4
        conflict_index = conf_raw / scale
        calm_index = calm_raw / scale
        
        # Zeta ve Omega Mapping
        zeta = 0.6 + 1.2 * calm_index
        wn = 2.3 + 2.3 * conflict_index
        
        if wn <= 0: wn = 1e-3
        if zeta <= 0: zeta = 1e-3 # Matematiksel koruma
        
        # 4. Transfer Fonksiyonu (5. Derece)
        num_core = [wn**2]
        den_core = [1, 2*zeta*wn, wn**2]
        
        # Ek Reel Kutuplar
        pA = 0.2 + (3.0 - 0.2)*(1 - An)
        pB = 0.2 + (2.5 - 0.2)*(1 - Bn)
        pG_mag = 0.05 + (1.5 - 0.05)*(Gn)
        
        # Unstable Kontrolü
        conf_unstable_thresh = 0.8
        is_unstable = False
        
        if conflict_index > conf_unstable_thresh:
            den_G = [1, -pG_mag] # RHP
            is_unstable = True
        else:
            den_G = [1, pG_mag] # LHP
            
        den_slow = np.convolve([1, pA], np.convolve([1, pB], den_G))
        
        # Zero'lar (C ve D)
        zC_min = 0.5; zC_max = 3.0
        zD_min = 0.4; zD_max = 2.0
        
        zC_mag = zC_min + (zC_max - zC_min) * Cn
        zD_mag = zD_min + (zD_max - zD_min) * Dn
        
        # MATLAB'deki LHP Zero mantığı (Orijinal koda sadık kalındı)
        # s + 1/zC -> Kök -1/zC
        num_zeros = np.convolve([1, 1/zC_mag], [1, 1/zD_mag])
        
        num_final = np.convolve(num_core, num_zeros)
        den_final = np.convolve(den_core, den_slow)
        
        system = signal.TransferFunction(num_final, den_final)
        
        # Steady State (Y_ss)
        y_ss_raw = (w['A']*An + w['B']*Bn + w['C']*Cn + w['D']*Dn) - (w['E']*En + w['F']*Fn + w['G']*Gn)
        
        # DC Gain Scaling
        if den_final[-1] == 0: dc = 1e9
        else: dc = num_final[-1] / den_final[-1]
            
        if abs(dc) < 1e-9: Kscale = 1
        else: Kscale = y_ss_raw / dc
        
        # --- GÖRSELLEŞTİRME ---
        st.subheader("📊 Analiz Sonuçları")
        
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Duygusal Denge (Zeta)", f"{zeta:.2f}")
        c2.metric("Tepki Hızı (Wn)", f"{wn:.2f}")
        c3.metric("Kararlılık", "KARARSIZ" if is_unstable else "KARARLI", 
                  delta="-Risk" if is_unstable else "+Güvenli")
        c4.metric("Mutluluk Puanı", f"{y_ss_raw:.2f}")
        
        st.success("Analiz tamamlandı! Detaylı grafikler aşağıdadır.")
        
        if is_unstable:
            st.error("⚠️ **KRİTİK UYARI:** Gelecek kaygısı ve savunmacılık seviyesi eşiği aştı. Sistem matematiksel olarak kararsız (unstable).")

        tab1, tab2, tab3 = st.tabs(["📈 Zaman Cevabı", "📍 Kutup Haritası", "〰️ Bode Diyagramı"])
        
        with tab1:
            # Step Response (Ölçeklenmiş)
            t = np.linspace(0, 20, 500)
            t, y = signal.step(system, T=t)
            y = y * Kscale # Scaling burada uygulanıyor
            
            fig, ax = plt.subplots(figsize=(10, 4))
            ax.plot(t, y, label='İlişki Seyri', linewidth=2, color='#C71585')
            ax.axhline(y_ss_raw, color='gray', linestyle='--', label='Hedef Mutluluk')
            
            # Grafik Süslemeleri
            ax.set_facecolor('#fff0f5') 
            fig.patch.set_facecolor('#fff0f5')
            ax.grid(True, alpha=0.3)
            ax.legend()
            st.pyplot(fig)
            st.caption("İlişkide yaşanan bir olayın zaman içindeki sönümlenme grafiği.")
            
        with tab2:
            fig, ax = plt.subplots(figsize=(8, 6))
            poles = system.poles
            zeros = system.zeros
            ax.scatter(np.real(poles), np.imag(poles), marker='x', color='red', s=100, label='Kutuplar')
            ax.scatter(np.real(zeros), np.imag(zeros), marker='o', color='blue', s=100, label='Sıfırlar')
            ax.axvline(0, color='k', linestyle='--')
            ax.axhline(0, color='k', linestyle='--')
            
            if is_unstable:
                ax.axvspan(0, max(np.real(poles))+1, alpha=0.2, color='red', label='Kararsız Bölge')
            
            ax.set_facecolor('#fff0f5')
            fig.patch.set_facecolor('#fff0f5')
            ax.grid(True)
            ax.legend()
            st.pyplot(fig)
            
        with tab3:
            w, mag, phase = signal.bode(system)
            fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(8, 8))
            
            ax1.semilogx(w, mag, color='#C71585')
            ax1.set_title("Bode Diyagramı")
            ax1.set_ylabel("Genlik (dB)")
            ax1.grid(True)
            ax1.set_facecolor('#fff0f5')
            
            ax2.semilogx(w, phase, color='#C71585')
            ax2.set_ylabel("Faz (derece)")
            ax2.set_xlabel("Frekans (rad/s)")
            ax2.grid(True)
            ax2.set_facecolor('#fff0f5')
            
            fig.patch.set_facecolor('#fff0f5')
            st.pyplot(fig)
