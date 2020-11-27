from pyrustic import default_style
from pyrustic.themes.darkmatter import constant
from pyrustic.theme import Theme


# == scrollbox theme
def get_theme():
    theme = Theme()
    theme.add_style(_get_scrollbox_style(), scope="*Scrollbox.")
    return theme

# scrollbox style
def _get_scrollbox_style():
    style = default_style.Frame()
    style.background = constant.COLOR_BLACK
    return style
