import tkinter as tk
from pyrustic.widget.tree import Tree
from hub.view.node_view import NodeView


class TreeView(Tree):
    def __init__(self, master, main_view, main_host):
        super().__init__(master, spacing=15)
        self._main_view = main_view
        self._main_host = main_host
        self._cache = {}

    # =============================
    #           PUBLIC
    # =============================


    # =============================
    #      IMPLEMENTATION OF TREE
    # =============================
    def _on_display(self):
        # insert first node
        node_id = self.insert()
        self.ghost(node_id)
        # request last activity
        host = self._main_host.last_activity
        consumer = (lambda data, self=self:
                    self.feed(datatype="last_activity", data=data))
        self._main_view.threadium.task(host, consumer=consumer)

    def _on_build_node(self, frame, node):
        node_id = node["node_id"]
        if node_id == 0:
            return
        node_view = NodeView(frame, self, self._main_view, self._main_host, node_id)
        node_view.build_pack(expand=1, fill=tk.X, side=tk.LEFT)
        self.tag(node_id, data={"node_view": node_view})
        node_type = node["data"]["type"]
        if node_type in ("description", "latest_release", "total_downloads"):
            node_view.populate()

    def _on_feed(self, *args, **kwargs):
        datatype = kwargs.get("datatype")
        data = kwargs.get("data")
        if datatype == "last_activity":
            self._load_last_activity(data)
        elif datatype == "add_owner_repo":
            self._add_owner_repo(*data)

    def _on_expand(self, node):
        node_id = node["node_id"]
        node_type = node["data"]["type"]
        node_view = node["data"].get("node_view", None)
        if node_view:
            node_view.edit_state(expanded=True)
        if node_type == "repo" and not self.children(node_id):
            self._insert_repo_sub_nodes(node_id)

    def _on_collapse(self, node):
        node_view = node["data"].get("node_view", None)
        if node_view:
            node_view.edit_state(expanded=False)

    # =============================
    #           PRIVATE
    # =============================
    def _load_last_activity(self, data):
        for owner, repos in data.items():
            # add owner to tree
            data = {"type": "owner", "name": owner}
            node_id = self.insert(parent=0, data=data, expand=True)
            for repo in repos:
                # add repo to owner
                data = {"type": "repo", "name": repo}
                self.insert(parent=node_id, data=data)

    # ===================
    def _request_data(self, node, node_type, node_view):
        repo_node = self.node(node["parent"])
        owner_node = self.node(repo_node["parent"])
        repo = repo_node["data"]["name"]
        owner = owner_node["data"]["name"]
        threadium = self._main_view.threadium
        host_choice = {"description": self._main_host.repo_description,
                       "latest_release": self._main_host.latest_release,
                       "total_downloads": self._main_host.latest_releases_downloads}
        host = host_choice[node_type]
        host_args = (owner, repo)
        consumer = (lambda data, datatype=node_type,
                           node_view=node_view:
                    node_view.feed(datatype, data=data))
        threadium.task(host, args=host_args, consumer=consumer)

    def _add_owner_repo(self, owner, repo):
        owner_node_id = self._add_owner(owner)
        repo_node_id = self._add_repo(owner_node_id, repo)
        # move owner node to top
        self.move(owner_node_id)
        # expand owner node
        self.expand(owner_node_id)
        # pull scrollbar to top
        self._main_view.central_view.scrollbox.yview_moveto(0)
        # expand repo
        self.expand(repo_node_id)

    def _add_owner(self, owner):
        node_id = None
        for node in self.children(0):
            cache = node["data"]["name"]
            if cache.lower() == owner.lower():
                node_id = node["node_id"]
                return node_id
        # add owner to tree
        data = {"type": "owner", "name": owner}
        node_id = self.insert(parent=0, data=data, expand=True, index=0)
        return node_id

    def _add_repo(self, parent_node_id, repo):
        for node in self.children(parent_node_id):
            cache = node["data"]["name"]
            if cache.lower() == repo.lower():
                node_id = node["node_id"]
                self.delete(node_id)
        # add repo
        data = {"type": "repo", "name": repo}
        node_id = self.insert(parent=parent_node_id, data=data, index=0)
        return node_id

    def _insert_repo_sub_nodes(self, node_id):
        # insert Description Node
        data = {"type": "description", "name": "Repository description"}
        self.insert(node_id, container=False, data=data)
        # insert Latest Release Node
        data = {"type": "latest_release", "name": "Latest release"}
        self.insert(node_id, container=False, data=data)
        # insert Total Downloads Node
        data = {"type": "total_downloads", "name": "Latest ten (pre)releases"}
        self.insert(node_id, container=False, data=data)
