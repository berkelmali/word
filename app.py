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

---

**📝 Dosya Adı**
Belgeyi indirmeden önce bir dosya adı yazmanız zorunludur. Uzantı (.docx) otomatik eklenir.
""",

        # Ana sayfa — Rehber (expander)
        "guide_expander": "📖 Hızlı Başlangıç (Tıklayarak Açın)",
        "guide_text": """
**3 adımda belge oluşturun:**

1️⃣ **Sol menüden** punto, satır aralığı ve arşiv modunu seçin.

2️⃣ **Metin kutusuna** yazınızı yazın. Başlık için `#`, liste için `1.` kullanın.
   - Emin değilseniz **💡 Örnek Şablon Yükle** butonuna basarak hazır bir örnek yükleyin.

3️⃣ **Dosya adını** yazın (zorunlu) ve **🚀 Oluştur** butonuna basın, ardından **📥 İndir** ile dosyanızı alın.

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

        # Örnek metin (UZATILMIŞ VERSİYON)
        "example_text": (
            "--- BAŞLIK ---\n"
            "ULUSLARARASI KIBRIS ÜNİVERSİTESİ\n"
            "MÜHENDİSLİK FAKÜLTESİ\n"
            "\n"
            "YAZILIM MÜHENDİSLİĞİ BÖLÜMÜ\n"
            "\n"
            "GOST R 7.0.97-2016 STANDARTLARI TEST VE KULLANIM KILAVUZU\n"
            "KAPSAMLI DÖNEM PROJESİ RAPORU\n"
            "\n"
            "Hazırlayan: Berk Elmalı\n"
            "Lefkoşa - 2026\n"
            "--- BAŞLIK ---\n"
            "\n"
            "# 1. GİRİŞ VE BELGE YAPISI\n"
            "\n"
            "Bu belge, GOST R 7.0.97-2016 standartlarına uygun olarak otomatik biçimlendirilmiş kapsamlı bir test dokümanıdır. "
            "Amacımız, tüm başlık, paragraf ve çok düzeyli liste (multilevel list) fonksiyonlarının Word ortamında sorunsuz "
            "bir şekilde render edildiğini doğrulamaktır. Paragraflar otomatik olarak 1,25 cm ilk satır girintisi alır ve iki yana "
            "yaslanır (justify). Sol menüden seçtiğiniz punto ve satır aralığı ayarları tüm metne kusursuzca uygulanır.\n"
            "\n"
            "Belgenin arşiv modu açıksa sol kenar boşluğu 3 cm, kapalıysa 2 cm olacaktır. Bu ayarların tümü Word'ün XML motoruna "
            "doğrudan native olarak yazılır.\n"
            "\n"
            "## 1.1 TEMEL PARAGRAF KURALLARI\n"
            "\n"
            "GOST standartlarına göre paragraflar arasında ekstra boşluk (Space Before/After) bırakılmaz. Sadece satır aralığı "
            "çarpanı (1.0, 1.2 veya 1.5) kullanılır. Ayrıca, Space (Boşluk) veya Tab tuşları ile girinti yapmak kesinlikle yasaktır; "
            "girintiler sistem tarafından paragraf özelliklerine (w:ind) işlenmelidir.\n"
            "\n"
            "## 1.2 BAŞLIKLAR VE HİYERARŞİ\n"
            "\n"
            "Başlıklar sayfaya ortalanır ve sonlarına kesinlikle nokta konmaz. İçerik oluştururken hiyerarşiyi bozmamak, "
            "okunabilirliği artırır. Şimdi bu yapıyı test eden ilk çok düzeyli listemize geçelim.\n"
            "\n"
            "# 2. BİRİNCİ LİSTE TESTİ: DONANIM VE YAZILIM GEREKSİNİMLERİ\n"
            "\n"
            "Aşağıdaki liste, Word'ün gerçek çok düzeyli liste özelliği ile oluşturulmuştur. Rakamların sonunda GOST gereği "
            "nokta bulunmaktadır.\n"
            "\n"
            "1. Sistem Gereksinimleri\n"
            "1.1. Donanım Gereksinimleri\n"
            "1.1.1. En az 16 GB RAM kapasitesi\n"
            "1.1.2. 512 GB NVMe SSD depolama alanı\n"
            "1.1.3. Çok çekirdekli modern bir işlemci\n"
            "1.2. Yazılım Gereksinimleri\n"
            "1.2.1. İşletim sistemi (Windows 11 veya macOS Sonoma)\n"
            "1.2.2. Python 3.12 veya üzeri sürümler\n"
            "1.2.3. Gerekli kütüphanelerin (python-docx, streamlit) kurulumu\n"
            "2. Ağ ve Güvenlik Altyapısı\n"
            "2.1. İç Ağ Yapılandırması\n"
            "2.2. Güvenlik Duvarı (Firewall) Ayarları\n"
            "2.2.1. Gelen bağlantı kuralları (Inbound rules)\n"
            "2.2.2. Giden bağlantı kuralları (Outbound rules)\n"
            "3. Kullanıcı Yetkilendirmeleri\n"
            "3.1. Yönetici (Admin) Yetkileri\n"
            "3.2. Standart Kullanıcı Yetkileri\n"
            "\n"
            "Bu kısımdan sonra normal bir paragraf girerek liste bağlamını (context) koparıyoruz. Word, araya normal metin veya "
            "başlık girdiğinde numaralandırmayı otomatik olarak sıfırlamalı veya yeni bir liste başlatacak şekilde ayarlanmalıdır.\n"
            "\n"
            "# 3. İKİNCİ LİSTE TESTİ: PROJE YÖNETİM SÜREÇLERİ\n"
            "\n"
            "Burada yeni bir liste başlatıyoruz. Bu listenin tekrar 1'den başlaması gerekmektedir, çünkü araya başlık ve normal "
            "metin girmiştir.\n"
            "\n"
            "1. Proje Başlatma Aşaması\n"
            "1.1. Paydaş analizi ve gereksinim toplantıları\n"
            "1.2. Proje tüzüğünün (Project Charter) hazırlanması\n"
            "2. Planlama Aşaması\n"
            "2.1. Kapsam yönetim planı\n"
            "2.2. Zaman çizelgesi ve Gantt şeması oluşturma\n"
            "2.2.1. Kritik yol (Critical Path) analizi\n"
            "2.2.2. Kaynak atamaları ve efor tahmini\n"
            "2.3. Bütçe ve Maliyet Planlaması\n"
            "2.3.1. Doğrudan maliyetler\n"
            "2.3.2. Dolaylı maliyetler ve rezervler\n"
            "3. Yürütme ve Kontrol Aşaması\n"
            "3.1. Kalite güvence metriklerinin takibi\n"
            "3.2. Risk yönetimi ve azaltma stratejileri\n"
            "4. Kapanış Aşaması\n"
            "\n"
            "Gördüğünüz gibi çok düzeyli listeler, araya farklı elemanlar girse bile hiyerarşiyi hatasız bir şekilde korur ve Word "
            "üzerinde 'Multilevel List' özelliğini aktif tutar.\n"
            "\n"
            "### ALT BÖLÜM: MADDE İMLERİ VE HARFLİ LİSTELER\n"
            "\n"
            "Numaralı listelerin yanı sıra, GOST standartlarında madde imleri (tire işareti) ve harfli listeler de sıklıkla kullanılır. "
            "Kiril veya Latin alfabesi fark etmeksizin asılı girinti (hanging indent) kuralları uygulanır.\n"
            "\n"
            "Harfli liste örneği (Performans Kriterleri):\n"
            "a) Sistemin yanıt süresinin 200ms altında olması\n"
            "b) Eşzamanlı 10.000 kullanıcıyı destekleyebilmesi\n"
            "c) Yüzde 99.9 (Three Nines) uptime garantisi sağlaması\n"
            "\n"
            "Madde imi (Tire) örneği (Güvenlik Önlemleri):\n"
            "- Uçtan uca şifreleme (E2EE) protokollerinin uygulanması\n"
            "- Veritabanı yedeklerinin günlük, haftalık ve aylık rotasyonlarla alınması\n"
            "- Düzenli sızma (Penetration) testlerinin gerçekleştirilmesi\n"
            "- Çok faktörlü kimlik doğrulama (MFA) zorunluluğu\n"
            "\n"
            "# 4. SONUÇ VE DEĞERLENDİRME\n"
            "\n"
            "Hazırlanan bu uzun test dokümanı, Word'ün iç yapısındaki numbering.xml dosyasına yapılan müdahalelerin ne kadar tutarlı "
            "çalıştığını kanıtlamak amacıyla oluşturulmuştur. Numaralandırma XML'i içerisine enjekte edilen w:abstractNum ve w:lvl "
            "tanımları sayesinde, her bir liste elemanı manuel olarak yazılmış gibi değil, Word'ün kendi liste motoruyla üretilmiş gibi davranır.\n"
            "\n"
            "1. Testlerin Başarı Durumu\n"
            "1.1. Numaralandırma mantığı başarılı\n"
            "1.2. Girinti ve asılı girinti (hanging indent) değerleri GOST standartlarında\n"
            "1.2.1. Seviye 1 girintisi (1.25 cm) başarılı\n"
            "1.2.2. Seviye 2 girintisi (2.50 cm) başarılı\n"
            "1.2.3. Seviye 3 girintisi (3.75 cm) başarılı\n"
            "\n"
            "Bu şablonu silerek kendi raporunuzu yazmaya başlayabilir veya yukarıdaki menüden ayarları değiştirerek belgeyi tekrar oluşturabilirsiniz."
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
            "Berk Elmalı\n"
            "Lefkoşa - 2026\n"
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
        "filename_label": "📝 Dosya Adı (.docx uzantısı otomatik eklenir):",
        "filename_placeholder": "Örn: Dönem Projesi Raporu",
        "warn_no_filename": "⚠️ Lütfen dosya adını yazın!",
        "warn_invalid_filename": "⚠️ Dosya adında şu karakterler kullanılamaz: < > : \" / \\ | ? *",
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

---

**📝 File Name**
You must enter a file name before downloading. The .docx extension is added automatically.
""",

        "guide_expander": "📖 Quick Start (Click to Expand)",
        "guide_text": """
**Create a document in 3 steps:**

1️⃣ **Left sidebar:** Choose font size, line spacing, and archive mode.

2️⃣ **Text box:** Write your text. Use `#` for headings, `1.` for lists.
   - Not sure? Click **💡 Load Template** to see a working example.

3️⃣ **Type a file name** (required), click **🚀 Generate**, then **📥 Download** your file.

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
            "CYPRUS INTERNATIONAL UNIVERSITY\n"
            "FACULTY OF ENGINEERING\n"
            "\n"
            "DEPARTMENT OF SOFTWARE ENGINEERING\n"
            "\n"
            "GOST R 7.0.97-2016 STANDARDS TEST AND USER GUIDE\n"
            "COMPREHENSIVE TERM PROJECT REPORT\n"
            "\n"
            "Prepared by: Berk Elmalı\n"
            "Nicosia - 2026\n"
            "--- TITLE ---\n"
            "\n"
            "# 1. INTRODUCTION AND DOCUMENT STRUCTURE\n"
            "\n"
            "This document is a comprehensive test file automatically formatted to comply with Russian GOST R 7.0.97-2016 standards. "
            "Our goal is to verify that all headings, paragraphs, and multilevel list functions render flawlessly in the native Word "
            "environment. Paragraphs automatically receive a 1.25 cm first-line indent and are fully justified. The font size and "
            "line spacing settings selected from the left menu are applied perfectly throughout the text.\n"
            "\n"
            "If the document's archive mode is enabled, the left margin will be 3 cm; otherwise, it is 2 cm. All these configurations "
            "are directly written into Word's XML engine (native).\n"
            "\n"
            "## 1.1 BASIC PARAGRAPH RULES\n"
            "\n"
            "According to GOST standards, extra spacing (Space Before/After) between paragraphs is not permitted. Only the line "
            "spacing multiplier (1.0, 1.2, or 1.5) is used. Furthermore, indenting using the Space or Tab keys is strictly forbidden; "
            "indents must be handled by the system through paragraph properties (w:ind).\n"
            "\n"
            "## 1.2 HEADINGS AND HIERARCHY\n"
            "\n"
            "Headings are centered on the page and must absolutely not end with a period. Maintaining hierarchy while creating "
            "content significantly improves readability. Now, let's move on to our first multilevel list to test this structure.\n"
            "\n"
            "# 2. FIRST LIST TEST: HARDWARE AND SOFTWARE REQUIREMENTS\n"
            "\n"
            "The list below is generated using Word's genuine multilevel list feature. In accordance with GOST, there is a period "
            "at the end of the digits.\n"
            "\n"
            "1. System Requirements\n"
            "1.1. Hardware Requirements\n"
            "1.1.1. Minimum 16 GB RAM capacity\n"
            "1.1.2. 512 GB NVMe SSD storage space\n"
            "1.1.3. A modern multi-core processor\n"
            "1.2. Software Requirements\n"
            "1.2.1. Operating system (Windows 11 or macOS Sonoma)\n"
            "1.2.2. Python 3.12 or newer versions\n"
            "1.2.3. Installation of required libraries (python-docx, streamlit)\n"
            "2. Network and Security Infrastructure\n"
            "2.1. Internal Network Configuration\n"
            "2.2. Firewall Settings\n"
            "2.2.1. Inbound connection rules\n"
            "2.2.2. Outbound connection rules\n"
            "3. User Authorizations\n"
            "3.1. Administrator (Admin) Privileges\n"
            "3.2. Standard User Privileges\n"
            "\n"
            "After this section, we insert a normal paragraph to break the list context. Word must automatically reset the numbering "
            "or start a new list when normal text or a heading is inserted in between.\n"
            "\n"
            "# 3. SECOND LIST TEST: PROJECT MANAGEMENT PROCESSES\n"
            "\n"
            "Here we are starting a completely new list. This list must restart from 1, because a heading and normal text have intervened.\n"
            "\n"
            "1. Project Initiation Phase\n"
            "1.1. Stakeholder analysis and requirement meetings\n"
            "1.2. Preparation of the Project Charter\n"
            "2. Planning Phase\n"
            "2.1. Scope management plan\n"
            "2.2. Timeline and Gantt chart creation\n"
            "2.2.1. Critical Path analysis\n"
            "2.2.2. Resource assignments and effort estimation\n"
            "2.3. Budget and Cost Planning\n"
            "2.3.1. Direct costs\n"
            "2.3.2. Indirect costs and reserves\n"
            "3. Execution and Control Phase\n"
            "3.1. Tracking quality assurance metrics\n"
            "3.2. Risk management and mitigation strategies\n"
            "4. Closure Phase\n"
            "\n"
            "As you can see, multilevel lists flawlessly preserve the hierarchy even if different elements intervene, and keep the "
            "'Multilevel List' feature active in Word.\n"
            "\n"
            "### SUBSECTION: BULLET POINTS AND LETTERED LISTS\n"
            "\n"
            "In addition to numbered lists, bullet points (em-dashes) and lettered lists are frequently used in GOST standards. "
            "Hanging indent rules apply regardless of whether the Cyrillic or Latin alphabet is used.\n"
            "\n"
            "Lettered list example (Performance Criteria):\n"
            "a) System response time must be under 200ms\n"
            "b) Must support 10,000 concurrent users\n"
            "c) Must guarantee 99.9% (Three Nines) uptime\n"
            "\n"
            "Bullet point (Dash) example (Security Measures):\n"
            "- Implementation of End-to-End Encryption (E2EE) protocols\n"
            "- Daily, weekly, and monthly rotation of database backups\n"
            "- Execution of regular Penetration tests\n"
            "- Mandatory Multi-Factor Authentication (MFA)\n"
            "\n"
            "# 4. CONCLUSION AND EVALUATION\n"
            "\n"
            "This lengthy test document was created to prove how consistently the interventions made to the numbering.xml file within "
            "Word's internal structure work. Thanks to the w:abstractNum and w:lvl definitions injected into the numbering XML, each "
            "list item acts as if it was produced by Word's own list engine, not manually typed.\n"
            "\n"
            "1. Test Success Status\n"
            "1.1. Numbering logic is successful\n"
            "1.2. Indent and hanging indent values meet GOST standards\n"
            "1.2.1. Level 1 indent (1.25 cm) successful\n"
            "1.2.2. Level 2 indent (2.50 cm) successful\n"
            "1.2.3. Level 3 indent (3.75 cm) successful\n"
            "\n"
            "You can delete this template to start writing your own report or modify the settings from the menu above to regenerate the document."
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
            "Berk Elmalı\n"
            "Nicosia - 2026\n"
            "--- TITLE ---\n"
        ),

        "placeholder": (
            "Start typing your text here...\n\n"
            "For headings: # Heading\n"
            "For lists: 1. Item\n"
            "Sub-list: 1.1. Sub-item\n\n"
            "or use the buttons above!"
        ),

        "filename_label": "📝 File Name (.docx extension is added automatically):",
        "filename_placeholder": "E.g.: Term Project Report",
        "warn_no_filename": "⚠️ Please enter a file name!",
        "warn_invalid_filename": "⚠️ File name cannot contain these characters: < > : \" / \\ | ? *",
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

---

**📝 Имя файла**
Перед загрузкой необходимо указать имя файла. Расширение .docx добавляется автоматически.
""",

        "guide_expander": "📖 Быстрый старт (нажмите, чтобы открыть)",
        "guide_text": """
**Создайте документ за 3 шага:**

1️⃣ **Левая панель:** выберите размер шрифта, интервал и архивный режим.

2️⃣ **Текстовое поле:** напишите текст. Используйте `#` для заголовков, `1.` для списков.
   - Не уверены? Нажмите **💡 Загрузить шаблон**, чтобы увидеть рабочий пример.

3️⃣ **Введите имя файла** (обязательно), нажмите **🚀 Создать**, затем **📥 Скачать**.

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
            "МЕЖДУНАРОДНЫЙ УНИВЕРСИТЕТ КИПРА\n"
            "ИНЖЕНЕРНЫЙ ФАКУЛЬТЕТ\n"
            "\n"
            "КАФЕДРА ПРОГРАММНОЙ ИНЖЕНЕРИИ\n"
            "\n"
            "ТЕСТОВОЕ И РУКОВОДСТВО ПО СТАНДАРТАМ ГОСТ Р 7.0.97-2016\n"
            "КОМПЛЕКСНЫЙ ОТЧЕТ ПО КУРСОВОМУ ПРОЕКТУ\n"
            "\n"
            "Выполнил: Berk Elmalı\n"
            "Никосия - 2026\n"
            "--- ТИТУЛ ---\n"
            "\n"
            "# 1. ВВЕДЕНИЕ И СТРУКТУРА ДОКУМЕНТА\n"
            "\n"
            "Данный документ представляет собой комплексный тестовый файл, автоматически отформатированный в соответствии с "
            "российскими стандартами ГОСТ Р 7.0.97-2016. Наша цель — убедиться, что все заголовки, абзацы и функции "
            "многоуровневых списков безупречно отображаются в собственной среде Word. Абзацы автоматически получают отступ "
            "первой строки 1,25 см и выравниваются по ширине. Настройки размера шрифта и межстрочного интервала, выбранные "
            "в левом меню, идеально применяются ко всему тексту.\n"
            "\n"
            "Если включен архивный режим документа, левое поле составит 3 см; в противном случае — 2 см. Все эти настройки "
            "напрямую записываются в XML-движок Word.\n"
            "\n"
            "## 1.1 ОСНОВНЫЕ ПРАВИЛА АБЗАЦА\n"
            "\n"
            "Согласно стандартам ГОСТ, дополнительные интервалы (до/после) между абзацами не допускаются. Используется только "
            "множитель межстрочного интервала (1.0, 1.2 или 1.5). Кроме того, категорически запрещается делать отступы с "
            "помощью клавиш Space или Tab; отступы должны обрабатываться системой через свойства абзаца (w:ind).\n"
            "\n"
            "## 1.2 ЗАГОЛОВКИ И ИЕРАРХИЯ\n"
            "\n"
            "Заголовки центрируются на странице и категорически не должны заканчиваться точкой. Сохранение иерархии при создании "
            "контента значительно улучшает читаемость. Теперь давайте перейдем к нашему первому многоуровневому списку для проверки "
            "этой структуры.\n"
            "\n"
            "# 2. ТЕСТ ПЕРВОГО СПИСКА: АППАРАТНЫЕ И ПРОГРАММНЫЕ ТРЕБОВАНИЯ\n"
            "\n"
            "Приведенный ниже список создан с использованием настоящей функции многоуровневого списка Word. В соответствии с "
            "ГОСТом, в конце цифр ставится точка.\n"
            "\n"
            "1. Системные требования\n"
            "1.1. Аппаратные требования\n"
            "1.1.1. Минимум 16 ГБ оперативной памяти\n"
            "1.1.2. 512 ГБ NVMe SSD дискового пространства\n"
            "1.1.3. Современный многоядерный процессор\n"
            "1.2. Программные требования\n"
            "1.2.1. Операционная система (Windows 11 или macOS Sonoma)\n"
            "1.2.2. Python 3.12 или более новые версии\n"
            "1.2.3. Установка необходимых библиотек (python-docx, streamlit)\n"
            "2. Сетевая инфраструктура и безопасность\n"
            "2.1. Конфигурация внутренней сети\n"
            "2.2. Настройки брандмауэра (Firewall)\n"
            "2.2.1. Правила входящих подключений\n"
            "2.2.2. Правила исходящих подключений\n"
            "3. Авторизация пользователей\n"
            "3.1. Права администратора (Admin)\n"
            "3.2. Права стандартного пользователя\n"
            "\n"
            "После этого раздела мы вставляем обычный абзац, чтобы разорвать контекст списка. Word должен автоматически сбросить "
            "нумерацию или начать новый список, когда между ними вставляется обычный текст или заголовок.\n"
            "\n"
            "# 3. ТЕСТ ВТОРОГО СПИСКА: ПРОЦЕССЫ УПРАВЛЕНИЯ ПРОЕКТАМИ\n"
            "\n"
            "Здесь мы начинаем совершенно новый список. Этот список должен начаться заново с 1, так как между ними вклинились "
            "заголовок и обычный текст.\n"
            "\n"
            "1. Фаза инициации проекта\n"
            "1.1. Анализ заинтересованных сторон и встречи по требованиям\n"
            "1.2. Подготовка Устава проекта (Project Charter)\n"
            "2. Фаза планирования\n"
            "2.1. План управления содержанием\n"
            "2.2. Создание временной шкалы и диаграммы Ганта\n"
            "2.2.1. Анализ критического пути (Critical Path)\n"
            "2.2.2. Назначение ресурсов и оценка трудозатрат\n"
            "2.3. Бюджет и планирование затрат\n"
            "2.3.1. Прямые затраты\n"
            "2.3.2. Косвенные затраты и резервы\n"
            "3. Фаза выполнения и контроля\n"
            "3.1. Отслеживание метрик обеспечения качества\n"
            "3.2. Управление рисками и стратегии их снижения\n"
            "4. Фаза завершения\n"
            "\n"
            "Как видите, многоуровневые списки безупречно сохраняют иерархию, даже если вмешиваются другие элементы, и сохраняют "
            "активной функцию «Многоуровневый список» в Word.\n"
            "\n"
            "### ПОДРАЗДЕЛ: МАРКИРОВАННЫЕ И БУКВЕННЫЕ СПИСКИ\n"
            "\n"
            "Помимо нумерованных списков, в стандартах ГОСТ часто используются маркированные (тире) и буквенные списки. Правила "
            "выступающего отступа (hanging indent) применяются независимо от того, используется кириллица или латиница.\n"
            "\n"
            "Пример буквенного списка (Критерии производительности):\n"
            "а) Время отклика системы должно быть менее 200 мс\n"
            "б) Поддержка 10 000 одновременных пользователей\n"
            "в) Гарантия аптайма 99,9% (Three Nines)\n"
            "\n"
            "Пример маркированного списка (Меры безопасности):\n"
            "- Внедрение протоколов сквозного шифрования (E2EE)\n"
            "- Ежедневная, еженедельная и ежемесячная ротация резервных копий баз данных\n"
            "- Регулярное проведение тестов на проникновение (Penetration tests)\n"
            "- Обязательная многофакторная аутентификация (MFA)\n"
            "\n"
            "# 4. ЗАКЛЮЧЕНИЕ И ОЦЕНКА\n"
            "\n"
            "Этот объемный тестовый документ был создан для того, чтобы доказать, насколько стабильно работают вмешательства "
            "в файл numbering.xml во внутренней структуре Word. Благодаря определениям w:abstractNum и w:lvl, внедренным в XML "
            "нумерации, каждый элемент списка ведет себя так, как будто он создан собственным движком списков Word, а не введен вручную.\n"
            "\n"
            "1. Статус успешности тестов\n"
            "1.1. Логика нумерации работает успешно\n"
            "1.2. Значения отступа и выступающего отступа (hanging indent) соответствуют стандартам ГОСТ\n"
            "1.2.1. Отступ 1-го уровня (1,25 см) успешен\n"
            "1.2.2. Отступ 2-го уровня (2,50 см) успешен\n"
            "1.2.3. Отступ 3-го уровня (3,75 см) успешен\n"
            "\n"
            "Вы можете удалить этот шаблон, чтобы начать писать собственный отчет, или изменить настройки в меню слева, "
            "чтобы перегенерировать документ."
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
            "Berk Elmalı\n"
            "Никосия - 2026\n"
            "--- ТИТУЛ ---\n"
        ),

        "placeholder": (
            "Начните набирать текст здесь...\n\n"
            "Для заголовков: # Заголовок\n"
            "Для списков: 1. Пункт\n"
            "Подсписок: 1.1. Подпункт\n\n"
            "или используйте кнопки выше!"
        ),

        "filename_label": "📝 Имя файла (расширение .docx добавляется автоматически):",
        "filename_placeholder": "Напр.: Курсовая Работа",
        "warn_no_filename": "⚠️ Пожалуйста, введите имя файла!",
        "warn_invalid_filename": "⚠️ Имя файла не может содержать символы: < > : \" / \\ | ? *",
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


# ── FILE NAME INPUT ─────────────────────────────────────────
st.write("")
file_name_input = st.text_input(
    t["filename_label"],
    value="",
    placeholder=t["filename_placeholder"],
    help=t.get("warn_invalid_filename", ""),
)

# ── GENERATE & DOWNLOAD ────────────────────────────────────
st.write("")
import re as _re
_INVALID_CHARS = _re.compile(r'[<>:"/\\|?*]')

if st.button(t["btn_generate"], type="primary", use_container_width=True):
    if not file_name_input.strip():
        st.warning(t["warn_no_filename"])
    elif _INVALID_CHARS.search(file_name_input.strip()):
        st.warning(t["warn_invalid_filename"])
    elif not st.session_state.doc_text.strip():
        st.warning(t["warn_empty"])
    else:
        final_filename = f"{file_name_input.strip()}.docx"

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
                    file_name=final_filename,
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    use_container_width=True,
                )
            except Exception as e:
                st.error(t["err_msg"].format(e))
