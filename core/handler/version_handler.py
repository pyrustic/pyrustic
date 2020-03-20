import os
import os.path
import about
from core.misc import funcs

class VersionHandler:
    """
    Description
    -----------
    Check current Pyrustic platform version and list offline versions available

    Usage
    -----
    -> version
    Checking
    """

    def __init__(self, arg):
        self._root = about.ROOT_DIR
        self._process(arg)

    def _process(self, arg):
        if not arg:
            self._afficher_version()
            return
        print("Incorrect command. Please check 'help version'")

    def _afficher_version(self):
        print("Current version:", about.VERSION, "build", about.BUILD)
        archive_dir = os.path.join(self._root, "archive")
        versions = os.listdir(archive_dir)
        if len(versions) == 0:
            print("No offline version exists")
            return
        print("List of archived versions:")
        for item in versions:
            splitted = item.split("_")
            if len(splitted) == 4:
                print("\tversion", splitted[1], "build", splitted[3])
