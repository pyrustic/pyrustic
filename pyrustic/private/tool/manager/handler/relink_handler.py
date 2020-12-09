from pyrustic.private.tool.common import constants
from pyrustic.jasonix import Jasonix
from pyrustic.private.tool.manager.handler.link_handler import LinkHandler
import os.path


class RelinkHandler:
    """
    Description
    -----------
    Link again the previous Target or one of last Targets.

    Usage
    -----
    - Description: Link again the previous Target
    - Command: relink

    - Description: Link again a previous Target with its index
    - Command: relink <index>

    Example
    -------
    - Description: Link again a previous Target
    - Preliminary: Assume you want to link again the Target
    with index #2 (found the index with the command "last")
    - Command: relink 2
    """
    def __init__(self, target, args):
        self._target = target
        self._process(args)

    @property
    def target(self):
        return self._target

    def _process(self, args):
        jasonix = Jasonix(constants.MANAGER_SHARED_DATA_FILE,
                          constants.DEFAULT_MANAGER_SHARED_DATA_FILE)
        path = jasonix.data["target"]
        if not jasonix.data["last"]:
            print("- Empty -")
            return
        if len(args) == 1:
            try:
                index = int(args[0])
                path = list(reversed(jasonix.data["last"]))[index]
            except Exception as e:
                print("Wrong index")
                return
        elif len(args) > 1:
            print("Wrong usage of this command")
            return
        link_handler = LinkHandler(self._target, [path])
        self._target = link_handler.target

    def _check_path(self, path):
        """ Returns True if the path is valid, else False """
        if not os.path.exists(path):
            print("{}".format(path))
            print("This path doesn't exist")
            return False
        return True
