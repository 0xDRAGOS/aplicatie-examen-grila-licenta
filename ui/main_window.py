import ttkbootstrap as tb
from ttkbootstrap.constants import *
from core.data_loader import load_subjects
from ui.pdf_selector import PDFSelector
from ui.study_panel import StudyPanel
from ui.test_panel import TestPanel
from ui.score_chart import ScoreChart
from ui.landing_page import LandingPage
from ui.style_utils import apply_custom_styles
from core.constants import QUESTION_FILE_PATH
from PIL import Image, ImageTk

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.subjects = load_subjects(QUESTION_FILE_PATH)

        self.header_frame = tb.Frame(self.root)
        self.header_frame.pack(fill=X, padx=10, pady=5)

        self.nav_frame = tb.Frame(self.root)
        self.nav_frame.pack(fill=X, padx=10, pady=5)

        logo_img = Image.open("assets/images/logo.png")
        logo_img = logo_img.resize((64, 64), Image.Resampling.LANCZOS)
        self.logo_tk = ImageTk.PhotoImage(logo_img)

        self.logo_label = tb.Label(self.nav_frame, image=self.logo_tk)
        self.logo_label.pack(side=LEFT, padx=(0, 10))

        self.home_btn = tb.Button(self.nav_frame, text="🏠 Acasă", command=self.show_landing)
        self.home_btn.pack(side=LEFT, padx=5)

        self.study_btn = tb.Button(self.nav_frame, text="📘 Mod Învățare", command=self.show_study_mode)
        self.study_btn.pack(side=LEFT, padx=5)

        self.test_btn = tb.Button(self.nav_frame, text="📝 Mod Test", command=self.show_test_mode)
        self.test_btn.pack(side=LEFT, padx=5)

        self.chart_btn = tb.Button(self.nav_frame, text="📈 Istoric Scoruri", command=self.show_score_chart)
        self.chart_btn.pack(side=LEFT, padx=5)

        self.pdf_btn = tb.Button(self.nav_frame, text="📄 Grile PDF", command=self.open_pdf_selector)
        self.pdf_btn.pack(side=LEFT, padx=5)

        self.panel_container = tb.Frame(self.root)
        self.panel_container.pack(fill=BOTH, expand=True, padx=10, pady=10)

        self.study_panel = StudyPanel(self.panel_container, self.subjects)
        self.test_panel = TestPanel(self.panel_container, self.subjects)
        self.chart_panel = ScoreChart(self.panel_container)
        self.landing_panel = LandingPage(
            self.panel_container,
            on_start_study=self.show_study_mode,
            on_start_test=self.show_test_mode,
            on_view_scores=self.show_score_chart
        )

        self.show_landing()

    def open_pdf_selector(self):
        PDFSelector(self.root)

    def show_landing(self):
        self.hide_all_panels()
        self.landing_panel.pack(fill=BOTH, expand=True)

    def show_study_mode(self):
        self.hide_all_panels()
        self.study_panel.pack(fill=BOTH, expand=True)

    def show_test_mode(self):
        self.hide_all_panels()
        self.test_panel.pack(fill=BOTH, expand=True)

    def show_score_chart(self):
        self.hide_all_panels()
        self.chart_panel.plot_scores()
        self.chart_panel.pack(fill=BOTH, expand=True)

    def hide_all_panels(self):
        for panel in [self.study_panel, self.test_panel, self.chart_panel, self.landing_panel]:
            panel.pack_forget()
