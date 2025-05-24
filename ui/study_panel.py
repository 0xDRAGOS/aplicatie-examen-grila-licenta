import os
import ttkbootstrap as tb
from tkinter import ttk
from PIL import Image, ImageTk
from ui.scrollable_frame import ScrollableFrame


class StudyPanel(tb.Frame):
    def __init__(self, parent, subjects):
        super().__init__(parent)

        self.subjects = subjects
        self.current_subject = None
        self.current_question_index = 0
        self.correct_count = 0

        self.subject_var = tb.StringVar()
        self.subject_selector = ttk.Combobox(self, textvariable=self.subject_var, state='readonly')
        self.subject_selector['values'] = [s['name'] for s in self.subjects]
        self.subject_selector.pack(pady=10)
        self.subject_selector.bind("<<ComboboxSelected>>", self.on_subject_selected)

        self.progress_label = tb.Label(self, text="Progres: 0/0", font=("Helvetica", 11, "bold"))
        self.progress_label.pack()

        self.scroll_frame = ScrollableFrame(self)
        self.scroll_frame.pack(fill=tb.BOTH, expand=True, pady=10)

        self.question_label = tb.Label(self.scroll_frame.scrollable_frame, text="", wraplength=1000, font=("Segoe UI Symbol", 14, "bold"))
        self.question_label.pack(anchor='w', padx=10, pady=(10, 5))

        self.image_label = tb.Label(self.scroll_frame.scrollable_frame)
        self.image_label.pack(pady=5, anchor='w')

        self.options_frame = tb.Frame(self.scroll_frame.scrollable_frame)
        self.options_frame.pack(anchor='w', padx=10)

        self.feedback_label = tb.Label(self.scroll_frame.scrollable_frame, text="", font=("Helvetica", 11))
        self.feedback_label.pack(pady=5, anchor='w', padx=10)

        self.button_frame = tb.Frame(self)
        self.button_frame.pack(pady=10)
        self.answer_btn = tb.Button(self.button_frame, text="Răspunde", command=self.check_answer)
        self.answer_btn.pack(side='left', padx=5)
        self.next_btn = tb.Button(self.button_frame, text="Următoarea", command=self.next_question, state='disabled')
        self.next_btn.pack(side='left', padx=5)

    def on_subject_selected(self, event=None):
        subject_name = self.subject_var.get()
        for subject in self.subjects:
            if subject['name'] == subject_name:
                self.questions = subject['questions']
                break
        self.current_question_index = 0
        self.correct_count = 0
        self.update_progress()
        self.show_question()

    def show_question(self):
        self.scroll_frame.scroll_to_top()
        self.feedback_label.config(text="")
        self.answer_btn.config(state='normal')
        self.next_btn.config(state='disabled')
        self.option_widgets = {}

        q = self.questions[self.current_question_index]
        self.question_label.config(text=q['text'])

        self.image_label.config(image='', text='')
        img_file = q.get('image')
        if img_file:
            path = os.path.join('assets', 'images', img_file)
            if os.path.exists(path):
                pil_img = Image.open(path)
                pil_img.thumbnail((500, 500))
                tk_img = ImageTk.PhotoImage(pil_img)
                self.image_label.image = tk_img
                self.image_label.config(image=tk_img)
            else:
                self.image_label.config(text=f"[Imagine lipsa: {img_file}]")

        for widget in self.options_frame.winfo_children():
            widget.destroy()

        self.answer_vars = {}
        self.correct_answer = q['correct_answer']
        if isinstance(self.correct_answer, list):
            for key, val in q['options'].items():
                var = tb.BooleanVar()
                cb = ttk.Checkbutton(self.options_frame, text=f"{key}. {val}", variable=var, style="Custom.TCheckbutton")
                cb.pack(anchor='w')
                self.answer_vars[key] = var
                self.option_widgets[key] = cb
        else:
            self.single_answer = tb.StringVar()
            for key, val in q['options'].items():
                rb = tb.Radiobutton(self.options_frame, text=f"{key}. {val}", value=k, variable=self.single_answer, style="Custom.TRadiobutton")
                rb.pack(anchor='w')
                self.option_widgets[key] = rb

        self.update_progress()

    def check_answer(self):
        user_answer = None
        if isinstance(self.correct_answer, list):
            user_answer = [k for k, v in self.answer_vars.items() if v.get()]
            is_correct = set(user_answer) == set(self.correct_answer)
        else:
            user_answer = self.single_answer.get()
            is_correct = user_answer == self.correct_answer

        if is_correct:
            self.feedback_label.config(text="Răspuns corect!", foreground="green")
            self.correct_count += 1
        else:
            answer_text = ', '.join(self.correct_answer) if isinstance(self.correct_answer, list) else self.correct_answer
            self.feedback_label.config(text=f"Răspuns greșit. Corect: {answer_text}", foreground="red")

        if isinstance(self.correct_answer, list):
            for k in self.correct_answer:
                if k in self.option_widgets:
                    self.option_widgets[k].config(style="MyCorrect.TCheckbutton")
        else:
            if self.correct_answer in self.option_widgets:
                self.option_widgets[self.correct_answer].config(style="MyCorrect.TRadiobutton")

        if not is_correct:
            if isinstance(self.correct_answer, list):
                for k in self.correct_answer:
                    if k in self.option_widgets:
                        self.option_widgets[k].config(style="MyWrong.TCheckbutton")
            else:
                if self.correct_answer in self.option_widgets:
                    self.option_widgets[self.correct_answer].config(style="MyWrong.TRadiobutton")

        self.answer_btn.config(state='disabled')
        self.next_btn.config(state='normal')

    def update_progress(self):
        total = len(self.questions) if hasattr(self, 'questions') else 0
        self.progress_label.config(text=f"Progres: {self.current_question_index + 1}/{total}")

    def next_question(self):
        self.current_question_index += 1
        if self.current_question_index < len(self.questions):
            self.show_question()
        else:
            self.feedback_label.config(text=f"🎉 Felicitări! Ai parcurs toate cele {len(self.questions)} întrebări!", foreground="blue")
            self.progress_label.config(text=f"Progres: {len(self.questions)}/{len(self.questions)}")
            self.answer_btn.config(state='disabled')
            self.next_btn.config(state='disabled')
