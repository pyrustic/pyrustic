import os.path
import os
from core.template import dao_template
from core.template import host_template
from core.template import view_template
from core.template import misc_template
from core.template import test_template
from core.misc import funcs


class DhvmHandler:

    def __init__(self, target, arg, op):
        self._target = target
        self._process(arg, op)

    def _process(self, arg, op):
        if not self._target:
            print("Impossible to continue. Set a Target first")
            return
        if not arg:
            print("Incomplete command. Please check 'help " + op + "'")
            return
        if len(arg) > 2:
            print("Incorrect command. Please check 'help " + op + "'")
            return
        self._dir = os.path.join(self._target, op)
        self._test_dir = os.path.join(self._target, "tests", op)
        if len(arg) == 2:
            # build package then mirror it inside tests
            try:
                self._dir = funcs.build_package(self._dir, arg[1])
                self._test_dir = funcs.build_package(self._test_dir, arg[1])
            except Exception as e:
                print("Failed to create package")
                return
        self._name = arg[0]
        self._class_name = funcs.module_name_to_class(self._name)
        self._filename = os.path.join(self._dir, self._name)
        self._test_name = "test_" + self._name
        self._test_class_name = funcs.module_name_to_class(self._test_name)
        self._test_filename = os.path.join(self._test_dir, self._test_name)
        # check if it already exists
        if os.path.exists(self._filename):
            print("Failed: File already exists")
            return
        # create files
        try:
            self._create_files(op)
        except Exception as e:
            print("Failed to create " + op + " file")

    def _create_files(self, op):
        with open(self._filename, "w") as file:
            if op == "dao":
                file.write(dao_template.data.format(self._class_name))
            elif op == "host":
                file.write(host_template.data.format(self._class_name))
            elif op == "view":
                file.write(view_template.data.format(self._class_name))
            elif op == "misc":
                file.write(misc_template.data.format(self._class_name))
            print("Done, " + op + " file successfully created !")
        # tests
        if os.path.exists(self._test_filename):
            print("A test file already exists")
            return
        with open(self._test_filename, "w") as file:
            file.write(test_template.data.format(self._test_class_name))
            print("Test file successfully created !")