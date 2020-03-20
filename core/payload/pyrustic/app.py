import platform
import tkinter as tk
import configparser

import about
import pyrustic.widget as pw
import os.path

from pyrustic.abstract.viewable import Viewable
from pyrustic.enhancetk import EnhanceTk
from pyrustic.exception import PyrusticException


"""
App

USAGE
=====
    app = App()
    app.start(view=any_viewable_instance, stylesheet=path)

PROPRIETIES
===========
    - tk: get the tk instance. U know, the one got with Tk()
    - body: get the body of the app. This is the body from the first view

METHODS
=======
    - start(self, view=None, stylesheet=None, style=None): Method to start the app.
        view: any viewable
        stylesheet: path to a stylesheet or tuple (path, priority_int)
        style: style like this: [ ("*background", "red"), ("*foreground", "yellow") ]
    - config(self, path=None): returns a configparser object.
        If path == None, returns the default config
    - persist_config(self, path=None): persist config
    - style(self, stylesheet=None, style=None): 
        - stylesheet: could be a string or a tuple. 
            String, if it is the path to a tk stylesheet (Xdefault).
            Tuple as this: (str_path_to_stylesheet, int_priority) 
        - style: [ (str_pattern, str_value, int_priority), (str_pattern, str_value), ...]
    - maximize_screen(self): maximize the screen ;)
    - on_close(self, callable): to register callables to call when the app is going to exit
    - close(self): close the app


"""


class App:
    def __init__(self):
        # === App Level Variables
        self._running = False
        self._debug = False
        self._show_gui = True
        self._configs = dict()
        self._default_config_path = os.path.join(about.ROOT_DIR, "config/app.ini")
        # === GUI Level Variables
        self._tk = None
        self._body = None
        self._allow_style = True
        self._maximize_screen = False
        self._geometry = "500x500+0+0"
        self._view = None
        # === Methods calls
        # load config
        self.config()
        # mirror config
        self._mirror_config()
        # === Cache
        self._callables = []

    @property
    def tk(self):
        return self._tk

    @property
    def body(self):
        return self._body

    def start(self, view=None, stylesheet=None, style=None):
        if self._running is True:
            return
        if self._show_gui:
            self._view = view
            # exec GUI
            self._exec_gui()
            # exec style
            if self._allow_style:
                self.style(stylesheet, style)
            # screen geometry
            if self._maximize_screen:
                self.maximize_screen()
            else:
                self._tk.geometry(self._geometry)
        #
        self._exec_view()
        self._running = True
        # mainloop
        if self._show_gui:
            self._tk.mainloop()

    def config(self, path=None):
        if path is None:
            path = self._default_config_path
        if not os.path.isfile(path):
            raise Exception("This path doesn't exist: " + path)
        if path not in self._configs:
            config = configparser.ConfigParser()
            config.read(path)
            self._configs[path] = config
        return self._configs[path]

    def persist_config(self, path=None):
        if path is None:
            path = self._default_config_path
        if path not in self._configs:
            return False
        with open(path, "w") as configfile:
            self._configs[path].edit(configfile)
        return True

    def style(self, stylesheet=None, style=None):
        if isinstance(stylesheet, str):
            self._tk.option_readfile(stylesheet)
        elif isinstance(stylesheet, tuple):
            self._tk.option_readfile(stylesheet[0], stylesheet[1])
        if style:
            for x in style:
                if len(x) == 2 or len(x) == 3:
                    self._tk.option_add(*x)

    def maximize_screen(self):
        #self._tk.geometry("{0}x{1}+0+0".format(self._tk.winfo_screenwidth(),
        #                                      self._tk.winfo_screenheight()))
        system = platform.system()
        if system == "Linux":
            self._tk.attributes("-zoomed", True)
        else: # for "Darwin" (OSX) and "Window"
            self._tk.state("zoomed")

    def on_close(self, callable):
        self._callables.append(callable)

    def close(self):
        if self._tk is not None:
            try:
                [x(self) for x in self._callables]
                self._spring.stop()
            except Exception as e:
                pass
            self._tk.destroy()

    def _exec_gui(self):
        self._tk = tk.Tk()
        EnhanceTk(self._tk)
        self._tk.protocol("WM_DELETE_WINDOW", self.close)

    def _exec_view(self):
        if self._view:
            if isinstance(self._view, Viewable):
                self._body = self._view.build()
            else:
                raise PyrusticException("The argument 'view' submitted to 'app.start()' isn't a Viewable")
        if self._show_gui and self._body:
            pw.pack(self._tk, self._body, expand=1, fill=tk.BOTH)
        elif self._show_gui and not self._body:
            text1 = "Hello friend ;)\n"
            text2 = "You need to implement a View that returns its body in its method _on_build()"
            tk.Label(self._tk, text=text1+text2).pack()
            tk.Button(self._tk, text="Close", command=self.close).pack()

    def _mirror_config(self):
        config = self._configs[self._default_config_path]
        self._debug = config["MAIN"].getboolean("debug", True)
        self._show_gui = config["GUI"].getboolean("show_gui", True)
        self._allow_style = config["GUI"].getboolean("allow_style", True)
        self._maximize_screen = config["GUI"].getboolean("maximize_screen", True)
        self._geometry = config["GUI"]["geometry"]
