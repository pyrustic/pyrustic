

class InternalDataManager:
    def __init__(self, internal_dao):
        self._internal_dao = internal_dao

    def store(self, project_path, database_path):
        self._internal_dao.store(project_path, database_path)

    def previously_stored(self, project_path):
        return self._internal_dao.get_last_path(project_path)

    def close(self):
        return self._internal_dao.close()
