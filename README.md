# GOST-Compliant Word Document Generator

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://6qns4xhzjch6tnawzjuaez.streamlit.app/#gost-standartlarinda-word-belgesi-olusturucu)

A professional, multi-lingual Streamlit application that generates Word (`.docx`) documents strictly complying with Russian **GOST R 7.0.97-2016** official document standards.

No prior knowledge of Microsoft Word formatting is required. Write in simple Markdown-like text, and the application will handle the margins, fonts, line spacing, native multilevel lists, and indents automatically.

## 🚀 Live Demo

You can try out the application online without any installation:
**[Go to the Live Application](https://6qns4xhzjch6tnawzjuaez.streamlit.app/#gost-standartlarinda-word-belgesi-olusturucu)**

## 🌟 Features

- **GOST R 7.0.97-2016 Compliance:** Automatically formats documents to meet official Russian standards.
- **Multi-language Support:** The interface is available in Turkish (TR), English (EN), and Russian (RU).
- **Native Word XML Generation:** Uses genuine Multilevel Lists feature of Microsoft Word, making downloaded files easy to edit.
- **Smart Formatting:**
  - A4 Portrait layout.
  - Automatic margins (Top/Bottom: 2cm, Left: 2cm, Right: 1cm).
  - Archive Mode (increases Left margin to 3cm for physically bound documents).
  - Times New Roman font (configurable size: 12, 14, or 16 pt).
  - Configurable line spacing (1.0, 1.2, or 1.5).
  - Justified text with 1.25cm first-line indent.
  - Centered page numbers (Arabic, hidden on title pages).
- **Markdown-like Syntax Support:**
  - Headings (`#`, `##`, `###`)
  - Numbered Lists (`1.`, `1.1.`, `1.1.1.`)
  - Bullet Points (`-`)
  - Lettered Lists (`a)`)
  - Title Pages (`--- TITLE ---`)

## 🛠️ Local Installation & Usage

If you prefer to run the application locally on your machine, follow these steps:

### Prerequisites

- Python 3.8 or higher.

### Installation

1. Clone this repository or download the source code.
2. Navigate to the project directory.
3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

### Running the App

Start the Streamlit server:

```bash
streamlit run app.py
```

The application will open in your default web browser (usually at `http://localhost:8501`).

## 📖 How to Use

1. **Configure Settings:** Use the left sidebar to choose your preferred font size, line spacing, and archive mode.
2. **Write Content:** Use the main text area to write your document. You can use `#` for headings, `1.` for lists, etc.
   - Click the **"Load Template"** button to see a full working example with proper syntax.
   - Use the quick-insert buttons above the text area to easily add formatted blocks.
3. **Generate:** Enter a file name and click the **"Generate Word Document"** button.
4. **Download:** Once processing is finished, download your `.docx` file using the provided download button.

## 📄 License

This project is open-source and available for use and modification.
