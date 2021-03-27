import os
import os.path
import math
import shutil
import subprocess
from pyrustic.jasonix import Jasonix


# TODO : refactor pymisc into util, tkmisc into tkutil, then put pyrustic.dist inside pyrustic.app

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


def edit_build_version(app_dir):
    about_json_path = os.path.join(app_dir, "pyrustic_data",
                                   "app.json")
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


def script(cmd, cwd=None, interactive=True):
    """
    Execute a cmd. Cmd is either a list of args or a string.
    Example of commands:
        - "something 'path/to/dir'"
        - ["something", "path/to/dir"]
    """
    if isinstance(cmd, str):
        cmd = parse_cmd(cmd)
    stdin = None if interactive else subprocess.DEVNULL
    stdout = None if interactive else subprocess.DEVNULL
    stderr = None if interactive else subprocess.DEVNULL
    process = subprocess.Popen(cmd, stdin=stdin, stdout=stdout,
                               stderr=stderr, cwd=cwd)
    if not interactive:
        return 0
    process.communicate()
    return process.returncode


def parse_cmd(cmd):
    """
    Split the cmd string. Delimiters are: space, simple and double quotes
    """
    SINGLE_QUOTE = "'"
    DOUBLE_QUOTE = "\""
    ESPACE = " "
    result = []
    cache = ""
    quote_context = None
    collect_cache = False
    for char in cmd:
        if quote_context is None:  # outside a quote context
            if char in (SINGLE_QUOTE, DOUBLE_QUOTE):
                quote_context = char
                collect_cache = True
            elif char == ESPACE:
                collect_cache = True
            else:
                cache += char
        else:  # inside a quote context
            if char == quote_context:
                quote_context = None
                collect_cache = True
            else:
                cache += char
        # cache collection
        if collect_cache:
            collect_cache = False
            if cache:
                result.append(cache)
            cache = ""
    if cache:
        result.append(cache)
    return result


def convert_size(size):
    """ Size should be in bytes.
    Return a tuple (float_or_int_val, str_unit) """
    if size == 0:
        return (0, "B")
    KILOBYTE = 1024
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size, KILOBYTE)))
    p = math.pow(KILOBYTE, i)
    result = round(size/p, 2)
    return (result, size_name[i])


def truncate_str(data, max_size=15, ellipsis="..."):
    val = ((data[:max_size] + ellipsis)
            if len(data) > max_size else data)
    return val
