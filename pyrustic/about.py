"""
WARNING ! DON'T EDIT THIS FILE ! OTHERWISE YOU WILL LOSE YOUR SOUL !
Instead, edit the file "about.json" in the folder "pyrustic_data"

Are available:

    - ROOT_DIR        str     example: "/path/to/my/project"
    - PROJECT_NAME    str     example: "project"
    - PROJECT_TITLE   str     example: "Project"
    - VERSION         str     example: "0.0.1"
    - AUTHOR          str     example: "John Jr. Doe"
    - EMAIL           str     example: "homo@sapiens.earth"
    - DEV_MODE        bool    example: True

"""


import os.path
from pyrustic.jasonix import Jasonix


def _get_data():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    about_json_path = os.path.join(root_dir, "pyrustic_data", "about.json")
    project_name = os.path.basename(root_dir)
    project_title = project_name.capitalize()
    dev_mode = True
    author = ""
    email = ""
    version = "0.0.1"
    if os.path.exists(about_json_path):
        jasonix = Jasonix(about_json_path, readonly=True)
        project_name = jasonix.data.get("project_name", project_name)
        project_title = jasonix.data.get("project_title", project_title)
        version = jasonix.data.get("version", version)
        author = jasonix.data.get("author", author)
        email = jasonix.data.get("email", email)
        dev_mode = jasonix.data.get("dev_mode", dev_mode)
    return {"root_dir": root_dir,
            "project_name": project_name,
            "project_title": project_title,
            "version": version,
            "author": author,
            "email": email,
            "dev_mode": dev_mode}


_data = _get_data()

ROOT_DIR = _data["root_dir"]
PROJECT_NAME = _data["project_name"]
PROJECT_TITLE = _data["project_title"]
VERSION = _data["version"]
AUTHOR = _data["author"]
DEV_MODE = _data["dev_mode"]
