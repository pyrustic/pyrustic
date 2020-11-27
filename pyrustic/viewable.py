import tkinter as tk
from pyrustic import tkmisc
from pyrustic.exception import PyrusticException


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
    - You need to implement the methods '_on_build()', '_on_display()' and '_on_destroy'.
    - You need to assign a tkinter object to the instance variable
        '_body' in the '_on_build()' method.
    That's all ! Of course, when you are ready to use the view, just call the 'build()' method.
    Calling the 'build()' method will return the body of the view. The one that you assigned
    to the instance variable '_body'. The same body can be retrieved with the property 'body'.
    The 'build()' method should be called once. Calling it more than once will still return
    the body object, but the view won't be built again.
    You can't re-build your view after destroying its body.
    You can destroy the body directly, by calling the conventional tkinter destruction method
     on that view. You can also destroy the body indirectly by calling the view's method
     'destroy()' inherited from the abstract class Viewable.
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
        return self._body

    # ==============================================
    #                 PUBLIC METHODS
    # ==============================================

    def build(self):
        """
        Build the view. Return the body
        """
        return self.__build()

    def build_pack(self, cnf={}, **kwargs):
        body = self.build()
        body.pack(cnf=cnf, **kwargs)

    def build_grid(self, cnf={}, **kwargs):
        body = self.build()
        body.grid(cnf=cnf, **kwargs)

    def build_place(self, cnf={}, **kwargs):
        body = self.build()
        body.place(cnf=cnf, **kwargs)

    def build_wait(self):
        """
        Build the view. Return the body
        """
        body = self.__build()
        if body:
            body.wait_window(body)

    def destroy(self):
        """
        Destroy the body of this view
        """
        self.build()
        return self.__exec_on_destroy(destroy=True)

    # ==============================================
    #               METHODS TO IMPLEMENT
    # ==============================================

    def _on_build(self):
        """
        You assign your tkinter window to an instance variable "_body" here.
        Put here the code that build the body of this view.
        It will be executed when you will call the method "build()".
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
        tkmisc.center_window(self._body, self.__master.winfo_toplevel())

    # ==============================================
    #                 INTERNAL METHODS
    # ==============================================

    def __build(self):
        self.__set_default_attributes()
        if self.__built:
            return self._body
        self._on_build()
        self.__built = True
        if self._body:
            self.__master = self._body.master
            if isinstance(self._body, tk.Toplevel):
                self.__toplevel = True
                self.__bind_destroy_event()
                self._toplevel_geometry()
                try:
                    self._body.wait_visibility()
                except Exception as e:
                    pass
                else:
                    self._on_display()
            elif isinstance(self._body, tk.Frame):
                self.__bind_destroy_event()
                self._body.after(0, self.__exec_on_display)
            else:
                message = "The body of a viewable should be a tk.Frame or a tk.Toplevel"
                raise PyrusticException(message)
        return self._body

    def __set_default_attributes(self):
        # __built
        try:
            self.__built
        except AttributeError:
            self.__built = False
        else:
            return
        # __toplevel
        try:
            self.__toplevel
        except AttributeError:
            self.__toplevel = False
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
        # _body
        try:
            self._body
        except AttributeError:
            self._body = None

    def __bind_destroy_event(self):
        command = (lambda event,
                          widget=self._body,
                          callback=self.__exec_on_destroy:
                   callback() if event.widget is widget else None)
        self._body.bind("<Destroy>", command, "+")

    def __exec_on_display(self):
        try:
            self._body.wait_visibility()
        except Exception as e:
            pass
        else:
            self._on_display()

    def __exec_on_destroy(self, destroy=False):
        if self.__built and not self.__destroyed:
            self.__destroyed = True
            self._on_destroy()
            if destroy:
                self._body.destroy()
            if self.__master.focus_get() is None:
                self.__master.winfo_toplevel().focus_lastfor().focus_force()
