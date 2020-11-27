from pyrustic import default_style
from pyrustic.themes.darkmatter import constant


def get_style():
    style = default_style.Scrollbar()
    style.activeBackground = constant.COLOR_ALMOST_WHITE
    style.background = "gray"
    style.highlightBackground = constant.COLOR_BLACK
    style.highlightColor = constant.COLOR_BLACK
    style.troughColor = constant.COLOR_BLACK
    style.relief = "flat"
    style.highlightThickness = 0
    style.borderWidth = 0
    return style
