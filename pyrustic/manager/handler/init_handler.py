import os
import os.path
import pkgutil
from pyrustic.manager.misc import funcs
from pyrustic.jasonix import Jasonix


class InitHandler:
    """
    Description
    -----------
    Use this command to init your project.
    Pyrustic Manager will install a basic
    project structure in your project.
    The PROJECT_DIR is the project's root
    directory.
    The APP_DIR is the directory of your
    source code.
    The APP_PKG is simply the name of the
    root package of your source code.

    Usage
    -----
    - Description: Init your project
    - Command: init

    Example
    -------
    Assume the linked target is:
    /home/alex/demo
    This target is also your project root
    directory. And 'demo' is your project's
    name. So let's assume that your target
    is an empty directory.
    When you issue the command 'init', this
    is what the project root will look like:
    demo # target or PROJECT_ROOT
        demo # APP_PKG or APP_DIR, source here
            __main__.py # entry point
            __init__.py
            version.py # __version__ = "0.0.1"
            view # the demo.view package
                main_view.py # module
            pyrustic_data # folder
                hubstore.json
                gui.json # configure your GUI
        tests
            __init__.py
        setup.py
        setup.cfg # edit your project config
        pyproject.toml
        MANIFEST.in # don't worry, I take care

    So when you want to add a file "my_file.txt"
    and the module "mod.py" in the package
    demo.view, you issue in the manager:
        - add demo.view my_file.txt mod.py

    """
    def __init__(self, target, app_pkg, args):
        self._target = target
        self._app_pkg = app_pkg
        self._process(args)

    def _process(self, args):
        if not self._target:
            print("You should link a Target first")
            return
        if args:
            print("Wrong usage of this command")
            return
        # ask for app_pkg
        self._set_app_pkg()
        # create package
        self._make_packages()
        # create folders
        self._make_folders()
        # add files
        self._add_files()
        # add json data files
        self._add_json_data_files()
        print("Successfully initialized !")

    def _make_packages(self):
        hooking_pkg = "{}.hooking".format(self._app_pkg)
        packages = (self._app_pkg, "tests", hooking_pkg)
        for package in packages:
            funcs.build_package(self._target, package)
        app_dir = os.path.join(self._target, self._app_pkg)
        packages = ("view", )
        for package in packages:
            funcs.build_package(app_dir, package)

    def _make_folders(self):
        folders = ("pyrustic_data",)
        for folder in folders:
            path = os.path.join(self._target, self._app_pkg, folder)
            if os.path.exists(path):
                continue
            os.mkdir(path)

    def _add_files(self):
        resource_prefix = "manager/template/"
        # add version.py
        resource = resource_prefix + "version_template.txt"
        app_dir = os.path.join(self._target, self._app_pkg)
        dest_path = os.path.join(app_dir, "version.py")
        data = pkgutil.get_data("pyrustic", resource).decode("utf-8")
        self._add_file(dest_path, data)
        # add __main__.py
        resource = resource_prefix + "main_template.txt"
        dest_path = os.path.join(app_dir, "__main__.py")
        data = pkgutil.get_data("pyrustic", resource).decode("utf-8")
        data = data.format(app_pkg=self._app_pkg)
        self._add_file(dest_path, data)
        # add main_view.py
        resource = resource_prefix + "main_view_template.txt"
        dest_path = os.path.join(app_dir, "view", "main_view.py")
        data = pkgutil.get_data("pyrustic", resource).decode("utf-8")
        self._add_file(dest_path, data)
        # add .gitignore
        resource = resource_prefix + "gitignore_template.txt"
        dest_path = os.path.join(self._target, ".gitignore")
        data = pkgutil.get_data("pyrustic", resource).decode("utf-8")
        self._add_file(dest_path, data)
        # add LICENSE
        resource = resource_prefix + "license_template.txt"
        dest_path = os.path.join(self._target, "LICENSE")
        data = pkgutil.get_data("pyrustic", resource).decode("utf-8")
        self._add_file(dest_path, data)
        # add README.md
        resource = resource_prefix + "readme_template.txt"
        dest_path = os.path.join(self._target, "README.md")
        data = pkgutil.get_data("pyrustic", resource).decode("utf-8")
        self._add_file(dest_path, data)
        # add MANIFEST.in
        resource = resource_prefix + "manifest_template.txt"
        dest_path = os.path.join(self._target, "MANIFEST.in")
        data = pkgutil.get_data("pyrustic", resource).decode("utf-8")
        data = data.format(app_pkg=self._app_pkg)
        self._add_file(dest_path, data)
        # add setup.py
        resource = resource_prefix + "setup_py_template.txt"
        dest_path = os.path.join(self._target, "setup.py")
        data = pkgutil.get_data("pyrustic", resource).decode("utf-8")
        self._add_file(dest_path, data)
        # add setup.cfg
        resource = resource_prefix + "setup_cfg_template.txt"
        dest_path = os.path.join(self._target, "setup.cfg")
        data = pkgutil.get_data("pyrustic", resource).decode("utf-8")
        data = data.format(project_name=os.path.basename(self._target),
                           app_pkg=self._app_pkg)
        self._add_file(dest_path, data)
        # add pyproject.toml
        resource = resource_prefix + "pyproject_template.txt"
        dest_path = os.path.join(self._target, "pyproject.toml")
        data = pkgutil.get_data("pyrustic", resource).decode("utf-8")
        self._add_file(dest_path, data)
        # add pre_building_hook.py
        resource = resource_prefix + "pre_building_hook_template.txt"
        dest_path = os.path.join(self._target, self._app_pkg,
                                 "hooking",
                                 "pre_building_hook.py")
        data = pkgutil.get_data("pyrustic", resource).decode("utf-8")
        self._add_file(dest_path, data)
        # add post_building_hook.py
        resource = resource_prefix + "post_building_hook_template.txt"
        dest_path = os.path.join(self._target, self._app_pkg,
                                 "hooking",
                                 "post_building_hook.py")
        data = pkgutil.get_data("pyrustic", resource).decode("utf-8")
        self._add_file(dest_path, data)
        # add pre_publishing_hook.py
        resource = resource_prefix + "pre_publishing_hook_template.txt"
        dest_path = os.path.join(self._target, self._app_pkg,
                                 "hooking",
                                 "pre_publishing_hook.py")
        data = pkgutil.get_data("pyrustic", resource).decode("utf-8")
        self._add_file(dest_path, data)
        # add post_publishing_hook.py
        resource = resource_prefix + "post_publishing_hook_template.txt"
        dest_path = os.path.join(self._target, self._app_pkg,
                                 "hooking",
                                 "post_publishing_hook.py")
        data = pkgutil.get_data("pyrustic", resource).decode("utf-8")
        self._add_file(dest_path, data)

    def _add_json_data_files(self):
        local_pyrustic_data_folder = os.path.join(self._target,
                                                  self._app_pkg,
                                                  "pyrustic_data")
        resource_prefix = "manager/default_json/pyrustic_data/"
        # add dev.json
        path = os.path.join(local_pyrustic_data_folder, "dev.json")
        default_resource = resource_prefix + "dev_default.json"
        data = pkgutil.get_data("pyrustic", default_resource)
        if not os.path.exists(path):
            with open(path, "wb") as file:
                file.write(data)
        jasonix = Jasonix(path)
        jasonix.data["hooking_pkg"] = "{}.hooking".format(self._app_pkg)
        jasonix.save()
        # add gui.json
        path = os.path.join(local_pyrustic_data_folder, "gui.json")
        default_resource = resource_prefix + "gui_default.json"
        data = pkgutil.get_data("pyrustic", default_resource)
        if not os.path.exists(path):
            with open(path, "wb") as file:
                file.write(data)
        # add publishing.json
        path = os.path.join(local_pyrustic_data_folder,
                            "publishing.json")
        default_resource = resource_prefix + "publishing_default.json"
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

    def _add_file(self, path, data):
        if os.path.exists(path):
            return
        with open(path, "w") as file:
            file.write(data)

    def _set_app_pkg(self):
        if self._app_pkg is not None:
            return
        self._app_pkg = os.path.basename(self._target)
