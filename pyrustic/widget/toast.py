import tkinter as tk
from pyrustic import widget
from pyrustic.view import View, CustomView
from pyrustic.tkmisc import merge_cnfs
from pyrustic import tkmisc


# Components
LABEL_HEADER = "label_header"
LABEL_MESSAGE = "label_message"


class Toast(widget.Toplevel):
    """
    A toast is a dialog box with or without decoration
    that is displayed for a given duration.

    Any "click" action on the Toast's body will close it.

    Example:
        import tkinter as tk
        from pyrustic.widget.toast import Toast

        root = tk.Tk()
        toast = Toast(root, header="My Header", message="My Message")
        toast.build()
        root.mainloop()

    """

    def __init__(self,
                 master=None,
                 title=None,
                 header=None,
                 message=None,
                 duration=1234,
                 decoration=False,
                 geometry=None,
                 cnfs=None):
        """
        PARAMETERS:

        - master: widget parent. Example: an instance of tk.Frame

        - title: title of dialog box

        - header: the text to show as header

        - message: the text to show as message

        - duration: int, in milliseconds.
            You can set None to duration to cancel the self-destroying timer

        - decoration: True or False to allow Window decoration

        - geometry: str, as the dialog box is a toplevel (BODY),
         you can edit its geometry. Example: "500x300"

        - options: dictionary of widgets options
            The widgets keys are: BODY, LABEL_HEADER, LABEL_MESSAGE.

            Example: Assume that you want to set the LABEL_MESSAGE's background to black
            and the BODY's background to red:
                options = { BODY: {"background": "red"},
                            LABEL_MESSAGE: {"background": "black"} }
        """
        self.__cnfs = merge_cnfs(None, cnfs, components=("body",
                        LABEL_HEADER, LABEL_MESSAGE))
        super().__init__(master=master,
                         class_="Toast",
                         cnf=self.__cnfs["body"],
                         on_build=self.__on_build,
                         on_display=self.__on_display,
                         on_destroy=self.__on_destroy,
                         toplevel_geometry=self.__toplevel_geometry)
        self.__title = title
        self.__header = header
        self.__message = message
        self.__duration = duration
        self.__decoration = decoration
        self.__geometry = geometry
        self.__cancel_id = None
        self.__components = {}
        self.__view = self.build()

    # ======================================
    #            PROPERTIES
    # ======================================

    @property
    def header(self):
        return self.__header

    @property
    def message(self):
        return self.__message

    @property
    def duration(self):
        return self.__duration

    @property
    def decoration(self):
        return self.__decoration

    @property
    def components(self):
        """
        Get the components (widgets instances) used to build this Toast.

        This property returns a dict. The keys are:
            BODY, LABEL_HEADER, LABEL_MESSAGE,
        """
        return self.__components

    # ======================================
    #            LIFECYCLE
    # ======================================
    def __on_build(self):
        if not self.__decoration:
            self.overrideredirect(1)
        if self.__geometry:
            self.geometry(self.__geometry)
        if self.__title:
            self.title(self.__title)
        self.bind("<Button-1>", self.__on_click, "+")
        if self.__header:
            label_header = tk.Label(self,
                                    name=LABEL_HEADER,
                                    text=self.__header,
                                    anchor="w",
                                    justify=tk.LEFT,
                                    cnf=self.__cnfs[LABEL_HEADER])
            self.__components[LABEL_HEADER] = label_header
            label_header.pack(fill=tk.X, padx=10, pady=10)
        if self.__message:
            label_message = tk.Label(self,
                                     name=LABEL_MESSAGE,
                                     text=self.__message,
                                     anchor="w",
                                     justify=tk.LEFT,
                                     cnf=self.__cnfs[LABEL_MESSAGE])
            self.__components[LABEL_MESSAGE] = label_message
            label_message.pack(fill=tk.X, padx=10, pady=10)

    def __on_display(self):
        if self.__duration is not None:
            self.__cancel_id = self.after(self.__duration, self.destroy)

    def __on_destroy(self):
        pass

    def __toplevel_geometry(self):
        tkmisc.center_window(self, within=self.master.winfo_toplevel())
        tkmisc.dialog_effect(self)

    def __on_click(self, event):
        self.destroy()


class _ToastTest(View):

    def __init__(self, root):
        super().__init__()
        self._root = root
        self._body = None

    def _on_build(self):
        self._body = tk.Frame(self._root)
        btn_launch = tk.Button(self._body, text="launch",
                               command=self._on_click_launch)
        btn_launch.pack()

    def _on_display(self):
        pass

    def _on_destroy(self):
        pass

    def _on_click_launch(self):
        Toast(self._body, title="Toast Title",
              header="Header", message="This is the message",
              duration=3000)


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("500x300+0+0")
    toast_test = _ToastTest(root)
    toast_test.build_pack()
    root.mainloop()
