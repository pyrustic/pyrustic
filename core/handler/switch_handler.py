import os
import os.path
import shutil
import zipfile
import about
from core.misc import funcs

class SwitchHandler:
    """
    Description
    -----------
    Switch to another existing version of the platform
    You can type 'version' to see the list of available versions
    To add a new version, download the zip, then use the command 'feed'

    Usage
    -----
    -> switch <version_or_build>
    Switching

    Example
    -------
    -> switch 3.0.1
    Switch to the highest build of the version 3.0.1

    -> switch 2356
    Switch to the build 2356
    """
    def __init__(self, arg):
        self._root = about.ROOT_DIR
        self._process(arg)

    def _process(self, arg):
        if not arg:
            print("Incomplete command. Please check 'help switch'")
            return
        if len(arg) > 1:
            print("Incorrect command. Please check 'help switch'")
            return
        version = arg[0]
        is_build_number = True
        if "." in version:
            is_build_number = False
        str_version = "build " + version if is_build_number else "version " + version
        path = funcs.path_to_version_or_build(self._root, version)
        if path:
            funcs.backup_current_version(self._root)
            funcs.install_version(self._root, path)
            print("Pyrustic platform switched successfully to", str_version, ".")
            print("Shell is going to exit. Please restart to enjoy this version")
            exit(1)
        else:
            print("This version doesn't exist")
