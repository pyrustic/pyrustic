import tkinter as tk
from pyrustic.view import CustomView

"""
GUIDE to make your own widget (megawidget to be precise)
========================================================

1- subclass one of the classes:
    - pyrustic.widget.Frame
    - pyrustic.widget.Toplevel
    
2- use the method 'build' at the end of your __init__

3- be sure to use double underscores on your private attributes

4- make sure to don't clash methods names with tk native methods:
    - check pyrustic/private/tk_frame_public_and_protected_attributes.txt
    - check pyrustic/private/tk_toplevel_public_and_protected_attributes.txt
"""
class Frame(tk.Frame):

    def __init__(self, master, class_, cnf,
                 on_build, on_display, on_destroy):
        super().__init__(master=master,
                         class_=class_,
                         cnf=cnf)
        self.__built = False
        self.__on_build = on_build
        self.__on_display = on_display
        self.__on_destroy = on_destroy
        self.__view = None

    def build(self):
        if self.__built:
            return
        self.__view = CustomView(body=self,
                                 on_build=self.__on_build,
                                 on_display=self.__on_display,
                                 on_destroy=self.__on_destroy)
        self.__view.build()
        self.__built = True
        return self.__view


class Toplevel(tk.Toplevel):

    def __init__(self, master, class_, cnf,
                 on_build, on_display, on_destroy,
                 toplevel_geometry):
        super().__init__(master=master,
                         class_=class_,
                         cnf=cnf)
        self.__built = False
        self.__on_build = on_build
        self.__on_display = on_display
        self.__on_destroy = on_destroy
        self.__toplevel_geometry = toplevel_geometry
        self.__view = None

    def build(self):
        if self.__built:
            return
        self.__view = CustomView(body=self,
                          on_build=self.__on_build,
                          on_display=self.__on_display,
                          on_destroy=self.__on_destroy,
                          toplevel_geometry=self.__toplevel_geometry)
        self.__view.build()
        self.__built = True
        return self.__view
