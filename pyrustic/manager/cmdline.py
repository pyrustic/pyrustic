import os
import os.path
import sys
import signal
import traceback
from cmd import Cmd
from pyrustic import manager
from pyrustic.manager.core import pymisc
from pyrustic.manager.handler.link_handler import LinkHandler
from pyrustic.manager.handler.unlink_handler import UnlinkHandler
from pyrustic.manager.handler.relink_handler import RelinkHandler
from pyrustic.manager.handler.target_handler import TargetHandler
from pyrustic.manager.handler.recent_handler import RecentHandler
from pyrustic.manager.handler.init_handler import InitHandler
from pyrustic.manager.handler.run_handler import RunHandler
from pyrustic.manager.handler.add_handler import AddHandler
from pyrustic.manager.handler.build_handler import BuildHandler
from pyrustic.manager.handler.publish_handler import PublishHandler
from pyrustic.manager.handler.hub_handler import HubHandler
#from pyrustic.manager.handler.version_handler import VersionHandler
from pyrustic.manager import constant
try:
    import readline
except ImportError:
    readline = None


# decorator for all commands handlers
def guard(func):
    def obj(self, arg):
        cache = None
        try:
            arg = pymisc.parse_cmd(arg) if isinstance(arg, str) else arg
            cache = func(self, arg)
        except Exception as e:
            print("Oops... Exception occurred !\n")
            print("".join(traceback.format_exception(*sys.exc_info())))
        return cache
    return obj


class Cmdline(Cmd):
    intro = ("""Pyrustic Project Manager\n"""
             + """Version: {}\n""".format(manager.dist_version("pyrustic"))
             + """Type "help" or "?" to list commands. Type "exit" to leave.\n""")

    prompt = "(pyrustic) "

    def __init__(self):
        super().__init__()
        self.__history_size = 420
        self.__history_file = None
        self.__target = None
        self.__app_pkg = None
        self.__setup()

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
        self.__app_pkg = None

    @property
    def app_pkg(self):
        if not self.__app_pkg:
            self.__app_pkg = manager.get_app_pkg(self.target)
        return self.__app_pkg

    @app_pkg.setter
    def app_pkg(self, val):
        self.__app_pkg = val

    @property
    def history_size(self):
        return self.__history_size

    @property
    def history_file(self):
        if not self.__history_file:
            path = os.path.join(constant.MANAGER_SHARED_FOLDER,
                                "cmd_history.txt")
            if not os.path.exists(path):
                with open(path, "w") as file:
                    pass
            self.__history_file = path
        return self.__history_file

    # ========== OVERRIDING ==========

    def preloop(self):
        if readline and self.history_file:
            readline.read_history_file(self.history_file)

    def postloop(self):
        if readline:
            readline.set_history_length(self.history_size)
            readline.write_history_file(self.history_file)

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

    # ========== COMMANDS ==========

    @guard
    def do_link(self, args):
        link_handler = LinkHandler(self.target, self.app_pkg,
                                   *args)
        self.target = link_handler.target

    @guard
    def do_unlink(self, args):
        unlink_handler = UnlinkHandler(self.target,
                                       self.app_pkg,
                                       *args)
        self.target = unlink_handler.target
        self.app_pkg = unlink_handler.app_pkg

    @guard
    def do_relink(self, args):
        relink_handler = RelinkHandler(self.target,
                                       self.app_pkg,
                                       *args)
        self.target = relink_handler.target

    @guard
    def do_target(self, args):
        TargetHandler(self.target,
                      self.app_pkg,
                      *args)

    @guard
    def do_recent(self, args):
        RecentHandler(self.target,
                      self.app_pkg, *args)

    @guard
    def do_init(self, args):
        InitHandler(self.target,
                    self.app_pkg, *args)

    @guard
    def do_run(self, args):
        RunHandler(self.target,
                   self.app_pkg, *args)

    @guard
    def do_add(self, args):
        AddHandler(self.target, self.app_pkg, *args)

    @guard
    def do_build(self, args):
        BuildHandler(self.target, self.app_pkg, *args)

    @guard
    def do_publish(self, args):
        PublishHandler(self.target, self.app_pkg, *args)

    @guard
    def do_hub(self, args):
        HubHandler(self.target, self.app_pkg, *args)

    #@guard
    #def do_version(self, args):
    #   VersionHandler(self.target, self.app_pkg, *args)

    @guard
    def do_exit(self, args):
        print("Exiting...")
        return True

    # ========== COMMANDS DOC ==========

    def help_link(self):
        print(LinkHandler.__doc__)

    def help_unlink(self):
        print(UnlinkHandler.__doc__)

    def help_relink(self):
        print(RelinkHandler.__doc__)

    def help_target(self):
        print(TargetHandler.__doc__)

    def help_recent(self):
        print(RecentHandler.__doc__)

    def help_init(self):
        print(InitHandler.__doc__)

    def help_run(self):
        print(RunHandler.__doc__)

    def help_add(self):
        print(AddHandler.__doc__)

    def help_build(self):
        print(BuildHandler.__doc__)

    def help_publish(self):
        print(PublishHandler.__doc__)

    def help_hub(self):
        print(HubHandler.__doc__)

    #def help_version(self):
    #    print(VersionHandler.__doc__)

    def help_exit(self):
        print("This command closes the program graciously.")

    def __setup(self):
        # ensure install
        manager.install()
        # Interrupt process (typically CTRL+C or 'delete' char or 'break' key)
        signal_num = signal.SIGINT
        handler = lambda signum, frame, self=self: _exit_handler(self)
        signal.signal(signal_num, handler)


def _exit_handler(cmdline):
    cmdline.onecmd("exit")
    cmdline.postloop()
    sys.exit()
