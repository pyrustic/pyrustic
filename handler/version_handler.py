import about
from misc import funcs


class VersionHandler:
    """
    Description
    -----------
    Use this command to check the version of the Pyrustic Manager.
    This command also displays the location of Pyrustic Manager.

    Usage
    -----
    - Description: Check information
    - Command: version
    """
    def __init__(self):
        self._process()

    def _process(self):
        version = funcs.get_target_version(about.ROOT_DIR)
        print("Pyrustic Manager: {}\nVersion: {}".format(about.ROOT_DIR, version))
