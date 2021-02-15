from pyrustic.manager import constant
from pyrustic.jasonix import Jasonix
import os.path


class LastHandler:
    """
    Description
    -----------
    Display the last Targets.
    The command "relink" links again Pyrustic Manager with the
    Target at index 0 from the "last" list.

    Usage
    -----
    - Description: List of last Targets
    - Command: last
    """

    def __init__(self, target,
                 app_pkg, args):
        self._target = target
        self._app_pkg = app_pkg
        self._process(args)

    def _process(self, args):
        if args:
            print("Wrong usage of this command")
            return
        jasonix = Jasonix(constant.MANAGER_SHARED_DATA_FILE)
        last_list = jasonix.data["last"]
        len_last_list = len(last_list)
        if len_last_list == 0:
            print("- Empty -")
        for i, path in enumerate(reversed(last_list)):
            print("#{}".format(i))
            print("Name: {}".format(os.path.basename(path)))
            print("Path: {}".format(path))
            if i < len_last_list - 1:
                print("")
