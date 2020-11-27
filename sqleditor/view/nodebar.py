from pyrustic.viewable import Viewable
from pyrustic.widget.table import Table
from pyrustic.widget.confirm import Confirm
import tkinter as tk


class Nodebar(Viewable):
    def __init__(self, parent_view,
                 node_id,
                 collapsable_frame,
                 file,
                 path,
                 real_path,
                 result,
                 datatype,
                 description):
        self._parent_view = parent_view
        self._node_id = node_id
        self._collapsable_frame = collapsable_frame
        self._file = file
        self._path = path
        self._real_path = real_path
        self._result = result
        self._datatype = datatype
        self._description = description
        self._body = None

    def _on_build(self):
        self._body = self._collapsable_frame
        text = tk.Text(self._body,
                       height=1,
                       name="textMessage",
                       wrap="word")
        result_frame = tk.Frame(self._body)
        result_frame.columnconfigure(0, weight=1)
        # install
        text.grid(row=0, column=0, sticky="we", ipadx=3, ipady=3, pady=(0, 3))
        result_frame.grid(row=1, column=0, sticky="nswe")
        # fill Text
        self._fill_text(text)
        # fill Frame
        self._fill_result_frame(result_frame)

    def _on_display(self):
        pass

    def _on_destroy(self):
        pass

    def _fill_text(self, text):
        message = ""
        background = "white"
        foreground = "white"
        if self._description == "success":
            tag = "textMessageSuccess"
            background = "#43A910"
            if self._datatype == "str_data":
                message = self._result
            elif self._datatype == "tabular_data":
                if not self._result[1]:
                    message = "There are not data to show"
                else:
                    message = "This is the data returned by the database"
            elif self._datatype == "db_schema":
                if not self._result:
                    message = "This database doesn't have a schema yet"
                else:
                    message = "This is the database schema"
        elif self._description == "warning":
            tag = "textMessageWarning"
            message = self._result
            background = "#FF285B"
        elif self._description == "error":
            tag = "textMessageError"
            message = self._result
            background = "#FF285B"
        message += " "
        text.insert("1.0", message)
        text.tag_add("message", "1.0", "1.{}".format(len(message)))
        text.tag_configure("message", background=background)
        text.tag_configure("message", foreground=foreground)
        text.tag_configure("message", lmargin1=3)
        text.tag_configure("message", rmargin=3)
        text.tag_configure("message", spacing1=3)
        text.tag_configure("message", spacing3=3)
        text.config(state="disabled")

    def _fill_result_frame(self, frame):
        if self._datatype == "db_schema":
            self._install_db_schema(frame, self._result)
        elif self._datatype == "tabular_data":
            self._install_result_table(frame, self._result)

    def _fill_request_result_frame(self, master):
        if self._datatype == "str_data":
            tk.Label(master, name="resultLabel",
                     text=self._result, anchor="w").pack(side=tk.LEFT)
        elif self._datatype == "db_schema":
            self._install_db_schema(master, self._result)
        elif self._datatype == "tabular_data":
            self._install_result_table(master, self._result)

    def _install_result_table(self, master, result):
        table = Table(master,
              orient="h",
              titles=result[0],
              data=result[1],
              mask=self._content_table_mask,
              options={"column_options": {"height": 0}})
        table.build_pack(side=tk.LEFT)

    def _install_db_schema(self, master, result, i=0, table_info=None):
        # TODO: improve this method with a generator ;)
        if table_info is None and not result:
            return
        if result and table_info is None:
            table_info = result[i]
            if i < len(result)-1:
                self._body.after(200, lambda :self._install_db_schema(master, result, i=i+1))
        header = ["Index", "Name", "Type", "Nullability", "Default", "Qualifier"]
        container = tk.Frame(master, class_="SchemaContainer")
        container.pack(pady=(0, 20), anchor="w")
        title_frame = tk.Frame(container)
        title_frame.pack(fill=tk.X, pady=(0,3))
        tk.Label(title_frame, name="schemaTitle", text=table_info[0]).pack(side=tk.LEFT)

        button_explore = tk.Button(title_frame,
                                   text="Explore",
                                   command=lambda name=table_info[0],
                                                  self=self: self._on_click_explore(name))
        button_explore.pack(side=tk.RIGHT)
        button_truncate = tk.Button(title_frame,
                                    text="Truncate",
                                    name="button_truncate",
                                    command=lambda name=table_info[0],
                                                   self=self: self._on_click_truncate(name))
        button_truncate.pack(side=tk.RIGHT, padx=(0, 3))
        button_drop = tk.Button(title_frame,
                                text="Drop",
                                name="button_drop",
                                command=lambda name=table_info[0],
                                               self=self: self._on_click_drop(name))
        button_drop.pack(side=tk.RIGHT, padx=(0, 3))
        table = Table(container, titles=header,
                      data=table_info[1],
                      hidden_columns=(0,),
                      orient="h",
                      mask=self._schema_table_mask,
                      options={"column_options": {"height": 0}})
        table.build_pack()

    def old_install_db_schema(self, master, result):  # TODO delete it or improve the new one
        i = 0
        for table_info in result:
            header = ["Index", "Name", "Type", "Nullability", "Default", "Qualifier"]
            container = tk.Frame(master, class_="SchemaContainer")
            title_frame = tk.Frame(container)
            title_frame.pack(fill=tk.X, pady=2)
            tk.Label(title_frame, name="schema_title", text=table_info[0]).pack(side=tk.LEFT)

            button_explore = tk.Button(title_frame,
                                       text="EXPLORE",
                                       command=lambda name=table_info[0],
                                                      self=self: self._on_click_explore(name))
            button_explore.pack(side=tk.RIGHT)
            button_truncate = tk.Button(title_frame,
                                        text="TRUNCATE",
                                        name="button_truncate",
                                        command=lambda name=table_info[0],
                                                       self=self: self._on_click_truncate(name))
            button_truncate.pack(side=tk.RIGHT)
            button_drop = tk.Button(title_frame,
                                    text="DROP",
                                    name="button_drop",
                                    command=lambda name=table_info[0],
                                                   self=self: self._on_click_drop(name))
            button_drop.pack(side=tk.RIGHT)
            table = Table(container, titles=header,
                          data=table_info[1],
                          hidden_columns=(0,),
                          orient="h",
                          mask=self._schema_table_mask,
                          options={"column_options": {"height": 0}})
            table.build_pack()
            command = lambda container=container: container.pack(pady=(0, 20), anchor="w")
            self._body.after(i, command)
            i += 500


    def _content_table_mask(self, index, data):
        return [((" " + str(x)) if x is not None else "") for x in data]

    def _schema_table_mask(self, index, data):
        nullability = "Not Null" if data[3] == 1 else "Null"
        default_value = "" if data[4] is None else data[4]
        qualifier_value = str(data[5]) if data[5] > 0 else ""
        qualifier_value = "" if not qualifier_value else ("Primary Key " + qualifier_value)
        return [(" " + str(x)) for x in
                (data[0], data[1], data[2].title(),
                 nullability, default_value, qualifier_value)]

    def _on_click_explore(self, name):
        self._parent_view.on_click_explore(name)

    def _on_click_truncate(self, name):
        confirm = Confirm(self._body,
                          title="Confirmation",
                          header="Truncate the table {}".format(name),
                          message="Do you really want to continue ?")
        confirm.build_wait()
        if confirm.ok:
            self._parent_view.on_click_truncate(name)

    def _on_click_drop(self, name):
        confirm = Confirm(self._body,
                          title="Confirmation",
                          header="Drop the table {}".format(name),
                          message="Do you really want to continue ?")
        confirm.build_wait()
        if confirm.ok:
            self._parent_view.on_click_drop(name)

    def _on_click_open(self):
        self._parent_view.on_change_database(self._real_path)
