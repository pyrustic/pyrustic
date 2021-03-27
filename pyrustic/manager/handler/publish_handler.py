import os
import os.path
import sys
import subprocess
import getpass
from pyrustic.jasonix import Jasonix
from pyrustic.manager.hubway import Catapult
from pyrustic.manager.misc.funcs import create_gurl, setup_config


class PublishHandler:
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
        self._pre_publishing_hook = None
        self._post_publishing_hook = None
        self._process(target, app_pkg)

    def _process(self, target, app_pkg):
        if target is None:
            print("Please link a Target first. Check 'help target'.")
            return
        if not app_pkg:
            print("Please initialize this project first. Check 'help init'.")
            return
        # get version
        self._version = self._get_version()
        # get confirmation
        message = "You are going to publish '{}' v{}.".format(app_pkg,
                                                              self._version)
        print(message)
        if not self._ask_for_confirmation("\nDo you want to continue ?"):
            return
        print("")
        # check build_report
        if not self._check_build_report():
            return
        # get publishing hooks
        cache = self._get_hooks()
        self._pre_publishing_hook, self._post_publishing_hook = cache
        # execute pre_publishing_hook.py
        if not self._run_pre_publishing_hook():
            return
        # publish
        if not self._publish():
            return
        # execute post_publishing_hook.py
        if not self._run_post_publishing_hook():
            return
        print("\nSuccessfully published !")

    def _check_build_report(self):
        path = os.path.join(self._target, self._app_pkg,
                            "pyrustic_data", "build_report.json")
        if os.path.exists(path):
            return True
        text = ("\nMissing 'build_report.json' file in 'pyrustic_data' folder.",
                "Please build the project first with the command 'build'")
        print("\n".join(text))
        return False

    def _run_pre_publishing_hook(self):
        if not self._pre_publishing_hook:
            return True
        args = ["-m", self._pre_publishing_hook, self._target,
                self._app_pkg, self._version]
        p = subprocess.Popen([sys.executable, *args],
                             cwd=self._target)
        p.communicate()
        code = p.returncode
        if code == 0:
            print("pre_publishing_hook.py executed with success")
            return True
        else:
            print("Failed to execute pre_publishing_hook.py")
            return False

    def _run_post_publishing_hook(self):
        if not self._post_publishing_hook:
            return True
        args = ["-m", self._post_publishing_hook, self._target,
                self._app_pkg, self._version]
        p = subprocess.Popen([sys.executable, *args],
                             cwd=self._target)
        p.communicate()
        code = p.returncode
        print("")
        if code == 0:
            print("post_publishing_hook.py executed with success")
            return True
        else:
            print("Failed to execute pre_publishing_hook.py")
            return False

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
        pre_publishing_hook = "{}.pre_publishing_hook".format(hooks_package)
        post_publishing_hook = "{}.post_publishing_hook".format(hooks_package)
        return pre_publishing_hook, post_publishing_hook

    def _publish(self):
        publishing_json_path = os.path.join(self._target, self._app_pkg,
                                            "pyrustic_data",
                                            "publishing.json")
        if not os.path.exists(publishing_json_path):
            print("Missing 'publishing.json' in 'pyrustic_data' folder.\nPlease init your app.")
            return False
        jasonix = Jasonix(publishing_json_path)
        owner = jasonix.data.get("owner", None)
        repo = jasonix.data.get("repo", None)
        name = jasonix.data.get("name", None)
        tag_name = jasonix.data.get("tag_name", None)
        target_commitish = jasonix.data.get("target_commitish", None)
        description = jasonix.data.get("description", None)
        prerelease = jasonix.data.get("prerelease", None)
        draft = jasonix.data.get("draft", None)
        asset_path = jasonix.data.get("asset_path", None)
        asset_name = jasonix.data.get("asset_name", None)
        asset_label = jasonix.data.get("asset_label", None)
        if (not name or not tag_name
                or not asset_path or not owner or not repo):
            print("Missing mandatory elements in $APP_DIR/pyrustic_data/publishing.json")
            return False
        gurl = create_gurl()
        gurl.token = getpass.getpass("\nYour Github Token: ")
        print("\nProcessing...")
        catapult = Catapult(gurl, owner, repo)
        cache = catapult.publish(name, tag_name,target_commitish,
                         description, prerelease, draft,
                         asset_path, asset_name, asset_label)
        meta_code = cache["meta_code"]
        status_code = cache["status_code"]
        status_text = cache["status_text"]
        if meta_code == 0:
            return True
        if meta_code == 1:
            print("Failed to create release.\n{} {}".format(status_code,
                                                            status_text))
            return False
        if meta_code == 2:
            print("Failed to upload asset.\n{} {}".format(status_code,
                                                            status_text))
            return False
        print("Unknown error")
        return False

    def _get_version(self):
        setup_config_dict = setup_config(self._target)
        version = None
        if setup_config_dict:
            version = setup_config_dict["version"]
        return version

    def _ask_for_confirmation(self, message, default="y"):
        cache = "Y/n" if default == "y" else "y/N"
        user_input = input("{} ({}): ".format(message, cache))
        if not user_input:
            user_input = default
        if user_input.lower() == "y":
            return True
        return False
