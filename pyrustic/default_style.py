import copy
from pyrustic.exception import PyrusticException


class _Style:
    _WIDGET_CLASS = None

    @property
    def widget_class(self):
        """
        Get the pyrustic_widget class
        """
        if self._WIDGET_CLASS is None:
            raise PyrusticException("The class attribute _WIDGET_CLASS is missing in the _Style subclass")
        return self._WIDGET_CLASS

    def copy(self):
        """
        Get a fresh new style copied from the actual one
        """
        return copy.copy(self)

    def target(self, widget, raise_exception=False):
        """
        Individually apply a style to a pyrustic_widget
        """
        data = self.__dict__
        cnf = {key.lower(): val for key, val in data.items()}
        if raise_exception:
            widget.config(cnf=cnf)
        else:
            for key, val in cnf.items():
                try:
                    widget.config(cnf={key: val})
                except Exception as e:
                    if raise_exception:
                        raise

    def style(self):
        """
        Get the dict-like style
        """
        return self.__dict__.copy()


class Button(_Style):
    _WIDGET_CLASS = "Button"

    def __init__(self):
        self.activeBackground = None  # "#ececec"
        self.activeForeground = None  # "#000000"
        self.anchor = None  # "center"
        self.background = None  # "#d9d9d9"
        self.borderWidth = None  # 1
        self.compound = None  # "none"
        self.default = None  # "disabled"
        self.disabledForeground = None  # "#a3a3a3"
        self.font = None  # TkDefaultFont
        self.foreground = None  # "#000000"
        self.height = None  # 0
        self.highlightBackground = None  # "#d9d9d9"
        self.highlightColor = None  # "#000000"
        self.highlightThickness = None  # 1
        self.justify = None  # "center"
        self.padX = None  # 3
        self.padY = None  # 1
        self.relief = None  # "raised"
        self.repeatDelay = None  # 0
        self.repeatInterval = None  # 0
        self.state = None  # "normal"
        self.underline = None  # -1
        self.width = None  # 0
        self.wrapLength = None  # 0


class Canvas(_Style):
    _WIDGET_CLASS = "Canvas"

    def __init__(self):
        self.background = None  # "#d9d9d9"
        self.borderWidth = None  # 0
        self.closeEnough = None  # 1
        self.confine = None  # 1
        self.height = None  # 7
        self.highlightBackground = None  # "#d9d9d9"
        self.highlightColor = None  # "#000000"
        self.highlightThickness = None  # 1
        self.insertBackground = None  # "#000000"
        self.insertBorderWidth = None  # 0
        self.insertOffTime = None  # 300
        self.insertOnTime = None  # 600
        self.insertWidth = None  # 2
        self.offset = None  # 0, 0
        self.relief = None  # "flat"
        self.selectBackground = None  # "#c3c3c3"
        self.selectBorderWidth = None  # 1
        self.selectForeground = None  # "#000000"
        self.state = None  # "normal"
        self.width = None  # 10
        self.xScrollIncrement = None  # 0
        self.yScrollIncrement = None  # 0


class Checkbutton(_Style):
    _WIDGET_CLASS = "Checkbutton"

    def __init__(self):
        self.activeBackground = None  # "#ececec"
        self.activeForeground = None  # "#000000"
        self.anchor = None  # "center"
        self.background = None  # "#d9d9d9"
        self.borderWidth = None  # 1
        self.compound = None  # "none"
        self.disabledForeground = None  # "#a3a3a3"
        self.font = None  # TkDefaultFont
        self.foreground = None  # "#000000"
        self.height = None  # 0
        self.highlightBackground = None  # "#d9d9d9"
        self.highlightColor = None  # "#000000"
        self.highlightThickness = None  # 1
        self.indicatorOn = None  # 1
        self.justify = None  # "center"
        self.offRelief = None  # "raised"
        self.offValue = None  # 0
        self.onValue = None  # 1
        self.padX = None  # 1
        self.padY = None  # 1
        self.relief = None  # "flat"
        self.selectColor = None  # "#ffffff"
        self.state = None  # "normal"
        self.underline = None  # -1
        self.width = None  # 0
        self.wrapLength = None  # 0


class Entry(_Style):
    _WIDGET_CLASS = "Entry"

    def __init__(self):
        self.background = None  # "#ffffff"
        self.borderWidth = None  # 1
        self.cursor = None  # xterm
        self.disabledBackground = None  # "#d9d9d9"
        self.disabledForeground = None  # "#a3a3a3"
        self.exportSelection = None  # 1
        self.font = None  # TkTextFont
        self.foreground = None  # # 000000
        self.highlightBackground = None  # "#d9d9d9"
        self.highlightColor = None  # # 000000
        self.highlightThickness = None  # 1
        self.insertBackground = None  # "#000000"
        self.insertBorderWidth = None  # 0
        self.insertOffTime = None  # 300
        self.insertOnTime = None  # 600
        self.insertWidth = None  # 2
        self.justify = None  # left
        self.readonlyBackground = None  # "#d9d9d9"
        self.relief = None  # sunken
        self.selectBackground = None  # "#c3c3c3"
        self.selectBorderWidth = None  # 0
        self.selectForeground = None  # "#000000"
        self.state = None  # normal
        self.validate = None  # none
        self.width = None  # 20


class Frame(_Style):
    _WIDGET_CLASS = "Frame"

    def __init__(self):
        self.background = None  # "#d9d9d9"
        self.borderWidth = None  # 0
        self.class_ = None  # Frame
        self.container = None  # 0
        self.height = None  # 0
        self.highlightBackground = None  # "#d9d9d9"
        self.highlightColor = None  # "#000000"
        self.highlightThickness = None  # 0
        self.padX = None  # 0
        self.padY = None  # 0
        self.relief = None  # flat
        self.takeFocus = None  # 0
        self.width = None  # 0


class Label(_Style):
    _WIDGET_CLASS = "Label"

    def __init__(self):
        self.activeBackground = None  # "#ececec"
        self.activeForeground = None  # "#000000"
        self.anchor = None  # center
        self.background = None  # "#d9d9d9"
        self.borderWidth = None  # 1
        self.compound = None  # none
        self.disabledForeground = None  # "#a3a3a3"
        self.font = None  # TkDefaultFont
        self.foreground = None  # # 000000
        self.height = None  # 0
        self.highlightBackground = None  # "#d9d9d9"
        self.highlightColor = None  # "#000000"
        self.highlightThickness = None  # 0
        self.justify = None  # center
        self.padX = None  # 1
        self.padY = None  # 1
        self.relief = None  # flat
        self.state = None  # normal
        self.takeFocus = None  # 0
        self.underline = None  # -1
        self.width = None  # 0
        self.wrapLength = None  # 0


class LabelFrame(_Style):
    _WIDGET_CLASS = "Labelframe"

    def __init__(self):
        self.background = None  # "#d9d9d9"
        self.borderWidth = None  # 2
        self.class_ = None  # Labelframe
        self.container = None  # 0
        self.font = None  # TkDefaultFont
        self.foreground = None  # "#000000"
        self.height = None  # 0
        self.highlightBackground = None  # "#d9d9d9"
        self.highlightColor = None  # "#000000"
        self.highlightThickness = None  # 0
        self.labelAnchor = None  # nw
        self.padX = None  # 0
        self.padY = None  # 0
        self.relief = None  # groove
        self.takeFocus = None  # 0
        self.width = None  # 0


class Listbox(_Style):
    _WIDGET_CLASS = "Listbox"

    def __init__(self):
        self.activeStyle = None  # dotbox
        self.background = None  # "#ffffff"
        self.borderWidth = None  # 1
        self.disabledForeground = None  # "#a3a3a3"
        self.exportSelection = None  # 1
        self.font = None  # TkDefaultFont
        self.foreground = None  # "#000000"
        self.height = None  # 10
        self.highlightBackground = None  # "#d9d9d9"
        self.highlightColor = None  # "#000000"
        self.highlightThickness = None  # 1
        self.justify = None  # left
        self.relief = None  # sunken
        self.selectBackground = None  # "#c3c3c3"
        self.selectBorderWidth = None  # 0
        self.selectForeground = None  # "#000000"
        self.selectMode = None  # browse
        self.setGrid = None  # 0
        self.state = None  # normal
        self.width = None  # 20


class Menu(_Style):
    _WIDGET_CLASS = "Menu"

    def __init__(self):
        self.activeBackground = None  # "#ececec"
        self.activeBorderWidth = None  # 1
        self.activeForeground = None  # "#000000"
        self.background = None  # "#d9d9d9"
        self.borderWidth = None  # 1
        self.cursor = None  # arrow
        self.disabledForeground = None  # "#a3a3a3"
        self.font = None  # TkMenuFont
        self.foreground = None  # "#000000"
        self.relief = None  # raised
        self.selectColor = None  # "#000000"
        self.takeFocus = None  # 0
        self.tearOff = None  # 1
        self.type = None  # normal


class Menubutton(_Style):
    _WIDGET_CLASS = "Menubutton"

    def __init__(self):
        self.activeBackground = None  # "#ececec"
        self.activeForeground = None  # "#000000"
        self.anchor = None  # center
        self.background = None  # "#d9d9d9"
        self.borderWidth = None  # 1
        self.compound = None  # none
        self.direction = None  # below
        self.disabledForeground = None  # "#a3a3a3"
        self.font = None  # TkDefaultFont
        self.foreground = None  # #000000
        self.height = None  # 0
        self.highlightBackground = None  # "#d9d9d9"
        self.highlightColor = None  # "#000000"
        self.highlightThickness = None  # 0
        self.indicatorOn = None  # 0
        self.justify = None  # center
        self.padX = None  # 4p
        self.padY = None  # 3p
        self.relief = None  # flat
        self.state = None  # normal
        self.takeFocus = None  # 0
        self.underline = None  # -1
        self.width = None  # 0
        self.wrapLength = None  # 0


class OptionMenu(_Style):
    _WIDGET_CLASS = "OptionMenu"

    def __init__(self):
        self.activeBackground = None  # "#ececec"
        self.activeForeground = None  # "#000000"
        self.anchor = None  # center
        self.background = None  # "#d9d9d9"
        self.borderWidth = None  # 2
        self.compound = None  # none
        self.cursor = None  #
        self.direction = None  # below
        self.disabledForeground = None  # #a3a3a3
        self.font = None  # TkDefaultFont
        self.foreground = None  # #000000
        self.height = None  # 0
        self.highlightBackground = None  # #d9d9d9
        self.highlightColor = None  # #000000
        self.highlightThickness = None  # 2
        self.image = None  #
        self.indicatorOn = None  # 1
        self.justify = None  # center
        self.menu = None  # .140544366545328.menu
        self.padX = None  # 5
        self.padY = None  # 4
        self.relief = None  # raised
        self.state = None  # normal
        self.takeFocus = None  # 0
        self.text = None  #
        self.textVariable = None  # PY_VAR0
        self.underline = None  # -1
        self.width = None  # 0
        self.wrapLength = None  # 0


class PanedWindow(_Style):
    _WIDGET_CLASS = "Panedwindow"

    def __init__(self):
        self.background = None  # "#d9d9d9"
        self.borderWidth = None  # 1
        self.handlePad = None  # 8
        self.handleSize = None  # 8
        self.opaqueResize = None  # 1
        self.orient = None  # horizontal
        self.proxyBorderWidth = None  # 2
        self.relief = None  # flat
        self.sashPad = None  # 0
        self.sashRelief = None  # flat
        self.sashWidth = None  # 3
        self.showHandle = None  # 0


class Radiobutton(_Style):
    _WIDGET_CLASS = "Radiobutton"

    def __init__(self):
        self.activeBackground = None  # #ececec
        self.activeForeground = None  # #000000
        self.anchor = None  # center
        self.background = None  # #d9d9d9
        self.borderWidth = None  # 1
        self.compound = None  # none
        self.disabledForeground = None  # #a3a3a3
        self.font = None  # TkDefaultFont
        self.foreground = None  # #000000
        self.height = None  # 0
        self.highlightBackground = None  # #d9d9d9
        self.highlightColor = None  # #000000
        self.highlightThickness = None  # 1
        self.indicatorOn = None  # 1
        self.justify = None  # center
        self.offRelief = None  # raised
        self.padX = None  # 1
        self.padY = None  # 1
        self.relief = None  # flat
        self.selectColor = None  # #ffffff
        self.state = None  # normal
        self.underline = None  # -1
        self.variable = None  # selectedButton
        self.width = None  # 0
        self.wrapLength = None  # 0


class Scale(_Style):
    _WIDGET_CLASS = "Scale"

    def __init__(self):
        self.activeBackground = None  # #ececec
        self.background = None  # #d9d9d9
        self.bigIncrement = None  # 0
        self.borderWidth = None  # 1
        self.digits = None  # 0
        self.font = None  # TkDefaultFont
        self.foreground = None  # #000000
        self.from_ = None  # 0
        self.highlightBackground = None  # #d9d9d9
        self.highlightColor = None  # #000000
        self.highlightThickness = None  # 1
        self.length = None  # 100
        self.orient = None  # vertical
        self.relief = None  # flat
        self.repeatDelay = None  # 300
        self.repeatInterval = None  # 100
        self.resolution = None  # 1
        self.showValue = None  # 1
        self.sliderLength = None  # 30
        self.sliderRelief = None  # raised
        self.state = None  # normal
        self.tickInterval = None  # 0
        self.to = None  # 100
        self.troughColor = None  # #b3b3b3
        self.width = None  # 15


class Scrollbar(_Style):
    _WIDGET_CLASS = "Scrollbar"

    def __init__(self):
        self.activeBackground = None  # #ececec
        self.activeRelief = None  # raised
        self.background = None  # #d9d9d9
        self.borderWidth = None  # 1
        self.elementBorderWidth = None  # -1
        self.highlightBackground = None  # #d9d9d9
        self.highlightColor = None  # #000000
        self.highlightThickness = None  # 0
        self.jump = None  # 0
        self.orient = None  # vertical
        self.relief = None  # sunken
        self.repeatDelay = None  # 300
        self.repeatInterval = None  # 100
        self.troughColor = None  # #b3b3b3
        self.width = None  # 11


class Spinbox(_Style):
    _WIDGET_CLASS = "Spinbox"

    def __init__(self):
        self.activeBackground = None  # #ececec
        self.background = None  # #ffffff
        self.borderWidth = None  # 1
        self.cursor = None  # xterm
        self.disabledBackground = None  # #d9d9d9
        self.disabledForeground = None  # #a3a3a3
        self.exportSelection = None  # 1
        self.font = None  # TkTextFont
        self.foreground = None  # #000000
        self.from_ = None  # 0
        self.highlightBackground = None  # #d9d9d9
        self.highlightColor = None  # #000000
        self.highlightThickness = None  # 1
        self.increment = None  # 1
        self.insertBackground = None  # #000000
        self.insertBorderWidth = None  # 0
        self.insertOffTime = None  # 300
        self.insertOnTime = None  # 600
        self.insertWidth = None  # 2
        self.justify = None  # left
        self.readonlyBackground = None  # #d9d9d9
        self.relief = None  # sunken
        self.repeatDelay = None  # 400
        self.repeatInterval = None  # 100
        self.selectBackground = None  # #c3c3c3
        self.selectBorderWidth = None  # 0
        self.selectForeground = None  # #000000
        self.state = None  # normal
        self.to = None  # 0
        self.validate = None  # none
        self.width = None  # 20
        self.wrap = None  # 0


class Text(_Style):
    _WIDGET_CLASS = "Text"

    def __init__(self):
        self.autoSeparators = None  # 1
        self.background = None  # "#ffffff"
        self.blockCursor = None  # 0
        self.borderWidth = None  # 1
        self.cursor = None  # xterm
        self.exportSelection = None  # 1
        self.font = None  # TkFixedFont
        self.foreground = None  # #000000
        self.height = None  # 24
        self.highlightBackground = None  # #d9d9d9
        self.highlightColor = None  # #000000
        self.highlightThickness = None  # 1
        self.inactiveSelectBackground = None  # #c3c3c3
        self.insertBackground = None  # #000000
        self.insertBorderWidth = None  # 0
        self.insertOffTime = None  # 300
        self.insertOnTime = None  # 600
        self.insertUnfocussed = None  # none
        self.insertWidth = None  # 2
        self.maxUndo = None  # 0
        self.padX = None  # 1
        self.padY = None  # 1
        self.relief = None  # sunken
        self.selectBackground = None  # #c3c3c3
        self.selectBorderWidth = None  # 0
        self.selectForeground = None  # #000000
        self.setGrid = None  # 0
        self.spacing1 = None  # 0
        self.spacing2 = None  # 0
        self.spacing3 = None  # 0
        self.state = None  # normal
        self.tabStyle = None  # tabular
        self.undo = None  # 0
        self.width = None  # 80
        self.wrap = None  # "char"


class Toplevel(_Style):
    _WIDGET_CLASS = "Toplevel"

    def __init__(self):
        self.background = None  # "#d9d9d9"
        self.borderWidth = None  # 0
        self.class_ = None  # "Toplevel"
        self.container = None  # 0
        self.height = None  # 0
        self.highlightBackground = None  # "#d9d9d9"
        self.highlightColor = None  # "#000000"
        self.highlightThickness = None  # 0
        self.padX = None  # 0
        self.padY = None  # 0
        self.relief = None  # "flat"
        self.takeFocus = None  # 0
        self.width = None  # 0
