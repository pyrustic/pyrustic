import sys
import time
import os
import os.path
import pkgutil
from jayson import Jayson
from pyrustic import manager
from pyrustic.manager.core.funcs import wheels_assets


def build(target, app_pkg):
    # version
    version = manager.get_version(target)
    # build
    ante_build_hooks, post_build_hooks = _get_hooks(target, app_pkg)
    # Run ante build hooks
    for hook in ante_build_hooks:
        if not _run_build_hook(target, app_pkg, version, hook):
            raise manager.AnteBuildHookError
    if sys.executable:
        args = ["setup.py", "--quiet", "sdist", "bdist_wheel"]
        code = manager.run(target, *args)
        if code == 0:
            _gen_build_report(target, app_pkg, version)
            # Run post build hooks
            for hook in post_build_hooks:
                if not _run_build_hook(target, app_pkg, version, hook):
                    raise manager.PostBuildHookError
            return
        raise manager.BuildError


def _run_build_hook(target, app_pkg, version, hook):
    if not hook:
        return True
    args = ["-m", hook, target,
            app_pkg, version]
    code = manager.run(target, *args)
    if code == 0:
        return True
    else:
        return False


def _gen_build_report(target, app_pkg, version):
    pyrustic_data_path = os.path.join(target,
                                      app_pkg,
                                      "pyrustic_data")
    try:
        os.mkdir(pyrustic_data_path)
    except Exception as e:
        pass
    res = "manager/default_json/pyrustic_data/build_report_default.json"
    default_build_report_json = pkgutil.get_data("pyrustic", res)
    build_report_json = os.path.join(pyrustic_data_path,
                                     "build_report.json")
    jasonix = Jayson(build_report_json,
                      default=default_build_report_json)
    jasonix.data["timestamp"] = int(time.time())
    wheels_assets_list = wheels_assets(target)
    wheel_asset = None
    if wheels_assets_list:
        wheel_asset = wheels_assets_list[0]
    jasonix.data["app_version"] = version
    jasonix.data["wheel_asset"] = wheel_asset
    jasonix.data["released"] = False
    jasonix.save()


def _get_hooks(target, app_pkg):
    hooking_json = os.path.join(target,
                                app_pkg,
                                "pyrustic_data",
                                "hooking.json")
    if not os.path.exists(hooking_json):
        return [], []
    jasonix = Jayson(hooking_json)
    ante_build_hooks = jasonix.data.get("ante_build", [])
    post_build_hooks = jasonix.data.get("post_build", [])
    return ante_build_hooks, post_build_hooks


class Error(Exception):
    def __init__(self, *args, **kwargs):
        self.message, self.code = (args[0], args[1]) if args else ("", None)
        super().__init__(self.message)

    def __str__(self):
        return self.message
