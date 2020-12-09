import os.path
from pyrustic import about as pyrustic_about


# general constants
PYRUSTIC_DATA = "PyrusticData"
PYRUSTIC_DATA_FOLDER = os.path.join(os.path.expanduser("~"),
                                  PYRUSTIC_DATA)
USER_AGENT = ("User-Agent", "Pyrustic")


# suite
SUITE_SHARED_FOLDER = os.path.join(PYRUSTIC_DATA_FOLDER, "suite")
SUITE_SHARED_DATA_FILE = os.path.join(SUITE_SHARED_FOLDER,
                                      "suite_shared_data.json")
DEFAULT_SUITE_SHARED_DATA_FILE = os.path.join(pyrustic_about.ROOT_DIR,
                                              "private",
                                              "tool",
                                              "common",
                                              "default_json_data",
                                              "default_suite_shared_data.json")

# manager constants
MANAGER_SHARED_FOLDER = os.path.join(SUITE_SHARED_FOLDER, "manager")

MANAGER_CACHE_FOLDER = os.path.join(MANAGER_SHARED_FOLDER, "cache")

MANAGER_SHARED_DATA_FILE = os.path.join(MANAGER_SHARED_FOLDER,
                                        "manager_shared_data.json")

DEFAULT_MANAGER_SHARED_DATA_FILE = os.path.join(pyrustic_about.ROOT_DIR,
                                                "private",
                                                "tool",
                                                "common",
                                                "default_json_data",
                                                "default_manager_shared_data.json")

# sqleditor constants
SQLEDITOR_SHARED_FOLDER = os.path.join(SUITE_SHARED_FOLDER, "sqleditor")

SQLEDITOR_CACHE_FOLDER = os.path.join(SQLEDITOR_SHARED_FOLDER, "cache")

SQLEDITOR_SHARED_DATA_FILE = os.path.join(SQLEDITOR_SHARED_FOLDER,
                                          "sqleditor_shared_data.json")

DEFAULT_SQLEDITOR_SHARED_DATA_FILE = os.path.join(pyrustic_about.ROOT_DIR,
                                                  "private",
                                                  "tool",
                                                  "common",
                                                  "default_json_data",
                                                  "default_sqleditor_shared_data.json")

# runtest constants
RUNTEST_SHARED_FOLDER = os.path.join(SUITE_SHARED_FOLDER, "runtest")

RUNTEST_CACHE_FOLDER = os.path.join(RUNTEST_SHARED_FOLDER, "cache")

RUNTEST_SHARED_DATA_FILE = os.path.join(RUNTEST_SHARED_FOLDER,
                                        "runtest_shared_data.json")

DEFAULT_RUNTEST_SHARED_DATA_FILE = os.path.join(pyrustic_about.ROOT_DIR,
                                                "private",
                                                "tool",
                                                "common",
                                                "default_json_data",
                                                "default_runtest_shared_data.json")

# hub constants
HUB_SHARED_FOLDER = os.path.join(SUITE_SHARED_FOLDER, "hub")

HUB_CACHE_FOLDER = os.path.join(HUB_SHARED_FOLDER, "cache")

HUB_SHARED_DATA_FILE = os.path.join(HUB_SHARED_FOLDER,
                                      "hub_shared_data.json")

DEFAULT_HUB_SHARED_DATA_FILE = os.path.join(pyrustic_about.ROOT_DIR,
                                            "private",
                                            "tool",
                                            "common",
                                            "default_json_data",
                                            "default_hub_shared_data.json")
