import sys
import subprocess
import os
import os.path
import about
from tempfile import TemporaryDirectory
import shutil
import fnmatch
from pyrustic import pymisc
from common.lite_test_runner import LiteTestRunner
from pyrustic.jasonix import Jasonix


class BuildHandler:
    """
    Description
    -----------
    Use this command to build an asset that could
    be published later with Hub.
    This command will block the Pyrustic Manager.

    Note: this command will read the json files:
    - ROOT_DIR/pyrustic_data/about.json: to extract
    the version;
    - and ROOT_DIR/pyrustic_data/build.json

    Usage
    -----
    - Description: Build
    - Command: build
    """
    def __init__(self, target):
        self._target = target
        self._jasonix_about = None
        self._jasonix_build = None
        self._tempfile = None
        self._cached_target = None
        self._asset_path = None
        self._process(target)

    def _process(self, target):
        if target is None:
            print("Please link a Target first. Check 'help target'.")
            return
        self._check_json_files()
        # get confirmation
        message = "You are going to build the target project\nDo you really want to continue ?"
        if not self._ask_for_confirmation(message):
            return
        # run prolog script + cache the project by following exclusion rules
        if not self._do_prolog():
            return
        # run act_1 script + run the tests
        if not self._do_act_1():
            return
        # package the project + move it to $TARGET/pyrustic_data/dist
        if not self._do_act_2():
            return
        # run epilog script
        if not self._do_epilog():
            return
        print("\n{}\nSuccessfully built !".format(self._asset_path))

    def _check_json_files(self):
        pyrustic_data_folder = os.path.join(self._target, "pyrustic_data")
        if not os.path.exists(pyrustic_data_folder):
            os.mkdir(pyrustic_data_folder)
        # about.json
        about_json = os.path.join(pyrustic_data_folder, "about.json")
        default_about_json = os.path.join(about.ROOT_DIR, "common",
                                          "default_json_data",
                                          "default_about.json")
        self._jasonix_about = Jasonix(about_json, default=default_about_json)

        # build.json
        build_json = os.path.join(pyrustic_data_folder, "build.json")
        default_build_json = os.path.join(about.ROOT_DIR, "common",
                                          "default_json_data",
                                          "default_build.json")
        self._jasonix_build = Jasonix(build_json, default=default_build_json)

    def _do_prolog(self):
        # find prolog script
        prolog = self._jasonix_build.data.get("prolog")
        if prolog:
            print("Running Prolog...")
            data = self._execute_script(prolog, args=[self._target])
            is_success, error, return_code = data
            if not is_success:
                print(error)
                return
            if return_code != 0:
                print("The Prolog returned with a non-zero code.")
                print("Building interrupted !")
                return False
            print("Done")
        # cache the project
        data = self._cache_the_target()
        print("\nCaching the target project...")
        is_success, self._tempfile, self._cached_target = data
        if not is_success:
            print("Failed to cache the target project")
            return False
        print("Done")
        return True

    def _do_act_1(self):
        # find act_1 script
        act_1 = self._jasonix_build.data.get("act_1")
        if act_1:
            print("\nRunning Act I ...")
            args = [self._target, self._cached_target]
            data = self._execute_script(act_1, args=args)
            is_success, error, return_code = data
            if not is_success:
                print(error)
                return
            if return_code != 0:
                print("Act 1 returned with a non-zero code.")
                print("Building interrupted !")
                return False
            print("Done")
        # test
        if not self._ask_for_confirmation("\nDo you want to run tests ?"):
            print("Cancelled")
            return True
        print("Running tests")
        test_exist, test_success, test_result = self._test_runner()
        if not test_exist:
            print("There aren't Tests")
            return True
        if test_success:
            print("Testing passed")
            return True
        else:
            print("Testing failed")
            print(test_result)
            return False

    def _do_act_2(self):
        # find act_1 script
        act_2 = self._jasonix_build.data.get("act_2")
        if act_2:
            print("\nRunning Act II ...")
            args = [self._target, self._cached_target]
            data = self._execute_script(act_2, args=args)
            is_success, error, return_code = data
            if not is_success:
                print(error)
                return False
            if return_code != 0:
                print("Act 2 returned with a non-zero code.")
                print("Building interrupted !")
                return False
            print("Done")
        # package !
        print("\nPackaging...")
        self._asset_path, zip_error = self._package_cached_target()
        result = False
        if not self._asset_path:
            print("Failed to package")
            print(zip_error if zip_error else "")
            result = False
        else:
            print("Done")
            result = True
        # cleanup
        if self._tempfile:
            self._tempfile.cleanup()
        return result

    def _do_epilog(self):
        # find act_1 script
        epilog = self._jasonix_build.data.get("epilog")
        if epilog and os.path.exists(self._asset_path):
            print("\nRunning Epilog...")
            args = [self._target, self._asset_path]
            data = self._execute_script(epilog, args=args)
            is_success, error, return_code = data
            if not is_success:
                print(error)
                return
            if return_code != 0:
                print("Epilog returned with a non-zero code.")
                print("Building interrupted !")
                return False
            print("Done")
        return True

    def _execute_script(self, script, args=None):
        args = [] if args is None else args
        if not sys.executable:
            error = "Cannot run the script. Unavailable Python interpreter"
            return False, error, None
        path = pymisc.convert_dotted_path(self._target,
                                          script,
                                          suffix=".py")
        if not os.path.exists(path):
            return False, "Missing script", None
        p = subprocess.Popen([sys.executable, "-m", script, *args],
                             cwd=self._target)
        p.communicate()
        return True, None, p.returncode

    def _cache_the_target(self):
        """ Cache the target in a folder named as the project name,
        inside a temp folder.
        Return bool is_success, tempfile """
        # == cache
        tmp_cache_tempfile = TemporaryDirectory()
        tmp_cache_path = tmp_cache_tempfile.name
        # == cache the target project
        cached_target_path = os.path.join(tmp_cache_path,
                            self._get_project_name())
        exclusion_file_path = self._jasonix_build.data.get("exclusion", None)
        paths_to_exclude = self._parse_exclusion_file(exclusion_file_path)
        result = self._copy_project_to_temp(cached_target_path, paths_to_exclude)
        if not result:
            tmp_cache_tempfile.cleanup()
            return False, None
        return True, tmp_cache_tempfile, cached_target_path

    def _parse_exclusion_file(self, path):
        paths_to_exclude = []
        if not path:
            return paths_to_exclude
        path = path.replace("./", "", 1) if path.startswith("./") else path
        path = os.path.join(self._target, path)
        if not os.path.exists(path):
            return paths_to_exclude
        with open(path, "r") as file:
            cache = file.readlines()
            for line in cache:
                line = line.strip()
                if line.startswith("#"):  # comment line
                    continue
                paths_to_exclude.append(line)
        return paths_to_exclude

    def _copy_project_to_temp(self, temp_cache, paths_to_exclude):
        ignore_func = (lambda directory, contents, self=self,
                              root=self._target,
                              paths_to_exclude=paths_to_exclude:
                                self._ignore_func(directory, contents,
                                                  root, paths_to_exclude))
        try:
            shutil.copytree(self._target, temp_cache, ignore=ignore_func)
        except Exception as e:
            return False
        return True

    def _ignore_func(self, directory, contents, root="", ignore_patterns=None):
        ignore_patterns = [] if not ignore_patterns else ignore_patterns
        exclude = []
        patterns_with_root = []
        patterns_without_root = []
        for pattern in ignore_patterns:
            if pattern.startswith("./"):
                cache = os.path.join(root, pattern.replace("./", "", 1))
                patterns_with_root.append(cache)
            else:
                patterns_without_root.append(pattern)
        for content in contents:
            content_with_root = os.path.join(directory, content)
            # check in patterns with root
            for pattern in patterns_with_root:
                if fnmatch.fnmatch(content_with_root, pattern):
                    exclude.append(content)
        # check in patterns without root
        for pattern in patterns_without_root:
            exclude.extend(fnmatch.filter(contents, pattern))
        return set(exclude)

    def _get_project_name(self):
        name = self._jasonix_about.data.get("project_name")
        return os.path.basename(self._target) if not name else name

    def _test_runner(self):
        test_path = os.path.join(self._cached_target, "tests")
        test_success = True
        test_result = None
        test_exist = False
        if os.path.exists(test_path):
            test_exist = True
            test_host = LiteTestRunner(test_path, self._cached_target)
            test_success, test_result = test_host.run()
        return test_exist, test_success, test_result

    def _package_cached_target(self):
        src = self._tempfile.name
        dest = os.path.join(self._target, "pyrustic_data", "dist")
        if not os.path.exists(dest):
            os.makedirs(dest)
        archive_format = "zip"
        self._jasonix_about.reload()
        version = self._jasonix_about.data.get("version", "0.0.1")
        if os.path.exists(os.path.join(dest,
                                       "{}.{}".format(version,
                                                      archive_format))):
            return None, "This package already exists"
        asset_path, zip_error = pymisc.make_archive(version, src,
                                                    dest, format=archive_format)
        return asset_path, zip_error

    def _ask_for_confirmation(self, message):
        cache = input("{} (y/N): ".format(message))
        if cache.lower() == "y":
            return True
        return False
