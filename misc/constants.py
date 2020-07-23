import about
import os.path


# constants
DB_PATH = os.path.join(about.ROOT_DIR, "cache", "manager", "db")
CREATIONAL_SCRIPT = "CREATE TABLE path (id INTEGER NOT NULL PRIMARY KEY, val TEXT NOT NULL)"
RELEASE_DATE = "July 20, 2020"
VERSION = "0.0.2"
PYRUSTIC_PROJECT_STRUCT = ["pyrustic", "tests", "cache", "main.py", "about.py"]
PYRUSTIC_PROJECT_OPTIONAL_STRUCT = ["dao", "host", "view", "misc", "script.py", "config.ini"]
