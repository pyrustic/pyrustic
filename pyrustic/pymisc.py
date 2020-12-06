import subprocess
import sys
import os
import os.path
import about
import shutil
from pyrustic.jasonix import Jasonix


def make_archive(name, src, dest, format="zip"):
    """
    - name is the zipfile name minus extension like 'my_archive_file';
    - src is the root dir of the project to zip like '/path/to/project';
    - dest is the dir where to save the final zip.
    Dest should exist like '/path/to/dest'
    format is "zip" or "tar" or "gztar" or "bztar" or “xztar”. Default to "zip"

    Returns the zipfile path and error. Zipfile could be None or str.
    error could be None or an exception instance
    """
    cache = None
    error = None
    try:
        zipfile = os.path.join(dest, name)
        cache = shutil.make_archive(zipfile, format, root_dir=src, base_dir=".")
    except Exception as e:
        error = e
    return cache, error


def convert_dotted_path(root, dotted_path, prefix="", suffix=""):
    # returns a dotted package name to a regular pathname
    # example: package_name_to_path("/home/proj", "view.lol", prefix="tests.")
    return os.path.join(root, *((prefix + dotted_path).split("."))) + suffix


def tab_to_space(text, tab_size=4):
    TAB = "\t"
    SPACE = " "
    lines = text.split("\n")
    results = []
    for line in lines:
        cache = str()
        for char in line:
            if char == TAB:
                while len(cache) % tab_size != 0:
                    cache += SPACE
            else:
                cache += char
        results.append(cache)
    return "\n".join(results)


def edit_build_version():
    about_json_path = os.path.join(about.ROOT_DIR, "pyrustic_data",
                                   "about.json")
    if not os.path.exists(about_json_path):
        return
    jasonix = Jasonix(about_json_path)
    current_version = jasonix.data.get("version", "0.0.1")
    message = "The current version is {}".format(current_version)
    print(message)
    message = "Set a new version or ignore: "
    new_version = input(message)
    if not new_version:
        return
    jasonix.data["version"] = new_version
    jasonix.save()

# ========================
#        PRIVATE
# ========================
def _script(command=None, cwd=None, py=True):  # ARCHIVE
    command = [] if not command else command
    command = [sys.executable, *command] if py else command
    p = subprocess.Popen(command,
                         cwd=cwd,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,
                         bufsize=1,
                         universal_newlines=True)
    stdout_data = []
    stderr_data = []
    for line in p.stdout:
        stdout_data.append(line)
    for line in p.stderr:
        stderr_data.append(line)
    p.communicate()
    return p.returncode, stdout_data, stderr_data
