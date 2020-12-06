import os
import os.path
from manager.misc import funcs
import about
import uuid
from pyrustic.jasonix import Jasonix


class SyncHandler:
    """
    Description
    -----------
    This command will synchronize your Target
    with the current Pyrustic Framework that
    powers Pyrustic Suite.

    Note: a backup of the previous Pyrustic Framework
    that powers your Target project will be saved
    into your project's "cache" folder.

    Usage
    -----
    - Description: Synchronize
    - Command: sync
    """
    def __init__(self, target, args):
        self._target = target
        self._synced = False
        self._process(args)

    @property
    def target(self):
        return self._target

    @property
    def synced(self):
        return self._synced

    def _process(self, args):
        if self._target is None:
            print("  Please link a Target first !")
            return
        if args:
            print("Wrong usage of this command")
            return
        print("  This command will edit the content of the Target.")
        data = input("  Do you want to continue ? (y/N): ")
        if data.lower() != "y":
            print("  Cancelled")
            return
        print("  ...")
        if self._cache_target_framework():
            if self._inject_framework_in_target():
                print("  Successfully synced !")
                self._synced = True

    def _cache_target_framework(self):
        if (not os.path.exists(os.path.join(self._target, "pyrustic"))
                 and not os.path.exists(os.path.join(self._target, "about.py"))):
            return True
        cache_path = os.path.join(self._target, "cache", "pyrustic",
                                  "framework_backup", str(uuid.uuid4()))
        # create cache
        if not os.path.exists(cache_path):
            os.makedirs(cache_path)
        cached = self._cache_this("pyrustic", cache_path)
        if cached:
            return True
        return False

    def _inject_framework_in_target(self):
        # inject pyrustic folder
        if not funcs.copyto(os.path.join(about.ROOT_DIR, "pyrustic"),
                            os.path.join(self._target, "pyrustic")):
            return False
        return True

    def _cache_this(self, name, cache_path):
        current_framework_path = os.path.join(self._target, name)
        path_exists = os.path.exists(current_framework_path)
        if not path_exists:
            return True
        return funcs.moveto(current_framework_path,
                            os.path.join(cache_path, name))
