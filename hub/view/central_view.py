import tkinter as tk
from pyrustic.viewable import Viewable
from pyrustic.widget.scrollbox import Scrollbox
from hub.view.tree_view import TreeView


class CentralView(Viewable):
    def __init__(self, master, main_view, main_host):
        self._master = master
        self._main_view = main_view
        self._main_host = main_host
        self._body = None
        self._tree_view = None

    @property
    def tree_view(self):
        return self._tree_view

    @property
    def scrollbox(self):
        return self._scrollbox

    # ===============================
    #            PROPERTY
    # ===============================

    # ===============================
    #            PUBLIC
    # ===============================

    def add_node(self, owner, repo):
        self._main_host.update_activity("add", owner, repo)
        self._collapse_nodes()
        self._tree_view.feed(datatype="add_owner_repo",
                             data=(owner, repo))

    # ===============================
    #            LIFECYCLE
    # ===============================
    def _on_build(self):
        self._body = tk.Frame(self._master)
        # scrollbox
        self._scrollbox = Scrollbox(self._body, orient="v")
        self._scrollbox.build_pack(expand=1, fill=tk.BOTH)
        # treeview
        self._tree_view = TreeView(self._scrollbox.box, self._main_view, self._main_host)
        self._tree_view.build_pack(expand=1, fill=tk.BOTH)
        # insert ghost root node
        self._insert_ghost_root()

    def _on_display(self):
        pass

    def _on_destroy(self):
        pass

    # ===============================
    #            PRIVATE
    # ===============================
    def _insert_ghost_root(self):
        # insert first node
        node_id = self._tree_view.insert()
        self._tree_view.ghost(node_id)

    def _collapse_nodes(self):
        for owner in self._tree_view.nodes:
            owner_node_id = owner["node_id"]
            if owner_node_id == 0:
                continue
            else:
                self._tree_view.collapse(owner_node_id)
