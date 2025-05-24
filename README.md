# 🧠 Exam Preparation App – Multiple Choice Training Environment

This is a desktop application built with Python and Tkinter (with ttkbootstrap) designed to help users study and test their knowledge using multiple choice questions. It is ideal for students preparing for exams that involve computer science, algorithms, or programming.

## 📦 Features

- **Learning Mode (Study Mode)**:  
  - Browse questions by subject  
  - Immediate feedback after each answer  
  - Highlighting of correct and incorrect options  

- **Test Mode**:  
  - 30 randomly selected questions  
  - Countdown timer  
  - Real-time scoring  
  - Final score summary  

- **Score History & Analytics**:  
  - View past scores in a chart  
  - Differentiates between study and test modes  

- **PDF Viewer**:  
  - Browse and open related exam PDFs  
  - Scrollable and readable inside the app  

- **Responsive UI**:  
  - Built with ttkbootstrap for modern look  
  - Automatically resizes based on screen resolution

## 📁 Project Structure

```
📂 assets/
   ├── grile.json               # Main question set
   ├── images/                  # Images used in questions
   └── pdf/                     # Official exam PDFs

📂 core/
   ├── data_loader.py          # Loads and parses JSON questions
   ├── score_manager.py        # Saves & loads score history
   └── constants.py            # Global app settings (e.g. TEST_DURATION)

📂 ui/
   ├── main_window.py          # Root UI layout and navigation
   ├── study_panel.py          # Learning mode interface
   ├── test_panel.py           # Testing mode interface
   ├── pdf_selector.py         # Lists PDFs
   ├── pdf_viewer.py           # PDF viewing window
   ├── score_chart.py          # Score history graph
   ├── style_utils.py          # Theme styling helpers
   └── scrollable_frame.py     # Reusable scrollable container

📂 scripts/
   └── creare_grile.py, indenteaza_cod.py  # Internal tools
```

## ✅ Requirements

- Python 3.10+
- `Pillow`
- `ttkbootstrap`
- `PyMuPDF` (fitz)
- `matplotlib`

You can install all dependencies using:

```bash
pip install -r requirements.txt
```

## 🚀 Getting Started

```bash
python ui/main.py
```

## ⚙️ Configuration

You can adjust test duration or score file location in `core/constants.py`:

```python
TEST_DURATION_SECONDS = 30 * 60  # 30 minutes
SCORE_FILE = "assets/scores.json"
```

## 📚 License

This project is created for educational use.
