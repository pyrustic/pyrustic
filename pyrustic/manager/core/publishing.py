import os
import os.path
from jayson import Jayson
from pyrustic import manager
from pyrustic.manager.core import github_client


def publish(kurl, target, app_pkg):
    version = manager.get_version(target)
    # get publishing hooks
    ante_release_hooks, post_release_hooks = _get_hooks(target, app_pkg)
    # execute ante_release_hook.py
    for hook in ante_release_hooks:
        if not _run_release_hook(target, app_pkg, version, hook):
            raise manager.AnteReleaseHookError
    # publish
    try:
        data = _publish(kurl, target, app_pkg, version)
    except Exception as e:
        raise manager.ReleaseError
    if data["meta_code"] != 0:
        return data
    # execute post_publishing_hook.py
    for hook in post_release_hooks:
        if not _run_release_hook(target, app_pkg, version, hook):
            raise manager.PostReleaseHookError
    return data


def _get_hooks(target, app_pkg):
    hooking_json = os.path.join(target,
                            app_pkg,
                            "pyrustic_data",
                            "hooking.json")
    if not os.path.exists(hooking_json):
        return [], []
    jayson = Jayson(hooking_json)
    ante_release_hooks = jayson.data.get("ante_release", [])
    post_release_hooks = jayson.data.get("post_release", [])
    return ante_release_hooks, post_release_hooks


def _run_release_hook(target, app_pkg, version, hook):
    if not hook:
        return True
    args = ["-m", hook, target,
            app_pkg, version]
    code = manager.run(target, *args)
    if code == 0:
        return True
    else:
        return False


def _publish(kurl, target, app_pkg, version):
    release_info_json_path = os.path.join(target, app_pkg,
                                        "pyrustic_data",
                                        "release_info.json")
    build_report_json_path = os.path.join(target, app_pkg,
                                          "pyrustic_data",
                                          "build_report.json")
    if not os.path.exists(release_info_json_path):
        raise manager.MissingReleaseInfoError
    jayson = Jayson(release_info_json_path)
    owner = jayson.data.get("owner", None)
    repository = jayson.data.get("repository", None)
    release_name = jayson.data.get("release_name", None)
    tag_name = jayson.data.get("tag_name", None)
    target_commitish = jayson.data.get("target_commitish", None)
    description = jayson.data.get("description", None)
    prerelease = jayson.data.get("is_prerelease", None)
    draft = jayson.data.get("is_draft", None)
    upload_asset = jayson.data.get("upload_asset", None)
    asset_name = jayson.data.get("asset_name", None)
    asset_path = os.path.join(target, "dist", asset_name)
    asset_path = None if not os.path.exists(asset_path) else asset_path
    asset_label = jayson.data.get("asset_label", None)
    if (not release_name or not tag_name
            or not asset_path or not owner or not repository):
        raise manager.InvalidReleaseInfoError
    github_release = github_client.Release(kurl, owner, repository)
    data = github_release.publish(release_name, tag_name,
                                  target_commitish, description,
                                  prerelease, draft, upload_asset,
                                  asset_path, asset_name, asset_label)
    if data["meta_code"] == 201:
        if os.path.exists(build_report_json_path):
            jayson = Jayson(build_report_json_path)
            if version == jayson.data["version"]:
                jayson.data["released"] = True
                jayson.save()
    return data


class Error(Exception):
    def __init__(self, *args, **kwargs):
        self.message, self.code = (args[0], args[1]) if args else ("", None)
        super().__init__(self.message)

    def __str__(self):
        return self.message
