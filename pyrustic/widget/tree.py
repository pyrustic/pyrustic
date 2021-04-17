import tkinter as tk
from pyrustic.view import CustomView
from pyrustic import widget
from pyrustic.tkmisc import merge_cnfs
from pyrustic.exception import PyrusticWidgetException


# Components
FRAME_NODE = "frame_node"
FRAME_HEADER = "frame_header"
FRAME_BOX = "frame_box"


class Tree(widget.Frame):
    """
    Tree is the megawidget to use to display the data as a tree.
    To use Tree, you need to subclass it.

    pyrustic.tree.SimpleTree is a nice example to study.

    Scroll to the bottom of this file at the top-level script
    environment to see the usage of SimpleTree
    """
    def __init__(self,
                 master=None,
                 indent=50,
                 spacing=10,
                 cnfs=None):
        """
        PARAMETERS:

        - master: widget parent. Example: an instance of tk.Frame

        - indent: left indent

        - spacing: space between two nodes

        - options: dictionary of widgets options
            The widgets keys are: BODY, NODE_FRAME, HEADER_FRAME, and BOX_FRAME.
            Example: Assume that you want to set the NODE_FRAME's background to black
            and the BODY's background to red:
                options = {BODY: {"background": "red"},
                           NODE_FRAME: {"background": "black"}}
        """
        self.__cnfs = merge_cnfs(None, cnfs, components=("body",
                    FRAME_NODE, FRAME_HEADER, FRAME_BOX))
        super().__init__(master=master,
                         class_="Tree",
                         cnf=self.__cnfs["body"],
                         on_build=self.__on_build,
                         on_display=self.__on_display,
                         on_destroy=self.__on_destroy)
        self.__indent = indent
        self.__spacing = spacing
        self.__root = None
        self.__nodes = {}
        self.__internal_count = 0
        self.__cache = None
        self.__hook = None
        self.__view = self.build()

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
    def root(self):
        return self.__root

    @property
    def nodes(self):
        """
        Returns sequence of nodes. Check the method 'node()' to
        see how an individual node data structure looks like.
        """
        return [node.copy() for key, node in self.__nodes.items()]

    @property
    def hook(self):
        return self.__hook

    @hook.setter
    def hook(self, val):
        self.__hook = val

    # ==============================================
    #                 PUBLIC METHODS
    # ==============================================
    def insert(self, parent=None, title="", index="end",
               data=None, container=True, expand=False):
        """
        Insert a node.
        - parent: the node_id of the parent or None if this is the root node of the tree
        - title: string
        - index: an integer to indicate where to put the node between
         its parent's descendants.
            Put "end" to indicate that this node should be added at the the end
        - data: None or dictionary to contain whatever data you want. It could help later.
        - container: boolean. True, if the node should contain another node. False else.
        - expand: boolean, True if this node should be expanded from creation. False else.
        Returns:
            None if failed to insert the node, else returns the newly created node_id
        """
        # a root node shouldn't have a parent and should have index "end"
        data = {} if data is None else data
        if not self.__nodes:
            if parent is not None or (index != "end"):
                return None
        # a non-root should be legal
        elif not self.__check_non_root_node_is_legal(parent, index):
            return None
        # create node and return its id
        return self.__build_node(parent, title, index, data, container, expand)

    def node(self, id_or_path):
        """
        Returns a node by its node_id or its dotted path.
        A node is a dictionary of data:
        node = {"parent": int, "node_id": int, "container": bool,
                "index": int, "expanded": bool, "data": dict, "title": str,
                "frame_node": tk.Frame, "frame_header": tk.Frame,
                "frame_box": tk.Frame, "attached": bool, "ghosted": bool}
        Example of dotted path (each number in the path is a position index):
            Hub
                Africa
                America
                Asia
                    China
            china node = "0.2.0"
        """
        node = None
        if isinstance(id_or_path, str):
            node = self.__node_from_path(id_or_path)
        elif isinstance(id_or_path, int):
            node = self.__get_node(id_or_path)
        if node:
            return node.copy()

    def feed(self, node_id, *args, **kwargs):
        """
        This method will call "_on_feed(*args, **kwargs").
        Use it to feed some data to the tree
        """
        node = self.__get_node(node_id)
        if not node:
            return
        view = node.get("view", None)
        if not view:
            return
        view.on_feed_node(self, self, node, *args, **kwargs)

    def descendants(self, node_id):
        """
        List of descendants nodes.
        [ node, node, ...]

        Please check the doc of the method "node()" to learn more about
        the structure of a node object (a dict in fact)
        """
        return [node.copy() for key, node in self.__nodes.items()
                if node["parent"] == node_id]

    def expand(self, node_id):
        """
        Expands this node. Returns True if it worked, else returns False
        """
        node = self.__get_node(node_id)
        if node and node["container"] and not node["expanded"]:
            node["expanded"] = True
            view = node.get("view", None)
            if view:
                view.on_expand_node(self, node)
            node["frame_box"].grid(row=1, column=0)
            return True
        return False

    def collapse(self, node_id):
        """
        Collapses this node. Returns True if it worked, else returns False
        """
        node = self.__get_node(node_id)
        if node and node["container"] and node["expanded"]:
            node["expanded"] = False
            view = node.get("view", None)
            if view:
                view.on_collapse_node(self, node)
            node["frame_box"].grid_remove()
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
        Useful method to toggle the state collapsed/expanded of the node
        """
        if not self.collapse(node_id):
            self.expand(node_id)

    def title(self, node_id, title=None):
        """
        Use this method to display or edit the title of a node.
        Returns this node's title if you don't set a title as argument
        """
        node = self.__get_node(node_id)
        data = None
        if node:
            if title:
                node["title_stringvar"].set(title)
            data = node["title_stringvar"].get()
        return data

    def tag(self, node_id, data=None):
        """
        Edits this node's data. Data should be None or a dict
        Returns the data
        """
        data = {} if data is None else data
        node = self.__get_node(node_id)
        if not node:
            return
        for key, value in data.items():
            node["data"][key] = value
        return node["data"].copy()

    def untag(self, node_id, data=None):
        """
        Edits this node's data. Data should be a sequence of keys.
        Returns the data
        """
        node = self.__get_node(node_id)
        if node:
            for tag in data:
                try:
                    del node["data"][tag]
                except KeyError:
                    pass

    def delete(self, node_id):
        """
        Deletes this node.
        Returns True or False
        """
        for key, node in self.__nodes.items():
            if key == node_id:
                if node["container"]:
                    for descendant in self.descendants(node_id):
                        self.delete(descendant["node_id"])
                try:
                    node["frame_node"].destroy()
                except Exception as e:
                    pass
                if node_id > 0:
                    self.node(node["parent"])["frame_box"].config(height=1)
                del self.__nodes[key]
                return True
        return False

    def clear(self, node_id):
        """
        Deletes the descendants of this node. Returns True if all right, else False.
        """
        cache = True
        descendants = self.descendants(node_id)
        for descendant in descendants:
            deleted = self.delete(descendant["node_id"])
            cache = False if not deleted else cache
        return cache

    def move(self, node_id, parent_id=None, index=0):
        """
        Moves a node to another index. Returns True if all right, else False.
        """
        node = self.__get_node(node_id)
        if not node:
            return False
        if parent_id is None:
            parent_id = node["parent"]
        parent_node = self.__get_node(parent_id)
        if parent_node is None:
            return False
        if not self.__check_non_root_node_is_legal(parent_id, index):
            return False
        if isinstance(index, int):
            if index < len([node for key, node in self.__nodes.items()
                            if node["parent"] == parent_id]):
                self.__relocate(parent_id, index, direction="+")
        node["parent"] = parent_id
        node["index"] = index
        node["frame_node"].grid_remove()
        node["frame_node"].grid(in_=parent_node["frame_box"], row=index)
        return True

    def walk(self, node_id):
        """
        Walks throughout the node.
        Example:
            for node_id, descendants in tree.walk(2):
                print(node_id, len(descendants))
        """
        for key, node in self.__nodes.items():
            if key == node_id:
                if node["container"]:
                    descendants = self.descendants(node_id)
                    yield node_id, descendants
                    for descendant in descendants:
                        for a, b in self.walk(descendant["node_id"]):
                            if a is None:
                                continue
                            yield a, b

    def attach(self, node_id):
        """
        Attaches (again) a detached node. Returns True if it worked, else False
        """
        node = self.__get_node(node_id)
        if node and not node["attached"]:
            node["frame_node"].grid()
            node["attached"] = True
            return True
        return False

    def detach(self, node_id):
        """
        Detaches an attached node. Returns True if it worked, else False.
        The detached node won't be visible anymore.
        The detached node's descendants won't be visible anymore.
        """
        node = self.__get_node(node_id)
        if node and node["attached"]:
            node["frame_node"].grid_remove()
            node["attached"] = False
            return True
        return False

    def ghost(self, node_id):
        """
        Hide the header frame of the node whose node_id is given.
        Note that the descendants nodes will still be visible.
        Use this method to give illusion that descendants nodes
        don't have a root at all (kind of floating without root).
        This method returns a boolean (True to indicate that all right, else False)
        """
        node = self.__get_node(node_id)
        if node and not node["ghosted"]:
            node["frame_header"].grid_remove()
            node["frame_box"].grid(padx=(0, 0))
            node["frame_node"].grid(pady=(0, 0))
            node["ghosted"] = True
            node["expanded"] = True
            return True
        return False

    def unghost(self, node_id):
        """
        Reveals the header frame of the node whose node_id is given.
        This method returns a boolean (True to indicate that all right, else False)
        """
        node = self.__get_node(node_id)
        if node and node["ghosted"]:
            node["frame_header"].grid()
            node["frame_box"].grid(padx=(self.__indent, 0))
            node["frame_node"].grid(pady=(self.__spacing, 0))
            node["ghosted"] = False
            return True
        return False


    # ==============================================
    #                 INTERNAL
    # ==============================================
    def __on_build(self):
        pass

    def __on_display(self):
        pass

    def __on_destroy(self):
        pass

    def __build_node(self, parent, title, index, data, container, expand):
        # Case 1: root node
        if parent is None:
            index = 0
        else:
            descendants_count = len([node for key, node in self.__nodes.items()
                                  if node["parent"] == parent])
            # Case 2: non-root node with an index "end" or count root descendants
            if index == "end" or index == descendants_count:
                if index == "end":
                    index = descendants_count
            # Case 3: non-root node with an existent index
            elif 0 <= index < descendants_count:
                # relocate
                self.__relocate(parent, index)
        node_id = self.__internal_count
        self.__internal_count += 1
        frame_node, frame_header, frame_box = self.__build_node_frame(parent,
                                                                      index)
        node = {"parent": parent, "node_id": node_id, "container": container,
                "index": index, "expanded": expand, "data": data, "title": title,
                "frame_node": frame_node, "frame_header": frame_header,
                "frame_box": frame_box, "attached": True, "ghosted": False}
        self.__nodes[node_id] = node
        if parent is None:
            self.__root = node
        view = self.__get_view(frame_header, node.copy())
        if view:
            node["view"] = view
            view.build()
        # Silently collapse
        if not expand:
            node["frame_box"].grid_remove()
        return node_id

    def __build_node_frame(self, parent, index):
        # node frame
        master = self if parent is None else self.__get_node(parent)["frame_box"]
        master.columnconfigure(0, weight=1)
        frame_node = tk.Frame(master, class_="FrameNode",
                              cnf=self.__cnfs[FRAME_NODE])
        frame_node.columnconfigure(0, weight=1)
        # grid frame_node
        if parent is None:
            frame_node.grid(column=0, row=0, sticky="we")
        else:
            frame_node.grid(column=0, row=index,
                            sticky="we", pady=(self.__spacing, 0))
        # header
        frame_header = tk.Frame(frame_node, name=FRAME_HEADER,
                                cnf=self.__cnfs[FRAME_HEADER])
        frame_header.columnconfigure(0, weight=1)
        frame_header.grid(row=0, column=0, sticky="we")
        # box
        frame_box = tk.Frame(frame_node, name=FRAME_BOX,
                             cnf=self.__cnfs[FRAME_BOX])
        frame_box.grid(row=1, column=0,
                       padx=(self.__indent, 0),
                       sticky="we")
        return frame_node, frame_header, frame_box

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
                node["frame_node"].grid(column=0, row=node["index"])

    def __check_non_root_node_is_legal(self, parent_id, index):
        # a non-root node should have a parent
        if parent_id is None:
            return False
        # a non-root node should have an existent parent
        if parent_id not in [key for key, node in self.__nodes.items()]:
            return False
        # a non-root node should have a legal index: "end" or an integer value
        if isinstance(index, str) and index != "end":
            return False
        elif isinstance(index, int):
            # a non-root node should have an index that exists or is the last index +1
            if not (0 <= index <= len([node for key, node in self.__nodes.items()
                                       if node["parent"] == parent_id])):
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
        cache = 0
        del path[0]
        for index in path:
            try:
                index = int(index)
            except Exception:
                return
            descendants = self.descendants(cache)
            if not descendants:
                return
            valid_index = False
            for descendant in descendants:
                if descendant["index"] == index:
                    valid_index = True
                    cache = descendant["node_id"]
                    break
            if not valid_index:
                return
        return self.__get_node(cache)

    def __get_view(self, body, node):
        if not self.__hook:
            return None
        hook = self.__hook()
        if not isinstance(hook, Hook):
            message = ("The hook should be a callable",
                       "that returns a pyrustic.widget.tree.hook.Hook")
            raise PyrusticWidgetException(" ".join(message))
        on_build = (lambda tree=self,
                           node=node,
                           frame=body,
                           hook=hook:
                    hook.on_build_node(tree, node, frame))
        on_display = (lambda tree=self,
                           node=node,
                           frame=body,
                           hook=hook:
                    hook.on_display_node(tree, node))
        on_destroy = (lambda tree=self,
                           node=node,
                           frame=body,
                           hook=hook:
                    hook.on_destroy_node(tree, node))
        view = CustomView(body=body, on_build=on_build,
                          on_display=on_display,
                          on_destroy=on_destroy)
        view.on_feed_node = hook.on_feed_node
        view.on_expand_node = hook.on_expand_node
        view.on_collapse_node = hook.on_collapse_node
        return view


class Hook:

    def on_build_node(self, tree, node, frame):
        pass

    def on_display_node(self, tree, node):
        pass

    def on_destroy_node(self, tree, node):
        pass

    def on_feed_node(self, tree, node, *args, **kwargs):
        pass

    def on_expand_node(self, tree, node):
        pass

    def on_collapse_node(self, tree, node):
        pass


# ====================================
#              DEMO
# ====================================
class ExampleHook(Hook):
    def __init__(self):
        self._expander_stringvar = tk.StringVar()
        self._title_stringvar = tk.StringVar()

    def on_build_node(self, tree, node, frame):
        node_id = node["node_id"]
        title = node["title"]
        container = node["container"]
        # Header_1 - contains Expander_btn and title_label
        titlebar = tk.Frame(frame, name="treeTitlebar")
        titlebar.grid(row=0, column=0, sticky="we")
        titlebar.columnconfigure(1, weight=1)
        # Header_2 - is a frame
        toolbar = tk.Frame(frame, name="treeToolbar")
        toolbar.grid(row=1, column=0, sticky="we")
        #
        if container:
            self._expander_stringvar.set("-" if node["expanded"] else "+")
            expander_btn = tk.Button(titlebar, name="treeExpander",
                                     textvariable=self._expander_stringvar,
                                     padx=0, pady=0,
                                     command=lambda self=self, node_id=node_id:
                                     tree.collexp(node_id))
            expander_btn.grid(row=0, column=0)
        self._title_stringvar.set(title)
        title_label = tk.Label(titlebar, name="treeTitleLabel",
                               anchor="w", textvariable=self._title_stringvar)
        title_label.grid(row=0, column=1, sticky="we")

    def on_display_node(self, tree, node):
        pass

    def on_destroy_node(self, tree, node):
        pass

    def on_collapse_node(self, tree, node):
        self._expander_stringvar.set("+")

    def on_expand_node(self, tree, node):
        self._expander_stringvar.set("-")

    def on_feed_node(self, tree, node, *args, **kwargs):
        pass

def _populate_example(tree):
    #
    hub_id = tree.insert(title="Hub")
    africa_id = tree.insert(title="Africa", parent=hub_id)
    america_id = tree.insert(title="America", parent=hub_id)
    asia_id = tree.insert(title="Asia", parent=hub_id)
    europe_id = tree.insert(title="Europe", parent=hub_id)
    #
    france_id = tree.insert(title="France", parent=europe_id)
    italy_id = tree.insert(title="Italy", parent=europe_id)
    china_id = tree.insert(title="China", parent=asia_id)
    japan_id = tree.insert(title="Japan", parent=asia_id)
    usa_id = tree.insert(title="USA", parent=america_id)
    mexico_id = tree.insert(title="Mexico", parent=america_id)
    ghana_id = tree.insert(title="Ghana", parent=africa_id)
    morocco_id = tree.insert(title="Morocco", parent=africa_id)
    tunisia_id = tree.insert(title="Tunisia", parent=africa_id)
    #
    paris_id = tree.insert(title="Paris", parent=france_id, container=False)
    accra_id = tree.insert(title="Accra", parent=ghana_id, container=False)
    tunis_id = tree.insert(title="Tunis", parent=tunisia_id, container=False)
    rabat_id = tree.insert(title="Rabat", parent=morocco_id, container=False)
    tokyo_id = tree.insert(title="Tokyo", parent=japan_id, container=False)

if __name__ == "__main__":
    from pyrustic.widget.scrollbox import Scrollbox

    root = tk.Tk()
    root.geometry("500x500+0+0")
    scrollbox = Scrollbox(root)
    scrollbox.pack(expand=1, fill=tk.BOTH)
    tree = Tree(scrollbox.box)
    tree.pack(side=tk.LEFT, anchor="nw")
    tree.hook = lambda: ExampleHook()
    _populate_example(tree)
    root.mainloop()
