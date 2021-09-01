"""Pyrustic Framework entry point"""
import platform
import tkinter as tk
import tkutil
import traceback
from viewable import Viewable, CustomView
from pyrustic.private.enhance_tk import EnhanceTk


class App:
    """
    Pyrustic Framework's entry point.
    This class should be instantiated inside "$APP_DIR/__main__.py".
    """
    def __init__(self):
        """
        """
        self._package = None
        self._is_running = False
        self._restartable = False
        self._root = tk.Tk()
        self._title = None
        self._theme = None
        self._theme_cache = None
        self._view = None
        self._view_cache = None
        self._center_window = False
        self._geometry = "+0+0"
        self._background = "black"
        self._ignore_theme = False
        self._resizable = (True, True)
        self._crash_resistant = True
        self._cached_report_callback_exception = None
        #self._exit_handler = None
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
    def title(self):
        """
        Get the title of the app
        """
        return self._title

    @title.setter
    def title(self, val):
        """
        Set the title of the app
        """
        self._title = val

    @property
    def theme(self):
        """
        Get the theme object. A theme is a subclass of
        themebase.Theme.
        """
        return self._theme

    @theme.setter
    def theme(self, val):
        """
        Set the theme object. A theme is a subclass of themebase.Theme.

        If you set None, it will invalidate the previous theme.

        Don't forget to call the method "restart()" or "start()" to apply the change !
        Remember that "start()" should be called only once !
        """
        self._theme_cache = val

    @property
    def view(self):
        """
        Get the view object.
        A view should implement "viewable.Viewable"
        """
        return self._view

    @view.setter
    def view(self, val):
        """
        Set a view object. A view should implement "viewable.Viewable".
        If you set None, the previous view will be destroyed.
        The new view will destroy the previous one if there are a previous one.

        Note: "val" can be a tkinter object or a callable (if u plan to REFRESH the app)
        that accepts the app reference as argument and returns a view or a tkinter object
        """
        self._view_cache = val

    @property
    def geometry(self):
        """ Get the geometry string. """
        return self._geometry

    @geometry.setter
    def geometry(self, val):
        """ Set the geometry string. """
        self._geometry = val

    @property
    def background(self):
        """ Get the background color string. By default: "black" """
        return self._background

    @background.setter
    def background(self, val):
        """ Set the background color string """
        self._background = val

    @property
    def ignore_theme(self):
        """ Get the ignore_theme boolean value """
        return self._ignore_theme

    @ignore_theme.setter
    def ignore_theme(self, val):
        """ Set True to ignore the theming """
        self._ignore_theme = val

    @property
    def resizable(self):
        """ Get the resizable boolean"""
        return self._resizable

    @resizable.setter
    def resizable(self, val):
        """ Set a boolean to allow the app to resize or not """
        self._resizable = val
        
    @property
    def crash_resistant(self):
        """ Get the crash_resistant boolean value """
        return self._crash_resistant

    @ignore_theme.setter
    def crash_resistant(self, val):
        """ Set True to allow the app to crash when an exception is raised """
        self._crash_resistant = val

    #@property
    #def exit_handler(self):
    #    """ Get the exit handler, a callable called when the app exits """
    #    return self._exit_handler

    #@exit_handler.setter
    #def exit_handler(self, val):
    #    """ Set the exit handler. It will be called when the app exits.
    #     The exit handler is just a callable """
    #    self._exit_handler = val

    @property
    def package(self):
        """ Get the package string name """
        return self._package

    @package.setter
    def package(self, val):
        """ Set the package string name """
        self._package = val

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
            raise Error(message)
        self._is_running = True
        self._build()
        # main loop
        try:
            self._root.mainloop()
        except KeyboardInterrupt:
            pass

    def restart(self):
        """
        Call this method to restart the app.
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
        """
        if self._is_running:
            self._is_running = False
            self._root.destroy()

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
        self._cached_report_callback_exception = self._root.report_callback_exception
        self._root.report_callback_exception = self._on_report_callback_exception

    def _build(self):
        # bind self._on_exit
        #self._root.protocol("WM_DELETE_WINDOW", self._root.destroy)
        self._root.protocol("WM_DELETE_WINDOW", self.exit)
        #handler = (lambda event,
        #                  root=self._root:
        #           self._on_exit() if event.widget is root else None)
        #self._root.bind("<Destroy>", handler)
        EnhanceTk(self._root)
        # set title, apply config, set theme then install view
        self._set_title()
        self._apply_config()
        self._apply_theme(self._theme_cache)
        self._install_view(self._view_cache)

    def _set_title(self):
        if not self._title:
            self._title = "Application"
        text = "{} | built with Pyrustic".format(self._title)
        self._root.title(text)

    def _apply_config(self):
        self._apply_gui_config()

    def _apply_gui_config(self):
        # geometry
        self._root.geometry(self._geometry)
        # resizable width and height
        resizable_width, resizable_height = self._resizable
        self._root.resizable(width=resizable_width, height=resizable_height)

    def _apply_theme(self, theme):
        if self._theme:
            self._root.option_clear()
        self._theme = theme
        if self._ignore_theme:
            return
        if not self._theme:
            return
        self._theme.target(self._root)

    def _install_view(self, view, is_refresh=False):
        self._view = self._get_view(view)
        body = self._view.build()
        if not body:
            return False
        if isinstance(body, tk.Frame):
            self._view.body.pack(in_=self._root,
                                 expand=1, fill=tk.BOTH)
        elif isinstance(body, tk.Toplevel):
            pass
        else:
            self._view.body.pack(in_=self._root)
        # center
        if not is_refresh and self._center_window:
            tkutil.center_window(self._root)
        # sync background color
        #background = body.option_get("background", body.winfo_class())
        self._background = body.cget("background")
        self._root.config(background=self._background)
        return True

    def _get_view(self, view):
        if callable(view):
            view = view(self)
        if isinstance(view, Viewable):
            return view
        #if isinstance(view, type) and issubclass(view, Viewable):
        #    return view()
        if view is None:
            view = tk.Frame(self._root,
                            width=350,
                            height=200)
        return CustomView(body=view)
        
    def _on_report_callback_exception(self, exc, val, tb):
        self._cached_report_callback_exception(exc, val, tb)
        if not self._crash_resistant:
            self.exit()

    #def _on_exit(self):
    #    if self._exit_handler:
    #        self._exit_handler()


class Error(Exception):
    def __init__(self, *args, **kwargs):
        self.message = args[0] if args else ""
        super().__init__(self.message)

    def __str__(self):
        return self.message
