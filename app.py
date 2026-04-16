import streamlit as st
import io
from belgeolusturucu import build_document

# ═══════════════════════════════════════════════════════════════
#  ÇOKLU DİL DESTEĞİ (LOCALIZATION) — TR / EN / RU
# ═══════════════════════════════════════════════════════════════

UI_TEXT = {
    # ───────────────────── TÜRKÇE ─────────────────────
    "tr": {
        "page_title": "GOST Word Oluşturucu",
        "title": "📄 GOST Standartlarında Word Belgesi Oluşturucu",
        "description": (
            "Rusya **GOST R 7.0.97-2016** standartlarına uygun Word (.docx) belgelerini "
            "saniyeler içinde oluşturun. Word programını hiç bilmenize gerek yok — "
            "düz yazı şeklinde yazın, gerisini programa bırakın!"
        ),

        # Sidebar — Ayarlar
        "settings": "⚙️ Belge Ayarları",
        "archive_mode": "📁 Arşiv Modu (Sol Kenar: 3 cm)",
        "archive_help": (
            "Belgeniz fiziksel bir dosyaya takılacaksa veya 10 yıldan uzun süre "
            "saklanacak arşiv belgesi ise bu ayarı açın. Sol kenar boşluğu 2 cm'den "
            "3 cm'ye çıkar (GOST zorunluluğu)."
        ),
        "font_size": "🔤 Yazı Tipi Boyutu (Punto)",
        "line_spacing": "↕️ Satır Aralığı",

        # Sidebar — Detaylı Kullanım Kılavuzu
        "sidebar_guide_title": "📖 Detaylı Kullanım Kılavuzu",
        "sidebar_guide": """
**Bu uygulama ne yapar?**
Yazdığınız düz metni, Rusya'nın resmi belge standardı olan GOST R 7.0.97-2016'ya tam uyumlu bir Word (.docx) dosyasına dönüştürür. Kenar boşlukları, yazı tipi, satır aralığı, girintiler ve sayfa numaraları otomatik olarak ayarlanır.

---

**🔵 Normal Paragraf Yazmak**
Metninizi olduğu gibi yazın. Her `Enter` tuşu yeni bir paragraf başlatır. Program otomatik olarak:
- İlk satıra **1,25 cm** girinti ekler
- Metni **iki yana yaslar** (justify)
- **Times New Roman** fontu uygular

---

**🟢 Başlık Eklemek**
Satırın başına `#` işareti koyun:

| Yazdığınız | Sonuç |
|---|---|
| `# Giriş` | **ANA BAŞLIK** (büyük, kalın, ortalı) |
| `## Alt Bölüm` | **Alt Başlık** (kalın, ortalı) |
| `### Küçük Başlık` | **Küçük Başlık** (kalın, ortalı) |

> ⚠️ GOST kuralı: Başlıkların sonuna **nokta konulmaz**.

---

**🟠 Numaralı Liste (Çok Düzeyli)**
Word'ün gerçek *Multilevel List* özelliğini kullanır. İndirdiğiniz dosyada Word'ün liste butonları aktif olacaktır!

| Yazdığınız | Seviye | Word'deki Görünüm |
|---|---|---|
| `1. Metin` | Seviye 1 | **1.** Metin |
| `1.1. Metin` | Seviye 2 | **1.1.** Metin |
| `1.1.1. Metin` | Seviye 3 | **1.1.1.** Metin |

> 💡 Numaraları siz yazarsınız ama Word dosyasında bunlar **otomatik numaralandırma** olarak kodlanır. Yani Word'de açıp Enter'a basarsanız bir sonraki numara otomatik gelir.

---

**🟣 Madde İmi (Bullet) ve Harf Listesi**

| Yazdığınız | Sonuç |
|---|---|
| `- Metin` | – Metin (GOST tire işareti) |
| `a) Metin` | a) Metin |
| `б) Текст` | б) Текст (Kiril harfleri de desteklenir) |

---

**🔴 Kapak Sayfası**
Metnin başına ve sonuna `--- BAŞLIK ---` etiketi koyun:
```
--- BAŞLIK ---
ÜNİVERSİTE ADI
Proje Adı
Ad Soyad
2026
--- BAŞLIK ---
```
Kapak sayfasında sayfa numarası otomatik olarak **gizlenir**.

---

**📐 Otomatik Uygulanan GOST Kuralları**
- 📄 A4 boyut (21×29,7 cm)
- 📏 Kenar boşlukları: Üst/Alt 2 cm, Sol 2 cm (arşiv: 3 cm), Sağ 1 cm
- 🔤 Times New Roman, siyah renk
- ↕️ Seçtiğiniz satır aralığı (1.0 / 1.2 / 1.5)
- 🔢 Sayfa numarası: Alt orta, Arap rakamları, noktasız
- ✏️ Paragraf girintisi: 1,25 cm (ilk satır)
""",

        # Ana sayfa — Rehber (expander)
        "guide_expander": "📖 Hızlı Başlangıç (Tıklayarak Açın)",
        "guide_text": """
**3 adımda belge oluşturun:**

1️⃣ **Sol menüden** punto, satır aralığı ve arşiv modunu seçin.

2️⃣ **Metin kutusuna** yazınızı yazın. Başlık için `#`, liste için `1.` kullanın.
   - Emin değilseniz **💡 Örnek Şablon Yükle** butonuna basarak hazır bir örnek yükleyin.

3️⃣ **🚀 Oluştur** butonuna basın, ardından **📥 İndir** ile dosyanızı alın.

> 💡 **İpucu:** Metin kutusunun üstündeki renkli butonları kullanarak başlık, liste ve kapak sayfası şablonlarını tek tıkla ekleyebilirsiniz!
""",

        # İçerik alanı
        "content_header": "### ✍️ Belge İçeriği",
        "content_desc": (
            "Metninizi aşağıdaki geniş alana yazın veya yapıştırın. "
            "Butonlara tıklayarak hazır şablonlar ekleyebilirsiniz."
        ),

        # Üst butonlar
        "btn_load_example": "💡 Örnek Şablon Yükle",
        "btn_clear_text": "🗑️ Metni Temizle",

        # Başlık butonları
        "group_headings": "📌 BAŞLIKLAR:",
        "btn_h1": "# Ana Başlık",
        "btn_h2": "## Alt Başlık",
        "btn_h3": "### Küçük Başlık",

        # Liste butonları
        "group_lists": "📋 LİSTELER (Word Native Multilevel):",
        "btn_num_1": "1️⃣ Seviye 1 (1.)",
        "btn_num_2": "2️⃣ Seviye 2 (1.1.)",
        "btn_num_3": "3️⃣ Seviye 3 (1.1.1.)",
        "btn_bullet": "➖ Madde İmi (-)",
        "btn_letter": "🔤 Harf (a))",

        # Özel
        "group_special": "📑 SAYFA DÜZENİ:",
        "btn_title_page": "📄 Kapak Sayfası",

        # Örnek metin
        "example_text": (
            "--- BAŞLIK ---\n"
            "T.C. MARMARA ÜNİVERSİTESİ\n"
            "MÜHENDİSLİK FAKÜLTESİ\n"
            "\n"
            "BİLGİSAYAR MÜHENDİSLİĞİ BÖLÜMÜ\n"
            "\n"
            "DÖNEM PROJESİ RAPORU\n"
            "\n"
            "\n"
            "Hazırlayan: Ad Soyad\n"
            "İstanbul - 2026\n"
            "--- BAŞLIK ---\n"
            "\n"
            "# GİRİŞ\n"
            "\n"
            "Bu belge, GOST R 7.0.97-2016 standartlarına uygun olarak otomatik biçimlendirilmiştir. "
            "Normal paragraflar otomatik olarak 1,25 cm ilk satır girintisi alır ve iki yana yaslanır. "
            "Satır aralığı ve punto ayarları sol menüden seçtiğiniz değerlere göre uygulanır.\n"
            "\n"
            "Word programında bir saat uğraşarak yapacağınız formata, burada sadece düz metin yazarak "
            "saniyeler içinde ulaşabilirsiniz.\n"
            "\n"
            "## NUMARALI LİSTE ÖRNEKLERİ\n"
            "\n"
            "Aşağıdaki liste, Word'ün gerçek çok düzeyli liste (Multilevel List) özelliği ile "
            "kodlanmaktadır. İndirdiğiniz dosyada Word'ün liste butonları aktif olacaktır:\n"
            "1. Birinci ana madde\n"
            "2. İkinci ana madde\n"
            "3. Üçüncü ana madde\n"
            "3.1. Üçüncü maddenin birinci alt maddesi\n"
            "3.2. Üçüncü maddenin ikinci alt maddesi\n"
            "3.2.1. En derin seviye örneği\n"
            "3.2.2. Bir diğer derin seviye maddesi\n"
            "4. Dördüncü ana madde\n"
            "\n"
            "### MADDE İMLERİ VE HARF LİSTESİ\n"
            "\n"
            "Harfli liste örneği:\n"
            "a) Harf ile başlayan birinci madde\n"
            "b) Harf ile başlayan ikinci madde\n"
            "\n"
            "Madde imleri (tire işareti) kullanımı:\n"
            "- Birinci noktalı madde\n"
            "- İkinci noktalı madde\n"
            "- Üçüncü noktalı madde\n"
            "\n"
            "# SONUÇ\n"
            "\n"
            "Siz sadece metninizi yazıp 'Word Belgesini Oluştur' butonuna tıklayın. "
            "Tüm GOST biçimlendirmesini arka plan motoru mükemmel bir şekilde uygulayacaktır."
        ),

        # Snippet'ler
        "snippet_h1": "# Yeni Ana Başlık\n",
        "snippet_h2": "## Yeni Alt Başlık\n",
        "snippet_h3": "### Küçük Başlık\n",
        "snippet_num_1": "1. Birinci madde\n2. İkinci madde\n3. Üçüncü madde\n",
        "snippet_num_2": "1.1. Alt madde bir\n1.2. Alt madde iki\n",
        "snippet_num_3": "1.1.1. Derin alt madde bir\n1.1.2. Derin alt madde iki\n",
        "snippet_bullet": "- Birinci madde\n- İkinci madde\n- Üçüncü madde\n",
        "snippet_letter": "a) Birinci madde\nb) İkinci madde\nc) Üçüncü madde\n",
        "snippet_title": (
            "--- BAŞLIK ---\n"
            "ÜNİVERSİTE ADI\n"
            "FAKÜLTE ADI\n"
            "\n"
            "PROJE ADI\n"
            "\n"
            "Ad Soyad\n"
            "Şehir - 2026\n"
            "--- BAŞLIK ---\n"
        ),

        # Metin kutusu
        "placeholder": (
            "Metninizi buraya yazmaya başlayın...\n\n"
            "Başlık için: # Başlık\n"
            "Liste için: 1. Madde\n"
            "Alt liste: 1.1. Alt madde\n\n"
            "veya yukarıdaki butonları kullanın!"
        ),

        # Oluştur / İndir
        "btn_generate": "🚀 WORD BELGESİNİ OLUŞTUR",
        "warn_empty": "⚠️ Lütfen önce metin kutusuna bir şeyler yazın!",
        "spinner": "GOST standartlarında belgeniz hazırlanıyor, lütfen bekleyin...",
        "success": "🎉 Harika! Belgeniz başarıyla oluşturuldu. Aşağıdaki butonla indirin.",
        "btn_download": "📥 TIKLA VE İNDİR (.docx)",
        "download_name": "GOST_Formatli_Belge.docx",
        "err_msg": "❌ Bir hata oluştu: {}",
    },

    # ───────────────────── ENGLISH ─────────────────────
    "en": {
        "page_title": "GOST Word Generator",
        "title": "📄 GOST-Compliant Word Document Generator",
        "description": (
            "Generate Word (.docx) documents compliant with Russian "
            "**GOST R 7.0.97-2016** standards in seconds. Zero Word knowledge "
            "required — just write plain text, we handle the rest!"
        ),

        "settings": "⚙️ Document Settings",
        "archive_mode": "📁 Archive Mode (Left Margin: 3 cm)",
        "archive_help": (
            "Enable this for documents that will be physically bound or "
            "archived for over 10 years. The left margin increases from "
            "2 cm to 3 cm as required by GOST."
        ),
        "font_size": "🔤 Font Size (pt)",
        "line_spacing": "↕️ Line Spacing",

        "sidebar_guide_title": "📖 Detailed Usage Guide",
        "sidebar_guide": """
**What does this app do?**
It converts your plain text into a Word (.docx) file fully compliant with the Russian GOST R 7.0.97-2016 official document standard. Margins, fonts, spacing, indents, and page numbers are set automatically.

---

**🔵 Writing Normal Paragraphs**
Just type your text. Each `Enter` key press starts a new paragraph. The program automatically:
- Adds a **1.25 cm** first-line indent
- **Justifies** the text (both sides)
- Applies **Times New Roman** font

---

**🟢 Adding Headings**
Place `#` at the beginning of a line:

| You Type | Result |
|---|---|
| `# Introduction` | **MAIN HEADING** (uppercase, bold, centered) |
| `## Subsection` | **Subheading** (bold, centered) |
| `### Small Title` | **Small Heading** (bold, centered) |

> ⚠️ GOST rule: Headings must **not** end with a period.

---

**🟠 Numbered Lists (Multilevel / Native)**
Uses Word's real *Multilevel List* feature. The downloaded file will have active list buttons in Word!

| You Type | Level | Word Output |
|---|---|---|
| `1. Text` | Level 1 | **1.** Text |
| `1.1. Text` | Level 2 | **1.1.** Text |
| `1.1.1. Text` | Level 3 | **1.1.1.** Text |

> 💡 You type the numbers but they are encoded as **automatic numbering** in the Word file. Pressing Enter in Word will auto-generate the next number.

---

**🟣 Bullet Points & Letter Lists**

| You Type | Result |
|---|---|
| `- Text` | – Text (GOST em-dash) |
| `a) Text` | a) Text |

---

**🔴 Title/Cover Page**
Wrap your title content with `--- TITLE ---` tags:
```
--- TITLE ---
UNIVERSITY NAME
Project Title
Your Name
2026
--- TITLE ---
```
Page numbers are automatically **hidden** on the title page.

---

**📐 Automatically Applied GOST Rules**
- 📄 A4 size (21×29.7 cm)
- 📏 Margins: Top/Bottom 2 cm, Left 2 cm (archive: 3 cm), Right 1 cm
- 🔤 Times New Roman, black color
- ↕️ Your chosen line spacing (1.0 / 1.2 / 1.5)
- 🔢 Page numbers: Bottom center, Arabic numerals, no period
- ✏️ Paragraph indent: 1.25 cm (first line)
""",

        "guide_expander": "📖 Quick Start (Click to Expand)",
        "guide_text": """
**Create a document in 3 steps:**

1️⃣ **Left sidebar:** Choose font size, line spacing, and archive mode.

2️⃣ **Text box:** Write your text. Use `#` for headings, `1.` for lists.
   - Not sure? Click **💡 Load Template** to see a working example.

3️⃣ Click **🚀 Generate**, then **📥 Download** your file.

> 💡 **Tip:** Use the colorful buttons above the text box to insert headings, lists, and title pages with one click!
""",

        "content_header": "### ✍️ Document Content",
        "content_desc": (
            "Write or paste your text below. "
            "Click the buttons to easily insert pre-formatted templates."
        ),

        "btn_load_example": "💡 Load Template",
        "btn_clear_text": "🗑️ Clear Text",

        "group_headings": "📌 HEADINGS:",
        "btn_h1": "# Main Heading",
        "btn_h2": "## Subheading",
        "btn_h3": "### Small Heading",

        "group_lists": "📋 LISTS (Word Native Multilevel):",
        "btn_num_1": "1️⃣ Level 1 (1.)",
        "btn_num_2": "2️⃣ Level 2 (1.1.)",
        "btn_num_3": "3️⃣ Level 3 (1.1.1.)",
        "btn_bullet": "➖ Bullet (-)",
        "btn_letter": "🔤 Letter (a))",

        "group_special": "📑 LAYOUT:",
        "btn_title_page": "📄 Title Page",

        "example_text": (
            "--- TITLE ---\n"
            "HARVARD UNIVERSITY\n"
            "DEPARTMENT OF COMPUTER SCIENCE\n"
            "\n"
            "TERM PROJECT REPORT\n"
            "\n"
            "\n"
            "Prepared by: John Doe\n"
            "Cambridge - 2026\n"
            "--- TITLE ---\n"
            "\n"
            "# INTRODUCTION\n"
            "\n"
            "This document has been automatically formatted to comply with GOST R 7.0.97-2016 standards. "
            "Normal paragraphs receive a 1.25 cm first-line indent and are justified. "
            "Line spacing and font size match your sidebar choices.\n"
            "\n"
            "What would take an hour of manual formatting in Word takes just seconds here by writing plain text.\n"
            "\n"
            "## NUMBERED LIST EXAMPLES\n"
            "\n"
            "The following list uses Word's native Multilevel List feature. "
            "The list buttons will be active when you open the file in Word:\n"
            "1. First main item\n"
            "2. Second main item\n"
            "3. Third main item\n"
            "3.1. First sub-item of the third\n"
            "3.2. Second sub-item of the third\n"
            "3.2.1. Deepest level example\n"
            "3.2.2. Another deep level item\n"
            "4. Fourth main item\n"
            "\n"
            "### BULLET POINTS AND LETTER LISTS\n"
            "\n"
            "Lettered list example:\n"
            "a) First letter item\n"
            "b) Second letter item\n"
            "\n"
            "Bullet point (dash) usage:\n"
            "- First bullet item\n"
            "- Second bullet item\n"
            "- Third bullet item\n"
            "\n"
            "# CONCLUSION\n"
            "\n"
            "Just write your text and click 'Generate Word Document'. "
            "The backend engine will apply all GOST formatting flawlessly."
        ),

        "snippet_h1": "# New Main Heading\n",
        "snippet_h2": "## New Subheading\n",
        "snippet_h3": "### Small Heading\n",
        "snippet_num_1": "1. First item\n2. Second item\n3. Third item\n",
        "snippet_num_2": "1.1. Sub-item one\n1.2. Sub-item two\n",
        "snippet_num_3": "1.1.1. Deep sub-item one\n1.1.2. Deep sub-item two\n",
        "snippet_bullet": "- First item\n- Second item\n- Third item\n",
        "snippet_letter": "a) First item\nb) Second item\nc) Third item\n",
        "snippet_title": (
            "--- TITLE ---\n"
            "UNIVERSITY NAME\n"
            "DEPARTMENT NAME\n"
            "\n"
            "PROJECT TITLE\n"
            "\n"
            "Your Name\n"
            "City - 2026\n"
            "--- TITLE ---\n"
        ),

        "placeholder": (
            "Start typing your text here...\n\n"
            "For headings: # Heading\n"
            "For lists: 1. Item\n"
            "Sub-list: 1.1. Sub-item\n\n"
            "or use the buttons above!"
        ),

        "btn_generate": "🚀 GENERATE WORD DOCUMENT",
        "warn_empty": "⚠️ Please write something in the text box first!",
        "spinner": "Your document is being prepared to GOST standards...",
        "success": "🎉 Awesome! Your document was generated successfully. Download it below.",
        "btn_download": "📥 CLICK TO DOWNLOAD (.docx)",
        "download_name": "GOST_Formatted_Document.docx",
        "err_msg": "❌ An error occurred: {}",
    },

    # ───────────────────── РУССКИЙ ─────────────────────
    "ru": {
        "page_title": "Генератор Word (ГОСТ)",
        "title": "📄 Генератор документов Word по ГОСТ",
        "description": (
            "Создавайте документы Word (.docx) по стандартам "
            "**ГОСТ Р 7.0.97-2016** за считанные секунды. Знания Word не требуются — "
            "просто набирайте текст, остальное сделаем мы!"
        ),

        "settings": "⚙️ Настройки документа",
        "archive_mode": "📁 Архивный режим (Левое поле: 3 см)",
        "archive_help": (
            "Включите для документов, подшиваемых в дело или хранящихся "
            "более 10 лет. Левое поле увеличится с 2 до 3 см (требование ГОСТ)."
        ),
        "font_size": "🔤 Размер шрифта (пт)",
        "line_spacing": "↕️ Межстрочный интервал",

        "sidebar_guide_title": "📖 Подробное руководство",
        "sidebar_guide": """
**Что делает это приложение?**
Преобразует ваш обычный текст в файл Word (.docx), полностью соответствующий стандарту ГОСТ Р 7.0.97-2016. Поля, шрифт, интервалы, отступы и нумерация страниц настраиваются автоматически.

---

**🔵 Обычный текст (Абзацы)**
Просто печатайте текст. Каждое нажатие `Enter` создает новый абзац. Программа автоматически:
- Добавляет отступ первой строки **1,25 см**
- **Выравнивание по ширине** (justify)
- Применяет шрифт **Times New Roman**

---

**🟢 Добавление заголовков**
Поставьте `#` в начале строки:

| Вы пишете | Результат |
|---|---|
| `# Введение` | **ГЛАВНЫЙ ЗАГОЛОВОК** (верхний регистр, жирный, по центру) |
| `## Подраздел` | **Подзаголовок** (жирный, по центру) |
| `### Пункт` | **Мелкий заголовок** (жирный, по центру) |

> ⚠️ Правило ГОСТ: В конце заголовков точка **не ставится**.

---

**🟠 Нумерованные списки (Многоуровневые / Нативные)**
Используется встроенная функция *Multilevel List* Word. В скачанном файле кнопки списков будут активны!

| Вы пишете | Уровень | Вывод Word |
|---|---|---|
| `1. Текст` | Уровень 1 | **1.** Текст |
| `1.1. Текст` | Уровень 2 | **1.1.** Текст |
| `1.1.1. Текст` | Уровень 3 | **1.1.1.** Текст |

> 💡 Вы набираете номера, но они кодируются как **автоматическая нумерация** в файле Word. При нажатии Enter в Word следующий номер генерируется автоматически.

---

**🟣 Маркеры и буквенные списки**

| Вы пишете | Результат |
|---|---|
| `- Текст` | – Текст (тире по ГОСТ) |
| `а) Текст` | а) Текст |

---

**🔴 Титульный лист**
Оберните текст титульного листа тегами `--- ТИТУЛ ---`:
```
--- ТИТУЛ ---
НАЗВАНИЕ ОРГАНИЗАЦИИ
Название работы
Имя Фамилия
2026
--- ТИТУЛ ---
```
Номер страницы на титульном листе автоматически **скрывается**.

---

**📐 Автоматически применяемые правила ГОСТ**
- 📄 Формат A4 (21×29,7 см)
- 📏 Поля: Верх/Низ 2 см, Лево 2 см (архив: 3 см), Право 1 см
- 🔤 Times New Roman, черный цвет
- ↕️ Выбранный межстрочный интервал (1.0 / 1.2 / 1.5)
- 🔢 Номера страниц: Внизу по центру, арабские цифры, без точки
- ✏️ Отступ абзаца: 1,25 см (первая строка)
""",

        "guide_expander": "📖 Быстрый старт (нажмите, чтобы открыть)",
        "guide_text": """
**Создайте документ за 3 шага:**

1️⃣ **Левая панель:** выберите размер шрифта, интервал и архивный режим.

2️⃣ **Текстовое поле:** напишите текст. Используйте `#` для заголовков, `1.` для списков.
   - Не уверены? Нажмите **💡 Загрузить шаблон**, чтобы увидеть рабочий пример.

3️⃣ Нажмите **🚀 Создать**, затем **📥 Скачать**.

> 💡 **Совет:** Используйте кнопки над текстовым полем для быстрой вставки заголовков, списков и титульных листов!
""",

        "content_header": "### ✍️ Содержимое документа",
        "content_desc": (
            "Введите или вставьте текст ниже. "
            "Нажмите кнопки, чтобы вставить готовые шаблоны."
        ),

        "btn_load_example": "💡 Загрузить шаблон",
        "btn_clear_text": "🗑️ Очистить текст",

        "group_headings": "📌 ЗАГОЛОВКИ:",
        "btn_h1": "# Главный",
        "btn_h2": "## Подзаголовок",
        "btn_h3": "### Мелкий",

        "group_lists": "📋 СПИСКИ (Нативные Word Multilevel):",
        "btn_num_1": "1️⃣ Уровень 1 (1.)",
        "btn_num_2": "2️⃣ Уровень 2 (1.1.)",
        "btn_num_3": "3️⃣ Уровень 3 (1.1.1.)",
        "btn_bullet": "➖ Маркер (-)",
        "btn_letter": "🔤 Буквы (а))",

        "group_special": "📑 МАКЕТ СТРАНИЦЫ:",
        "btn_title_page": "📄 Титульный лист",

        "example_text": (
            "--- ТИТУЛ ---\n"
            "МОСКОВСКИЙ ГОСУДАРСТВЕННЫЙ УНИВЕРСИТЕТ\n"
            "ФАКУЛЬТЕТ ВЫЧИСЛИТЕЛЬНОЙ МАТЕМАТИКИ И КИБЕРНЕТИКИ\n"
            "\n"
            "КУРСОВАЯ РАБОТА\n"
            "\n"
            "\n"
            "Выполнил: Иванов Иван Иванович\n"
            "Москва - 2026\n"
            "--- ТИТУЛ ---\n"
            "\n"
            "# ВВЕДЕНИЕ\n"
            "\n"
            "Настоящий документ автоматически оформлен в соответствии со стандартом ГОСТ Р 7.0.97-2016. "
            "Обычные абзацы получают отступ первой строки 1,25 см и выравнивание по ширине. "
            "Межстрочный интервал и размер шрифта соответствуют вашему выбору в боковой панели.\n"
            "\n"
            "То, на что в Word уходит час ручного форматирования, здесь занимает секунды.\n"
            "\n"
            "## ПРИМЕРЫ НУМЕРОВАННЫХ СПИСКОВ\n"
            "\n"
            "Следующий список использует встроенную функцию многоуровневого списка Word. "
            "Кнопки списков будут активны при открытии файла в Word:\n"
            "1. Первый основной пункт\n"
            "2. Второй основной пункт\n"
            "3. Третий основной пункт\n"
            "3.1. Первый подпункт третьего\n"
            "3.2. Второй подпункт третьего\n"
            "3.2.1. Пример глубокого уровня\n"
            "3.2.2. Ещё один пункт глубокого уровня\n"
            "4. Четвёртый основной пункт\n"
            "\n"
            "### МАРКИРОВАННЫЕ И БУКВЕННЫЕ СПИСКИ\n"
            "\n"
            "Буквенный список:\n"
            "а) Первый буквенный пункт\n"
            "б) Второй буквенный пункт\n"
            "\n"
            "Маркированный список (тире):\n"
            "- Первый пункт с маркером\n"
            "- Второй пункт с маркером\n"
            "- Третий пункт с маркером\n"
            "\n"
            "# ЗАКЛЮЧЕНИЕ\n"
            "\n"
            "Просто напишите текст и нажмите «Создать документ Word». "
            "Всё форматирование по ГОСТ применится автоматически."
        ),

        "snippet_h1": "# Новый главный заголовок\n",
        "snippet_h2": "## Новый подзаголовок\n",
        "snippet_h3": "### Мелкий заголовок\n",
        "snippet_num_1": "1. Первый пункт\n2. Второй пункт\n3. Третий пункт\n",
        "snippet_num_2": "1.1. Подпункт один\n1.2. Подпункт два\n",
        "snippet_num_3": "1.1.1. Глубокий подпункт один\n1.1.2. Глубокий подпункт два\n",
        "snippet_bullet": "- Первый пункт\n- Второй пункт\n- Третий пункт\n",
        "snippet_letter": "а) Первый пункт\nб) Второй пункт\nв) Третий пункт\n",
        "snippet_title": (
            "--- ТИТУЛ ---\n"
            "НАЗВАНИЕ ОРГАНИЗАЦИИ\n"
            "ПОДРАЗДЕЛЕНИЕ\n"
            "\n"
            "НАЗВАНИЕ РАБОТЫ\n"
            "\n"
            "Имя Фамилия\n"
            "Город - 2026\n"
            "--- ТИТУЛ ---\n"
        ),

        "placeholder": (
            "Начните набирать текст здесь...\n\n"
            "Для заголовков: # Заголовок\n"
            "Для списков: 1. Пункт\n"
            "Подсписок: 1.1. Подпункт\n\n"
            "или используйте кнопки выше!"
        ),

        "btn_generate": "🚀 СОЗДАТЬ ДОКУМЕНТ WORD",
        "warn_empty": "⚠️ Пожалуйста, сначала напишите что-нибудь в текстовом поле!",
        "spinner": "Ваш документ подготавливается по стандартам ГОСТ...",
        "success": "🎉 Отлично! Документ успешно создан. Скачайте его ниже.",
        "btn_download": "📥 СКАЧАТЬ (.docx)",
        "download_name": "Документ_ГОСТ.docx",
        "err_msg": "❌ Произошла ошибка: {}",
    },
}


# ═══════════════════════════════════════════════════════════════
#  STREAMLIT SESSION STATE & HELPERS
# ═══════════════════════════════════════════════════════════════

if "lang" not in st.session_state:
    st.session_state.lang = "tr"

if "doc_text" not in st.session_state:
    st.session_state.doc_text = ""


def add_snippet(snippet):
    """Append a text snippet to the editor, adding newlines if needed."""
    if st.session_state.doc_text and not st.session_state.doc_text.endswith('\n'):
        st.session_state.doc_text += '\n\n'
    st.session_state.doc_text += snippet


def load_example():
    """Replace editor text with the full example template for the active language."""
    st.session_state.doc_text = UI_TEXT[st.session_state.lang]["example_text"]


def clear_text():
    """Clear all text from the editor."""
    st.session_state.doc_text = ""


# ═══════════════════════════════════════════════════════════════
#  PAGE CONFIG & LANGUAGE SELECTOR
# ═══════════════════════════════════════════════════════════════

st.set_page_config(
    page_title=UI_TEXT[st.session_state.lang]["page_title"],
    page_icon="📄",
    layout="wide",
)

lang_options = {"Türkçe (TR)": "tr", "English (EN)": "en", "Русский (RU)": "ru"}
lang_reverse = {v: k for k, v in lang_options.items()}

# Language selector in top-right corner
lang_col1, lang_col2 = st.columns([8, 2])
with lang_col2:
    selected_lang = st.selectbox(
        "Language / Dil / Язык",
        options=list(lang_options.keys()),
        index=list(lang_options.keys()).index(lang_reverse[st.session_state.lang]),
    )
    if lang_options[selected_lang] != st.session_state.lang:
        st.session_state.lang = lang_options[selected_lang]
        st.rerun()

# Shorthand for active language texts
t = UI_TEXT[st.session_state.lang]
lang_code = st.session_state.lang


# ═══════════════════════════════════════════════════════════════
#  SIDEBAR — SETTINGS + DETAILED GUIDE
# ═══════════════════════════════════════════════════════════════

with st.sidebar:
    st.header(t["settings"])
    archive_mode = st.checkbox(t["archive_mode"], value=False, help=t["archive_help"])
    font_size = st.selectbox(t["font_size"], options=[12, 14, 16], index=1)
    line_spacing = st.selectbox(t["line_spacing"], options=[1.0, 1.2, 1.5], index=2)

    st.markdown("---")

    # Full detailed guide in the sidebar
    st.markdown(f"## {t['sidebar_guide_title']}")
    st.markdown(t["sidebar_guide"])


# ═══════════════════════════════════════════════════════════════
#  MAIN CONTENT AREA
# ═══════════════════════════════════════════════════════════════

st.title(t["title"])
st.markdown(t["description"])

# Quick start guide (collapsible)
with st.expander(t["guide_expander"]):
    st.markdown(t["guide_text"])

st.markdown("---")
st.markdown(t["content_header"])
st.markdown(t["content_desc"])


# ── TOP ACTION BUTTONS ──────────────────────────────────────
top_c1, top_c2, _ = st.columns([2, 2, 6])
with top_c1:
    st.button(t["btn_load_example"], on_click=load_example, use_container_width=True)
with top_c2:
    st.button(t["btn_clear_text"], on_click=clear_text, use_container_width=True)

st.write("")

# ── HEADING BUTTONS ─────────────────────────────────────────
st.write(f"**{t['group_headings']}**")
h_c1, h_c2, h_c3, _ = st.columns([2, 2, 2, 4])
with h_c1:
    st.button(t["btn_h1"], on_click=add_snippet, args=(t["snippet_h1"],), use_container_width=True)
with h_c2:
    st.button(t["btn_h2"], on_click=add_snippet, args=(t["snippet_h2"],), use_container_width=True)
with h_c3:
    st.button(t["btn_h3"], on_click=add_snippet, args=(t["snippet_h3"],), use_container_width=True)

# ── LIST BUTTONS ────────────────────────────────────────────
st.write(f"**{t['group_lists']}**")
l_c1, l_c2, l_c3, l_c4, l_c5 = st.columns(5)
with l_c1:
    st.button(t["btn_num_1"], on_click=add_snippet, args=(t["snippet_num_1"],), use_container_width=True)
with l_c2:
    st.button(t["btn_num_2"], on_click=add_snippet, args=(t["snippet_num_2"],), use_container_width=True)
with l_c3:
    st.button(t["btn_num_3"], on_click=add_snippet, args=(t["snippet_num_3"],), use_container_width=True)
with l_c4:
    st.button(t["btn_bullet"], on_click=add_snippet, args=(t["snippet_bullet"],), use_container_width=True)
with l_c5:
    st.button(t["btn_letter"], on_click=add_snippet, args=(t["snippet_letter"],), use_container_width=True)

# ── LAYOUT BUTTONS ──────────────────────────────────────────
st.write(f"**{t['group_special']}**")
s_c1, _ = st.columns([2, 8])
with s_c1:
    st.button(t["btn_title_page"], on_click=add_snippet, args=(t["snippet_title"],), use_container_width=True)


# ── TEXT EDITOR ─────────────────────────────────────────────
text_input = st.text_area(
    "Text Area",
    key="doc_text",
    height=500,
    label_visibility="collapsed",
    placeholder=t["placeholder"],
)


# ── GENERATE & DOWNLOAD ────────────────────────────────────
st.write("")
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
                    lang=lang_code,
                )

                bio = io.BytesIO()
                doc.save(bio)

                st.success(t["success"])

                st.download_button(
                    label=t["btn_download"],
                    data=bio.getvalue(),
                    file_name=t["download_name"],
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    use_container_width=True,
                )
            except Exception as e:
                st.error(t["err_msg"].format(e))
