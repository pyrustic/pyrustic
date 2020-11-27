from pyrustic.viewable import Viewable
import tkinter as tk


class NodeView(Viewable):
    def __init__(self, master, tree_view, main_view, main_host, node_id):
        self._master = master
        self._tree_view = tree_view
        self._main_view = main_view
        self._main_host = main_host
        self._node_id = node_id
        self._body = None
        self._strvar_expand = tk.StringVar()

    def edit_state(self, expanded=True):
        self._strvar_expand.set("-" if expanded else "+")

    def feed(self, datatype, data=None):
        if not self._node_still_exists():
            return
        status_code, status_text, data = data
        if status_code in (200, 304):
            success_layouts = {"description": self._set_description_layout,
                       "latest_release": self._set_latest_release_layout,
                       "total_downloads": self._set_total_downloads_layout}
            if datatype in success_layouts:
                success_layouts[datatype](data)
        else:
            self._set_failure_layout(datatype, status_code, status_text)

    def _on_build(self):
        self._body = tk.Frame(self._master)
        node = self._tree_view.node(self._node_id)
        data = node["data"]
        node_type = data["type"]
        if node_type in ("owner", "repo"):
            command = (lambda node_type=node_type:
                       self._on_click_button_expand(node_type))
            button_expand = tk.Button(self._body,
                                      name="button_expander",
                                      textvariable=self._strvar_expand,
                                      command=command)
            button_expand.pack(side=tk.LEFT, padx=2)
            instance_name = "label_owner" if node_type == "owner" else "label_repo"
            label = tk.Label(self._body, name=instance_name, text=data["name"])
            label.pack(side=tk.LEFT)
            command = self._on_click_button_close
            button_delete = tk.Button(self._body,
                                      name="button_close",
                                      text="x",
                                      command=command)
            button_delete.pack(side=tk.LEFT, padx=(10, 0))

    def _on_display(self):
        node = self._tree_view.node(self._node_id)
        expanded = node["expanded"]
        cache = "+"
        if expanded:
            cache = "-"
        self._strvar_expand.set(cache)

    def _on_destroy(self):
        pass

    def _on_click_button_expand(self, node_type):
        self._collexp_node()

    def _on_click_button_close(self):
        # get data from node
        node = self._tree_view.node(self._node_id)
        owner = None
        repo = None
        node_type = node["data"]["type"]
        node_name = node["data"]["name"]
        if node_type == "owner":
            owner = node_name
        else:
            repo = node_name
            parent_node = self._tree_view.node(node["parent"])
            owner = parent_node["data"]["name"]
        self._main_host.update_activity("delete", owner, repo)
        self._tree_view.delete(self._node_id)

    def _collexp_node(self):
        cache = "+"
        if self._strvar_expand.get() == "+":
            cache = "-"
        self._strvar_expand.set(cache)
        self._tree_view.collexp(self._node_id)

    def _set_loading_mode(self):
        node = self._tree_view.node(self._node_id)
        data = node["data"]
        self._clear_node()
        # label title
        label_title = tk.Label(self._body, name="label_info_title",
                               text="{}: ".format(data["name"]))
        label_title.pack(side=tk.LEFT, padx=0)
        # label info
        label_info = tk.Label(self._body, text="Loading...")
        label_info.pack(side=tk.LEFT, padx=0)

    def _clear_node(self):
        for child in self._body.winfo_children():
            child.destroy()

    def _set_description_layout(self, data):
        self._clear_node()
        # title
        text = self._tree_view.node(self._node_id)["data"]["name"]
        label_title = tk.Label(self._body, name="label_info_title", text=text)
        label_title.grid(column=0, row=0, sticky="w")
        # description
        text = data["description"]
        text = "- No description -" if text is None else text
        entry_description = tk.Entry(self._body, name="entry_repo_description",
                                     width=70)
        entry_description.insert(0, text)
        entry_description.config(state="readonly")
        entry_description.grid(column=0, row=1, sticky="w")
        # creation date
        text = "Created on {} UTC".format(data["created_at"])
        label_date = tk.Label(self._body, text=text)
        label_date.grid(column=0, row=2, sticky="w")
        # stargazers/subscribers
        stargazers_count = data["stargazers_count"]
        subscribers_count = data["subscribers_count"]
        suffix_str_stargazers = "s" if stargazers_count > 1 else ""
        suffix_str_subscribers = "s" if subscribers_count > 1 else ""
        text = "{} Stargazer{} and {} Subscriber{}".format(stargazers_count,
                                                           suffix_str_stargazers,
                                                           subscribers_count,
                                                           suffix_str_subscribers)
        label_stargazers = tk.Label(self._body, name="label_counts",
                                    text=text)
        label_stargazers.grid(column=0, row=3, sticky="w")
        # button refresh
        button_refresh = tk.Button(self._body, name="button_refresh",
                                   text="Refresh", command=self.populate)
        button_refresh.grid(column=0, row=4, sticky="w", pady=5)

    def _set_latest_release_layout(self, data):
        self._clear_node()
        # title
        text = self._tree_view.node(self._node_id)["data"]["name"]
        label_title = tk.Label(self._body, name="label_info_title", text=text)
        label_title.grid(column=0, row=0, sticky="w")
        # name
        text = "Tag name: {}".format(data["tag_name"])
        label_name = tk.Label(self._body, text=text)
        label_name.grid(column=0, row=1, sticky="w")
        # creation date
        text = "Published on {} UTC".format(data["published_at"])
        label_date = tk.Label(self._body, text=text)
        label_date.grid(column=0, row=2, sticky="w")
        # downloads
        downloads_count = data["downloads_count"]
        suffix_str_downloads = "s" if downloads_count > 1 else ""
        text = "{} Download{}".format(downloads_count, suffix_str_downloads)
        label_downloads = tk.Label(self._body, name="label_counts",
                                   text=text)
        label_downloads.grid(column=0, row=3, sticky="w")
        # button refresh
        button_refresh = tk.Button(self._body,
                                   name="button_refresh",
                                   text="Refresh", command=self.populate)
        button_refresh.grid(column=0, row=4, sticky="w", pady=5)

    def _set_total_downloads_layout(self, data):
        self._clear_node()
        # title
        text = self._tree_view.node(self._node_id)["data"]["name"]
        label_title = tk.Label(self._body, name="label_info_title", text=text)
        label_title.grid(column=0, row=0, sticky="w")
        # name
        suffix_str_downloads = "s" if data > 1 else ""
        text = "{} Download{}".format(data, suffix_str_downloads)
        label_downloads = tk.Label(self._body, name="label_counts",
                                   text=text)
        label_downloads.grid(column=0, row=1, sticky="w")
        # button refresh
        button_refresh = tk.Button(self._body, name="button_refresh",
                                   text="Refresh", command=self.populate)
        button_refresh.grid(column=0, row=2, sticky="w", pady=5)

    def _set_failure_layout(self, datatype, status_code, status_text):
        self._clear_node()
        name = self._tree_view.node(self._node_id)["data"]["name"]
        # frame
        frame_title = tk.Frame(self._body)
        frame_title.grid(column=0, row=0, sticky="w")
        # label title failure
        label_title = tk.Label(frame_title, name="label_info_title",
                               text="{}: ".format(name))
        label_title.pack(side=tk.LEFT, padx=0)
        # label info
        label_info = tk.Label(frame_title, name="label_error",
                              text=status_text)
        label_info.pack(side=tk.LEFT, padx=0)
        # button
        button_retry = tk.Button(self._body, name="button_retry",
                                 text="Retry", command=self.populate)
        button_retry.grid(column=0, row=1, sticky="w", pady=5)

    def populate(self):
        self._set_loading_mode()
        node = self._tree_view.node(self._node_id)
        node_type = node["data"]["type"]
        repo_node = self._tree_view.node(node["parent"])
        owner_node = self._tree_view.node(repo_node["parent"])
        repo = repo_node["data"]["name"]
        owner = owner_node["data"]["name"]
        threadium = self._main_view.threadium
        host_choice = {"description": self._main_host.repo_description,
                       "latest_release": self._main_host.latest_release,
                       "total_downloads": self._main_host.latest_releases_downloads}
        host = host_choice[node_type]
        host_args = (owner, repo)
        consumer = (lambda data, datatype=node_type,
                           self=self:
                    self.feed(datatype, data=data))
        threadium.task(host, args=host_args, consumer=consumer)

    def _node_still_exists(self):
        if self._tree_view.node(self._node_id) is None:
            return False
        return True
