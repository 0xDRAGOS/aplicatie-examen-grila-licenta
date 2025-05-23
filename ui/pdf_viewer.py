import os
from PIL import Image, ImageTk
import fitz
import ttkbootstrap as tb
from ui.scrollable_frame import ScrollableFrame


class PDFViewer(tb.Toplevel):
    def __init__(self, parent, filepath):
        super().__init__(parent)
        self.title(f"Vizualizare PDF - {os.path.basename(filepath)}")
        self.geometry("1280x720")

        self.scroll_frame = ScrollableFrame(self)
        self.scroll_frame.pack(fill="both", expand=True)

        self.load_pdf(filepath)

    def load_pdf(self, path):
        doc = fitz.open(path)
        zoom = 2
        mat = fitz.Matrix(zoom, zoom)

        for page in doc:
            pix = page.get_pixmap(matrix=mat)
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            photo = ImageTk.PhotoImage(image=img)
            lbl = tb.Label(self.scroll_frame.scrollable_frame, image=photo, background="white")
            lbl.image = photo  # Keep reference
            lbl.pack(pady=10)

        doc.close()
