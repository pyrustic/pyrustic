import sys
import subprocess


class TestHandler:
    """
    Description
    -----------
    Use this command to launch the Test Runner.
    This command won't block the Pyrustic Manager.

    Usage
    -----
    - Description: Launch the Test Runner
    - Command: test
    """
    def __init__(self, target, app_pkg):
        self._target = target
        self._app_pkg = app_pkg
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
            p = subprocess.Popen([sys.executable, "-m", "jupitest"], cwd=target)
            self._popen_instance = p
            self._print_catalog("opened")
        else:
            self._print_catalog("python_unavailable")

    def _print_catalog(self, item, **kwargs):
        message = ""
        if item == "missing_target":
            message = "Please link a Target first. Check 'help target'."
        elif item == "python_unavailable":
            message = "Impossible to launch the test runner. Python interpreter is not available."
        elif item == "launching":
            message = "Launching the test runner..."
        elif item == "opened":
            message = "Test runner is running !"
        print(message)
