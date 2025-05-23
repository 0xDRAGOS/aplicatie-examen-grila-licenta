import ttkbootstrap as tb

def apply_custom_styles(style: tb.Style):
    style.configure("MyCorrect.TCheckbutton", background="#d4edda")
    style.configure("MyWrong.TCheckbutton", background="#f8d7da")
    style.configure("MyCorrect.TRadiobutton", background="#d4edda")
    style.configure("MyWrong.TRadiobutton", background="#f8d7da")
