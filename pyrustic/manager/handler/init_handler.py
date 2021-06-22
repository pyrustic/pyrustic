from pyrustic import manager


class InitHandler:
    """
    Description
    -----------
    Use this command to initialize your project.
    The Project Manager will install a basic
    project structure in the Target.

    Usage
    -----
    - Description: Init your project
    - Command: init
    """
    def __init__(self, target, app_pkg, *args):
        self._target = target
        self._app_pkg = app_pkg
        self._process(args)

    def _process(self, args):
        if not self._target:
            print("You should link a Target first. Check 'help target'.")
            return
        if args:
            print("Wrong usage of this command. Check 'help init'.")
            return
        # ask for app_pkg
        manager.init(self._target, self._app_pkg)
        print("Successfully initialized !")
