import os
import os.path
from pyrustic import about as pyrustic_about
from pyrustic.private.tool.common import constants
from pyrustic.jasonix import Jasonix


SUITE_PATH = os.path.join(constants.PYRUSTIC_DATA_FOLDER, "suite")
MANAGER_PATH = os.path.join(SUITE_PATH, "manager")
RUNTEST_PATH = os.path.join(SUITE_PATH, "runtest")
SQLEDITOR_PATH = os.path.join(SUITE_PATH, "sqleditor")
HUB_PATH = os.path.join(SUITE_PATH, "hub")


def installation():
    success = True
    failure_message = "Failed to complete the installation"
    success_message = "Successfully completed"
    # Make folders
    if not make_folders():
        success = False
    # Add shared data files
    if success and not add_default_shared_data_files():
        success = False
    # Set root in suite shared data file
    if success and not set_root_in_suite_shared_data_file():
        success = False
    # check success
    if success:
        print(success_message)
    else:
        print(failure_message)


def make_folders():
    folders = (constants.PYRUSTIC_DATA_FOLDER,
               constants.SUITE_SHARED_FOLDER,
               constants.MANAGER_SHARED_FOLDER,
               constants.RUNTEST_SHARED_FOLDER,
               constants.SQLEDITOR_SHARED_FOLDER,
               constants.HUB_SHARED_FOLDER,
               constants.MANAGER_CACHE_FOLDER,
               constants.RUNTEST_CACHE_FOLDER,
               constants.SQLEDITOR_CACHE_FOLDER,
               constants.HUB_CACHE_FOLDER)
    for path in folders:
        if not _make_folder(path):
            return False
    return True


def add_default_shared_data_files():
    files = (("suite", constants.SUITE_SHARED_DATA_FILE,
              constants.DEFAULT_SUITE_SHARED_DATA_FILE),
             ("manager", constants.MANAGER_SHARED_DATA_FILE,
              constants.DEFAULT_MANAGER_SHARED_DATA_FILE),
             ("runtest", constants.RUNTEST_SHARED_DATA_FILE,
              constants.DEFAULT_RUNTEST_SHARED_DATA_FILE),
             ("sqleditor", constants.SQLEDITOR_SHARED_DATA_FILE,
              constants.DEFAULT_SQLEDITOR_SHARED_DATA_FILE),
             ("hub", constants.HUB_SHARED_DATA_FILE,
              constants.DEFAULT_HUB_SHARED_DATA_FILE))
    for element, file, default_file in files:
        try:
            Jasonix(file, default=default_file)
        except Exception as e:
            print("Failed to create '{}' shared data file".format(element))
            return False
    return True


def set_root_in_suite_shared_data_file():
    try:
        jasonix = Jasonix(constants.SUITE_SHARED_DATA_FILE)
        jasonix.data["root"] = pyrustic_about.ROOT_DIR
        jasonix.data["version"] = pyrustic_about.VERSION
        jasonix.save()
    except Exception as e:
        print("Failed to set root in suite shared data file")
        print(e)
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
    installation()
