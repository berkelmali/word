import streamlit as st
import io
from belgeolusturucu import build_document

# --- ÇOKLU DİL DESTEĞİ İÇİN METİNLER (LOCALIZATION) ---
UI_TEXT = {
    "tr": {
        "page_title": "GOST Word Oluşturucu",
        "title": "📄 GOST Standartlarında Word Belgesi Oluşturucu",
        "description": "Rusya GOST R 7.0.97-2016 standartlarına uygun Word (.docx) belgelerini saniyeler içinde oluşturun. **Word programını hiç bilmenize gerek yok; düz yazı şeklinde yazın, gerisini programa bırakın!**",
        "settings": "⚙️ Belge Ayarları",
        "archive_mode": "Arşiv Modu (Sol Kenar: 3cm)",
        "archive_help": "Belgeniz fiziksel bir dosyaya takılacaksa veya 10 yıldan uzun süre saklanacaksa bu ayarı açın.",
        "font_size": "Yazı Tipi Boyutu (Punto)",
        "line_spacing": "Satır Aralığı",
        
        # Guide
        "guide_expander": "📖 Uygulama Nasıl Kullanılır? (Yeni Başlayanlar İçin Adım Adım Rehber)",
        "guide_text": """
        Bu araç, hiçbir karmaşık tasarım ayarı yapmadan **resmi kurallara tam uyumlu** Word belgeleri üretmenizi sağlar.

        **1. Normal Yazı (Paragraflar)**
        Sadece klavyeden yazınızı yazın. Ara vermek veya yeni paragrafa geçmek için klavyeden `Enter` tuşuna basıp bir alt satıra geçmeniz yeterlidir. Program, paragrafların ilk satırına otomatik olarak girinti (1.25 cm) ekleyecek ve metni sağa-sola yaslayacaktır.
        
        **2. Başlık Eklemek**
        Başlık yapmak istediğiniz cümlenin en başına `#` (diyez) işareti koyun ve bir boşluk bırakıp yazın. 
        - Ana başlık için: `# Başlık`
        - Alt başlık için: `## Başlık`
        Program onları otomatik olarak kalın fontlu, büyük ve ortalanmış yapacaktır.
        
        **3. Madde Madde Yazmak (Liste)**
        Bir satıra klavyeden `1.` yazıp bir boşluk bırakıp (Örn: `1. Elma`) cümlenizi yazarsanız program o kısmı otomatik olarak numaralı liste formatına sokar. Alt seviyeler için `1.1` kullanabilirsiniz.
        Nokta tasarımlı liste (Madde imi) yapmak için cümlenin başına sadece eksi işareti ve boşluk (`- `) koymanız yeterlidir. Harfler için `a) ` kullanabilirsiniz.

        **👉 Zorlanırsanız:** Metin kutusunun hemen üstündeki **Hızlı Ekleme Butonlarını** kullanarak bu işaretlerin otomatik eklenmesini sağlayabilirsiniz!
        """,

        "content_header": "### ✍️ Belge İçeriği",
        "content_desc": "Metninizi aşağıdaki geniş alana yazın veya yapıştırın. İşinizi kolaylaştırmak için butonlara tıklayarak hazır şablonlar ekleyebilirsiniz.",
        
        "btn_load_example": "💡 Örnek Şablon Yükle",
        "btn_clear_text": "🗑️ Metni Temizle",
        
        "group_headings": "📌 BAŞLIKLAR:",
        "btn_h1": "Ana Başlık (#)",
        "btn_h2": "Alt Başlık (##)",
        "btn_h3": "Alt Başlık (###)",
        
        "group_lists": "📋 LİSTELER:",
        "btn_num_1": "Liste (1.)",
        "btn_num_2": "İç Liste (1.1)",
        "btn_bullet": "Nokta (-)",
        "btn_letter": "Harf (a))",
        
        "group_special": "📑 SAYFA DÜZENİ:",
        "btn_title_page": "Kapak Sayfası Ekle",

        "example_text": "--- BAŞLIK ---\nKAPAK SAYFASI METNİ (ÜNİVERSİTE VEYA ŞİRKET ADI)\n\nPROJE VEYA RAPOR ADI\n\n\nAd Soyad\nŞehir - Yıl\n--- BAŞLIK ---\n\n# GİRİŞ\n\nBu belge, uygulamanın nasıl kullanılacağını göstermek için oluşturulmuştur. Normal yazılar otomatik olarak GOST kurallarına göre ilk satırdan içe doğru girintili olarak numaralandırılacaktır. Satır aralığı ve punto, sol menüdeki ayarlardan seçtiğiniz gibi olacaktır.\n\nWord programında bir saat uğraşarak yapacağınız formata, burada sadece sıradan bir metin yazarak saniyeler içinde ulaşabilirsiniz.\n\n## LİSTE ÖRNEKLERİ\n\nAşağıda numaralı bir liste örneği bulunmaktadır. Listeler de resmi formata otomatik uyarlanır:\n1. Numaralı listenin birinci maddesi.\n2. Numaralı listenin ikinci maddesi.\n   1.1 Bu bir iç içe geçmiş maddedir (Alt liste).\n   1.2 İkinci iç madde.\n   1.2.1 Daha da içe geçmiş bir madde.\n\n### MADDE İMLERİ\n\nHarfli liste örneği:\na) Harf ile başlayan birinci madde.\nb) Harf ile başlayan ikinci madde.\n\nMadde imleri (noktalı liste) de kullanabilirsiniz:\n- Birinci noktalı madde.\n- İkinci noktalı madde.\n\n# SONUÇ\n\nSiz sadece metninizi yazıp 'Word Belgesini Oluştur' butonuna tıklayın. Gerisini arka plan motoru mükemmel bir şekilde halledecektir.",

        "snippet_h1": "# Yeni Ana Başlık\n",
        "snippet_h2": "## Yeni Alt Başlık\n",
        "snippet_h3": "### Küçük Başlık\n",
        "snippet_num_1": "1. Birinci madde\n2. İkinci madde\n",
        "snippet_num_2": "1.1 Birinci alt madde\n1.2 İkinci alt madde\n",
        "snippet_bullet": "- Birinci madde\n- İkinci madde\n",
        "snippet_letter": "a) Birinci madde\nb) İkinci madde\n",
        "snippet_title": "--- BAŞLIK ---\nÖRN: MARMARA ÜNİVERSİTESİ\n\nDönem Ödevi\n\nAd Soyad\n2026\n--- BAŞLIK ---\n",

        "placeholder": "Metninizi buraya yazmaya başlayın. Başlık eklemek isterseniz yukarıdaki 'Ana Başlık' butonuna basabilirsiniz...",
        "btn_generate": "🚀 WORD BELGESİNİ OLUŞTUR (İndirmeye Hazırla)",
        "warn_empty": "Lütfen önce metin kutusuna bir şeyler yazın!",
        "spinner": "GOST standartlarında belgeniz hazırlanıyor, lütfen bekleyin...",
        "success": "🎉 Harika! Saniyeler içinde kusursuz belgeniz oluşturuldu.",
        "btn_download": "📥 TIKLA VE İNDİR (.docx)",
        "download_name": "GOST_Formatli_Belge.docx",
        "err_msg": "Bir hata oluştu: {}"
    },
    "en": {
        "page_title": "GOST Word Generator",
        "title": "📄 GOST-Compliant Word Document Generator",
        "description": "Generate Word (.docx) documents compliant with Russian GOST R 7.0.97-2016 standards in seconds. **Zero Word knowledge required; just write plain text, we do the rest!**",
        "settings": "⚙️ Document Settings",
        "archive_mode": "Archive Mode (Left: 3cm)",
        "archive_help": "Enable this if the document will be kept in a physical folder or archived for over 10 years.",
        "font_size": "Font Size (pt)",
        "line_spacing": "Line Spacing",
        
        "guide_expander": "📖 How to Use? (Step-by-Step Guide for Beginners)",
        "guide_text": """
        This tool allows you to create **officially compliant** Word documents without dealing with layout settings.

        **1. Plain Text (Paragraphs)**
        Simply type your content. Press `Enter` to create a new paragraph. The program will automatically indent the first line (1.25 cm) and justify the text.
        
        **2. Adding Headings**
        Type `#` at the beginning of a line to make it a heading.
        - Main heading: `# Heading`
        - Subheading: `## Heading`
        The tool will automatically make them bold, uppercase (for main headings), and centered.
        
        **3. Making Lists**
        To make a numbered list, type `1. ` (one, period, space) and write your sentence. Do the same for sub-items like `1.1 `.
        To make a bulleted list, start your sentence with a hyphen and a space (`- `). For lettered lists, use `a) `.

        **👉 Short on time?** Use the **Quick Insert Buttons** right above the text box to insert these elements automatically!
        """,

        "content_header": "### ✍️ Document Content",
        "content_desc": "Write or paste your text below. Click the buttons to easily insert pre-formatted templates.",
        
        "btn_load_example": "💡 Load Example Template",
        "btn_clear_text": "🗑️ Clear Text",
        
        "group_headings": "📌 HEADINGS:",
        "btn_h1": "Main Heading (#)",
        "btn_h2": "Subheading (##)",
        "btn_h3": "Subheading (###)",
        
        "group_lists": "📋 LISTS:",
        "btn_num_1": "Numbered (1.)",
        "btn_num_2": "Nested (1.1)",
        "btn_bullet": "Bullet (-)",
        "btn_letter": "Letter (a))",
        
        "group_special": "📑 LAYOUT:",
        "btn_title_page": "Insert Title Page",

        "example_text": "--- TITLE ---\nTITLE PAGE CONTENT (UNIVERSITY OR COMPANY NAME)\n\nPROJECT OR REPORT TITLE\n\n\nName Surname\nCity - Year\n--- TITLE ---\n\n# INTRODUCTION\n\nThis document was created to show you how to use the application. Normal paragraphs will be automatically indented on the first line according to GOST standards. Line spacing and font sizes will match your left sidebar preferences.\n\nWhat would take an hour to format in Word natively, takes just seconds here by writing plain text.\n\n## LIST EXAMPLES\n\nBelow is an example of a numbered list. Lists are automatically formatted correctly:\n1. First item of the numbered list.\n2. Second item of the numbered list.\n   1.1 This is a nested item.\n   1.2 Second nested item.\n   1.2.1 Even deeper nested item.\n\n### BULLET POINTS\n\nHere is a lettered list:\na) First item starting with a letter.\nb) Second item starting with a letter.\n\nYou can also use bullet points:\n- First bulleted item.\n- Second bulleted item.\n\n# CONCLUSION\n\nJust write your text and click 'Generate Word Document'. The backend engine will neatly construct your file.",

        "snippet_h1": "# New Main Heading\n",
        "snippet_h2": "## New Subheading\n",
        "snippet_h3": "### Small Heading\n",
        "snippet_num_1": "1. First item\n2. Second item\n",
        "snippet_num_2": "1.1 First nested item\n1.2 Second nested item\n",
        "snippet_bullet": "- First item\n- Second item\n",
        "snippet_letter": "a) First item\nb) Second item\n",
        "snippet_title": "--- TITLE ---\nEX: HARVARD UNIVERSITY\n\nTerm Paper\n\nJohn Doe\n2026\n--- TITLE ---\n",

        "placeholder": "Start typing your text here. If you want a heading, click the 'Main Heading' button above...",
        "btn_generate": "🚀 GENERATE WORD DOCUMENT",
        "warn_empty": "Please write something in the text box first!",
        "spinner": "Your document is being prepared according to GOST standards...",
        "success": "🎉 Awesome! Your flawless document was generated in seconds.",
        "btn_download": "📥 CLICK TO DOWNLOAD (.docx)",
        "download_name": "GOST_Formatted_Document.docx",
        "err_msg": "An error occurred: {}"
    },
    "ru": {
        "page_title": "GOST Генератор Word",
        "title": "📄 Генератор Word Документов (ГОСТ)",
        "description": "Создавайте документы Word (.docx) по стандартам ГОСТ Р 7.0.97-2016 за считанные секунды. **Знания Word не требуются; просто пишите обычный текст, остальное сделаем мы!**",
        "settings": "⚙️ Настройки документа",
        "archive_mode": "Архивный режим (Поле: 3 см)",
        "archive_help": "Включите это, если документ будет храниться в папке или архивироваться более 10 лет.",
        "font_size": "Размер шрифта (пт)",
        "line_spacing": "Межстрочный интервал",
        
        "guide_expander": "📖 Как использовать? (Пошаговое руководство для новичков)",
        "guide_text": """
        Этот инструмент позволяет создавать **официально соответствующие** стандарту ГОСТ документы Word без настройки в самом Word.

        **1. Обычный текст (Абзацы)**
        Просто введите свой текст. Нажмите `Enter`, чтобы создать новый абзац. Программа автоматически сделает отступ первой строки (1,25 см) и выровняет текст по ширине.
        
        **2. Добавление заголовков**
        Поставьте `#` в начале строки, чтобы сделать её заголовком.
        - Главный заголовок: `# Заголовок`
        - Подзаголовок: `## Заголовок`
        Инструмент автоматически сделает их жирными, заглавными (для главных заголовков) и выровненными по центру.
        
        **3. Создание списков**
        Чтобы создать нумерованный список, введите `1. ` (один, точка, пробел) и напишите свое предложение. Тем же способом для подпунктов, например `1.1 `.
        Для маркированного списка начните предложение с дефиса и пробела (`- `). Для буквенных списков используйте `а) ` или `a) `.

        **👉 Нет времени вникать?** Используйте **Кнопки быстрой вставки** прямо над текстовым полем, чтобы добавить эти элементы автоматически!
        """,

        "content_header": "### ✍️ Содержимое документа",
        "content_desc": "Введите или вставьте свой текст ниже. Нажмите кнопки, чтобы легко вставить готовые шаблоны.",
        
        "btn_load_example": "💡 Загрузить пример шаблона",
        "btn_clear_text": "🗑️ Очистить текст",
        
        "group_headings": "📌 ЗАГОЛОВКИ:",
        "btn_h1": "Главный (#)",
        "btn_h2": "Подзаголовок (##)",
        "btn_h3": "Подзаголовок (###)",
        
        "group_lists": "📋 СПИСКИ:",
        "btn_num_1": "Нумерованный (1.)",
        "btn_num_2": "Вложенный (1.1)",
        "btn_bullet": "Маркер (-)",
        "btn_letter": "Буквенный (a))",
        
        "group_special": "📑 МАКЕТ:",
        "btn_title_page": "Титульный лист",

        "example_text": "--- ТИТУЛ ---\nТЕКСТ ТИТУЛЬНОГО ЛИСТА (УНИВЕРСИТЕТ ИЛИ НАЗВАНИЕ КОМПАНИИ)\n\nНАЗВАНИЕ ПРОЕКТА ИЛИ ОТЧЕТА\n\n\nИмя Фамилия\nГород - Год\n--- ТИТУЛ ---\n\n# ВВЕДЕНИЕ\n\nЭтот документ был создан, чтобы показать вам, как использовать приложение. Нормальные абзацы будут автоматически с отступом в первой строке в соответствии со стандартами ГОСТ. Межстрочный интервал и размеры шрифтов будут соответствовать вашим настройкам на левой боковой панели.\n\nТо, что в Word потребовало бы часа ручной настройки, здесь занимает секунды.\n\n## ПРИМЕРЫ СПИСКОВ\n\nНиже приведен пример нумерованного списка:\n1. Первый пункт нумерованного списка.\n2. Второй пункт нумерованного списка.\n   1.1 Это вложенный пункт.\n   1.2 Второй вложенный пункт.\n   1.2.1 Еще более вложенный пункт.\n\n### МАРКИРОВАННЫЕ СПИСКИ\n\nВот буквенный список:\nа) Первый пункт, начинающийся с буквы.\nб) Второй пункт, начинающийся с буквы.\n\nВы также можете использовать маркированные списки:\n- Первый пункт с маркером.\n- Второй пункт с маркером.\n\n# ЗАКЛЮЧЕНИЕ\n\nПросто напишите ваш текст и нажмите 'Создать Word документ'.",

        "snippet_h1": "# Новый главный заголовок\n",
        "snippet_h2": "## Новый подзаголовок\n",
        "snippet_h3": "### Мелкий заголовок\n",
        "snippet_num_1": "1. Первый пункт\n2. Второй пункт\n",
        "snippet_num_2": "1.1 Первый вложенный пункт\n1.2 Второй вложенный пункт\n",
        "snippet_bullet": "- Первый пункт\n- Второй пункт\n",
        "snippet_letter": "а) Первый пункт\nб) Второй пункт\n",
        "snippet_title": "--- ТИТУЛ ---\nПРИМЕР: МГУ имени М.В.Ломоносова\n\nКурсовая работа\n\nИван Иванов\n2026\n--- ТИТУЛ ---\n",

        "placeholder": "Начните печатать ваш текст здесь. Если вы хотите добавить заголовок, нажмите кнопку 'Главный' выше...",
        "btn_generate": "🚀 СОЗДАТЬ ДОКУМЕНТ WORD",
        "warn_empty": "Пожалуйста, напишите что-нибудь в текстовом поле сначала!",
        "spinner": "Ваш документ подготавливается по стандартам ГОСТ...",
        "success": "🎉 Потрясающе! Ваш безупречный документ был создан за считанные секунды.",
        "btn_download": "📥 НАЖМИТЕ, ЧТОБЫ СКАЧАТЬ (.docx)",
        "download_name": "Документ_ГОСТ.docx",
        "err_msg": "Произошла ошибка: {}"
    }
}

# --- YARDIMCI FONKSİYONLAR ---
# Session State for Language
if "lang" not in st.session_state:
    st.session_state.lang = "tr"

# Session State for Text Input
if "doc_text" not in st.session_state:
    st.session_state.doc_text = ""

def add_snippet(snippet):
    if st.session_state.doc_text and not st.session_state.doc_text.endswith('\n'):
        st.session_state.doc_text += '\n\n'
    st.session_state.doc_text += snippet

def load_example():
    st.session_state.doc_text = UI_TEXT[st.session_state.lang]["example_text"]

def clear_text():
    st.session_state.doc_text = ""

# --- ARAYÜZ TASARIMI ---
# Sayfa Ayarları
st.set_page_config(
    page_title=UI_TEXT[st.session_state.lang]["page_title"],
    page_icon="📄",
    layout="wide"
)

# Diller için haritalama
lang_options = {"Türkçe (TR)": "tr", "English (EN)": "en", "Русский (RU)": "ru"}
lang_reverse = {v: k for k, v in lang_options.items()}

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

# Başlık ve Açıklama
st.title(t["title"])
st.markdown(t["description"])

# Kullanım Klavuzu Özeti (Expander)
with st.expander(t["guide_expander"]):
    st.markdown(t["guide_text"])

# Yan Menü (Ayarlar)
with st.sidebar:
    st.header(t["settings"])
    archive_mode = st.checkbox(t["archive_mode"], value=False, help=t["archive_help"])
    font_size = st.selectbox(t["font_size"], options=[12, 14, 16], index=1)
    line_spacing = st.selectbox(t["line_spacing"], options=[1.0, 1.2, 1.5], index=2)

st.markdown("---")
st.markdown(t["content_header"])
st.markdown(t["content_desc"])

# --- HIZLI ARAÇ ÇUBUĞU (TOOLBAR) ---
# Üst Kısım: Örnek Yükle / Temizle
top_c1, top_c2, top_c3 = st.columns([2, 2, 6])
with top_c1:
    st.button(t["btn_load_example"], on_click=load_example, use_container_width=True)
with top_c2:
    st.button(t["btn_clear_text"], on_click=clear_text, use_container_width=True)

st.write("") # Boşluk

# Alt Kısım: Şablon Butonları Kategorize Edilmiş
st.write(f"**{t['group_headings']}**")
h_c1, h_c2, h_c3, _ = st.columns([2, 2, 2, 4])
with h_c1: st.button(t["btn_h1"], on_click=add_snippet, args=(t["snippet_h1"],), use_container_width=True)
with h_c2: st.button(t["btn_h2"], on_click=add_snippet, args=(t["snippet_h2"],), use_container_width=True)
with h_c3: st.button(t["btn_h3"], on_click=add_snippet, args=(t["snippet_h3"],), use_container_width=True)

st.write(f"**{t['group_lists']}**")
l_c1, l_c2, l_c3, l_c4, _ = st.columns([2, 2, 2, 2, 2])
with l_c1: st.button(t["btn_num_1"], on_click=add_snippet, args=(t["snippet_num_1"],), use_container_width=True)
with l_c2: st.button(t["btn_num_2"], on_click=add_snippet, args=(t["snippet_num_2"],), use_container_width=True)
with l_c3: st.button(t["btn_bullet"], on_click=add_snippet, args=(t["snippet_bullet"],), use_container_width=True)
with l_c4: st.button(t["btn_letter"], on_click=add_snippet, args=(t["snippet_letter"],), use_container_width=True)

st.write(f"**{t['group_special']}**")
s_c1, _ = st.columns([2, 8])
with s_c1: st.button(t["btn_title_page"], on_click=add_snippet, args=(t["snippet_title"],), use_container_width=True)


# Ana Metin Girişi
text_input = st.text_area(
    "Metin Alanı",
    key="doc_text",
    height=500, # Büyütüldü
    label_visibility="collapsed",
    placeholder=t["placeholder"]
)

# Oluşturma Butonu
st.write("") # Boşluk
if st.button(t["btn_generate"], type="primary", use_container_width=True):
    if not st.session_state.doc_text.strip():
        st.warning(t["warn_empty"])
    else:
        lines = st.session_state.doc_text.split('\n')
        
        with st.spinner(t["spinner"]):
            try:
                doc = build_document(
                    lines=lines,
                    archive_mode=archive_mode,
                    font_size=font_size,
                    line_spacing=line_spacing,
                    lang=lang_code
                )
                
                bio = io.BytesIO()
                doc.save(bio)
                
                st.success(t["success"])
                
                # Bembeyaz geniş buton yerine Streamlit varsayılanı kullanıp görünür yapıyoruz
                st.download_button(
                    label=t["btn_download"],
                    data=bio.getvalue(),
                    file_name=t["download_name"],
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    use_container_width=True
                )
            except Exception as e:
                st.error(t["err_msg"].format(e))
