import os.path
from pyrustic.gurl import Gurl
from pyrustic.jasonix import Jasonix
from common import constants
from manager.misc import funcs
from common import funcs as common_funcs
import tempfile
import shutil
import about


class UpdateHandler:
    """
    Description
    -----------
    Use this command to update the Pyrustic Suite.
    Make sure that you have an active internet connection.
    The latest release of Pyrustic Suite will be downloaded
    then installed. Your current Pyrustic Suite will be
    moved into the "backup" folder of "PyrusticData".

    Usage
    -----
    - Description: Update
    - Command: update
    """
    def __init__(self, target, args):
        self._target = target
        self._process(args)

    def _process(self, args):
        if self._target is None:
            print("  Please link a Target first !")
            return
        if args:
            print("Wrong usage of this command")
            return
        print("  You are going to update this software suite.")
        data = input("  Do you want to continue ? (y/N): ")
        if data.lower() != "y":
            print("  Cancelled")
            return
        print("  ...")
        if self._update():
            print("  Success ! Please restart the manager.")

    def _update(self):
        # get_gurl
        gurl = self._get_gurl()
        # check latest release
        code, status, url, name = self._check_latest_release(gurl)
        if code not in (200, 304):
            print("  Failed to check latest release !\n  {}".format(status))
            return False
        # download latest release
        cached_release_path, cache_temp = self._download_release(gurl, url, name)
        if cached_release_path is None:
            print("  Failed to download latest release !")
            return False
        if not self._backup_current_version():
            print("  Failed to backup the current version")
            return False
        if not self._pre_install(cached_release_path, cache_temp):
            print("  Failed to pre-install the latest release")
            return False
        return True

    def _get_gurl(self):
        accept_header = ("Accept", "application/vnd.github.v3+json")
        user_agent_header = constants.USER_AGENT
        gurl = Gurl(headers=(accept_header, user_agent_header))
        return gurl

    def _check_latest_release(self, gurl):
        url = None
        name = None
        res = "/repos/{}/{}/releases/latest".format("pyrustic", "pyrustic")
        response = gurl.request(common_funcs.get_hub_url(res))
        code = response.code
        json = response.json
        if code == 304:
            json = response.cached_response.json
        if (code in (200, 304)) and json:
            assets = json["assets"]
            if assets:
                asset = assets[0]
                url = asset["browser_download_url"]
                name = asset["name"]
        return (*response.status, url, name)

    def _download_release(self, gurl, url, name):
        cache_temp = tempfile.TemporaryDirectory()
        cache_path = cache_temp.name
        cached_zip = os.path.join(cache_path, name)
        response = gurl.request(url)
        try:
            with open(cached_zip, "wb") as file:
                file.write(response.body)
        except Exception as e:
            print("rror: ", e)
            cached_zip = None
            cache_temp.cleanup()
            cache_temp = None
        return cached_zip, cache_temp

    def _backup_current_version(self):
        backup_path = os.path.join(constants.PYRUSTIC_DATA_FOLDER,
                                   "suite",
                                   "backup",
                                   about.VERSION)
        if os.path.exists(backup_path):
            try:
                shutil.rmtree(backup_path, ignore_errors=True)
            except Exception as e:
                return False
        src = about.ROOT_DIR
        dest = backup_path
        return funcs.moveto(src, dest)

    def _pre_install(self, cached_release_path, cache_temp):
        src = cached_release_path
        dest = os.path.dirname(about.ROOT_DIR)
        try:
            shutil.unpack_archive(src,
                                  dest,
                                  format="zip")
        except Exception as e:
            return False
        finally:
            cache_temp.cleanup()
        return True
