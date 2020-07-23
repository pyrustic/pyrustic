import sys
import subprocess


class RunHandler:
    """
    Description
    -----------
    Use this command to run a module located in the Target.
    Only dotted name of a module is allowed, so please ignore
    the extension '.py'.
    Running a module blocks Pyrustic Manager till this module terminates.

    Usage
    -----
    - Description: Run a module
    - Command: run <the.module.name>

    - Description: Run the Target
    - Command: run
    - Note: The Manager will implicitly execute the command 'run main'.

    - Description: Run a module with some arguments
    - Command: run <the.module.name> <argument_1> <argument_2>

    Example
    -------
    - Description: Run the module
    - Preliminary: Assume that 'my_view.py' lives in package 'view'
    - Command: run view my_view

    - Description: Run the module with arguments
    - Preliminary: Assume that 'my_view.py' lives in package 'view'
    - Command: run view my_view argument_1 "argument 2"

    Note: Please use simple or double quotes as delimiters if a string
    contains space
    """
    def __init__(self, target, args):
        self._process(target, args)

    def _process(self, target, args):
        if not target:
            self._print_catalog("missing_target")
            return
        if len(args) == 0:
            args = ["main"]
        if sys.executable:
            self._print_catalog("running", module=args[0])
            p = subprocess.Popen([sys.executable, "-m", *args], cwd=target)
            p.communicate()

    def _print_catalog(self, item, **kwargs):
        message = ""
        if item == "missing_target":
            message = "Please link a Target first. Check 'help target'."
        elif item == "running":
            message = "Running '{}' ...".format(kwargs["module"])
        print(message)