import about
import os
import os.path
from misc import funcs


class DemoHandler:
    """
    Description
    -----------
    Use this command to build a demo that you could study.

    Usage
    -----
    - Description: Build the demo
    - Command: demo <path_to_empty_directory>

    Example
    -------
    - Description: Build a demo
    - Preliminary: Assume this directory '/home/demo' is empty
    - Command: demo /home/demo

    Note: Please use simple or double quotes as delimiters if a string
    contains space
    """
    def __init__(self, args):
        self._process(args)

    def _process(self, args):
        if not args:
            self._print_catalog("missing_demo")
            return
        demo_path = args[0]
        if not os.path.isdir(demo_path) or len(os.listdir(demo_path)) != 0:
            self._print_catalog("bad_demo_path")
            return
        zipped_demo_path = os.path.join(about.ROOT_DIR, "misc", "demo")
        val = funcs.unzip_to(zipped_demo_path, demo_path)
        if val:
            self._print_catalog("ready_demo", demo=demo_path)
        else:
            self._print_catalog("failed")

    def _print_catalog(self, item, **kwargs):
        message = ""
        if item == "missing_demo":
            message = "Please link a demo path first. Check 'help demo'."
        if item == "bad_demo_path":
            message = "You should submit an empty directory as demo path."
        elif item == "running":
            message = "Running '{}' ...".format(kwargs["module"])
        elif item == "ready_demo":
            message = "Demo successfully built.\nDemo at: {}".format(kwargs["demo"])
        elif item == "failed":
            message = "Failed to build the demo."
        print(message)