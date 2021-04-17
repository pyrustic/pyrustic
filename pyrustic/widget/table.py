import tkinter as tk
import operator
from pyrustic.exception import PyrusticTableException
from pyrustic import widget
from pyrustic.tkmisc import merge_cnfs


# Allowed Options for columns
COLUMN_OPTIONS = ["background", "borderwidth", "cursor",
                  "disabledforeground", "exportselection", "font",
                  "foreground", "height", "highlightbackground",
                  "highlightcolor", "highlightthickness", "justify",
                  "relief", "selectbackground", "selectborderwidth",
                  "selectforeground", "setgrid", "state", "takefocus",
                  "width"]

# Components of table
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


class Table(widget.Frame):  # TODO the select_mode MULTIPLE is buggy !
    """
    Table supports data sorting, multiple selection modes, and more...

    Example:
    ```python
    import tkinter as tk
    from pyrustic.widget.table import Table

    root = tk.Tk()
    my_titles = ("Name", "Job")
    my_data = (("Jack", "Architect"), ("Diana", "Physicist"))
    table = Table(root, titles=my_titles, data=my_data)
    table.build_pack()
    root.mainloop()
    ```

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
                 cnfs=None):
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
        self.__cnfs = merge_cnfs(None, cnfs,
                                 components=("body", VSB, HSB, CANVAS,
                        FRAME_BACKGROUND, FRAMES_HEADERS, LISTBOXES_COLUMNS,
                        LABELS_SORTING, LABELS_TITLES))
        super().__init__(master=master,
                         class_="Table",
                         cnf=self.__cnfs["body"],
                         on_build=self.__on_build,
                         on_display=self.__on_display,
                         on_destroy=self.__on_destroy)
        # check if listboxes options are valid
        _verify_options(self.__cnfs[LISTBOXES_COLUMNS])
        self.__titles_cache = () if titles is None else titles
        self.__titles = []
        self.__data_cache = () if data is None else data
        self.__data = []
        self.__hidden_columns = () if hidden_columns is None else hidden_columns
        self.__sorting = sorting
        self.__mask = mask
        self.__select_mode = select_mode
        self.__layout = layout
        self.__orient = orient
        self.__canvas_options = None
        self.__frame_background_options = None
        self.__frames_headers_options = None
        self.__labels_sorting_options = None
        self.__labels_titles_options = None
        self.__listboxes_columns_options = None
        # misc
        self.__components = {}
        self.__cache = None
        self.__current_sorting = None
        self.__current_column_index = None
        self.__current_row_index = None
        self.__selection_garbage = None
        self.__selection = None
        self.__header_clicked_handlers = []
        self.__header_event_handlers = {}
        self.__row_selected_handlers = []
        self.__row_event_handlers = {}
        self.__default_listbox_background = None
        self.__default_listbox_foreground = None
        self.__default_listbox_selectbackground = None
        self.__default_listbox_selectforeground = None
        # cache for sorting's labels, header's labels and listboxes
        self.__header_frames_cache = []
        self.__labels_sorting_cache = []
        self.__labels_titles_cache = []
        self.__listboxes_cache = []
        # string vars cache
        self.__labels_sorting_stringvars_cache = []
        self.__labels_titles_stringvars_cache = []
        # components
        self.__canvas = None
        self.__background = None
        self.__background_id = None
        self.__vsb = None
        self.__hsb = None
        self.__hsb_under_mouse = False
        # Sorry but the select_mode MULTIPLE is buggy
        if select_mode == MULTIPLE:
            raise PyrusticTableException("Sorry but the selection mode MULTIPLE is buggy")
        self.__view = self.build()

    # ==============================================
    #                   PROPERTIES
    # ==============================================
    @property
    def titles(self):
        return self.__titles

    @titles.setter
    def titles(self, titles):
        """
        Titles are a sequence of strings. This property overwrite the existing titles.
        """
        self.__reset_titles(titles)

    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, data):
        """
        Data is a sequence of sequences of strings.
        This property overwrite the existing data.
        Example:
            Assume that the titles are: ("Name", "Age")
            Data: ( ("Jack", 56), ("Jane", 47) )
        """
        self.__reset_data(data)

    @property
    def hidden_columns(self):
        return self.__hidden_columns

    @hidden_columns.setter
    def hidden_columns(self, val):
        """
        val: sequence of indexes to hide.
        Warning, even if you want to hide just one index,
        you should put this index into a tuple or list.
        Example: hide the column of index 1: (1, ) or [1]
        """
        self.__hidden_columns = val

    @property
    def mask(self):
        return self.__mask

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
        self.__mask = val

    @property
    def select_mode(self):
        return self.__select_mode

    @property
    def layout(self):
        return self.__layout

    @property
    def orient(self):
        return self.__orient

    @property
    def table_size(self):
        """
        returns the length of columns and rows: (rows, cols)
        Example:
            Assume that the table has 3 columns and 10 rows,
            this property will return (10, 3)
        """
        return len(self.__data), len(self.__titles)

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
        return self.__components

    @property
    def selection(self):
        """
        Return a sequence of the current selection.
        selection = ( item_1, item_2, ...)
        item_i = {"index": int, "data": data}
        data = a sequence of string representing the row at the index.
        """
        if not self.__selection:
            return ()
        data = []
        for i in self.__selection:
            cache = {"index": i, "data": self.__data[i]}
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
        if self.__check_data_row_size(data):
            self.__insert(index, data)
            self.__adjust_selection_after_insertion(index, len(data))

    def get(self, index_start, index_end=None):
        """
        Returns a line if you don't give a 'index_end'.
        Returns a sequence of lines if you give a 'index_end'.
        """
        if not index_end:
            return self.__data[index_start]
        else:
            result = []
            index_end_range = len(self.__data) if index_end == "end" else index_end + 1
            for i in range(index_start, index_end_range):
                result.append(self.__data[i])
            return result

    def delete(self, index_start, index_end=None):
        """
        Deletes lines (rows) from the table
        """
        if not index_end:
            del self.__data[index_start]
        else:
            index_fin_range = len(self.__data) if index_end == "end" else index_end + 1
            for _ in range(index_start, index_fin_range):
                del self.__data[index_start]
        for listbox in self.__listboxes_cache:
            listbox.delete(index_start, index_end)
        self.__selection_garbage = None
        self.__selection = None

    def clear(self):
        """
        Clear the table
        """
        for listbox in self.__listboxes_cache:
            listbox.delete(0, "end")
        self.__data = []

    def handle_row_selected(self, handler):
        """
        This callback will be called at the event 'row selection':
            handler(table, row_data, row_index, column_index)
        """
        self.__row_selected_handlers.append(handler)

    def handle_row_event(self, sequence, handler):
        """
        This callback will be called at a specific row event (sequence = string):
            handler(table, row_data, row_index, column_index)
        """
        for i, listbox in enumerate(self.__listboxes_cache):
            listbox.bind(sequence,
                         lambda event,
                                self=self,
                                handler=handler,
                                i=i: self.__build_handler_for_row_event(event, handler, i), "+")

    def see(self, index="end"):
        """
        The table will scroll to the given index
        """
        if self.__listboxes_cache:
            self.__listboxes_cache[0].see(index)

    def config_column(self, index=None, **options):
        """
        Configure column. If index is None, all columns will be configured
        """
        if index is None:
            for x in self.__listboxes_cache:
                x.config(**options)
                x.config(highlightcolor=x.cget("highlightbackground"))
        else:
            self.__listboxes_cache[index].config(**options)
            self.__listboxes_cache[index].config(highlightcolor=self.__listboxes_cache[index].cget("highlightbackground"))

    def cget_column(self, index=None, option="background"):
        """
        If index is None, returns a sequence of options of listboxes (columns).
        Else returns the options of the column at the given index
        """
        if index is not None and option:
            return self.__listboxes_cache[index].cget(option)
        if option:
            return [x.cget(option) for x in self.__listboxes_cache]

    # ==============================================
    #                 PRIVATE METHODS
    # ==============================================
    def __on_build(self):
        # reset titles and data
        self.__reset_titles(self.__titles_cache)
        self.__reset_data(self.__data_cache)

    def __on_display(self):
        pass

    def __on_destroy(self):
        pass

    def __build_table(self):
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.__canvas = tk.Canvas(self, name=CANVAS,
                                  cnf=self.__cnfs[CANVAS])
        self.__components[CANVAS] = self.__canvas
        self.__canvas.grid(row=0, column=0, sticky="nswe")
        self.__background = tk.Frame(self.__canvas, self.__frame_background_options)
        self.__components[FRAME_BACKGROUND] = self.__background
        self.__background_id = self.__canvas.create_window(0, 0,
                                                           window=self.__background,
                                                           anchor="nw")
        self.__background.bind("<Configure>", self.__on_configure_background, "+")
        self.__build_header_and_columns()
        self.__extract_listboxes_color()
        self.__set_scrollbars()

    def __build_header_and_columns(self):
        self.__components[FRAMES_HEADERS] = []
        self.__components[LABELS_SORTING] = []
        self.__components[LABELS_TITLES] = []
        self.__components[LISTBOXES_COLUMNS] = []
        ignored_i = 0
        for i, title in enumerate(self.__titles):
            if i in self.__hidden_columns:
                ignored_i += 1
                continue
            i -= ignored_i
            # Configure Background Grid
            if self.__layout == EQUALLY:
                self.__background.columnconfigure(i, weight=1, uniform=1)
            # Build Header
            # - install header frame
            frame_header = tk.Frame(self.__background,
                                    cnf=self.__cnfs[FRAMES_HEADERS])
            self.__components[FRAMES_HEADERS].append(frame_header)
            frame_header.grid(row=0, column=i, sticky="nswe")
            frame_header.columnconfigure(1, weight=1)
            self.__header_frames_cache.append(frame_header)
            # - install sorting label
            label_sorting_stringvar = tk.StringVar()
            self.__labels_sorting_stringvars_cache.append(label_sorting_stringvar)
            label_sorting = tk.Label(frame_header,
                                     textvariable=label_sorting_stringvar,
                                     cnf=self.__cnfs[LABELS_SORTING])
            self.__components[LABELS_SORTING].append(label_sorting)
            label_sorting.grid(row=0, column=0)
            label_sorting.bind("<Button-1>",
                               lambda event, i=i: self.__on_header_clicked(event, i), "+")
            label_sorting.grid_remove()
            self.__labels_sorting_cache.append(label_sorting)
            # - install title label
            label_title_stringvar = tk.StringVar()
            label_title_stringvar.set(title)
            self.__labels_titles_stringvars_cache.append(label_title_stringvar)
            label_title = tk.Label(frame_header,
                                   textvariable=label_title_stringvar,
                                   cnf=self.__cnfs[LABELS_TITLES])
            self.__components[LABELS_TITLES].append(label_title)
            label_title.grid(row=0, column=1, sticky="nswe")
            label_title.bind("<Button-1>",
                             lambda event, i=i: self.__on_header_clicked(event, i), "+")
            self.__labels_titles_cache.append(label_title)
            # Build Columns
            listbox = tk.Listbox(self.__background,
                                 activestyle="none",
                                 selectmode=BROWSE if self.__select_mode == MULTIPLE
                                 else self.__select_mode,
                                 cnf=self.__cnfs[LISTBOXES_COLUMNS], takefocus=0)
            self.__components[LISTBOXES_COLUMNS].append(listbox)
            listbox.config(highlightcolor=listbox.cget("highlightbackground"))
            listbox.grid(row=1, column=i, sticky="nswe")
            listbox.bind('<<ListboxSelect>>',
                         lambda event, i=i: self.__on_row_selected(event, i), "+")
            self.__listboxes_cache.append(listbox)

    def __extract_listboxes_color(self):
        self.__default_listbox_background = self.__listboxes_cache[0].cget("background")
        self.__default_listbox_foreground = self.__listboxes_cache[0].cget("foreground")
        self.__default_listbox_selectbackground = self.__listboxes_cache[0].cget("selectbackground")
        self.__default_listbox_selectforeground = self.__listboxes_cache[0].cget("selectforeground")

    def __set_scrollbars(self):
        if self.__orient in (BOTH, HORIZONTAL, "x", "h"):
            self.__hsb = tk.Scrollbar(self, name=HSB,
                                      orient="horizontal",
                                      command=self.__canvas.xview)
            self.__components[HSB] = self.__hsb
            self.__hsb.grid(row=1, column=0, columnspan=2, sticky="we")
            self.__hsb.bind("<Button-4>", self.__on_mouse_wheel, "+")
            self.__hsb.bind("<Button-5>", self.__on_mouse_wheel, "+")
            self.__canvas.config(xscrollcommand=self.__hsb.set)
        if self.__orient in (BOTH, VERTICAL, "y", "v"):
            self.__vsb = tk.Scrollbar(self, name=VSB,
                                      orient="vertical",
                                      command=self.__scroll_listboxes_sync)
            self.__components[VSB] = self.__vsb
            self.__vsb.grid(row=0, column=1, sticky="ns")
        for listbox in self.__listboxes_cache:
            listbox.config(yscrollcommand=self.__scroll_listboxes_and_scrollbar_sync)

    def __on_mouse_wheel(self, event):
        # NB: event.num 5 to go down and event.num 4 to go up
        # NB: event.delta if negative, goes down, and event.delta if positive goes up
        scroll = 1 if event.num == 5 or event.delta < 0 else -1
        # NB: scroll 1 to go down and scroll -1 to go up
        if self.__orient in ("both", "horizontal", "h", "x",
                            "vertical", "v", "y"):
            self.__canvas.xview_scroll(scroll, "units")

    def __scroll_listboxes_sync(self, *args):
        for listbox in self.__listboxes_cache:
            listbox.yview(*args)

    def __scroll_listboxes_and_scrollbar_sync(self, *args):
        for listbox in self.__listboxes_cache:
            listbox.yview_moveto(args[0])
        if self.__vsb:
            self.__vsb.set(*args)

    def __on_header_clicked(self, event, i):
        if self.__titles:
            self.__update_sorting(i)
        for handler in self.__header_clicked_handlers:
            handler(self, self.__titles, i)

    def __on_row_selected(self, event, column_index):
        selection = event.widget.curselection()
        if not selection:
            return
        self.__current_row_index = selection[0]
        self.__current_column_index = column_index
        if self.__selection is not None and self.__select_mode == MULTIPLE:
            selection = self.__fix_selection_in_multiple_selectmode(selection)
        self.__manage_selection_garbage(selection)
        self.__selection = selection
        self.__sync_selection()
        # Notify handlers
        for handler in self.__row_selected_handlers:
            if self.__select_mode == SINGLE or self.__select_mode == BROWSE:
                handler(self, self.__data[self.__selection[0]], self.__selection[0], column_index)
            elif self.__select_mode == MULTIPLE or self.__select_mode == EXTENDED:
                handler(self, [self.__data[row] for row in self.__selection],
                        self.__selection, column_index)

    def __build_handler_for_row_event(self, event, handler, i):
        row_index = event.widget.nearest(event.y)
        handler(self, self.__data[row_index], row_index, i)

    def __fix_selection_in_multiple_selectmode(self, selection):
        fixed_selection = list(selection)
        if self.__current_row_index in fixed_selection:
            fixed_selection.remove(self.__current_row_index)
        else:
            fixed_selection.append(self.__current_row_index)
        return tuple(fixed_selection)

    def __manage_selection_garbage(self, selection):
        if self.__selection is None:
            return
        if self.__select_mode in (SINGLE, BROWSE):
            if self.__selection[0] != selection[0]:
                self.__selection_garbage = self.__selection
            else:
                self.__selection_garbage = None
        elif self.__select_mode == MULTIPLE:
            if len(self.__selection) > len(selection):
                self.__selection_garbage = tuple([i for i in self.__selection if i not in selection])
            else:
                self.__selection_garbage = None
        elif self.__select_mode == EXTENDED:
            self.__selection_garbage = tuple([i for i in self.__selection if i not in selection])

    def __sync_selection(self):
        if self.__select_mode == SINGLE or self.__select_mode == BROWSE:
            if self.__selection is not None:
                self.__sync_selection_for_single_or_browse_mode()
        elif self.__select_mode == MULTIPLE or self.__select_mode == EXTENDED:
            self.__sync_selection_for_multiple_or_extended_mode()

    def __sync_selection_for_single_or_browse_mode(self):
        for i, listbox in enumerate(self.__listboxes_cache):
            if self.__selection_garbage:
                listbox.itemconfig(self.__selection_garbage[0],
                                   background=self.__default_listbox_background,
                                   foreground=self.__default_listbox_foreground)
            listbox.itemconfig(self.__selection[0], background=self.__default_listbox_selectbackground,
                               foreground=self.__default_listbox_selectforeground)

    def __sync_selection_for_multiple_or_extended_mode(self):
        for i, listbox in enumerate(self.__listboxes_cache):
            if self.__selection_garbage:
                for x in self.__selection_garbage:
                    listbox.itemconfig(x, background=self.__default_listbox_background,
                                       foreground=self.__default_listbox_foreground)
            for x in self.__selection:
                listbox.itemconfig(x, background=self.__default_listbox_selectbackground,
                                   foreground=self.__default_listbox_selectforeground)
        if self.__select_mode == MULTIPLE:
            if self.__current_row_index in self.__selection:
                selectbackground = self.__default_listbox_selectbackground
                selectforeground = self.__default_listbox_selectforeground
            else:
                selectbackground = self.__default_listbox_background
                selectforeground = self.__default_listbox_foreground
            self.__listboxes_cache[self.__current_column_index].config(
                selectbackground=selectbackground,
                selectforeground=selectforeground)

    def __adjust_selection_after_insertion(self, index, len_data):
        if not self.__selection:
            return
        if index == "end":
            return
        cache = []
        for x in self.__selection:
            if x >= index:
                x += len_data
            cache.append(x)
        self.__selection = tuple(cache)

    def __update_sorting(self, i):
        if not self.__sorting:
            return
        for index, label in enumerate(self.__labels_sorting_cache):
            if index == i:
                continue
            label.grid_remove()
        for index, stringvar in enumerate(self.__labels_sorting_stringvars_cache):
            if index == i:
                continue
            stringvar.set("")
        sorting_label = self.__labels_sorting_stringvars_cache[i]
        if sorting_label.get() == "":
            self.__labels_sorting_stringvars_cache[i].set(ASC)
            self.__labels_sorting_cache[i].grid()
        elif sorting_label.get() == ASC:
            self.__labels_sorting_stringvars_cache[i].set(DESC)
            self.__labels_sorting_cache[i].grid()
        elif sorting_label.get() == DESC:
            self.__labels_sorting_stringvars_cache[i].set("")
            self.__labels_sorting_cache[i].grid_remove()
        self.__sort_data(i)

    def __sort_data(self, i):
        sorting_label_stringvar = self.__labels_sorting_stringvars_cache[i]
        if sorting_label_stringvar.get() == ASC:
            self.__cache = self.__data
            data_sorted = self.__table_sorter(self.__cache, i, len(self.__titles))
        elif sorting_label_stringvar.get() == DESC:
            data_sorted = self.__table_sorter(self.__cache, i, len(self.__titles),
                                              sorting="desc")
        elif sorting_label_stringvar.get() == "":
            data_sorted = self.__cache
            self.__cache = None
        self.__reset_data(data_sorted)

    def __table_sorter(self, data, index, count_columns, sorting=ASC):
        reverse = False if sorting == ASC else True
        data_sorted = sorted(data,
                             key=operator.itemgetter(*range(index, count_columns)),
                             reverse=reverse)
        return data_sorted

    def __reset_titles(self, titles):
        if not titles:
            return
        if not self.__titles:
            self.__titles = titles
            self.__build_table()
        elif self.__titles and len(titles) == len(self.__titles):
            for i, title in enumerate(titles):
                self.__labels_titles_stringvars_cache[i].set(title)
        else:
            raise PyrusticTableException("Incorrect length of titles")

    def __reset_data(self, data):
        if not data:
            return
        if not self.__titles:
            raise PyrusticTableException("Please submit titles first !")
        # check data
        self.__check_data_row_size(data)
        # clean listboxes
        self.clear()
        self.__insert(0, data)

    def __insert(self, index, elements):
        # update self._data
        pos = index
        if index == "end":
            pos = len(self.__data)
        self.__data[pos:pos] = elements
        if self.__mask:
            elements = [self.__mask(i, element) for i, element in enumerate(elements)]
            self.__check_data_row_size(elements)
        ignored_i = 0
        for i, col in enumerate(zip(*elements)):
            if i in self.__hidden_columns:
                ignored_i += 1
                continue
            i -= ignored_i
            column_data = [(c if c is not None else "") for c in col]
            self.__listboxes_cache[i].insert(index, *column_data)

    def __check_data_row_size(self, data):
        regular_size = len(self.__titles) - len(self.__hidden_columns)
        for row in data:
            if (len(row) - len(self.__hidden_columns)) != regular_size:
                raise PyrusticTableException("Invalid data size")
        return True

    def __on_configure_background(self, event):
        self.__canvas.config(height=self.__background.winfo_height())
        self.__canvas.config(width=self.__background.winfo_width())
        self.__canvas.config(scrollregion=self.__canvas.bbox("all"))


def _verify_options(column_options):
    for option in column_options.keys():
        if not _check_option(option):
            del column_options[option]


def _check_option(option):
    if option in COLUMN_OPTIONS:
        return True
    raise PyrusticTableException("The column option -" + option
                                 + " doesn't exist. These are legal options for column: "
                                 + str(COLUMN_OPTIONS))


if __name__ == "__main__":
    # data
    titles = ["Name", "Age"]
    data = [("Jackson", 22), ("Pollock", 57), ("John", 24), ("Poly", 79),
            ("Joyce", 21), ("Johnny", 38), ("Jack", 29), ("Bam", 69),
            ("Joshua", 23), ("Matthew", 79), ("Mateo", 42), ("Willy", 39)]
    # app
    root = tk.Tk()
    table = Table(root, titles=titles, data=data)
    table.pack()
    table.handle_row_selected(lambda *args: print(args))
    root.mainloop()
