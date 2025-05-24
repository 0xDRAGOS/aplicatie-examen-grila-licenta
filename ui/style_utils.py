import ttkbootstrap as tb

_styles_applied = False

def apply_custom_styles(style: tb.Style):
    global _styles_applied
    if _styles_applied:
        return

    try:
        style.configure("MyCorrect.TCheckbutton", background="#d4edda", font=("Segoe UI Symbol", 14))
        style.configure("MyWrong.TCheckbutton", background="#f8d7da", font=("Segoe UI Symbol", 14))
        style.configure("MyCorrect.TRadiobutton", background="#d4edda", font=("Segoe UI Symbol", 14))
        style.configure("MyWrong.TRadiobutton", background="#f8d7da", font=("Segoe UI Symbol", 14))
        style.configure("Custom.TCheckbutton", font=("Segoe UI Symbol", 13))
        style.configure("Custom.TRadiobutton", font=("Segoe UI Symbol", 13))
        _styles_applied = True
    except Exception as e:
        print("Eroare la definirea stilurilor:", e)
