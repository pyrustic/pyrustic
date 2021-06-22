import os
import os.path
import tkinter as tk
from tkinter import filedialog
from pyrustic import manager
from pyrustic.manager.core import funcs


class LinkHandler:
    """
    Description
    -----------
    Link your Target project to the Project Manager.

    Usage
    -----
    - Description: Open the directory chooser
    - Command: link

    - Description: Link a Target
    - Command: link </path/to/target/project>

    """
    def __init__(self, target, app_pkg, *args):
        self._target = target
        self._app_pkg = app_pkg
        self._process(args)

    @property
    def target(self):
        return self._target

    def _process(self, args):
        path = None
        # no args, so open the folder chooser
        if not args:
            path = self._open_folder_chooser()
        # more than 1 arg isn't allowed
        elif len(args) > 1:
            print("Wrong usage of this command")
            return
        # 1 arg submitted: the path
        else:
            path = args[0]
        # invalid path
        if not self._check_path(path):
            return
        # linking
        path = os.path.abspath(path)
        self._link_to(path)

    def _open_folder_chooser(self):
        #initialdir = os.getcwd()
        initialdir = os.path.expanduser("~")
        root = tk.Tk()
        root.withdraw()
        path = filedialog.askdirectory(initialdir=initialdir,
                                            title="Select your project")
        root.destroy()
        if not isinstance(path, str) or not path:
            return
        return path

    def _check_path(self, path):
        """ Returns True if the path is valid, else False """
        if not path:
            print("You haven't submitted a path")
            return False
        if not os.path.exists(path):
            print("This path doesn't exist")
            return False
        return True

    def _link_to(self, path):
        manager.link(path)
        self._target = path
        print("Successfully linked !")
        app_pkg = os.path.basename(path)
        print("[{}] {}".format(app_pkg, path))
        data = funcs.check_project_state(path)
        if data == 1:
            print("")
            print("Not yet initialized project (check 'help init')")
