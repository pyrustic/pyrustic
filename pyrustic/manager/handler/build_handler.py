import os
import os.path
from jayson import Jayson
from pyrustic import manager


class BuildHandler:
    """
    Description
    -----------
    Use this command to build a distribution package
    that could be published later with the 'publish'
    command.
    The distribution package is a Wheel.

    Usage
    -----
    - Description: Build
    - Command: build

    Hooking
    -------
    This command will run hooks if they exist.
    The legal hooks are:
    - pre_building_hook.py
    - post_building_hook.py
    """

    def __init__(self, target, app_pkg, *args):
        self._target = target
        self._app_pkg = app_pkg
        self._version = None
        self._pre_building_hook = None
        self._post_building_hook = None
        self._process(target, app_pkg)

    def _process(self, target, app_pkg):
        if target is None:
            print("Please link a Target first. Check 'help target'.")
            return
        if not os.path.exists(os.path.join(target, "setup.py")):
            print("Please initialize this project first. Check 'help init'.")
            return
        if not self._run_tests():
            return
        version = self._ensure_version()
        try:
            manager.build(target, app_pkg)
        except manager.BuildError:
            print("Failed to build a distribution package")
        except manager.AnteBuildHookError:
            print("Error while running the pre-building hook")
        except manager.PostBuildHookError:
            print("Error while running the post-building hook")
        else:
            print("Successfully built '{}' v{} !".format(app_pkg, version))

    def _run_tests(self):
        if not manager.ask_for_confirmation("Do you want to run tests ?",
                                     "n"):
            print("")
            return True
        print("")
        print("Running tests...")
        test_success, test_result = manager.run_tests(self._target)
        if test_success is None:
            return True
        if test_success:
            print("Testing passed\n")
            return True
        else:
            print("Testing failed")
            print("")
            print(test_result)
            return False

    def _ensure_version(self):
        cur_version = manager.get_version(self._target)
        cache = os.path.join(self._target, self._app_pkg,
                             "pyrustic_data", "build_report.json")
        if not os.path.exists(cache):
            return cur_version
        jasonix = Jayson(cache, readonly=True)
        latest_build_ver = jasonix.data["app_version"]
        version = cur_version
        if latest_build_ver == cur_version:
            print("Current version: {}".format(cur_version))
            print("Type 'maj', 'min' or 'rev' for a fast version increment.")
            print("Ignore it to make an implicit 'rev' increment.")
            new_version = input("Submit a new version: ")
            print("")
            if not new_version:
                new_version = "rev"
            version = manager.interpret_version(cur_version, new_version)
            manager.set_version(self._target, version)
        return version
