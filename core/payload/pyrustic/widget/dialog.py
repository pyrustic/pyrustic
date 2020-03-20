import tkinter as tk
from pyrustic.abstract.viewable import Viewable


class Dialog(Viewable):
    """
    This is Dialog ! A cool class to use if u want to pop-up a toplevel centered on screen.
    The Pyrustic-Widgets 'toast' and 'choice' use Dialog as base class.

    The recommended way to use Dialog is to subclass it.

    PROPRIETIES
    ===========
    - body: get the body. This body won't exist if ur dialog use wait_window (check method 'show')

    METHODS
    =======
    - show(self, wait_window=True, body=None): show the dialog.
        The boolean wait_window when set to True, pause the execution of code after
        invocation of this method till the dialog is destroyed.
        The parameter 'body' can hold a toplevel already created. This toplevel will be centered
        and will react like another dialog implemented by subclassing Dialog.
        This method returns 'result' that you can put as argument
        to the method 'close(self, result=None)'.
        Example:
            from tkinter import *
            app = Tk()
            dialog = Dialog()
            my_toplevel = Toplevel(app)
            Button(my_toplevel, text="close dialog", command=dialog.close(result=20)).pack()
            result = dialog.show(body=my_toplevel)
            print(result) # 20
            print(dialog.result) # 20
            app.mainloop()

    - build(self, wait_window=True, body=None): alias for show. This method exists because Dialog
        uses the abstract class Viewable. For clarity, it is recommanded to use 'show' for
        toplevels, and use 'build' for others

    - close(self, result=None): close the dialog


    NOTE: When u subclass Dialog, u can create an __init__ method if you want, but u must implement
    the methods: _on_start(self); _on_build(self); _on_display(); _on_close(self, **kwargs)
    The method _on_build(self) must return the body of dialog, the one that should be closed
    if user click on close
    """

    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)
        instance.__body = None
        instance.__result = None
        return instance

    @property
    def body(self):
        return self.__body

    @property
    def result(self):
        return self.__result

    def show(self, wait_window=True, body=None):
        return self.__build(wait_window, body)

    def build(self, wait_window=True, body=None):
        return self.__build(wait_window, body)

    def _on_start(self):
        pass

    def _on_build(self):
        pass

    def _on_display(self):
        pass

    def _on_close(self, result=None):
        pass

    def close(self, result=None):
        if self.__body:
            self._on_close(result=result)
            self.__body.destroy()
            for key, val in self.__dict__.items():
                self.__dict__[key] = None
            self.__result = result

    # ================== INTERNAL =================
    def __build(self, wait_window, body):
        self._on_start()
        self.__body = self._on_build()
        if not self.__body:
            if body:
                self.__body = body
            else:
                self.__body = self.__build_default_body()
        #self.__body.lower()
        self.__center_window(self.__body)
        self.__body.wait_visibility(self.__body)
        self._on_display()
        self.__body.protocol("WM_DELETE_WINDOW", self.close)
        self.__body.transient(self.__body.master)
        self.__body.lift()
        self.__body.grab_set()
        self.__body.focus_set()
        if not wait_window:
            return self.__body
        self.__body.master.wait_window(self.__body)
        return self.__result

    def __build_default_body(self):
        body = tk.Toplevel(width=300, height=200)
        body.title("Pyrustic Dialog")
        tk.Label(body, text="Empty Dialog").pack()
        tk.Button(body, text="Close", command=self.close).pack()
        return body

    def __center_window(self, window):
        self.__body.update_idletasks()
        reqwidth = window.winfo_reqwidth()
        reqheight = window.winfo_reqheight()
        x = (window.winfo_screenwidth() // 2) - (reqwidth // 2)
        y = (window.winfo_screenheight() // 2) - (reqheight // 2)
        window.geometry("{}x{}+{}+{}".format(reqwidth, reqheight, x, y))


if __name__ == "__main__":
    app = tk.Tk()
    dialog = Dialog()
    toplevel = tk.Toplevel()
    tk.Label(toplevel, text="Hello Friend !").pack()
    tk.Button(toplevel, text="Close", command=dialog.close).pack()
    dialog.show(body=toplevel, wait_window=False)
    app.mainloop()
