import os
import os.path
from pyrustic.private.tool.manager.misc import funcs
from pyrustic import about as pyrustic_about
from pyrustic.jasonix import Jasonix
from pyrustic.private.tool.manager.handler.run_handler import RunHandler


class KstartHandler:
    """
    Description
    -----------
    Use this command to kickstart your project.
    Pyrustic Manager will execute the "sync" command,
    then install a basic project structure.

    Usage
    -----
    - Description: Kickstart your project
    - Command: kstart
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
        packages = ("view", "misc",
                "tests", "tests.view", "secret")
        for package in packages:
            funcs.build_package(self._target, package)

    def _make_folders(self):
        folders = ("cache", "pyrustic_data", "script")
        for folder in folders:
            path = os.path.join(self._target, folder)
            if os.path.exists(path):
                continue
            os.mkdir(path)

    def _add_files(self):
        template_path = os.path.join(pyrustic_about.ROOT_DIR,
                                     "private", "tool", "manager",
                                     "template")
        # add about.py
        src_path = os.path.join(template_path, "about_template.txt")
        dest_path = os.path.join(self._target, "about.py")
        data = self._get_data_from_template(src_path)
        self._add_file(dest_path, data)
        # add main.py
        src_path = os.path.join(template_path, "kstart_main_template.txt")
        dest_path = os.path.join(self._target, "main.py")
        data = self._get_data_from_template(src_path)
        self._add_file(dest_path, data)
        # add __main__.py
        dest_path = os.path.join(self._target, "__main__.py")
        data = "import main\n"
        self._add_file(dest_path, data)
        # add main_view.py
        src_path = os.path.join(template_path, "kstart_main_view_template.txt")
        dest_path = os.path.join(self._target, "view", "main_view.py")
        data = self._get_data_from_template(src_path)
        self._add_file(dest_path, data)
        # add scratch.py
        src_path = os.path.join(template_path, "scratch_template.txt")
        dest_path = os.path.join(self._target, "secret", "scratch.py")
        data = self._get_data_from_template(src_path)
        self._add_file(dest_path, data)
        # add notes.txt
        dest_path = os.path.join(self._target, "secret", "notes.txt")
        data = "# notes"
        self._add_file(dest_path, data)
        # add my_theme.py
        src_path = os.path.join(template_path, "kstart_my_theme_template.txt")
        dest_path = os.path.join(self._target, "misc", "my_theme.py")
        data = self._get_data_from_template(src_path)
        self._add_file(dest_path, data)
        # add test_main_view.py
        src_path = os.path.join(template_path, "kstart_test_main_view_template.txt")
        dest_path = os.path.join(self._target, "tests", "view", "test_main_view.py")
        data = self._get_data_from_template(src_path)
        self._add_file(dest_path, data)
        # add .gitignore
        src_path = os.path.join(template_path, "gitignore_template.txt")
        dest_path = os.path.join(self._target, ".gitignore")
        data = self._get_data_from_template(src_path)
        self._add_file(dest_path, data)
        # add build_epilog
        src_path = os.path.join(template_path, "build_epilog_template.txt")
        dest_path = os.path.join(self._target, "script", "build_epilog.py")
        data = self._get_data_from_template(src_path)
        self._add_file(dest_path, data)
        # add build_act_1
        src_path = os.path.join(template_path, "build_act_1_template.txt")
        dest_path = os.path.join(self._target, "script", "build_act_1.py")
        data = self._get_data_from_template(src_path)
        self._add_file(dest_path, data)
        # add build_act_2
        src_path = os.path.join(template_path, "build_act_2_template.txt")
        dest_path = os.path.join(self._target, "script", "build_act_2.py")
        data = self._get_data_from_template(src_path)
        self._add_file(dest_path, data)
        # add build_prolog
        src_path = os.path.join(template_path, "build_prolog_template.txt")
        dest_path = os.path.join(self._target, "script", "build_prolog.py")
        data = self._get_data_from_template(src_path)
        self._add_file(dest_path, data)
        # add build_exclusion
        src_path = os.path.join(template_path, "build_exclusion_template.txt")
        dest_path = os.path.join(self._target, "pyrustic_data",
                                 "build_exclusion.txt")
        data = self._get_data_from_template(src_path)
        self._add_file(dest_path, data)
        # add LICENSE
        src_path = os.path.join(template_path, "license_template.txt")
        dest_path = os.path.join(self._target, "LICENSE")
        data = self._get_data_from_template(src_path)
        self._add_file(dest_path, data)
        # add README.md
        src_path = os.path.join(template_path, "readme_template.txt")
        dest_path = os.path.join(self._target, "README.md")
        data = self._get_data_from_template(src_path)
        self._add_file(dest_path, data)

    def _add_json_data_files(self):
        local_pyrustic_data_folder = os.path.join(self._target,
                                                  "pyrustic_data")
        # add build.json
        path = os.path.join(local_pyrustic_data_folder, "build.json")
        default_path = os.path.join(pyrustic_about.ROOT_DIR,
                                    "private", "tool", "common",
                                    "default_json_data",
                                    "default_build.json")
        jasonix = Jasonix(path, default=default_path)
        jasonix.data["prolog"] = "script.build_prolog"
        jasonix.data["act_1"] = "script.build_act_1"
        jasonix.data["act_2"] = "script.build_act_2"
        jasonix.data["epilog"] = "script.build_epilog"
        jasonix.data["exclusion"] = "./pyrustic_data/build_exclusion.txt"
        jasonix.save()
        # add about.json
        path = os.path.join(local_pyrustic_data_folder, "about.json")
        default_path = os.path.join(pyrustic_about.ROOT_DIR,
                                    "private", "tool", "common",
                                    "default_json_data",
                                    "default_about.json")
        jasonix = Jasonix(path, default=default_path)
        project_name = os.path.basename(self._target)
        jasonix.data["project_name"] = project_name
        jasonix.data["project_title"] = project_name.capitalize()
        description = "A cool Python desktop application built with Pyrustic"
        jasonix.data["description"] = description
        jasonix.data["version"] = "0.0.1"
        jasonix.data["dev_mode"] = True
        jasonix.save()

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
