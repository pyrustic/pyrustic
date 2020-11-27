import copy
import platform
import sys
import about
import tkinter as tk
import os.path
from pyrustic.viewable import Viewable
from pyrustic.exception import PyrusticAppException
from pyrustic.private.enhance_tk import EnhanceTk
from pyrustic.jasonix import Jasonix


_DEFAULT_CONFIG_PATH = os.path.join(about.ROOT_DIR,
                                    "pyrustic",
                                    "private",
                                    "default_app_config.json")


class App:
    """
    Pyrustic Framework's entry point.
    This class should be instantiated inside the file "main.py".
    """
    def __init__(self):
        """
        Create an App instance.
        It's recommended to don't write any code above this instantiation.
        """
        self._is_running = False
        self._root = tk.Tk()
        self._config_path = None
        self._config_data = None
        self._theme = None
        self._view = None
        self._set_default_title()

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
        return self._config_path, copy.deepcopy(self._config_data)


    @config.setter
    def config(self, path):
        """
        The path to config file.
        Note that it should be a relative path to ROOT_DIR,
        Example:
            path = "my_config.json"

        Warning: it is recommended to avoid hard-coding paths.
        Avoid a path like this: "./this/is/a/relative/path"
        Instead, do this: os.path.join("this", "is", "a", "relative", "path")
        """
        path = os.path.join(about.ROOT_DIR, path)
        path = os.path.normpath(path)
        self._config_path = path

    @property
    def theme(self):
        """
        Get the theme object
        For more information about what a theme is:
        - check 'pyrustic.theme.Theme';
        - then check the beautiful theme 'pyrustic.themes.darkmatter'
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
        - then check the beautiful theme "pyrustic.themes.darkmatter"
        """
        self._root.option_clear()
        self._theme = val

    @property
    def view(self):
        """
        Get the view object.
        A view should implement "pyrustic.abstract.viewable.Viewable"
        """
        return self._view

    @view.setter
    def view(self, val):
        """
        Set a view object.
        If you set None, the previous view will be destroyed.
        A view should implement "pyrustic.abstract.viewable.Viewable".
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
        self._root.config(background="white")
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
        A quick exit will ignore the lifecycle of a Viewable (pyrustic.abstract.viewable).
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

    # ============================================
    #               PRIVATE METHODS
    # ============================================
    def _set_config(self):
        jasonix = Jasonix(self._config_path,
                            _DEFAULT_CONFIG_PATH)
        self._config_data = jasonix.data
        # app geometry
        if not self._config_data["gui"]["ignore_geometry"]:
            self._root.geometry(self._config_data["gui"]["root_geometry"])
        # resizable width and height
        resizable_width = self._config_data["gui"]["resizable_width"]
        resizable_height = self._config_data["gui"]["resizable_height"]
        self._root.resizable(width=resizable_width, height=resizable_height)
        # maximize screen
        if self._config_data["gui"]["maximize_window"]:
            self.maximize()

    def _set_theme(self):
        if not self._config_data["gui"]["allow_theme"]:
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
                      expand=1,
                      fill=tk.BOTH)

    def _on_exit(self):
        if not self._config_data["gui"]["exit_quickly"]:
            if self._root:
                self._root.destroy()
                self._root = None
        sys.exit()

    def _set_default_title(self):
        title = "{} | built with Pyrustic".format(about.PROJECT_NAME)
        self._root.title(title)
