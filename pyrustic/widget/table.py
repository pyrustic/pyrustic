import tkinter as tk
import operator
from pyrustic.exception import PyrusticTableException
from pyrustic.abstract.viewable import Viewable


# Allowed Options for table, header, and columns
TABLE_OPTIONS = ["background", "borderwidth", "cursor", "height",
                 "highlightbackground", "highlightcolor",
                 "highlightthickness", "name", "padx", "pady",
                 "relief", "takefocus", "width"]

HEADER_OPTIONS = ["activebackground", "activeforeground", "anchor",
                  "background", "bitmap", "borderwidth", "cursor",
                  "compound", "disabledforeground", "font", "foreground",
                  "height", "highlightbackground", "highlightcolor",
                  "highlightthickness", "image", "justify", "padx",
                  "pady", "relief", "state", "text", "textvariable",
                  "takefocus", "underline", "width", "wraplength"]

COLUMN_OPTIONS = ["background", "borderwidth", "cursor",
                  "disabledforeground", "exportselection", "font",
                  "foreground", "height", "highlightbackground",
                  "highlightcolor", "highlightthickness", "justify",
                  "relief", "selectbackground", "selectborderwidth",
                  "selectforeground", "setgrid", "state", "takefocus",
                  "width"]

# Components of table
HEADER = "header"
DATA = "data"
COLUMN = "column"
TABLE = "table"
ROW = "row"

# Layout
EQUALLY = "equally"
PROPORTIONALLY = "proportionally"

# Selection modes for rows
SINGLE = "single"
BROWSE = "browse"
MULTIPLE = "multiple"
EXTENDED = "extended"

# sort data as
ASC = "[+]"
DESC = "[-]"

STYLE = [("*Table*background", "red"),
         ("*Table*foreground", "blue")]


def _check_option(option):
    if option in COLUMN_OPTIONS:
        return True
    raise PyrusticTableException("The column option -" + option
                                 + " doesn't exist. These are legal options for column: "
                                 + str(COLUMN_OPTIONS))


def _verify_options(column_options):
    for option in column_options.keys():
        if not _check_option(option):
            del column_options[option]


class Table(Viewable):
    """
    Table supports data sorting, multiple selection modes, and more...

    Example:
        import tkinter as tk
        from pyrustic.widget.table import Table
        root = tk.Tk()
        titles = ("Name", "Job")
        data = [("Jack", "Architect"), ("Diana", "Physicist")]
        table = Table(root, titles=titles, data=data)
        table.body.pack()
        root.mainloop()
    """
    def __init__(self,
                 master=None,
                 titles=[],
                 data=[],
                 hidden_columns=[],
                 sorting=True,
                 mask=None,
                 select_mode=BROWSE,
                 layout=EQUALLY,
                 orient="both",
                 options={}):
        """
        - master: widget parent
        - titles: sequence of titles. Example: ("Name", "Job")
        - data: sequence of sequences. Each sub-sequence must have same size as titles.
            Example: [ ("Jack, "Architect"), ("Diana", "Physicist") ]
        - hidden_columns: sequence of columns to hide.
            Example: (1, 2) will hide the column at the index 1 and 2.
            Example: (0, ) will hide only the first column
        - sorting: boolean, set to True if you want the table to be able to do sorting when user
            clicks on a column title. Default: True
        - mask:
        - select_mode: selection modes: "single", "browse", "multiple" and "extended". Default: single
        - layout: "equally" or "proportionally". Default to "equally".
        - orient: orientation for scrollbars. "both" or "vertical" or "horizontal"
        - options: dictionary, these options will be used as argument to the widget's constructors.
            The widgets are: body, hsb, vsb, canvas, frame_window, frame_header, label_sorting,
            label_title and listbox_column.
            Example: Assume that you want to set the label_message's background to black
            and the horizontal scrollbar's background to red:
                options = {"body": {"background": "red"},
                           "hsb": {"background": "black"}}
        """
        if "column" in options:
            _verify_options(options["column"])
        self._master = master
        self._titles_cache = titles
        self._titles = []
        self._data_cache = data
        self._data = []
        self._hidden_columns = hidden_columns
        self._sorting = sorting
        self._mask = mask
        self._select_mode = select_mode
        self._layout = layout
        self._orient = orient
        self._options = options
        self._body_options = None
        self._hsb_options = None
        self._vsb_options = None
        self._canvas_options = None
        self._frame_window_options = None
        self._frame_header_options = None
        self._label_sorting_options = None
        self._label_title_options = None
        self._listbox_column_options = None
        self._parse_options(options)
        # misc
        self._components = {}
        self._cache = None
        self._current_sorting = None
        self._current_column_index = None
        self._current_row_index = None
        self._selection_garbage = None
        self._selection = None
        self._header_clicked_handlers = []
        self._header_event_handlers = {}
        self._row_selected_handlers = []
        self._row_event_handlers = {}
        self._default_listbox_background = None
        self._default_listbox_foreground = None
        self._default_listbox_selectbackground = None
        self._default_listbox_selectforeground = None
        # cache for sorting's labels, header's labels and listboxes
        self._header_frames_cache = []
        self._labels_sorting_cache = []
        self._labels_titles_cache = []
        self._listboxes_cache = []
        # string vars cache
        self._labels_sorting_stringvars_cache = []
        self._labels_titles_stringvars_cache = []
        # components
        self._body = None
        self._canvas = None
        self._window = None
        self._window_id = None
        self._vsb = None
        self._hsb = None
        self._hsb_under_mouse = False
        self.build()
        self._reset_titles(self._titles_cache)
        self._reset_data(self._data_cache)

    # ==============================================
    #                   PROPERTIES
    # ==============================================
    @property
    def body(self):
        return self._body

    @property
    def titles(self):
        return self._titles

    @titles.setter
    def titles(self, titles):
        self._reset_titles(titles)

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data):
        self._reset_data(data)

    @property
    def hidden_columns(self):
        return self._hidden_columns

    @hidden_columns.setter
    def hidden_columns(self, val):
        self._hidden_columns = val

    @property
    def mask(self):
        return self._mask

    @mask.setter
    def mask(self, val):
        self._mask = val

    @property
    def select_mode(self):
        return self._select_mode

    @property
    def layout(self):
        return self._layout

    @property
    def orient(self):
        return self._orient

    @property
    def size(self):
        # return (cols, rows)
        return len(self._titles), len(self._data)

    @property
    def components(self):
        """
        Get the components used to build this table.
        This property returns a dict. The keys are:
            'body', 'hsb', 'vsb', 'canvas', 'frame_window', 'frame_header_list',
            'label_sorting_list', 'label_title_list' and 'listbox_column_list'
        Warning: 'frame_header_list', 'label_sorting_list', 'label_title_list'
            and 'listbox_column_list' are sequence of widgets by index
        """
        return self._components

    @property
    def selection(self):
        if not self._selection:
            return ()
        data = []
        for i in self._selection:
            cache = {"index": i, "data": self._data[i]}
            data.append(cache)
        return tuple(data)


    # ==============================================
    #                 PUBLIC METHODS
    # ==============================================

    def fill(self, titles=None, data=None):
        """
        This will reset the titles or data with the new submitted titles or data
        """
        if titles:
            self.titles = titles
        if data:
            self.data = data

    def insert(self, index, data):
        """
        Insert into the table this data at this index. Index is an integer or is "end".
        This method doesn't erase the previous data at this index, but pull it down in the table.
        data is a sequence of sequences. Example if u want to insert a line, u need to put this
        line in a sequence.
        Assume you want to push ("Matrix", "Cameraman") at index 0.
            insert(0, [("Matrix", "Cameraman")])
        Assume you want to push ("Matrix", "Cameraman") and ("Diana", "Seller") at index "end".
            insert("end", [("Matrix", "Cameraman"), ("Diana", "Seller")])
        """
        if self._check_data_row_size(data):
            self._insert(index, data)
            self._adjust_selection_after_insertion(index, len(data))

    def get(self, index_start, index_end=None):
        """
        Returns a line if you don't give a 'index_end'.
        Returns a sequence of line if you give a 'index_end'.
        """
        if not index_end:
            return self._data[index_start]
        else:
            result = []
            index_end_range = len(self._data) if index_end == "end" else index_end + 1
            for i in range(index_start, index_end_range):
                result.append(self._data[i])
            return result

    def delete(self, index_start, index_end=None):
        """
        Delete lines from the table
        """
        if not index_end:
            del self._data[index_start]
        else:
            index_fin_range = len(self._data) if index_end == "end" else index_end + 1
            for _ in range(index_start, index_fin_range):
                del self._data[index_start]
        for listbox in self._listboxes_cache:
            listbox.delete(index_start, index_end)
        self._selection_garbage = None
        self._selection = None

    def clear(self):
        """
        Clear the table
        """
        for listbox in self._listboxes_cache:
            listbox.delete(0, "end")
        self._data = []

    def handle_row_selected(self, handler):
        """
        This handler will be called at the event 'row selection':
            handler(table, row_data, row_index, column_index)
        """
        self._row_selected_handlers.append(handler)

    def handle_row_event(self, sequence, handler):
        """
        This handler will be called at a row event:
            handler(table, row_data, row_index, column_index)
        """
        for i, listbox in enumerate(self._listboxes_cache):
            listbox.bind(sequence,
                         lambda event,
                                self=self,
                                handler=handler,
                                i=i: self._build_handler_for_row_event(event, handler, i), "+")

    def see(self, index="end"):
        """
        The table will scroll to the given index
        """
        if self._listboxes_cache:
            self._listboxes_cache[0].see(index)

    def config_column(self, index=None, **options):
        """

        """
        if index is None:
            for x in self._listboxes_cache:
                x.config(**options)
                x.config(highlightcolor=x.cget("highlightbackground"))
        else:
            self._listboxes_cache[index].config(**options)
            self._listboxes_cache[index].config(highlightcolor=self._listboxes_cache[index].cget("highlightbackground"))

    def cget_column(self, index=None, option="background"):
        """

        """
        if index is not None and option:
            return self._listboxes_cache[index].cget(option)
        if option:
            return [x.cget(option) for x in self._listboxes_cache]

    # ==============================================
    #                 PRIVATE METHODS
    # ==============================================
    def _on_build(self):
        self._body = tk.Frame(master=self._master,
                              class_="Table",
                              cnf=self._body_options)
        self._components["body"] = self._body

    def _on_display(self):
        pass

    def _on_destroy(self):
        pass

    def _build(self):
        self._body.columnconfigure(0, weight=1)
        self._body.rowconfigure(0, weight=1)
        self._canvas = tk.Canvas(self._body, self._canvas_options)
        self._components["canvas"] = self._canvas
        self._canvas.grid(row=0, column=0, sticky="nswe")
        self._window = tk.Frame(self._canvas, self._frame_window_options)
        self._components["frame_window"] = self._window
        self._window_id = self._canvas.create_window(0, 0, window=self._window, anchor="nw")
        self._window.bind("<Configure>", self._on_configure_window, "+")
        self._build_header_and_columns()
        self._extract_listboxes_color()
        self._set_scrollbars()

    def _build_header_and_columns(self):
        self._components["frame_header_list"] = []
        self._components["label_sorting_list"] = []
        self._components["label_title_list"] = []
        self._components["listbox_column_list"] = []
        ignored_i = 0
        for i, title in enumerate(self._titles):
            if i in self._hidden_columns:
                ignored_i += 1
                continue
            i -= ignored_i
            # Configure Window Grid
            if self._layout == EQUALLY:
                self._window.columnconfigure(i, weight=1, uniform=1)
            # Build Header
            # - install header frame
            frame_header = tk.Frame(self._window,
                                    class_="TableHeaderFrame",
                                    cnf=self._frame_header_options)
            self._components["frame_header_list"].append(frame_header)
            frame_header.grid(row=0, column=i, sticky="nswe")
            frame_header.columnconfigure(1, weight=1)
            self._header_frames_cache.append(frame_header)
            # - install sorting label
            label_sorting_stringvar = tk.StringVar()
            self._labels_sorting_stringvars_cache.append(label_sorting_stringvar)
            label_sorting = tk.Label(frame_header,
                                     textvariable=label_sorting_stringvar,
                                     cnf=self._label_sorting_options)
            self._components["label_sorting_list"].append(label_sorting)
            label_sorting.grid(row=0, column=0)
            label_sorting.bind("<Button-1>",
                             lambda event, i=i: self._on_header_clicked(event, i), "+")
            label_sorting.grid_remove()
            self._labels_sorting_cache.append(label_sorting)
            # - install title label
            label_title_stringvar = tk.StringVar()
            label_title_stringvar.set(title)
            self._labels_titles_stringvars_cache.append(label_title_stringvar)
            label_title = tk.Label(frame_header,
                                   textvariable=label_title_stringvar,
                                   cnf=self._label_title_options)
            self._components["label_title_list"].append(label_title)
            label_title.grid(row=0, column=1, sticky="nswe")
            label_title.bind("<Button-1>",
                             lambda event, i=i: self._on_header_clicked(event, i), "+")
            self._labels_titles_cache.append(label_title)
            # Build Columns
            listbox = tk.Listbox(self._window,
                                 activestyle="none",
                                 selectmode=BROWSE if self._select_mode == MULTIPLE
                                 else self._select_mode,
                                 cnf=self._listbox_column_options, takefocus=0)
            self._components["listbox_column_list"].append(listbox)
            listbox.config(highlightcolor=listbox.cget("highlightbackground"))
            listbox.grid(row=1, column=i, sticky="nswe")
            listbox.bind('<<ListboxSelect>>',
                         lambda event, i=i: self._on_row_selected(event, i), "+")
            self._listboxes_cache.append(listbox)

    def _extract_listboxes_color(self):
        self._default_listbox_background = self._listboxes_cache[0].cget("background")
        self._default_listbox_foreground = self._listboxes_cache[0].cget("foreground")
        self._default_listbox_selectbackground = self._listboxes_cache[0].cget("selectbackground")
        self._default_listbox_selectforeground = self._listboxes_cache[0].cget("selectforeground")

    def _set_scrollbars(self):
        if self._orient in ("both", "horizontal", "x", "h"):
            self._hsb = tk.Scrollbar(self._body, name="hsb",
                                     orient="horizontal",
                                     command=self._canvas.xview)
            self._components["hsb"] = self._hsb
            self._hsb.grid(row=1, column=0, columnspan=2, sticky="we")
            self._hsb.bind("<Button-4>", self._on_mouse_wheel, "+")
            self._hsb.bind("<Button-5>", self._on_mouse_wheel, "+")
            self._canvas.config(xscrollcommand=self._hsb.set)
        if self._orient in ("both", "vertical", "y", "v"):
            self._vsb = tk.Scrollbar(self._body, name="vsb",
                                     orient="vertical",
                                     command=self._scroll_listboxes_sync)
            self._components["vsb"] = self._vsb
            self._vsb.grid(row=0, column=1, sticky="ns")
        for listbox in self._listboxes_cache:
            listbox.config(yscrollcommand=self._scroll_listboxes_and_scrollbar_sync)

    def _on_mouse_wheel(self, event):
        # NB: event.num 5 to go down and event.num 4 to go up
        # NB: event.delta if negative, goes down, and event.delta if positive goes up
        scroll = 1 if event.num == 5 or event.delta < 0 else -1
        # NB: scroll 1 to go down and scroll -1 to go up
        if self._orient in ("both", "horizontal", "h", "x",
                            "vertical", "v", "y"):
            self._canvas.xview_scroll(scroll, "units")

    def _scroll_listboxes_sync(self, *args):
        for listbox in self._listboxes_cache:
            listbox.yview(*args)

    def _scroll_listboxes_and_scrollbar_sync(self, *args):
        for listbox in self._listboxes_cache:
            listbox.yview_moveto(args[0])
        if self._vsb:
            self._vsb.set(*args)

    def _on_header_clicked(self, event, i):
        if self._titles:
            self._update_sorting(i)
        for handler in self._header_clicked_handlers:
            handler(self, self._titles, i)

    def _on_row_selected(self, event, column_index):
        selection = event.widget.curselection()
        if not selection:
            return
        self._current_row_index = selection[0]
        self._current_column_index = column_index
        if self._selection is not None and self._select_mode == MULTIPLE:
            selection = self._fix_selection_in_multiple_selectmode(selection)
        self._manage_selection_garbage(selection)
        self._selection = selection
        self._sync_selection()
        # Notify handlers
        for handler in self._row_selected_handlers:
            if self._select_mode == SINGLE or self._select_mode == BROWSE:
                handler(self, self._data[self._selection[0]], self._selection[0], column_index)
            elif self._select_mode == MULTIPLE or self._select_mode == EXTENDED:
                handler(self, [self._data[row] for row in self._selection],
                        self._selection, column_index)

    def _build_handler_for_row_event(self, event, handler, i):
        row_index = event.widget.nearest(event.y)
        handler(self, self._data[row_index], row_index, i)

    def _fix_selection_in_multiple_selectmode(self, selection):
        fixed_selection = list(selection)
        if self._current_row_index in fixed_selection:
            fixed_selection.remove(self._current_row_index)
        else:
            fixed_selection.append(self._current_row_index)
        return tuple(fixed_selection)

    def _manage_selection_garbage(self, selection):
        if self._selection is None:
            return
        if self._select_mode in (SINGLE, BROWSE):
            if self._selection[0] != selection[0]:
                self._selection_garbage = self._selection
            else:
                self._selection_garbage = None
        elif self._select_mode == MULTIPLE:
            if len(self._selection) > len(selection):
                self._selection_garbage = tuple([i for i in self._selection if i not in selection])
            else:
                self._selection_garbage = None
        elif self._select_mode == EXTENDED:
            self._selection_garbage = tuple([i for i in self._selection if i not in selection])

    def _sync_selection(self):
        if self._select_mode == SINGLE or self._select_mode == BROWSE:
            if self._selection is not None:
                self._sync_selection_for_single_or_browse_mode()
        elif self._select_mode == MULTIPLE or self._select_mode == EXTENDED:
            self._sync_selection_for_multiple_or_extended_mode()

    def _sync_selection_for_single_or_browse_mode(self):
        for i, listbox in enumerate(self._listboxes_cache):
            if self._selection_garbage:
                listbox.itemconfig(self._selection_garbage[0],
                                   background=self._default_listbox_background,
                                   foreground=self._default_listbox_foreground)
            listbox.itemconfig(self._selection[0], background=self._default_listbox_selectbackground,
                               foreground=self._default_listbox_selectforeground)

    def _sync_selection_for_multiple_or_extended_mode(self):
        for i, listbox in enumerate(self._listboxes_cache):
            if self._selection_garbage:
                for x in self._selection_garbage:
                    listbox.itemconfig(x, background=self._default_listbox_background,
                                       foreground=self._default_listbox_foreground)
            for x in self._selection:
                listbox.itemconfig(x, background=self._default_listbox_selectbackground,
                                   foreground=self._default_listbox_selectforeground)
        if self._select_mode == MULTIPLE:
            if self._current_row_index in self._selection:
                selectbackground = self._default_listbox_selectbackground
                selectforeground = self._default_listbox_selectforeground
            else:
                selectbackground = self._default_listbox_background
                selectforeground = self._default_listbox_foreground
            self._listboxes_cache[self._current_column_index].config(
                selectbackground=selectbackground,
                selectforeground=selectforeground)

    def _adjust_selection_after_insertion(self, index, len_data):
        if not self._selection:
            return
        if index == "end":
            return
        cache = []
        for x in self._selection:
            if x >= index:
                x += len_data
            cache.append(x)
        self._selection = tuple(cache)

    def _update_sorting(self, i):
        if not self._sorting:
            return
        for index, label in enumerate(self._labels_sorting_cache):
            if index == i:
                continue
            label.grid_remove()
        for index, stringvar in enumerate(self._labels_sorting_stringvars_cache):
            if index == i:
                continue
            stringvar.set("")
        sorting_label = self._labels_sorting_stringvars_cache[i]
        if sorting_label.get() == "":
            self._labels_sorting_stringvars_cache[i].set(ASC)
            self._labels_sorting_cache[i].grid()
        elif sorting_label.get() == ASC:
            self._labels_sorting_stringvars_cache[i].set(DESC)
            self._labels_sorting_cache[i].grid()
        elif sorting_label.get() == DESC:
            self._labels_sorting_stringvars_cache[i].set("")
            self._labels_sorting_cache[i].grid_remove()
        self._sort_data(i)

    def _sort_data(self, i):
        sorting_label_stringvar = self._labels_sorting_stringvars_cache[i]
        if sorting_label_stringvar.get() == ASC:
            self._cache = self._data
            data_sorted = self._table_sorter(self._cache, i, len(self._titles))
        elif sorting_label_stringvar.get() == DESC:
            data_sorted = self._table_sorter(self._cache, i, len(self._titles),
                                             sorting="desc")
        elif sorting_label_stringvar.get() == "":
            data_sorted = self._cache
            self._cache = None
        self._reset_data(data_sorted)

    def _table_sorter(self, data, index, count_columns, sorting="asc"):
        reverse = False if sorting == "asc" else True
        data_sorted = sorted(data,
                             key=operator.itemgetter(*range(index, count_columns)),
                             reverse=reverse)
        return data_sorted

    def _reset_titles(self, titles):
        if not titles:
            return
        if not self._titles:
            self._titles = titles
            self._build()
        elif self._titles and len(titles) == len(self._titles):
            for i, title in enumerate(titles):
                self._labels_titles_stringvars_cache[i].set(title)
        else:
            raise PyrusticTableException("Incorrect length of titles")

    def _reset_data(self, data):
        if not data:
            return
        if not self._titles:
            raise PyrusticTableException("Please submit titles first !")
        # check data
        self._check_data_row_size(data)
        # clean listboxes
        self.clear()
        self._insert(0, data)

    def _insert(self, index, elements):
        # update self._data
        pos = index
        if index == "end":
            pos = len(self._data)
        self._data[pos:pos] = elements
        if self._mask:
            elements = [self._mask(i, element) for i, element in enumerate(elements)]
            self._check_data_row_size(elements)
        ignored_i = 0
        for i, col in enumerate(zip(*elements)):
            if i in self._hidden_columns:
                ignored_i += 1
                continue
            i -= ignored_i
            column_data = [(c if c is not None else "") for c in col]
            self._listboxes_cache[i].insert(index, *column_data)

    def _check_data_row_size(self, data):
        regular_size = len(self._titles) - len(self._hidden_columns)
        for row in data:
            if (len(row) - len(self._hidden_columns)) != regular_size:
                raise PyrusticTableException("Invalid data size")
        return True

    def _on_configure_window(self, event):
        self._canvas.config(height=self._window.winfo_height())
        self._canvas.config(width=self._window.winfo_width())
        self._canvas.config(scrollregion=self._canvas.bbox("all"))

    def _parse_options(self, options):
        self._body_options = options["body"] if "body" in options else {}
        self._hsb_options = options["hsb"] if "hsb" in options else {}
        self._vsb_options = options["vsb"] if "vsb" in options else {}
        self._canvas_options = options["canvas"] if "canvas" in options else {}
        self._frame_window_options = options["frame_window"] if "frame_window" in options else {}
        self._frame_header_options = options["frame_header"] if "frame_header" in options else {}
        self._label_sorting_options = options["label_sorting"] if "label_sorting" in options else {}
        self._label_title_options = options["label_title"] if "label_title" in options else {}
        self._listbox_column_options = options["listbox_column"] if "listbox_column" in options else {}




if __name__ == "__main__":

    # data
    titles = ["Name", "Age"]
    data = [("Jackson", 22), ("Pollock", 57), ("John", 24), ("Poly", 79),
            ("Joyce", 21), ("Johnny", 38), ("Jack", 29), ("Bam", 69),
            ("Joshua", 23), ("Matthew", 79), ("Mateo", 42), ("Willy", 39)]
    # app
    root = tk.Tk()
    table = Table(root, titles=titles, data=data, hidden_columns=(0,))
    table.handle_row_selected(lambda *args: print(args))
    table.body.pack()
    table.insert(0, (("Matrix", 34),))
    root.mainloop()
