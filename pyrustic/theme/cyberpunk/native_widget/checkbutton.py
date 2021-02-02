from pyrustic import default_style
from pyrustic.theme.cyberpunk import constant


def get_style():
    style = default_style.Checkbutton()
    style.background = constant.COLOR_BLACK
    style.foreground = "#CFCFCF"
    style.font = constant.FONT_FAV_NORMAL
    style.highlightThickness = 0
    style.selectColor = constant.COLOR_CHECKBUTTON
    style.activeBackground = constant.COLOR_CHECKBUTTON
    style.activeForeground = constant.COLOR_ALMOST_WHITE
    return style
