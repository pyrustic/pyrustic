import tkinter as tk
from pyrustic.widget.dialog import Dialog


class Confirm(Dialog):
    """
    Confirm is based on Dialog.
    This dialog will help you to get a confirmation from the user.
    You can configure this dialog to block or not the flow of your app.
    By default, this dialog blocks the flow of your app. Check the parameter 'wait'.

    Example:
        import tkinter as tk
        root = tk.Tk()
        Confirm(root, title="Title", header="Header", message="Message")
        root.mainloop()
    """
    def __init__(self,
                 master=None,
                 title=None,
                 header=None,
                 message=None,
                 handler=None,
                 geometry=None,
                 wait=True,
                 options={}):
        """
        - master: a tkinter widget object
        - title: str, the title of the dialog (if you set 'decoration' to True)
        - header: str, the header text
        - message: str, message to show
        - handler: a callback that will be called when the dialog will be closed.
            This callback should accept a boolean positional argument. True means Ok, confirmed.
        - geometry: str, the same geometry as described in tkinter doc. Example: "300x200+0+0"
        - wait: boolean to indicate if this dialog should block the app execution flow
        - options: dictionary, these options will be used as argument to the widget's constructors.
            The widgets are: 'body', 'label_header', 'text_message', 'frame_footer',
            'button_cancel', 'button_confirm'.

            Example: Assume that you want to set the text_message's background to black
            and the body's background to red:
                options = {"body": {"background": "red"},
                           "text_message": {"background": "black"}}
        """
        self._master = master
        self._title = title
        self._header = header
        self._message = message
        self._handler = handler
        self._geometry = geometry
        self._wait = wait
        self._body = None
        self._options = options
        self._body_options = None
        self._label_header_options = None
        self._text_message_options = None
        self._frame_footer_options = None
        self._button_cancel_options = None
        self._button_confirm_options = None
        self._parse_options(options)
        self._components = {}
        self._ok = False
        if self._wait:
            self.build_wait()
        else:
            self.build()

    # ====================================
    #           PROPERTIES
    # ====================================
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
    def handler(self):
        return self._handler

    @property
    def geometry(self):
        return self._geometry

    @property
    def options(self):
        return self._options

    @property
    def wait(self):
        return self._wait

    @property
    def ok(self):
        """
        Get True if user confirmed, else get False
        """
        return self._ok

    @property
    def components(self):
        """
        Get the components used to build this dialog.
        This property returns a dict. The keys are:
            'body', 'label_header', 'text_message', 'frame_footer',
            'button_cancel', 'button_confirm'
        """
        return self._components

    # ====================================
    #               INTERNAL
    # ====================================
    def _on_build(self):
        self._body = tk.Toplevel(self._master,
                                 class_="Confirm",
                                 cnf=self._body_options)
        self._components["body"] = self._body
        #
        if self._title:
            self._body.title(self._title)
        #
        if self._geometry:
            self._body.geometry(self._geometry)
        #
        if self._header:
            label_header = tk.Label(self._body,
                             text=self._header,
                             anchor="w",
                             name="header",
                             cnf=self._label_header_options)
            self._components["label_header"] = label_header
            label_header.pack(fill=tk.X, expand=1, anchor="w", pady=3, padx=3)
        #
        if self._message:
            text_message = tk.Text(self._body,
                           wrap="word",
                           width=35,
                           height=5,
                           name="message",
                           cnf=self._text_message_options)
            self._components["text_message"] = text_message
            text_message.pack(fill=tk.BOTH, expand=1, padx=3, pady=(0, 2))
            text_message.insert("end", self._message)
            text_message.config(state="disabled")
        #
        frame_footer = tk.Frame(self._body, cnf=self._frame_footer_options)
        self._components["frame_footer"] = frame_footer
        frame_footer.pack(anchor="e", pady=(0, 3), padx=3)
        #
        button_confirm = tk.Button(frame_footer,
                                   text="Confirm",
                                   name="confirm",
                                   command=self._on_click_confirm,
                                   cnf=self._button_confirm_options)
        self._components["button_confirm"] = button_confirm
        button_confirm.pack(side=tk.RIGHT)
        #
        button_cancel = tk.Button(frame_footer,
                                  text="Cancel",
                                  name="cancel",
                                  command=self._on_click_cancel,
                                  cnf=self._button_cancel_options)
        self._components["button_cancel"] = button_cancel
        button_cancel.pack(side=tk.RIGHT, padx=(0, 3))

    def _on_display(self):
        pass

    def _on_destroy(self):
        if self._handler:
            self._handler(self._ok)

    def _on_click_cancel(self):
        self._ok = False
        self._body.destroy()

    def _on_click_confirm(self):
        self._ok = True
        self._body.destroy()

    def _parse_options(self, options):
        self._body_options = options["body"] if "body" in options else {}
        self._label_header_options = options["label_header"] if "label_header" in options else {}
        self._text_message_options = options["text_message"] if "text_message" in options else {}
        self._frame_footer_options = options["frame_footer"] if "frame_footer" in options else {}
        self._button_cancel_options = options["button_cancel"] if "button_cancel" in options else {}
        self._button_confirm_options = options["button_confirm"] if "button_confirm" in options else {}


if __name__ == "__main__":
    def launch(root):
        confirm = Confirm(root, title="Title",
                          header="Header", message="My Message")
        print("Confirm:", confirm.ok)

    root = tk.Tk()
    root.geometry("500x500+0+0")
    tk.Button(root,
              text="Launch",
              command=lambda root=root: launch(root)).pack()
    root.mainloop()
