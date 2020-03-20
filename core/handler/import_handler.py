import os.path
import shutil
from core.misc import funcs


class ImportHandler:
    """
    Description
    -----------
    Import a file into the targeted project

    Usage
    -----
    -> import <dest_package_name> <src_path_to_file>
    Import a file into the targeted project

    Note: Destination isn't necessarily a strict package with __init__.py inside, but destination must already exists

    Example
    -------
    Assume you want to import "/home/user/my_file.txt" into the project root
    -> import . /home/user/my_file.txt
    Importing

    Assume you want to import "/home/user/my file.txt" into dao.client.okay
    -> import dao.client.okay "/home/user/my file.txt"
    Importing

    Note: Please use simple or double quotes if your path string contains space
    """

    def __init__(self, target, arg):
        self._target = target
        self._process(arg)

    def _process(self, arg):
        if not self._target:
            print("Impossible to continue. Set a Target first")
            return
        if not arg:
            print("Incomplete command. Please check 'help import'")
            return
        if len(arg) != 2:
            print("Incorrect command. Please check 'help import'")
            return
        self._src, self._dest = self._verif_src_dest(arg[1], arg[0])
        # === Correct src and dest
        if self._src and self._dest:
            if self._check_if_file_already_exists_in_dest():
                print("Failed: the file already exists in destination folder")
                return
            result = self._import()
            if result:
                print("File successfully imported !")
            else:
                print("Failed to complete import")
            return
        # === Wrong src and/or dest
        if not self._src:
            print("Failed: you should put as source a file that actually exists")
        if not self._dest:
            print("Failed: this package doesn't exist")

    def _verif_src_dest(self, src, dest):
        if not os.path.isfile(src):
            src = None
        dest = funcs.package_name_to_path(self._target, dest)
        if not os.path.isdir(dest):
            dest = None
        return src, dest

    def _check_if_file_already_exists_in_dest(self):
        basename = os.path.basename(self._src)
        if os.path.isfile(os.path.join(self._dest, basename)):
            return True
        return False

    def _import(self):
        try:
            shutil.copy(self._src, self._dest)
        except Exception as e:
            return False
        return True
