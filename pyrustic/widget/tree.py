import tkinter as tk
from pyrustic.abstract.viewable import Viewable


class Tree(Viewable):
    """
    To use Tree, you need to subclass it.
    pyrustic.widget.tree.SimpleTree is a nice example.
    """
    def __init__(self,
                 master=None,
                 indent=50,
                 spacing=10,
                 options={}):
        """
        - master: widget parent
        - indent: indentation to Left
        - spacing: space between two nodes
        - options: dictionary, these options will be used as argument to the widget's constructors.
            The widgets are: body, node_frame, header_frame, and box_frame.
            Example: Assume that you want to set the node_frame's background to black
            and the body's background to red:
                options = {"body": {"background": "red"},
                           "node_frame": {"background": "black"}}
        """
        self.__options = options
        self.__body_options = None
        self.__node_frame_options = None
        self.__master = master
        self.__indent = indent
        self.__spacing = spacing
        self.__body = None
        self.__nodes = {}
        self.__root = None
        self.__internal_count = 0
        self.__cache = None
        # build
        self.build()

    # ==============================================
    #                   PROPERTIES
    # ==============================================
    @property
    def indent(self):
        return self.__indent

    @property
    def spacing(self):
        return self.__spacing

    @property
    def options(self):
        return self.__options

    @property
    def body(self):
        return self.__body

    @property
    def root(self):
        return self.__root

    @property
    def nodes(self):
        return self.__nodes.copy()

    # ==============================================
    #                 PUBLIC METHODS
    # ==============================================
    def insert(self, parent=None, title="", index="end",
               tags={}, container=True, expand=False):
        """
        Insert a node.
        - parent: the node_id of the parent or None if this is the root node of the tree
        - title: string
        - index: an integer to indicate where to put the node between its parent's children.
            Put "end" to put the node at the end of children
        - tags: it is a dictionary to contain whatever data you want. It could help later.
        - container: boolean. True, if the node should contain another node. False else.
        - expand: boolean, True if this node should be expanded from creation. False else.
        Return:
            None if failed to insert the node, else return the newly created node_id
        """
        # a root node shouldn't have a parent and should have index "end"
        if not self.__nodes:
            if parent is not None or (index != "end"):
                return None
        # a non-root should be legal
        elif not self.__check_non_root_node_is_legal(parent, index):
            return None
        # create node and return its id
        return self.__build_node(parent, title, index, tags, container, expand)

    def node(self, id_or_path):
        """
        Get a node by its id or its dotted path.
        A node is a dictionary of data:
        node = {"parent": int, "node_id": int, "container": bool,
                         "index": int, "tags": dict, "expanded": bool,
                         "node_frame": Frame, "header_frame": Frame, "box_frame": Frame,
                         "attached": bool, "ghosted": bool}
        """
        node = None
        if isinstance(id_or_path, str):
            node = self.__node_from_path(id_or_path)
        elif isinstance(id_or_path, int):
            node = self.__get_node(id_or_path)
        if node:
            return node.copy()

    def children(self, node_id):
        """
        List of children nodes.
        Each node is a dictionary of data:
        node = {"parent": int, "node_id": int, "container": bool,
                         "index": int, "tags": dict, "expanded": bool,
                         "node_frame": Frame, "header_frame": Frame, "box_frame": Frame,
                         "attached": bool, "ghosted": bool}
        """
        return [(node["node_id"],
                 node["index"],
                 node["container"]) for key, node in self.__nodes.items()
                                        if node["parent"] == node_id]

    def expand(self, node_id):
        """
        Expand this node. Returns True if it worked
        """
        node = self.__get_node(node_id)
        if node and node["container"] and not node["expanded"]:
            node["expanded"] = True
            #node["expander_stringvar"].set("-")
            self._on_expand(node)
            node["box_frame"].grid(row=1, column=0)
            return True
        return False

    def collapse(self, node_id):
        """
        Collapse this node. Returns True if it worked
        """
        node = self.__get_node(node_id)
        if node and node["container"] and node["expanded"]:
            node["expanded"] = False
            #node["expander_stringvar"].set("+")
            self._on_collapse(node)
            node["box_frame"].grid_remove()
            return True
        return False

    def expanded(self, node_id):
        """
        Returns True if this node is actually expanded, else returns False
        """
        node = self.__get_node(node_id)
        if node:
            return node["expanded"]
        return None

    def collexp(self, node_id):
        """
        Useful method to collapse or to expand a node if it was expanded or collapsed respectively
        """
        if not self.collapse(node_id):
            self.expand(node_id)

    def title(self, node_id, title=None):
        """
        Set a title to a node.
        Returns this node's title if you don't set a title as argument
        """
        node = self.__get_node(node_id)
        data = None
        if node:
            if title:
                node["title_stringvar"].set(title)
            data = node["title_stringvar"].get()
        return data

    def tag(self, node_id, tags={}):
        """
        Edit this node's tags.
        Return the tags
        """
        node = self.__get_node(node_id)
        if not node:
            return
        for key, value in tags.items():
            node["tags"][key] = value
        return node["tags"].copy()

    def untag(self, node_id, tags=[]):
        """
        Edit this node's tags.
        Return the tags
        """
        node = self.__get_node(node_id)
        if node:
            for tag in tags:
                try:
                    del node["tags"][tag]
                except KeyError:
                    pass

    def delete(self, node_id):
        """
        Delete this node.
        Returns True or False
        """
        for key, node in self.__nodes.items():
            if key == node_id:
                if node["container"]:
                    for child in self.children(node_id):
                        self.delete(child[0])
                node["node_frame"].destroy()
                del self.__nodes[key]
                return True
        return False

    def clear(self, node_id):
        """
        Delete the children of this node
        """
        children = self.children(node_id)
        for child in children:
            self.delete(child[0])

    def move(self, node_id, to, index):
        """
        Move a node to another index
        """
        node = self.__get_node(node_id)
        parent_node = self.__get_node(to)
        if not node or not parent_node:
            return False
        if not self.__check_non_root_node_is_legal(to, index):
            return False
        if isinstance(index, int):
            if index < len([node for key, node in self.__nodes.items() if node["parent"] == to]):
                self.__relocate(to, index, direction="+")
        node["parent"] = to
        node["index"] = index
        node["node_frame"].grid_remove()
        node["node_frame"].grid(in_=parent_node["box_frame"], row=index)
        return True

    def walk(self, node_id):
        """
        Walk throughout the node.
        Example:
            for node_id, children in tree.walk(2):
                print(node_id, len(children))
        """
        for key, node in self.__nodes.items():
            if key == node_id:
                if node["container"]:
                    children = self.children(node_id)
                    yield node_id, children
                    for child in children:
                        for a, b in self.walk(child[0]):
                            if a is None:
                                continue
                            yield a, b

    def attach(self, node_id):
        """
        Attach a detached node. Return True if it worked.
        """
        node = self.__get_node(node_id)
        if node and not node["attached"]:
            node["node_frame"].grid()
            node["attached"] = True
            return True
        return False

    def detach(self, node_id):
        """
        Detach an attached node. Return True if it worked.
        The detached node won't be visible anymore, you can't see its children
        """
        node = self.__get_node(node_id)
        if node and node["attached"]:
            node["node_frame"].grid_remove()
            node["attached"] = False
            return True
        return False

    def ghost(self, node_id):
        """
        The header frame of the node disappears ! But you can still see its children.
        You can use it when u want to give illusion that children nodes don't have a root at all
        """
        node = self.__get_node(node_id)
        if node and not node["ghosted"]:
            node["header_frame"].grid_remove()
            node["box_frame"].grid(padx=(0, 0))
            node["node_frame"].grid(pady=(0, 0))
            node["ghosted"] = True
            node["expanded"] = True
            return True
        return False

    def unghost(self, node_id):
        """
        The header frame appears !
        """
        node = self.__get_node(node_id)
        if node and node["ghosted"]:
            node["header_frame"].grid()
            node["box_frame"].grid(padx=(self.__indent, 0))
            node["node_frame"].grid(pady=(self.__spacing, 0))
            node["ghosted"] = False
            return True
        return False

    # ==============================================
    #              OVERRIDABLE
    # ==============================================

    def _on_build_node(self, header_frame, node):
        pass

    def _on_expand(self, node):
        pass

    def _on_collapse(self, node):
        pass

    def _on_display(self):
        pass

    def _on_destroy(self):
        pass

    # ==============================================
    #                 INTERNAL
    # ==============================================
    def _on_build(self):
        self.__body = tk.Frame(master=self.__master, class_="Tree",
                               **self.__options)

    def __build_node(self, parent, title, index, tags, container, expand):
        # Case 1: root node
        if parent is None:
            index = 0
        else:
            children_count = len([node for key, node in self.__nodes.items()
                                  if node["parent"] == parent])
            # Case 2: non-root node with an index "end" or count root children
            if index == "end" or index == children_count:
                if index == "end":
                    index = children_count
            # Case 3: non-root node with an existent index
            elif 0 <= index < children_count:
                # relocate
                self.__relocate(parent, index)
        node_id = self.__internal_count
        self.__internal_count += 1
        node_frame, header_frame, box_frame = self.__build_node_frame(parent,
                                                                      index)
        node = {"parent": parent, "node_id": node_id, "container": container,
                "index": index, "expanded": True, "tags": tags, "title": title,
                "node_frame": node_frame, "header_frame": header_frame,
                "box_frame": box_frame, "attached": True, "ghosted": False}
        self.__nodes[node_id] = node
        if parent is None:
            self.__root = node
        self._on_build_node(header_frame, node.copy())
        if not expand:
            self.collapse(node_id)
        return node_id

    def __build_node_frame(self, parent, index):
        # node frame
        master = self.__body if parent is None else self.__get_node(parent)["box_frame"]
        master.columnconfigure(0, weight=1)
        node_frame = tk.Frame(master, class_="TreeNode")
        node_frame.columnconfigure(0, weight=1)
        # grid node_frame
        if parent is None:
            node_frame.grid(column=0, row=0, sticky="we")
        else:
            node_frame.grid(column=0, row=index,
                            sticky="we", pady=(self.__spacing, 0))
        # header
        header_frame = tk.Frame(node_frame, name="treeHeader")
        header_frame.columnconfigure(0, weight=1)
        header_frame.grid(row=0, column=0, sticky="we")
        # box
        box_frame = tk.Frame(node_frame, name="treeBox")
        box_frame.grid(row=1, column=0,
                       padx=(self.__indent, 0),
                       sticky="we")
        return node_frame, header_frame, box_frame

    def __relocate(self, parent, from_index, direction="+"):
        """
        direction = - or +
        """
        if direction not in ("+", "-"):
            return
        for key, node in self.__nodes.items():
            if node["parent"] == parent and node["index"] >= from_index:
                if direction == "-":
                    node["index"] -= 1
                elif direction == "+":
                    node["index"] += 1
                node["node_frame"].grid(column=0, row=node["index"])

    def __check_non_root_node_is_legal(self, parent, index):
        # a non-root node should have a parent
        if parent is None:
            return False
        # a non-root node should have an existent parent
        if parent not in [key for key, node in self.__nodes.items()]:
            return False
        # a non-root node should have a legal index: "end" or an integer value
        if isinstance(index, str) and index != "end":
            return False
        elif isinstance(index, int):
            # a non-root node should have an index that exists or is the last index +1
            if not (0 <= index <= len([node for key, node in self.__nodes.items()
                                            if node["parent"] == parent])):
                return False
        return True

    def __get_node(self, node_id):
        if self.__cache:
            if self.__cache["node_id"] == node_id:
                return self.__cache
        for key, node in self.__nodes.items():
            if key == node_id:
                self.__cache = node
                return node
        return None

    def __node_from_path(self, path):
        path = path.split(".")
        if not path or path[0] != "0":
            return
        current_container = 1
        cache = 1
        del path[0]
        for index in path:
            try:
                index = int(index)
            except Exception:
                return
            children = self.children(current_container)
            if not children:
                return
            for child in children:
                if child[1] == index:
                    cache = node[0]
                    current_container = node[0]
                    break
        return self.__get_node(cache)


# ====================================
#              DEMO
# ====================================
class SimpleTree(Tree):
    def __init__(self, master):
        super().__init__(master=master)
        self._nodes = dict()

    def _on_build_node(self, header_frame, node):
        expander_stringvar = tk.StringVar()
        title_stringvar = tk.StringVar()
        self._nodes[node["node_id"]] = {"expander_stringvar": expander_stringvar,
                                           "title_stringvar": title_stringvar}
        node_id = node["node_id"]
        title = node["title"]
        container = node["container"]
        # Header_1 - contains Expander_btn and title_label
        titlebar = tk.Frame(header_frame, name="treeTitlebar")
        titlebar.grid(row=0, column=0, sticky="we")
        titlebar.columnconfigure(1, weight=1)
        # Header_2 - is a frame
        toolbar = tk.Frame(header_frame, name="treeToolbar")
        toolbar.grid(row=1, column=0, sticky="we")
        #
        if container:
            expander_stringvar.set("+")
            expander_btn = tk.Button(titlebar, name="treeExpander",
                                     textvariable=expander_stringvar,
                                     padx=0, pady=0,
                                     command=lambda self=self, node_id=node_id:
                                     self.collexp(node_id))
            expander_btn.grid(row=0, column=0)
        title_stringvar.set(title)
        title_label = tk.Label(titlebar, name="treeTitleLabel",
                               anchor="w", textvariable=title_stringvar)
        title_label.grid(row=0, column=1, sticky="we")

    def _on_collapse(self, node):
        node_id = node["node_id"]
        self._nodes[node_id]["expander_stringvar"].set("+")

    def _on_expand(self, node):
        node_id = node["node_id"]
        self._nodes[node_id]["expander_stringvar"].set("-")


if __name__ == "__main__":

    app = tk.Tk()
    app.geometry("500x500+0+0")
    tree = SimpleTree(app)
    tree.build()
    tree.body.pack(side=tk.LEFT, anchor="nw")

    # insertion
    world_id = tree.insert(title="World")
    africa_id = tree.insert(title="Africa", parent=world_id)
    america_id = tree.insert(title="America", parent=world_id)
    asia_id = tree.insert(title="Asia", parent=world_id)
    europe_id = tree.insert(title="Europe", parent=world_id)
    #
    france_id = tree.insert(title="France", parent=europe_id)
    italia_id = tree.insert(title="Italie", parent=europe_id)
    china_id = tree.insert(title="China", parent=asia_id)
    japon_id = tree.insert(title="Japon", parent=asia_id)
    usa_id = tree.insert(title="USA", parent=america_id)
    mexique_id = tree.insert(title="Mexique", parent=america_id)
    ghana_id = tree.insert(title="Ghana", parent=africa_id)
    morroco_id = tree.insert(title="Maroc", parent=africa_id)
    tunisia_id = tree.insert(title="Tunisia", parent=africa_id)
    #
    paris_id = tree.insert(title="Paris", parent=france_id, container=False)
    accra_id = tree.insert(title="Accra", parent=ghana_id, container=False)
    tunis_id = tree.insert(title="Tunis", parent=tunisia_id, container=False)
    rabbat_id = tree.insert(title="Rabbat", parent=morroco_id, container=False)
    tokyo_id = tree.insert(title="Tokyo", parent=japon_id, container=False)
    path = "0.1.0.0"
    for node, children in tree.walk(world_id):
        print(node, children)

    #tree.ghost(1)
    #tree.unghost(1)
    app.mainloop()
