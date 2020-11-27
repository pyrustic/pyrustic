import tkinter as tk
from pyrustic.viewable import Viewable
from pyrustic import tkmisc


class FailureView(Viewable):
    def __init__(self, master, main_view, main_host, data):
        self._master = master
        self._main_view = main_view
        self._main_host = main_host
        self._data = data
        self._body = None

    def _on_build(self):
        self._body = tk.Toplevel(self._master)
        self._body.title("Failure")
        # text
        text = tk.Text(self._body,
                       name="failure_view",
                       width=50, height=10)
        text.pack(padx=5, pady=5)
        text.insert("1.0", self._data)
        # button quit
        button = tk.Button(self._body, text="Close", command=self.destroy)
        button.pack(anchor="e", padx=2, pady=2)

    def _on_display(self):
        pass

    def _on_destroy(self):
        pass

    def _toplevel_geometry(self):
        super()._toplevel_geometry()
        tkmisc.dialog_effect(self._body)
