import os
import os.path
from pyrustic.manager.misc import funcs
from pyrustic import about as pyrustic_about
from pyrustic.jasonix import Jasonix
from pyrustic.manager.handler.run_handler import RunHandler


class InitHandler:
    """
    Description
    -----------
    Use this command to init your project.
    Pyrustic Manager will install a basic
    project structure in your project.

    Usage
    -----
    - Description: Init your project
    - Command: init
    """
    def __init__(self, target, args):
        self._target = target
        self._process(args)

    def _process(self, args):
        if not self._target:
            print("You should link a Target first")
            return
        if args:
            print("Wrong usage of this command")
            return
        # create package
        self._make_packages()
        # create folders
        self._make_folders()
        # add files
        self._add_files()
        # add json data files
        self._add_json_data_files()
        print("Successfully installed basics !")
        # run
        data = input("\nDo you want to run the app ? (y/N): ")
        if data.lower() == "y":
            RunHandler(self._target, [])

    def _make_packages(self):
        packages = ("host", "view", "misc",
                    "tests", "tests.view", "tests.host",
                    "script.packaging")
        for package in packages:
            funcs.build_package(self._target, package)

    def _make_folders(self):
        folders = (("pyrustic_data", ),
                   ("script", ),
                   ("script", "packaging"))
        for folder in folders:
            path = os.path.join(self._target, *folder)
            if os.path.exists(path):
                continue
            os.mkdir(path)


    def _add_files(self):
        template_path = os.path.join(pyrustic_about.ROOT_DIR,
                                     "manager", "template")
        # add about.py
        src_path = os.path.join(template_path, "generic",
                                "about_template.txt")
        dest_path = os.path.join(self._target, "about.py")
        data = self._get_data_from_template(src_path)
        self._add_file(dest_path, data)
        # add main.py
        src_path = os.path.join(template_path, "init",
                                "main_template.txt")
        dest_path = os.path.join(self._target, "main.py")
        data = self._get_data_from_template(src_path)
        self._add_file(dest_path, data)
        # add main_view.py
        src_path = os.path.join(template_path, "init",
                                "main_view_template.txt")
        dest_path = os.path.join(self._target, "view", "main_view.py")
        data = self._get_data_from_template(src_path)
        self._add_file(dest_path, data)
        # add my_theme.py
        src_path = os.path.join(template_path, "init",
                                "my_theme_template.txt")
        dest_path = os.path.join(self._target, "misc", "my_theme.py")
        data = self._get_data_from_template(src_path)
        self._add_file(dest_path, data)
        # add test_main_view.py
        src_path = os.path.join(template_path, "init",
                                "test_main_view_template.txt")
        dest_path = os.path.join(self._target, "tests", "view", "test_main_view.py")
        data = self._get_data_from_template(src_path)
        self._add_file(dest_path, data)
        # add .gitignore
        src_path = os.path.join(template_path, "init",
                                "gitignore_template.txt")
        dest_path = os.path.join(self._target, ".gitignore")
        data = self._get_data_from_template(src_path)
        self._add_file(dest_path, data)
        # add packaging prolog
        src_path = os.path.join(template_path, "packaging",
                                "prolog_template.txt")
        dest_path = os.path.join(self._target, "script", "packaging",
                                 "prolog.py")
        data = self._get_data_from_template(src_path)
        self._add_file(dest_path, data)
        # add packaging Act I
        src_path = os.path.join(template_path, "packaging",
                                "act_1_template.txt")
        dest_path = os.path.join(self._target, "script", "packaging",
                                 "act_1.py")
        data = self._get_data_from_template(src_path)
        self._add_file(dest_path, data)
        # add packaging Act II
        src_path = os.path.join(template_path, "packaging",
                                "act_2_template.txt")
        dest_path = os.path.join(self._target, "script", "packaging",
                                 "act_2.py")
        data = self._get_data_from_template(src_path)
        self._add_file(dest_path, data)
        # add packaging epilog
        src_path = os.path.join(template_path, "packaging",
                                "epilog_template.txt")
        dest_path = os.path.join(self._target, "script", "packaging",
                                 "epilog.py")
        data = self._get_data_from_template(src_path)
        self._add_file(dest_path, data)
        # add packaging_exclusion
        src_path = os.path.join(template_path, "packaging",
                                "exclusion_template.txt")
        dest_path = os.path.join(self._target, "script", "packaging",
                                 "exclusion.txt")
        data = self._get_data_from_template(src_path)
        self._add_file(dest_path, data)
        # add LICENSE
        src_path = os.path.join(template_path, "init",
                                "license_template.txt")
        dest_path = os.path.join(self._target, "LICENSE")
        data = self._get_data_from_template(src_path)
        self._add_file(dest_path, data)
        # add README.md
        src_path = os.path.join(template_path, "init",
                                "readme_template.txt")
        dest_path = os.path.join(self._target, "README.md")
        data = self._get_data_from_template(src_path)
        self._add_file(dest_path, data)

    def _add_json_data_files(self):
        local_pyrustic_data_folder = os.path.join(self._target,
                                                  "pyrustic_data")
        # add app.json
        path = os.path.join(local_pyrustic_data_folder, "app.json")
        default_path = os.path.join(pyrustic_about.ROOT_DIR,
                                    "manager",
                                    "default_json",
                                    "pyrustic_data",
                                    "app_default.json")
        jasonix = Jasonix(path, default=default_path)
        project_name = os.path.basename(self._target)
        jasonix.data["project_name"] = project_name
        jasonix.data["project_title"] = project_name.capitalize()
        description = "A cool Python desktop application built with Pyrustic"
        jasonix.data["description"] = description
        jasonix.data["version"] = "0.0.1"
        jasonix.data["dev_mode"] = True
        jasonix.save()
        # add gui.json
        path = os.path.join(local_pyrustic_data_folder, "gui.json")
        default_path = os.path.join(pyrustic_about.ROOT_DIR,
                                    "manager",
                                    "default_json",
                                    "pyrustic_data",
                                    "gui_default.json")
        jasonix = Jasonix(path, default=default_path)
        # add packaging.json
        path = os.path.join(local_pyrustic_data_folder, "packaging.json")
        default_path = os.path.join(pyrustic_about.ROOT_DIR,
                                    "manager",
                                    "default_json",
                                    "pyrustic_data",
                                    "packaging_default.json")
        jasonix = Jasonix(path, default=default_path)
        jasonix.data["prolog"] = "script.packaging.prolog"
        jasonix.data["act_1"] = "script.packaging.act_1"
        jasonix.data["act_2"] = "script.packaging.act_2"
        jasonix.data["epilog"] = "script.packaging.epilog"
        jasonix.data["exclusion"] = "./script/packaging/exclusion.txt"
        jasonix.save()
        # add hubstore.json
        path = os.path.join(local_pyrustic_data_folder, "hubstore.json")
        default_path = os.path.join(pyrustic_about.ROOT_DIR,
                                    "manager",
                                    "default_json",
                                    "pyrustic_data",
                                    "hubstore_default.json")
        jasonix = Jasonix(path, default=default_path)

    def _get_data_from_template(self, path):
        data = ""
        with open(path, "r") as file:
            data = file.read()
        return data

    def _add_file(self, path, data):
        if os.path.exists(path):
            return
        with open(path, "w") as file:
            file.write(data)
