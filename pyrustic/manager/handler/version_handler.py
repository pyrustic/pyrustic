from pyrustic import about as pyrustic_about


class VersionHandler:
    """
    Description
    -----------
    Use this command to check the version of Pyrustic.
    This command also displays the location of Pyrustic.

    Usage
    -----
    - Description: Check information
    - Command: version
    """
    def __init__(self):
        self._process()

    def _process(self):
        print("Version: {}\nPath: {}".format(pyrustic_about.VERSION,
                                                   pyrustic_about.ROOT_DIR))
