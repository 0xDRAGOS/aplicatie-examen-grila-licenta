import os
from ttkbootstrap import Toplevel, Button, Label
from ui.pdf_viewer import PDFViewer

class PDFSelector(Toplevel):
    def __init__(self, parent, pdf_folder="assets/pdf"):
        super().__init__(parent)
        self.title("Grile PDF")
        self.geometry("400x300")
        self.pdf_folder = pdf_folder

        Label(self, text="Selectează un PDF pentru a-l vizualiza:", font=("Helvetica", 12, "bold")).pack(pady=10)

        for filename in os.listdir(self.pdf_folder):
            if filename.lower().endswith(".pdf"):
                full_path = os.path.join(self.pdf_folder, filename)
                btn = Button(self, text=filename, command=lambda f=full_path: self.open_pdf(f))
                btn.pack(fill="x", padx=20, pady=5)

    def open_pdf(self, path):
        PDFViewer(self, path)
