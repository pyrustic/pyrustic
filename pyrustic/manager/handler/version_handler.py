from pyrustic import dist


class VersionHandler:
    """
    Description
    -----------
    Use this command to check the version of Pyrustic.

    Usage
    -----
    - Description: Check information
    - Command: version
    """
    def __init__(self):
        self._process()

    def _process(self):
        print("Pyrustic Manager")
        print("Version: {}".format(dist("pyrustic")["version"]))
