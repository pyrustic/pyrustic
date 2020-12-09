from pyrustic.theme import Theme
from pyrustic import default_style
from pyrustic.themes.darkmatter import theme as darkmatter_theme
from pyrustic.themes.darkmatter import constant
from pyrustic.themes.darkmatter.pyrustic_widget import tree
from pyrustic.themes.darkmatter.pyrustic_widget import scrollbox
from pyrustic.themes.darkmatter.pyrustic_widget import confirm
from pyrustic.themes.darkmatter.pyrustic_widget import table
from pyrustic.themes.darkmatter.native_widget import frame
from pyrustic.themes.darkmatter.native_widget import label
from pyrustic.themes.darkmatter.native_widget import entry
from pyrustic.themes.darkmatter.native_widget import button
from pyrustic.themes.darkmatter.native_widget import text


# ========================================
# DATABRO THEME BASED ON DARKMATTER THEME
# ========================================
def get_theme():
    theme = darkmatter_theme.get_theme()
    theme.add_theme(_get_general_theme())
    theme.add_theme(tree.get_theme())
    theme.add_theme(scrollbox.get_theme())
    theme.add_theme(confirm.get_theme())
    theme.add_theme(table.get_theme())
    return theme

# ========================================
#               PRIVATE
# ========================================
def _get_general_theme():
    theme = Theme()
    theme.add_style(_get_frame_header_bar_style(), scope="*HeaderBar*")
    theme.add_style(_get_label_header_bar_style(), scope="*HeaderBar*Label*")
    theme.add_style(_get_entry_database_style(), scope="*HeaderBar*Entry*")
    theme.add_style(_get_button_expander_style(), scope="*treeExpanderButton*")
    theme.add_style(_get_button_edit_style(), scope="*buttonEdit*")
    theme.add_style(_get_entry_tree_title_style(), scope="*treeTitle*")
    theme.add_style(_get_frame_collapsable_style(), scope="*CollapsableFrame*")
    theme.add_style(_get_frame_collapsable_style(), scope="*CollapsableFrame*Frame*")
    theme.add_style(_get_text_message_style(), scope="*CollapsableFrame*textMessage*")
    theme.add_style(_get_button_clear_x_style(), scope="*buttonClearX*")
    theme.add_style(_get_text_editor_style(), scope="*Editor*Text*")
    theme.add_style(_get_label_schema_title_style(), scope="*CollapsableFrame*schemaTitle*")
    theme.add_style(_get_button_above_table_style(), scope="*CollapsableFrame*Button*")
    return theme


# header bar
def _get_frame_header_bar_style():
    style = frame.get_style()
    return style


# Label header bar
def _get_label_header_bar_style():
    style = label.get_style()
    style.background = "#005954"
    style.foreground = "#ECFFFF"
    style.font = constant.FONT_FAV_BOLD
    return style


# Entry database on header bar
def _get_entry_database_style():
    style = entry.get_style()
    style.background = "white"
    style.readonlyBackground = "#18817C"
    style.foreground = "#ECFFFF"
    return style


# Button expander
def _get_button_expander_style():
    style = button.get_style()
    style.font = constant.FONT_FAV_BOLD
    style.background = constant.COLOR_BLACK
    style.foreground = "gray"
    style.highlightThickness = 0
    style.borderWidth = 0
    style.activeBackground = "#F0F8FF"
    style.padX = 3
    style.padY = 1
    return style


# Button edit
def _get_button_edit_style():
    style = _get_button_expander_style()
    return style


# Tree title (sql previously executed)
def _get_entry_tree_title_style():
    style = entry.get_style()
    style.readonlyBackground = constant.COLOR_BLACK
    style.font = constant.FONT_FAV_BOLD
    style.foreground = "#CFCFCF"
    style.relief = "flat"
    return style


# Collapsable frame
def _get_frame_collapsable_style():
    style = frame.get_style()
    style.background = constant.COLOR_BLACK
    return style


# Text message success
def _get_text_message_style():
    style = text.get_style()
    style.foreground = "white"
    style.background = constant.COLOR_BLACK
    style.highlightThickness = 0
    style.relief = "flat"
    return style


# button clear x
def _get_button_clear_x_style():
    style = button.get_style()
    style.background = "#FF6060"
    style.foreground = "white"
    style.activeBackground = "red"
    style.activeForeground = "white"
    return style


# text editor
def _get_text_editor_style():
    style = text.get_style()
    style.background = "#005954"
    style.foreground = "white"
    style.insertBackground = "#CFCFCF"
    style.highlightThickness = 0
    style.highlightColor = "#005954"
    return style


# label schema
def _get_label_schema_title_style():
    style = label.get_style()
    style.foreground = "#E0D7D7"
    style.font = constant.FONT_FAV_BOLD
    return style


# buttons above table
def _get_button_above_table_style():
    style = button.get_style()
    style.background = constant.COLOR_BLACK
    style.foreground = "#486B6B"
    style.highlightBackground = "#486B6B"
    style.relief = "flat"
    return style
