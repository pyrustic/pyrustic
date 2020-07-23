import tkinter as tk
from pyrustic.widget.tree import Tree


class Tree(Tree):
    def __init__(self, master, callback):
        super().__init__(master=master, spacing=20)
        self._callback = callback
        self._nodes = dict()

    def _on_build_node(self, header_frame, node):
        title = node["title"]
        node_id = node["node_id"]
        node_type = node["tags"]["type"]
        container = node["container"]
        expander_stringvar = tk.StringVar()
        title_one_stringvar = tk.StringVar()
        title_two_stringvar = tk.StringVar()
        self._nodes[node_id] = {"expander_stringvar": expander_stringvar,
                                "title_one_stringvar": title_one_stringvar,
                                "title_two_stringvar": title_two_stringvar}
        # Titlebar
        titlebar = tk.Frame(header_frame)
        titlebar.grid(row=0, column=0, sticky="we")
        #titlebar.bindtags((str(node_id),))
        # Toolbar
        toolbar = tk.Frame(header_frame)
        toolbar.columnconfigure(0, weight=1)
        toolbar.grid(row=1, column=0, sticky="we")
        # expander
        if container:
            expander_stringvar.set("+")
            command = lambda self=self, node_id=node_id: self.collexp(node_id)
            expander = tk.Button(titlebar,
                                 name="treeExpanderButton",
                                 textvariable=expander_stringvar,
                                 command=command)
            expander.grid(row=0, column=0, sticky="w", padx=(0, 5))
        # titlelabel_one
        title_one_stringvar.set(node_type)
        titlelabel_one = tk.Label(titlebar,
                                  name="treeTitleLabelOne",
                                  textvariable=title_one_stringvar)
        titlelabel_one.grid(row=0, column=1, sticky="w", padx=(0, 5))
        # titlelabel_two
        title_two_stringvar.set(title)
        titlelabel_two = tk.Label(titlebar,
                                  name="treeTitleLabelTwo",
                                  textvariable=title_two_stringvar)
        titlelabel_two.grid(row=0, column=2, sticky="w")
        # binding command to titlebar, so callback will trigger toolbar
        command = (lambda event,
                          self=self,
                          toolbar=toolbar,
                          node=node: self._callback.on_title_clicked(node, toolbar))
        titlelabel_one.bind("<Button-1>", command)
        titlelabel_two.bind("<Button-1>", command)

    def _on_collapse(self, node):
        node_id = node["node_id"]
        self._nodes[node_id]["expander_stringvar"].set("+")
        self._callback.on_node_collapsed(node)

    def _on_expand(self, node):
        node_id = node["node_id"]
        self._nodes[node_id]["expander_stringvar"].set("-")
        self._callback.on_node_expanded(node)
