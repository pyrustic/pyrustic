from core.misc.dhvm_handler import DhvmHandler


class MiscHandler:
    """
    Description
    -----------
    Create a dao file with this command
    It automatically creates a test file inside 'tests'

    Usage
    -----
    -> misc <filename>
    Create a misc file inside the package 'misc'

    -> misc <filename> <destination_package_inside_misc_package>
    Create a misc file inside a misc sub-package (will be created if it is missing)

    Example
    -------
    Assume you want to create "my_module.py" inside the package misc
    -> misc my_module.py
    Creation

    Assume you want to create "my_module.py" inside the package misc.new.pack
    -> misc my_module new.pack
    Creation
    """
    def __init__(self, target, arg):
        DhvmHandler(target, arg, "misc")