from pyrustic.manager import constant
from pyrustic.jasonix import Jasonix
import os.path


class RecentHandler:
    """
    Description
    -----------
    Display the recent Targets.
    The command "relink" links again Pyrustic Manager with the
    Target at index 0 from the "recent" list.

    Usage
    -----
    - Description: List of recent Targets
    - Command: recent
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
        recent_list = jasonix.data["recent"]
        len_recent_list = len(recent_list)
        if len_recent_list == 0:
            print("- Empty -")
        for i, path in enumerate(reversed(recent_list)):
            print("#{}".format(i))
            print("Name: {}".format(os.path.basename(path)))
            print("Path: {}".format(path))
            if i < len_recent_list - 1:
                print("")
