from pyrustic.themes.darkmatter.native_widget import label
from pyrustic.themes.darkmatter.native_widget import toplevel
from pyrustic.themes.darkmatter import constant
from pyrustic.theme import Theme


# == toast theme
def get_theme():
    theme = Theme()
    theme.add_style(toplevel.get_style(), scope="*Toast.")
    theme.add_style(_get_toast_header_label_style(), scope="*Toast*header*")
    theme.add_style(_get_toast_message_label_style(), scope="*Toast*message*")
    return theme


# ========================================
#                PRIVATE
# ========================================
# toast toplevel
def _get_toast_toplevel_style():
    style = toplevel.get_style()
    return style


# toast header
def _get_toast_header_label_style():
    style = label.get_style()
    style.font = constant.FONT_FAV_BOLD
    return style


# toast message
def _get_toast_message_label_style():
    style = label.get_style()
    style.foreground = "#C8C8C8"
    style.background = constant.COLOR_BLACK
    return style
