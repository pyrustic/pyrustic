import tkinter as tk
from pyrustic.viewable import Viewable
from pyrustic.widget.toast import Toast
from pyrustic.widget.choice import Choice
from pyrustic.private.tool.hub.view.auth_view import AuthView
from pyrustic.private.tool.hub.view.publishing_view import PublishingView


class FooterView(Viewable):
    def __init__(self, master, main_view, main_host):
        self._master = master
        self._main_view = main_view
        self._main_host = main_host
        self._body = None
        self._auth_view = None
        self._auth_strvar = tk.StringVar(value="Authenticate")
        self._auth_intvar = tk.IntVar(value=0)
        self._cache = None
        self._toast_auth = None

    # ===================================
    #              PUBLIC
    # ===================================
    def set_auth(self, code, info, data):
        if code in (200, 304):
            text = "Authenticated ({})".format(data)
            self._cache = (1, text)
            self._auth_strvar.set(text)
            self._auth_intvar.set(1)
            welcome_text = "Welcome Friend"
            if code == 304:
                welcome_text = "Welcome back Friend !"
            Toast(message=welcome_text).build()
        else:
            Toast(message=info).build()
            self.cancel_authenticating()
        if self._toast_auth:
            self._toast_auth.destroy()
            self._toast_auth = None

    def notify_authenticating(self):
        message = "Authenticating..."
        self._toast_auth = Toast(self._body, message=message, duration=None)
        self._toast_auth.build()

    def cancel_authenticating(self):
        self._auth_intvar.set(0)
        self._auth_strvar.set("Authenticate")

    # ===================================
    #              LIFECYCLE
    # ===================================
    def _on_build(self):
        self._body = tk.Frame(self._master)
        # checkbutton Auth
        checkbutton_auth = tk.Checkbutton(self._body,
                                          name="checkbutton_auth",
                                          textvariable=self._auth_strvar,
                                          variable=self._auth_intvar,
                                          onvalue=1, offvalue=0,
                                          command=self._on_click_checkbutton)
        checkbutton_auth.pack(side=tk.LEFT, anchor="s", ipadx=5)
        # button Publish
        button_publishing = tk.Button(self._body, name="button_publishing", text="Publish",
                                    command=self._on_click_button_publishing)
        button_publishing.pack(side=tk.RIGHT, padx=2, pady=2)

    def _on_display(self):
        pass

    def _on_destroy(self):
        pass

    # =============================
    #           PRIVATE
    # =============================
    def _on_click_checkbutton(self):
        state = self._auth_intvar.get()
        text = self._auth_strvar.get()
        if state == 0:
            self._auth_strvar.set("Authenticate")
            self._auth_intvar.set(0)
            self._main_host.unauth()
        else:
            self._auth_strvar.set("Authenticating...")
            auth_view = AuthView(self._master, self._main_view, self._main_host)
            auth_view.build_wait()

    def _on_click_button_publishing(self):
        if self._main_host.login is None:
            toast = Toast(self._body, message="Please authenticate yourself !")
            toast.build()
            return
        items = self._main_host.get_assets_from_dist_folder()
        if not items:
            message = "Please build an asset first !\nType 'build' in the Manager."
            toast = Toast(self._body, message=message,
                          duration=5000)
            toast.build_wait()
            return
        message = "This is the list of available assets "
        message += "in the folder $TARGET/pyrustic_data/dist"
        choice = Choice(self._body,
                        items=items,
                        title="Asset selection",
                        header="Select an asset",
                        message=message,
                        is_long_message=True,
                        use_scrollbox=True,
                        flavor="radio")
        choice.build_wait()
        asset_version = choice.selected
        if not asset_version:
            return
        asset_version = asset_version[1]
        publishing_view = PublishingView(self._body,
                                         self._main_view,
                                         self._main_host,
                                         asset_version)
        publishing_view.build()

    def _get_scrollbox_config(self):
        data = { "scrollbox":
                    {"canvas":
                         {"width": 100}}}
        return data
