from misc import funcs
import about
from misc import constants
import os.path


INSERTION_SQL = "INSERT INTO path (id, val) VALUES (1, ?)"
UPDATE_SQL = "UPDATE path SET val=? WHERE id=1"
SELECTION_SQL = "SELECT * FROM path WHERE id=1"


class TargetHandler:
    """
    Description
    -----------
    Use this command to set a new Target or to check the current Target.
    If your Target is an empty directory, Pyrustic Manager will automatically
    add the packages 'dao', 'host' and 'view' in addition to the standard
    files/dirs.
    Else, if your Target is not an empty directory, Pyrustic Manager will
    only add standard files/dirs.

    Usage
    -----
    - Description: Set a Target
    - Command: target <path_to_folder>

    - Description: Set the current working directory as Target
    - Command: target .

    - Description: Check current Target (+ additional info)
    - Command: target

    Example
    -------
    - Description: Target 'my_project'
    - Preliminary: Assume 'my_project' lives at '/home/user/projects'
    - Command: target /home/user/projects/my_project

    - Description: Target 'my_project'
    - Preliminary: Assume 'my_project' lives at '/home/user/secret projects'
    - Command: target "/home/user/secret projects/my_project"

    - Description: Target 'my_project'
    - Preliminary: Assume 'my_project' is the current working directory
    - Command: target .

    Note: Please use simple or double quotes if a string contains space
    """
    def __init__(self, current_target, args, dao):
        self._args = args
        self._dao = dao
        self._target = self._process(current_target, args)

    @property
    def target(self):
        return self._target

    def _process(self, current_target, args):
        cache = current_target
        # == case: no arg
        if not args:
            if current_target is None:
                cache = self._get_previously_saved_path()
            cache = self._show_target_info(cache)
            if cache is None:
                self._print_catalog("none")
        # == case: 1 arg
        elif len(args) == 1:
            candidate_target = os.path.realpath(args[0])
            cache = self._open_target(current_target, candidate_target)
        # == case: multiple args
        else:
            self._print_catalog("invalid_request")
        return cache

    def _get_previously_saved_path(self):
        data = self._dao.query(SELECTION_SQL)
        if not data[1]:
            return None
        else:
            return data[1][0][1]

    def _show_target_info(self, target):
        if target is None:
            return None
        if not funcs.valid_target(target):
            return None
        self._print_catalog("info_target",
                            target=target,
                            version=funcs.get_target_version(target))
        return target

    def _open_target(self, current_target, candidate_target):
        if not os.path.isdir(candidate_target):
            self._print_catalog("invalid_target")
            return current_target
        if not funcs.valid_target(candidate_target):
            if self._build_target(candidate_target):
                self._save_path(candidate_target)
                return candidate_target
            return current_target
        if self._show_target_info(candidate_target) is None:
            return current_target
        self._save_path(candidate_target)
        return candidate_target

    def _build_target(self, path):
        # if dir is empty
        if not len(os.listdir(path)):
            elements = [*constants.PYRUSTIC_PROJECT_STRUCT,
                        *constants.PYRUSTIC_PROJECT_OPTIONAL_STRUCT]
        else:
            elements = [*constants.PYRUSTIC_PROJECT_STRUCT]
        self._print_catalog("announce_install")
        answer = input("Do you confirm ? (y/n): ")
        if answer != "y":
            self._print_catalog("cancelled")
            return False
        return self._install_into_target(path, elements=elements)


    def _install_into_target(self, path, elements=[]):
        for element in elements:
            self._print_catalog("installing", element = element)
            if element in ("pyrustic", "about.py"):
                src = os.path.join(about.ROOT_DIR, element)
                dest = os.path.join(path, element)
                if not funcs.copyto(src, dest):
                    self._print_catalog("failed_install", element=element)
                    return False
            elif element in ("tests", "dao", "host", "view", "misc"):
                if funcs.build_package(path, element) is None:
                    return False
            elif element == "cache":
                try:
                    os.mkdir(os.path.join(path, element))
                except Exception as e:
                    self._print_catalog("failed_install", element=element)
                    return False
            elif element == "main.py":
                src = os.path.join(about.ROOT_DIR, "template", element)
                dest = os.path.join(path, element)
                if not funcs.copyto(src, dest):
                    self._print_catalog("failed_install", element=element)
                    return False
            elif element == "script.py":
                src = os.path.join(about.ROOT_DIR, "template", element)
                dest = os.path.join(path, element)
                if not funcs.copyto(src, dest):
                    self._print_catalog("failed_install", element=element)
                    return False
            elif element == "config.ini":
                src = os.path.join(about.ROOT_DIR, "template", element)
                dest = os.path.join(path, element)
                if not funcs.copyto(src, dest):
                    self._print_catalog("failed_install", element=element)
                    return False
        self._print_catalog("success")
        return True


    def _save_path(self, path):
        data = self._dao.query(SELECTION_SQL)
        if not data[1]:
            self._dao.edit(INSERTION_SQL, (path,))
        else:
            self._dao.edit(UPDATE_SQL, (path,))

    def _print_catalog(self, item, **kwargs):
        message = ""
        if item == "none":
            message = "None"
        elif item == "invalid_request":
            message = "Your request isn't valid ! Please check 'help target'."
        elif item == "info_target":
            message ="Target: {}\nFramework version: {}".format(kwargs["target"],
                                                                kwargs["version"])
        elif item == "invalid_target":
            message = "Invalid Target ! The path submitted isn't a directory."
        elif item == "announce_install":
            message = "Pyrustic Framework will be installed in the Target."
        elif item == "cancelled":
            message = "Operation cancelled."
        elif item == "installing":
            message = "  - installing '{}' ...".format(kwargs["element"])
        elif item == "failed_install":
            message = "Failed to install '{}' in the Target !".format(kwargs["element"])
        elif item == "success":
            message = "Success ! Your project is ready !"
        print(message)
