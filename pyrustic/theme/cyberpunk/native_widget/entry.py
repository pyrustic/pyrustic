from pyrustic import default_style
from pyrustic.theme.cyberpunk import constant


def get_style():
    style = default_style.Entry()
    style.font = constant.FONT_FAV_NORMAL
    style.readonlyBackground = "#EFEFEF"
    style.highlightThickness = 0
    style.foreground = constant.COLOR_BLACK
    style.relief = "flat"
    style.selectBackground = "#B4C7EF"
    return style
