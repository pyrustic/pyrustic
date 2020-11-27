from pyrustic.theme import Theme
from pyrustic import default_style
from pyrustic.themes.darkmatter import theme as darkmatter_theme
from pyrustic.themes.darkmatter import constant
from pyrustic.themes.darkmatter.pyrustic_widget import tree
from pyrustic.themes.darkmatter.native_widget import label
from pyrustic.themes.darkmatter.native_widget import button


# ========================================
# RUNTEST THEME BASED ON DARKMATTER THEME
# ========================================
def get_theme():
    theme = darkmatter_theme.get_theme()
    theme.add_theme(_get_tree_theme())
    theme.add_theme(_get_toolbar_theme())
    theme.add_theme(_get_log_window_theme())
    return theme


# ========================================
#                   TREE
# ========================================
# == Tree Theme
def _get_tree_theme():
    theme = tree.get_theme()
    theme.add_style(_get_tree_titlebar_style(), scope="*Tree*")
    theme.add_style(_get_tree_expander_button_style(), scope="*Tree*treeExpanderButton.")
    theme.add_style(_get_tree_title_one_label_style(), scope="*Tree*treeTitleLabelOne.")
    theme.add_style(_get_tree_title_two_label_style(), scope="*Tree*treeTitleLabelTwo.")
    return theme


# titlebar
def _get_tree_titlebar_style():
    style = default_style.Frame()
    style.background = constant.COLOR_BLACK
    return style


# expander button
def _get_tree_expander_button_style():
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


# title_one label
def _get_tree_title_one_label_style():
    style = default_style.Label()
    style.font = constant.FONT_FAV_BOLD
    style.background = constant.COLOR_BLACK
    style.foreground = "gray"
    return style


# title_two label
def _get_tree_title_two_label_style():
    style = default_style.Label()
    style.font = constant.FONT_FAV_BOLD
    style.background = constant.COLOR_BLACK
    style.foreground = "#CFCFCF"
    return style


# ========================================
#            TOOLBAR
# ========================================
# == toolbar theme
def _get_toolbar_theme():
    theme = Theme()
    theme.add_style(_get_toolbar_body_style(), scope="*runtestToolbar*")
    theme.add_style(_get_toolbar_label_testing_passed_style(),
                            scope="*runtestToolbar*labelTestingPassed.")
    theme.add_style(_get_toolbar_label_testing_failed_style(),
                            scope="*runtestToolbar*labelTestingFailed.")
    theme.add_style(_get_toolbar_button_run(), scope="*runtestToolbar*buttonRun.")
    theme.add_style(_get_toolbar_button_rerun(), scope="*runtestToolbar*buttonRerun.")
    theme.add_style(_get_toolbar_button_stop(), scope="*runtestToolbar*buttonStop.")
    theme.add_style(_get_toolbar_button_cancel(), scope="*runtestToolbar*buttonCancel.")
    theme.add_style(_get_toolbar_button_clean(), scope="*runtestToolbar*buttonClean.")
    theme.add_style(_get_toolbar_button_log(), scope="*runtestToolbar*buttonLog.")
    return theme


# toolbar body
def _get_toolbar_body_style():
    style = default_style.Frame()
    style.background = "#002323"
    return style


# label testing passed
def _get_toolbar_label_testing_passed_style():
    style = label.get_style()
    style.foreground = "#40A640"
    style.background = "#002323"
    return style


# label testing failed
def _get_toolbar_label_testing_failed_style():
    style = label.get_style()
    style.foreground = "#F73030"
    style.background = "#002323"
    return style


# button run
def _get_toolbar_button_run():
    style = button.get_style()
    style.background = "#004600"
    style.foreground = constant.COLOR_ALMOST_WHITE
    style.activeBackground = "#006600"
    style.activeForeground = constant.COLOR_ALMOST_WHITE
    style.highlightBackground = constant.COLOR_ALMOST_WHITE
    style.highlightColor = constant.COLOR_ALMOST_WHITE
    return style

# button rerun
def _get_toolbar_button_rerun():
    style = _get_toolbar_button_run()
    return style


# button stop
def _get_toolbar_button_stop():
    style = _get_toolbar_button_run()
    style.background = "#CF0000"
    style.activeBackground = "#FF0000"
    return style


# button cancel
def _get_toolbar_button_cancel():
    style = _get_toolbar_button_run()
    style.background = "#BF2600"
    style.activeBackground = "#D73E18"
    return style


# button clean
def _get_toolbar_button_clean():
    style = _get_toolbar_button_run()
    style.background = constant.COLOR_BLACK
    style.activeBackground = "#FF0000"
    style.foreground = "gray"
    style.borderWidth = 0
    style.highlightThickness = 0
    return style


# button log
def _get_toolbar_button_log():
    style = _get_toolbar_button_run()
    style.background = "#003366"
    style.activeBackground = "#204B7E"
    return style


# ========================================
#               LOG WINDOW
# ========================================
# == log window theme
def _get_log_window_theme():
    theme = Theme()
    theme.add_style(_get_log_window_text_style(), scope="*Text.")
    return theme


# log window
def _get_log_window_text_style():
    style = default_style.Text()
    style.font = constant.FONT_DEFAULT_FAMILY, 15, "normal"
    style.background = "#033669"
    style.foreground = "#7EB1B1"
    style.highlightThickness = 0
    return style
