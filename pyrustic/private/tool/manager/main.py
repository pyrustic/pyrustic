import cmd
import os.path
import sys
import signal
import traceback
from pyrustic import pymisc
from pyrustic import about as pyrustic_about
from pyrustic.private.tool.common import constants
from pyrustic.private.tool.manager.handler.link_handler import LinkHandler
from pyrustic.private.tool.manager.handler.unlink_handler import UnlinkHandler
from pyrustic.private.tool.manager.handler.relink_handler import RelinkHandler
from pyrustic.private.tool.manager.handler.target_handler import TargetHandler
from pyrustic.private.tool.manager.handler.last_handler import LastHandler
from pyrustic.private.tool.manager.handler.kstart_handler import KstartHandler
from pyrustic.private.tool.manager.handler.run_handler import RunHandler
from pyrustic.private.tool.manager.handler.add_handler import AddHandler
from pyrustic.private.tool.manager.handler.sql_handler import SqlHandler
from pyrustic.private.tool.manager.handler.test_handler import TestHandler
from pyrustic.private.tool.manager.handler.hub_handler import HubHandler
from pyrustic.private.tool.manager.handler.version_handler import VersionHandler
from pyrustic.private.tool.manager.handler.build_handler import BuildHandler
from pyrustic.private.tool import install


# decorator for all commands handlers
def guard(func):
    def obj(self, arg):
        try:
            func(self, pymisc.parse_cmd(arg))
        except Exception as e:
            print("Oops... Exception occurred !")
            print("".join(traceback.format_exception(*sys.exc_info())))
    return obj


class PyrusticManager(cmd.Cmd):
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
    def do_kstart(self, args):
        KstartHandler(self.target, args)

    @guard
    def do_run(self, args):
        RunHandler(self.target, args)

    @guard
    def do_add(self, args):
        AddHandler(self.target, args)

    @guard
    def do_build(self, args):
        BuildHandler(self.target)

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

    def help_kstart(self):
        print(KstartHandler.__doc__)

    def help_run(self):
        print(RunHandler.__doc__)

    def build_run(self):
        print(BuildHandler.__doc__)

    def help_add(self):
        print(AddHandler.__doc__)

    def help_build(self):
        print(BuildHandler.__doc__)

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


def signal_handler(signum, frame, pm):
    pm.do_exit([])
    return


def check_installation():
    should_install = False
    paths = (constants.SUITE_SHARED_FOLDER,
             constants.MANAGER_SHARED_FOLDER,
             constants.SQLEDITOR_SHARED_FOLDER,
             constants.RUNTEST_SHARED_FOLDER,
             constants.HUB_SHARED_FOLDER)
    for path in paths:
        if not os.path.exists(path):
            should_install = True
            break
    if not should_install:
        return
    print("\n-----\n")
    print("You haven't completed the installation of Pyrustic")
    print("Installation...")
    install.installation()
    print("\n-----\n")


def main():
    check_installation()
    pm = PyrusticManager()
    signal.signal(signal.SIGINT,
                  lambda signum, frame, pm=pm: signal_handler(signum, frame, pm))
    pm.cmdloop()
