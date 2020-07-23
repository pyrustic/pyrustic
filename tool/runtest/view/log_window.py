from pyrustic.widget.dialog import Dialog
import tkinter as tk


class LogWindow(Dialog):
    def __init__(self, master, message):
        self._master = master
        self._message = message
        self._text = None
        # build
        self.build_wait()

    def _on_build(self):
        self._body = tk.Toplevel()
        self._body.title("Log - Pyrustic Test Runner")
        scrollbar = tk.Scrollbar(self._body)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self._text = tk.Text(self._body, name="logWindow",
                             width=75, height=25)
        self._text.pack(side=tk.RIGHT, expand=1, fill=tk.BOTH)
        scrollbar.config(command=self._text.yview)
        self._text.config(yscrollcommand=scrollbar.set)
        return self._body

    def _on_display(self):
        self._text.insert("0.0", self._message)
        self._text.config(state="disabled")

    def _on_destroy(self):
        pass
