import unittest


class Result(unittest.TestResult):

    def __init__(self, test_id, queue):
        super().__init__(self)
        self._test_id = test_id
        self._queue = queue

    def startTestRun(self):
        super().startTestRun()
        data = {"id": self._test_id, "event": "start_test_run"}
        self._queue.put(data)

    def stopTestRun(self):
        super().stopTestRun()
        data = {"id": self._test_id, "event": "stop_test_run",
                "was_successful": self.wasSuccessful()}
        self._queue.put(data)

    def startTest(self, test):
        super().startTest(test)
        data = {"id": self._test_id, "event": "start_test",
                "test": test}
        self._queue.put(data)

    def stopTest(self, test):
        super().stopTest(test)
        data = {"id": self._test_id, "event": "stop_test",
                "test": test}
        self._queue.put(data)

    def addError(self, test, err):
        """'err' is a tuple of values as returned by sys.exc_info()"""
        super().addError(test, err)
        data = {"id": self._test_id, "event": "add_error",
                "test": test, "err": err}
        self._queue.put(data)

    def addFailure(self, test, err):
        super().addFailure(test, err)
        data = {"id": self._test_id, "event": "add_failure",
                "test": test, "err": err}
        self._queue.put(data)

    def addSuccess(self, test):
        super().addSuccess(test)
        data = {"id": self._test_id, "event": "add_success",
                "test": test}
        self._queue.put(data)

    def addSkip(self, test, reason):
        super().addSkip(test, reason)
        data = {"id": self._test_id, "event": "add_skip",
                "test": test, "reason": reason}
        self._queue.put(data)

    def addExpectedFailure(self, test, err):
        super().addExpectedFailure(test, err)
        data = {"id": self._test_id, "event": "add_expected_failure",
                "test": test, "err": err}
        self._queue.put(data)

    def addUnexpectedSuccess(self, test):
        super().addUnexpectedSuccess(test)
        data = {"id": self._test_id, "event": "add_unexpected_success",
                "test": test}
        self._queue.put(data)

    def addSubTest(self, test, subtest, outcome):
        try:  # new in Python version 3.4
            super().addSubTest(test, subtest, outcome)
        except Exception as e:
            return
        data = {"id": self._test_id, "event": "add_sub_test",
                "test": test, "sub_test": subtest, "outcome": outcome}
        self._queue.put(data)
