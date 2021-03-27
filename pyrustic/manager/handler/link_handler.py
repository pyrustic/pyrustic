import tkinter as tk
from tkinter import filedialog
import os
import os.path
from pyrustic import dist
from pyrustic.manager.misc import funcs


class LinkHandler:
    """
    Description
    -----------
    This will link your Target project to Pyrustic Manager.

    Usage
    -----
    - Description: Open the directory chooser
    - Command: link

    - Description: Link a Target
    - Command: link </path/to/target/project>

    """
    def __init__(self, target, app_pkg, args):
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
        path = os.path.normpath(path)
        self._link_to(path)

    def _open_folder_chooser(self):
        #initialdir = os.path.expanduser("~")
        initialdir = os.getcwd()
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
        if not self._store_target(path):
            print("Failed to store the Target in config")
            return
        self._target = path
        print("Successfully linked !")
        app_pkg = os.path.basename(path)
        print("[{}] {}".format(app_pkg, path))
        data = funcs.check_project_state(path)
        if data == 0:
            print("Version: {}".format(dist(app_pkg)["version"]))
        elif data == 1:
            print("Not yet initialized project (check 'help init')")
        elif data == 2:
            print("Not yet installed project (think about: 'pip install -e .')")

    def _store_target(self, path):
        jasonix = funcs.get_manager_jasonix(False)
        recent_list = jasonix.data["recent"]
        for i, item in enumerate(recent_list):
            if item == path:
                del recent_list[i]
        recent_list.append(path)
        len_recent_list = len(recent_list)
        max_items = 5
        if len_recent_list > max_items:
            for i in range(len_recent_list - max_items):
                del recent_list[0]
        jasonix.data["target"] = path
        jasonix.save()
        return True
