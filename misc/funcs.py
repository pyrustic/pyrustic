import os
import os.path
import shutil
from zipfile import ZipFile
from misc import constants


def valid_target(path):
    # return True if target is a valid Pyrustic-like project
    if not os.path.isdir(path):
        return False
    actual_elements = os.listdir(path)
    for element in constants.PYRUSTIC_PROJECT_STRUCT:
        if element not in actual_elements:
            return False
    return True


def get_target_version(path):
    """returns a version from a file living in pyrustic folder that
     follows: pyrustic_version_<version>
    else returns None"""
    cache = ""
    for element in os.listdir(os.path.join(path, "pyrustic")):
        if element.startswith("pyrustic_version_"):
            cache = element
            break
    version = None
    splitted = cache.split("_")
    if len(splitted) != 3:
        pass
    elif splitted[0] == "pyrustic" and splitted[1] == "version":
        version = splitted[2]
    return version


def copyto(src, dest):
    """
    Please make sure that DEST doesn't exist yet !
    Copy a file or directory (src) to a destination folder (dest)
    """
    if not os.path.exists(src) or os.path.exists(dest):
        return False
    if os.path.isdir(src):
        try:
            shutil.copytree(src, dest)
        except Exception as e:
            return False
    else:
        try:
            shutil.copy2(src, dest)
        except Exception as e:
            return False
    return True


def moveto(src, dest):
    """
    Please make sure that DEST doesn't exist yet !
    Move a file or directory (src) to a destination folder (dest)
    """
    if not os.path.exists(src) or os.path.exists(dest):
        return False
    try:
        shutil.move(src, dest)
    except Exception as e:
        return False
    return True


def split_arg(arg):
    """
    Split the string arg. Delimiters are space, simple and double quotes
    """
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


def package_name_to_path(target, package_name, prefix=""):
    # returns a dotted package name to a regular pathname
    # example: package_name_to_path("/home/proj", "view.lol", prefix="tests.")
    return os.path.join(target, *((prefix + package_name).split(".")))


def build_package(target, package_name, prefix=""):
    """
    Literally build a package, returns None or the string pathname
    package represented by prefix must already exist
    """
    splitted = package_name.split(".")
    dir = package_name_to_path(target, prefix) if prefix else target
    for item in splitted:
        dir = os.path.join(dir, item)
        if os.path.exists(dir):
            continue
        try:
            os.mkdir(dir)
            with open(os.path.join(dir, "__init__.py"), "w") as file:
                pass
        except Exception as e:
            return None
    if not os.path.isdir(dir):
        return None
    return dir


def module_name_to_class(module_name):
    """
    Convert a module name like my_module.py to a class name like MyModule
    """
    name = os.path.splitext(module_name)[0]
    # ...
    if not "_" in name:
        return strictly_capitalize(name)
    else:
        splitted = name.split("_")
        cache = []
        for x in splitted:
            cache.append(strictly_capitalize(x))
        return "".join(cache)

def strictly_capitalize(string):
    return string[0].upper() + string[1:]

def get_root_from_package(package_name):
    """
    Return the root from a dotted package name.
    Example the root here "my.package.is.great" is "my".
    """
    splitted = package_name.split(".")
    root = None
    for x in splitted:
        if x == "" or x.isspace():
            continue
        root = x
        break
    return root


def unzip_to(src, dest):
    """
    Please make sure that DEST does exist yet !
    Unzip an archive (src) into a location (dest)
    """
    if not os.path.isfile(src) or not os.path.exists(dest):
        return False
    #os.mkdir(dest)
    with ZipFile(src, 'r') as zip:
        # Extract all the contents of zip file in different directory
        try:
            zip.extractall(dest)
        except Exception as e:
            #shutil.rmtree(dest)
            return False
    return True
