from pyrustic.threadium import Threadium
from runtest.host.main_host import MainHost
from runtest.host.result import Result
from runtest.host.reloader import Reloader
from runtest.view.log_window import LogWindow
from runtest.view.toolbar import Toolbar
from runtest.view.tree import Tree
from runtest.view.main_view import MainView
import os
import os.path
from common import funcs


class MainHostBuilder:
    def build(self, root_path):
        return MainHost(root_path, Reloader(), ResultBuilder())


class ResultBuilder:
    def build(self, test_id, queue):
        return Result(test_id, queue)


class LogWindowBuilder:
    def build(self, master, message):
        return LogWindow(master, message).build_wait()


class ToolbarBuilder:
    def build(self, node_id, parent, callback):
        toolbar = Toolbar(node_id, parent, callback, LogWindowBuilder())
        toolbar.build()
        return toolbar


class TreeBuilder:
    def build(self, master, callback):
        return Tree(master, callback)


class MainViewBuilder:
    def build(self, app):
        jasonix = funcs.get_manager_jasonix()
        target = jasonix.data["target"]
        tests_path = os.path.join(target, "tests")
        return MainView(app,
                        Threadium(app.root),
                        MainHostBuilder().build(target),
                        ToolbarBuilder(),
                        tests_path)
