import tkinter as tk
from pyrustic import tkmisc
from pyrustic.viewable import Viewable


# Components
BODY = "body"
LABEL_HEADER = "label_header"
TEXT_MESSAGE = "text_message"
LABEL_MESSAGE = "label_message"
FRAME_FOOTER = "frame_footer"
BUTTON_CANCEL = "button_cancel"
BUTTON_CONFIRM = "button_confirm"


class Confirm(Viewable):
    """
    Confirm is a dialog box to ask the user to confirm an action.

    Example:

        import tkinter as tk
        from pyrustic.widget.confirm import Confirm

        def my_handler(result):
            print(result)

        root = tk.Tk()
        confirm = Confirm(root, title="Confirm", header="Confirmation",
                        message="Do you really want to continue ?",
                        handler=my_handler)
        confirm.build()
        root.mainloop()

    """
    def __init__(self,
                 master=None,
                 title=None,
                 header=None,
                 message=None,
                 is_long_message=False,
                 handler=None,
                 geometry=None,
                 options=None):
        """
        PARAMETERS:

        - master: widget parent. Example: an instance of tk.Frame

        - title: title of dialog box

        - header: the text to show as header

        - message: the text to show as message

        - is_long_message: bool, set it to True if you want the message
        widget to be a Text. Set it to False if you want the message to be a Label

        - handler: a callback to be executed immediately after closing the dialog box.
            This callback should accept a boolean positional argument.
            True means Ok, confirmed.

        - geometry: str, as the dialog box is a toplevel (BODY),
         you can edit its geometry. Example: "500x300"

        - options: dictionary of widgets options
            The widgets keys are: BODY, LABEL_HEADER, TEXT_MESSAGE,
             LABEL_MESSAGE, FRAME_FOOTER, BUTTON_CANCEL, BUTTON_CONFIRM.

            Example: Assume that you want to set the LABEL_MESSAGE's background to black
            and the BODY's background to red:
                options = { BODY: {"background": "red"},
                            LABEL_MESSAGE: {"background": "black"} }

        """
        self._master = master
        self._title = title
        self._header = header
        self._message = message
        self._is_long_message = is_long_message
        self._handler = handler
        self._geometry = geometry
        self._body = None
        self._options = {} if options is None else options
        self._body_options = None
        self._label_header_options = None
        self._text_message_options = None
        self._label_message_options = None
        self._frame_footer_options = None
        self._button_cancel_options = None
        self._button_confirm_options = None
        self._parse_options(self._options)
        self._components = {}
        self._ok = False

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
    def is_long_message(self):
        return self._is_long_message

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
    def ok(self):
        """
        Returns True if user confirmed, else get False
        """
        return self._ok

    @property
    def components(self):
        """
        Get the components (widgets instances) used to build this dialog.

        This property returns a dict. The keys are:
            BODY, LABEL_HEADER, TEXT_MESSAGE,
            LABEL_MESSAGE, FRAME_FOOTER, BUTTON_CANCEL, BUTTON_CONFIRM

        Warning: check the presence of key before usage. Example,
        the widget linked to the LABEL_MESSAGE key may be missing because
        TEXT_MESSAGE replaced it
        """
        return self._components

    # ====================================
    #               INTERNAL
    # ====================================
    def _on_build(self):
        self._body = tk.Toplevel(self._master,
                                 class_="Confirm",
                                 cnf=self._body_options)
        self._body.resizable(0, 0)
        self._components[BODY] = self._body
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
            self._components[LABEL_HEADER] = label_header
            label_header.pack(fill=tk.X, expand=1, anchor="w", pady=5, padx=5)
        #
        if self._message:
            if self._is_long_message:
                text_message = tk.Text(self._body,
                               wrap="word",
                               width=35,
                               height=5,
                               name="long_message",
                               cnf=self._text_message_options)
                self._components[TEXT_MESSAGE] = text_message
                text_message.pack(fill=tk.BOTH, expand=1, padx=5, pady=5)
                text_message.insert("end", self._message)
                text_message.config(state="disabled")
            else:
                label_message = tk.Label(self._body,
                                         name="message",
                                         text=self._message,
                                         anchor="w",
                                         cnf=self._label_message_options)
                self._components[LABEL_MESSAGE] = label_message
                label_message.pack(fill=tk.BOTH,
                                   expand=1, padx=5, pady=(5, 10))
        #
        frame_footer = tk.Frame(self._body, cnf=self._frame_footer_options)
        self._components[FRAME_FOOTER] = frame_footer
        frame_footer.pack(anchor="e", pady=(0, 2), padx=2)
        #
        button_confirm = tk.Button(frame_footer,
                                   text="Confirm",
                                   name="confirm",
                                   command=self._on_click_confirm,
                                   cnf=self._button_confirm_options)
        self._components[BUTTON_CONFIRM] = button_confirm
        button_confirm.pack(side=tk.RIGHT)
        #
        button_cancel = tk.Button(frame_footer,
                                  text="Cancel",
                                  name="cancel",
                                  command=self._on_click_cancel,
                                  cnf=self._button_cancel_options)
        self._components[BUTTON_CANCEL] = button_cancel
        button_cancel.pack(side=tk.RIGHT, padx=(0, 2))

    def _on_display(self):
        pass

    def _on_destroy(self):
        if self._handler:
            self._handler(self._ok)

    def _toplevel_geometry(self):
        super()._toplevel_geometry()
        tkmisc.dialog_effect(self._body)

    def _on_click_cancel(self):
        self._ok = False
        self._body.destroy()

    def _on_click_confirm(self):
        self._ok = True
        self._body.destroy()

    def _parse_options(self, options):
        self._body_options = (options[BODY] if BODY in options else {})
        self._label_header_options = (options[LABEL_HEADER]
                                      if LABEL_HEADER in options else {})
        self._text_message_options = (options[TEXT_MESSAGE]
                                      if TEXT_MESSAGE in options else {})
        self._label_message_options = (options[LABEL_MESSAGE]
                                       if LABEL_MESSAGE in options else {})
        self._frame_footer_options = (options[FRAME_FOOTER]
                                      if FRAME_FOOTER in options else {})
        self._button_cancel_options = (options[BUTTON_CANCEL]
                                       if BUTTON_CANCEL in options else {})
        self._button_confirm_options = (options[BUTTON_CONFIRM]
                                        if BUTTON_CONFIRM in options else {})


class _ConfirmTest(Viewable):
    def __init__(self, root):
        self._root = root
        self._body = None
        self._text_widget = None

    def _on_build(self):
        self._body = tk.Frame(self._root)
        btn_launch = tk.Button(self._body, text="Launch",
                               command=self._on_click_launch)
        btn_launch.pack()

    def _on_display(self):
        pass

    def _on_destroy(self):
        pass

    def _on_click_launch(self):
        confirm = Confirm(root, title="Confirm",
                          header="Confirmation",
                          message="Do you really want to continue ?")
        confirm.build_wait()
        print("Confirm:", confirm.ok)


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("500x300+0+0")
    confirm_test = _ConfirmTest(root)
    confirm_test.build_pack()
    root.mainloop()
