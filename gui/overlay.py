import tkinter as tk
import screeninfo

def calculate_bounding_box(scale):
    """Calculate the parameters of a bounding box at the center of the main monitor.

    Args:
        scale (float): Scaling factor for the size of the bounding box

    Returns:
        sleft (int): The horizontal coordinate of the top-left corner of the bounding box
        stop (int): The vertical coordinate of the top-left corner of the bounding box
        box_width (int): The width of the bounding box
        box_height (int): The height of the bounding box
    """
    monitor = screeninfo.get_monitors()[0]
    sleft = monitor.width // 2 - (monitor.width * scale) // 2
    stop = monitor.height // 2 - (monitor.height * scale) // 2
    box_width = monitor.width * scale
    box_height = monitor.height * scale
    return sleft, stop, box_width, box_height

def create_tinker_window(sleft, stop, box_width, box_height, border_thickness):
    """Create a tkinter window that draws a green bounding box given the arguments.

    Args:
        sleft (int): The horizontal coordinate of the top-left corner of the bounding box
        stop (int): The vertical coordinate of the top-left corner of the bounding box
        box_width (int): The width of the bounding box
        box_height (int): The height of the bounding box
        border_thickness (int): The thickness of the border of the bounding box

    Returns:
        root (tkinter.Tk): The tkinter window object
    """
    root = tk.Tk()
    root.overrideredirect(True)
    root.geometry(f"{int(box_width)}x{int(box_height)}+{int(sleft)}+{int(stop)}")
    root.lift()
    root.wm_attributes("-topmost", True)
    root.wm_attributes("-disabled", True)
    root.wm_attributes("-transparentcolor", "white")
    canvas = tk.Canvas(root, width=box_width, height=box_height, bg='white', highlightthickness=0)
    canvas.pack()
    canvas.create_rectangle(0, 0, box_width - 1, box_height - 1, outline="green", width=border_thickness)
    return root
