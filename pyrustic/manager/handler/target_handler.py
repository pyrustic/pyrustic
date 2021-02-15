import os.path
from pyrustic import dist
from pyrustic.manager.misc import funcs


class TargetHandler:
    """
    Description
    -----------
    Use this command to check the currently linked Target.

    Usage
    -----
    - Description: Check the currently linked Target
    - Command: target

    Note: This command also shows the version of your project
    if the data is available.
    """
    def __init__(self, target,
                 app_pkg,
                 args):
        self._target = target
        self._app_pkg = app_pkg
        self._process(target, app_pkg, args)

    @property
    def target(self):
        return self._target

    def _process(self, target, app_pkg, args):
        if not target:
            print("None")
            return
        # args are present: invalid command
        if args:
            print("Wrong usage of this command")
            return
        #
        data = funcs.check_project_state(target)
        print("[{}] {}".format(os.path.basename(target), self._target))
        if data == 0:
            print("Version: {}".format(dist(app_pkg)["version"]))
        elif data == 1:
            print("Not yet initialized project (check 'help init')")
        elif data == 2:
            print("Not yet installed project (think about: 'pip install -e .')")
