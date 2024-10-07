#import pillow for images loading
from PIL import ImageTk, Image



def open_img(path,size):
    """
    Function to load an image in a specific size
    path: path where the image is located
    size:  desired size
    """
    return ImageTk.PhotoImage( Image.open(path).resize(size, Image.ADAPTIVE))

def centerw(window,app_w,app_h):   
    """
    Function for centering the window and setting a specific size
    window: window to center
    app_w: desired width
    app_h: desired heigth
    """ 
    pantall_ancho = window.winfo_screenwidth()
    pantall_largo = window.winfo_screenheight()
    x = int((pantall_ancho/2) - (app_w/2))
    y = int((pantall_largo/2) - (app_h/2))
    return window.geometry(f"{app_w}x{app_h}+{x}+{y}")


def clear_frame(frame):
    """
    Function to clear a specific frame
    frame: frame to be cleared
    """
    # Iterate through every widget inside the frame
    for widget in frame.winfo_children():
        widget.destroy()  #destroy all widgets
