import tkinter as tk


def handle_on_destroy(widget, callback):
    if isinstance(widget, tk.Toplevel):
        command = (lambda event, widget=widget, callback=callback:
                   callback() if event.widget is widget else None)
        widget.bind("<Destroy>", command, "+")
    else:
        widget.bind("<Destroy>", lambda event: callback(), "+")


def old_center_window(window):
    reqwidth = window.winfo_reqwidth()
    reqheight = window.winfo_reqheight()
    x = (window.winfo_screenwidth() // 2) - (reqwidth // 2)
    y = (window.winfo_screenheight() // 2) - (reqheight // 2)
    window.geometry("{}x{}+{}+{}".format(reqwidth, reqheight, x, y))


def center_window(window, within=None):
    width = window.winfo_width()
    height = window.winfo_height()
    if within is None:
        x = (window.winfo_screenwidth() // 2) - (width // 2)
        y = (window.winfo_screenheight() // 2) - (height // 2)
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
    window.geometry("{}x{}+{}+{}".format(width, height, x, y))


def dialog_effect(window):
    window.transient(window.master)
    window.lift()
    window.grab_set()
    window.focus_set()


def formal_geometry(window):
    # data: width, x, height, +-, X, +-, Y
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    data = split_geometry(window.geometry())
    width = data[0]
    height = data[2]
    coord_x = data[4]
    coord_y = data[6]
    if data[3] == "-":
        coord_x = screen_width - width - coord_x
    if data[5] == "-":
        coord_y = screen_height - height - coord_y
    return width, height, coord_x, coord_y


def split_geometry(val):
    data = []
    cache = ""
    for char in val:
        if char in ("x", "+", "-"):
            if char == "-" and data[len(data)-1] in ("+", "-"):
                cache += char
            else:
                data.append(int(cache))
                data.append(char)
                cache = ""
        else:
            cache += char
    data.append(int(cache))
    return data


class EnhanceTk:
    """ Ctrl-a in an Entry or Text doesn't make a text selection by default.
        Now it's possible ! Enjoy !

        DON'T USE THIS CLASS ! ALREADY USED BY APP """

    def __init__(self, root_tk):
        root_tk.bind_class("Entry", "<Control-a>", self._select_all_in_entry, "+")
        root_tk.bind_class("Text", "<Control-a>", self._select_all_in_text, "+")

    def _select_all_in_entry(self, event):
        widget = event.widget
        widget.focus()
        widget.select_range(0, tk.END)
        widget.icursor(tk.END)

    def _select_all_in_text(self, event):
        widget = event.widget
        widget.tag_add(tk.SEL, "1.0", tk.END)
