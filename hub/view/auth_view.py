from pyrustic.viewable import Viewable
from pyrustic import tkmisc
import tkinter as tk


class AuthView(Viewable):
    def __init__(self, master, main_view, main_host):
        self._master = master
        self._main_view = main_view
        self._main_host = main_host
        self._body = None
        self._strvar_token = tk.StringVar()
        self._data_submitted = False

    def _on_build(self):
        self._body = tk.Toplevel(self._master)
        self._body.title("Authentication")
        # token
        label = tk.Label(self._body, text="Token")
        label.pack(anchor="w", padx=5, pady=(10, 0))
        entry = tk.Entry(self._body, show="*",
                         textvariable=self._strvar_token)
        entry.pack(anchor="w", fill=tk.X, padx=5, pady=(0, 30))
        entry.focus_set()
        entry.bind("<Return>", lambda e, self=self: self._on_click_auth())
        # footer
        footer = tk.Frame(self._body)
        footer.pack(padx=2, pady=2)
        # button auth
        button_auth = tk.Button(footer, name="button_confirm",
                                text="Authenticate",
                                command=self._on_click_auth)
        button_auth.pack(side=tk.RIGHT)
        # button cancel
        button_cancel = tk.Button(footer, name="button_cancel",
                                  text="Cancel",
                                  command=self._on_click_cancel)
        button_cancel.pack(side=tk.RIGHT, padx=(5, 2))

    def _on_display(self):
        tkmisc.dialog_effect(self._body)

    def _on_destroy(self):
        if not self._data_submitted:
            self._main_view.footer_view.cancel_authenticating()

    def _on_click_auth(self):
        token = self._strvar_token.get()
        if token:
            consumer = (lambda code, info, data:
                        self._main_view.footer_view.set_auth(code, info, data))
            self._main_view.threadium.task(self._main_host.auth, args=[token],
                                           consumer=consumer, unpack_result=True)
            self._data_submitted = True
            self._main_view.footer_view.notify_authenticating()
        self.destroy()

    def _on_click_cancel(self):
        self.destroy()
