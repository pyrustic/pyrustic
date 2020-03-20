import os.path
import os
import shutil
import about
from core.misc import funcs

class MakeHandler:
    """
    Description
    -----------
    Make a new project

    Usage
    -----
    -> make <project_name> <path_where_project_folder_will_be_created>
    Make a new project

    -> make <project_name> .
    Make a new project in current working directory

    Example
    -------
    Assume you want to make 'my_project' in '/home/user/all projects'
    -> make my_project "/home/user/all projects"
    Make a new project

    Note: Please use simple or double quotes if your path string contains space
    """
    def __init__(self, target, arg):
        self._target = target
        self._root = about.ROOT_DIR
        self._process(arg)

    @property
    def target(self):
        return self._target

    def _process(self, arg):
        # Empty arg
        if not arg:
            print("Incomplete command. Please check 'help make'")
            return
        # arg splitted != 2
        if len(arg) != 2:
            print("Incorrect command. Please check 'help make'")
            return
        target = self._verif(arg)
        if not target:
            print("Failed to make the project. Please try again and make sure the project doesn't already exist")
            return
        target = self._make(target)
        if not target:
            print("Error: failed to make the project")
            return
        print("Project successfully created !")
        self._target = target

    def _verif(self, data):
        project_name = data[0]
        path = os.path.abspath(data[1])
        target = os.path.join(path, project_name)
        if os.path.isdir(target): # exists
            target = None
        return target

    def _make(self, target):
        try:
            shutil.copytree(os.path.join(self._root, "core", "payload"), target)
        except Exception as e:
            return None
        return target

