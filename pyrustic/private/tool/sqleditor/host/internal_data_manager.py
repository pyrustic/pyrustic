

class InternalDataManager:
    def __init__(self, manager_jasonix, sqleditor_jasonix):
        self._manager_jasonix = manager_jasonix
        self._sqleditor_jasonix = sqleditor_jasonix

    def store(self, target, database_path):
        if target not in self._manager_jasonix.data["last"]:
            return
        self._sqleditor_jasonix.data[target] = database_path
        # clean
        for target in self._sqleditor_jasonix.data.keys():
            if target not in self._manager_jasonix.data["last"]:
                del self._sqleditor_jasonix.data[target]
        self._sqleditor_jasonix.save()

    def previously_stored(self, target):
        return self._sqleditor_jasonix.data.get(target, None)
