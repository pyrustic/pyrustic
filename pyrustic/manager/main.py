import os
import os.path
import sys
import signal
import traceback
import pyrustic
from cmd import Cmd
from pyrustic import pymisc
from pyrustic.manager import install
from pyrustic.manager.handler.link_handler import LinkHandler
from pyrustic.manager.handler.unlink_handler import UnlinkHandler
from pyrustic.manager.handler.relink_handler import RelinkHandler
from pyrustic.manager.handler.target_handler import TargetHandler
from pyrustic.manager.handler.last_handler import LastHandler
from pyrustic.manager.handler.init_handler import InitHandler
from pyrustic.manager.handler.run_handler import RunHandler
from pyrustic.manager.handler.add_handler import AddHandler
from pyrustic.manager.handler.build_handler import BuildHandler
from pyrustic.manager.handler.sql_handler import SqlHandler
from pyrustic.manager.handler.test_handler import TestHandler
from pyrustic.manager.handler.hub_handler import HubHandler
from pyrustic.manager.handler.version_handler import VersionHandler


def main(argv=None, target=None):
    if not argv:
        argv = sys.argv[1:]
    pm = init_pyrustic_manager()
    # Non interactive mode
    if len(argv) > 0:
        _non_interactive_mode(pm, argv, target)
    # Enable Interactive Mode
    else:
        _interactive_mode(pm, target)


def init_pyrustic_manager():
    install.main()
    pm = PyrusticManager()
    # Interrupt process (typically CTRL+C or 'delete' char or 'break' key)
    signal_num = signal.SIGINT
    handler = lambda signum, frame, pm=pm: pm.do_exit([])
    signal.signal(signal_num, handler)
    return pm


# decorator for all commands handlers
def guard(func):
    def obj(self, arg):
        try:
            arg = pymisc.parse_cmd(arg) if isinstance(arg, str) else arg
            func(self, arg)
        except Exception as e:
            print("Oops... Exception occurred !\n")
            print("".join(traceback.format_exception(*sys.exc_info())))
    return obj


class PyrusticManager(Cmd):
    intro = ("""Welcome to Pyrustic Manager !\n"""
             + """Version: {}\n""".format(pyrustic.__version__)
             + """Type "help" or "?" to list commands. Type "exit" to leave.\n""")

    prompt = "(pyrustic) "

    def __init__(self):
        super().__init__()
        self.__target = None
        self.__app_pkg = None
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

    @property
    def app_pkg(self):
        if self.__app_pkg is None and self.target is not None:
            self.__app_pkg = _find_app_pkg(self.target)
        if self.__app_pkg:
            source_dir = os.path.join(self.target, self.__app_pkg)
            if not os.path.exists(source_dir):
                self.__app_pkg = None
        return self.__app_pkg

    @app_pkg.setter
    def app_pkg(self, val):
        self.__app_pkg = val

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
        link_handler = LinkHandler(self.target, self.app_pkg,
                                   args)
        self.target = link_handler.target

    @guard
    def do_unlink(self, args):
        unlink_handler = UnlinkHandler(self.target,
                                       self.app_pkg,
                                       args)
        self.target = unlink_handler.target
        self.app_pkg = unlink_handler.app_pkg

    @guard
    def do_relink(self, args):
        relink_handler = RelinkHandler(self.target,
                                       self.app_pkg,
                                       args)
        self.target = relink_handler.target

    @guard
    def do_target(self, args):
        TargetHandler(self.target,
                      self.app_pkg,
                      args)

    @guard
    def do_last(self, args):
        LastHandler(self.target,
                    self.app_pkg, args)

    @guard
    def do_init(self, args):
        InitHandler(self.target,
                    self.app_pkg, args)

    @guard
    def do_run(self, args):
        RunHandler(self.target,
                   self.app_pkg, args)

    @guard
    def do_add(self, args):
        AddHandler(self.target, self.app_pkg, args)

    @guard
    def do_build(self, args):
        BuildHandler(self.target, self.app_pkg)

    @guard
    def do_sql(self, args):
        handler = SqlHandler(self.target, self.app_pkg)
        self.__popen_instances.append(handler.popen_instance)

    @guard
    def do_test(self, args):
        handler = TestHandler(self.target, self.app_pkg)
        self.__popen_instances.append(handler.popen_instance)

    @guard
    def do_hub(self, args):
        handler = HubHandler(self.target, self.app_pkg)
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


def _interactive_mode(pm, target):
    pm.target = target
    pm.cmdloop()


def _non_interactive_mode(pm, data, target):
    if not target:
        target = os.getcwd()
    pm.target = target
    command = data[0]
    args = []
    handler = None
    if len(data) > 1:
        args = data[1:]
    if command == "help":
        handler = pm.do_help
        args = " ".join(args)
    else:
        handler = getattr(pm, "do_{}".format(command))
    if handler is None:
        print("Failed to process your request. Type <help>")
    handler(args)


def _find_app_pkg(target):
    if not os.path.exists(target):
        return None
    app_pkg = os.path.basename(target)
    return app_pkg
