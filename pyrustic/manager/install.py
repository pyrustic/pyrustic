import os
import os.path
from pyrustic.manager import constant
from pyrustic.jasonix import Jasonix


def main():
    set_environment()


def set_environment():
    success = True
    # Make folders
    if not make_folders():
        success = False
    # Add shared data files
    if success and not add_default_shared_data_files():
        success = False
    # check success
    if success:
        return True
    else:
        return False


def make_folders():
    folders = (constant.PYRUSTIC_DATA_FOLDER,
               constant.MANAGER_SHARED_FOLDER,
               constant.RUNTEST_SHARED_FOLDER,
               constant.SQLEDITOR_SHARED_FOLDER,
               constant.HUB_SHARED_FOLDER,
               constant.MANAGER_CACHE_FOLDER,
               constant.RUNTEST_CACHE_FOLDER,
               constant.SQLEDITOR_CACHE_FOLDER,
               constant.HUB_CACHE_FOLDER)
    for path in folders:
        if not _make_folder(path):
            return False
    return True


def add_default_shared_data_files():
    files = (("manager", constant.MANAGER_SHARED_DATA_FILE,
              constant.DEFAULT_MANAGER_SHARED_DATA_FILE),
             ("jupitest", constant.RUNTEST_SHARED_DATA_FILE,
              constant.DEFAULT_RUNTEST_SHARED_DATA_FILE),
             ("rustiql", constant.SQLEDITOR_SHARED_DATA_FILE,
              constant.DEFAULT_SQLEDITOR_SHARED_DATA_FILE),
             ("hubway", constant.HUB_SHARED_DATA_FILE,
              constant.DEFAULT_HUB_SHARED_DATA_FILE))
    for element, file, default_file in files:
        try:
            Jasonix(file, default=default_file)
        except Exception as e:
            print("Failed to create '{}' shared data file".format(element))
            return False
    return True


def _make_folder(path):
    if not os.path.exists(path):
        try:
            os.mkdir(path)
        except Exception as e:
            print("Failed to make directory '{}'".format(path))
            print(e)
            return False
    return True


if __name__ == "__main__":
    main()
