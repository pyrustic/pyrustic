from pyrustic.widget.scrollbox import Scrollbox
from pyrustic.abstract.viewable import Viewable
from tool.runtest.view.tree import Tree
import os.path
import os
import tkinter as tk


class MainView(Viewable):

    def __init__(self, master, threadium, host, toolbar_builder, root_path):
        self._master = master
        self._threadium = threadium
        self._host = host
        self._toolbar_builder = toolbar_builder
        self._root_path = root_path
        self._focused_node = dict()
        self._test_running = False
        self._waiting_list = list()
        # build
        self.build()

    # ========================================
    #          INTERACTION WITH HOST
    # ========================================
    def fill_directory(self, node_id, data):
        self._tree.clear(node_id)
        if data is None:
            return
        count_tests, directories, modules = data
        self._tree.tag(node_id)["count_tests_stringvar"].set(count_tests)
        path = self._tree.node(node_id)["tags"]["path"]
        for directory in directories:
            self._tree.insert(parent=node_id,
                              title= directory,
                              tags={"path": os.path.join(path, directory),
                                    "type": "directory",
                                    "count_tests_stringvar": tk.StringVar()})
        for module in modules:
            self._tree.insert(parent=node_id,
                              title= module,
                              tags={"path": os.path.join(path, module),
                                    "type": "module",
                                    "count_tests_stringvar": tk.StringVar()})

    def fill_module(self, node_id, data):
        self._tree.clear(node_id)
        if data is None:
            return
        count_tests, classes = data
        if count_tests == 0:
            return
        self._tree.tag(node_id)["count_tests_stringvar"].set(count_tests)
        path = self._tree.node(node_id)["tags"]["path"]
        for class_ in classes:
            self._tree.insert(parent=node_id,
                              title=class_,
                              tags={"path": path,
                                    "type": "class",
                                    "name": class_,
                                    "count_tests_stringvar": tk.StringVar()})

    def fill_class(self, node_id, data):
        self._tree.clear(node_id)
        if data is None:
            return
        count_tests, methods = data
        self._tree.tag(node_id)["count_tests_stringvar"].set(count_tests)
        node = self._tree.node(node_id)
        module_path = node["tags"]["path"]
        name = node["tags"]["name"]
        for method in methods:
            self._tree.insert(parent=node_id,
                              title=method,
                              container=False,
                              tags={"path": module_path,
                                    "type": "method",
                                    "class": name,
                                    "name": method,
                                    "count_tests_stringvar": tk.StringVar()})

    def notify_running_test_event(self, data):
        node_id = data["id"]
        event = data["event"]
        if node_id not in self._focused_node:
            return
        node = self._focused_node[node_id]
        toolbar = node["toolbar"]
        node["log"].append(data)
        if event == "start_test_run":
            self._test_running = True
            toolbar.set_running_state()
        elif event == "stop_test_run":
            self._test_running = False
            toolbar.set_stop_state(data["was_successful"], node["log"])
            node["log"] = []
            self._threadium.stop(node["qid"])
            if self._waiting_list:
                next_task = self._waiting_list[0]
                del self._waiting_list[0]
                self._run_test(*next_task)
        elif event == "time_elapsed":
            toolbar.notify_time_elapsed(data["time"])
        elif event == "start_test":
            toolbar.notify_start_test(data["test"])
        elif event == "stop_test":
            toolbar.notify_stop_test(data["test"])
        elif event == "add_error":
            toolbar.notify_add_error(data["test"], data["err"])
        elif event == "add_failure":
            toolbar.notify_add_failure(data["test"], data["err"])
        elif event == "add_success":
            toolbar.notify_add_success(data["test"])
        elif event == "add_skip":
            toolbar.notify_add_skip(data["test"], data["reason"])
        elif event == "add_expected_failure":
            toolbar.notify_add_expected_failure(data["test"], data["err"])
        elif event == "add_unexpected_success":
            toolbar.notify_add_unexpected_success(data["test"])
        elif event == "add_sub_test":
            toolbar.notify_add_sub_test(data["test"], data["sub_test"], data["outcome"])

    def notify_running_exception(self, exception):
        pass

    # ==================================
    #       INTERACTION WITH TREE
    # ==================================

    def on_node_collapsed(self, node):
        self._tree.clear(node["node_id"])
        node["box_frame"].config(height=1)

    def on_node_expanded(self, node):
        node_id = node["node_id"]
        node_type = node["tags"]["type"]
        path = node["tags"]["path"]

        if node_type in ("directory", "root"):
            self._threadium.task(self._host.tests_in_directory, args=(path,),
                        consumer=lambda data, self=self, node_id=node_id:
                        self.fill_directory(node_id, data))
        elif node_type == "module":
            self._threadium.task(self._host.tests_in_module, args=(path,),
                           consumer=lambda data, self=self, node_id=node_id:
                           self.fill_module(node_id, data))
        elif node_type == "class":
            name = node["tags"]["name"]
            self._threadium.task(self._host.tests_in_class, args=(path, name),
                           consumer=lambda data, self=self, node_id=node_id:
                           self.fill_class(node_id, data))

    def on_title_clicked(self, node, toolbar_parent):
        node_id = node["node_id"]
        toolbar = None
        operation = "create"
        if node_id in self._focused_node:
            toolbar = self._focused_node[node_id]["toolbar"]
            operation = "hide" if toolbar.is_visible else "show"
        if operation == "hide":
            toolbar.show_or_hide()
            self._focused_node[node_id]["parent"].config(height=1)
            return
        path = node["tags"]["path"]
        class_name = method_name = None
        if node["tags"]["type"] == "class":
            class_name = node["tags"]["name"]
        elif node["tags"]["type"] == "method":
            class_name = node["tags"]["class"]
            method_name = node["tags"]["name"]
        data = self._host.count_tests(path, class_name=class_name,
                                      method_name=method_name)
        if data is None:
            self._tree.collapse(node["parent"])
            self._tree.node(node["parent"])["box"].config(height=1)
            return
        count_tests = data[0]
        if operation == "show":
            toolbar.count_tests = count_tests
            toolbar.show_or_hide()
            return
        toolbar = self._toolbar_builder.build(node_id, toolbar_parent, self)
        toolbar.count_tests = count_tests
        data = {"toolbar": toolbar, "parent": toolbar_parent,
                "running": False, "queue": None, "qid": None, "log": []}
        self._focused_node[node_id] = data


    # ========================================
    #          INTERACTION WITH TOOLBAR
    # ========================================
    def on_run_clicked(self, node_id, failfast):
        failfast = True if failfast else False
        toolbar = self._focused_node[node_id]["toolbar"]
        if self._test_running:
            toolbar.set_waiting_state()
            self._waiting_list.append((node_id, failfast))
        else:
            self._run_test(node_id, failfast)

    def on_stop_clicked(self, node_id):
        self._host.stop(node_id)

    def on_cancel_clicked(self, node_id):
        for x, data in enumerate(self._waiting_list):
            if node_id == data[0]:
                del self._waiting_list[x]


    # ===========================================
    #         VIEWABLE METHODS IMPLEMENTATION
    # ===========================================
    def _on_build(self):
        # == Widgets
        self._body = tk.Frame(self._master)
        self._scrollbox = Scrollbox(self._body)
        self._tree = Tree(self._scrollbox.box, self)
        # == Layout
        self._scrollbox.body.pack(expand=1, fill=tk.BOTH)
        self._tree.body.pack(expand=1, fill=tk.BOTH, padx=(5, 50), pady=(5, 50))
        # ==
        return self._body

    def _on_display(self):
        self._tree.insert(title="tests",
                          tags={"path": self._root_path,
                                "type": "root",
                                "count_tests_stringvar": tk.StringVar()})

    def _on_destroy(self):
        pass

    # ==================================
    #          PRIVATE METHODS
    # ==================================
    def _delete_node(self, node_id):
        self._tree.delete(node_id)
        try:
            del self._focused_node[node_id]
        except KeyError:
            pass

    def _run_test(self, node_id, failfast):
        node = self._tree.node(node_id)
        path = node["tags"]["path"]
        class_name = method_name = None
        if node["tags"]["type"] == "class":
            class_name = node["tags"]["name"]
        elif node["tags"]["type"] == "method":
            class_name = node["tags"]["class"]
            method_name = node["tags"]["name"]
        data = self._host.count_tests(path, class_name=class_name, method_name=method_name)
        if data is None:
            self._tree.node(node["parent"])["box"].config(height=1)
            self._tree.collapse(node["parent"])
            return
        count_tests, suite = data
        toolbar = self._focused_node[node_id]["toolbar"]
        toolbar.count_tests = count_tests
        queue = self._threadium.q()
        self._focused_node[node_id]["queue"] = queue
        self._threadium.task(self._host.run_suite, args=(node_id, suite, queue),
                             kwargs={"failfast": failfast})
        qid = self._threadium.consume(queue, consumer=self.notify_running_test_event,
                                exception_handler=self.notify_running_exception)
        self._focused_node[node_id]["qid"] = qid
