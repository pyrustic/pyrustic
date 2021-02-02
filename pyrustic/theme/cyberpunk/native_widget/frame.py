from pyrustic import default_style
from pyrustic.theme.cyberpunk import constant


def get_style():
    style = default_style.Frame()
    style.background = constant.COLOR_BLACK
    return style
