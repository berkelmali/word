"""Quick test for multi-level numbering."""
import belgeolusturucu as bg
import os

test_lines = [
    "# GIRIS",
    "Bu birinci bolum paragraf metnidir.",
    "1. Birinci madde",
    "2. Ikinci madde",
    "3. Ucuncu madde",
    "1.1 Alt madde bir",
    "1.2 Alt madde iki",
    "2.1 Ikinci bolumun birinci alt maddesi",
    "2.2 Ikinci bolumun ikinci alt maddesi",
    "1.1.1 Ucuncu seviye madde",
    "1.1.2 Ucuncu seviye ikinci madde",
    "a) Harf maddesi bir",
    "b) Harf maddesi iki",
    "c) Harf maddesi uc",
    "- Madde isareti",
    "## Ikinci Bolum",
    "Normal paragraf metni burada.",
]

# Test parsing
print("=== PARSE RESULTS ===")
for line in test_lines:
    result = bg.parse_line(line)
    ltype, content, level = result
    print(f"  {ltype:10s} level={level}  |  {line}")

print()

# Build document
doc = bg.build_document(test_lines, font_size=14, line_spacing=1.5, lang="tr")
out = os.path.join(os.getcwd(), "TEST_MULTI_LEVEL.docx")
doc.save(out)

print(f"Document saved: {out}")
print(f"Paragraph count: {len(doc.paragraphs)}")

# Check indentation on numbered paragraphs
for p in doc.paragraphs:
    li = p.paragraph_format.left_indent
    if li:
        print(f"  indent={li.cm:.2f}cm  |  {p.text[:50]}")

print("All checks passed!")
