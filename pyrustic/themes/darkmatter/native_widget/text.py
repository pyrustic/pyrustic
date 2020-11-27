from pyrustic import default_style
from pyrustic.themes.darkmatter import constant


def get_style():
    style = default_style.Text()
    style.font = constant.FONT_FAV_NORMAL
    style.relief = "flat"
    style.selectBackground = "#B4C7EF"
    return style
