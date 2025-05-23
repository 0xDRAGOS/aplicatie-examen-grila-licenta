import ttkbootstrap as tb
from tkinter import ttk
from core.score_manager import load_scores
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class ScoreChart(tb.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        tb.Label(self, text="Istoric Scoruri", font=("Helvetica", 16, "bold")).pack(pady=10)

        chart_frame = tb.Frame(self)
        chart_frame.pack(fill=tb.BOTH, expand=True, padx=10, pady=5)

        self.figure = plt.Figure(figsize=(8, 4), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, master=chart_frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill=tb.BOTH, expand=True)

        # Listă scoruri
        self.history_frame = tb.Frame(self)
        self.history_frame.pack(fill=tb.BOTH, expand=True, padx=10, pady=(0, 10))

        self.history_tree = ttk.Treeview(self.history_frame, columns=("data", "mod", "scor", "total"), show="headings")
        self.history_tree.heading("data", text="Dată")
        self.history_tree.heading("mod", text="Mod")
        self.history_tree.heading("scor", text="Scor")
        self.history_tree.heading("total", text="Total")
        self.history_tree.pack(fill=tb.BOTH, expand=True)

        self.plot_scores()

    def plot_scores(self):
        data = load_scores()
        self.ax.clear()
        for row in self.history_tree.get_children():
            self.history_tree.delete(row)

        if not data:
            self.ax.text(0.5, 0.5, 'Fără date disponibile', horizontalalignment='center', verticalalignment='center')
        else:
            dates = [entry['timestamp'] for entry in data]
            scores = [entry['score'] for entry in data]
            totals = [entry['total'] for entry in data]
            modes = [entry['mode'] for entry in data]

            for entry in data:
                self.history_tree.insert("", "end", values=(entry['timestamp'], entry['mode'], entry['score'], entry['total']))

            labels = [f"{m}\n{s}/{t}" for m, s, t in zip(modes, scores, totals)]
            self.ax.plot(dates, scores, marker='o', label='Scor')
            self.ax.set_title("Evoluție Scoruri")
            self.ax.set_ylabel("Punctaj")
            self.ax.set_xlabel("Dată")
            self.ax.set_xticks(dates)
            self.ax.set_xticklabels(labels, rotation=45, ha='right', fontsize=8)
            self.ax.set_ylim(0, max(totals) + 1)
            self.ax.grid(True)
            self.ax.legend()

        self.figure.tight_layout()
        self.canvas.draw()
