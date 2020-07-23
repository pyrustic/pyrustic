import cmd
from misc import funcs
import traceback
import sys
import signal
from misc import constants
from pyrustic.dao import Dao
from handler.target_handler import TargetHandler
from handler.add_handler import AddHandler
from handler.dbase_handler import DbaseHandler
from handler.test_handler import TestHandler
from handler.run_handler import RunHandler
from handler.demo_handler import DemoHandler
from handler.tutorial_handler import TutorialHandler
from handler.version_handler import VersionHandler


# decorator for all commands handlers
def guard(func):
    def obj(self, arg):
        try:
            func(self, funcs.split_arg(arg))
        except Exception as e:
            print("Oops... Exception occurred !")
            print("".join(traceback.format_exception(*sys.exc_info())))
    return obj


class PyrusticManager(cmd.Cmd):
    intro = ("Welcome to Pyrustic Manager\n"
            + "{} - - - ".format(constants.RELEASE_DATE)
            + "(version {})\n".format(constants.VERSION)
            + "Type 'help' or '?' to list commands. Type 'exit' to leave.\n")
    prompt = "(pyrustic) "

    def __init__(self):
        super().__init__()
        self._pyrustic_target = None
        self._pyrustic_dao = None
        self._popen_instances = []

    @property
    def pyrustic_target(self):
        if not self._pyrustic_target:
            return None
        if not funcs.valid_target(self._pyrustic_target):
            self._pyrustic_target = None
        return self._pyrustic_target

    @pyrustic_target.setter
    def pyrustic_target(self, val):
        self._pyrustic_target = val

    # ===============================
    #           OVERRIDING
    # ===============================
    def preloop(self):
        self.pyrustic_dao = Dao(constants.DB_PATH,
                                creational_script=("str",
                                                   constants.CREATIONAL_SCRIPT))

    def precmd(self, line):
        if line == "EOF":
            line = ""
        return line

    def postcmd(self, stop, line):
        print("")
        return stop

    def emptyline(self):
        pass

    # ===============================
    #            COMMANDS
    # ===============================
    @guard
    def do_target(self, args):
        target_handler = TargetHandler(self.pyrustic_target,
                                       args,
                                       self.pyrustic_dao)
        self.pyrustic_target = target_handler.target

    @guard
    def do_add(self, args):
        AddHandler(self.pyrustic_target, args)

    @guard
    def do_dbase(self, args):
        handler = DbaseHandler(self.pyrustic_target)
        self._popen_instances.append(handler.popen_instance)

    @guard
    def do_test(self, args):
        handler = TestHandler(self.pyrustic_target)
        self._popen_instances.append(handler.popen_instance)

    @guard
    def do_run(self, args):
        RunHandler(self.pyrustic_target, args)

    @guard
    def do_demo(self, args):
        DemoHandler(args)

    @guard
    def do_tutorial(self, args):
        TutorialHandler(args)

    @guard
    def do_version(self, args):
        VersionHandler()

    @guard
    def do_exit(self, args):
        for x in self._popen_instances:
            if x:
                x.kill()
        print("Exiting...")
        sys.exit()

    # ===============================
    #            COMMANDS
    # ===============================
    def help_target(self):
        print(TargetHandler.__doc__)

    def help_add(self):
        print(AddHandler.__doc__)

    def help_dbase(self):
        print(DbaseHandler.__doc__)

    def help_test(self):
        print(TestHandler.__doc__)

    def help_run(self):
        print(RunHandler.__doc__)

    def help_demo(self):
        print(DemoHandler.__doc__)

    def help_tutorial(self):
        print(TutorialHandler.__doc__)

    def help_version(self):
        print("This command shows the version of this Pyrustic Manager.")

    def help_exit(self):
        print("This command closes the program graciously.")


def signal_handler(signum, frame, pm):
    pm.do_exit([])
    return


pm = PyrusticManager()
signal.signal(signal.SIGTSTP,
              lambda signum, frame, pm=pm: signal_handler(signum, frame, pm))
pm.cmdloop()
