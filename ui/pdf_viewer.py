import os
from PIL import Image, ImageTk, ImageDraw
import fitz
import ttkbootstrap as tb
from ui.scrollable_frame import ScrollableFrame


class PDFViewer(tb.Toplevel):
    def __init__(self, parent, filepath):
        super().__init__(parent)
        self.title(f"Vizualizare PDF - {os.path.basename(filepath)}")
        self.geometry("1280x720")

        self.filepath = filepath
        self.images = []
        self.labels = []
        self.matches = []
        self.current_match_index = -1

        self.search_frame = tb.Frame(self)
        self.search_frame.pack(fill="x", padx=10, pady=5)

        self.search_entry = tb.Entry(self.search_frame, width=50)
        self.search_entry.pack(side="left", padx=(0, 10))

        self.search_button = tb.Button(self.search_frame, text="Caută", command=self.search_text)
        self.search_button.pack(side="left")

        self.next_button = tb.Button(self.search_frame, text="Următorul", command=self.next_match, state="disabled")
        self.next_button.pack(side="left", padx=(10, 0))

        self.scroll_frame = ScrollableFrame(self)
        self.scroll_frame.pack(fill="both", expand=True)

        self.load_pdf(filepath)

    def load_pdf(self, path):
        self.doc = fitz.open(path)
        zoom = 2
        mat = fitz.Matrix(zoom, zoom)

        for page_num, page in enumerate(self.doc):
            pix = page.get_pixmap(matrix=mat)
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

            photo = ImageTk.PhotoImage(image=img)
            lbl = tb.Label(self.scroll_frame.scrollable_frame, image=photo, background="white")
            lbl.image = photo
            lbl.pack(pady=10)

            self.images.append(img)
            self.labels.append(lbl)

    def search_text(self):
        query = self.search_entry.get()
        if not query:
            return

        self.matches = []
        self.current_match_index = -1
        zoom = 2
        mat = fitz.Matrix(zoom, zoom)

        for page_num, page in enumerate(self.doc):
            pix = page.get_pixmap(matrix=mat)
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            photo = ImageTk.PhotoImage(image=img)
            lbl = self.labels[page_num]
            lbl.configure(image=photo)
            lbl.image = photo
            self.images[page_num] = img

        for page_num, page in enumerate(self.doc):
            text_instances = page.search_for(query)
            for rect in text_instances:
                self.matches.append((page_num, rect))

        if self.matches:
            self.next_button.config(state="normal")
            self.current_match_index = -1
            self.next_match()
        else:
            self.next_button.config(state="disabled")

    def next_match(self):
        if not self.matches:
            return

        self.current_match_index = (self.current_match_index + 1) % len(self.matches)
        page_num, rect = self.matches[self.current_match_index]

        zoom = 2
        mat = fitz.Matrix(zoom, zoom)
        page = self.doc[page_num]
        pix = page.get_pixmap(matrix=mat)
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

        draw = ImageDraw.Draw(img)
        r = [int(zoom * x) for x in rect]
        draw.rectangle(r, outline="red", width=5)

        photo = ImageTk.PhotoImage(image=img)
        lbl = self.labels[page_num]
        lbl.configure(image=photo)
        lbl.image = photo
        self.images[page_num] = img

        lbl.update_idletasks()
        self.scroll_frame.canvas.yview_moveto(lbl.winfo_y() / self.scroll_frame.scrollable_frame.winfo_height())
