from ui.main_window import MainWindow
from ui.style_utils import apply_custom_styles
import ttkbootstrap as tb
from PIL import Image, ImageTk
import tkinter as tk
from ui.style_utils import apply_custom_styles
from core.constants import WINDOW_WIDTH_RATIO, WINDOW_HEIGHT_RATIO, WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT

def main():
    app = tb.Window(themename="flatly")
    app.title("Mediu de Învățare și Testare")

    screen_width = app.winfo_screenwidth()
    screen_height = app.winfo_screenheight()
    width = int(screen_width * WINDOW_WIDTH_RATIO)
    height = int(screen_height * WINDOW_HEIGHT_RATIO)
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    app.geometry(f"{width}x{height}+{x}+{y}")
    app.resizable(True, True)
    app.minsize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)

    apply_custom_styles(app.style)

    icon_path = "assets/images/logo_32x32.png"
    icon_image = Image.open(icon_path)
    icon_tk = ImageTk.PhotoImage(icon_image)
    app.iconphoto(False, icon_tk)

    window = MainWindow(app)
    app.mainloop()

if __name__ == '__main__':
    main()
