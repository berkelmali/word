"""
belgeolusturucu.py — GOST-Compliant Word Document Generator
Generates .docx files conforming to Russian GOST R 7.0.97-2016 standards.

Supported Languages: Türkçe (TR), English (EN), Русский (RU)

Features:
  - A4 portrait, configurable margins (archive mode: left=3cm)
  - Times New Roman, selectable font size (12/14/16 pt), black color
  - Justified text, 1.25cm first-line indent
  - Selectable line spacing (1.0 / 1.2 / 1.5)
  - Centered page numbers (Arabic, bottom), hidden on title page
  - Markdown-like heading syntax (# Heading 1, ## Heading 2, ### Heading 3)
  - Centered headings, no trailing period, bold, no indent
  - Numbered lists (1. item) and bulleted lists (- item / • item)
  - Title page support (--- TITLE --- block)

Usage:
  python belgeolusturucu.py
"""

import re
import sys
import os
from docx import Document
from docx.shared import Cm, Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.section import WD_ORIENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn, nsdecls
from lxml import etree


# ═══════════════════════════════════════════════════════════════
#  LOCALIZATION
# ═══════════════════════════════════════════════════════════════

STRINGS = {
    "tr": {
        "lang_prompt": "Dil seçin / Select language / Выберите язык (tr/en/ru): ",
        "welcome": "═══ GOST Uyumlu Word Belgesi Oluşturucu ═══",
        "archive_prompt": "Arşiv modu (sol kenar boşluğu 3 cm)? (e/h): ",
        "font_size_prompt": "Font boyutu (12 / 14 / 16) [varsayılan: 14]: ",
        "line_spacing_prompt": "Satır aralığı (1.0 / 1.2 / 1.5) [varsayılan: 1.5]: ",
        "filename_prompt": "Dosya adı (uzantısız) [varsayılan: Formatli_Belge]: ",
        "input_header": "Metni aşağıya yapıştırın. Biçimlendirme kuralları:",
        "rule_heading": "  # Başlık 1  |  ## Başlık 2  |  ### Başlık 3",
        "rule_list_1": "  1. Birinci seviye  |  1.1 İkinci seviye  |  1.1.1 Üçüncü seviye",
        "rule_list_2": "  a) Harf listesi  |  - Madde işareti  |  • Madde işareti",
        "rule_title": "  --- BAŞLIK --- ... --- BAŞLIK --- (Kapak sayfası bloğu)",
        "rule_end": "Bitirmek için boş satıra BITIR / END / КОНЕЦ yazın.",
        "separator": "─" * 56,
        "saving": "Kaydediliyor...",
        "success": "🎉 Belge başarıyla oluşturuldu: '{}'",
        "end_keywords": ["BITIR", "BİTİR", "END", "КОНЕЦ"],
        "title_start": "--- BAŞLIK ---",
        "title_end": "--- BAŞLIK ---",
        "yes_char": "e",
        "invalid_input": "Geçersiz giriş, varsayılan kullanılıyor.",
        "no_content": "⚠ İçerik girilmedi, belge oluşturulmadı.",
    },
    "en": {
        "lang_prompt": "Dil seçin / Select language / Выберите язык (tr/en/ru): ",
        "welcome": "═══ GOST-Compliant Word Document Generator ═══",
        "archive_prompt": "Archive mode (left margin 3 cm)? (y/n): ",
        "font_size_prompt": "Font size (12 / 14 / 16) [default: 14]: ",
        "line_spacing_prompt": "Line spacing (1.0 / 1.2 / 1.5) [default: 1.5]: ",
        "filename_prompt": "File name (without extension) [default: Formatted_Document]: ",
        "input_header": "Paste your text below. Formatting rules:",
        "rule_heading": "  # Heading 1  |  ## Heading 2  |  ### Heading 3",
        "rule_list_1": "  1. First level  |  1.1 Second level  |  1.1.1 Third level",
        "rule_list_2": "  a) Letter list  |  - Bullet  |  • Bullet",
        "rule_title": "  --- TITLE --- ... --- TITLE --- (Title page block)",
        "rule_end": "Type END / BITIR / КОНЕЦ on a blank line to finish.",
        "separator": "─" * 56,
        "saving": "Saving...",
        "success": "🎉 Document created successfully: '{}'",
        "end_keywords": ["END", "BITIR", "BİTİR", "КОНЕЦ"],
        "title_start": "--- TITLE ---",
        "title_end": "--- TITLE ---",
        "yes_char": "y",
        "invalid_input": "Invalid input, using default.",
        "no_content": "⚠ No content entered, document not created.",
    },
    "ru": {
        "lang_prompt": "Dil seçin / Select language / Выберите язык (tr/en/ru): ",
        "welcome": "═══ Генератор документов Word (ГОСТ) ═══",
        "archive_prompt": "Архивный режим (левое поле 3 см)? (д/н): ",
        "font_size_prompt": "Размер шрифта (12 / 14 / 16) [по умолчанию: 14]: ",
        "line_spacing_prompt": "Межстрочный интервал (1.0 / 1.2 / 1.5) [по умолчанию: 1.5]: ",
        "filename_prompt": "Имя файла (без расширения) [по умолчанию: Форматированный_Документ]: ",
        "input_header": "Вставьте текст ниже. Правила форматирования:",
        "rule_heading": "  # Заголовок 1  |  ## Заголовок 2  |  ### Заголовок 3",
        "rule_list_1": "  1. Первый уровень  |  1.1 Второй  |  1.1.1 Третий",
        "rule_list_2": "  а) Буквенный  |  - Маркер  |  • Маркер",
        "rule_title": "  --- ТИТУЛ --- ... --- ТИТУЛ --- (Блок титульного листа)",
        "rule_end": "Введите КОНЕЦ / END / BITIR на пустой строке для завершения.",
        "separator": "─" * 56,
        "saving": "Сохранение...",
        "success": "🎉 Документ успешно создан: '{}'",
        "end_keywords": ["КОНЕЦ", "END", "BITIR", "BİTİR"],
        "title_start": "--- ТИТУЛ ---",
        "title_end": "--- ТИТУЛ ---",
        "yes_char": "д",
        "invalid_input": "Неверный ввод, используется значение по умолчанию.",
        "no_content": "⚠ Содержимое не введено, документ не создан.",
    },
}


# ═══════════════════════════════════════════════════════════════
#  XML HELPERS
# ═══════════════════════════════════════════════════════════════

def add_page_number_field(run):
    """Insert a PAGE field code into the given run (for footer)."""
    fldChar_begin = OxmlElement('w:fldChar')
    fldChar_begin.set(qn('w:fldCharType'), 'begin')

    instrText = OxmlElement('w:instrText')
    instrText.set(qn('xml:space'), 'preserve')
    instrText.text = " PAGE "

    fldChar_sep = OxmlElement('w:fldChar')
    fldChar_sep.set(qn('w:fldCharType'), 'separate')

    # Placeholder text shown before field updates
    fldChar_text = OxmlElement('w:t')
    fldChar_text.text = "1"

    fldChar_end = OxmlElement('w:fldChar')
    fldChar_end.set(qn('w:fldCharType'), 'end')

    run._r.append(fldChar_begin)
    run._r.append(instrText)
    run._r.append(fldChar_sep)
    run._r.append(fldChar_text)
    run._r.append(fldChar_end)


def set_run_font(run, font_name="Times New Roman", font_size=14, bold=False):
    """Configure a run's font properties to GOST standards."""
    run.font.name = font_name
    run.font.size = Pt(font_size)
    run.font.color.rgb = RGBColor(0, 0, 0)
    run.bold = bold
    # Ensure Times New Roman is applied for Cyrillic/Latin via rFonts
    rPr = run._r.get_or_add_rPr()
    rFonts = OxmlElement('w:rFonts')
    rFonts.set(qn('w:ascii'), font_name)
    rFonts.set(qn('w:hAnsi'), font_name)
    rFonts.set(qn('w:cs'), font_name)
    rFonts.set(qn('w:eastAsia'), font_name)
    rPr.insert(0, rFonts)


def suppress_page_number_on_first_page(section):
    """Set the section so that page numbering starts but is hidden on the first page (title page)."""
    section.different_first_page_header_footer = True
    # The first-page footer is intentionally left empty so no number appears


def set_page_number_start(section, start=1):
    """Set the starting page number for a section."""
    sectPr = section._sectPr
    pgNumType = OxmlElement('w:pgNumType')
    pgNumType.set(qn('w:start'), str(start))
    sectPr.append(pgNumType)


# ═══════════════════════════════════════════════════════════════
#  LINE PARSERS
# ═══════════════════════════════════════════════════════════════

HEADING_RE = re.compile(r'^(#{1,3})\s+(.+)$')

# Multi-level numbering patterns (order matters — most specific first)
# Level 3: "1.1.1" or "1.1.1)" followed by text
NUMBERED_L3_RE = re.compile(r'^(\d+\.\d+\.\d+)[.)\s]\s*(.+)$')
# Level 2: "1.1" or "1.1)" followed by text
NUMBERED_L2_RE = re.compile(r'^(\d+\.\d+)[.)\s]\s*(.+)$')
# Level 1: "1." or "1)" followed by text
NUMBERED_L1_RE = re.compile(r'^(\d+)[.)]\s+(.+)$')
# Letter numbering: "a)" / "b)" / "a." / "b." etc.
LETTER_LIST_RE = re.compile(r'^([a-zA-Zа-яА-ЯёЁ])[.)]\s+(.+)$')

BULLET_LIST_RE = re.compile(r'^[-•–]\s+(.+)$')


def parse_line(line):
    """
    Determine line type and return (type, content, level).
    Types: 'heading', 'numbered', 'letter', 'bullet', 'text', 'empty'
    Level: indentation depth (1, 2, 3 for numbered; 0 for others)
    """
    stripped = line.strip()

    if not stripped:
        return ('empty', '', 0)

    # Heading: # / ## / ###
    m = HEADING_RE.match(stripped)
    if m:
        level = len(m.group(1))  # 1, 2, or 3
        text = m.group(2).rstrip('.')  # Remove trailing period per GOST
        return ('heading', text, level)

    # Multi-level numbered lists (check deepest first)
    # Level 3: "1.1.1 text"
    m = NUMBERED_L3_RE.match(stripped)
    if m:
        return ('numbered', stripped, 3)

    # Level 2: "1.1 text" or "2.1 text"
    m = NUMBERED_L2_RE.match(stripped)
    if m:
        return ('numbered', stripped, 2)

    # Level 1: "1. text" or "1) text"
    m = NUMBERED_L1_RE.match(stripped)
    if m:
        return ('numbered', stripped, 1)

    # Letter list: "a) text" or "б. text"
    m = LETTER_LIST_RE.match(stripped)
    if m:
        return ('letter', stripped, 0)

    # Bulleted list: "- text" or "• text" or "– text"
    m = BULLET_LIST_RE.match(stripped)
    if m:
        return ('bullet', m.group(1), 0)

    return ('text', stripped, 0)


# ═══════════════════════════════════════════════════════════════
#  DOCUMENT BUILDER
# ═══════════════════════════════════════════════════════════════

def build_document(lines, *, archive_mode=False, font_size=14, line_spacing=1.5, lang="tr"):
    """Build and return a python-docx Document from parsed lines."""
    doc = Document()
    s = STRINGS[lang]

    # ── Section: A4 Portrait with GOST margins ──────────────
    section = doc.sections[0]
    section.page_height = Cm(29.7)
    section.page_width = Cm(21.0)
    section.orientation = WD_ORIENT.PORTRAIT
    section.top_margin = Cm(2.0)
    section.bottom_margin = Cm(2.0)
    section.left_margin = Cm(3.0) if archive_mode else Cm(2.0)
    section.right_margin = Cm(1.0)

    # ── Page numbering starts at 1 ─────────────────────────
    set_page_number_start(section, start=1)

    # ── Normal style: GOST font & paragraph rules ──────────
    style_normal = doc.styles['Normal']
    style_normal.font.name = 'Times New Roman'
    style_normal.font.size = Pt(font_size)
    style_normal.font.color.rgb = RGBColor(0, 0, 0)

    pf = style_normal.paragraph_format
    pf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    pf.first_line_indent = Cm(1.25)
    pf.line_spacing = line_spacing
    pf.space_before = Pt(0)
    pf.space_after = Pt(0)

    # Ensure Times New Roman for all character sets on default style
    rPr = style_normal._element.get_or_add_rPr()
    rFonts = OxmlElement('w:rFonts')
    rFonts.set(qn('w:ascii'), 'Times New Roman')
    rFonts.set(qn('w:hAnsi'), 'Times New Roman')
    rFonts.set(qn('w:cs'), 'Times New Roman')
    rFonts.set(qn('w:eastAsia'), 'Times New Roman')
    rPr.insert(0, rFonts)

    # ── Detect title page block ─────────────────────────────
    title_lines = []
    body_lines = []
    title_start_tag = s["title_start"].strip().upper()
    title_end_tag = s["title_end"].strip().upper()

    in_title_block = False
    title_closed = False
    for line in lines:
        upper = line.strip().upper()
        if not in_title_block and not title_closed and upper == title_start_tag:
            in_title_block = True
            continue
        if in_title_block and upper == title_end_tag:
            in_title_block = False
            title_closed = True
            continue
        if in_title_block:
            title_lines.append(line)
        else:
            body_lines.append(line)

    # ── Title page (if given) ───────────────────────────────
    has_title_page = len(title_lines) > 0

    if has_title_page:
        # Hide page number on title page
        suppress_page_number_on_first_page(section)

        # Center title content vertically by adding spacing
        for i, tl in enumerate(title_lines):
            stripped = tl.strip()
            if not stripped:
                doc.add_paragraph("")  # Preserve blank lines on title page
                continue
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.first_line_indent = Cm(0)
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            run = p.add_run(stripped)
            set_run_font(run, font_size=font_size, bold=(i < 3))

        # Add page break after title
        doc.add_page_break()

    # ── Footer: centered page number ────────────────────────
    footer = section.footer
    footer.is_linked_to_previous = False
    footer_para = footer.paragraphs[0]
    footer_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    footer_run = footer_para.add_run()
    set_run_font(footer_run, font_size=font_size)
    add_page_number_field(footer_run)

    # ── Indentation per numbering level ──────────────────────
    # Level 1: standard 1.25cm indent | Level 2: +1.25cm | Level 3: +2.5cm
    LIST_INDENT = {
        1: Cm(1.25),   # "1. text"  — first level
        2: Cm(2.50),   # "1.1 text" — second level
        3: Cm(3.75),   # "1.1.1 text" — third level
    }

    # ── Process body lines ──────────────────────────────────
    for line in body_lines:
        line_type, content, level = parse_line(line)

        if line_type == 'empty':
            # Preserve paragraph breaks (empty line = visual separator)
            continue

        elif line_type == 'heading':
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.first_line_indent = Cm(0)
            p.paragraph_format.space_before = Pt(12)
            p.paragraph_format.space_after = Pt(6)
            run = p.add_run(content)
            # Heading level styling
            if level == 1:
                set_run_font(run, font_size=font_size, bold=True)
                run.font.all_caps = True
            elif level == 2:
                set_run_font(run, font_size=font_size, bold=True)
            else:
                set_run_font(run, font_size=font_size, bold=True)

        elif line_type == 'numbered':
            indent = LIST_INDENT.get(level, Cm(1.25))
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            p.paragraph_format.first_line_indent = Cm(0)
            p.paragraph_format.left_indent = indent
            run = p.add_run(content)
            set_run_font(run, font_size=font_size)

        elif line_type == 'letter':
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            p.paragraph_format.first_line_indent = Cm(0)
            p.paragraph_format.left_indent = Cm(2.50)  # Same as level 2
            run = p.add_run(content)
            set_run_font(run, font_size=font_size)

        elif line_type == 'bullet':
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            p.paragraph_format.first_line_indent = Cm(0)
            p.paragraph_format.left_indent = Cm(1.25)
            run = p.add_run(f"– {content}")  # GOST uses em-dash for bullets
            set_run_font(run, font_size=font_size)

        else:  # 'text'
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            p.paragraph_format.first_line_indent = Cm(1.25)
            p.paragraph_format.line_spacing = line_spacing
            run = p.add_run(content)
            set_run_font(run, font_size=font_size)

    return doc


# ═══════════════════════════════════════════════════════════════
#  INTERACTIVE MENU
# ═══════════════════════════════════════════════════════════════

def choose_language():
    """Prompt for language selection."""
    while True:
        choice = input("Dil seçin / Select language / Выберите язык (tr/en/ru): ").strip().lower()
        if choice in STRINGS:
            return choice
        print("→ tr / en / ru")


def get_yes_no(prompt, yes_char):
    """Return True if user answers yes."""
    answer = input(prompt).strip().lower()
    return answer == yes_char


def get_choice(prompt, valid, default, s):
    """Return a validated numeric choice or default."""
    raw = input(prompt).strip()
    if not raw:
        return default
    try:
        val = type(default)(raw)
        if val in valid:
            return val
    except (ValueError, TypeError):
        pass
    print(f"  {s['invalid_input']}")
    return default


def main():
    """Main entry point — interactive document creation."""
    # ── Language ────────────────────────────────────────────
    lang = choose_language()
    s = STRINGS[lang]

    print()
    print(s["welcome"])
    print(s["separator"])

    # ── Configuration ───────────────────────────────────────
    archive_mode = get_yes_no(s["archive_prompt"], s["yes_char"])

    font_size = get_choice(
        s["font_size_prompt"],
        valid=[12, 14, 16],
        default=14,
        s=s
    )

    line_spacing = get_choice(
        s["line_spacing_prompt"],
        valid=[1.0, 1.2, 1.5],
        default=1.5,
        s=s
    )

    # ── Default filenames per language ──────────────────────
    default_names = {"tr": "Formatli_Belge", "en": "Formatted_Document", "ru": "Форматированный_Документ"}
    filename_raw = input(s["filename_prompt"]).strip()
    filename = filename_raw if filename_raw else default_names[lang]
    # Sanitize filename
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)

    print()
    print(s["separator"])
    print(s["input_header"])
    print(s["rule_heading"])
    print(s["rule_list_1"])
    print(s["rule_list_2"])
    print(s["rule_title"])
    print(s["rule_end"])
    print(s["separator"])
    print()

    # ── Text input ──────────────────────────────────────────
    end_keywords = {kw.upper() for kw in s["end_keywords"]}
    lines = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        if line.strip().upper() in end_keywords:
            break
        lines.append(line)

    if not any(l.strip() for l in lines):
        print(s["no_content"])
        return

    # ── Build & save ────────────────────────────────────────
    print()
    print(s["saving"])

    doc = build_document(
        lines,
        archive_mode=archive_mode,
        font_size=font_size,
        line_spacing=line_spacing,
        lang=lang,
    )

    output_path = os.path.join(os.getcwd(), f"{filename}.docx")
    doc.save(output_path)

    print(s["separator"])
    print(s["success"].format(output_path))


if __name__ == "__main__":
    main()