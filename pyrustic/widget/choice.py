import tkinter as tk
from pyrustic import tkmisc
from pyrustic.widget.scrollbox import Scrollbox
from pyrustic.viewable import Viewable


# button flavor
CHECK = "check"  # for checkbutton
RADIO = "radio"  # for radiobutton

# Components
BODY = "body"
LABEL_HEADER = "label_header"
SCROLLBOX = "scrollbox"
LABEL_MESSAGE = "label_message"
TEXT_MESSAGE = "text_message"
FRAME_PANE = "frame_pane"
FRAME_FOOTER = "frame_footer"
BUTTON_CONTINUE = "button_continue"
BUTTON_CANCEL = "button_cancel"
RADIOBUTTONS = "radiobuttons"
CHECKBUTTONS = "checkbuttons"


class Choice(Viewable):
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
                 is_long_message=False,
                 use_scrollbox=False,
                 items=(),
                 selected=None,
                 flavor="radio",
                 handler=None,
                 geometry=None,
                 options=None):
        """
        PARAMETERS:

        - master: widget parent. Example: an instance of tk.Frame

        - title: title of dialog box

        - header: the text to show as header

        - message: the text to show as message

        - is_long_message: bool, set it to True if you want the message
        widget to be a Text. Set it to False if you want the message to be a Label

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
            The widgets keys are: BODY, LABEL_HEADER, SCROLLBOX, LABEL_MESSAGE, TEXT_MESSAGE,
            FRAME_PANE, FRAME_FOOTER, BUTTON_CONTINUE, BUTTON_CANCEL,
            RADIOBUTTONS, CHECKBUTTONS.

            Example: Assume that you want to set the LABEL_MESSAGE's background to black
            and the BODY's background to red:
                options = { BODY: {"background": "red"},
                            LABEL_MESSAGE: {"background": "black"} }

        """
        self._master = master
        self._title = title
        self._header = header
        self._message = message
        self._is_long_message = is_long_message
        self._use_scrollbox = use_scrollbox
        self._items = items
        self._selected = selected
        self._flavor = flavor
        self._handler = handler
        self._geometry = geometry
        self._options = {} if options is None else options
        #
        self._body_options = None
        self._label_header_options = None
        self._scrollbox_options = None
        self._label_message_options = None
        self._text_message_options = None
        self._frame_pane_options = None
        self._frame_footer_options = None
        self._button_continue_options = None
        self._button_cancel_options = None
        self._checkbutton_options = None
        self._radiobutton_options = None
        self._parse_options(self._options)
        #
        self._result = None
        self._closing_context = "close"
        self._components = dict()
        self._body = None
        self._label_header = None
        self._label_message = None
        self._pane = None
        self._footer = None
        self._buttons = None
        self._intvar = tk.IntVar()
        self._intvars = []
        # components
        self._components = {}

    # ======================================
    #            PROPERTIES
    # ======================================
    @property
    def master(self):
        return self._master

    @property
    def title(self):
        return self._title

    @property
    def header(self):
        return self._header

    @property
    def message(self):
        return self._message

    @property
    def is_long_message(self):
        return self._is_long_message

    @property
    def items(self):
        return self._items.copy()

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
        return self._result

    @property
    def flavor(self):
        return self._flavor

    @property
    def handler(self):
        return self._handler

    @property
    def geometry(self):
        return self._geometry

    @property
    def options(self):
        return self._options

    @property
    def components(self):
        """
        Get the components (widgets instances) used to build this dialog.

        This property returns a dict. The keys are:
            BODY, LABEL_HEADER, SCROLLBOX, LABEL_MESSAGE, TEXT_MESSAGE,
            FRAME_PANE, FRAME_FOOTER, BUTTON_CONTINUE, BUTTON_CANCEL,
            RADIOBUTTONS, CHECKBUTTONS.

        Warning: radiobuttons and checkbuttons are sequences of widgets positioned
        in the sequence according to the index.

        Another Warning: check the presence of key before usage. Example,
        the widget linked to the LABEL_MESSAGE key may be missing because
        TEXT_MESSAGE replaced it
        """
        return self._components

    # ======================================
    #            INTERNAL
    # ======================================
    def _on_build(self):
        self._body = tk.Toplevel(self._master,
                                 class_="Choice",
                                 cnf=self._body_options)
        self._body.resizable(0, 0)
        self._components[BODY] = self._body
        self._body.title(self._title)
        #
        if self._geometry:
            self._body.geometry(self._geometry)
        #
        if self._header:
            label_header = tk.Label(self._body,
                                    name="header",
                                    justify=tk.LEFT,
                                    anchor="w",
                                    cnf=self._label_header_options)
            self._components[LABEL_HEADER] = label_header
            label_header.pack(fill=tk.X, anchor="w",
                                    padx=(5, 0), pady=(5, 5))
            label_header.config(text=self._header)
        # Scrollbox
        container = self._body
        if self._use_scrollbox:
            scrollbox = Scrollbox(self._body,
                                  options=self._scrollbox_options)
            self._components[SCROLLBOX] = scrollbox
            scrollbox.build_pack(expand=1, fill=tk.BOTH)
            container = scrollbox.box
        if self._message:
            if self._is_long_message:
                text_message = tk.Text(container,
                                       wrap="word",
                                       width=35,
                                       height=5,
                                       name="long_message",
                                       cnf=self._text_message_options)
                self._components[TEXT_MESSAGE] = text_message
                text_message.pack(fill=tk.BOTH, expand=1, padx=5, pady=5)
                text_message.insert("end", self._message)
                text_message.config(state="disabled")
            else:
                label_message = tk.Label(container,
                                         name="message",
                                         justify=tk.LEFT,
                                         anchor="w",
                                         cnf=self._label_message_options)
                self._components[LABEL_MESSAGE] = label_message
                label_message.pack(fill=tk.X, anchor="w",
                                         padx=(5, 0), pady=(0, 5))
                label_message.config(text=self._message)
        #
        pane = tk.Frame(container,
                        name="pane",
                        cnf=self._frame_pane_options)
        self._components[FRAME_PANE] = pane
        pane.pack(fill=tk.X, anchor="w", pady=(0, 10))
        #
        self._footer = tk.Frame(self._body,
                                name="footer",
                                cnf=self._frame_footer_options)
        self._components[FRAME_FOOTER] = self._footer
        self._footer.pack(side=tk.BOTTOM, fill=tk.X, pady=(30, 0))
        #
        button_continue = tk.Button(self._footer, name="continue",
                                    text="Continue",
                                    command=self._on_click_continue,
                                    cnf=self._button_continue_options)
        self._components[BUTTON_CONTINUE] = button_continue
        button_continue.pack(side=tk.RIGHT, padx=2, pady=2)
        #
        button_cancel = tk.Button(self._footer, name="cancel",
                                  text="Cancel",
                                  command=self._on_click_cancel,
                                  cnf=self._button_cancel_options)
        self._components[BUTTON_CANCEL] = button_cancel
        button_cancel.pack(side=tk.RIGHT, pady=2)
        # install and populate check/radio buttons
        key = RADIOBUTTONS if self._flavor == "radio" else CHECKBUTTONS
        self._components[key] = []
        cache = None
        for i, choice in enumerate(self._items):
            if not self._flavor or self._flavor not in ("radio", "check"):
                break
            if self._flavor == "radio":
                cache = tk.Radiobutton(pane,
                                       variable=self._intvar,
                                       text=choice, value=i)
                self._components[RADIOBUTTONS].append(cache)
            elif self._flavor == "check":
                tk_var = tk.IntVar()
                self._intvars.append(tk_var)
                cache = tk.Checkbutton(pane,
                                       variable=tk_var,
                                       onvalue=1, offvalue=0,
                                       text=choice)
                self._components[CHECKBUTTONS].append(cache)
            if cache:
                cache.pack(anchor="w", expand=1)

    def _on_display(self):
        # fill selected items
        if self._flavor == RADIO and self._selected is not None:
            if isinstance(self._selected, int) and self._selected >= 0:
                self._intvar.set(self._selected)
        elif self._flavor == CHECK and self._selected is not None:
            if isinstance(self._selected, tuple):
                for i in self._selected:
                    try:
                        self._intvars[i].set(1)
                    except IndexError:
                        pass
            elif isinstance(self._selected, int):
                self._intvars[self._selected].set(1)

    def _on_destroy(self):
        if self._closing_context == "continue":
            self._result = self._get_result()
        if self._handler:
            self._handler(self._result)

    def _toplevel_geometry(self):
        super()._toplevel_geometry()
        tkmisc.dialog_effect(self._body)

    def _on_click_continue(self):
        self._closing_context = "continue"
        self._body.destroy()

    def _on_click_cancel(self):
        self._closing_context = "cancel"
        self._body.destroy()

    def _get_result(self):
        result = None
        if self._flavor == "radio":
            index = self._intvar.get()
            result = (index, self._items[index])
        elif self._flavor == "check":
            cache = []
            for i, intvar in enumerate(self._intvars):
                intvar_index = intvar.get()
                cache.append((intvar_index, self._items[i]))
            result = tuple(cache)
        return result

    def _parse_options(self, options):
        self._body_options = (options[BODY] if BODY in options else {})
        self._label_header_options = (options[LABEL_HEADER]
                                      if LABEL_HEADER in options else {})
        self._scrollbox_options = (options[SCROLLBOX]
                                   if SCROLLBOX in options else {})
        self._label_message_options = (options[LABEL_MESSAGE]
                                       if LABEL_MESSAGE in options else {})
        self._text_message_options = (options[TEXT_MESSAGE]
                                      if TEXT_MESSAGE in options else {})
        self._frame_pane_options = (options[FRAME_PANE]
                                    if FRAME_PANE in options else {})
        self._frame_footer_options = (options[FRAME_FOOTER]
                                      if FRAME_FOOTER in options else {})
        self._button_continue_options = (options[BUTTON_CONTINUE]
                                         if BUTTON_CONTINUE in options else {})
        self._button_cancel_options = (options[BUTTON_CANCEL]
                                       if BUTTON_CANCEL in options else {})
        self._checkbutton_options = (options[CHECKBUTTONS]
                                     if CHECKBUTTONS in options else {})
        self._radiobutton_options = (options[RADIOBUTTONS]
                                     if RADIOBUTTONS in options else {})


class _ChoiceTest(Viewable):
    def __init__(self, root):
        self._root = root
        self._body = None

    def _on_build(self):
        self._body = tk.Frame(self._body)
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
        choice = Choice(self._root, title="Title", header="header", flavor="check",
                        message="message", geometry=None,
                        items=["first", "second", "third"],
                        selected=1, handler=self._choice_handler)
        choice.build_wait()

    def _on_click_btn_radio(self):
        tests = ("test "*10).split()
        choice = Choice(self._root, title="Title", header="header", flavor="radio",
                        use_scrollbox=True, is_long_message=True,
                        message="message", geometry=None,
                        items=["first", "second", "third", *tests],
                        selected=1, handler=self._choice_handler)
        choice.build_wait()

    def _choice_handler(self, data):
        print("Choice: {}".format(data))


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("500x300+0+0")
    choice_test = _ChoiceTest(root)
    choice_test.build_pack()
    root.mainloop()
