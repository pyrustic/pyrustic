from pyrustic.theme.cyberpunk.native_widget import frame
from pyrustic.theme.cyberpunk.native_widget import label
from pyrustic.theme.cyberpunk.native_widget import listbox
from pyrustic.theme.cyberpunk.native_widget import scrollbar
from pyrustic.theme import Theme
from pyrustic.theme.cyberpunk import constant


# == table theme
def get_theme():
    theme = Theme()
    theme.add_style(_get_table_header_frame_style(), scope="*Table*frame_background*Frame*")
    theme.add_style(_get_table_header_style(), scope="*Table*Label*")
    theme.add_style(_get_table_column_style(), scope="*Table*Listbox*")
    theme.add_style(_get_table_hsb_style(), scope="*Table*hsb*")
    theme.add_style(_get_table_vsb_style(), scope="*Table*vsb*")
    return theme


# ========================================
#                PRIVATE
# ========================================
# header frames
def _get_table_header_frame_style():
    style = frame.get_style()
    style.highlightBackground = "#003B3B"
    style.highlightThickness = 1
    return style


# header label
def _get_table_header_style():
    style = label.get_style()
    style.font = constant.FONT_FAV_BOLD
    style.foreground = "#C8EBEB"
    style.background = "#486B6B"
    return style


# column
def _get_table_column_style():
    style = listbox.get_style()
    style.foreground = "#585858"
    style.background = "#F0F7F7"
    style.font = constant.FONT_FAV_NORMAL
    style.highlightBackground = "#003B3B"
    style.selectBackground = "#B4C7EF"
    return style


# hsb
def _get_table_hsb_style():
    style = scrollbar.get_style()
    return style


# vsb
def _get_table_vsb_style():
    style = scrollbar.get_style()
    return style
