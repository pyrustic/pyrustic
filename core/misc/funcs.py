import os.path
import os
import shutil
import time
from zipfile import ZipFile


def package_name_to_path(target, package_name, prefix=""):
    return os.path.join(target, *((prefix + package_name).split(".")))

def module_name_to_class(module_name):
    name = os.path.splitext(module_name)[0]
    # ...
    if not "_" in name:
        return name.capitalize()
    else:
        splitted = name.split("_")
        cache = []
        for x in splitted:
            cache.append(x.capitalize())
        return "".join(cache)

def build_package(target, package_name, prefix=""):
    """
    package represented by prefix must already exist
    """
    splitted = package_name.split(".")
    dir = package_name_to_path(target, prefix) if prefix else target
    for item in splitted:
        dir = os.path.join(dir, item)
        if os.path.exists(dir):
            continue
        os.mkdir(dir)
        with open(os.path.join(dir, "__init__.py"), "w") as file:
            pass
    return dir

def backup_current_version(root):
    dest = os.path.join(root, "cache", "rollback")
    # delete current rollback folder
    if os.path.isdir(dest):
        try:
            shutil.rmtree(dest)
        except Exception as e:
            pass
    try:
        os.mkdir(dest)
    except Exception as e:
        return False
    for item in os.listdir(root):
        if item in ("archive", "cache"):
            continue
        src = os.path.join(root, item)
        try:
            shutil.move(src, dest)
        except Exception as e:
            return False
    return True

def install_version(root, path):
    if not os.path.isfile(path):
        return False
    # Extract in temporary
    basename = os.path.basename(path)
    cache_folder = os.path.splitext(basename)[0] + "_" + str(int(time.time()))
    cache_folder = os.path.join(root, "cache", cache_folder)
    os.mkdir(cache_folder)
    with ZipFile(path, 'r') as zip:
        # Extract all the contents of zip file in different directory
        try:
            zip.extractall(cache_folder)
        except Exception as e:
            shutil.rmtree(cache_folder)
            return False
    for item in os.listdir(cache_folder):
        if item in ("archive", "cache"):
            continue
        src = os.path.join(cache_folder, item)
        if os.path.isdir(src):  # is dir
            try:
                shutil.copytree(src, os.path.join(root, item))
            except Exception as e:
                shutil.rmtree(cache_folder)
                return False
        elif os.path.isfile(src):  # is file
            try:
                shutil.copy2(src, root)
            except Exception as e:
                shutil.rmtree(cache_folder)
                return False
    shutil.rmtree(cache_folder)
    return True

def path_to_highest_build_of_version(root, version):
    results = []
    cache = None
    for item in os.listdir(os.path.join(root, "archive")):
        item = os.path.splitext(item)[0]
        splitted = item.split("_")
        if len(splitted) == 4:
            if splitted[1] == version:
                results.append(splitted)
    for item in results:
        if not cache:
            cache = item
            continue
        try:
            if int(item[3]) > int(cache[3]):
                cache = item
        except Exception as e:
            pass
    if cache:
        cache = os.path.join(root, "archive", ("_".join(cache)) + ".zip")
    return cache

def path_to_version_or_build(root, arg):
    is_build_number = True
    if "." in arg:
        is_build_number = False
    if not is_build_number:  # Version
        return path_to_highest_build_of_version(root, arg)
    for item in os.listdir(os.path.join(root, "archive")):  # Build
        item = os.path.splitext(item)[0]
        splitted = item.split("_")
        if len(splitted) == 4:
            if splitted[3] == arg:
                return os.path.join(root, "archive", item + ".zip")
    return None

def get_version_build_from_release(path):
    """returns a version and build if name follows pyrustic_<version>_build_<build>
    else returns None None"""
    version = None
    build = None
    basename = os.path.basename(path)
    basename_without_extension = os.path.splitext(basename)[0]
    splitted = basename_without_extension.split("_")
    if len(splitted) != 4:
        pass
    elif splitted[0] == "pyrustic" and splitted[2] == "build":
        version = splitted[1]
        build = splitted[3]
    return version, build

def split_arg(arg):
    args = []
    cache = ""
    simple_quote_on = False
    double_quote_on = False
    collect_cache = False
    for char in arg:
        # Quotes stuff
        if char == "'":  # simple quote
            collect_cache = True
            simple_quote_on = False if simple_quote_on else True
        elif char == '"':  # double quote
            collect_cache = True
            double_quote_on = False if double_quote_on else True
        # space stuff
        elif char == " " and (not simple_quote_on and not double_quote_on):
            collect_cache = True
        else:
            cache += char
        # caching
        if collect_cache:
            collect_cache = False
            if cache:
                args.append(cache)
                cache = ""
    if cache:
        args.append(cache)
    return args
