import streamlit as st
import io
from belgeolusturucu import build_document

# --- ÇOKLU DİL DESTEĞİ İÇİN METİNLER (LOCALIZATION) ---
UI_TEXT = {
    "tr": {
        "page_title": "GOST Word Oluşturucu",
        "title": "📄 GOST Standartlarında Word Belgesi Oluşturucu",
        "description": "Rusya GOST R 7.0.97-2016 standartlarına uygun Word (.docx) belgelerini saniyeler içinde oluşturun.",
        "settings": "⚙️ Belge Ayarları",
        "archive_mode": "Arşiv Modu (Sol Kenar: 3cm)",
        "archive_help": "10 yıldan uzun süre saklanacak belgeler için seçin.",
        "font_size": "Yazı Tipi Boyutu (Punto)",
        "line_spacing": "Satır Aralığı",
        "how_it_works": "**Nasıl Çalışır?**\nProgram yazdığınız metni otomatik analiz eder. Normal paragraflardan listelere geçerken özel bir ayar yapmanıza gerek yoktur, sadece alt satıra geçip `1.` yazmanız yeterlidir.",
        "content_header": "### ✍️ Belge İçeriği",
        "content_desc": "Metninizi aşağıya yazın. Paragraf yazarken aniden listeye veya başlığa geçmek isterseniz işinizi kolaylaştırmak için aşağıdaki **Hızlı Ekleme Butonlarını** kullanabilirsiniz.",
        "btn_heading": "📌 Ana Başlık",
        "btn_numbered": "1️⃣ Numaralı Liste",
        "btn_sublist": "🔢 Alt Liste",
        "btn_bullet": "⏺️ Madde İmi",
        "btn_title_page": "📑 Kapak Sayfası",
        "snippet_heading": "# Yeni Başlık\n",
        "snippet_numbered": "1. Birinci madde\n2. İkinci madde\n",
        "snippet_sublist": "1.1 Birinci alt madde\n1.2 İkinci alt madde\n",
        "snippet_bullet": "- Birinci madde\n- İkinci madde\n",
        "snippet_title_page": "--- BAŞLIK ---\nKAPAK SAYFASI METNİ\n--- BAŞLIK ---\n",
        "placeholder": "Metninizi buraya yazmaya başlayın veya başka bir yerden kopyalayıp yapıştırın...",
        "btn_generate": "🚀 Word Belgesini Oluştur",
        "warn_empty": "Lütfen önce bir metin girin!",
        "spinner": "GOST standartlarında belgeniz hazırlanıyor...",
        "success": "🎉 Belgeniz başarıyla oluşturuldu!",
        "btn_download": "📥 Word Dosyasını İndir (.docx)",
        "download_name": "GOST_Formatli_Belge.docx",
        "err_msg": "Bir hata oluştu: {}"
    },
    "en": {
        "page_title": "GOST Word Generator",
        "title": "📄 GOST-Compliant Word Document Generator",
        "description": "Generate Word (.docx) documents compliant with Russian GOST R 7.0.97-2016 standards in seconds.",
        "settings": "⚙️ Document Settings",
        "archive_mode": "Archive Mode (Left: 3cm)",
        "archive_help": "Select for documents to be kept for more than 10 years.",
        "font_size": "Font Size (pt)",
        "line_spacing": "Line Spacing",
        "how_it_works": "**How it works?**\nThe program automatically analyzes your text. No special settings are needed when switching from paragraphs to lists, just go to the next line and type `1.`.",
        "content_header": "### ✍️ Document Content",
        "content_desc": "Write your text below. You can use the **Quick Insert Buttons** to easily insert lists or headings while typing.",
        "btn_heading": "📌 Main Heading",
        "btn_numbered": "1️⃣ Numbered List",
        "btn_sublist": "🔢 Sub List",
        "btn_bullet": "⏺️ Bullet Point",
        "btn_title_page": "📑 Title Page",
        "snippet_heading": "# New Heading\n",
        "snippet_numbered": "1. First item\n2. Second item\n",
        "snippet_sublist": "1.1 First sub-item\n1.2 Second sub-item\n",
        "snippet_bullet": "- First item\n- Second item\n",
        "snippet_title_page": "--- TITLE ---\nTITLE PAGE TEXT\n--- TITLE ---\n",
        "placeholder": "Start typing your text here or paste from somewhere else...",
        "btn_generate": "🚀 Generate Word Document",
        "warn_empty": "Please enter some text first!",
        "spinner": "Your document is being prepared to GOST standards...",
        "success": "🎉 Document generated successfully!",
        "btn_download": "📥 Download Word File (.docx)",
        "download_name": "GOST_Formatted_Document.docx",
        "err_msg": "An error occurred: {}"
    },
    "ru": {
        "page_title": "GOST Генератор Word",
        "title": "📄 Генератор Word Документов (ГОСТ)",
        "description": "Создавайте документы Word (.docx) по стандартам ГОСТ Р 7.0.97-2016 за считанные секунды.",
        "settings": "⚙️ Настройки документа",
        "archive_mode": "Архивный режим (Поле: 3 см)",
        "archive_help": "Выберите для документов, хранящихся более 10 лет.",
        "font_size": "Размер шрифта (пт)",
        "line_spacing": "Межстрочный интервал",
        "how_it_works": "**Как это работает?**\nПрограмма автоматически анализирует текст. Для перехода к спискам просто перейдите на новую строку и введите `1.`.",
        "content_header": "### ✍️ Содержимое документа",
        "content_desc": "Введите ваш текст ниже. Используйте **Кнопки быстрой вставки**, чтобы легко добавлять списки или заголовки.",
        "btn_heading": "📌 Главный заголовок",
        "btn_numbered": "1️⃣ Нумерованный список",
        "btn_sublist": "🔢 Подсписок",
        "btn_bullet": "⏺️ Маркер",
        "btn_title_page": "📑 Титульный лист",
        "snippet_heading": "# Новый заголовок\n",
        "snippet_numbered": "1. Первый пункт\n2. Второй пункт\n",
        "snippet_sublist": "1.1 Первый подпункт\n1.2 Второй подпункт\n",
        "snippet_bullet": "- Первый пункт\n- Второй пункт\n",
        "snippet_title_page": "--- ТИТУЛ ---\nТЕКСТ ТИТУЛЬНОГО ЛИСТА\n--- ТИТУЛ ---\n",
        "placeholder": "Начните вводить текст здесь или вставьте скопированный текст...",
        "btn_generate": "🚀 Создать Word документ",
        "warn_empty": "Пожалуйста, сначала введите текст!",
        "spinner": "Ваш документ подготавливается по стандартам ГОСТ...",
        "success": "🎉 Документ успешно создан!",
        "btn_download": "📥 Скачать файл Word (.docx)",
        "download_name": "Документ_ГОСТ.docx",
        "err_msg": "Произошла ошибка: {}"
    }
}

# Session State for Language
if "lang" not in st.session_state:
    st.session_state.lang = "tr"

# Diller için haritalama
lang_options = {"Türkçe (TR)": "tr", "English (EN)": "en", "Русский (RU)": "ru"}
lang_reverse = {v: k for k, v in lang_options.items()}

# Sayfa Ayarları
st.set_page_config(
    page_title=UI_TEXT[st.session_state.lang]["page_title"],
    page_icon="📄",
    layout="wide"
)

# Session State for Text Input
if "doc_text" not in st.session_state:
    st.session_state.doc_text = ""

# Dil seçiciyi üste koyalım
lang_col1, lang_col2 = st.columns([8, 2])
with lang_col2:
    selected_lang = st.selectbox(
        "Language / Dil / Язык",
        options=list(lang_options.keys()),
        index=list(lang_options.keys()).index(lang_reverse[st.session_state.lang])
    )
    if lang_options[selected_lang] != st.session_state.lang:
        st.session_state.lang = lang_options[selected_lang]
        st.rerun()

# Aktif dili al
t = UI_TEXT[st.session_state.lang]
lang_code = st.session_state.lang

def add_snippet(snippet):
    if st.session_state.doc_text and not st.session_state.doc_text.endswith('\n'):
        st.session_state.doc_text += '\n\n'
    st.session_state.doc_text += snippet

st.title(t["title"])
st.markdown(t["description"])

# Yan Menü (Ayarlar)
with st.sidebar:
    st.header(t["settings"])
    archive_mode = st.checkbox(t["archive_mode"], value=False, help=t["archive_help"])
    font_size = st.selectbox(t["font_size"], options=[12, 14, 16], index=1)
    line_spacing = st.selectbox(t["line_spacing"], options=[1.0, 1.2, 1.5], index=2)
    st.markdown("---")
    st.markdown(t["how_it_works"])

st.markdown(t["content_header"])
st.markdown(t["content_desc"])

# --- HIZLI ARAÇ ÇUBUĞU (TOOLBAR) ---
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.button(t["btn_heading"], on_click=add_snippet, args=(t["snippet_heading"],), use_container_width=True)
with col2:
    st.button(t["btn_numbered"], on_click=add_snippet, args=(t["snippet_numbered"],), use_container_width=True)
with col3:
    st.button(t["btn_sublist"], on_click=add_snippet, args=(t["snippet_sublist"],), use_container_width=True)
with col4:
    st.button(t["btn_bullet"], on_click=add_snippet, args=(t["snippet_bullet"],), use_container_width=True)
with col5:
    st.button(t["btn_title_page"], on_click=add_snippet, args=(t["snippet_title_page"],), use_container_width=True)

# Ana Metin Girişi
text_input = st.text_area(
    "Metin Alanı",
    key="doc_text",
    height=400,
    label_visibility="collapsed",
    placeholder=t["placeholder"]
)

# Oluşturma Butonu
if st.button(t["btn_generate"], type="primary"):
    if not st.session_state.doc_text.strip():
        st.warning(t["warn_empty"])
    else:
        lines = st.session_state.doc_text.split('\n')
        
        with st.spinner(t["spinner"]):
            try:
                # Arka planda belgeyi oluştur - 'lang' parametresini kullanıcının seçtiği dil yapıyoruz
                doc = build_document(
                    lines=lines,
                    archive_mode=archive_mode,
                    font_size=font_size,
                    line_spacing=line_spacing,
                    lang=lang_code
                )
                
                # Dosyayı hafızada (RAM) tutarak indirmeye hazır hale getir
                bio = io.BytesIO()
                doc.save(bio)
                
                st.success(t["success"])
                
                # İndirme Butonu
                st.download_button(
                    label=t["btn_download"],
                    data=bio.getvalue(),
                    file_name=t["download_name"],
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )
            except Exception as e:
                st.error(t["err_msg"].format(e))
