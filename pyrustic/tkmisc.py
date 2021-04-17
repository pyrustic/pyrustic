import tkinter as tk


def center_window(window, within=None):
    """ Center the window within another window (tk obj) or the screen (None)"""
    window.withdraw()
    window.update_idletasks()
    window.geometry("+0+0")
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    if within is None:
        x = (window.winfo_screenwidth() - width) // 2
        y = (window.winfo_screenheight() - height) // 2
    else:
        if isinstance(within, tk.Tk):
            pass
        elif isinstance(within, tk.Toplevel):
            pass
        else:
            within = within.winfo_toplevel()
        data = formal_geometry(within)
        x = ((data[0] // 2) + data[2]) - (width//2)
        y = ((data[1] // 2) + data[3]) - (height//2)
    if (window.winfo_screenwidth() - x) < width:
        x = window.winfo_screenwidth() - width
    if (window.winfo_screenheight() - y) < height:
        y = window.winfo_screenheight() - height
    window.geometry("+{}+{}".format(x, y))
    window.deiconify()


def align_window(window, under=None):
    window.withdraw()
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    under_x = under.winfo_rootx()
    under_y = under.winfo_rooty()
    x = under_x
    y = under_y + under.winfo_height()
    x = abs(x)
    y = abs(y)
    if window.winfo_screenwidth() - x < width:
        x = window.winfo_screenwidth() - width
    if window.winfo_screenheight() - y < height:
        y = window.winfo_screenheight() - height
    # align
    window.geometry("+{}+{}".format(x, y))
    window.deiconify()


def dialog_effect(window):
    window.transient(window.master)
    window.lift()
    window.grab_set()
    window.focus_set()


def formal_geometry(window):
    width = window.winfo_width()
    height = window.winfo_height()
    coord_x = window.winfo_x()
    coord_y = window.winfo_y()
    return width, height, coord_x, coord_y


def merge_cnfs(main_cnfs, extra_cnfs, components=None):
    main_cnfs = {} if not main_cnfs else main_cnfs
    extra_cnfs = {} if not extra_cnfs else extra_cnfs
    components = {} if not components else components
    cnfs = {}
    # components
    for item in components:
        cnfs[item] = {}
    # parse extra_cnf
    for key, val in extra_cnfs.items():
        cnfs[key] = val
    # parse main_cnf
    for key, val in main_cnfs.items():
        if val is not None:
            cnfs[key] = val
    return cnfs
