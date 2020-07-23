

class InternalDao:
    def __init__(self, dao):
        self._dao = dao

    def store(self, project_path, database_path):
        if self.get_last_path(project_path)[1]:
            return self._update(project_path, database_path)
        return self._store(project_path, database_path)

    def get_last_path(self, project_path):
        sql = "SELECT * FROM path WHERE project = ?"
        return self._dao.query(sql, (project_path,))

    def close(self):
        self._dao.close()

    def _store(self, project_path, database_path):
        sql = "INSERT INTO path (project, database) VALUES (?, ?)"
        return self._dao.edit(sql, (project_path, database_path))

    def _update(self, project_path, database_path):
        sql = "UPDATE path SET database=? WHERE project=?"
        return self._dao.edit(sql, (database_path, project_path))
