import os
import os.path
import pkgutil
from jayson import Jayson
from pyrustic.manager.core import funcs


def init(target, app_pkg):
    # create package
    _make_packages(target, app_pkg)
    # create folders
    _make_folders(target, app_pkg)
    # add files
    _add_files(target, app_pkg)
    # add json data files
    _add_json_data_files(target, app_pkg)


def _make_packages(target, app_pkg):
    hooking_pkg = "{}.hooking".format(app_pkg)
    packages = (app_pkg, hooking_pkg, "tests")
    for package in packages:
        funcs.build_package(target, package)


def _make_folders(target, app_pkg):
    # folders to make inside app_pkg
    folders = ("pyrustic_data",)
    for folder in folders:
        path = os.path.join(target, app_pkg, folder)
        if os.path.exists(path):
            continue
        os.mkdir(path)


def _add_files(target, app_pkg):
    resource_prefix = "manager/template/"
    app_dir = os.path.join(target, app_pkg)
    # add VERSION
    resource = resource_prefix + "version_template.txt"
    dest_path = os.path.join(target, "VERSION")
    data = pkgutil.get_data("pyrustic", resource).decode("utf-8")
    _add_file(dest_path, data)
    # add __main__.py
    resource = resource_prefix + "main_template.txt"
    dest_path = os.path.join(app_dir, "__main__.py")
    data = pkgutil.get_data("pyrustic", resource).decode("utf-8")
    data = data.format(title=app_pkg)
    _add_file(dest_path, data)
    # add .gitignore
    resource = resource_prefix + "gitignore_template.txt"
    dest_path = os.path.join(target, ".gitignore")
    data = pkgutil.get_data("pyrustic", resource).decode("utf-8")
    _add_file(dest_path, data)
    # add LICENSE
    resource = resource_prefix + "license_template.txt"
    dest_path = os.path.join(target, "LICENSE")
    data = pkgutil.get_data("pyrustic", resource).decode("utf-8")
    _add_file(dest_path, data)
    # add README.md
    resource = resource_prefix + "readme_template.txt"
    dest_path = os.path.join(target, "README.md")
    data = pkgutil.get_data("pyrustic", resource).decode("utf-8")
    _add_file(dest_path, data)
    # add MANIFEST.in
    resource = resource_prefix + "manifest_template.txt"
    dest_path = os.path.join(target, "MANIFEST.in")
    data = pkgutil.get_data("pyrustic", resource).decode("utf-8")
    data = data.format(app_pkg=app_pkg)
    _add_file(dest_path, data)
    # add setup.py
    resource = resource_prefix + "setup_py_template.txt"
    dest_path = os.path.join(target, "setup.py")
    data = pkgutil.get_data("pyrustic", resource).decode("utf-8")
    _add_file(dest_path, data)
    # add setup.cfg
    resource = resource_prefix + "setup_cfg_template.txt"
    dest_path = os.path.join(target, "setup.cfg")
    data = pkgutil.get_data("pyrustic", resource).decode("utf-8")
    data = data.format(project_name=os.path.basename(target),
                       app_pkg=app_pkg)
    _add_file(dest_path, data)
    # add pyproject.toml
    resource = resource_prefix + "pyproject_template.txt"
    dest_path = os.path.join(target, "pyproject.toml")
    data = pkgutil.get_data("pyrustic", resource).decode("utf-8")
    _add_file(dest_path, data)
    # add LATEST_RELEASE.Md
    resource = resource_prefix + "latest_release_template.txt"
    dest_path = os.path.join(target, "LATEST_RELEASE.md")
    data = pkgutil.get_data("pyrustic", resource).decode("utf-8")
    _add_file(dest_path, data)
    # add CHANGELOG.Md
    resource = resource_prefix + "changelog_template.txt"
    dest_path = os.path.join(target, "CHANGELOG.md")
    data = pkgutil.get_data("pyrustic", resource).decode("utf-8")
    _add_file(dest_path, data)
    # add ante_build_hook.py
    resource = resource_prefix + "ante_build_hook_template.txt"
    dest_path = os.path.join(target, app_pkg,
                             "hooking",
                             "ante_build_hook.py")
    data = pkgutil.get_data("pyrustic", resource).decode("utf-8")
    _add_file(dest_path, data)
    # add post_build_hook.py
    resource = resource_prefix + "post_build_hook_template.txt"
    dest_path = os.path.join(target, app_pkg,
                             "hooking",
                             "post_build_hook.py")
    data = pkgutil.get_data("pyrustic", resource).decode("utf-8")
    _add_file(dest_path, data)
    # add ante_release_hook.py
    resource = resource_prefix + "ante_release_hook_template.txt"
    dest_path = os.path.join(target, app_pkg,
                             "hooking",
                             "ante_release_hook.py")
    data = pkgutil.get_data("pyrustic", resource).decode("utf-8")
    _add_file(dest_path, data)
    # add post_release_hook.py
    resource = resource_prefix + "post_release_hook_template.txt"
    dest_path = os.path.join(target, app_pkg,
                             "hooking",
                             "post_release_hook.py")
    data = pkgutil.get_data("pyrustic", resource).decode("utf-8")
    _add_file(dest_path, data)


def _add_json_data_files(target, app_pkg):
    local_pyrustic_data_folder = os.path.join(target,
                                              app_pkg,
                                              "pyrustic_data")
    resource_prefix = "manager/default_json/pyrustic_data/"
    # add hooking.json
    path = os.path.join(local_pyrustic_data_folder, "hooking.json")
    default_resource = resource_prefix + "hooking_default.json"
    data = pkgutil.get_data("pyrustic", default_resource)
    if not os.path.exists(path):
        with open(path, "wb") as file:
            file.write(data)
    jayson = Jayson(path)
    jayson.data["ante_build"] = ["{}.hooking.ante_build_hook".format(app_pkg)]
    jayson.data["post_build"] = ["{}.hooking.post_build_hook".format(app_pkg)]
    jayson.data["ante_release"] = ["{}.hooking.ante_release_hook".format(app_pkg)]
    jayson.data["post_release"] = ["{}.hooking.post_release_hook".format(app_pkg)]
    jayson.save()
    # add release_info.json
    path = os.path.join(local_pyrustic_data_folder,
                        "release_info.json")
    default_resource = resource_prefix + "release_info_default.json"
    data = pkgutil.get_data("pyrustic", default_resource)
    if not os.path.exists(path):
        with open(path, "wb") as file:
            file.write(data)
    # add hubstore.json
    path = os.path.join(local_pyrustic_data_folder, "hubstore.json")
    default_resource = resource_prefix + "hubstore_default.json"
    data = pkgutil.get_data("pyrustic", default_resource)
    if not os.path.exists(path):
        with open(path, "wb") as file:
            file.write(data)


def _add_file(path, data):
    if os.path.exists(path):
        return
    with open(path, "w") as file:
        file.write(data)
    
        
class Error(Exception):
    def __init__(self, *args, **kwargs):
        self.message = args[0] if args else ""
        super().__init__(self.message)

    def __str__(self):
        return self.message
