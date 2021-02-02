from pyrustic import default_style
from pyrustic.theme.cyberpunk import constant


def get_style():
    style = default_style.Canvas()
    style.background = constant.COLOR_BLACK
    style.highlightThickness = 0
    return style
