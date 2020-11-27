from pyrustic.theme import Theme
from pyrustic.themes.darkmatter.native_widget import toplevel
from pyrustic.themes.darkmatter.native_widget import label
from pyrustic.themes.darkmatter.native_widget import text
from pyrustic.themes.darkmatter import constant


# == confirm theme
def get_theme():
    theme = Theme()
    theme.add_style(_get_confirm_toplevel_style(), scope="*Confirm.")
    theme.add_style(_get_confirm_label_header_style(), scope="*Confirm*header*")
    theme.add_style(_get_confirm_label_message_style(), scope="*Confirm*message*")
    theme.add_style(_get_confirm_text_message_style(), scope="*Confirm*long_message*")
    return theme


# ========================================
#                PRIVATE
# ========================================
# confirm toplevel
def _get_confirm_toplevel_style():
    style = toplevel.get_style()
    return style


# confirm header label
def _get_confirm_label_header_style():
    style = label.get_style()
    style.font = constant.FONT_FAV_BOLD
    return style


# confirm message label
def _get_confirm_label_message_style():
    style = label.get_style()
    return style


# confirm message text
def _get_confirm_text_message_style():
    style = text.get_style()
    style.highlightThickness = 0
    style.foreground = "#C8C8C8"
    style.background = constant.COLOR_BLACK
    return style
