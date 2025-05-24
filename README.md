# 🧠 Exam Preparation App – Multiple Choice Training Environment

This is a desktop application built with Python and Tkinter (using `ttkbootstrap`) designed to help users study and test their knowledge using multiple choice questions. It is ideal for students preparing for computer science-related exams.

## 📦 Features

- **Learning Mode (Study Panel)**  
  - Select questions by subject  
  - Instant feedback  
  - Highlights correct/incorrect options  
  - View explanation for each answer  

- **Test Mode (Test Panel)**  
  - 30 randomized questions  
  - 30-minute countdown timer  
  - Real-time scoring  
  - Final score and performance summary  

- **Explanation Window**  
  - Click "See Explanation" after answering  
  - Opens a separate window with detailed explanation  

- **PDF Viewer**  
  - View original PDF exams  
  - Search functionality  
  - Scrollable display  

- **Score Analytics**  
  - Visual chart for score history  
  - Tracks study vs. test results  

- **Modern Interface**  
  - Built with `ttkbootstrap`  
  - Scrollable UI components  
  - Auto resizing to screen resolution  

## 📁 Project Structure

```
📂 assets/
   ├── grile.json, grile2.json, grile_fara_indentare.json
   ├── scores.json
   ├── images/                 # Question images
   └── pdf/                    # PDF source files

📂 core/
   ├── constants.py            # Constants like test time, question count
   ├── data_loader.py          # Loads and parses questions
   └── score_manager.py        # Score saving/loading

📂 scripts/
   ├── creare_grile.py         # Generate new question sets
   ├── genereaza_explicatii.py # Generate explanations via OpenAI API
   ├── tradu_explicatii.py     # Translate explanations to Romanian
   ├── indenteaza_cod.py       # JSON code formatter
   └── sterge_pyc.py           # Cleanup utility

📂 ui/
   ├── main_window.py          # Main UI container
   ├── landing_page.py         # Starting panel
   ├── study_panel.py          # Learning interface
   ├── test_panel.py           # Testing interface
   ├── explanation_window.py   # Explanation popup after answering
   ├── scrollable_frame.py     # Scrollable frame wrapper
   ├── pdf_selector.py         # PDF file list UI
   ├── pdf_viewer.py           # PDF reader with search
   ├── score_chart.py          # Graph view of scores
   └── style_utils.py          # Theme and style utilities

📄 main.py                     # App entry point
📄 old_main.py                 # Legacy entry (backup)
📄 requirements.txt            # Python dependencies
📄 README.md                   # Project description
```

## ✅ Requirements

- Python 3.10+
- `ttkbootstrap`
- `Pillow`
- `PyMuPDF` (fitz)
- `matplotlib`
- `openai`
- `python-dotenv`

Install them via:

```bash
pip install -r requirements.txt
```

## 🚀 Getting Started

```bash
python main.py
```

## 🔐 API Keys

To generate explanations via OpenAI:
1. Create a `.env` file in the `scripts/` folder.
2. Add your key:

```
OPENAI_API_KEY=sk-...
```

3. Run `scripts/genereaza_explicatii.py` or `tradu_explicatii.py` for generation/translation.

## ⚙️ Configurable Settings

You can change test duration or number of questions in:

```python
# core/constants.py
TEST_DURATION_SECONDS = 30 * 60
NUM_TEST_QUESTIONS = 30
```

## 📚 License

This project is intended for educational use and academic exam preparation.