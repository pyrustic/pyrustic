from pyrustic.widget.toast import Toast
from pyrustic.viewable import Viewable
import tkinter as tk
from pyrustic import tkmisc
from tkinter import filedialog


class Editor(Viewable):
    def __init__(self, parent_view, project):
        self._parent_view = parent_view
        self._project = project
        self._body = None
        self._text_widget = None
        # intvar
        self._intvar_is_script = tk.IntVar()

    def _on_build(self):
        self._body = tk.Toplevel(class_="Editor")
        self._body.protocol("WM_DELETE_WINDOW", self._on_click_cancel)
        self._body.columnconfigure(0, weight=1)
        self._body.rowconfigure(0, weight=1)
        self._body.title("Editor")
        self._text_widget = tk.Text(self._body,
                                    undo=True,
                                    wrap="word")
        buttons_bar = tk.Frame(self._body)
        # buttons
        button_run = tk.Button(buttons_bar,
                               text="Run",
                               command=self._on_click_run)
        button_load = tk.Button(buttons_bar,
                                text="Load",
                                command=self._on_click_load)
        button_clear = tk.Button(buttons_bar,
                                 text="Clear",
                                 command=self._on_click_clear)
        button_cancel = tk.Button(buttons_bar,
                                  text="Cancel",
                                  command=self._on_click_cancel)
        # checkbutton
        checkbutton = tk.Checkbutton(buttons_bar, text="Script",
                                     variable=self._intvar_is_script,
                                     onvalue=1, offvalue=0)
        # install
        buttons_bar.grid(row=1, column=0, sticky="we", ipady=3)
        self._text_widget.grid(row=0, column=0, sticky="nswe")
        button_run.pack(side=tk.RIGHT, padx=(0, 3))
        button_load.pack(side=tk.RIGHT, padx=(0,3))
        button_clear.pack(side=tk.RIGHT, padx=(0,3))
        button_cancel.pack(side=tk.RIGHT, padx=(3, 3))
        checkbutton.pack(side=tk.LEFT)

    def _on_display(self):
        tkmisc.dialog_effect(self._body)
        intvar, sql = self._parent_view.cache_editor_data
        self._intvar_is_script.set(intvar)
        self._text_widget.insert("end", sql)
        self._focus_text()

    def _on_destroy(self):
        pass

    def _toplevel_geometry(self):
        tkmisc.center_window(self._body)

    # ========================================
    #           EVENTS HANDLERS
    # ========================================
    def _on_click_run(self):
        self._backup_data()
        self._parent_view.notify_sql_to_run()

    def _on_click_load(self):
        filename = filedialog.askopenfilename(parent=self._body,
                                              initialdir=self._project,
                                              title="Select a file")
        if isinstance(filename, str) and filename:
            data = ""
            try:
                with open(filename, "r") as file:
                    data = file.read()
            except Exception as e:
                Toast(self._body,
                      message="Failed to load the data",
                      duration=2000).build()

            self._text_widget.insert("end", data)

    def _on_click_clear(self):
        self._text_widget.delete("1.0", "end")

    def _on_click_cancel(self):
        self._backup_data()
        self.destroy()

    def _backup_data(self):
        sql = self._text_widget.get("1.0", "end-1c")
        self._parent_view.cache_editor_data = (self._intvar_is_script.get(),
                                               sql)

    def _focus_text(self):
        self._text_widget.focus()
