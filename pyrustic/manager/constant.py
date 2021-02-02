import os.path
from pyrustic import about as pyrustic_about


# general constants
USER_AGENT = ("User-Agent", "Pyrustic")
PYRUSTIC_DATA = "PyrusticData"
PYRUSTIC_DATA_FOLDER = os.path.join(os.path.expanduser("~"),
                                  PYRUSTIC_DATA)


# manager constants
MANAGER_SHARED_FOLDER = os.path.join(PYRUSTIC_DATA_FOLDER, "manager")

MANAGER_CACHE_FOLDER = os.path.join(MANAGER_SHARED_FOLDER, "cache")

MANAGER_SHARED_DATA_FILE = os.path.join(MANAGER_SHARED_FOLDER,
                                        "manager_shared_data.json")

DEFAULT_MANAGER_SHARED_DATA_FILE = os.path.join(pyrustic_about.ROOT_DIR,
                                                "manager",
                                                "default_json",
                                                "PyrusticData",
                                                "manager_default.json")

# sqleditor constants
SQLEDITOR_SHARED_FOLDER = os.path.join(PYRUSTIC_DATA_FOLDER, "rustiql")

SQLEDITOR_CACHE_FOLDER = os.path.join(SQLEDITOR_SHARED_FOLDER, "cache")

SQLEDITOR_SHARED_DATA_FILE = os.path.join(SQLEDITOR_SHARED_FOLDER,
                                          "rustiql_shared_data.json")

DEFAULT_SQLEDITOR_SHARED_DATA_FILE = os.path.join(pyrustic_about.ROOT_DIR,
                                                  "manager",
                                                  "default_json",
                                                  "PyrusticData",
                                                  "rustiql_default.json")

# runtest constants
RUNTEST_SHARED_FOLDER = os.path.join(PYRUSTIC_DATA_FOLDER, "jupitest")

RUNTEST_CACHE_FOLDER = os.path.join(RUNTEST_SHARED_FOLDER, "cache")

RUNTEST_SHARED_DATA_FILE = os.path.join(RUNTEST_SHARED_FOLDER,
                                        "jupitest_shared_data.json")

DEFAULT_RUNTEST_SHARED_DATA_FILE = os.path.join(pyrustic_about.ROOT_DIR,
                                                "manager",
                                                "default_json",
                                                "PyrusticData",
                                                "jupitest_default.json")

# hub constants
HUB_SHARED_FOLDER = os.path.join(PYRUSTIC_DATA_FOLDER, "hubway")

HUB_CACHE_FOLDER = os.path.join(HUB_SHARED_FOLDER, "cache")

HUB_SHARED_DATA_FILE = os.path.join(HUB_SHARED_FOLDER,
                                      "hubway_shared_data.json")

DEFAULT_HUB_SHARED_DATA_FILE = os.path.join(pyrustic_about.ROOT_DIR,
                                            "manager",
                                            "default_json",
                                            "PyrusticData",
                                            "hubway_default.json")
