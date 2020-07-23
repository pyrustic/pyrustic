import tkinter as tk
from pyrustic.widget.dialog import Dialog


class Toast(Dialog):
    """
    This is Toast ! Based on Dialog, this class pop-up a dialog for a given duration.
    Any 'click' action on the app will destroy the toast.
    Example:
        import tkinter as tk
        from pyrustic.widget.toast import Toast
        root = tk.Tk()
        Toast(root, header="My Header", message="My Message")
        root.mainloop()

    """

    def __init__(self,
                 master=None,
                 title=None,
                 header=None,
                 message=None,
                 duration=2000,
                 decoration=False,
                 geometry=None,
                 options={}):
        """
        - master: a tkinter widget object
        - title: str, the title of the dialog (if you set 'decoration' to True)
        - header: str, the header text
        - message: str, message to show
        - duration: int, in milliseconds.
            You can set None to duration to cancel the self-destroying timer
        - decoration: True or False to allow Window decoration
        - geometry: str, the same geometry as described in tkinter doc. Example: "300x200+0+0"
        - options: dictionary, these options will be used as argument to the widget's constructors.
            The widgets are: body, label_header and label_message.
            Example: Assume that you want to set the label_message's background to black
            and the body's background to red:
                options = {"body": {"background": "red"},
                           "label_message": {"background": "black"}}
        """
        self._master = master
        self._title = title
        self._header = header
        self._message = message
        self._duration = duration
        self._decoration = decoration
        self._geometry = geometry
        self._options = options
        self._body_options = None
        self._label_header_options = None
        self._label_message_options = None
        self._parse_options(options)
        self._body = None
        self._cancel_id = None
        self._components = {}
        self.build()

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
        Get the components used to build this dialog.
        This property returns a dict. The keys are:
            'body', 'label_header', and 'label_message'
        """
        return self._components

    # ======================================
    #            INTERNAL
    # ======================================
    def _on_build(self):
        self._body = tk.Toplevel(self._master,
                                 class_="Toast",
                                 cnf=self._body_options)
        self._components["body"] = self._body
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
            self._components["label_header"] = label_header
            label_header.pack(fill=tk.X, padx=10, pady=10)
        if self._message:
            label_message = tk.Label(self._body,
                               name="message",
                               text=self._message,
                               anchor="w",
                               justify=tk.LEFT,
                               cnf=self._label_message_options)
            self._components["label_message"] = label_message
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
        self._body_options = options["body"] if "body" in options else {}
        self._label_header_options = options["label_header"] if "label_header" in options else {}
        self._label_message_options = options["label_message"] if "label_message" in options else {}


if __name__ == "__main__":
    def launch_toast(root):
        print("toasting !")
        Toast(root,
              title="Pyrustic Toast",
              header="This is the long\nheader",
              message="Hello !\nThis is the message")

    root = tk.Tk()
    root.geometry("500x500+0+0")
    tk.Button(root, text="Launch Toast",
              command=lambda root=root: launch_toast(root)).pack()
    root.mainloop()
