from pyrustic import manager


class VersionHandler:
    """
    Description
    -----------
    Use this command to check or edit the version of the
    Target project.

    Usage
    -----
    - Description: Check the current version
    - Command: version

    - Description: Set a new version
    - Command: version <sequence>

    - Description: Increment the major number
    - Command: version maj

    - Description: Increment the minor number
    - Command: version min

    - Description: Increment the revision number
    - Command: version rev

    Example
    -------
    - Description: Increment the major number
    - Preliminary: Assume the current version 1.2.3
    - Command: version maj
    - Result: The new version is: 2.0.0

    - Description: Set a version
    - Command: version 2.0.1
    """
    def __init__(self, target, app_pkg, *args):
        self._target = target
        self._app_pkg = app_pkg
        self._version = None
        self._process(args)

    def _process(self, args):
        if not self._target:
            print("You should link a Target first. Check 'help target'.")
            return
        self._version = manager.get_version(self._target)
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
        print("Project version: {}".format(self._version))

    def _change_current_version(self, new_version):
        new_version = manager.interpret_version(self._version, new_version)
        manager.set_version(self._target, new_version)
        print("Previous value : {}".format(self._version))
        print("Project version: {}".format(new_version))
        self._version = new_version
