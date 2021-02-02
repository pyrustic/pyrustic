from pyrustic.manager.misc import funcs
import os
import os.path
from pyrustic import about as pyrustic_about


class AddHandler:
    """
    Description
    -----------
    Use this command to add a file, a package or a regular folder
    to the Target.
    Pyrustic Manager will assume that files with extension ".py"
    are modules. In this case, the Manager will create the
    corresponding test package and the test file.
    Some convenient lines of code may be automatically inserted
    into modules based on the package name.

    Usage
    -----
    - Description: Add a file
    - Command: add <destination> <file.ext>

    - Description: Add multiple files
    - Command: add <destination> <file_1.ext> <file_2.ext>

    - Description: Add a module
    - Command: add <destination> <file.py>

    - Description: Add a package
    - Command: add <my.pack.age>

    - Description: Add a file to the Target's ROOT_DIR
    - Command: add ./ <file.ext>

    - Description: Add a module to the Target's ROOT_DIR
    - Command: add . <file.py>

    Note: The destination is either a relative path to the
    Target's ROOT_DIR, or a package name.
    Also, only SLASH is allowed in the path as separator.

    Example
    -------
    - Description: Add a module
    - Preliminary: Assume you want to add "my_view.py"
    to the package 'view'
    - Command: add view my_view.py

    - Description: Add a package
    - Preliminary: Assume you want to add 'my.new.package'
    - Command: add my.new.package

    Note: Please use simple or double quotes as delimiters if a
    string contains space
    """
    def __init__(self, target, args):
        self._target = target
        self._args = args
        self._is_tests_package_built = False
        self._process(target, args)

    def _process(self, target, args):
        if not target:
            self._print_catalog("missing_target")
            return
        if not args:
            self._print_catalog("incomplete")
            return
        # package or folder
        package_or_folder_name = args[0]
        if (package_or_folder_name == "."
                or ("/" not in package_or_folder_name
                and "\\" not in package_or_folder_name)):
            self._process_package_and_files(target, args)
        else:
            self._process_folder_and_files(target, args)

    def _process_package_and_files(self, target, args):
        package_name = args[0]
        if len(args) > 1:
            if not self._handle_package_part(target, package_name, verbose=False):
                return
            self._add_files_into_package(target, package_name, args[1:])
        else:
            self._handle_package_part(target, package_name)

    def _process_folder_and_files(self, target, args):
        folder = args[0]
        if len(args) > 1:
            if not self._handle_folder_part(target, folder, verbose=False):
                return
            self._add_files_into_folder(target, folder, args[1:])
        else:
            self._handle_folder_part(target, folder)

    def _handle_package_part(self, target, package_name, verbose=True):
        path = funcs.package_name_to_path(target, package_name)
        if os.path.isdir(path):
            if verbose:
                self._print_catalog("package_already_exists")
            return True
        self._print_catalog("package_not_exists")
        self._print_catalog("building_package", package_name=package_name)
        path = funcs.build_package(target, package_name)
        if path is None:
            self._print_catalog("failed_to_build_package")
            return False
        else:
            self._print_catalog("package_built")
            return True

    def _add_files_into_package(self, target, package_name, files):
        for file in files:
            # Is module
            if file.endswith(".py"):
                if not self._install_module(target, package_name, file):
                    return False
            # Is simple file
            else:
                if not self._install_file(target, package_name, file):
                    return False
        return True

    def _handle_folder_part(self, target, folder, verbose=True):
        path = os.path.join(target, folder)
        path = os.path.normpath(path)
        if os.path.isdir(path):
            if verbose:
                self._print_catalog("folder_already_exists")
            return True
        self._print_catalog("folder_not_exists")
        self._print_catalog("creating_folder", folder=folder)
        try:
            os.makedirs(path)
        except Exception as e:
            self._print_catalog("failed_to_create_folder")
            return False
        else:
            self._print_catalog("folder_created")
            return True

    def _add_files_into_folder(self, target, folder, files):
        path = os.path.join(target, folder)
        path = os.path.normpath(path)
        for filename in files:
            path = os.path.join(path, filename)
            if os.path.exists(path):
                self._print_catalog("file_exists", filename=filename)
                continue
            try:
                with open(path, "w") as file:
                    pass
            except Exception as e:
                self._print_catalog("file_creation_failed", filename=filename)
                return False
            self._print_catalog("file_created", filename=filename)
        return True

    def _install_module(self, target, package_name, filename):
        # mirror package in tests
        if (not self._is_tests_package_built
                and not funcs.get_root_from_package(package_name) == "tests"):
            self._is_tests_package_built = True
            if not self._mirror_tests_package(target, package_name):
                return False
        # creating file
        class_name = funcs.module_name_to_class(filename)
        test_class_name = "Test{}".format(class_name)
        path = funcs.package_name_to_path(target, package_name)
        path = os.path.join(path, filename)
        test_filename = "test_{}".format(filename)
        test_path = funcs.package_name_to_path(target, package_name, prefix="tests.")
        test_path = os.path.join(test_path, test_filename)
        if os.path.exists(path):
            self._print_catalog("module_exists", module=filename)
            return True
        template_path = os.path.join(pyrustic_about.ROOT_DIR,
                                     "private", "suite",
                                     "manager", "template")
        with open(path, "w") as file:
            if funcs.get_root_from_package(package_name) == "dao":
                path = os.path.join(template_path, "dao_template.txt")
                data = self._get_data_from_template(path)
                file.write(data.format(class_name))
            elif funcs.get_root_from_package(package_name) == "host":
                path = os.path.join(template_path, "host_template.txt")
                data = self._get_data_from_template(path)
                file.write(data.format(class_name))
            elif funcs.get_root_from_package(package_name) == "view":
                path = os.path.join(template_path, "view_template.txt")
                data = self._get_data_from_template(path)
                file.write(data.format(class_name))
            elif funcs.get_root_from_package(package_name) == "tests":
                path = os.path.join(template_path, "test_template.txt")
                data = self._get_data_from_template(path)
                file.write(data.format(class_name))
            else:
                path = os.path.join(template_path, "module_template.txt")
                data = self._get_data_from_template(path)
                file.write(data.format(class_name))
            self._print_catalog("module_created", module=filename)
        if os.path.exists(test_path):
            return True
        if funcs.get_root_from_package(package_name) == "tests":
            return True
        with open(test_path, "w") as file:
            path = os.path.join(template_path, "test_template.txt")
            data = self._get_data_from_template(path)
            file.write(data.format(test_class_name))
            self._print_catalog("test_module_created", module=test_filename)
        return True

    def _install_file(self, target, package_name, filename):
        path = funcs.package_name_to_path(target, package_name)
        path = os.path.join(path, filename)
        if os.path.exists(path):
            self._print_catalog("file_exists", filename=filename)
            return True
        try:
            with open(path, "w") as file:
                pass
        except Exception as e:
            self._print_catalog("file_creation_failed", filename=filename)
            return False
        self._print_catalog("file_created", filename=filename)
        return True

    def _create_file(self):
        pass

    def _mirror_tests_package(self, target, package_name):
        tests_path = os.path.join(target, "tests")
        if not os.path.exists(tests_path):
            os.mkdir(tests_path)
        path = funcs.package_name_to_path(tests_path, package_name)
        if os.path.exists(path):
            return True
        path = funcs.build_package(tests_path, package_name)
        if path is None:
            self._print_catalog("failed_to_build_tests_package")
            return False
        self._print_catalog("tests_package_built")
        return True

    def _get_data_from_template(self, path):
        data = ""
        with open(path, "r") as file:
            data = file.read()
        return data

    def _print_catalog(self, item, **kwargs):
        message = ""
        if item == "missing_target":
            message = "Please link a Target first. Check 'help target'."
        elif item == "incomplete":
            message = "Incomplete command. Check 'help add'."
        elif item == "package_already_exists":
            message = "This package already exists !"
        elif item == "package_not_exists":
            message = "This package doesn't exist yet."
        elif item == "building_package":
            message = "Building package '{}'".format(kwargs["package_name"])
        elif item == "package_built":
            message = "Package successfully built."
        elif item == "failed_to_build_package":
            message = "Failed to finish the package building."
        elif item == "failed_to_build_tests_package":
            message = "Failed to finish the tests package building."
        elif item == "tests_package_built":
            message = "Tests package successfully built."
        elif item == "file_created":
            message = "File '{}' successfully created.".format(kwargs["filename"])
        elif item == "file_creation_failed":
            message = "Failed to create file '{}'.".format(kwargs["filename"])
        elif item == "file_exists":
            message = "The file '{}' already exists.".format(kwargs["filename"])
        elif item == "module_exists":
            message = "The module '{}' already exists.".format(kwargs["module"])
        elif item == "module_created":
            message = "Module '{}' successfully created.".format(kwargs["module"])
        elif item == "test_module_created":
            message = "Test module '{}' successfully created.".format(kwargs["module"])
        elif item == "folder_already_exists":
            message = "This folder already exists !"
        elif item == "folder_not_exists":
            message = "This folder doesn't exist yet."
        elif item == "creating_folder":
            message = "Creating folder '{}'".format(kwargs["folder"])
        elif item == "folder_created":
            message = "Folder successfully created."
        elif item == "failed_to_create_folder":
            message = "Failed to create the folder."
        print(message)
