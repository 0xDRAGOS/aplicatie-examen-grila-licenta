import json
import random
import os
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk


class ScrollableFrame(ttk.Frame):
    def __init__(self, container, **kwargs):
        super().__init__(container, **kwargs)
        try:
            parent_bg = container.master.cget('background')
        except Exception:
            parent_bg = '#f0f2f5'

        canvas = tk.Canvas(self, bg=parent_bg, highlightthickness=0)
        v_scroll = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        h_scroll = ttk.Scrollbar(self, orient="horizontal", command=canvas.xview)

        self.scrollable_frame = ttk.Frame(canvas, style='TFrame')

        def on_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        self.scrollable_frame.bind("<Configure>", on_configure)

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)

        canvas.grid(row=0, column=0, sticky="nsew")
        v_scroll.grid(row=0, column=1, sticky="ns")
        h_scroll.grid(row=1, column=0, sticky="ew")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)


class LearningApp(tk.Tk):
    def __init__(self, json_path):
        super().__init__()
        self.title("Mediu de Invatare si Testare")
        self.geometry("1280x720")
        self.configure(bg="#f0f2f5")

        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure('TButton', font=('Helvetica', 11), padding=8)
        style.configure('TLabel', font=('Helvetica', 12), background="#f0f2f5")
        style.configure('Header.TLabel', font=('Helvetica', 14, 'bold'))
        style.configure('Score.TLabel', font=('Helvetica', 12, 'bold'), foreground="#333")
        style.configure('Feedback.TLabel', font=('Helvetica', 11), foreground="#00529B")
        style.configure('TFrame', background="#f0f2f5")
        style.configure('Wrong.TRadiobutton', background='red')
        style.configure('Wrong.TCheckbutton', background='red')
        style.configure('Correct.TRadiobutton', background='green')
        style.configure('Correct.TCheckbutton', background='green')

        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        self.subjects = data.get('subjects', [])

        self.mode = 'study'
        self.study_questions = []
        self.study_index = 0
        self.study_correct_count = 0

        self.test_questions = []
        self.test_index = 0
        self.test_correct_count = 0

        self.create_mode_selector()
        self.create_subject_selector()
        self.create_flashcard_panel()
        self.create_test_panel()
        self.show_study_mode()

    def create_mode_selector(self):
        frame = ttk.Frame(self, style='TFrame')
        frame.pack(pady=10)
        ttk.Button(frame, text="Mod Invatare", command=self.show_study_mode).pack(side=tk.LEFT, padx=10)
        ttk.Button(frame, text="Mod Test (30 grile)", command=self.start_test).pack(side=tk.LEFT, padx=10)

    def create_subject_selector(self):
        self.subject_frame = ttk.Frame(self, style='TFrame')
        self.subject_frame.pack(pady=10)
        ttk.Label(self.subject_frame, text="Selecteaza materia:", style='Header.TLabel').pack(side=tk.LEFT)
        self.subject_var = tk.StringVar()
        names = [s.get('name') for s in self.subjects]
        combo = ttk.Combobox(self.subject_frame, values=names, textvariable=self.subject_var, state="readonly",
                             font=('Helvetica', 11))
        combo.pack(side=tk.LEFT, padx=10)
        combo.bind("<<ComboboxSelected>>", self.on_subject_selected)

    def create_flashcard_panel(self):
        self.card_frame = ttk.Frame(self, style='TFrame', relief=tk.RIDGE, padding=20)
        self.card_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        self.study_score_label = ttk.Label(self.card_frame, text="Progres: 0/0", style='Score.TLabel')
        self.study_score_label.pack(anchor=tk.E)

        self.study_scroll = ScrollableFrame(self.card_frame)
        self.study_scroll.pack(fill=tk.BOTH, expand=True)

        self.q_label = ttk.Label(
            self.study_scroll.scrollable_frame,
            text="", wraplength=1400, justify=tk.LEFT, style='Header.TLabel'
        )
        self.q_label.pack(pady=(10, 15), anchor=tk.W)

        self.study_image_label = ttk.Label(self.study_scroll.scrollable_frame)
        self.study_image_label.pack(pady=(0, 10), anchor=tk.W)

        self.study_options_frame = ttk.Frame(self.study_scroll.scrollable_frame, style='TFrame')
        self.study_options_frame.pack(pady=(0, 10), anchor=tk.W)

        btn_frame = ttk.Frame(self.card_frame, style='TFrame')
        btn_frame.pack(pady=10)
        self.study_respond_btn = ttk.Button(btn_frame, text="Raspunde", command=self.evaluate_study)
        self.study_respond_btn.pack(side=tk.LEFT, padx=10)
        self.study_next_btn = ttk.Button(btn_frame, text="Urmatoarea", command=self.next_study_question, state=tk.DISABLED)
        self.study_next_btn.pack(side=tk.LEFT, padx=10)

        self.study_feedback_label = ttk.Label(
            self.study_scroll.scrollable_frame,
            text="",
            wraplength=1400,
            justify=tk.LEFT,
            style='Feedback.TLabel'
        )
        self.study_feedback_label.pack(pady=(10, 0), anchor=tk.W)

    def create_test_panel(self):
        self.test_frame = ttk.Frame(self, style='TFrame', relief=tk.RIDGE, padding=20)

        self.test_score_label = ttk.Label(self.test_frame, text="Scor: 0/0", style='Score.TLabel')
        self.test_score_label.pack(anchor=tk.E)

        self.test_scroll = ScrollableFrame(self.test_frame)
        self.test_scroll.pack(fill=tk.BOTH, expand=True)

        self.test_q_label = ttk.Label(
            self.test_scroll.scrollable_frame,
            text="", wraplength=1400, justify=tk.LEFT, style='Header.TLabel'
        )
        self.test_q_label.pack(pady=(10, 15), anchor=tk.W)

        self.test_image_label = ttk.Label(self.test_scroll.scrollable_frame)
        self.test_image_label.pack(pady=(0, 10), anchor=tk.W)

        self.test_options_frame = ttk.Frame(self.test_scroll.scrollable_frame, style='TFrame')
        self.test_options_frame.pack(pady=(0, 10), anchor=tk.W)

        btn_frame = ttk.Frame(self.test_frame, style='TFrame')
        btn_frame.pack(pady=10)
        self.test_respond_btn = ttk.Button(btn_frame, text="Raspunde", command=self.evaluate_test)
        self.test_respond_btn.pack(side=tk.LEFT, padx=10)
        self.test_next_btn = ttk.Button(btn_frame, text="Urmatoarea", command=self.next_test_question, state=tk.DISABLED)
        self.test_next_btn.pack(side=tk.LEFT, padx=10)

        self.test_feedback_label = ttk.Label(
            self.test_scroll.scrollable_frame,
            text="",
            wraplength=1400,
            justify=tk.LEFT,
            style='Feedback.TLabel'
        )
        self.test_feedback_label.pack(pady=(10, 0), anchor=tk.W)

    def show_study_mode(self):
        self.mode = 'study'
        self.test_frame.pack_forget()
        self.subject_frame.pack()
        self.card_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

    def on_subject_selected(self, event=None):
        name = self.subject_var.get()
        for sub in self.subjects:
            if sub.get('name') == name:
                self.study_questions = sub.get('questions', [])
                break
        self.study_index = 0
        self.study_correct_count = 0
        total = len(self.study_questions)
        self.study_score_label.config(text=f"Progres: 0/{total}")
        self.show_study_question()

    def show_study_question(self):
        self.study_feedback_label.config(text="")
        self.study_respond_btn.state(["!disabled"])
        self.study_next_btn.state(["disabled"])
        q = self.study_questions[self.study_index]

        self.study_image_label.config(image='', text='')
        img_file = q.get('image')
        if img_file:
            path = os.path.join('assets', 'images', img_file)
            if os.path.exists(path):
                pil_img = Image.open(path)
                pil_img.thumbnail((600, 600), Image.Resampling.LANCZOS)
                tk_img = ImageTk.PhotoImage(pil_img)
                self.study_image_label.image = tk_img
                self.study_image_label.config(image=tk_img)
            else:
                self.study_image_label.config(text=f"[Imagine lipsa: {img_file}]")

        self.q_label.config(text=f"{self.study_index + 1}. {q.get('text')}")

        for w in self.study_options_frame.winfo_children():
            w.destroy()
        ans = q.get('correct_answer')
        self.study_widgets = {}
        if isinstance(ans, list):
            self.study_vars = {}
            for opt, txt in q.get('options', {}).items():
                var = tk.BooleanVar()
                cb = ttk.Checkbutton(
                    self.study_options_frame,
                    text=f"{opt}. {txt}",
                    variable=var,
                    style='TCheckbutton'
                )
                cb.pack(anchor=tk.W, pady=2)
                self.study_vars[opt] = var
                self.study_widgets[opt] = cb
        else:
            self.study_var = tk.StringVar()
            for opt, txt in q.get('options', {}).items():
                rb = ttk.Radiobutton(
                    self.study_options_frame,
                    text=f"{opt}. {txt}",
                    value=opt,
                    variable=self.study_var,
                    style='TRadiobutton'
                )
                rb.pack(anchor=tk.W, pady=2)
                self.study_widgets[opt] = rb

    def evaluate_study(self):
        q = self.study_questions[self.study_index]
        ans = q.get('correct_answer')
        selected = ([opt for opt, var in self.study_vars.items() if var.get()]
                    if isinstance(ans, list) else self.study_var.get())
        is_correct = (set(ans) == set(selected)) if isinstance(ans, list) else (ans == selected)

        if is_correct:
            for opt in (ans if isinstance(ans, list) else [ans]):
                w = self.study_widgets.get(opt)
                if w:
                    style_name = 'Correct.TCheckbutton' if isinstance(ans, list) else 'Correct.TRadiobutton'
                    w.configure(style=style_name)
            self.study_correct_count += 1
            feedback = "Raspuns corect!"
        else:
            for opt in (ans if isinstance(ans, list) else [ans]):
                w = self.study_widgets.get(opt)
                if w:
                    style_name = 'Wrong.TCheckbutton' if isinstance(ans, list) else 'Wrong.TRadiobutton'
                    w.configure(style=style_name)
            feedback = f"Raspuns corect: {', '.join(ans) if isinstance(ans, list) else ans}"

        total = len(self.study_questions)
        self.study_feedback_label.config(text=feedback)
        self.study_score_label.config(text=f"Progres: {self.study_correct_count}/{total}")
        self.study_respond_btn.state(["disabled"])
        self.study_next_btn.state(["!disabled"])

    def next_study_question(self):
        self.study_index += 1
        if self.study_index < len(self.study_questions):
            self.show_study_question()
        else:
            messagebox.showinfo("Sfarsit Studiu", f"Ai parcurs toate intrebarile! Scor: {self.study_correct_count}/{len(self.study_questions)}")
            self.show_study_mode()

    def start_test(self):
        all_q = [q for sub in self.subjects for q in sub.get('questions', [])]
        count = min(30, len(all_q))
        self.test_questions = random.sample(all_q, count)
        self.test_index = 0
        self.test_correct_count = 0
        total = len(self.test_questions)
        self.test_score_label.config(text=f"Scor: 0/{total}")
        self.card_frame.pack_forget()
        self.subject_frame.pack_forget()
        self.mode = 'test'
        self.test_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        self.show_test_question()

    def show_test_question(self):
        self.test_feedback_label.config(text="")
        self.test_respond_btn.state(["!disabled"])
        self.test_next_btn.state(["disabled"])
        q = self.test_questions[self.test_index]

        self.test_image_label.config(image='', text='')
        img_file = q.get('image')
        if img_file:
            path = os.path.join('assets', 'images', img_file)
            if os.path.exists(path):
                pil_img = Image.open(path)
                pil_img.thumbnail((600, 600), Image.Resampling.LANCZOS)
                tk_img = ImageTk.PhotoImage(pil_img)
                self.test_image_label.image = tk_img
                self.test_image_label.config(image=tk_img)
            else:
                self.test_image_label.config(text=f"[Imagine lipsa: {img_file}]")

        self.test_q_label.config(text=f"{self.test_index + 1}. {q.get('text')}")

        for w in self.test_options_frame.winfo_children():
            w.destroy()
        ans = q.get('correct_answer')
        self.test_widgets = {}
        if isinstance(ans, list):
            self.test_vars = {}
            for opt, txt in q.get('options', {}).items():
                var = tk.BooleanVar()
                cb = ttk.Checkbutton(
                    self.test_options_frame,
                    text=f"{opt}. {txt}",
                    variable=var,
                    style='TCheckbutton'
                )
                cb.pack(anchor=tk.W, pady=2)
                self.test_vars[opt] = var
                self.test_widgets[opt] = cb
        else:
            self.test_var = tk.StringVar()
            for opt, txt in q.get('options', {}).items():
                rb = ttk.Radiobutton(
                    self.test_options_frame,
                    text=f"{opt}. {txt}",
                    value=opt,
                    variable=self.test_var,
                    style='TRadiobutton'
                )
                rb.pack(anchor=tk.W, pady=2)
                self.test_widgets[opt] = rb

    def evaluate_test(self):
        q = self.test_questions[self.test_index]
        ans = q.get('correct_answer')
        selected = ([opt for opt, var in self.test_vars.items() if var.get()]
                    if isinstance(ans, list) else self.test_var.get())
        is_correct = (set(ans) == set(selected)) if isinstance(ans, list) else (ans == selected)

        if is_correct:
            for opt in (ans if isinstance(ans, list) else [ans]):
                w = self.test_widgets.get(opt)
                if w:
                    style_name = 'Correct.TCheckbutton' if isinstance(ans, list) else 'Correct.TRadiobutton'
                    w.configure(style=style_name)
            self.test_correct_count += 1
            feedback = "Raspuns corect!"
        else:
            for opt in (ans if isinstance(ans, list) else [ans]):
                w = self.test_widgets.get(opt)
                if w:
                    style_name = 'Wrong.TCheckbutton' if isinstance(ans, list) else 'Wrong.TRadiobutton'
                    w.configure(style=style_name)
            feedback = f"Raspuns corect: {', '.join(ans) if isinstance(ans, list) else ans}"

        total = len(self.test_questions)
        self.test_feedback_label.config(text=feedback)
        self.test_score_label.config(text=f"Scor: {self.test_correct_count}/{total}")
        self.test_respond_btn.state(["disabled"])
        self.test_next_btn.state(["!disabled"])

    def next_test_question(self):
        self.test_index += 1
        if self.test_index < len(self.test_questions):
            self.show_test_question()
        else:
            messagebox.showinfo("Final Test", f"Test incheiat! Scorul final: {self.test_correct_count}/{len(self.test_questions)}")
            self.show_study_mode()


if __name__ == '__main__':
    app = LearningApp('assets/grile.json')
    app.mainloop()
