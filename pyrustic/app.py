import configparser
import copy
import platform
import sys
import tkinter as tk
import os.path
from pyrustic.abstract.viewable import Viewable
from pyrustic.exception import PyrusticAppException
from pyrustic.tkmisc import EnhanceTk


_GUI_CONFIG = {"root_geometry": "+0+0",
               "ignore_geometry": False,
               "resizable_width": True,
               "resizable_height": True,
               "allow_theme": True,
               "maximize_screen": False,
               "exit_quickly": False}

_DEFAULT_CONFIG = {"GUI": _GUI_CONFIG}


class App:
    """
    Pyrustic Framework's entry point.
    This class should be instantiated inside the file 'main.py'.
    """
    def __init__(self):
        """
        Create an App instance. It's recommended to don't write any code above this.
        """
        self._is_running = False
        self._root = tk.Tk()
        self._config = None
        self._theme = None
        self._view = None
        self._set_config()

    # ============================================
    #                PROPERTIES
    # ============================================
    @property
    def root(self):
        """
        Get the main tk root
        """
        return self._root

    @property
    def config(self):
        """
        Get a dict-like version of your config file, if it exists and is valid.
        Else you will get the default config dict.
        """
        return copy.deepcopy(self._config)

    @config.setter
    def config(self, val):
        """
        Set a config file path
        """
        self._set_config(val)

    @property
    def theme(self):
        """
        Get the theme object
        For more information about what a theme is:
        - check 'pyrustic.theme.Theme';
        - then check the theme 'pyrustic.themes.darkmatter'
        """
        return self._theme

    @theme.setter
    def theme(self, val):
        """
        Set the theme object.
        If u set None, it will invalidate the previous theme.
        Don't forget to call the method 'restart()' or 'start()' to apply the change !
        Remember that 'start()' should be called only once !
        Also, you should set a theme before creating an instance of your view !
        For more information about what a theme is:
        - check 'pyrustic.theme.Theme';
        - then check the theme 'pyrustic.themes.darkmatter'
        """
        self._root.option_clear()
        self._theme = val
        self._set_theme()

    @property
    def view(self):
        """
        Get the view object.
        A view should implement 'pyrustic.abstract.viewable.Viewable'
        """
        return self._view

    @view.setter
    def view(self, val):
        """
        Set a view object.
        If you set None, the previous view will be destroyed.
        A view should implement 'pyrustic.abstract.viewable.Viewable'.
        The new view will destroy the previous one if there are a previous one.
        """
        if val is not None and not isinstance(val, Viewable):
            raise PyrusticAppException("{} isn't a Viewable".format(val))
        if self._view:
            self._view.destroy()
        self._view = val

    # ============================================
    #               PUBLIC METHODS
    # ============================================
    def start(self):
        """
        Call this method to start the app.
        It should be called once and put on the last line of the file 'main.py'.
        """
        if self._is_running:
            message = "This method shouldn't be called twice. Please use 'restart' instead"
            raise PyrusticAppException(message)
        self._is_running = True
        self._root.config(background="white")
        self._root.protocol("WM_DELETE_WINDOW", self._on_exit)
        EnhanceTk(self._root)
        self._install_view()
        self._root.mainloop()

    def restart(self):
        """
        Call this method to restart the app.
        You would need to submit a new view first before calling this method.
        """
        if not self._is_running:
            message = "The app should be already running before you could call this method"
            raise PyrusticAppException(message)
        self._install_view()

    def exit(self):
        """
        Exit, simply ;-)
        Dependently of your config file, the app will exit quickly or not.
        A quick exit will ignore the lifecycle of a Viewable (pyrustic.abstract.viewable).
        In others words, '_on_destroy()' methods won't be called.
        Exit quickly if you don't care clean-up but want the app to close as fast as possible.
        """
        self._on_exit()

    # ============================================
    #               PRIVATE METHODS
    # ============================================
    def _set_config(self, new_config=None):
        self._config = self._merge_configs(new_config, copy.deepcopy(_DEFAULT_CONFIG))
        # app geometry
        if not self._config["GUI"]["ignore_geometry"]:
            self._root.geometry(self._config["GUI"]["root_geometry"])
        # resizable width and height
        resizable_width = self._config["GUI"]["resizable_width"]
        resizable_height = self._config["GUI"]["resizable_height"]
        self._root.resizable(width=resizable_width, height=resizable_height)
        # maximize screen
        if self._config["GUI"]["maximize_screen"]:
            self._maximize_screen()

    def _set_theme(self):
        if not self._config["GUI"]["allow_theme"]:
            return
        if not self._theme:
            return
        self._theme.target(self._root)

    def _install_view(self):
        if not self._view:
            return
        body = self._view.build()
        if not body:
            return
        body.pack(in_=self._root,
                  expand=1,
                  fill=tk.BOTH)

    def _on_exit(self):
        if not self._config["GUI"]["exit_quickly"]:
            self._root.destroy()
        sys.exit()

    def _merge_configs(self, new_config, default):
        if new_config is None:
            return default
        if not isinstance(new_config, str):
            raise PyrusticAppException("The config should be a path")
        if not os.path.isfile(new_config):
            raise PyrusticAppException("This path doesn't exist: {}".format(new_config))
        config = configparser.ConfigParser()
        config.read(new_config)
        if "GUI" not in config:
            return
        if "root_geometry" in config["GUI"]:
            default["GUI"]["root_geometry"] = config["GUI"]["root_geometry"]
        if "ignore_geometry" in config["GUI"]:
            default["GUI"]["ignore_geometry"] = config["GUI"].getboolean("ignore_geometry",
                                                                         False)
        if "resizable_width" in config["GUI"]:
            default["GUI"]["resizable_width"] = config["GUI"].getboolean("resizable_width",
                                                                         True)
        if "resizable_height" in config["GUI"]:
            default["GUI"]["resizable_height"] = config["GUI"].getboolean("resizable_height",
                                                                         True)
        if "allow_theme" in config["GUI"]:
            default["GUI"]["allow_theme"] = config["GUI"].getboolean("allow_theme",
                                                                         True)
        if "maximize_screen" in config["GUI"]:
            default["GUI"]["maximize_screen"] = config["GUI"].getboolean("maximize_screen",
                                                                         False)
        if "exit_quickly" in config["GUI"]:
            default["GUI"]["exit_quickly"] = config["GUI"].getboolean("exit_quickly",
                                                                         False)
        return default

    def _maximize_screen(self):
        system = platform.system()
        if system == "Linux":
            self._root.attributes("-zoomed", True)
        else:  # for "Darwin" (OSX) and "Window"
            self._root.state("zoomed")
