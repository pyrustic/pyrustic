import tkinter as tk
from pyrustic import tkmisc
from pyrustic.exception import PyrusticException


# Constants
NEW = "new"
BUILT = "built"
DISPLAYED = "displayed"
DESTROYED = "destroyed"


class View:
    """
    Subclass this if you are going to create a view.

    Lifecycle of a view:
        1- you instantiate the view
        2- '__init__()' is implicitly called
        3- you call the method '.build()'
        4- '_on_build()' is implicitly called
        5- '_on_display()' is implicitly called once the widget is visible
        6- '_on_destroy()' is implicitly called when the widget is destroyed/closed

    The rules to create your view is simple:
    - You need to subclass Viewable.
    - You need to implement the methods '_on_build()', and optionally
        implement '_on_display()' and '_on_destroy()'.
    - You need to set an instance variable '_body' with either a tk.Frame or tk.Toplevel
        in the method '_on_build()'
    That's all ! Of course, when you are ready to use the view, just call the 'build()' method.
    Calling the 'build()' method will return the body of the view. The one that you assigned
    to the instance variable '_body'. The same body can be retrieved with the property 'body'.
    The 'build()' method should be called once. Calling it more than once will still return
    the body object, but the view won't be built again.
    You can't re-build your same view instance after destroying its body.
    You can destroy the body directly, by calling the conventional tkinter destruction method
     on the view's body. But it's recommended to destroy the view by calling the view's method
     'destroy()' inherited from the class Viewable.
    The difference between these two ways of destruction is that when u call the Viewable's
     'destroy()' method, the method '_on_destroy()' will be called BEFORE the effective
     destruction of the body. If u call directly 'destroy' conventionally on the tkinter
     object (the body), the method '_on_destroy()' will be called AFTER the beginning
      of destruction of the body.

      By the way, you can use convenience methods "build_pack", "build_grid", "build_place"
      to build and pack/grid/place your widget in the master !!
      Use "build_wait" for toplevels if you want the app to wait till the window closes
    """

    def __init__(self):
        self.__master = None
        self.__state = 0
        self.__built = False
        self.__bind_id = None
        self.__destroyed = False
        self._body = None

    # ==============================================
    #                 PROPERTIES
    # ==============================================

    @property
    def body(self):
        """
        Get the body of this view.
        """
        return self._body

    @property
    def state(self):
        """ Return the current state of the Viewable instance.
        States are integers, you can use these constants:
            - pyrustic.view.NEW: the state just after instantiation;
            - pyrustic.view.BUILT: the state after the call of on_body
            - pyrustic.view.DISPLAYED: the state after the call of on_display
            - pyrustic.view.DESTROYED: the state after the call of on_destroy
        """
        return self.__state
    # ==============================================
    #                 PUBLIC METHODS
    # ==============================================

    def build(self):
        """
        Build the view. Return the body
        """
        return self.__build()

    def build_pack(self, cnf=None, **kwargs):
        cnf = {} if not cnf else cnf
        body = self.__build()
        self._check_missing_body(body)
        body.pack(cnf=cnf, **kwargs)

    def build_grid(self, cnf=None, **kwargs):
        cnf = {} if not cnf else cnf
        body = self.__build()
        self._check_missing_body(body)
        body.grid(cnf=cnf, **kwargs)

    def build_place(self, cnf=None, **kwargs):
        cnf = {} if not cnf else cnf
        body = self.__build()
        self._check_missing_body(body)
        body.place(cnf=cnf, **kwargs)

    def build_wait(self):
        """
        Build the view. Return the body
        """
        body = self.__build()
        body.wait_window(body)

    def destroy(self):
        """
        Destroy the body of this view
        """
        self.__build()
        self.__exec_on_destroy()


    # ==============================================
    #               METHODS TO IMPLEMENT
    # ==============================================

    def _on_build(self):
        """
        Put here the code that build the body of this view.
        The body is either a tk.Frame or a tk.Toplevel instance.
        """
        pass

    def _on_display(self):
        """
        Put here the code that will be executed once the body is visible.
        """
        pass

    def _on_destroy(self):
        """
        Put here the code that will be executed as clean-up.
        """
        pass

    def _toplevel_geometry(self):
        """
        If the body of this view is a toplevel and
        you need to change the geometry of this toplevel,
        override this method !
        """
        tkmisc.center_window(self.body, self.__master.winfo_toplevel())
        tkmisc.dialog_effect(self.body)

    # ==============================================
    #                 INTERNAL METHODS
    # ==============================================

    def __build(self):
        if self.__built:
            return self.body
        self._on_build()
        self.__built = True
        self.__state = BUILT
        if not self.body:
            return
        try:
            self.__master = self.body.master
        except Exception:
            pass
        is_toplevel = isinstance(self.body, tk.Toplevel)
        #is_frame = isinstance(self.body, tk.Frame)
        if is_toplevel:
            #self.body.protocol("WM_DELETE_WINDOW", self.__exec_on_destroy)
            self._toplevel_geometry()
        self.__bind_destroy_event()
        if self.body.winfo_viewable():
            self.__exec_on_display()
        else:
            self.__bind_id = self.body.bind("<Map>",
                                            self.__exec_on_display,
                                            "+")
        return self.body

    def __exec_on_display(self, event=None):
        self._on_display()
        self.__state = DISPLAYED
        if self.__bind_id is not None:
            self.body.unbind("<Map>", self.__bind_id)

    def __bind_destroy_event(self):
        command = (lambda event,
                          widget=self.body,
                          callback=self.__exec_on_destroy:
                   callback() if event.widget is widget else None)
        self.body.bind("<Destroy>", command, "+")

    def __exec_on_destroy(self):
        if not self.__built or self.__destroyed:
            return
        if not self.body:
            return
        window_manager = self.body.winfo_manager()
        """
        # Hide the window first to avoid the visual
        # iterative (slow) destruction
        # of each child
        #
        if window_manager == "wm":
            if self.body.winfo_ismapped():
                self.body.withdraw()
        elif window_manager == "grid":
            if self.body.winfo_ismapped():
                self.body.grid_forget()
        elif window_manager == "pack":
            if self.body.winfo_ismapped():
                self.body.pack_forget()
        elif window_manager == "place":
            if self.body.winfo_ismapped():
                self.body.place_forget()
        """
        try:
            self.body.destroy()
        except Exception as e:
            pass
        self.__destroyed = True
        self._on_destroy()
        self.__state = DESTROYED
        try:
            if self.__master.focus_get() is None:
                self.__master.winfo_toplevel().focus_lastfor().focus_force()
        except Exception as e:
            pass

    def _check_missing_body(self, body):
        if not body:
            raise PyrusticException("Missing body")


class CustomView(View):
    def __init__(self, body=None, on_build=None,
                 on_display=None,
                 on_destroy=None,
                 toplevel_geometry=None):
        super().__init__()
        self._body = body
        if on_build:
            self._on_build = on_build
        if on_display:
            self._on_display = on_display
        if on_destroy:
            self._on_destroy = on_destroy
        if toplevel_geometry:
            self._toplevel_geometry = toplevel_geometry
