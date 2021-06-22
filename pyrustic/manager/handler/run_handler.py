import os
import os.path
from pyrustic import manager


class RunHandler:
    """
    Description
    -----------
    Use this command to run a module.
    The module can be located either in the Target or in
    a regular place where Python stores packages.
    Only dotted name of a module is allowed, so please ignore
    the extension ".py".

    Usage
    -----
    - Description: Run a module
    - Command: run <the.module.name>

    - Description: Run the Target
    - Command: run
    Note: Project Manager will implicitly run APP_DIR/__main__.py

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

    - Description: Display the Zen of Python
    - Command: run this

    Note: Please use simple or double quotes as delimiters if a string
    contains space.
    """
    def __init__(self, target, app_pkg, *args):
        self._target = target
        self._app_pkg = app_pkg
        self._process(target, app_pkg, args)

    def _process(self, target, app_pkg, args):
        name = None
        if not args and not target:
            self._print_catalog("missing_target")
            return
        if not args and not os.path.exists(os.path.join(target, app_pkg)):
            print("Please initialize this project first. Check 'help init'.")
            return
        if not args and target:
            args = ["-m", app_pkg]
        else:
            args = ["-m", *args]
        name = " ".join(args)
        self._print_catalog("running", module=name)
        print("")
        manager.run(target, *args)

    def _print_catalog(self, item, **kwargs):
        message = ""
        if item == "missing_target":
            message = "Please link a Target first. Check 'help target'."
        elif item == "running":
            message = "Running '{}' ...".format(kwargs["module"])
        elif item == "missing_app_pkg":
            message = "Please init the project first. Check 'help init'."
        print(message)
