import about
from manager.misc import funcs


class VersionHandler:
    """
    Description
    -----------
    Use this command to check the version of the Pyrustic Suite.
    This command also displays the location of Pyrustic Suite.

    Usage
    -----
    - Description: Check information
    - Command: version
    """
    def __init__(self):
        self._process()

    def _process(self):
        print("  Pyrustic Suite: {}\n  Version: {}".format(about.ROOT_DIR,
                                                         about.VERSION))
