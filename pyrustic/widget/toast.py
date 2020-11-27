import tkinter as tk
from pyrustic.viewable import Viewable


# Components
BODY = "body"
LABEL_HEADER = "label_header"
LABEL_MESSAGE = "label_message"


class Toast(Viewable):
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
                 options=None):
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
        self._master = master
        self._title = title
        self._header = header
        self._message = message
        self._duration = duration
        self._decoration = decoration
        self._geometry = geometry
        self._options = {} if options is None else options
        self._body_options = None
        self._label_header_options = None
        self._label_message_options = None
        self._parse_options(self._options)
        self._body = None
        self._cancel_id = None
        self._components = {}

    # ======================================
    #            PROPERTIES
    # ======================================
    @property
    def master(self):
        return self._master

    @property
    def title(self):
        return self._title

    @property
    def header(self):
        return self._header

    @property
    def message(self):
        return self._message

    @property
    def duration(self):
        return self._duration

    @property
    def decoration(self):
        return self._decoration

    @property
    def geometry(self):
        return self._geometry

    @property
    def options(self):
        return self._options

    @property
    def components(self):
        """
        Get the components (widgets instances) used to build this Toast.

        This property returns a dict. The keys are:
            BODY, LABEL_HEADER, LABEL_MESSAGE,
        """
        return self._components

    # ======================================
    #            LIFECYCLE
    # ======================================
    def _on_build(self):
        self._body = tk.Toplevel(self._master,
                                 class_="Toast",
                                 cnf=self._body_options)
        self._components[BODY] = self._body
        if not self._decoration:
            self._body.overrideredirect(1)
        if self._geometry:
            self._body.geometry(self._geometry)
        if self._title:
            self._body.title(self._title)
        self._body.bind("<Button-1>", self._on_click, "+")
        if self._header:
            label_header = tk.Label(self._body,
                              name="header",
                              text=self._header,
                              anchor="w",
                              justify=tk.LEFT,
                              cnf=self._label_header_options)
            self._components[LABEL_HEADER] = label_header
            label_header.pack(fill=tk.X, padx=10, pady=10)
        if self._message:
            label_message = tk.Label(self._body,
                               name="message",
                               text=self._message,
                               anchor="w",
                               justify=tk.LEFT,
                               cnf=self._label_message_options)
            self._components[LABEL_MESSAGE] = label_message
            label_message.pack(fill=tk.X, padx=10, pady=10)

    def _on_display(self):
        if self._duration is not None:
            self._cancel_id = self._body.after(self._duration, self._body.destroy)

    def _on_destroy(self):
        pass

    def _on_click(self, event):
        if self._body:
            self._body.destroy()

    def _parse_options(self, options):
        self._body_options = (options[BODY] if BODY in options else {})
        self._label_header_options = (options[LABEL_HEADER]
                                      if LABEL_HEADER in options else {})
        self._label_message_options = (options[LABEL_MESSAGE]
                                       if LABEL_MESSAGE in options else {})


class _ToastTest(Viewable):

    def __init__(self, root):
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
        toast = Toast(self._body, title="Toast Title",
                      header="Header", message="This is the message",
                      duration=3000)
        toast.build_wait()


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("500x300+0+0")
    toast_test = _ToastTest(root)
    toast_test.build_pack()
    root.mainloop()
