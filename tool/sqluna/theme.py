from pyrustic.theme import Theme
from pyrustic.themes import darkmatter


# ========================================
#               GENERAL
# ========================================
# header bar
frame_header_bar_style = darkmatter.frame_style.copy()

# Label header bar
label_header_bar = darkmatter.label_style.copy()
label_header_bar.background = "#005954"
label_header_bar.foreground = "#ECFFFF"
label_header_bar.font = darkmatter.FONT_FAV_BOLD

# Entry database on header bar
entry_database_style = darkmatter.entry_style.copy()
entry_database_style.background = "white"
entry_database_style.readonlyBackground = "#18817C"
entry_database_style.foreground = "#ECFFFF"

# Button expander
button_expander_style = darkmatter.button_style.copy()
button_expander_style.font = darkmatter.FONT_FAV_BOLD
button_expander_style.background = darkmatter.COLOR_BLACK
button_expander_style.foreground = "gray"
button_expander_style.highlightThickness = 0
button_expander_style.borderWidth = 0
button_expander_style.activeBackground = "#F0F8FF"
button_expander_style.padX = 3
button_expander_style.padY = 1

# Button edit
button_expander_style = button_expander_style.copy()

# Tree title (sql previously executed)
entry_tree_title = darkmatter.entry_style.copy()
entry_tree_title.readonlyBackground = darkmatter.COLOR_BLACK
entry_tree_title.font = darkmatter.FONT_FAV_BOLD
entry_tree_title.foreground = "#CFCFCF"
entry_tree_title.relief = "flat"

# Collapsable frame
frame_collapsable = darkmatter.frame_style.copy()
frame_collapsable.background = darkmatter.COLOR_BLACK

# Text message success
text_message = darkmatter.text_style.copy()
text_message.foreground = "white"
text_message.background = darkmatter.COLOR_BLACK
text_message.highlightThickness = 0
text_message.relief = "flat"

# button clear x
button_clear_x = darkmatter.button_style.copy()
button_clear_x.background = "#FF6060"
button_clear_x.foreground = "white"
button_clear_x.activeBackground = "red"
button_clear_x.activeForeground = "white"

# text editor
text_editor = darkmatter.text_style.copy()
text_editor.background = "#005954"
text_editor.foreground = "white"
text_editor.insertBackground = "#CFCFCF"
text_editor.highlightThickness = 0
text_editor.highlightColor = "#005954"

# label schema
label_schema_title_style = darkmatter.label_style.copy()
label_schema_title_style.foreground = "#E0D7D7"
label_schema_title_style.font = darkmatter.FONT_FAV_BOLD

# buttons above table
button_above_table = darkmatter.button_style.copy()
button_above_table.background = darkmatter.COLOR_BLACK
button_above_table.foreground = "#486B6B"
button_above_table.highlightBackground = "#486B6B"
button_above_table.relief = "flat"

general_theme = Theme()
general_theme.add_style(frame_header_bar_style, scope="*HeaderBar*")
general_theme.add_style(label_header_bar, scope="*HeaderBar*Label*")
general_theme.add_style(entry_database_style, scope="*HeaderBar*Entry*")
general_theme.add_style(button_expander_style, scope="*treeExpanderButton*")
general_theme.add_style(button_expander_style, scope="*buttonEdit*")
general_theme.add_style(entry_tree_title, scope="*treeTitle*")
general_theme.add_style(frame_collapsable, scope="*CollapsableFrame*")
general_theme.add_style(frame_collapsable, scope="*CollapsableFrame*Frame*")
general_theme.add_style(text_message, scope="*CollapsableFrame*textMessage*")
general_theme.add_style(button_clear_x, scope="*buttonClearX*")
general_theme.add_style(text_editor, scope="*Editor*Text*")
general_theme.add_style(label_schema_title_style, scope="*CollapsableFrame*schemaTitle*")
general_theme.add_style(button_above_table, scope="*CollapsableFrame*Button*")

# ========================================
# SQLUNA THEME BASED ON TURQUOISE THEME
# ========================================

SQLUNA_THEME = darkmatter.general_theme
SQLUNA_THEME.add_theme(general_theme)
SQLUNA_THEME.add_theme(darkmatter.tree_theme)
SQLUNA_THEME.add_theme(darkmatter.scrollbox_theme)
SQLUNA_THEME.add_theme(darkmatter.confirm_theme)
SQLUNA_THEME.add_theme(darkmatter.table_theme)
