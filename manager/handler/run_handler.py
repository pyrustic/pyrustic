import sys
import subprocess
import os.path


class RunHandler:
    """
    Description
    -----------
    Use this command to run a module located in the Target.
    Only dotted name of a module is allowed, so please ignore
    the extension ".py".
    Running a module blocks Pyrustic Manager.

    Usage
    -----
    - Description: Run a module
    - Command: run <the.module.name>

    - Description: Run the Target
    - Command: run
    - Note: The Manager will implicitly execute __main__.py

    - Description: Run a module with some arguments
    - Command: run <the.module.name> <argument_1> <argument_2>

    Example
    -------
    - Description: Run the module
    - Preliminary: Assume that "my_view.py" is in the "view" package
    - Command: run view.my_view

    - Description: Run the module with arguments
    - Preliminary: Assume that "my_view.py" is in the "view" package
    - Command: run view.my_view argument_1 "argument 2"

    Note: Please use simple or double quotes as delimiters if a string
    contains space
    """
    def __init__(self, target, args):
        self._process(target, args)

    def _process(self, target, args):
        if not target:
            self._print_catalog("missing_target")
            return
        name = None
        if len(args) == 0:
            if os.path.exists(os.path.join(target, "__main__.py")):
                args = ["__main__.py"]
                name = "__main__"
            else:
                print("  Missing entry point")
        else:
            args = ["-m", *args]
            name = " ".join(args)
        if not args:
            return
        if sys.executable:
            self._print_catalog("running", module=name)
            p = subprocess.Popen([sys.executable, *args], cwd=target)
            p.communicate()

    def _print_catalog(self, item, **kwargs):
        message = ""
        if item == "missing_target":
            message = "  Please link a Target first. Check 'help target'."
        elif item == "running":
            message = "  Running '{}' ...".format(kwargs["module"])
        print(message)
