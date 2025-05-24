import os
import random
import ttkbootstrap as tb
from tkinter import ttk
from PIL import Image, ImageTk
from core.score_manager import save_score
from core.constants import TEST_DURATION_SECONDS, NUM_TEST_QUESTIONS
from ui.scrollable_frame import ScrollableFrame
from ui.explanation_window import ExplanationWindow


class TestPanel(tb.Frame):
    def __init__(self, parent, subjects):
        super().__init__(parent)
        self.subjects = subjects
        self.questions = []
        self.current_index = 0
        self.correct_count = 0
        self.timer_id = None
        self.remaining_seconds = TEST_DURATION_SECONDS
        self.option_widgets = {}

        self.top_bar = tb.Frame(self)
        self.top_bar.pack(fill="x", pady=(10, 0), padx=10)

        self.top_stats = tb.Frame(self.top_bar)
        self.top_stats.pack(fill="x")
        self.score_label = tb.Label(self.top_stats, text="📊 Scor: 0/0 - Parcurs: 0/0", font=("Helvetica", 0, "bold"))
        self.score_label.pack(side="right")

        self.title_frame = tb.Frame(self)
        self.title_frame.pack(pady=10)

        self.test_info_label = tb.Label(self.title_frame, text=f"🧪 Test din {NUM_TEST_QUESTIONS} întrebări aleatorii",
                                        font=("Helvetica", 13, "bold"))
        self.test_info_label.pack()

        self.timer_label = tb.Label(self.title_frame, text="⏳ Timp rămas: 30:00", font=("Helvetica", 11),
                                    foreground="blue")
        self.timer_label.pack(pady=2)

        self.start_btn = tb.Button(self.title_frame, text="🚀 Începe Testul", command=self.start_test,
                                   bootstyle="success")
        self.start_btn.pack(pady=5)

        self.scroll_frame = ScrollableFrame(self)
        self.scroll_frame.pack(fill=tb.BOTH, expand=True, pady=10)

        self.q_label = tb.Label(self.scroll_frame.scrollable_frame, text="", wraplength=1000, font=("Segoe UI Symbol", 14, "bold"))
        self.q_label.pack(anchor='w', padx=10, pady=(10, 5))

        self.img_label = tb.Label(self.scroll_frame.scrollable_frame)
        self.img_label.pack(pady=5, anchor='w')

        self.options_frame = tb.Frame(self.scroll_frame.scrollable_frame)
        self.options_frame.pack(anchor='w', padx=10)

        self.feedback_label = tb.Label(self.scroll_frame.scrollable_frame, text="", font=("Helvetica", 11))
        self.feedback_label.pack(pady=5, anchor='w', padx=10)

        self.button_frame = tb.Frame(self)
        self.button_frame.pack(pady=10)
        self.answer_btn = tb.Button(self.button_frame, text="Răspunde", command=self.check_answer, state='disabled')
        self.answer_btn.pack(side='left', padx=5)
        self.next_btn = tb.Button(self.button_frame, text="Următoarea", command=self.next_question, state='disabled')
        self.next_btn.pack(side='left', padx=5)
        self.explanation_btn = tb.Button(self.button_frame, text="Vezi Explicația", command=self.show_explanation,
                                         state='disabled')
        self.explanation_btn.pack(side='left', padx=5)

    def update_score(self):
        self.score_label.config(
            text=f"📊 Scor: {self.correct_count}/{len(self.questions)} - Parcurs: {self.current_index + 1}/{len(self.questions)}")

    def start_test(self):
        all_questions = [q for s in self.subjects for q in s['questions']]
        self.questions = random.sample(all_questions, min(NUM_TEST_QUESTIONS, len(all_questions)))
        self.current_index = 0
        self.correct_count = 0
        self.remaining_seconds = TEST_DURATION_SECONDS
        self.update_timer()
        self.show_question()
        self.answer_btn.config(state='normal')
        self.update_score()

    def update_timer(self):
        mins, secs = divmod(self.remaining_seconds, 60)
        self.timer_label.config(text=f"Timp rămas: {mins:02}:{secs:02}")
        if self.remaining_seconds > 0:
            self.remaining_seconds -= 1
            self.timer_id = self.after(1000, self.update_timer)
        else:
            self.finish_test(timeout=True)

    def show_question(self):
        self.scroll_frame.scroll_to_top()
        self.feedback_label.config(text="")
        self.answer_btn.config(state='normal')
        self.next_btn.config(state='disabled')
        self.option_widgets = {}

        q = self.questions[self.current_index]
        self.q_label.config(text=q['text'])

        self.img_label.config(image='', text='')
        img_file = q.get('image')
        if img_file:
            path = os.path.join('assets', 'images', img_file)
            if os.path.exists(path):
                pil_img = Image.open(path)
                pil_img.thumbnail((500, 500))
                tk_img = ImageTk.PhotoImage(pil_img)
                self.img_label.image = tk_img
                self.img_label.config(image=tk_img)
            else:
                self.img_label.config(text=f"[Imagine lipsă: {img_file}]")

        for w in self.options_frame.winfo_children():
            w.destroy()

        self.correct_answer = q['correct_answer']
        self.answer_vars = {}
        if isinstance(self.correct_answer, list):
            for k, v in q['options'].items():
                var = tb.BooleanVar()
                cb = tb.Checkbutton(self.options_frame, text=f"{k}. {v}", variable=var, style="Custom.TCheckbutton")
                cb.pack(anchor='w')
                self.answer_vars[k] = var
                self.option_widgets[k] = cb
        else:
            self.single_answer = tb.StringVar()
            for k, v in q['options'].items():
                rb = tb.Radiobutton(self.options_frame, text=f"{k}. {v}", value=k, variable=self.single_answer, style="Custom.TRadiobutton")
                rb.pack(anchor='w')
                self.option_widgets[k] = rb

    def check_answer(self):
        if isinstance(self.correct_answer, list):
            selected = [k for k, v in self.answer_vars.items() if v.get()]
            correct = set(selected) == set(self.correct_answer)
        else:
            selected = self.single_answer.get()
            correct = selected == self.correct_answer

        if correct:
            self.correct_count += 1
            self.feedback_label.config(text="Răspuns corect!", foreground="green")
        else:
            corect = ", ".join(self.correct_answer) if isinstance(self.correct_answer, list) else self.correct_answer
            self.feedback_label.config(text=f"Greșit. Corect: {corect}", foreground="red")

        if isinstance(self.correct_answer, list):
            for k in self.correct_answer:
                if k in self.option_widgets:
                    self.option_widgets[k].config(style="MyCorrect.TCheckbutton")
        else:
            if self.correct_answer in self.option_widgets:
                self.option_widgets[self.correct_answer].config(style="MyCorrect.TRadiobutton")

        if not correct:
            if isinstance(self.correct_answer, list):
                for k in self.correct_answer:
                    if k in self.option_widgets:
                        self.option_widgets[k].config(style="MyWrong.TCheckbutton")
            else:
                if self.correct_answer in self.option_widgets:
                    self.option_widgets[self.correct_answer].config(style="MyWrong.TRadiobutton")

        self.update_score()
        self.answer_btn.config(state='disabled')
        self.next_btn.config(state='normal')
        self.explanation_btn.config(state='normal')

    def next_question(self):
        self.current_index += 1
        if self.current_index < len(self.questions):
            self.show_question()
        else:
            self.finish_test()
        self.update_score()

    def finish_test(self, timeout=False):
        if self.timer_id:
            self.after_cancel(self.timer_id)
        self.q_label.config(text=f"Test finalizat! Scor: {self.correct_count}/{len(self.questions)}")
        self.answer_btn.config(state='disabled')
        self.next_btn.config(state='disabled')
        self.feedback_label.config(
            text="Timpul a expirat!" if timeout else "Ai terminat testul!",
            foreground="blue"
        )
        save_score(self.correct_count, len(self.questions), "test")
        self.update_score()

    def show_explanation(self):
        question = self.questions[self.current_index]
        explanation = question.get("explanation", "(Nu există explicație pentru această întrebare.)")
        ExplanationWindow(self, explanation)
