# -*- coding: utf-8 -*-import streamlit as st
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
    page_icon="💜"
)

# --- 🎨 ÖZEL TASARIM (CSS) ---
def local_css():
    st.markdown("""
    <style>
    /* 1. ANA ARKA PLAN (Açık Toz Pembe) */
    .stApp {
        background-color: #ffe4e1; /* MistyRose */
    }

    /* 2. TÜM YAZILAR (Koyu Mor - Okunabilirlik İçin) */
    .stMarkdown, .stText, p, h1, h2, h3, h4, h5, h6, label, span, div, li {
        color: #4B0082 !important; /* Indigo / Koyu Mor */
        font-family: 'Helvetica Neue', sans-serif;
    }
    
    /* 3. BAŞLIKLAR İÇİN ÖZEL STİL */
    h1 {
        text-shadow: 1px 1px 0px #ffb6c1;
        font-weight: 800 !important;
    }

    /* 4. SLIDER (KAYDIRMA ÇUBUĞU) TASARIMI */
    /* Çubuğun kendisi */
    div.stSlider > div[data-baseweb="slider"] > div > div {
        background: linear-gradient(to right, #DA70D6, #800080);
    }
    /* Yuvarlak tutamaç */
    div.stSlider > div[data-baseweb="slider"] > div > div > div[role="slider"] {
        background-color: #800080;
        box-shadow: 0px 0px 5px rgba(0,0,0,0.2);
    }
    /* Slider üzerindeki sayılar */
    div[data-testid="stSliderTickBarMin"], div[data-testid="stSliderTickBarMax"] {
        color: #4B0082 !important;
    }

    /* 5. BUTON TASARIMI */
    div.stButton > button {
        background-color: #800080; /* Mor */
        color: white !important;
        border-radius: 15px;
        border: none;
        font-weight: bold;
        transition: transform 0.2s;
    }
    div.stButton > button:hover {
        background-color: #4B0082; /* Koyu Mor */
        color: white !important;
        transform: scale(1.05);
    }
    /* Form Submit Butonu (Analizi Başlat) */
    div.stButton > button[kind="primary"] {
        background-color: #C71585;
        font-size: 18px;
        padding: 10px 20px;
    }

    /* 6. SIDEBAR (YAN PANEL) */
    section[data-testid="stSidebar"] {
        background-color: #fff0f5; /* LavenderBlush */
        border-right: 2px solid #D8BFD8;
    }
    
    /* 7. EXPANDER (AÇILIR KUTULAR) */
    .streamlit-expanderHeader {
        background-color: #fff;
        border: 1px solid #D8BFD8;
        border-radius: 8px;
        color: #4B0082 !important;
    }
    
    /* 8. METRİK KUTULARI */
    div[data-testid="stMetricValue"] {
        color: #800080 !important;
    }
    div[data-testid="stMetricLabel"] {
        color: #4B0082 !important;
    }
    </style>
    """, unsafe_allow_html=True)

local_css()

# --- FONKSİYONLAR: STATE YÖNETİMİ (BUTONLAR İÇİN) ---
# Sorun buradaydı: Slider'lar "key" ile state'e bağlanmalı.
def randomize():
    for i in range(54):
        st.session_state[f"q_{i}"] = np.random.randint(0, 5)

def reset():
    for i in range(54):
        st.session_state[f"q_{i}"] = 0

# Başlangıç değerlerini ata (Eğer yoksa)
if "q_0" not in st.session_state:
    for i in range(54):
        st.session_state[f"q_{i}"] = 0

# --- ❤️ ANİMASYON ---
def load_lottieurl(url):
    try:
        r = requests.get(url)
        if r.status_code != 200: return None
        return r.json()
    except: return None

# Mor Kalp Animasyonu
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

# --- AĞIRLIKLAR VE GRUPLAR ---
W_FIXED = {'A': 0.1724, 'B': 0.1498, 'C': 0.1228, 'D': 0.1596, 'E': 0.1974, 'F': 0.0923, 'G': 0.1057}
GROUPS_IDX = {
    'A': list(range(9, 20)), 'B': list(range(4, 9)), 'C': list(range(20, 30)),
    'D': list(range(0, 4)),  'E': list(range(30, 41)), 'F': list(range(41, 47)),
    'G': list(range(47, 54))
}

# --- SIDEBAR (YAN PANEL) ---
with st.sidebar:
    st.markdown("### ⚙️ Kontrol Paneli")
    
    # Butonlar artık fonksiyonlara bağlı
    col1, col2 = st.columns(2)
    with col1: st.button("🎲 Rastgele", on_click=randomize, use_container_width=True)
    with col2: st.button("↺ Sıfırla", on_click=reset, use_container_width=True)
    
    st.markdown("---")
    st.info("Soruları **0 (Asla)** ile **4 (Her Zaman)** arasında puanlayın.")
    st.caption("Geliştiren: İlişki Mühendisliği Ekibi")

# --- ANA EKRAN ---
col_anim, col_title = st.columns([1, 4])

with col_anim:
    if lottie_heart: st_lottie(lottie_heart, height=120, key="heart")
    else: st.markdown("# 💜")

with col_title:
    st.title("İlişki Dinamikleri Analizi")
    st.markdown("**Aşkın Matematiği:** Kontrol Teorisi ile ilişkinizi test edin.")

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
    
    # Slider'lar artık doğrudan session_state["q_i"]'ye bağlı
    for title, start, end in sections:
        with st.expander(title, expanded=(start==0)):
            for i in range(start, end):
                st.slider(QUESTIONS[i], 0, 4, key=f"q_{i}")
    
    st.markdown("###")
    submitted = st.form_submit_button("🚀 ANALİZİ BAŞLAT", type="primary", use_container_width=True)

# --- ANALİZ MOTORU ---
if submitted:
    st.divider()
    
    try: rain(emoji="💜", font_size=20, falling_speed=5, animation_length=2)
    except: pass

    with st.spinner('Matematiksel model çalıştırılıyor...'):
        # Verileri State'ten Çek
        user_answers = np.array([st.session_state[f"q_{i}"] for i in range(54)])
        Qn = user_answers / 4.0
        
        # Skorlar
        scores = {key: np.mean(Qn[idxs]) for key, idxs in GROUPS_IDX.items()}
        An, Bn, Cn = scores['A'], scores['B'], scores['C']
        Dn, En, Fn, Gn = scores['D'], scores['E'], scores['F'], scores['G']
        
        # Matematiksel Hesaplamalar (MATLAB Mantığı)
        w = W_FIXED
        conf_raw = (w['E']*En + w['G']*Gn + w['F']*Fn) - (w['D']*Dn + w['A']*An + 0.5*w['B']*Bn)
        calm_raw = (w['D']*Dn + w['A']*An + 0.5*w['B']*Bn) - (w['E']*En + w['G']*Gn)
        
        scale = 0.4
        conflict_index = conf_raw / scale
        calm_index = calm_raw / scale
        
        zeta = 0.6 + 1.2 * calm_index
        wn = 2.3 + 2.3 * conflict_index
        
        if wn <= 0: wn = 1e-3
        if zeta <= 0: zeta = 1e-3
        
        # Transfer Fonksiyonu
        num_core = [wn**2]
        den_core = [1, 2*zeta*wn, wn**2]
        
        pA = 0.2 + (2.8)*(1 - An)
        pB = 0.2 + (2.3)*(1 - Bn)
        pG_mag = 0.05 + (1.45)*(Gn)
        
        is_unstable = False
        if conflict_index > 0.8:
            den_G = [1, -pG_mag] # RHP
            is_unstable = True
        else:
            den_G = [1, pG_mag]
            
        den_slow = np.convolve([1, pA], np.convolve([1, pB], den_G))
        
        # Zero
        if Cn > 0.6: 
            zC = 1.5/Cn
            num_zeros = np.convolve([1, -1/zC], [1, 1/(1.5/Dn)]) if Dn>0 else [1, -1/zC]
        else:
            num_zeros = [1, 1] 

        # Basitleştirilmiş TF oluşturma (Grafik için)
        num_final = np.convolve(num_core, num_zeros)
        den_final = np.convolve(den_core, den_slow)
        system = signal.TransferFunction(num_final, den_final)
        
        y_ss_raw = (w['A']*An + w['B']*Bn + w['C']*Cn + w['D']*Dn) - (w['E']*En + w['F']*Fn + w['G']*Gn)
        
        # DC Gain Scale
        dc = num_final[-1]/den_final[-1] if den_final[-1] != 0 else 1e9
        Kscale = y_ss_raw / dc if abs(dc) > 1e-9 else 1
        
        # --- GÖRSELLEŞTİRME ---
        st.subheader("📊 Analiz Sonuçları")
        
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Duygusal Denge (Zeta)", f"{zeta:.2f}")
        c2.metric("Tepki Hızı (Wn)", f"{wn:.2f}")
        c3.metric("Kararlılık", "KARARSIZ" if is_unstable else "KARARLI", 
                  delta="-Risk" if is_unstable else "+Güvenli")
        c4.metric("Mutluluk Puanı", f"{y_ss_raw:.2f}")
        
        if is_unstable:
            st.error("⚠️ **KRİTİK UYARI:** Gelecek kaygısı ve savunmacılık seviyesi eşiği aştı. Ayrılık riski yüksek.")

        tab1, tab2, tab3 = st.tabs(["📈 Zaman Cevabı", "📍 Kutup Haritası", "〰️ Bode Diyagramı"])
        
        with tab1:
            t = np.linspace(0, 20, 500)
            t, y = signal.step(system, T=t)
            y = y * Kscale
            
            fig, ax = plt.subplots(figsize=(10, 4))
            # Grafik renklerini de Mor/Pembe yapalım
            ax.plot(t, y, label='İlişki Seyri', linewidth=2, color='#800080')
            ax.axhline(y_ss_raw, color='#C71585', linestyle='--', label='Hedef Mutluluk')
            
            # Grafik Arka Planı
            ax.set_facecolor('#ffe4e1')
            fig.patch.set_facecolor('#ffe4e1')
            
            # Eksen yazıları mor olsun
            ax.tick_params(colors='#4B0082')
            ax.xaxis.label.set_color('#4B0082')
            ax.yaxis.label.set_color('#4B0082')
            ax.title.set_color('#4B0082')
            for spine in ax.spines.values(): spine.set_edgecolor('#4B0082')

            ax.grid(True, alpha=0.3, color='#800080')
            ax.legend(facecolor='#ffe4e1', edgecolor='#4B0082', labelcolor='#4B0082')
            st.pyplot(fig)
            
        with tab2:
            fig, ax = plt.subplots(figsize=(8, 6))
            poles = system.poles
            zeros = system.zeros
            ax.scatter(np.real(poles), np.imag(poles), marker='x', color='red', s=100, label='Kutuplar')
            ax.scatter(np.real(zeros), np.imag(zeros), marker='o', color='blue', s=100, label='Sıfırlar')
            ax.axvline(0, color='#4B0082', linestyle='--')
            ax.axhline(0, color='#4B0082', linestyle='--')
            
            if is_unstable:
                ax.axvspan(0, max(np.real(poles))+1, alpha=0.2, color='red', label='Kararsız Bölge')
            
            ax.set_facecolor('#ffe4e1')
            fig.patch.set_facecolor('#ffe4e1')
            ax.tick_params(colors='#4B0082')
            for spine in ax.spines.values(): spine.set_edgecolor('#4B0082')
            
            ax.grid(True, color='#800080', alpha=0.2)
            ax.legend(facecolor='#ffe4e1', edgecolor='#4B0082', labelcolor='#4B0082')
            st.pyplot(fig)
            
        with tab3:
            w, mag, phase = signal.bode(system)
            fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(8, 8))
            
            ax1.semilogx(w, mag, color='#800080')
            ax1.set_ylabel("Genlik (dB)", color='#4B0082')
            ax1.grid(True, color='#800080', alpha=0.2)
            ax1.set_facecolor('#ffe4e1')
            ax1.tick_params(colors='#4B0082')
            
            ax2.semilogx(w, phase, color='#800080')
            ax2.set_ylabel("Faz (derece)", color='#4B0082')
            ax2.set_xlabel("Frekans (rad/s)", color='#4B0082')
            ax2.grid(True, color='#800080', alpha=0.2)
            ax2.set_facecolor('#ffe4e1')
            ax2.tick_params(colors='#4B0082')
            
            fig.patch.set_facecolor('#ffe4e1')
            st.pyplot(fig)
