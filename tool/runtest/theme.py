from pyrustic.theme import Theme
from pyrustic import default_style
from pyrustic.themes import darkmatter


# ========================================
#                   TREE
# ========================================
# titlebar
tree_titlebar_style = default_style.Frame()
tree_titlebar_style.background = darkmatter.COLOR_BLACK

# expander button
tree_expander_button_style = default_style.Button()
tree_expander_button_style.font = darkmatter.FONT_FAV_BOLD
tree_expander_button_style.background = darkmatter.COLOR_BLACK
tree_expander_button_style.foreground = "gray"
tree_expander_button_style.highlightThickness = 0
tree_expander_button_style.borderWidth = 0
tree_expander_button_style.activeBackground = "#F0F8FF"
tree_expander_button_style.padX = 3
tree_expander_button_style.padY = 1

# title_one label
tree_title_one_label_style = default_style.Label()
tree_title_one_label_style.font = darkmatter.FONT_FAV_BOLD
tree_title_one_label_style.background = darkmatter.COLOR_BLACK
tree_title_one_label_style.foreground = "gray"

# title_two label
tree_title_two_label_style = default_style.Label()
tree_title_two_label_style.font = darkmatter.FONT_FAV_BOLD
tree_title_two_label_style.background = darkmatter.COLOR_BLACK
tree_title_two_label_style.foreground = "#CFCFCF"

# == Tree Theme
tree_theme = darkmatter.tree_theme
tree_theme.add_style(tree_titlebar_style, scope="*Tree*")
tree_theme.add_style(tree_expander_button_style, scope="*Tree*treeExpanderButton.")
tree_theme.add_style(tree_title_one_label_style, scope="*Tree*treeTitleLabelOne.")
tree_theme.add_style(tree_title_two_label_style, scope="*Tree*treeTitleLabelTwo.")


# ========================================
#            TOOLBAR
# ========================================
# toolbar body
toolbar_body_style = default_style.Frame()
toolbar_body_style.background = "#002323"

# label testing passed
toolbar_label_testing_passed_style = darkmatter.label_style.copy()
toolbar_label_testing_passed_style.foreground = "#40A640"
toolbar_label_testing_passed_style.background = "#002323"

# label testing failed
toolbar_label_testing_failed_style = darkmatter.label_style.copy()
toolbar_label_testing_failed_style.foreground = "#F73030"
toolbar_label_testing_failed_style.background = "#002323"

# button run
toolbar_button_run = darkmatter.button_style.copy()
toolbar_button_run.background = "#004600"
toolbar_button_run.foreground = darkmatter.COLOR_ALMOST_WHITE
toolbar_button_run.activeBackground = "#006600"
toolbar_button_run.activeForeground = darkmatter.COLOR_ALMOST_WHITE
toolbar_button_run.highlightBackground = darkmatter.COLOR_ALMOST_WHITE
toolbar_button_run.highlightColor = darkmatter.COLOR_ALMOST_WHITE

# button rerun
toolbar_button_rerun = toolbar_button_run.copy()

# button stop
toolbar_button_stop =  toolbar_button_run.copy()
toolbar_button_stop.background = "#CF0000"
toolbar_button_stop.activeBackground = "#FF0000"

# button cancel
toolbar_button_cancel = toolbar_button_run.copy()
toolbar_button_cancel.background = "#BF2600"
toolbar_button_cancel.activeBackground = "#D73E18"

# button clean
toolbar_button_clean =  toolbar_button_run.copy()
toolbar_button_clean.background = darkmatter.COLOR_BLACK
toolbar_button_clean.activeBackground = "#FF0000"
toolbar_button_clean.foreground = "gray"
toolbar_button_clean.borderWidth = 0
toolbar_button_clean.highlightThickness = 0

# button log
toolbar_button_log =  toolbar_button_run.copy()
toolbar_button_log.background = "#003366"
toolbar_button_log.activeBackground = "#204B7E"

# == toolbar theme
toolbar_theme = Theme()
toolbar_theme.add_style(toolbar_body_style, scope="*runtestToolbar*")
toolbar_theme.add_style(toolbar_label_testing_passed_style,
                        scope="*runtestToolbar*labelTestingPassed.")
toolbar_theme.add_style(toolbar_label_testing_failed_style,
                        scope="*runtestToolbar*labelTestingFailed.")
toolbar_theme.add_style(toolbar_button_run, scope="*runtestToolbar*buttonRun.")
toolbar_theme.add_style(toolbar_button_rerun, scope="*runtestToolbar*buttonRerun.")
toolbar_theme.add_style(toolbar_button_stop, scope="*runtestToolbar*buttonStop.")
toolbar_theme.add_style(toolbar_button_cancel, scope="*runtestToolbar*buttonCancel.")
toolbar_theme.add_style(toolbar_button_clean, scope="*runtestToolbar*buttonClean.")
toolbar_theme.add_style(toolbar_button_log, scope="*runtestToolbar*buttonLog.")


# ========================================
#               LOG WINDOW
# ========================================
# log window
log_window_text_style = default_style.Text()
log_window_text_style.font = darkmatter.FONT_DEFAULT_FAMILY, 15, "normal"
log_window_text_style.background = "#033669"
log_window_text_style.foreground = "#7EB1B1"
log_window_text_style.highlightThickness = 0

# == log window theme
log_window_theme = Theme()
log_window_theme.add_style(log_window_text_style, scope="*Text.")


# ========================================
# RUNTEST THEME BASED ON DARKMATTER THEME
# ========================================
RUNTEST_THEME = darkmatter.DARKMATTER_THEME
RUNTEST_THEME.add_theme(tree_theme)
RUNTEST_THEME.add_theme(toolbar_theme)
RUNTEST_THEME.add_theme(log_window_theme)
