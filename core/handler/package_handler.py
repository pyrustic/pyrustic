import os.path
import os
from core.template import dao_template
from core.misc import funcs

class PackageHandler:
    """
    Description
    -----------
    Use this command to create a Python package in your project (the Target)

    Usage
    -----
    -> package <package.to.create>
    Creation

    Example
    -------
    Assume you want to create the package 'my.new.package' in the root directory
    -> package my.new.package
    Creation

    Assume you want to create a package 'client.people' inside 'dao'
    -> package dao.client.people
    Creation
    """
    def __init__(self, target, arg):
        self._target = target
        self._process(arg)

    def _process(self, arg):
        if not self._target:
            print("Impossible to continue. Set a Target first")
            return
        if len(arg) == 0:
            print("Incomplete command. Please check 'help package'")
            return
        if len(arg) > 1:
            print("Incorrect command. Please check 'help package'")
            return
        name = arg[0]
        if os.path.exists(funcs.package_name_to_path(self._target, name)):
            print("This package already exists")
            return
        try:
            funcs.build_package(self._target, name)
        except Exception as e:
            print("Error: failed to build package")
        else:
            print("Package successfully built !")
