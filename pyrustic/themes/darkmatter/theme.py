from pyrustic.theme import Theme
from pyrustic.themes.darkmatter.native_widget import button
from pyrustic.themes.darkmatter.native_widget import canvas
from pyrustic.themes.darkmatter.native_widget import checkbutton
from pyrustic.themes.darkmatter.native_widget import entry
from pyrustic.themes.darkmatter.native_widget import frame
from pyrustic.themes.darkmatter.native_widget import label
from pyrustic.themes.darkmatter.native_widget import label_frame
from pyrustic.themes.darkmatter.native_widget import listbox
from pyrustic.themes.darkmatter.native_widget import menu
from pyrustic.themes.darkmatter.native_widget import menubutton
from pyrustic.themes.darkmatter.native_widget import paned_window
from pyrustic.themes.darkmatter.native_widget import radiobutton
from pyrustic.themes.darkmatter.native_widget import scale
from pyrustic.themes.darkmatter.native_widget import scrollbar
from pyrustic.themes.darkmatter.native_widget import spinbox
from pyrustic.themes.darkmatter.native_widget import text
from pyrustic.themes.darkmatter.native_widget import toplevel
from pyrustic.themes.darkmatter.pyrustic_widget import choice
from pyrustic.themes.darkmatter.pyrustic_widget import confirm
from pyrustic.themes.darkmatter.pyrustic_widget import scrollbox
from pyrustic.themes.darkmatter.pyrustic_widget import spinner
from pyrustic.themes.darkmatter.pyrustic_widget import table
from pyrustic.themes.darkmatter.pyrustic_widget import toast
from pyrustic.themes.darkmatter.pyrustic_widget import tree


def get_theme():
    """
    Darkmatter Theme
    """
    theme = Theme()
    _add_native_widget(theme)
    _add_pyrustic_widget(theme)
    return theme


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
