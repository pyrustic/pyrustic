from pyrustic import manager


class AddHandler:
    """
    Description
    -----------
    Use this command to add an empty file, a package or a regular
    folder to the Target.

    Usage
    -----
    - Description: Add a package
    - Command: add <my.pack.age>

    - Description: Add a module
    - Command: add <destination> <file.py>

    - Description: Add multiple files
    - Command: add <destination> <file_1.ext> <file_2.ext>

    - Description: Add a file to the Target's APP_DIR
    - Command: add ./ <file.ext>

    Note: The destination is either a relative path to the
    Target's PROJECT_DIR, or a package name.

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
    string contains space.
    """
    def __init__(self, target,
                 app_pkg, *args):
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
        manager.add(target, package_or_folder_name, *args[1:])
        print("Success !")

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
