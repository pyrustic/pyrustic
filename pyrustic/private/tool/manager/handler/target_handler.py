import os.path
from pyrustic.jasonix import Jasonix


class TargetHandler:
    """
    Description
    -----------
    Use this command to check the currently linked Target.

    Usage
    -----
    - Description: Check the currently linked Target
    - Command: target

    Note: This command also shows the version of the
    Pyrustic Framework that powers your project if
    the data is available.
    """
    def __init__(self, target, args):
        self._target = target
        self._process(target, args)

    @property
    def target(self):
        return self._target

    def _process(self, target, args):
        if not target:
            print("Please link a Target first. Check 'help target'.")
            return
        # args are present: invalid command
        if args:
            print("Wrong usage of this command")
            return
        # target version
        cache = os.path.join(self._target, "pyrustic_data", "about.json")
        target_version = None
        if os.path.exists(cache):
            jasonix = Jasonix(cache)
            target_version = jasonix.data.get("version", None)
        # target framework version
        target_framework_version = None
        cache = os.path.join(self._target, "pyrustic", "about.json")
        if os.path.exists(cache):
            jasonix = Jasonix(cache)
            target_framework_version = jasonix.data.get("version", None)
        # print results
        print("Target: {}".format(self._target))
        if target_version:
            print("Target version: {}".format(target_version))
        if target_framework_version:
            print("Framework version: {}".format(target_framework_version))
