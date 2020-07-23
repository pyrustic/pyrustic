from tool.sqluna.dao.internal_dao import InternalDao
from tool.sqluna.dao.external_dao import ExternalDao
from tool.sqluna.host.main_host import MainHost
from tool.sqluna.host.internal_data_manager import InternalDataManager
from tool.sqluna.view.main_view import MainView
from tool.sqluna.view.header import Header
from tool.sqluna.view.tree import Tree
from tool.sqluna.view.footer import Footer
from tool.sqluna.view.editor import Editor
from tool.sqluna.view.nodebar import Nodebar
import sys
import about
import os.path
from pyrustic.dao import Dao


class InternalDaoBuilder:
    def build(self):
        path = os.path.join(about.ROOT_DIR,
                            "cache",
                            "sqluna",
                            "internal_database")
        creational_script = os.path.join(about.ROOT_DIR,
                                         "tool",
                                         "sqluna",
                                         "misc",
                                         "creational_script_internal_database")
        dao = Dao(path, creational_script=("file", creational_script))
        return InternalDao(dao)


class ExternalDaoBuilder:
    def build(self, path):
        dao = Dao(path)
        return ExternalDao(dao)


class InternalDataManagerBuilder:
    def build(self):
        dao = InternalDaoBuilder().build()
        return InternalDataManager(dao)


class MainHostBuilder:
    def build(self):
        return MainHost(ExternalDaoBuilder())


class MainViewBuilder:
    def build(self, app):
        project = sys.argv[1] if len(sys.argv) == 2 else os.getcwd()
        main_host = MainHostBuilder().build()
        internal_data_manager = InternalDataManagerBuilder().build()
        return MainView(app, project, main_host, internal_data_manager,
                        HeaderBuilder(), TreeBuilder(), FooterBuilder())


class HeaderBuilder:
    def build(self, parent_view, host, internal_database_manager, project):
        header = Header(parent_view, host, internal_database_manager, project)
        return header


class TreeBuilder:
    def build(self, parent_view, box, host):
        tree = Tree(parent_view, box, NodebarBuilder(), host)
        return tree


class FooterBuilder:
    def build(self, parent_view, main_host, project):
        footer = Footer(parent_view, main_host, EditorBuilder(project))
        return footer

class EditorBuilder:
    def __init__(self, project):
        self._project = project

    def build(self, parent_view):
        editor = Editor(parent_view, self._project)
        return editor

class NodebarBuilder:
    def build(self, parent_view, node_id,
              collapsable_frame, file, path,
              real_path, result, datatype,
              description):
        node = Nodebar(parent_view, node_id,
                       collapsable_frame, file, path, real_path,
                       result, datatype,
                       description)
        return node
