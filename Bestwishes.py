import streamlit as st
import google.generativeai as genai
from fpdf import FPDF
import subprocess

def install_requirements():
    subprocess.run(["pip", "install", "-r", "requirements.txt"])

def run_streamlit_app():
    subprocess.run(["streamlit", "run", "Bestwishes.py"])

# API Anahtarı
GEMINI_ANAHTARI = "AIzaSyC5_ActnFp7AW2P2r05nZVwHEP7wa8JN5A"
genai.configure(api_key=GEMINI_ANAHTARI)
model = genai.GenerativeModel('gemini-1.5-flash')

@st.cache_data
def generate_bestwishes(contents, recipient, mood, age_group, sex, length):
    prompt = f"""
    Bir tebrik kartı oluşturucusu olarak, tek işin iyi dilek kartı yazmak. Şu bilgilere göre Türkçe bir tebrik kartı oluştur:
    İçerik: {contents}
    Kime Yazıyorsun: {recipient}
    Duygu: {mood}
    Yaş Grubu: {age_group}
    Cinsiyet: {sex}
    Uzunluk: {length} cümle

    Tebrik kartı özgün olmalı.
    Cümlelerin sonunda nokta kullanmayı unutma.
    Çoğul ekler kullanma bireysel dille yaz.
    Cinsiyet ve yaş grubuna uygun olmalı.
    İçten bir dilek olmalı.
    Cümleler arasında tutarlılık olmalı.
    """
    return model.generate_content(prompt).text

# Streamlit App Configuration
st.title('Tebrik Kartı Hazırlayıcı 🍾 ')
st.markdown("Bu uygulama ile sevdiklerinize özel tebrik mesajları oluşturabilirsiniz.")

# Story Elements Tab
tab1, tab2 = st.tabs(["Tebrik Kartı Mesajı Oluştur 💌", "Tebrik Kartını Kaydet ⏺️",])

with tab1:
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 💝️ Tebrik Kartı Konusu")
        contents = st.selectbox(
            "Tebrik kartı konusu seçin:",
                [
                "Yılbaşı Kutlaması",
                "Bayram Tebriği",
                "Yeni İş Tebriği",
                "Doğum Günü Kutlaması",
                "Mezuniyet Tebriği",
                "Yıldönümü Kutlaması",
                "Başarı Tebriği",
                "Düğün Tebriği",
                "Yeni Ev Tebriği",
                "Sağlık Tebriği",
                "Özür Dileme",
                "Teşekkür Mesajı",
                "Sevgililer Günü",
                "Anneler Günü",
                "Babalar Günü",
                "Öğretmenler Günü",
                "Kadınlar Günü"
                 ]
             )
        recipient = st.text_input("Kime yazıyorsunuz? (Örneğin: Arkadaşıma, İş Arkadaşım Ali'ye, Aileme, Sevgilime)")

    with col2:
        st.markdown("### ⚙️ Tebrik Kartı Seçenekleri")

        age_group = st.slider("Yaş ", 7, 100, 30)
        length = st.slider("Tebrik Kartı Uzunluğu (Cümle)", 2, 10, 4)

    st.markdown("### 📝 Tebrik Kartı Detayları")
    col3, col4 = st.columns(2)

    with col3:
        mood = st.selectbox(
            "Tebrik Kartı Duygusu 🤯",
            ["Neşeli", "Komik", "Duygusal", "Resmi", "Samimi", "Romantik"])

        sex = st.radio("Cinsiyet ", ["Kadın", "Erkek", "Cinsiyet Belirtmek İstemiyorum"])

    with col4:
        st.markdown("### 🎨 Görsel Tercihler")
        text_color = st.color_picker("Metin Rengi", "#1E1E1E")
        font_size = st.slider("Yazı Boyutu", 12, 24, 16)

    if st.button("🧚🏻‍♂️ Tebrik Kartı Oluştur"):
        with st.spinner("Sevdiklerinizi mutlu edecek tebrik kartı yaratılıyor..."):
            wishes = generate_bestwishes(contents, recipient, mood, sex, age_group, length)
            st.session_state['wishes'] = wishes
            st.markdown(f"<div style='color:{text_color};font-size:{font_size}px'>{wishes}</div>", unsafe_allow_html=True)

with tab2:
    st.markdown("### 💾 Tebrik Kartını Kaydet")
    bestwishes_title = st.text_input("Tebrik Kartı Başlığı")

    if st.button("📥 Tebrik Kartını İndir"):
        st.info("PDF indirme özelliği yakında eklenecek!")
