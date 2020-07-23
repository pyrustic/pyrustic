import sys
import subprocess
import about


class DbaseHandler:
    """
    Description
    -----------
    Use this command to launch the database editor tool.
    This command won't block the Pyrustic Manager.

    Usage
    -----
    - Description: Launch the database editor tool
    - Command: dbase
    """
    def __init__(self, target):
        self._target = target
        self._popen_instance = None
        self._process(target)

    @property
    def popen_instance(self):
        return self._popen_instance

    def _process(self, target):
        if target is None:
            self._print_catalog("missing_target")
            return
        if sys.executable:
            self._print_catalog("launching")
            p = subprocess.Popen([sys.executable, "-m", "tool.sqluna.main", target],
                             cwd=about.ROOT_DIR)
            self._popen_instance = p
            self._print_catalog("opened")
        else:
            self._print_catalog("python_unavailable")

    def _print_catalog(self, item, **kwargs):
        message = ""
        if item == "missing_target":
            message = "Please link a Target first. Check 'help target'."
        elif item == "python_unavailable":
            message = "Impossible to launch the database editor. Python interpreter is not available."
        elif item == "launching":
            message = "Launching the database editor..."
        elif item == "opened":
            message = "Database editor is running !"
        print(message)
