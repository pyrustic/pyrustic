import unittest
import os.path
import sys


class LiteTestRunner:
    def __init__(self, path, app_dir):
        self._path = path
        self._app_dir = app_dir

    def run(self, failfast=True):
        reloader = _Reloader()
        reloader.save_state()
        cache = self._run(failfast)
        reloader.restore_state()
        return cache

    def _run(self, failfast):
        if not os.path.exists(self._path):
            return False, "This path doesn't exist"
        test_loader = unittest.TestLoader()
        suite = test_loader.discover(self._path, top_level_dir=self._app_dir)
        result = unittest.TestResult()
        try:
            result.startTestRun()
            result.failfast = failfast
            suite.run(result)
        except Exception as e:
            return False, e
        finally:
            result.stopTestRun()
        if result.wasSuccessful():
            return True, None
        else:
            return False, self._stringify_result(result)

    def _stringify_result(self, result):
        data = []
        if result.errors:
            for error in result.errors:
                cache = "{}\n{}\n\n".format(error[0], error[1])
                data.append(cache)
        if result.failures:
            for failure in result.failures:
                cache = "{}\n{}\n\n".format(failure[0], failure[1])
                data.append(cache)
        if result.unexpectedSuccesses:
            for expected_failure in result.expectedFailures:
                cache = "{}\n{}\n\n".format(expected_failure[0],
                                            expected_failure[1])
                data.append(cache)

        return "".join(data)


class _Reloader:
    def __init__(self):
        self._state = None

    def save_state(self):
        self._state = sys.modules.copy()

    def restore_state(self):
        for x in sys.modules.copy().keys():
            if not x in self._state:
                del sys.modules[x]
