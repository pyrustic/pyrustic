from abc import ABC, abstractmethod
from pyrustic import tkmisc
import tkinter as tk


class Viewable(ABC):
    """
    This is the abstract class to subclass if you are going to create a view.

    Lifecycle of a view:
        1- instantiate
        2- -> '__init__()' is implicitly called
        3- call the method '.build()'
        4- -> '_on_build()' is implicitly called
        5- -> '_on_display()' is implicitly called once the window is visible
        6- -> '_on_destroy()' is implicitly called when the window is destroyed/closed

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
     object (the body), the method '_on_destroy()' will be called AFTER the beginning of destruction
     of the body.
    """
    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)
        instance._body = None
        instance.__built = False
        instance.__master = None
        instance.__destroyed = False
        return instance

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
        Build the view.
        """
        return self.__build()

    def destroy(self):
        """
        Destroy the body of this view
        """
        return self.__exec_on_destroy(destroy=True)

    # ==============================================
    #               METHODS TO IMPLEMENT
    # ==============================================

    @abstractmethod
    def _on_build(self):
        """
        You assign your tkinter window to an instance variable "_body" here.
        Put here the code that build the body of this view.
        It will be executed when you will call the method "build()".
        """
        pass

    @abstractmethod
    def _on_display(self):
        """
        Put here the code that will be executed once the body is visible.
        """
        pass

    @abstractmethod
    def _on_destroy(self):
        """
        Put here the code that will be executed as clean-up.
        """
        pass

    # ==============================================
    #                 INTERNAL METHODS
    # ==============================================

    def __build(self):
        if self.__built:
            return self._body
        self._on_build()
        self.__built = True
        if self._body:
            self.__master = self._body.master
            self._body.after(0, self.__exec_on_display)
        return self._body

    def __exec_on_display(self):
        try:
            self._body.wait_visibility()
        except Exception as e:
            pass
        else:
            tkmisc.handle_on_destroy(self._body, self.__exec_on_destroy)
            self._on_display()

    def __exec_on_destroy(self, destroy=False):
        if self.__built and not self.__destroyed:
            self.__destroyed = True
            self._on_destroy()
            if destroy:
                self._body.destroy()
            if self.__master.focus_get() is None:
                self.__master.winfo_toplevel().focus_lastfor().focus_force()
