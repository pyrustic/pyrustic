import tkinter as tk
from pyrustic.widget.tree import Tree as PyrusticTree


class Tree(PyrusticTree):
    def __init__(self, parent_view, box, nodebar_builder, host):
        super().__init__(master=box, spacing=20)
        self._parent_view = parent_view
        self._nodebar_builder = nodebar_builder
        self._host = host
        self._nodes = dict()

    def on_change_database(self, path):
        self._parent_view.open_database(path)

    def on_click_truncate(self, table):
        sql = "DELETE FROM {}".format(table)
        formatter = "inline"
        self._parent_view.push_sql(sql, formatter, execute=True)

    def on_click_drop(self, table):
        sql = "DROP TABLE {}".format(table)
        formatter = "inline"
        self._parent_view.push_sql(sql, formatter, execute=True)

    def on_click_explore(self, table):
        sql = "SELECT * FROM {}".format(table)
        formatter = "inline"
        self._parent_view.push_sql(sql, formatter, execute=True)

    def _on_build_node(self, header_frame, node):
        if node["node_id"] == 0:
            return
        # some vars
        title = node["title"]
        node_id = node["node_id"]
        result = node["data"]["result"]
        datatype = node["data"]["type"]
        description = node["data"]["description"]
        file = node["data"]["file"]
        path = node["data"]["path"]
        real_path = node["data"]["realpath"]
        formatter = node["data"]["formatter"]
        # stringvars
        stringvar_expander = tk.StringVar()
        stringvar_title = tk.StringVar()

        # Populate stringvars
        stringvar_expander.set("-" if node["expanded"] else "+")
        stringvar_title.set(title)
        # config header frame
        header_frame.columnconfigure(0, weight=0)
        header_frame.columnconfigure(1, weight=0)
        header_frame.columnconfigure(2, weight=1)
        # collapsable_frame
        collapsable_frame = tk.Frame(header_frame, class_="CollapsableFrame")
        collapsable_frame.columnconfigure(0, weight=1)
        # - install
        collapsable_frame.grid(row=1, column=2, sticky="w", padx=(0, 20))
        # Fill titlebar
        # - button expander
        command = lambda self=self, node_id=node_id: self.collexp(node_id)
        button_expander = tk.Button(header_frame,
                                    name="treeExpanderButton",
                                    textvariable=stringvar_expander,
                                    command=command)
        # - button edit
        button_edit = tk.Button(header_frame,
                                text="edit",
                                name="buttonEdit",
                                command=lambda self=self, node_id=node_id:
                                    self._on_click_edit(node_id))
        # - entry title
        entry_title = tk.Entry(header_frame, name="treeTitle",
                               state="readonly",
                               textvariable=stringvar_title)
        entry_title.bind("<Button-1>",
                         lambda e, self=self, node_id=node_id:
                            self._on_click_sql(node_id))
        # - install
        button_expander.grid(row=0, column=0, padx=(0, 5), sticky="w")
        button_edit.grid(row=0, column=1, padx=(0, 5), sticky="w")
        entry_title.grid(row=0, column=2, sticky="nswe")
        # Fill collapsable frame
        nodebar = self._nodebar_builder.build(self, node_id, collapsable_frame,
                                              file, path, real_path, result,
                                              datatype, description)
        # save data
        self._nodes[node_id] = {"stringvar_expander": stringvar_expander,
                                "stringvar_title": stringvar_title,
                                "collapsable_frame": collapsable_frame,
                                "nodebar": nodebar,
                                "formatter": formatter}

    def _on_expand(self, node):
        node_id = node["node_id"]
        if node_id == 0:
            return
        self._nodes[node_id]["stringvar_expander"].set("-")
        self._nodes[node_id]["collapsable_frame"].grid()

    def _on_collapse(self, node):
        node_id = node["node_id"]
        if node_id == 0:
            return
        self._nodes[node_id]["stringvar_expander"].set("+")
        self._nodes[node_id]["collapsable_frame"].grid_remove()

    def _on_click_sql(self, node_id):
        self.collexp(node_id)

    def _on_click_edit(self, node_id):
        formatter = self._nodes[node_id]["formatter"]
        sql = self._nodes[node_id]["stringvar_title"].get()
        self._parent_view.push_sql(sql, formatter)
