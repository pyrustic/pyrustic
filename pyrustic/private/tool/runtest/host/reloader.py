import sys


class Reloader:
    def __init__(self):
        self._state = None

    def save_state(self):
        self._state = sys.modules.copy()

    def restore_state(self):
        for x in sys.modules.copy().keys():
            if not x in self._state:
                del sys.modules[x]
