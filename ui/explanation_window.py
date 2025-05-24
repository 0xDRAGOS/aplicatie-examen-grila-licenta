import ttkbootstrap as tb

class ExplanationWindow(tb.Toplevel):
    def __init__(self, parent, explanation_text):
        super().__init__(parent)
        self.title("Explicație")
        self.geometry("600x400")
        label = tb.Label(self, text="Explicație:", font=("Helvetica", 13, "bold"))
        label.pack(pady=10)

        text_widget = tb.Text(self, wrap="word", font=("Helvetica", 11))
        text_widget.insert("1.0", explanation_text)
        text_widget.config(state="disabled")
        text_widget.pack(expand=True, fill="both", padx=10, pady=10)
