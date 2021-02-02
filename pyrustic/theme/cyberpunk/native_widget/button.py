from pyrustic import default_style
from pyrustic.theme.cyberpunk import constant


def get_style():
    style = default_style.Button()
    style.font = constant.FONT_FAV_BOLD
    style.background = "#181818"
    style.foreground = "#A098A0"
    style.highlightBackground = "#484048"
    style.highlightColor = "white"
    style.highlightThickness = 1
    style.activeBackground = "white"
    style.relief = "flat"
    style.padY = 0
    style.activeBackground = "#202020"
    style.activeForeground = "#D0C8D0"
    style.cursor = "hand1"
    return style

"""
def get_style():
    style = default_style.Button()
    style.font = constant.FONT_FAV_BOLD
    style.foreground = "#CFCFCF"
    style.background = constant.COLOR_BLACK
    style.highlightBackground = "#CFCFCF"
    style.activeBackground = "white"
    style.activeForeground = constant.COLOR_BLACK
    return style
"""