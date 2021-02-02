import tkinter as tk
from pyrustic import tkmisc
from pyrustic.exception import PyrusticException


# Constants
NEW = "new"
BUILT = "built"
DISPLAYED = "displayed"
DESTROYED = "destroyed"


class Viewable():
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

    # ==============================================
    #                 PROPERTIES
    # ==============================================

    @property
    def body(self):
        """
        Get the body of this view.
        """
        try:
            self._body
        except AttributeError:
            self.__set_default_attributes()
        return self._body

    @property
    def state(self):
        """ Return the current state of the Viewable instance.
        States are integers, you can use these constants:
            - viewable.NEW: the state just after instantiation;
            - viewable.BUILT: the state after the call of on_body
            - viewable.DISPLAYED: the state after the call of on_display
            - viewable.DESTROYED: the state after the call of on_destroy
        """
        try:
            self.__state
        except AttributeError:
            self.__set_default_attributes()
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
        body.pack(cnf=cnf, **kwargs)

    def build_grid(self, cnf=None, **kwargs):
        cnf = {} if not cnf else cnf
        body = self.__build()
        body.grid(cnf=cnf, **kwargs)

    def build_place(self, cnf=None, **kwargs):
        cnf = {} if not cnf else cnf
        body = self.__build()
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
        try:
            self.__built
        except AttributeError:
            self.__set_default_attributes()
        if self.__built:
            return self.body
        self._on_build()
        self.__built = True
        self.__state = BUILT
        try:
            self.__master = self.body.master
        except Exception:
            pass
        if isinstance(self.body, tk.Toplevel):
            self.__is_toplevel = True
            self.body.protocol("WM_DELETE_WINDOW", self.__exec_on_destroy)
            self.__bind_destroy_event()
            self._toplevel_geometry()
            try:
                self.body.wait_visibility()
            except Exception as e:
                pass
            else:
                self._on_display()
                self.__state = DISPLAYED
        elif isinstance(self.body, tk.Frame):
            self.__bind_destroy_event()
            self.body.after(0, self.__exec_on_display)
        else:
            message = "The body of a a Viewable should be either a tk.Frame or a tk.Toplevel"
            raise PyrusticException(message)
        return self.body

    def __set_default_attributes(self):
        # __state
        try:
            self.__state
        except AttributeError:
            self.__state = 0
        # __built
        try:
            self.__built
        except AttributeError:
            self.__built = False
        # _body
        try:
            self._body
        except AttributeError:
            self._body = None
        # __toplevel
        try:
            self.__is_toplevel
        except AttributeError:
            self.__is_toplevel = False
        # __master
        try:
            self.__master
        except AttributeError:
            self.__master = None
        # __destroyed
        try:
            self.__destroyed
        except AttributeError:
            self.__destroyed = False

    def __bind_destroy_event(self):
        command = (lambda event,
                          widget=self.body,
                          callback=self.__exec_on_destroy:
                   callback() if event.widget is widget else None)
        self.body.bind("<Destroy>", command, "+")

    def __exec_on_display(self):
        try:
            self.body.wait_visibility()
        except Exception as e:
            pass
        else:
            self._on_display()
            self.__state = DISPLAYED

    def __exec_on_destroy(self):
        if not self.__built or self.__destroyed:
            return
        self.__destroyed = True
        self._on_destroy()
        self.__state = DESTROYED
        window_manager = self.body.winfo_manager()
        # Hide the window first to avoid the visual slow destruction
        # of each child
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
        try:
            self.body.destroy()
        except Exception as e:
            pass
        try:
            if self.__master.focus_get() is None:
                self.__master.winfo_toplevel().focus_lastfor().focus_force()
        except Exception as e:
            pass
