import sys
import copy
import platform
import pkgutil
import tkinter as tk
import pyrustic
from pyrustic.view import View, CustomView
from pyrustic import tkmisc
from pyrustic.jasonix import Jasonix
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
        self._restartable = False
        self._root = tk.Tk()
        self._theme = None
        self._theme_cache = None
        self._view = None
        self._view_cache = None
        self._center_window = False
        self._config = None
        self._gui_config = None
        self._exit_handler = None
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
    def installed(self):
        data = pyrustic.dist(self._package)
        return True if data else False

    @property
    def config(self):
        return copy.deepcopy(self._config)

    @config.setter
    def config(self, val):
        """ val is dict, path or file-like object"""
        jasonix = Jasonix(val)
        self._config = jasonix.data
        if self._config:
            self._gui_config = self._config.get("gui", self._gui_config)

    @property
    def gui_config(self):
        """
        Setter et Getter
        """
        return copy.deepcopy(self._gui_config)

    @gui_config.setter
    def gui_config(self, val):
        jasonix = Jasonix(val)
        self._gui_config = jasonix.data
        if self._gui_config:
            self._config["gui"] = self._gui_config

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
        self._theme_cache = val

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
        The new view will destroy the previous one if there are a previous one.
        VAL can be a tkinter object or a callable (if u plan to REFRESH the app)
        """
        self._view_cache = val

    @property
    def body(self):
        return self._body

    @body.setter
    def body(self, val):
        self._body = val

    @property
    def exit_handler(self):
        return self._exit_handler

    @exit_handler.setter
    def exit_handler(self, val):
        self._exit_handler = val

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
        self._build()
        # main loop
        try:
            self._root.mainloop()
        except KeyboardInterrupt:
            pass

    def refresh(self):
        """
        Call this method to refresh the app.
        If you have submitted a new view or a new theme,
        the previous view or theme will be removed and the new one installed
        """
        if not self._is_running:
            return False
        if not self._view_cache or not callable(self._view_cache):
            return False
        if self._theme_cache:
            self._apply_theme(self._theme_cache)
            self._theme_cache = None
        if self._view:
            self._view.destroy()
        self._body = None
        return self._install_view(self._view_cache,
                                  is_refresh=True)

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

    def _setup(self):
        # gui_config
        self._set_config()
        # set default title
        self._set_default_title()

    def _build(self):
        # bind self._on_exit
        self._root.protocol("WM_DELETE_WINDOW", self._on_exit)
        handler = (lambda event,
                          root=self._root:
                   self._on_exit() if event.widget is root else None)
        self._root.bind("<Destroy>", handler)
        EnhanceTk(self._root)
        # apply config, set theme then install view
        self._apply_config()
        self._apply_theme(self._theme_cache)
        self._install_view(self._view_cache)

    def _set_config(self):
        self._set_gui_config()

    def _set_gui_config(self):
        gui_config_json = None
        gui_config_json_resource = "pyrustic_data/gui.json"
        default_gui_json_resource = \
            "manager/default_json/pyrustic_data/gui_default.json"
        if self._package:
            try:
                gui_config_json = pkgutil.get_data(self._package,
                                                   gui_config_json_resource)
            except Exception as e:
                pass
        if not gui_config_json:
            gui_config_json = pkgutil.get_data(__package__,
                                               default_gui_json_resource)
        jasonix = Jasonix(gui_config_json)
        self._gui_config = jasonix.data
        self._config = {"gui": self._gui_config}

    def _set_default_title(self):
        name = self._package
        if not self._package or "." in name:
            name = "Application"
        title = "{} | built with Pyrustic".format(name)
        self._root.title(title)

    def _apply_config(self):
        self._apply_gui_config()

    def _apply_gui_config(self):
        # app geometry
        if not self._gui_config["ignore_geometry"]:
            self._root.geometry(self._gui_config["root_geometry"])
        # background
        background_color = self._gui_config["root_background"]
        self._root.config(background=background_color)
        # resizable width and height
        resizable_width = self._gui_config["resizable_width"]
        resizable_height = self._gui_config["resizable_height"]
        self._root.resizable(width=resizable_width, height=resizable_height)
        # maximize screen
        if self._gui_config["maximize_window"]:
            self.maximize()

    def _apply_theme(self, theme):
        if self._theme:
            self._root.option_clear()
        self._theme = theme
        if not self._gui_config["allow_theme"]:
            return
        if not self._theme:
            return
        self._theme.target(self._root)

    def _install_view(self, view, is_refresh=False):
        self._view = self._get_view(view)
        self._view.build()
        if not self._view.build():
            return False
        body = self._view.body
        if isinstance(body, tk.Frame):
            self._view.body.pack(in_=self._root,
                                 expand=1, fill=tk.BOTH)
        elif isinstance(body, tk.Toplevel):
            pass
        else:
            self._view.body.pack(in_=self._root)
        # center
        if not is_refresh and self._center_window:
            tkmisc.center_window(self._root)
        return True

    def _get_view(self, view):
        if callable(view):
            view = view()
        if isinstance(view, View):
            return view
        if isinstance(view, type) and issubclass(view, View):
            return view()
        if view is None:
            view = tk.Frame(self._root,
                            bg="black",
                            width=350,
                            height=200)
        return CustomView(body=view)

    def _on_exit(self):
        if self._exit_handler:
            val = self._exit_handler()
            if not val:
                return
        if self._view:
            if self._view.body:
                pass
                #self._root.iconify()
                #self._root.withdraw()
            self._view.destroy()
            self._view = None
        if self._root:
            self._root.destroy()
            self._root = None
        sys.exit()
