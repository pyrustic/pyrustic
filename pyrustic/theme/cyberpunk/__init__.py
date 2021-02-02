from pyrustic.theme import Theme
from pyrustic.theme.cyberpunk.native_widget import button
from pyrustic.theme.cyberpunk.native_widget import canvas
from pyrustic.theme.cyberpunk.native_widget import checkbutton
from pyrustic.theme.cyberpunk.native_widget import entry
from pyrustic.theme.cyberpunk.native_widget import frame
from pyrustic.theme.cyberpunk.native_widget import label
from pyrustic.theme.cyberpunk.native_widget import label_frame
from pyrustic.theme.cyberpunk.native_widget import listbox
from pyrustic.theme.cyberpunk.native_widget import menu
from pyrustic.theme.cyberpunk.native_widget import menubutton
from pyrustic.theme.cyberpunk.native_widget import paned_window
from pyrustic.theme.cyberpunk.native_widget import radiobutton
from pyrustic.theme.cyberpunk.native_widget import scale
from pyrustic.theme.cyberpunk.native_widget import scrollbar
from pyrustic.theme.cyberpunk.native_widget import spinbox
from pyrustic.theme.cyberpunk.native_widget import text
from pyrustic.theme.cyberpunk.native_widget import toplevel
from pyrustic.theme.cyberpunk.pyrustic_widget import choice
from pyrustic.theme.cyberpunk.pyrustic_widget import confirm
from pyrustic.theme.cyberpunk.pyrustic_widget import scrollbox
from pyrustic.theme.cyberpunk.pyrustic_widget import spinner
from pyrustic.theme.cyberpunk.pyrustic_widget import table
from pyrustic.theme.cyberpunk.pyrustic_widget import toast
from pyrustic.theme.cyberpunk.pyrustic_widget import tree


class Cyberpunk(Theme):
    def __init__(self):
        super().__init__()
        _add_native_widget(self)
        _add_pyrustic_widget(self)


def _add_native_widget(theme):
    elements = (button, canvas, checkbutton, entry,
                frame, label, label_frame, listbox,
                menu, menubutton, paned_window, radiobutton,
                scale, scrollbar, spinbox, text, toplevel)
    for element in elements:
        theme.add_style(element.get_style())


def _add_pyrustic_widget(theme):
    elements = (choice, confirm, scrollbox, spinner, table,
                toast, tree)
    for element in elements:
        theme.add_theme(element.get_theme())
