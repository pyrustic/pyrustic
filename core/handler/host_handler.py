from core.misc.dhvm_handler import DhvmHandler


class HostHandler:
    """
    Description
    -----------
    Create a host file with this command
    It automatically creates a test file inside 'tests'

    Usage
    -----
    -> host <filename>
    Create a host file inside the package 'host'

    -> host <filename> <destination_package_inside_host_package>
    Create a host file inside a host sub-package (will be created if it is missing)

    Example
    -------
    Assume you want to create "my_module.py" inside the package host
    -> host my_module.py
    Creation

    Assume you want to create "my_module.py" inside the package host.new.pack
    -> host my_module new.pack
    Creation
    """
    def __init__(self, target, arg):
        DhvmHandler(target, arg, "host")