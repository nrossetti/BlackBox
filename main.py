import tkinter as tk
from tkinter import simpledialog
from PIL import Image
import pystray
from pystray import MenuItem as item, Menu as menu
import threading
import sys, os

color_names = {
    '#000000': 'Black',
    '#FFFFFF': 'White',
    '#00FF00': 'Green',
    '#0000FF': 'Blue',
}
current_color_hex = '#000000'
window_visible = False

def create_image():
    if getattr(sys, 'frozen', False):
        icon_folder = os.path.join(sys._MEIPASS, 'static')
    else:
        icon_folder = 'static'

    image_path = os.path.join(icon_folder, "bb_sys.png")
    return Image.open(image_path)

def apply_color(color_hex):
    try:
        root.configure(background=color_hex)
        global current_color_hex
        current_color_hex = color_hex
        update_tray_icon()
    except tk.TclError:
        print(f"Invalid color: {color_hex}")

def prompt_for_custom_color():
    color = simpledialog.askstring("Input Color", "Enter color (hex, e.g., #rrggbb, or RGB, e.g., 255,255,255):", parent=root)
    if color:
        apply_color(color)

def toggle_window_visibility(icon=None, item=None):
    global window_visible
    if window_visible:
        root.withdraw()
    else:
        root.deiconify()
    window_visible = not window_visible
    update_tray_icon()

def quit_program(icon, item):
    icon.stop()
    root.destroy()
    sys.exit()

def show_custom_color_menu(icon=None, item=None):
    root.after(0, prompt_for_custom_color)

def get_color_item_text(color_hex):
    color_name = [name for hex, name in color_names.items() if hex == color_hex][0] if color_hex in color_names else 'Custom'
    return f"{color_name} {'✓' if current_color_hex == color_hex else ''}"

def create_tray_icon():
    global tray_icon
    tray_icon = pystray.Icon("AppIcon", create_image(), menu=menu(
        item(lambda text: 'Hide' if window_visible else 'Show', toggle_window_visibility),
        item('Color', menu(
            item(lambda text: get_color_item_text('#000000'), lambda icon, item: apply_color('#000000')),
            item(lambda text: get_color_item_text('#FFFFFF'), lambda icon, item: apply_color('#FFFFFF')),
            item(lambda text: get_color_item_text('#00FF00'), lambda icon, item: apply_color('#00FF00')),
            item(lambda text: get_color_item_text('#0000FF'), lambda icon, item: apply_color('#0000FF')),
            item('Custom...', show_custom_color_menu))),
        item('Quit', quit_program)
    ))
    tray_icon.run()

def update_tray_icon():
    if tray_icon:
        tray_icon.update_menu()

root = tk.Tk()
root.overrideredirect(True)
root.geometry("400x400+100+100")
root.configure(background=current_color_hex)
root.attributes("-topmost", True)

resize_direction = ""

def on_press(event):
    global offsetX, offsetY, resize_direction
    offsetX, offsetY = event.x, event.y
    resize_direction = ""
    if event.x < 10:
        resize_direction += "W"
    elif event.x > root.winfo_width() - 10:
        resize_direction += "E"
    if event.y < 10:
        resize_direction += "N"
    elif event.y > root.winfo_height() - 10:
        resize_direction += "S"

def on_drag(event):
    global offsetX, offsetY, resize_direction
    x, y = root.winfo_x(), root.winfo_y()
    w, h = root.winfo_width(), root.winfo_height()

    if "E" in resize_direction:
        new_w = max(root.winfo_pointerx() - x, 100)
        root.geometry(f"{new_w}x{h}")
    elif "W" in resize_direction:
        new_w = max(x + w - root.winfo_pointerx(), 100)
        root.geometry(f"{new_w}x{h}+{root.winfo_pointerx()}+{y}")
    if "S" in resize_direction:
        new_h = max(root.winfo_pointery() - y, 100)
        root.geometry(f"{w}x{new_h}")
    elif "N" in resize_direction:
        new_h = max(y + h - root.winfo_pointery(), 100)
        root.geometry(f"{w}x{new_h}+{x}+{root.winfo_pointery()}")

    if resize_direction == "":
        deltaX = event.x_root - offsetX
        deltaY = event.y_root - offsetY
        root.geometry(f"+{deltaX}+{deltaY}")

def update_cursor(event):
    border = 10
    cursor = "arrow"
    if event.x < border or event.x > root.winfo_width() - border:
        cursor = "sb_h_double_arrow"
    if event.y < border or event.y > root.winfo_height() - border:
        cursor = "sb_v_double_arrow"
    if (event.x < border and event.y < border) or (event.x > root.winfo_width() - border and event.y > root.winfo_height() - border):
        cursor = "fleur"
    root.config(cursor=cursor)

root.bind("<Button-1>", on_press)
root.bind("<B1-Motion>", on_drag)
root.bind("<Motion>", update_cursor)

root.withdraw()
window_visible = False
threading.Thread(target=create_tray_icon, daemon=True).start()

root.mainloop()
