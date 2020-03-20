import sqlite3 as sqlite
import os.path
import atexit


class Dao:
    def __init__(self, path, script=None, script_is_file=True, raise_exception=True, raise_warning=True):
        """
        Hello Friend ! This is Dao ! It's encouraged to use this class by composition.
        DAO: Data Access Object (this one is built to work with SQLite).
        U give an SQL request, it spills out the result !

        __init__(self, path, script=None, script_is_file=True, raise_exception=True, raise_warning=True)

        PARAMETERS
        ==========
        - path: path to database file

        - script: The string to execute as creational script.
            It could be a regular string to parse, or the path to an SQL file.
            To indicate if it is a regular string, please set False to the flag script_is_file
            Example_a: script="/path/to/script.sql", script_is_file=True
            Example_b: script="CREATE TABLE my_table(id INTEGER NOT NULL PRIMARY KEY);",
                        script_is_file=False

        - script_is_file: Boolean to indicate if script is a path to an sql file or a regular string.
            True to indicate that it's a path, False to indicate that it's a regular string.

        - raise_exception: By default, True, so exceptions (sqlite.Error) will be raised

        - raise_warning: By default, True, so exceptions (sqlite.Warning) will be raised

        PROPERTIES
        ==========
        - path: get database file path
        - con: get connection object
        - script: get the script
        - script_is_file: get the boolean
        - is_new: get True if this database is freshly created, else False

        METHODS
        =======
        - test(self): returns True if legal database, else returns False

        - edit(self, sql, param=()): use this to run DDL and DML.
            It returns True or False or raises sqlite.Error, sqlite.Warning

        - query(self, sql, param=()): use this to run DQL
            It returns a tuple: (data, description).
                Data is a list with data from ur query.
                Description is a list with the name of columns related to data
            Example: ( [1, "Jack", 50], ["id", "name", "age"] )
            This method can raise sqlite.Error, sqlite.Warning

        - exec_script(self, script, is_file=True): use this to execute a script
            This method returns nothing and can raise sqlite.Error, sqlite.Warning

        - export(self): export the database, it returns a string
            This method can raise sqlite.Error, sqlite.Warning

        - get_table_list(self): list of tables.
            Example: ["table_1", "table_2"]
            This method can raise sqlite.Error, sqlite.Warning

        - get_column_list(self, table): list of columns of a table name
            Example: ["column_1", "column_2"]
            This method can raise sqlite.Error, sqlite.Warning

        - close(self): well, it closes the connection
        """

        self._path = path
        self._script = script
        self._script_is_file = script_is_file
        self._raise_exception = raise_exception
        self._raise_warning = raise_warning
        use_creational_script = False
        self._con = None
        self._is_new = False
        if not os.path.isfile(path):
            self._is_new = True
            use_creational_script = True
        try:
            self._con = sqlite.connect(path)
        except sqlite.Error as e:
            raise e
        finally:
            atexit.register(self.close)
        if use_creational_script and script:
            self.exec_script(script, script_is_file)

    # ============ PROPERTIES ============
    @property
    def path(self):
        return self._path

    @property
    def con(self):
        return self._con

    @property
    def script(self):
        return self._script

    @property
    def script_is_file(self):
        return self._script_is_file

    @property
    def is_new(self):
        return self._is_new

    # ============= PUBLIC METHODS ==============
    def test(self):
        """ Return True if legal database, else returns False"""
        cache = self._raise_exception
        self._raise_exception = True
        legal = True
        try:
            self.get_table_list()
        except sqlite.Error as e:
            legal = False
        except sqlite.Warning as e:
            legal = False
        self._raise_exception = cache
        return legal

    def edit(self, sql, param=()):
        # for Data Definition Language (DDL) and Data Manipulation Language (DML)
        result = True
        cur = None
        try:
            cur = self._con.cursor()
            cur.execute(sql, param)
            self._con.commit()
        except sqlite.Error as e:
            result = False
            if self._raise_exception:
                raise
        except sqlite.Warning as e:
            result = False
            if self._raise_warning:
                raise
        finally:
            if cur:
                cur.close()
        return result

    def query(self, sql, param=()):
        # for Data Query Language (DQL)
        description = []
        data = []
        cur = None
        try:
            cur = self._con.cursor()
            cur.execute(sql, param)
            data = cur.fetchall()
            description = cur.description
        except sqlite.Error as e:
            if self._raise_exception:
                raise
        except sqlite.Warning as e:
            if self._raise_warning:
                raise
        finally:
            if cur:
                cur.close()
        return [x[0] for x in description], data

    def exec_script(self, script, is_file=True):
        cur = None
        try:
            if is_file:
                with open(script, "r") as script:
                    script = script.read()
            cur = self._con.cursor()
            cur.executescript(script)
        except sqlite.Error as e:
            if self._raise_exception:
                raise
        except sqlite.Warning as e:
            if self._raise_warning:
                raise
        finally:
            if cur:
                cur.close()

    def export(self):
        result = ""
        try:
            "\n".join(self._con.iterdump())
        except sqlite.Error as e:
            if self._raise_exception:
                raise
        except sqlite.Warning as e:
            if self._raise_warning:
                raise
        return result

    def get_table_list(self):
        data = []
        cur = None
        try:
            cur = self._con.cursor()
            cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
            data = cur.fetchall()
        except sqlite.Error as e:
            if self._raise_exception:
                raise
        except sqlite.Warning as e:
            if self._raise_warning:
                raise
        finally:
            if cur:
                cur.close()
        return data

    def get_column_list(self, table):
        data = []
        cur = None
        try:
            cur = self._con.cursor()
            cur.execute("pragma table_info('{}')".format(table))
            data = cur.fetchall()
        except sqlite.Error as e:
            if self._raise_exception:
                raise
        except sqlite.Warning as e:
            if self._raise_warning:
                raise
        finally:
            if cur:
                cur.close()
        return data

    def close(self):
        if self._con:
            self._con.close()
            self._con = None
            atexit.unregister(self.close)
