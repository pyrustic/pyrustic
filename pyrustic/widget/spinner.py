import tkinter as tk
from pyrustic.viewable import Viewable
from pyrustic import tkmisc


# Components
BODY = "body"
ENTRY = "entry"
DIALOG = "dialog"
LABEL_HEADER = "label_header"
LABELS = "labels"


class Spinner(Viewable):
    """
    Spinner is essentially an entry with a floating dialog to pick an item
    from a sequence of items.

    Example:

        import tkinter as tk
        from pyrustic.widget.spinner import Spinner

        def handler(data):
            print(data)

        root = tk.Tk()
        root.geometry("500x300+0+0")
        my_items = ("Lion", "Jaguar", "Eagle")
        spinner = Spinner(root, items=my_items, width=10,
                          selected=1, handler=handler)
        spinner.build_pack()
        root.mainloop()

    """
    def __init__(self,
                 master=None,
                 prompt="- Select -",
                 items=None,
                 selected=None,
                 width=None,
                 handler=None,
                 options=None):
        """
        PARAMETERS:

        - master: widget parent. Example: an instance of tk.Frame

        - prompt: str, prompt

        - items: a sequence of strings. Example: ("banana", "apple").

        - selected: int, index of the item to set as default

        - width: int, width of the Spinner. Actually it is the ENTRY width.

        - handler: a callback to be executed immediately
        after picking an item in the dialog box.
        The callback should allow one parameter, the result:
            - if the user picks the prompt, the result is None,
            - else the result is a tuple like: (index, str item)
            Example: None or (0, "item 1")

        - options: dictionary of widgets options.
            The widgets keys are: BODY, ENTRY, DIALOG, LABEL_HEADER, LABELS.

        """
        self._master = master
        self._prompt = prompt
        self._items = () if not items else items
        self._selected = selected
        self._width = width
        self._handler = handler
        self._body_options = None
        self._entry_options = None
        self._options = {} if options is None else options
        self._body_options = None
        self._parse_options(self._options)
        self._stringvar = tk.StringVar()
        self._index = selected
        self._dialog = None
        self._is_dialog_expanded = False
        self._body = None

    # ==============================================
    #                   PROPERTIES
    # ==============================================

    @property
    def master(self):
        return self._master

    @property
    def body(self):
        return self._body

    @property
    def prompt(self):
        return self._prompt

    @property
    def items(self):
        return self._items

    @property
    def selected(self):
        """
        If the user picks the prompt, this method returns None.
        Else this method returns a tuple like: (index, str item)

        Example: None or (0, "item 1")
        """
        if self._index is None or not self._items:
            return None
        return self._index, self._items[self._index]


    # ==============================================
    #               PUBLIC METHODS
    # ==============================================
    def select(self, index=None):
        """
        Selects an item (integer) or the prompt (None)
        """
        self._index = index
        self._update_entry()
        # call callback
        if self._handler:
            self._handler(self.selected)

    # ==============================================
    #               LIFECYCLE
    # ==============================================
    def _on_build(self):
        self._body = tk.Frame(self._master,
                              class_="Spinner", cnf=self._body_options)
        entry = tk.Entry(self._body,
                         textvariable=self._stringvar,
                         state="readonly",
                         width=self._width,
                         cnf=self._entry_options)
        entry.pack()
        # bind
        entry.bind("<Button-1>",
                   lambda event,
                          self=self:
                   self._on_click_entry(event),
                   "+")
        entry.bind("<Up>", lambda event,
                                  self=self:
                                        self._on_key_up_entry(event))
        entry.bind("<Down>", lambda event,
                                    self=self:
                                        self._on_key_down_entry(event))

    def _on_display(self):
        self._update_entry()

    def _on_destroy(self):
        pass

    # ==============================================
    #                   PRIVATE
    # ==============================================
    def _on_close_dialog(self):
        self._dialog = None

    def _update_entry(self):
        if self._items:
            cache = self._prompt
            if self._index is not None:
                try:
                    cache = self._items[self._index]
                except Exception as e:
                    pass
            self._stringvar.set(cache)

    def _on_click_entry(self, event):
        if not self._dialog:
            self._dialog = _SpinnerDialog(self._body,
                                          self._prompt,
                                          self._items,
                                          self._index,
                                          self.select,
                                          self._on_close_dialog,
                                          self._options)
            self._dialog.build_wait()
        else:
            self._dialog.destroy()
            self._dialog = None

    def _on_key_up_entry(self, event):
        if not self._items:
            return
        if (self._index - 1) >= 0:
            self._index -= 1
            self._update_entry()

    def _on_key_down_entry(self, event):
        if not self._items:
            return
        if (self._index + 1) < len(self._items):
            self._index += 1
            self._update_entry()

    def _parse_options(self, options):
        self._body_options = options[BODY] if BODY in options else {}
        self._entry_options = options[ENTRY] if ENTRY in options else {}


class _SpinnerDialog(Viewable):
    def __init__(self, master, prompt, data, index,
                 callback, close_dialog_callback,
                 options=None):
        # master should not be None
        self._master = master
        self._prompt = prompt
        self._items = data
        self._index = index
        self._handler = callback
        self._close_dialog_callback = close_dialog_callback
        self._dialog_options = None
        self._label_header_options = None
        self._labels_options = None
        self._options = {} if options is None else options
        self._parse_options(self._options)

    def _on_build(self):
        # body
        self._body = tk.Toplevel(self._master,
                                 class_="SpinnerDialog",
                                 cnf=self._dialog_options)
        self._body.overrideredirect(1)
        self._body.bind("<Button-1>", self._on_close, "+")
        self._body.bind("<Escape>", self._on_close, "+")
        self._master.winfo_toplevel().bind("<Configure>", self._on_close, "+")
        # prompt
        label_header = tk.Label(self._body,
                                name="header",
                                cnf=self._label_header_options,
                                text=self._prompt)
        label_header.pack(anchor="w")
        label_header.bind("<Button-1>",
                   lambda event,
                          self=self:
                   self._handler())
        for index, item in enumerate(self._items):
            name = None
            if index == self._index:
                name = "selected"
            label = tk.Label(self._body,
                             name=name,
                             text=item,
                             anchor="w",
                             cnf=self._labels_options)
            label.pack(expand=1, fill=tk.X)
            label.bind("<Button-1>",
                       lambda event,
                              self=self,
                              index=index:
                                self._on_click_item(event, index))

    def _on_display(self):
        tkmisc.dialog_effect(self._body)

    def _on_destroy(self):
        pass

    def _toplevel_geometry(self):
        tkmisc.align_window(self._body, under=self._master)

    def _on_click_item(self, event, index):
        self._close_dialog_callback()
        self._handler(index)
        self._body.destroy()

    def _on_close(self, event):
        self._close_dialog_callback()
        self._body.destroy()

    def _parse_options(self, options):
        self._dialog_options = (options[DIALOG] if
                                DIALOG in options else {})
        self._label_header_options = (options[LABEL_HEADER] if
                                      LABEL_HEADER in options else {})
        self._labels_options = (options[LABELS] if
                                LABELS in options else {})


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("500x300+0+0")
    my_items = ("Lion", "Jaguar", "Eagle")
    spinner = Spinner(root, items=my_items, selected=0)
    spinner.build_pack()
    root.mainloop()
