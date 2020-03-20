import cmd
import os.path
from core.misc import funcs
from core.handler.make_handler import MakeHandler
from core.handler.dao_handler import DaoHandler
from core.handler.package_handler import PackageHandler
from core.handler.host_handler import HostHandler
from core.handler.import_handler import ImportHandler
from core.handler.misc_handler import MiscHandler
from core.handler.feed_handler import FeedHandler
from core.handler.sync_handler import SyncHandler
from core.handler.view_handler import ViewHandler
from core.handler.target_handler import TargetHandler
from core.handler.switch_handler import SwitchHandler
from core.handler.version_handler import VersionHandler
from core.handler.tutorial_handler import TutorialHandler
import about


def beta(func):
    def exec(self, arg):
        #func(self, funcs.split_arg(arg))
        #return
        try:
            func(self, funcs.split_arg(arg))
        except Exception as e:
            print("Beta version here. Exception occured ! \n", e)
    return exec


def get_target():
    if not PyruShell.pyr_target:
        return None
    if not os.path.exists(PyruShell.pyr_target):
        PyruShell.pyr_target = None
    return PyruShell.pyr_target


class PyruShell(cmd.Cmd):
    intro = ("Welcome to Pyrustic Platform Shell\n"
            + "March 20, 2020 - - - "
            + "(version " + about.VERSION + " build " + about.BUILD + ")\n"
            + "Type help or ? to list commands.\n")
    prompt = "(pyrushell) "
    file = None
    pyr_target = None

    def postcmd(self, stop, line):
        print("")
        return stop

    def do_EOF(self, line):
        return True

    # ----------- COMMANDS ----------
    @beta
    def do_feed(self, arg):
        FeedHandler(get_target(), arg)

    @beta
    def do_sync(self, arg):
        SyncHandler(get_target(), arg)

    @beta
    def do_target(self, arg):
        target_handler = TargetHandler(get_target(), arg)
        PyruShell.pyr_target = target_handler.target

    @beta
    def do_make(self, arg):
        make_handler = MakeHandler(get_target(), arg)
        PyruShell.pyr_target = make_handler.target

    @beta
    def do_import(self, arg):
        ImportHandler(get_target(), arg)

    @beta
    def do_package(self, arg):
        PackageHandler(get_target(), arg)

    @beta
    def do_switch(self, arg):
        SwitchHandler(arg)

    @beta
    def do_version(self, arg):
        VersionHandler(arg)

    @beta
    def do_dao(self, arg):
        DaoHandler(get_target(), arg)

    @beta
    def do_host(self, arg):
        HostHandler(get_target(), arg)

    @beta
    def do_view(self, arg):
        ViewHandler(get_target(), arg)

    @beta
    def do_misc(self, arg):
        MiscHandler(get_target(), arg)

    @beta
    def do_tutorial(self, arg):
        print(TutorialHandler.__doc__)

    # -------------- HELP -----------------
    def help_feed(self):
        print(FeedHandler.__doc__)

    def help_sync(self):
        print(SyncHandler.__doc__)

    def help_target(self):
        print(TargetHandler.__doc__)

    def help_make(self):
        print(MakeHandler.__doc__)

    def help_import(self):
        print(ImportHandler.__doc__)

    def help_package(self):
        print(PackageHandler.__doc__)

    def help_switch(self):
        print(SwitchHandler.__doc__)

    def help_version(self):
        print(VersionHandler.__doc__)

    def help_dao(self):
        print(DaoHandler.__doc__)

    def help_host(self):
        print(HostHandler.__doc__)

    def help_view(self):
        print(ViewHandler.__doc__)

    def help_misc(self):
        print(MiscHandler.__doc__)

    def help_tutorial(self):
        print(TutorialHandler.__doc__)

    def help_EOF(self):
        print("Ctrl+D to leave")