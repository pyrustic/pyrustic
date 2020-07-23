from pyrustic import default_style
from pyrustic.theme import Theme


"""
This is DARKMATTER, the nice theme included in Pyrustic Framework.
To use it, you just need to assign pyrustic.themes.darkmatter.DARKMATTER_THEME
to pyrustic.app.App's property 'theme'.
Example:
    from pyrustic.app import App
    from pyrustic.themes.darkmatter import DARKMATTER_THEME
    app = App()
    app.theme = DARKMATTER_THEME
    app.start()

You can make your own theme by overriding whatever part of DARKMATTER_THEME you want.
You can also freely and proudly copy the content of darkmatter.py inside your theme.py then edit it.
"""

# ========================================
#       CONSTANTS - COLORS AND FONTS
# ========================================
COLOR_ALMOST_WHITE = "#F0F8FF"
COLOR_BLACK = "#101010"
COLOR_GRAY = "gray"
COLOR_CHECKBUTTON = "#001313"
FONT_DEFAULT_FAMILY = "Liberation Mono"
FONT_FAV_BOLD = FONT_DEFAULT_FAMILY, 13, "bold"
FONT_FAV_NORMAL = FONT_DEFAULT_FAMILY, 13, "normal"


# ========================================
#                   GENERAL
# ========================================
# Button
button_style = default_style.Button()
button_style.font = FONT_FAV_BOLD
button_style.foreground = "#CFCFCF"
button_style.background = COLOR_BLACK
button_style.highlightBackground = "#CFCFCF"
button_style.activeBackground = "white"
button_style.activeForeground = COLOR_BLACK

# Canvas
canvas_style = default_style.Canvas()
canvas_style.background = COLOR_BLACK
canvas_style.highlightThickness = 0

# Checkbutton
checkbutton_style = default_style.Checkbutton()
checkbutton_style.background = COLOR_BLACK
checkbutton_style.foreground = "#CFCFCF"
checkbutton_style.font = FONT_FAV_NORMAL
checkbutton_style.highlightThickness = 0
checkbutton_style.selectColor = COLOR_CHECKBUTTON
checkbutton_style.activeBackground = COLOR_CHECKBUTTON
checkbutton_style.activeForeground = COLOR_ALMOST_WHITE

# Entry
entry_style = default_style.Entry()
entry_style.font = FONT_FAV_NORMAL
entry_style.readonlyBackground = "#EFEFEF"
entry_style.highlightThickness = 0
entry_style.foreground = COLOR_BLACK
entry_style.relief = "flat"
entry_style.selectBackground = "#B4C7EF"

# Frame
frame_style = default_style.Frame()
frame_style.background = COLOR_BLACK

# Label
label_style = default_style.Label()
label_style.font = FONT_FAV_NORMAL
label_style.background = COLOR_BLACK
label_style.foreground = "#CFCFCF"

# LabelFrame
label_frame_style = default_style.LabelFrame()

# Listbox
listbox_style = default_style.Listbox()

# Menu
menu_style = default_style.Menu()

# Menubutton
menubutton_style = default_style.Menubutton()

# PanedWindow
paned_window_style = default_style.PanedWindow()

# Radiobutton
radiobutton_style = default_style.Radiobutton()

# Scale
scale_style = default_style.Scale()

# Scrollbar
scrollbar_style = default_style.Scrollbar()
scrollbar_style.activeBackground = COLOR_ALMOST_WHITE
scrollbar_style.background = "gray"
scrollbar_style.highlightBackground = COLOR_BLACK
scrollbar_style.highlightColor = COLOR_BLACK
scrollbar_style.troughColor = COLOR_BLACK
scrollbar_style.relief = "flat"
scrollbar_style.highlightThickness = 0
scrollbar_style.borderWidth = 0

# Spinbox
spinbox_style = default_style.Spinbox()

# Text
text_style = default_style.Text()
text_style.font = FONT_FAV_NORMAL
text_style.relief = "flat"
text_style.selectBackground = "#B4C7EF"

# Toplevel
toplevel_style = default_style.Toplevel()
toplevel_style.background = COLOR_BLACK

# == General theme
general_theme = Theme()
for style in (button_style, canvas_style,
              checkbutton_style, entry_style,
              frame_style, label_style,
              label_frame_style, listbox_style,
              menu_style, menubutton_style,
              paned_window_style, radiobutton_style,
              scale_style, scrollbar_style, spinbox_style,
              text_style, toplevel_style):
    general_theme.add_style(style)
general_theme.add_style(frame_style)


# ========================================
#                   TREE
# ========================================
# tree body
tree_body_style = default_style.Frame()
tree_body_style.background = COLOR_BLACK

# tree node
tree_node_style = default_style.Frame()
tree_node_style.background = COLOR_BLACK

# tree header
tree_header_style = default_style.Frame()
tree_header_style.background = COLOR_BLACK

# tree box
tree_box_style = default_style.Frame()
tree_box_style.background = COLOR_BLACK

# == tree theme
tree_theme = Theme()
tree_theme.add_style(tree_body_style, scope="*Tree.")
tree_theme.add_style(tree_node_style, scope="*Tree*TreeNode.")
tree_theme.add_style(tree_header_style, scope="*Tree*treeHeader.")
tree_theme.add_style(tree_box_style, scope="*Tree*treeBox.")


# ========================================
#                SCROLLBOX
# ========================================
# scrollbox
scrollbox_style = default_style.Frame()
scrollbox_style.background = COLOR_BLACK

# == scrollbox theme
scrollbox_theme = Theme()
scrollbox_theme.add_style(scrollbox_style, scope="*Scrollbox.")


# ========================================
#                TABLE
# ========================================
# header frames
table_header_frame_style = frame_style.copy()
table_header_frame_style.highlightBackground = "#003B3B"
table_header_frame_style.highlightThickness = 1

# header label
table_header_style = label_style.copy()
table_header_style.font = FONT_FAV_BOLD
table_header_style.foreground = "#C8EBEB"
table_header_style.background = "#486B6B"

# column
table_column_style = listbox_style.copy()
table_column_style.foreground = "#585858"
table_column_style.background = "#F0F7F7"
table_column_style.font = FONT_FAV_NORMAL
table_column_style.highlightBackground = "#003B3B"
table_column_style.selectBackground = "#B4C7EF"

# hsb
table_hsb_style = scrollbar_style.copy()

# vsb
table_vsb_style = scrollbar_style.copy()

# == table theme
table_theme = Theme()
table_theme.add_style(table_header_frame_style, scope="*Table*TableHeaderFrame*")
table_theme.add_style(table_header_style, scope="*Table*Label*")
table_theme.add_style(table_column_style, scope="*Table*Listbox*")
table_theme.add_style(table_hsb_style, scope="*Table*hsb*")
table_theme.add_style(table_vsb_style, scope="*Table*vsb*")


# ========================================
#                CONFIRM
# ========================================
# confirm toplevel
confirm_toplevel_style = toplevel_style.copy()

# confirm label
confirm_label_style = label_style.copy()
confirm_label_style.font = FONT_FAV_BOLD

# confirm text
confirm_text_style = text_style.copy()
confirm_text_style.highlightThickness = 0
confirm_text_style.foreground = "gray"
confirm_text_style.background = COLOR_BLACK

# == confirm theme
confirm_theme = Theme()
confirm_theme.add_style(confirm_toplevel_style, scope="*Confirm.")
confirm_theme.add_style(confirm_label_style, scope="*Confirm*Label*")
confirm_theme.add_style(confirm_text_style, scope="*Confirm*Text*")


# ========================================
#                TOAST
# ========================================
# toast toplevel
toast_toplevel_style = toplevel_style.copy()

# toast header
toast_header_label_style = label_style.copy()
toast_header_label_style.font = FONT_FAV_BOLD

# toast message
toast_message_label_style = label_style.copy()
toast_message_label_style.foreground = "gray"
toast_message_label_style.background = COLOR_BLACK

# == toast theme
toast_theme = Theme()
toast_theme.add_style(confirm_toplevel_style, scope="*Toast.")
toast_theme.add_style(toast_header_label_style, scope="*Toast*header*")
toast_theme.add_style(toast_message_label_style, scope="*Toast*message*")


# ========================================
#             DARKMATTER THEME
# ========================================
DARKMATTER_THEME = Theme()
DARKMATTER_THEME.add_theme(general_theme)
DARKMATTER_THEME.add_theme(tree_theme)
DARKMATTER_THEME.add_theme(scrollbox_theme)
DARKMATTER_THEME.add_theme(table_theme)
DARKMATTER_THEME.add_theme(confirm_theme)
DARKMATTER_THEME.add_theme(toast_theme)
