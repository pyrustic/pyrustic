from pyrustic import default_style
from pyrustic.themes.darkmatter import constant


def get_style():
    style = default_style.Button()
    style.font = constant.FONT_FAV_BOLD
    style.foreground = "#CFCFCF"
    style.background = constant.COLOR_BLACK
    style.highlightBackground = "#CFCFCF"
    style.activeBackground = "white"
    style.activeForeground = constant.COLOR_BLACK
    return style
