import tkinter as tk
import operator
from pyrustic.exception import PyrusticTableException
from pyrustic.viewable import Viewable


# Allowed Options for columns
COLUMN_OPTIONS = ["background", "borderwidth", "cursor",
                  "disabledforeground", "exportselection", "font",
                  "foreground", "height", "highlightbackground",
                  "highlightcolor", "highlightthickness", "justify",
                  "relief", "selectbackground", "selectborderwidth",
                  "selectforeground", "setgrid", "state", "takefocus",
                  "width"]

# Components of table
BODY = "body"
VSB = "vsb"
HSB = "hsb"
CANVAS = "canvas"
FRAME_BACKGROUND = "frame_background"
FRAMES_HEADERS = "frames_headers"
LISTBOXES_COLUMNS = "listboxes_columns"
LABELS_SORTING = "labels_sorting"
LABELS_TITLES = "labels_titles"

# Layout
EQUALLY = "equally"
PROPORTIONALLY = "proportionally"

# Selection modes for rows
SINGLE = "single"
BROWSE = "browse"
MULTIPLE = "multiple"
EXTENDED = "extended"

# Orient
BOTH = "both"
VERTICAL = "vertical"
HORIZONTAL = "horizontal"

# sort data as
ASC = "[+]"
DESC = "[-]"


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


class Table(Viewable):  # TODO the select_mode MULTIPLE is buggy !
    """
    Table supports data sorting, multiple selection modes, and more...

    Example:

        import tkinter as tk
        from pyrustic.widget.table import Table

        root = tk.Tk()
        my_titles = ("Name", "Job")
        my_data = (("Jack", "Architect"), ("Diana", "Physicist"))
        table = Table(root, titles=my_titles, data=my_data)
        table.build_pack()
        root.mainloop()

    """
    def __init__(self,
                 master=None,
                 titles=None,
                 data=None,
                 hidden_columns=None,
                 sorting=True,
                 mask=None,
                 select_mode=BROWSE,
                 layout=EQUALLY,
                 orient=BOTH,
                 options=None):
        """
        PARAMETERS:

        - master: widget parent. Example: an instance of tk.Frame

        - titles: sequence of titles. Example: ("Name", "Job")

        - data: sequence of sequences. Each sub-sequence must have same size as titles.
            Example: ( ("Jack, "Architect"), ("Diana", "Physicist") )

        - hidden_columns: sequence of columns to hide.
            Example: (1, 2) will hide the column at the index 1 and 2.
            Example: (0, ) will hide only the first column

        - sorting: boolean, set to True if you want the table to be able to do sorting when user
            clicks on a column title. Default: True

        - mask: a callable that will be called at each insertion of line of data
        in the table.
            The mask must accept 2 arguments:
                - index: int, index of the row (line)
                - data: the sequence of strings to insert at this given row
            The mask must returns a new data with same length or the same old data

        - select_mode: selection modes: SINGLE, BROWSE,
         MULTIPLE and EXTENDED. Default: SINGLE.
         Selection modes are the same as described in the tk.Listbox's documentation.

        - layout: EQUALLY or PROPORTIONALLY. Default: EQUALLY

        - orient: orientation for scrollbars. BOTH or VERTICAL or HORIZONTAL

        - options: dictionary of widgets options
            The widgets keys are: BODY, VSB, HSB, CANVAS, FRAME_BACKGROUND,
            FRAMES_HEADERS, LISTBOXES_COLUMNS, LABELS_SORTING and LABELS_TITLES.
            Example: Assume that you want to set the BODY's background to black
            and the horizontal scrollbar's background to red:
                options = {"BODY": {"background": "red"},
                           "HSB": {"background": "black"}}
        """
        self._options = {} if options is None else options
        if "LISTBOXES_COLUMNS" in self._options:
            _verify_options(self._options["column"])
        self._master = master
        self._titles_cache = () if titles is None else titles
        self._titles = []
        self._data_cache = () if data is None else data
        self._data = []
        self._hidden_columns = () if hidden_columns is None else hidden_columns
        self._sorting = sorting
        self._mask = mask
        self._select_mode = select_mode
        self._layout = layout
        self._orient = orient
        self._body_options = None
        self._hsb_options = None
        self._vsb_options = None
        self._canvas_options = None
        self._frame_background_options = None
        self._frames_headers_options = None
        self._labels_sorting_options = None
        self._labels_titles_options = None
        self._listboxes_columns_options = None
        self._parse_options(self._options)
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
        self._background = None
        self._background_id = None
        self._vsb = None
        self._hsb = None
        self._hsb_under_mouse = False
        # Sorry but the select_mode MULTIPLE is buggy
        if select_mode == MULTIPLE:
            raise PyrusticTableException("Sorry but the selection mode MULTIPLE is buggy")


    # ==============================================
    #                   PROPERTIES
    # ==============================================
    @property
    def master(self):
        return self._master

    @property
    def body(self):
        return self._body

    @property
    def titles(self):
        return self._titles

    @titles.setter
    def titles(self, titles):
        """
        Titles are a sequence of strings. This property overwrite the existing titles.
        """
        self._reset_titles(titles)

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data):
        """
        Data is a sequence of sequences of strings.
        This property overwrite the existing data.
        Example:
            Assume that the titles are: ("Name", "Age")
            Data: ( ("Jack", 56), ("Jane", 47) )
        """
        self._reset_data(data)

    @property
    def hidden_columns(self):
        return self._hidden_columns

    @hidden_columns.setter
    def hidden_columns(self, val):
        """
        val: sequence of indexes to hide.
        Warning, even if you want to hide just one index,
        you should put this index into a tuple or list.
        Example: hide the column of index 1: (1, ) or [1]
        """
        self._hidden_columns = val

    @property
    def mask(self):
        return self._mask

    @mask.setter
    def mask(self, val):
        """
        val: a callable that will be called at each insertion of line of data
        in the table.
            The mask must accept 2 arguments:
                - index: int, index of the row (line)
                - data: the sequence of strings to insert at this given row
            The mask must returns a new data with same length or the same old data
        """
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
        """
        returns the length of columns and rows: (rows, cols)
        Example:
            Assume that the table has 3 columns and 10 rows,
            this property will return (10, 3)
        """
        return len(self._data), len(self._titles)

    @property
    def components(self):
        """
        Get the components (widgets instances) used to build this dialog.

        This property returns a dict. The keys are:
            BODY, VSB, HSB, CANVAS, FRAME_BACKGROUND,
            FRAMES_HEADERS, LISTBOXES_COLUMNS, LABELS_SORTING and LABELS_TITLES
        Warning: FRAMES_HEADERS, LABELS_TITLES, LABELS_SORTING
         and LISTBOXES_COLUMNS are sequences of widgets by index
        """
        return self._components

    @property
    def selection(self):
        """
        Return a sequence of the current selection.
        selection = ( item_1, item_2, ...)
        item_i = {"index": int, "data": data}
        data = a sequence of string representing the row at the index.
        """
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
        This will overwrite the titles and/or data with the new given titles or data
        """
        if titles:
            self.titles = titles
        if data:
            self.data = data

    def insert(self, index, data):
        """
        Insert into the table this data at this index.
        Index is an integer or the string "end" (meaning, put the data at the end of table).
        This method doesn't wipe the previous data stored at this index but instead,
        pull that data down.

        data is a sequence of sequences of strings.

        Example:
        Assume you want to push the new line ("Matrix", "Cameraman") at index 0.
            insert(0, [("Matrix", "Cameraman")])
        Assume you want to push ("Matrix", "Cameraman") and ("Diana", "Seller")
        at index "end".
            insert("end", [("Matrix", "Cameraman"), ("Diana", "Seller")])
        """
        if self._check_data_row_size(data):
            self._insert(index, data)
            self._adjust_selection_after_insertion(index, len(data))

    def get(self, index_start, index_end=None):
        """
        Returns a line if you don't give a 'index_end'.
        Returns a sequence of lines if you give a 'index_end'.
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
        Deletes lines (rows) from the table
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
        This callback will be called at the event 'row selection':
            handler(table, row_data, row_index, column_index)
        """
        self._row_selected_handlers.append(handler)

    def handle_row_event(self, sequence, handler):
        """
        This callback will be called at a specific row event (sequence = string):
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
        Configure column. If index is None, all columns will be configured
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
        If index is None, returns a sequence of options of listboxes (columns).
        Else returns the options of the column at the given index
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
        self._components[BODY] = self._body
        # reset titles and data
        self._reset_titles(self._titles_cache)
        self._reset_data(self._data_cache)

    def _on_display(self):
        pass

    def _on_destroy(self):
        pass

    def _build(self):
        self._body.columnconfigure(0, weight=1)
        self._body.rowconfigure(0, weight=1)
        self._canvas = tk.Canvas(self._body, cnf=self._canvas_options)
        self._components[CANVAS] = self._canvas
        self._canvas.grid(row=0, column=0, sticky="nswe")
        self._background = tk.Frame(self._canvas, self._frame_background_options)
        self._components[FRAME_BACKGROUND] = self._background
        self._background_id = self._canvas.create_window(0, 0,
                                                         window=self._background,
                                                         anchor="nw")
        self._background.bind("<Configure>", self._on_configure_background, "+")
        self._build_header_and_columns()
        self._extract_listboxes_color()
        self._set_scrollbars()

    def _build_header_and_columns(self):
        self._components[FRAMES_HEADERS] = []
        self._components[LABELS_SORTING] = []
        self._components[LABELS_TITLES] = []
        self._components[LISTBOXES_COLUMNS] = []
        ignored_i = 0
        for i, title in enumerate(self._titles):
            if i in self._hidden_columns:
                ignored_i += 1
                continue
            i -= ignored_i
            # Configure Background Grid
            if self._layout == EQUALLY:
                self._background.columnconfigure(i, weight=1, uniform=1)
            # Build Header
            # - install header frame
            frame_header = tk.Frame(self._background,
                                    class_="TableHeaderFrame",
                                    cnf=self._frames_headers_options)
            self._components[FRAMES_HEADERS].append(frame_header)
            frame_header.grid(row=0, column=i, sticky="nswe")
            frame_header.columnconfigure(1, weight=1)
            self._header_frames_cache.append(frame_header)
            # - install sorting label
            label_sorting_stringvar = tk.StringVar()
            self._labels_sorting_stringvars_cache.append(label_sorting_stringvar)
            label_sorting = tk.Label(frame_header,
                                     textvariable=label_sorting_stringvar,
                                     cnf=self._labels_sorting_options)
            self._components[LABELS_SORTING].append(label_sorting)
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
                                   cnf=self._labels_titles_options)
            self._components[LABELS_TITLES].append(label_title)
            label_title.grid(row=0, column=1, sticky="nswe")
            label_title.bind("<Button-1>",
                             lambda event, i=i: self._on_header_clicked(event, i), "+")
            self._labels_titles_cache.append(label_title)
            # Build Columns
            listbox = tk.Listbox(self._background,
                                 activestyle="none",
                                 selectmode=BROWSE if self._select_mode == MULTIPLE
                                 else self._select_mode,
                                 cnf=self._listboxes_columns_options, takefocus=0)
            self._components[LISTBOXES_COLUMNS].append(listbox)
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
        if self._orient in (BOTH, HORIZONTAL, "x", "h"):
            self._hsb = tk.Scrollbar(self._body, name="hsb",
                                     orient="horizontal",
                                     command=self._canvas.xview)
            self._components[HSB] = self._hsb
            self._hsb.grid(row=1, column=0, columnspan=2, sticky="we")
            self._hsb.bind("<Button-4>", self._on_mouse_wheel, "+")
            self._hsb.bind("<Button-5>", self._on_mouse_wheel, "+")
            self._canvas.config(xscrollcommand=self._hsb.set)
        if self._orient in (BOTH, VERTICAL, "y", "v"):
            self._vsb = tk.Scrollbar(self._body, name="vsb",
                                     orient="vertical",
                                     command=self._scroll_listboxes_sync)
            self._components[VSB] = self._vsb
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

    def _table_sorter(self, data, index, count_columns, sorting=ASC):
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

    def _on_configure_background(self, event):
        self._canvas.config(height=self._background.winfo_height())
        self._canvas.config(width=self._background.winfo_width())
        self._canvas.config(scrollregion=self._canvas.bbox("all"))

    def _parse_options(self, options):
        self._body_options = (options[BODY] if BODY in options else {})
        self._hsb_options = (options[HSB] if HSB in options else {})
        self._vsb_options = (options[VSB] if VSB in options else {})
        self._canvas_options = (options[CANVAS] if
                                CANVAS in options else {})
        self._frame_background_options = (options[FRAME_BACKGROUND]
                                      if FRAME_BACKGROUND in options else {})
        self._frames_headers_options = (options[FRAMES_HEADERS]
                                      if FRAMES_HEADERS in options else {})
        self._labels_sorting_options = (options[LABELS_SORTING]
                                       if LABELS_SORTING in options else {})
        self._labels_titles_options = (options[LABELS_TITLES]
                                     if LABELS_TITLES in options else {})
        self._listboxes_columns_options = (options[LISTBOXES_COLUMNS]
                                        if LISTBOXES_COLUMNS in options else {})


if __name__ == "__main__":
    # data
    titles = ["Name", "Age"]
    data = [("Jackson", 22), ("Pollock", 57), ("John", 24), ("Poly", 79),
            ("Joyce", 21), ("Johnny", 38), ("Jack", 29), ("Bam", 69),
            ("Joshua", 23), ("Matthew", 79), ("Mateo", 42), ("Willy", 39)]
    # app
    root = tk.Tk()
    table = Table(root, titles=titles, data=data)
    table.build_pack()
    table.handle_row_selected(lambda *args: print(args))
    root.mainloop()
