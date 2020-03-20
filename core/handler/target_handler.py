import os.path
import os
import about
from core.misc import funcs

class TargetHandler:
    """
    Description
    -----------
    Use this command to check the current target or to set a new target

    Usage
    -----
    -> target <path_to_target_folder>
    Set a Target

    -> target
    Check current Target (path and framework's version)

    Example
    -------
    Assume 'my_project' lives at '/home/user/projects'
    -> target /home/user/projects
    Target 'my_project'

    Assume 'my_project' lives at '/home/user/secret projects'
    -> target "/home/user/secret projects"
    Target 'my_project'

    Note: Please use simple or double quotes if your path string contains space
    """
    def __init__(self, target, arg):
        self._target = target
        self._root = about.ROOT_DIR
        self._process(arg)

    @property
    def target(self):
        return self._target

    def _process(self, arg):
        if len(arg) > 1:
            print("Incomplete command. Please check 'help target'")
            return
        arg = None if len(arg) == 0 else arg[0]
        # === Command: check current Target
        if not arg:
            print(self._target)
            if self._target:
                self._current_version()
            return
        # === Command: set a Target
        arg = os.path.abspath(arg)
        if self._is_valid_pyrustic_project(arg):
            self._target = arg
            print("Valid Target")
            print(self._target)
            print("Done !")
        else:
            print("Failed: the path submitted isn't a valid Pyrustic project")

    def _is_valid_pyrustic_project(self, arg):
        if not os.path.isdir(arg):
            return False
        content_project_dir = os.listdir(arg)
        content_payload_dir = os.listdir(os.path.join(self._root, "core", "payload"))
        skip_these_items = ("__pycache__", "__init__.py")
        for item in content_payload_dir:
            if item in skip_these_items:
                continue
            if not item in content_project_dir:
                return False
        return True

    def _current_version(self):
        if not self._target:
            return
        for item in os.listdir(os.path.join(self._target, "pyrustic")):
            if item.startswith("pyrustic_"):
                splitted = item.split("_")
                if len(splitted) == 4 and splitted[2] == "build":
                    print("Target running on Pyrustic version ", splitted[1], " build ", splitted[3])
                    return
