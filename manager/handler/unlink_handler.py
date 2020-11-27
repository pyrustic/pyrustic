

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

    def __init__(self, target, args):
        self._target = target
        self._process(args)

    @property
    def target(self):
        return self._target

    def _process(self, args):
        # args are present: invalid command
        if args:
            print("  Wrong usage of this command")
            return
        # valid command
        if self._target:
            self._target = None
            print("  Successfully unlinked !")
        print("  Target: {}".format(self._target))
