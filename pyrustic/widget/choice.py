import tkinter as tk
from pyrustic import tkmisc
from pyrustic import widget
from pyrustic.widget.scrollbox import Scrollbox
from pyrustic.view import View
from pyrustic.tkmisc import merge_cnfs


# select button flavor
CHECK = "check"  # for checkbutton
RADIO = "radio"  # for radiobutton


# Components
LABEL_HEADER = "label_header"
SCROLLBOX = "scrollbox"
LABEL_MESSAGE = "label_message"
FRAME_PANE = "frame_pane"
FRAME_FOOTER = "frame_footer"
BUTTON_CONTINUE = "button_continue"
BUTTON_CANCEL = "button_cancel"
RADIOBUTTONS = "radiobuttons"
CHECKBUTTONS = "checkbuttons"


class Choice(widget.Toplevel):
    """
    Choice is a dialog box to make the user select some items among others.
    The Choice could be implemented with either radiobuttons or checkbuttons.

    Example:

        import tkinter as tk
        from pyrustic.widget.choice import Choice

        def my_handler(result):
            print(result)

        root = tk.Tk()
        my_items = ("first", "second", "third")
        choice = Choice(root, title="Choice", header="Make a choice",
                        items=my_items, handler=my_handler)
        choice.build()
        root.mainloop()

    """

    def __init__(self,
                 master=None,
                 title=None,
                 header=None,
                 message=None,
                 items=None,
                 selected=None,
                 flavor="radio",
                 handler=None,
                 geometry=None,
                 cnfs=None):
        """
        PARAMETERS:

        - master: widget parent. Example: an instance of tk.Frame

        - title: title of dialog box

        - header: the text to show as header

        - message: the text to show as message

        - use_scrollbox: bool, set it to True to make the Dialog scrollable

        - items: a sequence of strings. Example: ("banana", "apple").

        - selected: a sequence of indexes to indicate default selection.
        Set it to None if u don't need it.

        - flavor: it could be either RADIO or CHECK
        for respectively radiobutton and checkbutton

        - handler: a callback to be executed immediately
        after closing the dialog box.
        The callback should allow one parameter, the result:

            - If the flavor is RADIO,
             then, result is a tuple like: (the selected index, item string).

            - If the flavor is CHECK,
             then, result is a sequence of tuples.
             Each tuple is like: (integer, item string),
             with integer being 1 if the button has been clicked, else 0.

        - geometry: str, as the dialog box is a toplevel (BODY),
         you can edit its geometry. Example: "500x300"

        - options: dictionary of widgets options
            The widgets keys are: BODY, LABEL_HEADER, SCROLLBOX, LABEL_MESSAGE,
            FRAME_PANE, FRAME_FOOTER, BUTTON_CONTINUE, BUTTON_CANCEL,
            RADIOBUTTONS, CHECKBUTTONS.

            Example: Assume that you want to set the LABEL_MESSAGE's background to black
            and the BODY's background to red:
                options = { BODY: {"background": "red"},
                            LABEL_MESSAGE: {"background": "black"} }

        """
        self.__cnfs = merge_cnfs(None, cnfs, components=("body",
                                LABEL_HEADER, SCROLLBOX, LABEL_MESSAGE,
                                FRAME_PANE, FRAME_FOOTER, BUTTON_CONTINUE,
                                BUTTON_CANCEL, RADIOBUTTONS, CHECKBUTTONS))
        super().__init__(master=master,
                         class_="Choice",
                         cnf=self.__cnfs["body"],
                         on_build=self.__on_build,
                         on_display=self.__on_display,
                         on_destroy=self.__on_destroy,
                         toplevel_geometry=self.__toplevel_geometry)
        self.__title = title
        self.__header = header
        self.__message = message
        self.__items = [] if not items else items
        self.__selected = selected
        self.__flavor = flavor
        self.__handler = handler
        self.__geometry = geometry
        #
        self.__result = None
        self.__closing_context = "close"
        self.__components = dict()
        self.__label_header = None
        self.__label_message = None
        self.__pane = None
        self.__footer = None
        self.__buttons = None
        self.__intvar = tk.IntVar()
        self.__intvars = []
        # components
        self.__components = {}
        # build
        self.__view = self.build()

    # ======================================
    #            PROPERTIES
    # ======================================

    @property
    def header(self):
        return self.__header

    @property
    def message(self):
        return self.__message

    @property
    def items(self):
        return self.__items.copy()

    @property
    def selected(self):
        """
        - If the flavor is RADIO,
             then, result is a tuple like: (the selected index, item string).
             Example: 3 items, the second has been selected:
                result = (1, "Item at index 1")

        - If the flavor is CHECK,
         then, result is a sequence of tuples, each positioned in
         the sequence according to its index number.
         Each tuple is like: (integer, item string),
         with integer being 1 if the button has been clicked, else 0.
         Example: 3 items, only the last 2 are checked:
            result = ( (0, "item 1"), (1, "item 2"), (1, "item 3") )
        """
        return self.__result

    @property
    def flavor(self):
        return self.__flavor

    @property
    def handler(self):
        return self.__handler

    @property
    def components(self):
        """
        Get the components (widgets instances) used to build this dialog.

        This property returns a dict. The keys are:
            BODY, LABEL_HEADER, SCROLLBOX, LABEL_MESSAGE,
            FRAME_PANE, FRAME_FOOTER, BUTTON_CONTINUE, BUTTON_CANCEL,
            RADIOBUTTONS, CHECKBUTTONS.

        Warning: radiobuttons and checkbuttons are sequences of widgets positioned
        in the sequence according to the index.

        Another Warning: check the presence of key before usage.
        """
        return self.__components

    # ======================================
    #            INTERNAL
    # ======================================
    def __on_build(self):
        self.title(self.__title)
        self.resizable(0, 0)
        #
        if self.__geometry:
            self.geometry(self.__geometry)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=0)
        self.rowconfigure(2, weight=2, uniform="a")
        self.rowconfigure(3, weight=0, uniform="a")
        # == Set Header
        if self.__header:
            label_header = tk.Label(self,
                                    name=LABEL_HEADER,
                                    text=self.__header,
                                    justify=tk.LEFT,
                                    anchor="w",
                                    cnf=self.__cnfs[LABEL_HEADER])
            self.__components[LABEL_HEADER] = label_header
            label_header.grid(row=0, column=0, sticky="w",
                                    padx=(5, 5), pady=(5, 5))
            label_header.config(text=self.__header)
        # == Set Message
        if self.__message:
            label_message = tk.Label(self,
                                     name=LABEL_MESSAGE,
                                     text=self.__message,
                                     justify=tk.LEFT,
                                     anchor="w",
                                     cnf=self.__cnfs[LABEL_MESSAGE])
            self.__components[LABEL_MESSAGE] = label_message
            label_message.grid(row=1, column=0, sticky="w",
                               padx=(5, 5), pady=(0, 5))
        # == Scrollbox
        scrollbox = Scrollbox(self, orient="vertical",
                              cnfs=self.__cnfs[SCROLLBOX])
        self.__components[SCROLLBOX] = scrollbox
        scrollbox.grid(row=2, column=0, sticky="nswe",
                             padx=5)
        # == Footer
        self.__footer = tk.Frame(self,
                                 name=FRAME_FOOTER,
                                 cnf=self.__cnfs[FRAME_FOOTER])
        self.__components[FRAME_FOOTER] = self.__footer
        self.__footer.grid(row=3, column=0, sticky="swe", pady=(30, 0))
        #
        button_continue = tk.Button(self.__footer, name=BUTTON_CONTINUE,
                                    text="Continue",
                                    command=self.__on_click_continue,
                                    cnf=self.__cnfs[BUTTON_CONTINUE])
        self.__components[BUTTON_CONTINUE] = button_continue
        button_continue.pack(side=tk.RIGHT, padx=2, pady=2)
        #
        button_cancel = tk.Button(self.__footer, name=BUTTON_CANCEL,
                                  text="Cancel",
                                  command=self.__on_click_cancel,
                                  cnf=self.__cnfs[BUTTON_CANCEL])
        self.__components[BUTTON_CANCEL] = button_cancel
        button_cancel.pack(side=tk.RIGHT, padx=(2, 0), pady=2)
        # install and populate check/radio buttons
        key = RADIOBUTTONS if self.__flavor == "radio" else CHECKBUTTONS
        self.__components[key] = []
        cache = None
        for i, choice in enumerate(self.__items):
            if not self.__flavor or self.__flavor not in ("radio", "check"):
                break
            if self.__flavor == "radio":
                cache = tk.Radiobutton(scrollbox.box,
                                       variable=self.__intvar,
                                       text=choice, value=i,
                                       cnf=self.__cnfs[RADIOBUTTONS])
                self.__components[RADIOBUTTONS].append(cache)
            elif self.__flavor == "check":
                tk_var = tk.IntVar()
                self.__intvars.append(tk_var)
                cache = tk.Checkbutton(scrollbox.box,
                                       variable=tk_var,
                                       onvalue=1, offvalue=0,
                                       text=choice,
                                       cnf=self.__cnfs[CHECKBUTTONS])
                self.__components[CHECKBUTTONS].append(cache)
            if cache:
                cache.pack(anchor="w", expand=1)

    def __on_display(self):
        # fill selected items
        if self.__flavor == RADIO and self.__selected is not None:
            if isinstance(self.__selected, int) and self.__selected >= 0:
                self.__intvar.set(self.__selected)
        elif self.__flavor == CHECK and self.__selected is not None:
            if isinstance(self.__selected, tuple):
                for i in self.__selected:
                    try:
                        self.__intvars[i].set(1)
                    except IndexError:
                        pass
            elif isinstance(self.__selected, int):
                self.__intvars[self.__selected].set(1)

    def __on_destroy(self):
        if self.__closing_context == "continue":
            self.__result = self.__get_result()
        if self.__handler:
            self.__handler(self.__result)

    def __toplevel_geometry(self):
        tkmisc.center_window(self, within=self.master.winfo_toplevel())
        tkmisc.dialog_effect(self)

    def __on_click_continue(self):
        self.__closing_context = "continue"
        self.destroy()

    def __on_click_cancel(self):
        self.__closing_context = "cancel"
        self.destroy()

    def __get_result(self):
        result = None
        if self.__flavor == "radio":
            index = self.__intvar.get()
            result = (index, self.__items[index])
        elif self.__flavor == "check":
            cache = []
            for i, intvar in enumerate(self.__intvars):
                intvar_index = intvar.get()
                cache.append((intvar_index, self.__items[i]))
            result = tuple(cache)
        return result


class _ChoiceTest(View):
    def __init__(self, root):
        super().__init__()
        self._root = root
        self._body = None

    def _on_build(self):
        self._body = tk.Frame(self._root)
        btn_launch_check_choice = tk.Button(self._body,
                                            text="Launch checkbutton choice",
                                            command=self._on_click_btn_check)
        btn_launch_check_choice.pack(side=tk.LEFT, anchor="nw")
        btn_launch_radio_choice = tk.Button(self._body,
                                            text="Launch radiobutton choice",
                                            command=self._on_click_btn_radio)
        btn_launch_radio_choice.pack(side=tk.LEFT, anchor="nw")


    def _on_display(self):
        pass

    def _on_destroy(self):
        pass

    def _on_click_btn_check(self):
        Choice(self._body, title="Title", header="header", flavor="check",
                        message="message",
                        items=["first", "second", "third"],
                        selected=1,
               handler=self._choice_handler)

    def _on_click_btn_radio(self):
        tests = ("test "*10).split()
        Choice(self._root,
               title="Title", header="header", flavor="radio",
               message="message",
               items=["first", "second", "third", *tests],
               selected=1, handler=self._choice_handler)

    def _choice_handler(self, data):
        print("Choice: {}".format(data))


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("500x300+0+0")
    choice_test = _ChoiceTest(root)
    choice_test.build_pack()
    root.mainloop()
