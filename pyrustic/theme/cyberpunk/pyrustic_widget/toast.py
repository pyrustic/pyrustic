from pyrustic.theme.cyberpunk.native_widget import label
from pyrustic.theme.cyberpunk.native_widget import toplevel
from pyrustic.theme.cyberpunk import constant
from pyrustic.theme import Theme


# == toast theme
def get_theme():
    theme = Theme()
    theme.add_style(_get_toast_toplevel_style(), scope="*Toast*")
    theme.add_style(_get_toast_header_label_style(), scope="*Toast*header*")
    theme.add_style(_get_toast_message_label_style(), scope="*Toast*message*")
    return theme


# ========================================
#                PRIVATE
# ========================================
# toast toplevel
def _get_toast_toplevel_style():
    style = toplevel.get_style()
    style.background = "#101818"
    return style


# toast header
def _get_toast_header_label_style():
    style = label.get_style()
    style.font = constant.FONT_FAV_BOLD
    style.background = "#101818"
    style.foreground = "#B4C7EF"
    return style


# toast message
def _get_toast_message_label_style():
    style = label.get_style()
    style.foreground = "#C8C8C8"
    style.background = "#101818"
    return style
