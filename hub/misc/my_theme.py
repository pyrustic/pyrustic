from pyrustic.theme import Theme
from pyrustic import default_style
from pyrustic.themes.darkmatter import theme as darkmatter_theme
from pyrustic.themes.darkmatter import constant
from pyrustic.themes.darkmatter.pyrustic_widget import tree
from pyrustic.themes.darkmatter.native_widget import label
from pyrustic.themes.darkmatter.native_widget import entry
from pyrustic.themes.darkmatter.native_widget import button
from pyrustic.themes.darkmatter.native_widget import text
from pyrustic.themes.darkmatter.native_widget import checkbutton
from pyrustic.themes.darkmatter.native_widget import toplevel


# ========================================
# HUB THEME BASED ON DARKMATTER THEME
# ========================================
def get_theme():
    theme = darkmatter_theme.get_theme()
    theme.add_theme(_get_general_theme())
    return theme


# ===================================
#              GENERAL
# ===================================
def _get_general_theme():
    theme = Theme()
    theme.add_style(_get_label_query_style(), scope="*label_query*")
    theme.add_style(_get_button_go_style(), scope="*button_go*")
    theme.add_style(_get_button_rate_style(), scope="*button_rate*")
    theme.add_style(_get_button_publishing_style(), scope="*button_publishing*")
    theme.add_style(_get_button_expander_style(), scope="*button_expander*")
    theme.add_style(_get_toolbar_button_close_style(), scope="*button_close*")
    theme.add_style(_get_checkbutton_auth_style(), scope="*checkbutton_auth*")
    theme.add_style(_get_label_owner_style(), scope="*label_owner*")
    theme.add_style(_get_label_repo_style(), scope="*label_repo*")
    theme.add_style(_get_button_refresh_style(), scope="*button_refresh*")
    theme.add_style(_get_button_retry_style(), scope="*button_retry*")
    theme.add_style(_get_label_info_title_style(), scope="*label_info_title*")
    theme.add_style(_get_label_error_style(), scope="*label_error*")
    theme.add_style(_get_label_counts_style(), scope="*label_counts*")
    theme.add_style(_get_button_cancel_style(), scope="*button_cancel*")
    theme.add_style(_get_button_confirm_style(), scope="*button_confirm*")
    theme.add_style(_get_entry_style(), scope="*Entry*")
    theme.add_style(_get_entry_search_style(), scope="*entry_search*")
    theme.add_style(_get_entry_repo_description_style(),
                    scope="*entry_repo_description*")
    theme.add_style(_get_toplevel_style(), scope="*Toplevel.")
    theme.add_style(_get_text_description_style(), scope="*text_description*")
    theme.add_style(_get_label_repo_style(), scope="*frame_form*Label*")
    theme.add_style(_get_label_project_style(), scope="*label_project*")
    theme.add_style(_get_entry_project_style(), scope="*entry_project*")
    theme.add_style(label.get_style(), scope="*label_mandatory*")
    theme.add_style(_get_failure_view_text_style(), scope="*failure_view*")
    return theme

# label query
def _get_label_query_style():
    style = label.get_style()
    style.background = "#005954"
    style.foreground = "#ECFFFF"
    style.font = constant.FONT_FAV_BOLD
    return style

# button go (search)
def _get_button_go_style():
    style = button.get_style()
    style.highlightBackground = "#000000"
    style.highlightColor = "#000000"
    style.background = "#ffffff"
    style.foreground = "#005954"
    style.activeBackground = "#005954"
    style.activeForeground = "#ECFFFF"
    style.highlightThickness = 0
    style.relief = "flat"
    style.padY = 0
    return style

# button rate
def _get_button_rate_style():
    style = button.get_style()
    style.background = "#181818"
    style.foreground = "#A098A0"
    style.highlightBackground = "#484048"
    style.highlightColor = "white"
    style.highlightThickness = 1
    style.relief = "flat"
    style.padY = 0
    return style

# button publishing
def _get_button_publishing_style():
    style = button.get_style()
    style.background = "#285B28"
    style.foreground = "#E0FFFF"
    style.highlightBackground = "#689B68"
    style.highlightColor = "white"
    style.highlightThickness = 1
    style.relief = "flat"
    return style

# expander button
def _get_button_expander_style():
    style = default_style.Button()
    style.font = constant.FONT_FAV_BOLD
    style.background = constant.COLOR_BLACK
    style.foreground = "gray"
    style.highlightThickness = 0
    style.borderWidth = 0
    style.activeBackground = "#F0F8FF"
    style.padX = 3
    style.padY = 1
    return style

# button close
def _get_toolbar_button_close_style():
    style = default_style.Button()
    style.background = "#191919"
    style.activeBackground = "#670000"
    style.activeForeground = "#FF0023"
    style.foreground = "#606060"
    style.borderWidth = 0
    style.highlightThickness = 0
    style.padX = 3
    style.padY = 0
    return style

# checkbox 'Authentication'
def _get_checkbutton_auth_style():
    style = checkbutton.get_style()
    style.foreground = "#D0D0D0"
    style.background = "#001B1B"
    style.activeBackground = "#003333"
    return style

# label owner
def _get_label_owner_style():
    style = label.get_style()
    style.foreground = "#9F9F9F"
    return style

# label owner
def _get_label_repo_style():
    style = label.get_style()
    style.foreground = "#D0D0D0"
    style.font = constant.FONT_FAV_BOLD
    return style

# button refresh
def _get_button_refresh_style():
    style = _get_button_rate_style()
    return style

# button retry
def _get_button_retry_style():
    style = button.get_style()
    style.background = "#301818"
    style.foreground = "#B898A0"
    style.highlightBackground = "#604048"
    style.highlightColor = "white"
    style.highlightThickness = 1
    style.relief = "flat"
    style.padY = 0
    return style

# node info
def _get_node_info_style():
    style = default_style.Frame()
    style.background = "#002323"
    return style

# label info title
def _get_label_info_title_style():
    style = label.get_style()
    style.foreground = "#9F9FC7"
    return style

# label error
def _get_label_error_style():
    style = label.get_style()
    style.foreground = "#D898A0"
    return style

# label stargazers
def _get_label_counts_style():
    style = label.get_style()
    style.font = constant.FONT_FAV_BOLD
    return style

# entry repo description
def _get_entry_repo_description_style():
    style = default_style.Entry()
    style.readonlyBackground = constant.COLOR_BLACK
    style.background = constant.COLOR_BLACK
    style.font = constant.FONT_FAV_NORMAL
    style.foreground = "#CFCFCF"
    return style

# button cancel
def _get_button_cancel_style():
    style = _get_button_retry_style()
    return style

# button confirm
def _get_button_confirm_style():
    style = _get_button_publishing_style()
    style.padY = 0
    return style

# entries
def _get_entry_style():
    style = entry.get_style()
    style.background = "#182020"
    style.foreground = "#C8D8E0"
    style.insertBackground = "#C8D8E0"
    style.readonlyBackground = "#101818"
    return style

# entry search
def _get_entry_search_style():
    style = entry.get_style()
    style.background = "white"
    style.insertBackground = constant.COLOR_BLACK
    return style

# toplevel
def _get_toplevel_style():
    style = toplevel.get_style()
    return style

# label project
def _get_label_project_style():
    style = _get_label_query_style()
    return style

# text description
def _get_text_description_style():
    style = text.get_style()
    style.highlightThickness = 0
    style.insertBackground = "#C8D8E0"
    style.background = "#182020"
    style.foreground = "#C8D8E0"
    return style

# entry project
def _get_entry_project_style():
    style = entry.get_style()
    return style

def _get_failure_view_text_style():
    style = text.get_style()
    style.foreground = "#C8C8C8"
    style.highlightThickness = 0
    style.background = constant.COLOR_BLACK
    return style