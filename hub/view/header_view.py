import tkinter as tk
from pyrustic.viewable import Viewable
from pyrustic import pymisc
from pyrustic.widget.toast import Toast


class HeaderView(Viewable):
    def __init__(self, master, main_view, main_host):
        self._master = master
        self._main_view = main_view
        self._main_host = main_host
        self._body = None
        self._toast_loading = None
        # stringvar
        self._stringvar = tk.StringVar()

    def show_rate(self, data):
        if self._toast_loading:
            self._toast_loading.destroy()
            self._toast_loading = None
        status_code, status_text, data = data
        message = None
        duration = 5000
        if status_code in (200, 304):
            message = "Rate Limit:\t{}\nRemaining :\t{}".format(data["limit"],
                                                             data["remaining"])
            message = pymisc.tab_to_space(message, tab_size=4)
        else:
            duration = 1000
            message = "Failed to load data\n{}".format(status_text)
        toast = Toast(self._body, message=message, duration=duration)
        toast.build()

    # =========================================
    #               LIFECYCLE
    # =========================================
    def _on_build(self):  # TODO, on windows, the ">" button isn't well aligned with widgets at Left
        self._body = tk.Frame(self._master)
        # label Query
        label_query = tk.Label(self._body, name="label_query", text="Query:")
        label_query.pack(side=tk.LEFT, anchor="n")
        # entry
        entry_search = tk.Entry(self._body, name="entry_search",
                                width=40,
                                textvariable=self._stringvar)
        entry_search.bind("<Return>", lambda e, self=self: self._on_click_search())
        entry_search.pack(side=tk.LEFT, anchor="n")
        entry_search.focus()
        # button run
        button_run = tk.Button(self._body, name="button_go", text=">",
                               command=self._on_click_search)
        button_run.pack(side=tk.LEFT, anchor="n")
        # button rate
        button_rate = tk.Button(self._body, name="button_rate", text="Rate",
                                command=self._on_click_rate)
        button_rate.pack(side=tk.RIGHT, anchor="n", padx=2, pady=2)

    def _on_display(self):
        pass

    def _on_destroy(self):
        pass

    # =========================================
    #               PRIVATE
    # =========================================
    def _on_click_search(self):
        data = self._stringvar.get()
        if data:
            data = self._main_host.extract_owner_repo_from_url(data)
        if not data:
            return
        self._stringvar.set("{}/{}".format(*data))
        self._main_view.central_view.add_node(*data)

    def _on_click_rate(self):
        if self._toast_loading:
            return
        self._toast_loading = Toast(self._body,
                                    message="Rate Limit: Loading...",
                                    duration=None)
        self._toast_loading.build()
        threadium = self._main_view.threadium
        host = self._main_host.rate
        consumer = self.show_rate
        threadium.task(host, consumer=consumer)
