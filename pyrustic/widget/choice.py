import tkinter as tk
from pyrustic.widget.dialog import Dialog


# button flavor
CHECK = "check"  # for checkbutton
RADIO = "radio"  # for radiobutton


class Choice(Dialog):
    """
    Choice is based on Dialog. With Choice, you give the possibility to pick some options displayed
    on a dialog. The choice to make could be with radiobuttons or with checkbuttons

    Example:
        import tkinter as tk
        from pyrustic.widget.choice import Choice
        root = tk.Tk()
        my_handler = lambda result: print(result)
        Choice(root, title="Title", items=("first", "second", "third"), handler=my_handler)
        root.mainloop()

    """

    def __init__(self,
                 master=None,
                 title=None,
                 header=None,
                 message=None,
                 items=[],
                 selected=None,
                 flavor="radio",
                 handler=None,
                 geometry=None,
                 wait=True,
                 options={}):
        """
        - master: widget parent
        - title: title of dialog
        - header: the text to show as header
        - message: the text to show as message
        - items: a list of strings. Example: ['banana', 'apple']. Will show a pane with 2 items
        - selected: a list of indexes to indicate default selection. Set it to None if u don't need it
        - flavor: it could be 'radio' or 'check' for respectively radiobutton and checkbutton
        - handler: a callback to execute before the dialog close.
            The callback should have one parameter, the result:
            - If the flavor is 'radio', result is a tuple (the selected index, item string).
            - If the flavor is 'check', result is a sequence of tuples. Each tuple is like:
                (integer, item string), with integer being 1 if the button has been clicked, else 0.
        - options: dictionary, these options will be used as argument to the widget's constructors.
            The widgets are: 'body', 'label_header', 'label_message', 'frame_pane', 'frame_footer',
            'button_continue', 'button_cancel', 'radiobutton', 'checkbutton'.

            Example: Assume that you want to set the text_message's background to black
            and the body's background to red:
                options = {"body": {"background": "red"},
                           "text_message": {"background": "black"}}
        """
        self._master = master
        self._title = title
        self._header = header
        self._message = message
        self._items = items
        self._selected = selected
        self._flavor = flavor
        self._handler = handler
        self._geometry = geometry
        self._wait = wait
        self._options = options
        #
        self._body_options = None
        self._label_header_options = None
        self._label_message_options = None
        self._frame_pane_options = None
        self._frame_footer_options = None
        self._button_continue_options = None
        self._button_cancel_options = None
        self._checkbutton_options = None
        self._radiobutton_options = None
        self._parse_options(options)
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
        #
        if wait:
            self.build_wait()
        else:
            self.build()

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
    def items(self):
        return self._items.copy()

    @property
    def selected(self):
        if isinstance(self._selected, int):
            return self._selected
        return self._selected.copy()

    @property
    def handler(self):
        return self._handler

    @property
    def flavor(self):
        return self._flavor

    @property
    def geometry(self):
        return self._geometry

    @property
    def wait(self):
        return self._wait

    @property
    def options(self):
        return self._options

    @property
    def result(self):
        return self._result

    @property
    def components(self):
        """
        Get the components used to build this dialog.
        This property returns a dict. The keys are:
            'body', 'label_header', 'label_message', 'frame_pane', 'frame_footer',
            'button_continue', 'button_cancel', 'radiobutton_list', 'checkbutton_list'.
        Warning: radiobutton_list and checkbutton_list are sequences of widgets by index !
        """
        return self._components

    # ======================================
    #            INTERNAL
    # ======================================
    def _on_build(self):
        self._body = tk.Toplevel(self._master,
                                 class_="Choice",
                                 cnf=self._body_options)
        self._components["body"] = self._body
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
            self._components["label_header"] = label_header
            label_header.pack(fill=tk.X, anchor="w",
                                    padx=(5, 0), pady=(0, 5))
            label_header.config(text=self._header)
        if self._message:
            label_message = tk.Label(self._body,
                                     name="message",
                                     justify=tk.LEFT,
                                     anchor="w",
                                     cnf=self._label_message_options)
            self._components["label_message"] = label_message
            label_message.pack(fill=tk.X, anchor="w",
                                     padx=(5, 0), pady=(0, 5))
            label_message.config(text=self._message)
        #
        pane = tk.Frame(self._body,
                        name="pane",
                        cnf=self._frame_pane_options)
        self._components["frame_pane"] = pane
        pane.pack(fill=tk.X, anchor="w", pady=(0, 10))
        #
        self._footer = tk.Frame(self._body,
                                name="footer",
                                cnf=self._frame_footer_options)
        self._components["frame_footer"] = self._footer
        self._footer.pack(side=tk.BOTTOM, fill=tk.X)
        #
        button_continue = tk.Button(self._footer, name="continue",
                                    text="Continue",
                                    command=self._on_click_continue,
                                    cnf=self._button_continue_options)
        self._components["button_continue"] = button_continue
        button_continue.pack(side=tk.RIGHT)
        #
        button_cancel = tk.Button(self._footer, name="cancel",
                                  text="Cancel",
                                  command=self._on_click_cancel,
                                  cnf=self._button_cancel_options)
        self._components["button_cancel"] = button_cancel
        button_cancel.pack(side=tk.RIGHT)
        # install and populate check/radio buttons
        key = "radiobutton_list" if self._flavor == "radio" else "checkbutton_list"
        self._components[key] = []
        cache = None
        for i, choice in enumerate(self._items):
            if not self._flavor or self._flavor not in ("radio", "check"):
                break
            if self._flavor == "radio":
                cache = tk.Radiobutton(pane,
                                       variable=self._intvar,
                                       text=choice, value=i)
                self._components["radiobutton"].append(cache)
            elif self._flavor == "check":
                tk_var = tk.IntVar()
                self._intvars.append(tk_var)
                cache = tk.Checkbutton(pane,
                                       variable=tk_var,
                                       onvalue=1, offvalue=0,
                                       text=choice)
                self._components["checkbutton"].append(cache)
            if cache:
                cache.pack(anchor="w", expand=1)

    def _on_display(self):
        # fill selected items
        if self._flavor == "radio" and self._selected is not None:
            if isinstance(self._selected, int) and self._selected >= 0:
                self._intvar.set(self._selected)
        elif self._flavor == "check" and self._selected is not None:
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
        self._body_options = options["body"] if "body" in options else {}
        self._label_header_options = options["label_header"] if "label_header" in options else {}
        self._label_message_options = options["label_message"] if "label_message" in options else {}
        self._frame_pane_options = options["frame_pane"] if "frame_pane" in options else {}
        self._frame_footer_options = options["frame_footer"] if "frame_footer" in options else {}
        self._button_continue_options = (options["button_continue"]
                                         if "button_continue" in options else {})
        self._button_cancel_options = options["button_cancel"] if "button_cancel" in options else {}
        self._checkbutton_options = options["checkbutton"] if "checkbutton" in options else {}
        self._radiobutton_options = options["radiobutton"] if "radiobutton" in options else {}


if __name__ == "__main__":
    def handler(result):
        print("handler result:", result)

    def launch(app):
        Choice(app, title="Title", header="header", flavor="check",
               message="message", geometry=None,
               items=["first", "second", "third"],
               selected=1, handler=handler)

    app = tk.Tk()
    app.geometry("500x500+0+0")
    tk.Button(app, text="Launch Choice",
              command=lambda app=app: launch(app)).pack()
    app.mainloop()
