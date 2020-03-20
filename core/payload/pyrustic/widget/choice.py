import tkinter as tk
import pyrustic.widget as pw
from pyrustic.widget.dialog import Dialog


# button flavor
CHECK = "check" # for checkbutton
RADIO = "radio" # for radiobutton


class Choice(Dialog):
    """
    Choice is based on Dialog. With Choice, you give the possibility to pick some options displayed
    on a dialog with help of radiobuttons or checkbuttons

    PARAMETERS
    ==========
    - parent: widget parent
    - title: title of dialog
    - header: the text to show above the radiobuttons or checkbuttons
    - items: a list of strings. Example: ['banana', 'apple']. Will show a pane with 2 items
    - selected: a list of indexes to indicate default selection. Set it to None if u don't need it
    - flavor: it could be 'radio' or 'check' for respectively radiobutton and checkbutton
    - handler: a callback to execute before the dialog close.
        The callback should have one parameter: index.
        If the flavor is 'radio', index is an integer, the selected index.
        If the flavor is 'check', index is a tuple of indexes selected.
    - options: dictionary, options to build the toplevel (body)
    - label_options: dictionary, options to build the label (header)
    - pane_options: dictionary, options to build the pane (frame to contain the check|radio buttons)
    - footer_options: dictionary, options to build the footer (frame to contain buttons Cancel|Continue)

    METHODS
    =======
    - show(self): show the choice and return result.
        If the flavor is 'radio', result is an integer, the selected index.
        If the flavor is 'check', result is a tuple of indexes selected.

    """


    def __init__(self, parent=None, title=None,
                 header=None, items=[], selected=None, handler=None,
                 flavor="radio", options={}, label_options={},
                 pane_options={}, footer_options={}):
        self._parent = parent
        self._title = title
        self._header = header
        self._items = items
        self._selected = selected
        self._handler = handler
        self._flavor = flavor
        self._handler = handler
        self._options = options
        self._label_options = label_options
        self._pane_options = pane_options
        self._footer_options = footer_options
        # ===
        self._body = None
        self._label = None
        self._pane = None
        self._footer = None
        self._radiobuttons = None
        self._checkbuttons = None
        self._buttons = None
        self._tk_variable = tk.IntVar()
        self._tk_variables = []

    def _on_start(self):
        pass

    def _on_build(self):
        max_height = 10 + len(self._items)
        maxi_width = len(self._header)
        for x in self._items:
            if len(x) > maxi_width:
                maxi_width = len(x)
        charsize = pw.charsize(char="0", family="Liberation Sans", weight="bold",
                               size="17")
        width = charsize * (maxi_width + 5)
        height = charsize * max_height

        #self._options = pw.merge(self._options, width=width, height=height)
        self._body = tk.Toplevel(self._parent,
                                class_="Choice", **self._options)
        self._label = tk.Label(self._body, name="header", anchor="w", **self._label_options)
        self._pane = tk.Frame(self._body, name="pane", **self._pane_options)
        self._footer = tk.Frame(self._body, name="footer", **self._footer_options)
        self._label.pack(fill=tk.X, anchor="w")
        self._pane.pack(fill=tk.X, anchor="w", pady=(0, 10))
        self._footer.pack(side=tk.BOTTOM, fill=tk.X)
        cache = None
        for i, choice in enumerate(self._items):
            if not self._flavor or self._flavor not in ("radio", "check"):
                break
            if self._flavor == "radio":
                cache = tk.Radiobutton(self._pane,
                                       variable=self._tk_variable,
                                       text=choice, value=i)
            elif self._flavor == "check":
                tk_var = tk.IntVar()
                self._tk_variables.append(tk_var)
                cache = tk.Checkbutton(self._pane,
                                       variable=tk_var,
                                       onvalue=1, offvalue=0,
                                       text=choice)
            if cache:
                cache.pack(anchor="w", expand=1)
        tk.Button(self._footer, name="continue", text="CONTINUE",
                  command=self._on_click_continue).pack(
            side=tk.RIGHT)
        tk.Button(self._footer, name="cancel",
                  text="CANCEL", command=self.close).pack(side=tk.RIGHT)
        self._body.title(self._title)
        self._label.config(text=self._header)
        return self._body

    def _on_display(self):
        # fill selected items
        if self._flavor == "radio" and self._selected is not None:
            if isinstance(self._selected, int) and self._selected >= 0:
                self._tk_variable.set(self._selected)
        elif self._flavor == "check" and self._selected is not None:
            if isinstance(self._selected, tuple):
                    for i in self._selected:
                        try:
                            self._tk_variables[i].set(1)
                        except IndexError:
                            pass

    def _on_close(self, result=None):
        if self._handler:
            self._handler(result)

    def _on_click_continue(self):
        if self._flavor == "radio":
            var = self._tk_variable.get()
            self.close(result=var)
        elif self._flavor == "check":
            result = []
            for item in self._tk_variables:
                result.append(item.get())
            self.close(result=tuple(result))


if __name__ == "__main__":
    app = tk.Tk()

    choice = Choice(title="titre", header="header", flavor="check",
                    items=["first", "second", "third"],
                    selected=(0,1,2))
    result = choice.show()
    print(result)
    app.mainloop()
