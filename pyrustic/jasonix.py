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
    def __init__(self, path, default=None, readonly=False):
        """
        PARAMETERS:

        - path: absolute JSON file path. If it doesn't exist, a new one will be created
        or not according to the parameter "default"

        - default: absolute default JSON file path.

        - readonly: bool
        """
        self._path = path
        self._default = default
        self._readonly = readonly
        #
        self._data = None
        self._default_config = None
        #
        self._load_default(self._default)
        self._load_path(self._path)
        if self._data is None and self._default_config is not None:
            self._data = self._default_config
            if self._path:
                self.save()

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
    def path(self):
        return self._path

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
        self._json_dump(self._path, self._data)

    def reload(self):
        """
        Reload data from JSON file
        """
        self._load_default(self._default)
        self._load_path(self._path)

    # ==============================================
    #               PRIVATE METHODS
    # ==============================================

    def _load_default(self, path):
        if path and os.path.exists(path):
            self._default_config = self._json_load(path)

    def _load_path(self, path):
        if not path:
            return
        if not os.path.exists(path):
            with open(path, "w") as file:
                pass
        else:
            self._data = self._json_load(path)

    def _json_load(self, path):
        data = None
        with open(path, "r") as file:
            data = json.load(file)
        return data

    def _json_dump(self, path, data):
        with open(path, "w") as file:
            json.dump(data, file, indent=4, sort_keys=True)
