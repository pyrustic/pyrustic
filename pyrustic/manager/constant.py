import os.path


# == Shared data
# PyrusticData
SHARED_PYRUSTIC_DATA = os.path.join(os.path.expanduser("~"),
                                    "PyrusticData")
# Manager
MANAGER_SHARED_FOLDER = os.path.join(SHARED_PYRUSTIC_DATA, "manager")
MANAGER_SHARED_DATA_FILE = os.path.join(MANAGER_SHARED_FOLDER,
                                        "manager_shared_data.json")
MANAGER_CACHE_FOLDER = os.path.join(MANAGER_SHARED_FOLDER, "cache")














# ============ TODO : delete -->

# sqleditor constants
SQLEDITOR_SHARED_FOLDER = os.path.join(SHARED_PYRUSTIC_DATA, "rustiql")

SQLEDITOR_CACHE_FOLDER = os.path.join(SQLEDITOR_SHARED_FOLDER, "cache")

SQLEDITOR_SHARED_DATA_FILE = os.path.join(SQLEDITOR_SHARED_FOLDER,
                                          "rustiql_shared_data.json")


# runtest constants
RUNTEST_SHARED_FOLDER = os.path.join(SHARED_PYRUSTIC_DATA, "jupitest")

RUNTEST_CACHE_FOLDER = os.path.join(RUNTEST_SHARED_FOLDER, "cache")

RUNTEST_SHARED_DATA_FILE = os.path.join(RUNTEST_SHARED_FOLDER,
                                        "jupitest_shared_data.json")


# hub constants
HUB_SHARED_FOLDER = os.path.join(SHARED_PYRUSTIC_DATA, "hubway")

HUB_CACHE_FOLDER = os.path.join(HUB_SHARED_FOLDER, "cache")

HUB_SHARED_DATA_FILE = os.path.join(HUB_SHARED_FOLDER,
                                      "hubway_shared_data.json")
