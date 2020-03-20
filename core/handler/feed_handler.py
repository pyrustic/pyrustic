import os
import os.path
import shutil
import about
from core.misc import funcs

class FeedHandler:
    """
    - Feed the Platform with a new release
        feed <path_to_new_release_archive.zip>

    Example:
        - Feed the Platform with the 3.0.1 version
            feed /home/user/documents/pyrustic_3.0.1_build_567.zip

        Note: Please use simple or double quotes if your path string contains space
    """
    def __init__(self, target, arg):
        self._root = about.ROOT_DIR
        self._target = target
        self._basename_without_extension = ""
        self._path_to_zip = None
        self._process(arg)

    def _process(self, arg):
        if len(arg) == 0:
            print("Incomplete command. Please check 'help feed'")
            return
        if len(arg) > 1:
            print("Incorrect command. Please check 'help feed'")
            return
        arg = arg[0]

        self._path_to_zip = os.path.abspath(arg)
        if os.path.isfile(self._path_to_zip):
            self._feed_platform()
            return
        print("Failed: argument should be a string 'target' or path to zip file")

    def _feed_platform(self):
        # check if zip name is correct
        version, build = funcs.get_version_build_from_release(self._path_to_zip)
        if not version:
            print("Invalid zip name. Should be named as 'pyrustic_<version>_build_<build>.zip'")
            return
        # check if this version already exists in 'archive' folder
        archive_path = os.path.join(self._root, "archive")
        basename = os.path.basename(self._path_to_zip)
        for item in os.listdir(archive_path):
            if basename == item:
                print("This version already exists")
                return
        # is this the highest build
        is_highest_build = self._is_highest_build(build)
        if not is_highest_build:
            print("This is not a new version. It will be archived but not installed")
        else:
            print("This is a new version. It will be archived then installed")
        # copy zip to archive
        shutil.copy2(self._path_to_zip, archive_path)
        print("Archived")
        if not is_highest_build:
            print("Done !")
            return
        if not funcs.backup_current_version(self._root):
            print("Failed to backup current version")
            return
        print("Backup of current version done. Location:",
                  os.path.join(self._root, "cache", "rollback"))
        if not funcs.install_version(self._root, os.path.join(self._root, "archive", basename)):
            print("Failed to install the version", version, "build", build)
            return
        print("Successfully installed version", version, "build", build, "!")
        print("Shell is going to exit. Please restart to enjoy the new version")
        exit(1)

    def _is_highest_build(self, build):
        for item in os.listdir(os.path.join(self._root, "archive")):
            splitted = item.split("_")
            if len(splitted) == 4:
                if splitted[3] > build:
                    return False
        return True
