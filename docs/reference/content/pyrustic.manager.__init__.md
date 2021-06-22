
Back to [Reference Overview](https://github.com/pyrustic/pyrustic/blob/master/docs/reference/README.md)

# pyrustic.manager.\_\_init\_\_

Pyrustic Project Manager API

<br>


```python

def add(target, destination, *files):
    """
    Create files and packages in the target project.
    
    Parameters:
        - target: str, path to the target project
        - destination: str, dotted package name or path relative to the target.
        - files: str, filenames to create.
    
    Note:
        - The destination can be a dot (in this case, the target is the destination).
        - If a filename already exists, its content is preserved.
        - If destination doesn't exist, it's created.
    """

```

<br>

```python

def ask_for_confirmation(message, default='y'):
    """
    Use this function to request a confirmation from the user.
    
    Parameters:
        - message: str, the message to display
        - default: str, either "y" or "n" to tell "Yes by default"
        or "No, by default".
    
    Returns: a boolean, True or False to reply to the request.
    
    Note: this function will append a " (y/N): " or " (Y/n): " to the message.
    """

```

<br>

```python

def build(target, app_pkg):
    """
    Build the target project. A Wheel distribution package is
    created and put in the "dist" folder ($PROJECT_DIR/dist).
    
    Parameters:
        - target: str, the target
        - app_pkg: str, the application package
    
    Exceptions:
        - BuildingError: raised if the build fails
        - PreBuildingHookError: raised when pre_building_hook.py exits with non zero
        - PostBuildingHookError: raised when pre_building_hook.py exits with non zero
    
    Note: this function uses setuptools to build both a source package distribution
    as well as a Wheel package distribution.
    """

```

<br>

```python

def dist(name):
    """
    Use this function to get some info about a distribution package
    
    Parameters:
        name: the distribution name, example: "wheel"
    
    Returns: A dict with these keys:
        name, author, author_email, description, home_page,
        maintainer, maintainer_email, version.
    
    Note: All values in the returned dict are strings.
    """

```

<br>

```python

def dist_version(package):
    """
    Returns the version of the installed distribution package,
    otherwise returns None.
    """

```

<br>

```python

def get_app_pkg(target):
    """
    This function extracts the application package name from a target path.
    Basically it extracts the basename from the path then turns dashes "-" into
    "underscores" "_".
    
    Parameters:
        - target: str, path to the target project
    
    Returns: str, the application package name.
    """

```

<br>

```python

def get_version(target):
    """
    This function read the VERSION file in the target project
    then returns the version (str) of the project.
    
    Parameters:
         - target: str, path to the target project
    
    Returns: str, version extracted from $PROJECT_DIR/VERSION or None
    """

```

<br>

```python

def github_downloads(kurl, owner, repo, maxi=10):
    """
    Get from a remote Github repository the total downloads count
    of the latest x (maxi) releases assets.
    
    Parameters:
        - kurl: python.kurl.Kurl instance
        - owner: str, the Github repository's owner name
        - repo: str, the Github repository's repo name
        - maxi: int, number of releases to take in consideration
         (from the latest to the oldest)
    
    Returns: (status_code, status_text, data)
    
        The status_code is an int, status_text is a string and
        data is an integer to indicate the downloads count
    """

```

<br>

```python

def github_latest_release(kurl, owner, repo):
    """
    Get from a remote Github repository, useful information about
    the latest release (download count, published at, tag_name)
    
    Parameters:
        - kurl: python.kurl.Kurl instance
        - owner: str, the Github repository's owner name
        - repo: str, the Github repository's repo name
    
    Returns: (status_code, status_text, data)
    
        The status_code is an int, status_text is a string and
        data = {"tag_name": str, "published_at": date,
                "downloads_count": int}
    """

```

<br>

```python

def github_repo_description(kurl, owner, repo):
    """
    Get useful information about a remote Github repository
    
    Returns: (status_code, status_text, data)
    
        The status_code is an int, status_text is a string and
        data = {"created_at": date, "description": str,
                "stargazers_count": int, "subscribers_count": int}
    """

```

<br>

```python

def init(target, app_pkg):
    """
    Initialize a project by creating a basic project structure inside.
    
    Parameters:
        - target: str, path to the target project
        - app_pkg: str, the application package
    
    Note: use the function get_app_pkg to extract what could be a
    legal app_pkg from a target.
    """

```

<br>

```python

def install():
    """
    This function does this:
    - create the folder ~/PyrusticData
    - fill the folder with some useful files and sub-folders,
    like a config file for the Project Manager and a "trash"
    folder that apps could use.
    """

```

<br>

```python

def interpret_version(cur_version, new_version):
    """
    This function interprets the command to set a new version.
    
    Parameters:
        - cur_version: str, the current version, the one to alter.
        - new_version: str, the command to set a new version.
    
    A command can be an actual new version string, or one of the keywords:
     - "maj": to increment the major number of the current version,
     - "min": to increment the minor number of the current version,
     - "rev": to increment the revision number of the current version.
    
    Returns: The new version as it should be saved in version.py
    """

```

<br>

```python

def link(target):
    """
    Edits the content of ~/PyrusticData/manager/manager_shared_data.json
    
    This function will edit the "target" value and the "recent" list.
    """

```

<br>

```python

def publish(kurl, target, app_pkg):
    """
    Publish the latest built distribution package of the target project.
    
    Parameters:
        - kurl: a pyrustic.kurl.Kurl instance
        - target: str, path to the target project
        - app_pkg: str, application package
    
    Exceptions:
        - PublishingError: raised if the publishing failed
        - PrePublishingHookError: raised if pre_publishing_hook.py exits with non zero
        - PrePublishingHookError: raised if pre_publishing_hook.py exits with non zero
    
    Note: this function uses Github API to create a new release
    in the Github repository, then upload the distribution package
    as an asset.
    
    The JSON file "publishing.json" located at $APP_DIR/pyrustic_data
    is read to extract useful data to perform this operation.
    """

```

<br>

```python

def recent():
    """
    Returns a LIFO-sorting list of recently linked targets.
    """

```

<br>

```python

def run(target, *args):
    """
    Run a module or the target project
    
    Parameters:
        - target: str, path to the target project. Or None. If target is None,
        it will be replaced with the current working directory path.
        - *args: the arguments to run the module with.
    
    Returns: This function returns the exit code.
    
    Exception:
        - MissingSysExecutableError: raised when sys.executable is missing.
    
    Note: this function will block the execution of the thread in
    which it is called till the module exits.
    """

```

<br>

```python

def run_tests(target):
    """
    Runs the tests in the target.
    
    Parameters:
        - target: str, path to the target project
    
    Returns: a tuple (bool, object). The bool indicate the success
    (True) or the failure (False) of the tests.
    The second item in the tuple can be None, an Exception instance, or a string.
    
    Note: the tests should be located at $PROJECT_DIR/tests
    """

```

<br>

```python

def set_version(target, version):
    """
    This function edits the content of $PROJECT_DIR/VERSION
    
    Parameters:
         - target: str, path to the target project
         - version: str, the version
    
    Returns:
        - bool, False, if the module version.py is missing
        - bool, True if all right
    """

```

<br>

```python

class AnteBuildHookError:
    """
    
    """

```

<br>

```python

class AnteReleaseHookError:
    """
    
    """

```

<br>

```python

class BuildError:
    """
    
    """

```

<br>

```python

class Error:
    """
    
    """

    def __init__(self, *args, **kwargs):
        """
        
        """

```

<br>

```python

class InvalidReleaseInfoError:
    """
    
    """

```

<br>

```python

class MissingReleaseInfoError:
    """
    
    """

```

<br>

```python

class MissingSysExecutableError:
    """
    
    """

```

<br>

```python

class PostBuildHookError:
    """
    
    """

```

<br>

```python

class PostReleaseHookError:
    """
    
    """

```

<br>

```python

class ReleaseError:
    """
    
    """

```

