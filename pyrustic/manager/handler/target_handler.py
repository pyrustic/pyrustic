from pyrustic import manager
from pyrustic.manager.core import funcs


class TargetHandler:
    """
    Description
    -----------
    Use this command to check the currently linked Target.

    Usage
    -----
    - Description: Check the currently linked Target
    - Command: target

    Note: This command also shows additional useful
    information about the Target.
    """
    def __init__(self, target,
                 app_pkg, *args):
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
        # no arg
        if not args:
            self._show_current_version()
        # set a new version
        elif len(args) == 1:
            self._change_current_version(args[0])
        # wrong usage of this command
        else:
            print("Wrong usage of this command")

    def _show_current_version(self):
        data = funcs.check_project_state(self._target)
        print("[{}] {}".format(self._app_pkg,
                               self._target))
        print("Version: {}".format(manager.get_version(self._target)))
        if data == 1:
            print("")
            print("Not yet initialized project (check 'help init')")
        #elif data == 2:
        #    print("Not yet installed project (think about: 'pip install -e .')")

    def _change_current_version(self, new_version):
        pass
