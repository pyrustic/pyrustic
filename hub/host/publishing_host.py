from pyrustic.gurl import dict_to_json_body
from pyrustic.jasonix import Jasonix
from pyrustic import pymisc
from common import constants
from common.funcs import get_hub_url
from hub.host.test_host import TestHost
import urllib.parse
import os
import os.path
import shutil
import fnmatch
import about
import tempfile


class PublishingHost:
    def __init__(self, gurl, target_project, owner, repo,
                 run_tests=True, run_scripts=True):
        self._gurl = gurl
        self._target_project = target_project
        self._owner = owner
        self._repo = repo
        self._run_tests = run_tests
        self._run_scripts = run_scripts

    def publishing(self, name, tag_name,
                 target_commitish, description, prerelease,
                 asset_name, asset_label):
        """
        Return {"meta_code":, "status_code", "status_text", "data"}
        meta code:
            0- success
            1- failed to cache the target project
            2- tests failed (check 'data')
            3- failed to execute prolog (check 'data')
            4- failed to zip (check 'data')
            5- failed to create release (check 'status_code', 'status_text')
            6- failed to upload zip (check 'status_code', 'status_text')
            7- failed to execute epilog (check 'data')
        """
        publishing_result = {"meta_code": None, "status_code": None,
                            "status_text": None, "data": None}
        config = self._get_publishing_config()
        # == publishing cache
        publishing_cache_tempfile = tempfile.TemporaryDirectory()
        publishing_cache_path = publishing_cache_tempfile.name
        # == cache the target project
        cached_target_path = os.path.join(publishing_cache_path,
                                          "uncompressed", self._repo)
        exclusion_file_path = config.get("exclusion", None)
        paths_to_exclude = self._parse_exclusion_file(exclusion_file_path)
        result = self._copy_project_to_temp(cached_target_path, paths_to_exclude)
        if not result:
            publishing_result["meta_code"] = 1
            publishing_cache_tempfile.cleanup()
            return publishing_result
        # == run tests (from the cache dir)
        if self._run_tests:
            test_success, test_result = self._test_runner(cached_target_path)
            if not test_success:
                publishing_result["meta_code"] = 2
                publishing_result["data"] = test_result
                publishing_cache_tempfile.cleanup()
                return publishing_result
        # == store publishing form data into publishing_form.json
        form_data = self._store_publishing_form_data(publishing_cache_path,
                                                   target_commitish,
                                                   tag_name,
                                                   name,
                                                   asset_name,
                                                   asset_label,
                                                   description,
                                                   prerelease)
        # == execute prolog (from the target root dir)
        if self._run_scripts:
            prolog = config.get("prolog", None)
            s_exit, s_stdout, s_stderr = self._exec_script(prolog,
                                                           cached_target_path,
                                                           form_data)
            if s_exit != 0:
                publishing_result["meta_code"] = 3
                text = "Exit code: {}\n{}\n{}".format(s_exit, s_stdout, s_stderr)
                publishing_result["data"] = text
                publishing_cache_tempfile.cleanup()
                return publishing_result
        # zip (from the cache dir)
        zip_src = os.path.dirname(cached_target_path)
        zip_dest = publishing_cache_path
        asset_path, zip_error = pymisc.make_archive(asset_name, zip_src,
                                                    zip_dest)
        if not asset_path:
            publishing_result["meta_code"] = 4
            publishing_result["data"] = zip_error
            publishing_cache_tempfile.cleanup()
            return publishing_result
        # == create release
        response = self._create_release(self._owner, self._repo, name, tag_name,
                                        target_commitish, description,
                                        prerelease)
        code = response.code
        if code != 201:
            publishing_result["meta_code"] = 5
            publishing_result["status_code"] = code
            publishing_result["status_text"] = response.status[1]
            publishing_cache_tempfile.cleanup()
            return publishing_result
        # == upload zip
        upload_url = response.json["upload_url"]
        response = self._upload_release_asset(upload_url, asset_path,
                                              asset_name, asset_label)
        code = response.code
        if code != 201:
            publishing_result["meta_code"] = 6
            publishing_result["status_code"] = code
            publishing_result["status_text"] = response.status[1]
            publishing_cache_tempfile.cleanup()
            return publishing_result
        # == execute epilog (from the cache dir)
        if self._run_scripts:
            epilog = config.get("epilog", None)
            s_exit, s_stdout, s_stderr = self._exec_script(epilog,
                                                           cached_target_path,
                                                           form_data)
            if s_exit != 0:
                publishing_result["meta_code"] = 7
                text = "Exit code: {}\n{}\n{}".format(s_exit, s_stdout, s_stderr)
                publishing_result["data"] = text
                publishing_cache_tempfile.cleanup()
                return publishing_result
        publishing_result["meta_code"] = 0
        publishing_cache_tempfile.cleanup()
        return publishing_result

    def _publishing(self, name, tag_name,
                 target_commitish, description, prerelease,
                 asset_path, asset_name, asset_label):

        response = self._create_release(self._owner, self._repo, name, tag_name,
                                        target_commitish, description,
                                        prerelease)
        code = response.code
        if code == 201:
            upload_url = response.json["upload_url"]
            response = self._upload_release_asset(upload_url, asset_path,
                                                  asset_name, asset_label)
        return response.status

    def _create_release(self, owner, repo, name, tag_name, target_commitish,
                        description, prerelease):
        res = "/repos/{}/{}/releases".format(owner, repo)
        body = {"tag_name": tag_name, "target_commitish": target_commitish,
                "name": name, "body": description, "draft": False,
                "prerelease": prerelease}
        body = dict_to_json_body(body)
        response = self._gurl.request(get_hub_url(res), body=body, method="POST")
        return response

    def _upload_release_asset(self, upload_url, path, name, label):
        name = "{}.zip".format(name)
        url = upload_url.replace("{?name,label}", "?{}")
        parameters = urllib.parse.urlencode({"label": label, "name": name})
        url = url.format(parameters)
        with open(path, "rb") as file:
            data = file.read()
        header = ("Content-Type", "application/zip")
        response = self._gurl.request(url, body=data, method="POST",
                                      headers=(header, ))
        return response

    def _get_publishing_cache(self):
        hub_cache_path = constants.HUB_CACHE_FOLDER
        publishing_cache = os.path.join(hub_cache_path, "publishing")
        return publishing_cache

    def _get_publishing_config(self):
        project_pyrustic_data_path = os.path.join(self._target_project, ".pyrustic_data")
        if not os.path.exists(project_pyrustic_data_path):
             return []
        project_publishing_path = os.path.join(project_pyrustic_data_path,
                                               "hub", "publishing.json")
        default_publishing_path = os.path.join(about.ROOT_DIR, "common",
                                             "default_json_data",
                                             "default_publishing.json")
        jasonix = Jasonix(project_publishing_path, default=default_publishing_path)
        return jasonix.data

    def _copy_project_to_temp(self, temp_cache, paths_to_exclude):
        ignore_func = (lambda dir, contents, self=self,
                              root=self._target_project,
                              paths_to_exclude=paths_to_exclude:
                                self._ignore_func(dir, contents, root, paths_to_exclude))
        try:
            shutil.copytree(self._target_project, temp_cache, ignore=ignore_func)
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

    def _test_runner(self, cached_target_path):
        test_path = os.path.join(cached_target_path, "tests")
        test_success = True
        test_result = None
        if os.path.exists(test_path):
            test_host = TestHost(test_path, cached_target_path)
            test_success, test_result = test_host.run()
        return test_success, test_result

    def _exec_script(self, script, cached_target_path, form_data):
        if script is None:
            return 0, None, None
        if script is not None:
            script = script.replace("./", "", 1) if script.startswith("./") else script
            command = [script, cached_target_path, self._gurl.token, form_data]
            try:
                script_result = pymisc.py_script(command, cwd=self._target_project)
            except Exception as e:
                return 1, "", str(e)
            script_exit_code = script_result[0]
            script_stdout = "".join(script_result[1])
            script_stderr = "".join(script_result[2])
            return script_exit_code, script_stdout, script_stderr

    def _parse_exclusion_file(self, path):
        paths_to_exclude = []
        if not path:
            return paths_to_exclude
        path = path.replace("./", "", 1) if path.startswith("./") else path
        path = os.path.join(self._target_project, path)
        if not os.path.exists(path):
            return paths_to_exclude
        with open(path, "r") as file:
            cache = file.readlines()
            for line in cache:
                line = line.strip()
                if line.startswith("###"):  # comment line
                    continue
                paths_to_exclude.append(line)
        return paths_to_exclude

    def _store_publishing_form_data(self,
                                  publishing_cache_path,
                                  target_commitish,
                                  tag_name,
                                  name,
                                  asset_name,
                                  asset_label,
                                  description,
                                  pre_release):
        publishing_form_data_path = os.path.join(publishing_cache_path,
                                                 "publishing_form.json")
        default_publishing_form_data_path = os.path.join(about.ROOT_DIR,
                                                       "common",
                                                       "default_json_data",
                                                       "default_publishing_form.json")
        jasonix = Jasonix(publishing_form_data_path,
                          default=default_publishing_form_data_path)
        jasonix.data["owner"] = self._owner
        jasonix.data["repository"] = self._repo
        jasonix.data["target_commitish"] = target_commitish
        jasonix.data["tag_name"] = tag_name
        jasonix.data["release_name"] = name
        jasonix.data["archive_format"] = "zip"
        jasonix.data["asset_name"] = asset_name
        jasonix.data["asset_label"] = asset_label
        jasonix.data["description"] = description
        jasonix.data["run_tests"] = self._run_tests
        jasonix.data["pre_release"] = pre_release
        jasonix.save()
        return publishing_form_data_path
