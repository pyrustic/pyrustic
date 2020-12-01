import sqlite3 as sqlite
import os.path
import atexit
import threading


class LiteDao:
    """
    It's recommended to use LiteDao by composition. Meaning: don't subclass it.
    DAO: Data Access Object (this one is built to work with SQLite).
    You give an SQL request with some params or not, it spills out the result nicely !
    You can even get the list of tables or columns.
    """
    def __init__(self, path, creational_script=None, raise_exception=True,
                 raise_warning=True, connection_kwargs={}):
        """
        - path: absolute path to database file

        - creational_script: A tuple (format, value).
            - Format is a string that is either "inline" or "file".
            - Value is either the inline sql script or the absolute path to the file.
            Example_a: ("inline", "CREATE TABLE my_table(id INTEGER NOT NULL PRIMARY KEY);"
            Example_b: ("file", "/path/to/script.sql")

        - raise_exception: By default, True, so exceptions (sqlite.Error) will be raised

        - raise_warning: By default, True, so exceptions (sqlite.Warning) will be raised

        - connection_kwargs: connections arguments used while calling the
         method "sqlite.connect()"
        """

        self._path = os.path.normpath(path)
        self._creational_script = creational_script
        self._raise_exception = raise_exception
        self._raise_warning = raise_warning
        self._lock = threading.Lock()
        use_creational_script = False
        self._con = None
        self._is_new = False
        if not os.path.isfile(path):
            self._is_new = True
            use_creational_script = True
        try:
            if "check_same_thread" in connection_kwargs:
                del connection_kwargs["check_same_thread"]
            self._con = sqlite.connect(path, check_same_thread=False, **connection_kwargs)
        except sqlite.Error as e:
            raise e
        finally:
            atexit.register(self.close)
        if use_creational_script and creational_script:
            is_file = True if creational_script[0] == "file" else False
            self.script(creational_script[1], is_file)

    # ====================================
    #              PROPERTIES
    # ====================================
    @property
    def path(self):
        return self._path

    @property
    def con(self):
        """
        Connection object
        """
        return self._con

    @property
    def creational_script(self):
        return self._creational_script

    @property
    def is_new(self):
        """
        Returns True if the database has just been created, otherwise returns False
        """
        return self._is_new

    # ====================================
    #            PUBLIC METHODS
    # ====================================
    def test(self):
        """
        Returns True if this is a legal database, otherwise returns False
        """
        cache = self._raise_exception
        self._raise_exception = True
        legal = True
        try:
            self.tables()
        except sqlite.Error as e:
            legal = False
        except sqlite.Warning as e:
            legal = False
        self._raise_exception = cache
        return legal

    def edit(self, sql, param=None):
        """
        Use this method to edit your database.
        Formally: Data Definition Language (DDL) and Data Manipulation Language (DML).
        It returns True or False or raises sqlite.Error, sqlite.Warning
        Example:
            edit( "SELECT * FROM table_x WHERE age=?", param=(15, ) )
        """
        with self._lock:
            param = () if param is None else param
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

    def query(self, sql, param=None):
        """
        Use this method to query your database.
        Formally: Data Query Language (DQL)
        It returns a tuple: (data, description).
                Data is a list with data from ur query.
                Description is a list with the name of columns related to data
            Example: ( [1, "Jack", 50], ["id", "name", "age"] )
            This method can raise sqlite.Error, sqlite.Warning
        """
        with self._lock:
            param = () if param is None else param
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

    def script(self, script, is_file=True):
        """
        Executes the string script as an sql-script. Meaning: there are multiple lines of sql.
        This method returns nothing but could raise sqlite.Error, sqlite.Warning
        """
        with self._lock:
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
        """
        export the database: it returns a string of sql code.
        This method can raise sqlite.Error, sqlite.Warning
        """
        with self._lock:
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

    def tables(self):
        """
        Returns the list of tables names.
        Example: ["table_1", "table_2"]
        This method can raise sqlite.Error, sqlite.Warning
        """
        with self._lock:
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

    def columns(self, table):
        """
        Returns the list of columns names of the given table name
        A column is like:
            (int_id, str_column_name, str_column_datatype, int_boolean_nullability,
            default_value, int_primary_key)
        Example:
            [(0, "id", "INTEGER", 1, None, 1),
            (1, "name", "TEXT", 0, None, 0),
            (2, "age", "INTEGER", 1, None, 0)]

        This method can raise sqlite.Error, sqlite.Warning
        """
        with self._lock:
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
        """
        Well, it closes the connection
        """
        with self._lock:
            if self._con:
                try:
                    self._con.close()
                except Exception:
                    pass
                self._con = None
                atexit.unregister(self.close)
