from ui.main_window import MainWindow
from ui.style_utils import apply_custom_styles
import ttkbootstrap as tb

def main():
    app = tb.Window(themename="flatly")
    app.title("Mediu de Învățare și Testare")

    screen_width = app.winfo_screenwidth()
    screen_height = app.winfo_screenheight()
    width = int(screen_width * 0.8)
    height = int(screen_height * 0.8)
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    app.geometry(f"{width}x{height}+{x}+{y}")
    app.resizable(True, True)

    apply_custom_styles(app.style)

    window = MainWindow(app)
    app.mainloop()

if __name__ == '__main__':
    main()
