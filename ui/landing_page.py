import ttkbootstrap as tb
from ttkbootstrap.constants import CENTER
from ui.scrollable_frame import ScrollableFrame


class LandingPage(tb.Frame):
    def __init__(self, parent, on_start_study, on_start_test, on_view_scores):
        super().__init__(parent)

        scrollable = ScrollableFrame(self)
        scrollable.pack(fill="both", expand=True)
        content = scrollable.scrollable_frame

        content.columnconfigure(0, weight=1)

        wrapper = tb.Frame(content)
        wrapper.grid(row=0, column=0, pady=30)
        wrapper.columnconfigure(0, weight=1)

        hero = tb.Frame(wrapper)
        hero.grid(row=0, column=0, pady=30)

        tb.Label(hero, text="🎓 Mediu de Învățare și Testare", font=("Helvetica", 28, "bold"), justify=CENTER).pack(pady=10)
        tb.Label(
            hero,
            text="Exersează, testează-te și urmărește-ți progresul. Totul într-un singur loc."
                 " Aplicație educațională modernă pentru pregătire profesională și academică.",
            font=("Helvetica", 13), wraplength=900, justify=CENTER
        ).pack(pady=10)

        tb.Button(hero, text="📘 Începe Învățarea", bootstyle="primary", width=25, command=on_start_study).pack(pady=5)
        tb.Button(hero, text="📝 Începe un Test", bootstyle="success", width=25, command=on_start_test).pack(pady=5)
        tb.Button(hero, text="📊 Vezi Istoric Scoruri", bootstyle="info", width=25, command=on_view_scores).pack(pady=5)

        benefits = tb.Frame(wrapper)
        benefits.grid(row=1, column=0, pady=20)

        tb.Label(benefits, text="🔍 Ce îți oferim", font=("Helvetica", 16, "bold"), justify=CENTER).pack(pady=10)
        for text in [
            "✔️ Feedback instant la fiecare întrebare",
            "✔️ Teste cronometrate cu rezultate salvate",
            "✔️ Vizualizare evoluție scoruri în timp",
            "✔️ Interfață prietenoasă"
        ]:
            tb.Label(benefits, text=text, font=("Helvetica", 11)).pack(pady=2)

        steps = tb.Frame(wrapper)
        steps.grid(row=2, column=0, pady=20)
        tb.Label(steps, text="🔧 Cum funcționează", font=("Helvetica", 16, "bold"), justify=CENTER).pack(pady=10)
        for idx, step in enumerate([
            "1️⃣ Selectează o materie",
            "2️⃣ Parcurge întrebările pe rând",
            "3️⃣ Primește feedback în timp real",
            "4️⃣ Monitorizează progresul tău"
        ], 1):
            tb.Label(steps, text=step, font=("Helvetica", 11)).pack(pady=2)

        footer = tb.Frame(wrapper)
        footer.grid(row=3, column=0, pady=20)
        tb.Label(footer, text="© 2025 Aplicație educațională în Python", font=("Helvetica", 9), foreground="gray").pack()
