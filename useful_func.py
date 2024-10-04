#import pygetwindow as gw
from PIL import ImageTk, Image



def open_img(path,size):
    return ImageTk.PhotoImage( Image.open(path).resize(size, Image.ADAPTIVE))

def centerw(window,app_w,app_h):    
    pantall_ancho = window.winfo_screenwidth()
    pantall_largo = window.winfo_screenheight()
    x = int((pantall_ancho/2) - (app_w/2))
    y = int((pantall_largo/2) - (app_h/2))
    return window.geometry(f"{app_w}x{app_h}+{x}+{y}")


def clear_frame(frame):
    # Iterate through every widget inside the frame
    for widget in frame.winfo_children():
        widget.destroy()  
