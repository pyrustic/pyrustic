import os
import os.path
import json
try:
    from pyrustic.exception import PyrusticException
except ImportError:
    class PyrusticException(Exception):
        pass


class Jasonix:
    """
    Jasonix allows you to play with JSON files like toys ! (really)
    """
    def __init__(self, target, default=None, readonly=False):
        """
        PARAMETERS:

        - target: dict or file-like object or a path to a json file. If target is a path
         and this path doesn't exist, a new file will be created or not according
        to the parameter "default

        - default: file-like object or a path or a dict.

        - readonly: bool
        """
        self._target = target
        self._default = default
        self._readonly = readonly
        #
        self._data = None
        #
        self._setup()


    # ==============================================
    #               PROPERTIES
    # ==============================================

    @property
    def data(self):
        """
        The dict-like representation of the JSON file
        """
        return self._data

    @data.setter
    def data(self, val):
        """
        The dict to push into JSON file
        """
        self._data = val

    @property
    def target(self):
        return self._target

    @property
    def default(self):
        return self._default

    # ==============================================
    #               PUBLIC METHODS
    # ==============================================

    def save(self):
        """"
        Push data into the JSON file (not the default file !) if 'readonly' is False
        """
        if self._readonly:
            PyrusticException("Attempt to save a readonly config !")
        self._json_dump(self._target, self._data)

    def reload(self):
        """
        Reload data from JSON file
        """
        self._setup()

    # ==============================================
    #               PRIVATE METHODS
    # ==============================================
    def _setup(self):
        if not self._target:
            return
        data = self._json_load(self._target,
                               ignore_exception=True)
        if data is None:
            if isinstance(self._target, str):
                with open(self._target, "w") as file:
                    pass
            if not self._default:
                raise PyrusticException("Missing target !")
            default_data = self._json_load(self._default)
            if default_data is None:
                message = ("Missing target !",
                           "And invalid default json.")
                raise PyrusticException(" ".join(message))
            self._data = default_data
            self.save()
            return
        self._data = data

    def _json_load(self, target, ignore_exception=False):
        data = None
        if isinstance(target, str):
            data = self._json_load_from_path(target,
                                             ignore_exception)
        elif isinstance(target, dict):
            data = target
        elif isinstance(target, bytes):
            target = target.decode("utf-8")
            data = json.loads(target)
        else:
            data = self._json_load_from_file(target,
                                             ignore_exception)
        return data

    def _json_load_from_path(self, path,
                             ignore_exception=False):
        data = None
        try:
            with open(path, "r") as file:
                data = json.load(file)
        except Exception as e:
            if not ignore_exception:
                raise e
        return data

    def _json_load_from_file(self, file,
                             ignore_exception=False):
        data = None
        try:
            data = json.load(file)
        except Exception as e:
            if not ignore_exception:
                raise e
        return data

    def _json_dump(self, target, data,
                   ignore_exception=False):
        if isinstance(target, str):
            self._json_dump_to_path(target, data, ignore_exception)
        else:
            self._json_dump_to_file(target, data, ignore_exception)

    def _json_dump_to_path(self, path, data,
                           ignore_exception=False):
        try:
            with open(path, "w") as file:
                json.dump(data, file, indent=4, sort_keys=True)
        except Exception as e:
            if not ignore_exception:
                raise e

    def _json_dump_to_file(self, file, data,
                           ignore_exception=False):
        try:
            json.dump(data, file, indent=4, sort_keys=True)
        except Exception as e:
            if not ignore_exception:
                raise e
