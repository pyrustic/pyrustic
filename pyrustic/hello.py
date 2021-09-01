import tkinter as tk
from viewable import Viewable
from megawidget.toast import Toast


class HelloView(Viewable):
    """Graphical equivalent of a Hello World"""
    def __init__(self, app):
        super().__init__()
        self._app = app
        self._root = app.root
        self._body = None
        self._btn_max = None

    # ============ VIEW LIFECYCLE ===========

    def _build(self):
        self._body = tk.Frame(self._root)
        self._root.geometry("500x300")
        # Label
        label = tk.Label(self._body, text="Hello Friend !")
        label.pack(expand=1, fill=tk.BOTH)
        # Footer
        footer = tk.Frame(self._body)
        footer.pack(side=tk.BOTTOM, fill=tk.X, padx=2, pady=2)
        # Button Leave
        btn_leave = tk.Button(footer, text="Leave",
                              command=self._on_click_btn_leave)
        btn_leave.pack(side=tk.RIGHT)
        # Button Crash
        self._btn_max = tk.Button(footer, text="Crash",
                                  command=self._on_click_btn_crash)
        self._btn_max.pack(side=tk.RIGHT, padx=2)
        # Button Maximize
        self._btn_max = tk.Button(footer, text="Maximize",
                                  command=self._on_click_btn_max)
        self._btn_max.pack(side=tk.RIGHT)

    def _on_map(self):
        super()._on_map()

    def _on_destroy(self):
        super()._on_destroy()

    # ============ HANDLERS =============

    def _on_click_btn_max(self):
        self._app.maximize()
        self._btn_max.destroy()

    def _on_click_btn_crash(self):
        self._app.crash_resistant = False
        raise Exception("Deliberately raised exception !")

    def _on_click_btn_leave(self):
        toast = Toast(self._body, message="Goodbye Friend !")
        toast.wait_window()
        self._app.exit()
