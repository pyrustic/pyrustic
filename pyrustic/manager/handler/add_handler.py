from pyrustic.manager.misc import funcs
import os
import os.path
import pkgutil


class AddHandler:
    """
    Description
    -----------
    Use this command to add a file, a package or a regular folder
    to the Target.
    Pyrustic Manager will assume that files with extension ".py"
    are modules.
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

    - Description: Add a file to the Target's APP_DIR
    - Command: add ./ <file.ext>

    - Description: Add a module to the Target's APP_DIR
    - Command: add . <file.py>

    Note: The destination is either a relative path to the
    Target's APP_DIR, or a package name.
    Also, only SLASH is allowed in the path as separator.

    Example
    -------
    - Description: Add a module
    - Preliminary: Assume you want to add "my_view.py"
    to the package 'demo.view'
    - Command: add demo.view my_view.py

    - Description: Add a package
    - Preliminary: Assume you want to add 'my.new.package'
    - Command: add my.new.package

    Note: Please use simple or double quotes as delimiters if a
    string contains space
    """
    def __init__(self, target,
                 app_pkg, args):
        self._target = target
        self._app_pkg = app_pkg
        self._args = args
        self._process(target, app_pkg, args)

    def _process(self, target, app_pkg, args):
        if not target:
            self._print_catalog("missing_target")
            return
        if not app_pkg:
            print("Please init the project first. Check 'help init'.")
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
        # creating file
        class_name = funcs.module_name_to_class(filename)
        path = funcs.package_name_to_path(target, package_name)
        path = os.path.join(path, filename)
        if os.path.exists(path):
            self._print_catalog("module_exists", module=filename)
            return True
        resource_prefix = "manager/template/"
        if not self._app_pkg:
            self._print_catalog("module_created", module=filename)
            return True
        with open(path, "wb") as file:
            if package_name.startswith("{}.view".format(self._app_pkg)):
                resource = resource_prefix + "view_template.txt"
                data = pkgutil.get_data("pyrustic", resource).decode("utf-8")
                data = data.format(app_pkg=self._app_pkg,
                                   class_name=class_name)
                file.write(data)
            else:
                print("HEEEREE !!!!")
                resource = resource_prefix + "module_template.txt"
                data = pkgutil.get_data("pyrustic", resource).decode("utf-8")
                data = data.format(app_pkg=self._app_pkg,
                                   class_name=class_name)
                file.write(data)
            self._print_catalog("module_created", module=filename)
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
