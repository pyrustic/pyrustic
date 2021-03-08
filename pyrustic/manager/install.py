import os
import os.path
import pkgutil
from pyrustic.jasonix import Jasonix
from pyrustic.manager import constant


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
               constant.MANAGER_CACHE_FOLDER,
               constant.RUNTEST_SHARED_FOLDER,
               constant.RUNTEST_CACHE_FOLDER,
               constant.SQLEDITOR_SHARED_FOLDER,
               constant.SQLEDITOR_CACHE_FOLDER,
               constant.HUB_SHARED_FOLDER,
               constant.HUB_CACHE_FOLDER)
    for path in folders:
        if not _make_folder(path):
            return False
    return True


def add_default_shared_data_files():
    resource_prefix = "manager/default_json/PyrusticData/"
    data = (("manager_default.json", constant.MANAGER_SHARED_DATA_FILE),
            ("jupitest_default.json", constant.RUNTEST_SHARED_DATA_FILE),
            ("rustiql_default.json", constant.SQLEDITOR_SHARED_DATA_FILE),
            ("hubway_default.json", constant.HUB_SHARED_DATA_FILE))
    for json_name, path in data:
        data = pkgutil.get_data("pyrustic",
                                resource_prefix + json_name)
        if os.path.exists(path):
            return True
        try:
            Jasonix(path, default=data)
        except Exception as e:
            print("Failed to initialize {}".format(json_name))
            print(e)
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
