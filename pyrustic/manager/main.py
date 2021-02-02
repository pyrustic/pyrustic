from cmd import Cmd
import os.path
import sys
import signal
import traceback
from pyrustic import pymisc
from pyrustic.manager import install
from pyrustic import about as pyrustic_about
from pyrustic.manager.handler.link_handler import LinkHandler
from pyrustic.manager.handler.unlink_handler import UnlinkHandler
from pyrustic.manager.handler.relink_handler import RelinkHandler
from pyrustic.manager.handler.target_handler import TargetHandler
from pyrustic.manager.handler.last_handler import LastHandler
from pyrustic.manager.handler.init_handler import InitHandler
from pyrustic.manager.handler.run_handler import RunHandler
from pyrustic.manager.handler.add_handler import AddHandler
from pyrustic.manager.handler.pkg_handler import PkgHandler
from pyrustic.manager.handler.sql_handler import SqlHandler
from pyrustic.manager.handler.test_handler import TestHandler
from pyrustic.manager.handler.hub_handler import HubHandler
from pyrustic.manager.handler.version_handler import VersionHandler


# decorator for all commands handlers
def guard(func):
    def obj(self, arg):
        try:
            func(self, pymisc.parse_cmd(arg))
        except Exception as e:
            print("Oops... Exception occurred !\n")
            print("".join(traceback.format_exception(*sys.exc_info())))
    return obj


class PyrusticManager(Cmd):
    intro = ("""Welcome to Pyrustic Manager !\n"""
             + """Version: {}\n""".format(pyrustic_about.VERSION)
             + """Type "help" or "?" to list commands. Type "exit" to leave.\n""")

    prompt = "(pyrustic) "

    def __init__(self):
        super().__init__()
        self.__target = None
        self.__popen_instances = []

    @property
    def target(self):
        if not self.__target:
            return None
        if not os.path.isabs(self.__target):
            self.__target = None
        return self.__target

    @target.setter
    def target(self, val):
        self.__target = val

    # ===============================
    #           OVERRIDING
    # ===============================
    def preloop(self):
        pass

    def precmd(self, line):
        if line == "EOF":
            line = ""
        print("")
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
    def do_link(self, args):
        link_handler = LinkHandler(self.target, args)
        self.target = link_handler.target

    @guard
    def do_unlink(self, args):
        unlink_handler = UnlinkHandler(self.target, args)
        self.target = unlink_handler.target

    @guard
    def do_relink(self, args):
        relink_handler = RelinkHandler(self.target, args)
        self.target = relink_handler.target

    @guard
    def do_target(self, args):
        TargetHandler(self.target, args)

    @guard
    def do_last(self, args):
        LastHandler(self.target, args)

    @guard
    def do_init(self, args):
        InitHandler(self.target, args)

    @guard
    def do_run(self, args):
        RunHandler(self.target, args)

    @guard
    def do_add(self, args):
        AddHandler(self.target, args)

    @guard
    def do_pkg(self, args):
        PkgHandler(self.target)

    @guard
    def do_sql(self, args):
        handler = SqlHandler(self.target)
        self.__popen_instances.append(handler.popen_instance)

    @guard
    def do_test(self, args):
        handler = TestHandler(self.target)
        self.__popen_instances.append(handler.popen_instance)

    @guard
    def do_hub(self, args):
        handler = HubHandler(self.target)
        self.__popen_instances.append(handler.popen_instance)

    @guard
    def do_version(self, args):
        VersionHandler()

    @guard
    def do_exit(self, args):
        for x in self.__popen_instances:
            if x:
                x.terminate()
                pass
        print("Exiting...")
        sys.exit()

    # ===============================
    #            COMMANDS
    # ===============================
    def help_link(self):
        print(LinkHandler.__doc__)

    def help_unlink(self):
        print(UnlinkHandler.__doc__)

    def help_relink(self):
        print(RelinkHandler.__doc__)

    def help_target(self):
        print(TargetHandler.__doc__)

    def help_last(self):
        print(LastHandler.__doc__)

    def help_init(self):
        print(InitHandler.__doc__)

    def help_run(self):
        print(RunHandler.__doc__)

    def help_add(self):
        print(AddHandler.__doc__)

    def help_pkg(self):
        print(PkgHandler.__doc__)

    def help_sql(self):
        print(SqlHandler.__doc__)

    def help_test(self):
        print(TestHandler.__doc__)

    def help_hub(self):
        print(HubHandler.__doc__)

    def help_version(self):
        print(VersionHandler.__doc__)

    def help_exit(self):
        print("This command closes the program graciously.")


def main():
    install.main()
    pm = PyrusticManager()
    # Interrupt process (typically CTRL+C or 'delete' char or 'break' key)
    signal_num = signal.SIGINT
    handler = lambda signum, frame, pm=pm: pm.do_exit([])
    signal.signal(signal_num, handler)
    pm.cmdloop()
