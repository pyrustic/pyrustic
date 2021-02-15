import sys
import json
import copy
import platform
import pkgutil
import tkinter as tk
from pyrustic import dist
from pyrustic.viewable import Viewable
from pyrustic import tkmisc
from pyrustic.exception import PyrusticAppException
from pyrustic.private.enhance_tk import EnhanceTk


class App:
    """
    Pyrustic Framework's entry point.
    This class should be instantiated inside the file "main.py".
    """
    def __init__(self, package):
        """
        Create an App instance.
        package: the name of the package in which the caller is. Use __package__.

        It's recommended to don't write any code above this instantiation.
        """
        self._package = package
        self._is_running = False
        self._root = tk.Tk()
        self._theme = None
        self._view = None
        self._center_window = False
        self._config_data = None
        self._setup()

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
        Get a dict-like deepcopy of your config file if it exists and is valid.
        Else you will get the default config dict.
        """
        return copy.deepcopy(self._config_data)

    @property
    def theme(self):
        """
        Get the theme object
        For more information about what a theme is:
        - check 'pyrustic.theme.Theme';
        - then check the beautiful theme 'pyrustic.theme.cyberpunk'
        """
        return self._theme

    @theme.setter
    def theme(self, val):
        """
        Set the theme object.
        If you set None, it will invalidate the previous theme.
        Don't forget to call the method "restart()" or "start()" to apply the change !
        Remember that "start()" should be called only once !
        For more information about what a theme is:
        - check "pyrustic.theme.Theme";
        - then check the beautiful theme "pyrustic.theme.cyberpunk"
        """
        self._root.option_clear()
        self._theme = val

    @property
    def view(self):
        """
        Get the view object.
        A view should implement "pyrustic.viewable.Viewable"
        """
        return self._view

    @view.setter
    def view(self, val):
        """
        Set a view object.
        If you set None, the previous view will be destroyed.
        A view should implement "pyrustic.viewable.Viewable".
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
        It should be called once and put on the last line of the file.
        """
        if self._is_running:
            message = "This method shouldn't be called twice. Please use 'restart' instead"
            raise PyrusticAppException(message)
        self._is_running = True
        self._root.protocol("WM_DELETE_WINDOW", self._on_exit)
        EnhanceTk(self._root)
        self._set_config()
        self._set_theme()
        self._install_view()
        try:
            self._root.mainloop()
        except KeyboardInterrupt:
            pass

    def restart(self):
        """
        Call this method to restart the app.
        You would need to submit a new view first before calling this method.
        """
        if not self._is_running:
            message = "The app should be already running before you could call this method"
            raise PyrusticAppException(message)
        self._set_theme()
        self._install_view()

    def exit(self):
        """
        Exit, simply ;-)
        Depending on your config file, the application will close quickly or not.
        A quick exit will ignore the lifecycle of a Viewable (pyrustic.viewable).
        In others words, '_on_destroy()' methods won't be called.
        Exit quickly if you don't care clean-up but want the app to close as fast as possible.
        """
        self._on_exit()

    def maximize(self):
        """
        Maximize the window
        """
        system = platform.system()
        if system == "Linux":
            self._root.attributes("-zoomed", True)
        else:  # for "Darwin" (OSX) and "Window"
            self._root.state("zoomed")

    def center(self):
        """
        Center the window
        """
        self._center_window = True

    # ============================================
    #               PRIVATE METHODS
    # ============================================
    def _set_config(self):
        # app geometry
        if not self._config_data["ignore_geometry"]:
            self._root.geometry(self._config_data["root_geometry"])
        # background
        background_color = self._config_data["root_background"]
        self._root.config(background=background_color)
        # resizable width and height
        resizable_width = self._config_data["resizable_width"]
        resizable_height = self._config_data["resizable_height"]
        self._root.resizable(width=resizable_width, height=resizable_height)
        # maximize screen
        if self._config_data["maximize_window"]:
            self.maximize()

    def _set_theme(self):
        if not self._config_data["allow_theme"]:
            return
        if not self._theme:
            return
        self._theme.target(self._root)

    def _install_view(self):
        if not self._view:
            return
        if not self._view.build():
            return
        if isinstance(self._view.body, tk.Frame):
            self._view.body.pack(in_=self._root,
                                 expand=1, fill=tk.BOTH)
        # center
        if self._center_window:
            tkmisc.center_window(self._root)


    def _on_exit(self):
        if self._view:
            self._view.destroy()
            self._view = None
        if self._root:
            self._root.destroy()
            self._root = None
        sys.exit()

    def _set_default_title(self):
        name = self._package
        if "." in name:
            name = "Application"
        title = "{} | built with Pyrustic".format(name)
        self._root.title(title)

    def _setup(self):
        if not self._package:
            raise PyrusticAppException("Missing package name.")
        # config_data
        gui_json_resource = "pyrustic_data/gui.json"
        default_gui_json_resource = "manager/default_json/pyrustic_data/gui_default.json"
        gui_json = pkgutil.get_data(self._package, gui_json_resource)
        if not gui_json:
            gui_json = pkgutil.get_data(__package__, default_gui_json_resource)
        self._config_data = json.loads(gui_json)
        # set default title
        self._set_default_title()
