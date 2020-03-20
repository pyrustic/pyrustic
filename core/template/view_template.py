data ="""
import tkinter as tk
import about
import pyrustic.widget as pw
from pyrustic.abstract.viewable import Viewable
from pyrustic.widget.choice import Choice
from pyrustic.widget.dialog import Dialog
from pyrustic.widget.scrollbox import Scrollbox
from pyrustic.widget.table import Table
from pyrustic.widget.toast import Toast


class {}(Viewable):

    def __init__(self):
        pass

    def _on_start(self):
        self._body = tk.Frame()

    def _on_build(self):
        var = "View " + str(self.__class__) + " displayed !"  # delete me
        tk.Label(self._body, text=var).pack()  # delete me
        return self._body

    def _on_display(self):
        Toast(message="Hello Friend !").show()  # delete me
        pass

    def _on_map(self, event):
        pass

    def _on_unmap(self, event):
        pass

    def _on_close(self, **kwargs):
        pass

"""
