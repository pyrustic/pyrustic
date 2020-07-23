from pyrustic.threadium import Threadium
from tool.runtest.host.main_host import MainHost
from tool.runtest.host.result import Result
from tool.runtest.host.reloader import Reloader
from tool.runtest.view.log_window import LogWindow
from tool.runtest.view.toolbar import Toolbar
from tool.runtest.view.tree import Tree
from tool.runtest.view.main_view import MainView
import sys
import os
import os.path


class MainHostBuilder:
    def build(self, root_path):
        return MainHost(root_path, Reloader(), ResultBuilder())


class ResultBuilder:
    def build(self, test_id, queue):
        return Result(test_id, queue)


class LogWindowBuilder:
    def build(self, master, message):
        return LogWindow(master, message)


class ToolbarBuilder:
    def build(self, node_id, parent, callback):
        return Toolbar(node_id, parent, callback, LogWindowBuilder())


class TreeBuilder:
    def build(self, master, callback):
        return Tree(master, callback)


class MainViewBuilder:
    def build(self, master):
        root_path = sys.argv[1]
        tests_path = os.path.join(root_path, "tests")
        return MainView(master,
                        Threadium(master),
                        MainHostBuilder().build(root_path),
                        ToolbarBuilder(),
                        tests_path)
