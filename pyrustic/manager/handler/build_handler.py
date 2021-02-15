import sys
import subprocess
import os
import os.path
from pyrustic.manager.misc.lite_test_runner import LiteTestRunner


class BuildHandler:
    """
    Description
    -----------
    Use this command to build a distribution package
    that could be published later with Hub.
    This command will block the Pyrustic Manager.
    The distribution package is a Wheel.

    Usage
    -----
    - Description: Build
    - Command: build
    """
    def __init__(self, target, app_pkg):
        self._target = target
        self._app_pkg = app_pkg
        self._process(target, app_pkg)

    def _process(self, target, app_pkg):
        if target is None:
            print("Please link a Target first. Check 'help target'.")
            return
        if not app_pkg:
            print("Please initialize this project first. Check 'help init'.")
            return
        # get confirmation
        message = "You are going to build '{}'.".format(app_pkg)
        print(message)
        # tests
        if not self._run_tests():
            return
        # build
        print("\nBuilding...\n")
        if sys.executable:
            args = ["setup.py", "sdist", "bdist_wheel"]
            p = subprocess.Popen([sys.executable, *args], cwd=target)
            p.communicate()
            code = p.returncode
            if code == 0:
                print("\nSuccessfully built !")
                return
            print("\nFailed to built the project.\nReturn code: {}".format(code))

    def _run_tests(self):
        if not self._ask_for_confirmation("Do you want to run tests first ?"):
            print("Cancelled")
            return True
        print("Running tests...")
        test_exist, test_success, test_result = self._test_runner()
        if not test_exist:
            print("There aren't Tests")
            return True
        if test_success:
            print("Testing passed")
            return True
        else:
            print("Testing failed")
            print(test_result)
            return False

    def _test_runner(self):
        test_path = os.path.join(self._target, "tests")
        test_success = True
        test_result = None
        test_exist = False
        if os.path.exists(test_path):
            test_exist = True
            test_host = LiteTestRunner(test_path, self._target)
            test_success, test_result = test_host.run()
        return test_exist, test_success, test_result

    def _ask_for_confirmation(self, message):
        cache = input("{} (y/N): ".format(message))
        if cache.lower() == "y":
            return True
        return False
