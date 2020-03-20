from core.misc.dhvm_handler import DhvmHandler


class ViewHandler:
    """
    Description
    -----------
    Create a view file with this command
    It automatically creates a test file inside 'tests'

    Usage
    -----
    -> view <filename>
    Create a view file inside the package 'view'

    -> view <filename> <destination_package_inside_view_package>
    Create a view file inside a view sub-package (will be created if it is missing)

    Example
    -------
    Assume you want to create "my_module.py" inside the package view
    -> view my_module.py
    Creation

    Assume you want to create "my_module.py" inside the package view.new.pack
    -> view my_module new.pack
    Creation
    """
    def __init__(self, target, arg):
        DhvmHandler(target, arg, "view")