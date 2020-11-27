import sqlite3 as sqlite


class MainHost:
    def __init__(self, dao_builder):
        self._dao_builder = dao_builder
        self._dao = None
        self._path = None

    @property
    def path(self):
        return self._path

    def open(self, path):
        dao = self._open(path)
        if dao is None:
            return False
        if self._dao:
            self._dao.close()
        self._dao = dao
        self._path = path
        return True

    def is_data_query_language(self, sql):
        if not sql:
            return
        splitted = sql.split(maxsplit=1)
        command = splitted[0]
        if command.lower() == "select":
            return True
        return False

    def exec_query_request(self, sql):
        return self._dao.query(sql)

    def exec_edit_request(self, sql):
        return self._dao.edit(sql)

    def exec_script(self, script, is_file=False):
        return self._dao.script(script, is_file=is_file)

    def tables(self):
        sqlite_prefix = "sqlite_"
        tables = []
        data = self._dao.tables()
        for x in data:
            if not x[0].startswith(sqlite_prefix):
                tables.append(x[0])
        return tables

    def db_schema(self):
        db_schema = []
        for table in sorted(self.tables()):
            columns = self.columns(table)
            table_data = (table, columns)
            db_schema.append(table_data)
        return db_schema

    def columns(self, name):
        return self._dao.columns(name)

    def table_content(self, name):
        return self._dao.table_content(name)

    def _open(self, path):
        dao = None
        error = False
        try:
            dao = self._dao_builder.build(path)
        except sqlite.Error:
            error = True
        if not error and dao.test():
            return dao
        dao.close()
        return None

    def close(self):
        return self._dao.close()
