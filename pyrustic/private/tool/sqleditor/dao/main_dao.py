

class MainDao:
    def __init__(self, dao):
        self._dao = dao

    def script(self, path, is_file=False):
        self._dao.script(path, is_file)

    def tables(self):
        return self._dao.tables()

    def columns(self, table):
        return self._dao.columns(table)

    def table_content(self, table):
        sql = "SELECT * FROM " + table
        return self._dao.query(sql)

    def edit(self, sql):
        return self._dao.edit(sql)

    def query(self, sql):
        return self._dao.query(sql)

    def test(self):
        return self._dao.test()

    def close(self):
        self._dao.close()
