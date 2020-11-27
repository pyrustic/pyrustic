import tkinter as tk


class EnhanceTk:
    """ Ctrl-a in an Entry or Text doesn't make a text selection by default.
        Now it's possible ! Enjoy ! """

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
