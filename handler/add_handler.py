from misc import funcs
from misc import constants
import os.path
from template import module_template
from template import dao_template
from template import host_template
from template import view_template
from template import test_template


class AddHandler:
    """
    Description
    -----------
    Use this command to add a file or a package to the Target.
    Pyrustic Manager will assume that files with extension '.py' are modules.
    In this case, the Manager will create a test file and the corresponding
    test package.
    If you are going to add a module in the package 'dao', 'host' or 'view,
    Pyrustic Manager will add your module with the suitable content.

    Usage
    -----
    - Description: Add a file
    - Command: add <destination_package> <file.ext>

    - Description: Add multiple files
    - Command: add <destination_package> <file_1.ext> <file_2.ext>

    - Description: Add a module
    - Command: add <destination_package> <file.py>

    - Description: Add a package
    - Command: add <my.package>

    - Description: Add a file in the Target (ROOT DIR)
    - Command: add . <file.ext>

    Example
    -------
    - Description: Add a module
    - Preliminary: Assume you want to add 'my_view.py' to the package 'view'
    - Command: add view my_view.py

    - Description: Add a package
    - Preliminary: Assume you want to add 'my.new.package'
    - Command: add my.new.package

    Note: Please use simple or double quotes as delimiters if a string
    contains space
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
        # build package
        package_name = args[0]
        if len(args) > 1:
            if not self._handle_package_part(target, package_name, verbose=False):
                return
            self._handle_files_part(target, package_name, args[1:])
        else:
            self._handle_package_part(target, package_name)

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

    def _handle_files_part(self, target, package_name, files):
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

    def _install_module(self, target, package_name, filename):
        # mirror package in tests
        if not self._is_tests_package_built:
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
        with open(path, "w") as file:
            if funcs.get_root_from_package(package_name) == "dao":
                file.write(dao_template.data.format(class_name))
            elif funcs.get_root_from_package(package_name) == "host":
                file.write(host_template.data.format(class_name))
            elif funcs.get_root_from_package(package_name) == "view":
                file.write(view_template.data.format(class_name))
            else:
                file.write(module_template.data.format(class_name))
            self._print_catalog("module_created", module=filename)
        if os.path.exists(test_path):
            return True
        with open(test_path, "w") as file:
            file.write(test_template.data.format(test_class_name))
            self._print_catalog("test_module_created", module=test_filename)
        return True


        for x in constants.PYRUSTIC_PROJECT_OPTIONAL_STRUCT:
            if package_name.startswith("{}.".format(x)):
                print("creation module special", x)

            with open(path, "w") as file:
                pass
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
        path = funcs.package_name_to_path(tests_path, package_name)
        if os.path.exists(path):
            return True
        path = funcs.build_package(tests_path, package_name)
        if path is None:
            self._print_catalog("failed_to_build_tests_package")
            return False
        self._print_catalog("tests_package_built")
        return True

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
        print(message)