import tkinter as tk
from tkinter import filedialog
import os
import os.path
from pyrustic.private.tool.common import funcs as common_funcs


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
    def __init__(self, target, args):
        self._target = target
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
        if not self._store_target(path):
            print("Failed to store the Target in config")
            return
        print("Successfully linked !\nTarget: {}".format(path))
        self._target = path

    def _store_target(self, path):
        jasonix = common_funcs.get_manager_jasonix(False)
        last_list = jasonix.data["last"]
        for i, item in enumerate(last_list):
            if item == path:
                del last_list[i]
        last_list.append(path)
        len_last_list = len(last_list)
        max_items = 5
        if len_last_list > max_items:
            for i in range(len_last_list - max_items):
                del last_list[0]
        jasonix.data["target"] = path
        jasonix.save()
        return True
