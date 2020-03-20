from core.misc.dhvm_handler import DhvmHandler


class DaoHandler:
    """
    Description
    -----------
    Create a dao file with this command
    It automatically creates a test file inside 'tests'

    Usage
    -----
    -> dao <filename>
    Create a dao file inside the package 'dao'

    -> dao <filename> <destination_package_inside_dao_package>
    Create a dao file inside a dao sub-package (will be created if it is missing)

    Example
    -------
    Assume you want to create "my_module.py" inside the package dao
    -> dao my_module.py
    Creation

    Assume you want to create "my_module.py" inside the non existent package dao.new.pack
    -> dao my_module new.pack
    Creation
    """
    def __init__(self, target, arg):
        DhvmHandler(target, arg, "dao")