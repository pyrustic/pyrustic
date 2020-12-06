from pyrustic.theme import Theme
from pyrustic.themes.darkmatter.native_widget import radiobutton
from pyrustic.themes.darkmatter.native_widget import text
from pyrustic.themes.darkmatter.native_widget import label
from pyrustic.themes.darkmatter.native_widget import frame
from pyrustic.themes.darkmatter import constant


def get_theme():
    theme = Theme()
    theme.add_style(_get_body_style(), scope="*Choice*")
    theme.add_style(_get_radiobutton_style(), scope="*Choice*Radiobutton*")
    theme.add_style(_get_text_style(), scope="*Choice*Text*")
    theme.add_style(_get_header_style(), scope="*Choice*header*")
    return theme


# ========================================
#                PRIVATE
# ========================================


# body
def _get_body_style():
    style = frame.get_style()
    style.foreground = "#C8C8C8"
    style.background = constant.COLOR_BLACK
    style.font = constant.FONT_FAV_NORMAL
    #style.activeBackground = constant.COLOR_BLACK
    #style.activeForeground = "#C8C8C8"
    return style


# radiobuttons
def _get_radiobutton_style():
    style = radiobutton.get_style()
    style.foreground = "#C8C8C8"
    style.background = constant.COLOR_BLACK
    style.font = constant.FONT_FAV_NORMAL
    style.activeBackground = constant.COLOR_BLACK
    style.activeForeground = "#C8C8C8"
    style.selectColor = constant.COLOR_BLACK
    style.relief = "flat"
    style.highlightThickness = 0
    return style

# header
def _get_header_style():
    style = label.get_style()
    style.font = constant.FONT_FAV_BOLD
    return style

# text
def _get_text_style():
    style = text.get_style()
    style.highlightThickness = 0
    return style
