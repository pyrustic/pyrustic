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
from pyrustic.manager.handler.version_handler import VersionHandler
from pyrustic.manager import pymisc, get_app_pkg
import os


HANDLERS = {"add": AddHandler, "build": BuildHandler,
            "hub": HubHandler, "init": InitHandler,
            "link": LinkHandler, "publish": PublishHandler,
            "recent": RecentHandler, "relink": RelinkHandler,
            "run": RunHandler, "target": TargetHandler,
            "unlink": UnlinkHandler, "version": VersionHandler}


def command(line=None, target=None):
    """
    Param:
        - line is a string or a list. Example "link /home/project" or ["link", "/home/proj"]
        - target is a path string
    """
    args = None
    if not line:
        return
    if isinstance(line, str):
        args = pymisc.parse_cmd(line)
    else:
        args = line
    app_pkg = get_app_pkg(target)
    if not target:
        target = os.getcwd()
    operation = args[0]
    args = args[1:]
    if operation == "help":
        _show_help(args)
        return
    try:
        HANDLERS[operation](target, app_pkg, *args)
    except KeyError:
        print("Unknown operation")
    except Exception as e:
        raise e
        print("error: ", e)
        print("Oops an error occurred")


def _show_help(args):
    if not args:
        print("Type 'help <operation>' to access the doc.")
        print("Available operations: ")
        for key in HANDLERS.keys():
            print(" - {}".format(key))
        return
    if len(args) > 1:
        print("Incorrect usage of the help command.")
        return
    operation = args[0]
    try:
        print(HANDLERS[operation].__doc__)
    except KeyError:
        print("Unknown operation")
    except Exception:
        print("Oops an error occurred")
