import tkinter as tk
import pyrustic.widget as pw
from pyrustic.widget.dialog import Dialog


class Toast(Dialog):
    """
    This is Toast ! Based on Dialog, this class pop-up a dialog for a duration.
    Click on the Toast will destroy it.

    PARAMETERS
    ==========
    - message: message to show
    - duration: in milliseconds. U can set None to duration to cancel the self-destroying timer
    - options: dictionary, options to build the toplevel (body).
        Example: {background="red"}
    - label_options: dictionary, options to build the label on toplevel.
        Example: {background="yellow", justify=tk.CENTER}
    - title: the title of the dialog

    METHODS
    =======
        show(self): show the toast

    EXAMPLE
    =======
        from tkinter import *
        app = Tk()
        Toast(message="this is a toast !", duration=3000).show() # will last 3 seconds !
        app.mainloop()

    """
    def __init__(self, parent=None, message="Hello Friend !", duration=4321,
                 options={}, label_options={}, title="Pyrustic Toast"):
        self._parent = parent
        self._message = message
        self._duration = duration
        self._options = options
        self._label_options = label_options
        self._title = title
        self._cancel_id = None
        self._body = None

    def show(self):
        return super().show(wait_window=False)

    def _on_start(self):
        pass

    def _on_build(self):
        maxi_width = len(self._message)
        max_height = 10
        if "\n" in self._message:
            split = self._message.split(sep="\n")
            maxi_width = 0
            for x in split:
                if len(x) > maxi_width:
                    maxi_width = len(x)
            max_height = max_height + len(split)
        charsize = pw.charsize(char="0", family="Liberation Sans", weight="bold",
                               size="17")
        width = charsize * (maxi_width+5)
        height = charsize * max_height

        #self._options = pw.merge(self._options, width=width, height=height)
        self._body = tk.Toplevel(self._parent, class_="Toast", **self._options)
        self._body.overrideredirect(1)
        #self._body.title(self._title)
        self._body.bind("<Button-1>", self._on_click, "+")
        label = tk.Label(self._body, text=self._message,
                 **self._label_options)
        label.pack(expand=1, fill=tk.BOTH, padx=10, pady=10, anchor="w")
        #text.insert("0.0", self._message)
        return self._body

    def _on_display(self):
        if self._duration is not None:
            self._cancel_id = self._body.after(self._duration, self.close)

    def _on_close(self, result=None):
        pass

    def _on_click(self, event):
        if self._body:
            if self._cancel_id is not None:
                self._body.after_cancel(self._cancel_id)
            self._body.destroy()


if __name__ == "__main__":
    app = tk.Tk()
    Toast().show()
    app.mainloop()
