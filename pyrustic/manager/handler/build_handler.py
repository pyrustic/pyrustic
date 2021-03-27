import sys
import time
import subprocess
import os
import os.path
import pkgutil
from pyrustic.jasonix import Jasonix
from pyrustic.manager.misc.lite_test_runner import LiteTestRunner
from pyrustic.manager.misc.funcs import setup_config, wheels_assets


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
        self._version = None
        self._pre_building_hook = None
        self._post_building_hook = None
        self._process(target, app_pkg)

    def _process(self, target, app_pkg):
        if target is None:
            print("Please link a Target first. Check 'help target'.")
            return
        if not app_pkg:
            print("Please initialize this project first. Check 'help init'.")
            return
        # version
        self._version = self._get_version()
        # get confirmation
        message = "You are going to build '{}' v{}.".format(app_pkg,
                                                        self._version)
        print(message)
        if not self._ask_for_confirmation("\nDo you want to continue ?"):
            return
        print("")
        # tests
        if not self._run_tests():
            return
        # build
        pre, post = self._get_hooks()
        self._pre_building_hook, self._post_building_hook = pre, post
        if not self._run_pre_building_hook():
            return
        print("\nBuilding...")
        if sys.executable:
            args = ["setup.py", "--quiet", "sdist", "bdist_wheel"]
            p = subprocess.Popen([sys.executable, *args], cwd=target)
            p.communicate()
            code = p.returncode
            if code == 0:
                self._gen_build_report()
                if not self._run_post_building_hook():
                    return
                print("\nSuccessfully built !")
                return
            print("\nFailed to built the project.\nReturn code: {}".format(code))

    def _run_tests(self):
        if not self._ask_for_confirmation("Do you want to run tests first ?",
                                          "n"):
            return True
        print("Running tests...")
        test_exist, test_success, test_result = self._test_runner()
        if not test_exist:
            print("There aren't Tests\n")
            return True
        if test_success:
            print("Testing passed\n")
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

    def _ask_for_confirmation(self, message, default="y"):  #TODO: fix, EOF error (ctrl+d)
        cache = "Y/n" if default == "y" else "y/N"
        user_input = input("{} ({}): ".format(message, cache))
        if not user_input:
            user_input = default
        if user_input.lower() == "y":
            return True
        return False

    def _run_pre_building_hook(self):
        if not self._pre_building_hook:
            return True
        args = ["-m", self._pre_building_hook, self._target,
                self._app_pkg, self._version]
        p = subprocess.Popen([sys.executable, *args],
                             cwd=self._target)
        p.communicate()
        code = p.returncode
        print("")
        if code == 0:
            print("pre_building_hook.py executed with success")
            return True
        else:
            print("Failed to execute pre_building_hook.py")
            return False

    def _run_post_building_hook(self):
        if not self._post_building_hook:
            return True
        args = ["-m", self._post_building_hook, self._target,
                self._app_pkg, self._version]
        p = subprocess.Popen([sys.executable, *args],
                             cwd=self._target)
        p.communicate()
        code = p.returncode
        print("")
        if code == 0:
            print("post_building_hook.py executed with success")
            return True
        else:
            print("Failed to execute post_building_hook.py")
            return False

    def _gen_build_report(self):
        pyrustic_data_path = os.path.join(self._target,
                                          self._app_pkg,
                                          "pyrustic_data")
        try:
            os.mkdir(pyrustic_data_path)
        except Exception as e:
            pass
        res = "manager/default_json/pyrustic_data/build_report_default.json"
        default_build_report_json = pkgutil.get_data("pyrustic", res)
        build_report_json = os.path.join(pyrustic_data_path,
                                         "build_report.json")
        jasonix = Jasonix(build_report_json,
                          default=default_build_report_json)
        jasonix.data["timestamp"] = int(time.time())
        jasonix.data["target"] = self._target
        jasonix.data["app_pkg"] = self._app_pkg
        wheels_assets_list = wheels_assets(self._target)
        wheel_asset = None
        if wheels_assets_list:
            wheel_asset = wheels_assets_list[0]
            wheel_asset = os.path.join(self._target,
                                       "dist",
                                       wheel_asset)
        jasonix.data["app_version"] = self._version
        jasonix.data["wheel_asset"] = wheel_asset
        jasonix.save()

    def _get_hooks(self):
        dev_json = os.path.join(self._target,
                                self._app_pkg,
                                "pyrustic_data",
                                "dev.json")
        if not os.path.exists(dev_json):
            return None, None
        jasonix = Jasonix(dev_json)
        hooks_package = jasonix.data.get("hooking_pkg", None)
        if not hooks_package:
            return None, None
        pre_building_hook = "{}.pre_building_hook".format(hooks_package)
        post_building_hook = "{}.post_building_hook".format(hooks_package)
        return pre_building_hook, post_building_hook

    def _get_version(self):
        setup_config_dict = setup_config(self._target)
        version = None
        if setup_config_dict:
            version = setup_config_dict["version"]
        return version
