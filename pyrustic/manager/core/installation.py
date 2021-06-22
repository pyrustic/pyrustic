import os
import os.path
import pkgutil
from jayson import Jayson
from pyrustic.manager.constant import SHARED_PYRUSTIC_DATA, MANAGER_SHARED_DATA_FILE


def install():
    # mkdir $HOME/PyrusticData/manager
    _make_shared_dir()
    # add default shared data
    _add_default_shared_data()


def _make_shared_dir():
    path = os.path.join(SHARED_PYRUSTIC_DATA, "manager")
    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except Exception as e:
            msg = ("Failed to create the",
                   "shared PyrusticData/manager",
                   "directory inside $HOME")
            raise Error(" ".join(msg))


def _add_default_shared_data():
    resource_prefix = "default_json/PyrusticData"
    resource_json = "manager_shared_data_default.json"
    resource = "/".join((resource_prefix, resource_json))
    data = pkgutil.get_data("pyrustic.manager", resource)
    path = os.path.join(SHARED_PYRUSTIC_DATA, "manager",
                        "manager_shared_data.json")
    try:
        Jayson(MANAGER_SHARED_DATA_FILE, default=data)
    except Exception as e:
        raise Error("Failed to initialize 'manager_shared_data.json'")


class Error(Exception):
    def __init__(self, *args, **kwargs):
        self.message = args[0] if args else ""
        super().__init__(self.message)

    def __str__(self):
        return self.message
