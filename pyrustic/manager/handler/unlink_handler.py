

class UnlinkHandler:
    """
    Description
    -----------
    Use this command to unlink the currently linked Target.

    Usage
    -----
    - Description: Unlink the currently linked Target
    - Command: unlink
    """

    def __init__(self, target, app_pkg, args):
        self._target = target
        self._app_pkg = app_pkg
        self._process(args)

    @property
    def target(self):
        return self._target

    @property
    def app_pkg(self):
        return self._app_pkg

    def _process(self, args):
        # args are present: invalid command
        if args:
            print("Wrong usage of this command")
            return
        # valid command
        if self._target:
            self._target = None
            self._app_pkg = None
            print("Successfully unlinked !")
        print("Target: {}".format(self._target))
