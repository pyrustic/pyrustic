import os
import os.path
import shutil
import about

class SyncHandler:
    """
    Description
    -----------
    Sync the Target with the current version of framework embedded in Pyrustic Platform Shell
    That's like update/upgrade (or downgrade?) your project's framework

    Usage
    -----
    -> sync
    Syncing

    Example
    -------
    Assume the Platform is currently running on version 2.0.0
    Assume the Target project 'my_project' is running on version 1.0.0
    Let upgrade the framework of 'my_project' to version 2.0.0
    -> sync
    Syncing
    """
    def __init__(self, target, arg):
        self._root = about.ROOT_DIR
        self._target = target
        self._basename_without_extension = ""
        self._path_to_zip = None
        self._process(arg)

    def _process(self, arg):
        if len(arg) != 0:
            print("Incorrect command. Please check 'help sync'")
            return
        if not self._target:
            print("Impossible to continue. Set a Target first. Check 'help target'")
            return
        self._sync_target()
        return

    def _sync_target(self):
        target_rollback_path = os.path.join(self._target, "cache", "rollback")  # target
        target_pyrustic_path = os.path.join(self._target, "pyrustic")  # target
        framework_path = os.path.join(self._root, "core", "payload", "pyrustic")  # platform
        # delete current rollback folder inside target folder
        try:
            shutil.rmtree(target_rollback_path)
        except Exception as e:
            pass
        try:
            os.mkdir(target_rollback_path)
        except Exception as e:
            print("Failed: cannot create rollback folder inside Target's cache")
            return
        # backup Target's Pyrustic folder inside 'rollback'
        try:
            shutil.move(target_pyrustic_path, target_rollback_path)
        except Exception as e:
            print("Failed: cannot make a backup of current Target's framework ")
            return
        # copy pyrustic from platform's payload folder to Target pyrustic folder
        try:
            shutil.copytree(framework_path, target_pyrustic_path)
        except Exception as e:
            print("Failed: cannot install framework in Target")
        target_basename = "'" + os.path.basename(self._target) + "'"
        platform_version = about.VERSION
        platform_build = about.BUILD
        print("Successfully switched the framework of", target_basename,
              "to version", platform_version,
              "build", platform_build)
