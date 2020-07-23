import tkinter as tk
from pyrustic.abstract.viewable import Viewable
from pyrustic import tkmisc


class Dialog(Viewable):
    """
    This is Dialog ! A cool class to use if u want to pop-up a toplevel centered on screen.
    The Pyrustic-Widgets 'toast', 'choice' and 'confirm' use Dialog as base class.

    Don't use Dialog directly, instead, subclass it.
    You can override the method '_on_center()' if you don't like the default 'center' algorithm.
    """

    # =============================================
    #              PUBLIC METHODS
    # =============================================
    def build(self):
        """
        Build the dialog with this method. The program execution flow won't be interrupted.
        If u want the program execution flow to block till the dialog is close,
        so use the method 'build_wait()'
        """
        return self.__build()

    def build_wait(self):
        """
        This method build the dialog then block the flow of execution of the program till
        you close the dialog.
        """
        if not self.__built:
            self.__build()
            if self._body:
                self._body.wait_window(self._body)
        return self._body

    # =============================================
    #              IMPLEMENT THESE METHODS
    # =============================================
    def _on_build(self):
        pass

    def _on_display(self):
        pass

    def _on_destroy(self):
        pass

    def _on_center(self):
        """
        If you override this, then the dialog won't be centered on screen anymore.
        """
        tkmisc.center_window(self._body, within=self.__master)

    # =============================================
    #                   INTERNAL
    # =============================================
    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)
        instance.__built = None
        instance.__master = None
        return instance

    def __build(self):
        if self.__built:
            return self._body
        super().build()
        self.__built = True
        if self._body:
            self.__master = self._body.master
            self._body.after(0, self.__set_dialog_effect_then_center)
        return self._body

    def __set_dialog_effect_then_center(self):
        try:
            self._body.wait_visibility(window=self._body)
        except Exception as e:
            pass
        else:
            tkmisc.dialog_effect(self._body)
            self._on_center()


# =============================================
#                   DEMO DIALOG
# =============================================
class _Demo(Dialog):
    def __init__(self):
        self._body = None

    def _on_build(self):
        self._body = tk.Toplevel()
        self._body.geometry("300x100")
        self._body.title("My Dialog")
        tk.Label(self._body, text="Hi ! I am Dialog !").pack()
        tk.Button(self._body, text="Close", command=self._body.destroy).pack()

    def _on_display(self):
        pass

    def _on_destroy(self):
        pass


if __name__ == "__main__":
    app = tk.Tk()
    app.title("Main Window")
    app.geometry("500x500+0+0")
    tk.Button(app, text="Launch Dialog", command=lambda: _Demo().build()).pack()
    tk.Button(app, text="Print Hello", command=lambda: print("Hello !")).pack()
    app.mainloop()
