import tkinter as tk
from pyrustic.viewable import Viewable
from pyrustic.widget.toast import Toast
import sqlite3 as sqlite


"""
formatter: inline, expanded, script
datatype: tabular_data, str_data, db_schema
"""
class Footer(Viewable):
    def __init__(self, parent_view, main_host, editor_builder):
        self._parent_view = parent_view
        self._main_host = main_host
        self._editor_builder = editor_builder
        # widgets
        self._body = None
        self._entry_sql = None
        # stringvar
        self._stringvar_sql = tk.StringVar()
        # cache
        self._inline_sql_history = []
        self._index_inline_sql_history = None
        self._cache_editor_data = (0, "")


    # ==================================
    #       INTERACTION WITH MAIN_VIEW
    # ==================================

    @property
    def cache_editor_data(self):
        return self._cache_editor_data

    @cache_editor_data.setter
    def cache_editor_data(self, val):
        self._cache_editor_data = val

    def push(self, request, formatter="inline", execute=False):
        if formatter == "inline":
            self._update_inline_sql_history(request)
            self._stringvar_sql.set(request)
            self._focus_entry()
        elif formatter == "expanded":
            self._cache_editor_data = (0, request)
            self._on_click_editor()
        elif formatter == "script":
            self._cache_editor_data = (1, request)
            self._on_click_editor()
        if not execute:
            return
        self._exec_sql(request, formatter)

    def notify_sql_to_run(self):
        is_script, sql = self._cache_editor_data
        self._exec_sql(sql,
                       formatter="script" if is_script == 1 else "expanded",
                       is_script=True if is_script == 1 else False)

    # ==================================
    #           VIEW LIFECYCLE
    # ==================================
    def _on_build(self):
        self._body = tk.Frame(self._parent_view.body)
        self._body.columnconfigure(1, weight=1)
        # button clean
        button_clear = tk.Button(self._body, text="x", name="buttonClearX",
                                 command=self._on_click_clear)
        # entry sql
        self._entry_sql = tk.Entry(self._body, textvariable=self._stringvar_sql)
        self._entry_sql.bind("<Return>", lambda e: self._on_click_run())
        self._entry_sql.bind("<Up>", lambda e: self._on_up_or_down_inside_entry(e, "up"))
        self._entry_sql.bind("<Down>", lambda e: self._on_up_or_down_inside_entry(e, "down"))
        # button run
        button_run = tk.Button(self._body,
                               text="Run",
                               command=self._on_click_run)

        # button editor
        button_editor = tk.Button(self._body,
                                  text="Editor",
                                  command=self._on_click_editor)
        # install
        button_clear.grid(row=0, column=0)
        button_run.grid(row=0, column=2, padx=(3, 3))
        button_editor.grid(row=0, column=3, padx=(0, 0))
        self._entry_sql.grid(row=0, column=1, sticky="nswe")
        return self._body

    def _on_display(self):
        pass

    def _on_destroy(self):
        pass

    # ==================================
    #           PRIVATE METHODS
    # ==================================
    def _exec_sql(self, sql, formatter, is_script=False):
        if self._main_host.path is None:
            Toast(self._body, header="Error",
                  message="Database missing !", duration=2000).build()
            return
        result = result_datatype = description = None
        close_app = False
        try:
            result, result_datatype = self._sql_executor(sql, is_script)
            description = "success"
        except sqlite.Error as e:
            result = str(e)
            result_datatype = "str_data"
            description = "error"
        except sqlite.Warning as e:
            result = str(e)
            result_datatype = "str_data"
            description = "warning"

        self._parent_view.notify_operation_execution(result, result_datatype, description,
                                                     sql, formatter)

    def _sql_executor(self, sql, is_script):
        result_datatype = None
        result = None
        if is_script:
            self._main_host.exec_script(sql)
            result = "Request executed successfully !"
            result_datatype = "str_data"
        elif sql.lower() == "tables":
            result = self._main_host.db_schema()
            result_datatype = "db_schema"
            if not result:
                result = "Empty database"
                result_datatype = "str_data"
        elif sql.lower() in ("quit", "leave", "exit", "close"):
            self._parent_view.leave_app()
        else:
            if self._main_host.is_data_query_language(sql):
                result = self._main_host.exec_query_request(sql)
                result_datatype = "tabular_data"
                if result and not result[1]:
                    result = "Empty table"
                    result_datatype = "str_data"
            else:
                self._main_host.exec_edit_request(sql)
                result = "Request executed successfully !"
                result_datatype = "str_data"
        return result, result_datatype

    def _focus_entry(self):
        self._entry_sql.focus()
        self._entry_sql.select_range(0, 'end')
        self._entry_sql.icursor('end')

    def _on_click_run(self):
        inline_sql = self._stringvar_sql.get()
        self._exec_sql(inline_sql, "inline")
        self._update_inline_sql_history(inline_sql)

    def _on_click_editor(self):
        self._editor_builder.build(self)

    def _on_click_clear(self):
        self._entry_sql.delete(0, "end")
        self._focus_entry()

    def _update_inline_sql_history(self, sql):
        self._inline_sql_history.append(sql)
        self._index_inline_sql_history = len(self._inline_sql_history) - 1

    def _on_up_or_down_inside_entry(self, event, direction):
        if self._index_inline_sql_history is None:
            return
        if direction == "up":
            if self._index_inline_sql_history > 0:
                self._index_inline_sql_history = self._index_inline_sql_history - 1
        elif direction == "down":
            if self._index_inline_sql_history < (len(self._inline_sql_history) - 1):
                self._index_inline_sql_history = self._index_inline_sql_history + 1
        inline_sql = self._inline_sql_history[self._index_inline_sql_history]
        self._stringvar_sql.set(inline_sql)
        self._focus_entry()
