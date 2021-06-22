import os
import os.path
import getpass
from pyrustic import manager
from pyrustic.manager.handler.build_handler import BuildHandler
from pyrustic.manager.core.funcs import create_kurl
from jayson import Jayson


class PublishHandler:
    """
    Description
    -----------
    Use this command to publish the latest distribution
    package previously built with the command 'build'.

    Usage
    -----
    - Description: Publish
    - Command: publish

    Hooking
    -------
    This command will run hooks if they exist.
    The legal hooks are:
    - pre_publishing_hook.py
    - post_publishing_hook.py
    """

    def __init__(self, target, app_pkg, *args):
        self._target = target
        self._app_pkg = app_pkg
        self._pre_publishing_hook = None
        self._post_publishing_hook = None
        self._process(target, app_pkg)

    def _process(self, target, app_pkg):
        if target is None:
            print("Please link a Target first. Check 'help target'.")
            return
        if not os.path.exists(os.path.join(target, "setup.py")):
            print("Please initialize this project first. Check 'help init'.")
            return
        # check build_report
        self._check_build_report()
        version = manager.get_version(target)
        gurl = create_kurl()
        gurl.token = getpass.getpass("Your Github Token: ")
        print("Processing...")
        print("")
        try:
            data = manager.publish(gurl, target, app_pkg)
        except manager.ReleaseError as e:
            print("Failed to publish the distribution package")
        except manager.AnteReleaseHookError:
            print("Error while running the pre-publishing hook")
        except manager.PostReleaseHookError:
            print("Error while running the post-publishing hook")
        except manager.InvalidReleaseInfoError:
            msg = ("Missing mandatory elements in ",
                   "$APP_DIR/pyrustic_data/publishing.json")
            print("".join(msg))
        except manager.MissingReleaseInfoError:
            msg = ("Missing 'publishing.json' in ",
                   "'pyrustic_data' folder.\nPlease init your app.")
            print("".join(msg))
        else:
            success = self._interpret_release_data(data)
            if success:
                msg = "Successfully published '{}' v{} !"
                print(msg.format(app_pkg, version))

    def _check_build_report(self):
        build_report_json_path = os.path.join(self._target, self._app_pkg,
                                              "pyrustic_data", "build_report.json")
        if not os.path.exists(build_report_json_path):
            BuildHandler(self._target, self._app_pkg)
        jayson = Jayson(build_report_json_path)
        if jayson.data["released"]:
            BuildHandler(self._target, self._app_pkg)

    def _interpret_release_data(self, data):
        meta_code = data["meta_code"]
        status_code = data["status_code"]
        status_text = data["status_text"]
        if meta_code == 0:
            return True
        if meta_code == 1:
            print("Failed to create release.")
            if status_code:
                print("{} {}".format(status_code, status_text))
            else:
                print(status_text)
            return False
        if meta_code == 2:
            print("Failed to upload asset.\n{} {}".format(status_code,
                                                          status_text))
            return False
        print("Unknown error")
        return False
