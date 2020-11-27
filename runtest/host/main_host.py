import os
import os.path
import about
import unittest
import time


class MainHost:

    def __init__(self, root_path, reloader, result_builder):
        self._root_path = root_path
        self._reloader = reloader
        self._result_builder = result_builder
        self._is_running = False
        self._running_test = dict()
        self._reloader.save_state()

    def count_tests(self, path, class_name=None, method_name=None, test_loader=None):
        self._reloader.restore_state()
        if not os.path.exists(path):
            return
        dotted_module_name = None
        test_loader = test_loader if test_loader else unittest.TestLoader()
        if os.path.isfile(path):
            dirname, ext = os.path.splitext(path)
            if ext != ".py":
                return
            dotted_module_name = self._convert_path_to_dotted_path(dirname, start="tests")
        suite = None
        try:
            if dotted_module_name:
                dotted_module_name += "." + class_name if class_name else ""
                dotted_module_name += "." + method_name if method_name else ""
                suite = test_loader.loadTestsFromName(name=dotted_module_name)
            else:
                suite = test_loader.discover(start_dir=path, top_level_dir=self._root_path)
        except Exception:
            return
        if suite is None:
            return
        return suite.countTestCases(), suite

    def tests_in_directory(self, path):
        if not os.path.exists(path):
            return
        directories = []
        modules = []
        count_tests = 0
        for name in sorted(os.listdir(path)):
            if name in ("__init__.py", "__pycache__"):
                continue
            entry_path = os.path.join(path, name)
            path_is_dir = True if os.path.isdir(entry_path) else False
            data = self.count_tests(entry_path)
            if data is None:
                continue
            if data[0] == 0:
                continue
            count_tests += data[0]
            if path_is_dir:
                directories.append(name)
            else:
                modules.append(name)
        return count_tests, directories, modules

    def tests_in_module(self, path):
        if not os.path.exists(path):
            return
        data = self.count_tests(path)
        if data is None:
            return
        count_tests, suite = data
        flatten_suite = self._flatten_suite(suite, [])
        classes = []
        for x in flatten_suite:
            if x.__class__ not in classes:
                classes.append(x.__class__)
        return count_tests, tuple([x.__name__ for x in classes])

    def tests_in_class(self, path, class_name):
        if not os.path.exists(path):
            return
        test_loader = unittest.TestLoader()
        data = self.count_tests(path, class_name=class_name, test_loader=test_loader)
        if data is None:
            return
        count_tests, suite = data
        flatten_suite = self._flatten_suite(suite, [])
        class_ = None
        for x in flatten_suite:
            if x.__class__.__name__ == class_name:
                class_ = x.__class__
                break
        if class_:
            test_cases = test_loader.getTestCaseNames(class_)
            return len(test_cases), test_cases

    def run(self, test_id, queue, path, class_name=None, method_name=None, failfast=False):
        data = self.count_tests(path, class_name=class_name, method_name=method_name)
        if data is None:
            return False
        count_tests, suite = data
        self.run_suite(test_id, suite, queue, failfast)

    def run_suite(self, test_id, suite, queue, failfast=False):
        self._reloader.restore_state()
        result = self._result_builder.build(test_id, queue)
        self._running_test[test_id] = dict()
        self._running_test[test_id]["result"] = result
        self._running_test[test_id]["suite"] = suite
        time_a = time.time()
        try:
            result.startTestRun()
            result.failfast = failfast
            suite.run(result)
        except Exception as e:
            return False
        finally:
            time_b = time.time()
            time_elapsed = time_b - time_a
            data = {"id": test_id, "event": "time_elapsed", "time": time_elapsed}
            queue.put(data)
            result.stopTestRun()

    def stop(self, test_id):
        try:
            self._running_test[test_id]["result"].stop()
        except Exception as e:
            pass

    def _flatten_suite(self, suite, result):
        if hasattr(suite, "__iter__"):
            for x in suite:
                self._flatten_suite(x, result)
        else:
            result.append(suite)
        return result

    def _convert_path_to_dotted_path(self, path, start=None):
        path = os.path.normpath(path)
        parts = path.split(os.sep)
        result = ""
        access = False if start else True
        for i, x in enumerate(parts):
            if not access:
                if x == start:
                    access = True
            if access:
                result += x
                if i < (len(parts) - 1):
                    result += "."
        return result
