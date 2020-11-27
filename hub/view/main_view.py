import tkinter as tk
from pyrustic.threadium import Threadium
from pyrustic.viewable import Viewable
from hub.host.main_host import MainHost
from hub.view.header_view import HeaderView
from hub.view.central_view import CentralView
from hub.view.footer_view import FooterView


class MainView(Viewable):
    def __init__(self, app):
        self._app = app
        self._root = app.root
        self._main_host = MainHost()
        self._threadium = Threadium(self._root)
        self._body = None
        self._header_view = None
        self._central_view = None
        self._footer_view = None

    @property
    def root(self):
        return self._root

    @property
    def threadium(self):
        return self._threadium

    @property
    def header_view(self):
        return self._header_view

    @property
    def central_view(self):
        return self._central_view

    @property
    def footer_view(self):
        return self._footer_view

    def _on_build(self):
        self._body = tk.Frame(self._root)
        # header
        self._header_view = HeaderView(self._body, self, self._main_host)
        self._header_view.build_pack(fill=tk.X, pady=(0, 10))
        # central
        self._central_view = CentralView(self._body, self, self._main_host)
        self._central_view.build_pack(expand=1, fill=tk.BOTH, padx=(5, 3))
        # footer
        self._footer_view = FooterView(self._body, self, self._main_host)
        self._footer_view.build_pack(fill=tk.X, pady=(10, 0))

    def _on_display(self):
        pass

    def _on_destroy(self):
        pass
