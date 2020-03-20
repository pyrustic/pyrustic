import tkinter as tk

from pyrustic.abstract.viewable import Viewable
from pyrustic.exception import PyrusticTableException

"""
Table
=====
Table(master=None, header=[], data=[], hidden_indexes=[],
        mask=None, select_mode=BROWSE, layout=EQUALLY,
        stylesheet=None, style=None, orient="both",
        canvas_padx=(0, 0), canvas_pady=(0, 0), sticky="nswe",
        options={}, header_options={}, column_options={},
        canvas_options={}, window_options={}, 
        vsb_options={}, hsb_options={}, raise_exception=True)
    
    PARAMETERS
    ==========
    - master: the widget parent
    
    - header: sequence of titles for the table. Example: Table with 2 columns: ["Names", "Ages"]
    
    - data: sequence of data to fill rows. Example, a table with 2 columns and 3 rows:
        [ ("Jack", "67"), ("Bauer", "87"), ("John", "97") ]
    
    - hidden_indexes: indexes to hide while displaying data. Example: [1, 3] hides indexes 1 and 3
    
    - mask: None or a function accepting 2 arguments. 
        That function is called for each row before display them. 
        Arguments are: an integer index representing a row, a sequence of string elements (the row)
        The function must return the same sequence of elements or an edited version with same size
    
    - select_mode: SINGLE, BROWSE, MULTIPLE, EXTENDED. All are defined in this file table.py
        You can still use strings in lowercase. Default select_mode is BROWSE.
        Selection modes are described in the section 'SELECTION MODES'
    
    - layout: EQUALLY or PROPORTIONALLY. All are defined in this file table.py
        You can still use strings in lowercase. Default layout is EQUALLY.
        Layout is about how u want the grid representing the table looks.
    
    - stylesheet: could be a string or a tuple. 
        String, if it is the path to a tk stylesheet (Xdefault).
        Tuple as this: (str_path_to_stylesheet, int_priority) 
    
    - style: [ (str_pattern, str_value, int_priority), (str_pattern, str_value), ...]
    
    - orient: could be None, or "both" or "vertical" or "horizontal" or "x" or "y" or "v" or "h"
    
    - canvas_padx: tuple to set horitonzal pad around canvas
    
    - canvas_pady: tuple to set vertical pad around canvas
    
    - sticky: sticky option for canvas. By default is "nswe"
    
    - options: options for the body. 
        Example: {"background": "red", "foreground": "red"}
    
    - header_options: options for header. Example: {"background": "red", "foreground": "red"}
    
    - column_options: options for columns. Example: {"background": "red", "foreground": "red"}
    
    - canvas_options: options for canvas. Example: {"background": "red", "foreground": "red"}
    
    - window_options: options for window. Example: {"background": "red", "foreground": "red"}
    
    - vsb_options: options for vertical scrollbar.
        Example: {"background": "red", "foreground": "red"}
    
    - hsb_options: options for horizontal scrollbar.
        Example: {"background": "red", "foreground": "red"}
        
    - raise_exception: boolean, by default is True. Will typically raise PyrusticTableException
    
    PROPERTIES
    ==========
    - master:           get
    - body:             get
    - header:           get|set
    - hidden_indexes:   get
    - data:             get|set
    - size:             get
    - vsb:              get the widget vsb instance
    - hsb:              get the widget hsb instance
    - orient:           get
    
    METHODS
    =======
    - fill(self, header=None, data=None)
    - insert(self, index, *elements)
    - get(self, index_debut, index_fin=None)
    - content(self)
    - delete(self, index_debut, index_fin=None)
    - handle_header_clicked(self, handler)
    - handle_header_event(self, sequence, handler)
    - handle_row_selected(self, handler)
    - handle_row_event(self, sequence, handler)
    - see(self, index="end")
    - config_header(self, index=None, **options)
    - config_column(self, index=None, **options)
    - cget_header(self, index=None, option="background")
    - cget_column(self, index=None, option="background")
    - destroy(self)
    
    Table options:
    ==============
    background
    borderwidth
    cursor
    height
    highlightbackground
    highlightcolor
    highlightthickness
    name
    padx
    pady
    relief
    takefocus
    width

    Header options:
    ===============
    activebackground
    activeforeground
    anchor
    background
    bitmap
    borderwidth
    cursor
    compound
    disabledforeground
    font
    foreground
    height
    highlightbackground
    highlightcolor
    highlightthickness
    image
    justify
    padx
    pady
    relief
    state
    text
    textvariable
    takefocus
    underline
    width
    wraplength

    Column options:
    ===============
    background
    borderwidth
    cursor
    disabledforeground
    exportselection
    font
    foreground
    height
    highlightbackground
    highlightthickness
    justify
    relief
    selectbackground
    selectborderwidth 
    selectforeground
    setgrid
    state
    takefocus
    width
    
    SELECTION MODES
    ===============

    It determines how many items can be selected and how mouse drags alter the selection
    
    BROWSE: This is the default mode. Only one row can be selected. If you click on a row and then drag to a different row, the selection will follow the mouse. This is the default.
    
    SINGLE: Only one row can be selected. Drag the mouse won't have an effect.
    
    MULTIPLE: Any number of rows can be selected at once. Clicking on any row toggles whether or not it is selected.
    
    EXTENDED: Select any adjacent group of rows at once by clicking on the first row and dragging to the last row.

"""

# Options for table, header, and columns
TABLE_OPTIONS = ["background", "borderwidth", "cursor", "height", "highlightbackground",
                 "highlightcolor", "highlightthickness", "name", "padx", "pady", "relief", "takefocus",
                 "width"]

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
SINGLE = 'single'
BROWSE = 'browse'
MULTIPLE = 'multiple'
EXTENDED = 'extended'


STYLE = [("*Table*background", "red"),
         ("*Table*foreground", "blue")]


def _check_option(target, option, raise_exception):
    if target == HEADER:
        if option in HEADER_OPTIONS:
            return True
        if not raise_exception:
            return False
        raise PyrusticTableException("The header option -" + option
                                         + " doesn't exist. This is legal options for header: "
                                         + str(HEADER_OPTIONS))
    elif target == COLUMN:
        if option in COLUMN_OPTIONS:
            return True
        if not raise_exception:
            return False
        raise PyrusticTableException("The column option -" + option
                                         + " doesn't exist. This is legal options for column: "
                                         + str(COLUMN_OPTIONS))
    return False


def _verify_options(header_options, column_options, raise_exception):
    for option in header_options.keys():
        if not _check_option(HEADER, option, raise_exception):
            del header_options[option]
    for option in column_options.keys():
        if not _check_option(COLUMN, option, raise_exception):
            del column_options[option]


class Table(Viewable):

    def __init__(self,
                 master=None,
                 header=[],
                 data=[],
                 hidden_indexes=[],
                 mask=None,
                 select_mode=BROWSE,
                 layout=EQUALLY,
                 stylesheet=None,
                 style=None,
                 orient="both",
                 canvas_padx=(0, 0),
                 canvas_pady=(0, 0),
                 sticky="nswe",
                 options={},
                 header_options={},
                 column_options={},
                 canvas_options={},
                 window_options={},
                 vsb_options={},
                 hsb_options={},
                 raise_exception=True):
        _verify_options(header_options, column_options, raise_exception)
        self._body = tk.Frame(master=master, class_="Table", **options)
        self._master = master
        self._header = header
        self._data = []
        self._hidden_indexes = hidden_indexes
        self._mask = mask
        self._select_mode = select_mode
        self._layout = layout
        self._orient = orient
        self._canvas_padx = canvas_padx
        self._canvas_pady = canvas_pady
        self._sticky = sticky
        self._options = options
        self._header_options = header_options
        self._column_options = column_options
        self._canvas_options = canvas_options
        self._window_options = window_options
        self._vsb_options = vsb_options
        self._hsb_options = hsb_options
        self._raise_exception = raise_exception
        # misc
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
        # cache for header's labels and listboxes
        self._labels_cache = []
        self._listboxes_cache = []
        # building table
        self._style(stylesheet, style)
        self._canvas = None
        self._window = None
        self._window_id = None
        self._vsb = None
        self._hsb = None
        self._hsb_under_mouse = False
        self.build()
        # fill data inside table with method _refresh()
        self._refresh(ROW, data)


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
    def header(self):
        return self._header

    @header.setter
    def header(self, header):
        if not header:
            return
        if not self._canvas:
            self.build()
        self._refresh(HEADER, header)

    @property
    def hidden_indexes(self):
        return self._hidden_indexes

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data):
        if not self._header:
            raise PyrusticTableException("Can't load data while Header is missing")
        self._refresh(ROW, data)

    @property
    def size(self):
        x = y = 0
        if self._header:
            x = len(self._header)
        if self._data:
            y = len(self._data)
        return x, y

    @property
    def vsb(self):
        return self._vsb

    @property
    def hsb(self):
        return self._hsb

    @property
    def orient(self):
        return self._orient
    # ==============================================
    #                 PUBLIC METHODS
    # ==============================================

    def build(self):
        if not self._header:
            return
        super().build()

    def fill(self, header=None, data=None):
        if header:
            self.header = header
        if data:
            self.data = data

    def insert(self, index, *elements):
        if self._check_data_row_size(elements):
            self._insert(index, elements)

    def get(self, index_debut, index_fin=None):
        if not index_fin:
            return self._data[index_debut]
        else:
            result = []
            index_fin_range = len(self._data) if index_fin == "end" else index_fin + 1
            for i in range(index_debut, index_fin_range):
                result.append(self._data[i])
            return result

    def content(self):
        return self._header, self._data

    def delete(self, index_debut, index_fin=None):
        if not index_fin:
            del self._data[index_debut]
        else:
            index_fin_range = len(self._data) if index_fin == "end" else index_fin + 1
            for _ in range(index_debut, index_fin_range):
                del self._data[index_debut]
        for listbox in self._listboxes_cache:
            listbox.delete(index_debut, index_fin)

    def handle_header_clicked(self, handler):
        # handler(table, header, header_index)
        self._header_clicked_handlers.append(handler)

    def handle_header_event(self, sequence, handler):
        # handler(table, header, header_index)
        for i, label in enumerate(self._labels_cache):
            label.bind(sequence,
                       lambda event,
                              self=self,
                              handler=handler,
                              i=i: handler(self, self._header, i), "+")

    def handle_row_selected(self, handler):
        # handler(table, row_data, row_index, column_index)
        self._row_selected_handlers.append(handler)

    def handle_row_event(self, sequence, handler):
        # handler(table, row_data, row_index, column_index)
        for i, listbox in enumerate(self._listboxes_cache):
            listbox.bind(sequence,
                         lambda event,
                                self=self,
                                handler=handler,
                                i=i: self._build_handler_for_row_event(event, handler, i), "+")

    def see(self, index="end"):
        if self._listboxes_cache:
            self._body.update_idletasks()
            table._listboxes_cache[0].see(index)

    def config_header(self, index=None, **options):
        if index is None:
            for x in self._labels_cache:
                x.config(**options)
        else:
            self._labels_cache[index].config(**options)

    def config_column(self, index=None, **options):
        if index is None:
            for x in self._listboxes_cache:
                x.config(**options)
                x.config(highlightcolor=x.cget("highlightbackground"))
        else:
            self._listboxes_cache[index].config(**options)
            self._listboxes_cache[index].config(highlightcolor=self._listboxes_cache[index].cget("highlightbackground"))

    def cget_header(self, index=None, option="background"):
        if index is not None and option:
            return self._labels_cache[index].cget(option)
        if option:
            return [x.cget(option) for x in self._labels_cache]

    def cget_column(self, index=None, option="background"):
        if index is not None and option:
            return self._listboxes_cache[index].cget(option)
        if option:
            return [x.cget(option) for x in self._listboxes_cache]

    def close(self):
        if self._body:
            self._body.destroy()
        for key, val in self.__dict__.items():
            self.__dict__[key] = None

    # ==============================================
    #                 PRIVATE METHODS
    # ==============================================

    def _style(self, steelsheet, style):
        if not self._body:
            return
        if isinstance(steelsheet, str):
            self._body.option_readfile(steelsheet)
        elif isinstance(steelsheet, tuple):
            self._body.option_readfile(steelsheet[0], steelsheet[1])
        if style:
            for x in style:
                if len(x) == 2 or len(x) == 3:
                    self._body.option_add(*x)

    def _on_start(self):
        self._body.columnconfigure(0, weight=1)
        self._body.rowconfigure(0, weight=1)
        self._canvas = tk.Canvas(self._body, self._canvas_options)
        self._canvas.grid(row=0, column=0, padx=self._canvas_padx,
                          pady=self._canvas_pady, sticky=self._sticky)
        self._window = tk.Frame(self._canvas, self._window_options)
        self._window_id = self._canvas.create_window(0, 0, window=self._window, anchor="nw")
        self._window.bind("<Configure>", self._on_configure, "+")

    def _on_build(self):
        self._build_header_and_columns()
        self._extract_listboxes_color()
        self._set_scrollbars()

    def _on_display(self):
        pass

    def _on_close(self, **kwargs):
        pass

    def _extract_listboxes_color(self):
        self._default_listbox_background = self._listboxes_cache[0].cget("background")
        self._default_listbox_foreground = self._listboxes_cache[0].cget("foreground")
        self._default_listbox_selectbackground = self._listboxes_cache[0].cget("selectbackground")
        self._default_listbox_selectforeground = self._listboxes_cache[0].cget("selectforeground")

    def _build_header_and_columns(self):
        for i, title in enumerate(self._header):
            # Configure Window Grid
            if self._layout is EQUALLY:
                self._window.columnconfigure(i, weight=1, uniform=1)
            # Build Header
            label = tk.Label(self._window,
                             text=title, **self._header_options)
            label.grid(row=0, column=i, sticky="nswe")
            label.bind("<Button-1>", lambda event, i=i: self._on_header_clicked(event, i), "+")
            self._labels_cache.append(label)
            # Build Columns
            listbox = tk.Listbox(self._window,
                                 activestyle="none",
                                 selectmode=BROWSE if self._select_mode == MULTIPLE
                                 else self._select_mode, **self._column_options, takefocus=0)
            listbox.config(highlightcolor=listbox.cget("highlightbackground"))
            listbox.grid(row=1, column=i, sticky="nswe")
            listbox.bind('<<ListboxSelect>>', lambda event, i=i: self._on_row_selected(event, i), "+")
            self._listboxes_cache.append(listbox)

    def _on_configure(self, event):
        if not self._window:
            return
        self._canvas.config(height=self._window.winfo_height())
        self._canvas.config(width=self._window.winfo_width())
        self._canvas.config(scrollregion=self._canvas.bbox("all"))

    def _insert(self, index, elements):
        # update self._data
        pos = index
        if index == "end":
            pos = len(self._data)
        self._data[pos:pos] = elements
        if self._mask:
            elements = [self._mask(i, element) for i, element in enumerate(elements)]
            self._check_data_row_size(elements)
        for i, (*col,) in enumerate(zip(*elements)):
            if i in self._hidden_indexes:
                continue
            column_data = [(c if c is not None else "") for c in col]
            self._listboxes_cache[i].insert(index, *column_data)

    def _check_data_row_size(self, data):
        regular_size = len(self._header)
        for row in data:
            if (len(row) - len(self._hidden_indexes)) != regular_size:
                if self._raise_exception:
                    raise PyrusticTableException("Your data should have same columns number for each row !")
                return False
        return True

    def _on_header_clicked(self, event, i):
        for handler in self._header_clicked_handlers:
            handler(self, self._header, i)

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
        fixed_selection = list(selection) # TODO javais mis originellement list(selection)
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
            self._body.update_idletasks()

    def _refresh(self, target, data):
        if target == HEADER:
            if self._header and len(data) != len(self._header):
                if self._raise_exception:
                    raise PyrusticTableException("Header has bad size")
            for i, title in enumerate(self.data):
                self._labels_cache[i].config(text=title)
        if target == ROW:
            # check data
            if not self._check_data_row_size(data):
                return
            # clean listboxes
            for listbox in self._listboxes_cache:
                listbox.delete(0, "end")
            self._insert(0, data)

    def _set_scrollbars(self):
        if self._orient in ("both", "horizontal", "x", "h"):
            self._hsb = tk.Scrollbar(self._body, class_="HorizontalScrollbar",
                                     orient="horizontal",
                                     command=self._canvas.xview)
            self._hsb.grid(row=1, column=0, columnspan=2, sticky="we")
            self._hsb.bind("<Button-4>", self._on_mouse_wheel, "+")
            self._hsb.bind("<Button-5>", self._on_mouse_wheel, "+")
            self._canvas.config(xscrollcommand=self._hsb.set)
        if self._orient in ("both", "vertical", "y", "v"):
            self._vsb = tk.Scrollbar(self._body, orient="vertical",
                                     class_="VerticalScrollbar",
                                     command=self._scroll_listboxes_sync)
            self._vsb.grid(row=0, column=1, sticky="ns")
        for listbox in self._listboxes_cache:
            listbox.config(yscrollcommand=self._scroll_listboxes_and_scrollbar_sync)

    def _on_mouse_wheel(self, event):
        # NB: event.num 5 fais descendre et event.num 4 fait monter
        # NB: event.delta négatif fait descendre et event.delta positif fait monter
        scroll = 1 if event.num == 5 or event.delta < 0 else -1
        # NB: scroll 1 fais descendre et scroll -1 fais monter
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

    # ==============================================
    #                 MAGIC METHODS
    # ==============================================
    def __getattr__(self, item):
        return getattr(self._body, item)


if __name__ == "__main__":

    # HEADER (3 items)
    header = ["Code", "Name", "Age"]

    # SHORT DATA (6 rows)
    short_data = [("BASH", "Linux", "39"),
                  ("EFRON", "Zack", "54"),
                  ("BOSS", "Big", "23"),
                  ("ACK", "Lama", "42"),
                  ("SYN", "Sweet", "98"),
                  ("DARK", "Hope", "72")]

    app = tk.Tk()
    screenwidth = app.winfo_screenwidth()
    screenheight = app.winfo_screenheight()
    app.geometry("{0}x{1}+0+0".format(screenwidth,
                                      screenheight))
    table = Table(app, header=header, orient="both", data=short_data,
                  select_mode=BROWSE,
                  options={"highlightcolor":"yellow",
                        "highlightthickness":10},
                  header_options={"background":"red"},
                  column_options={"background":"green",
                                  "selectbackground":"black",
                                  "selectforeground":"white"})
    table.config_column(height=3)
    table.handle_row_selected(lambda *args, **kwargs: print(args, kwargs))
    #table.data = short_data
    table.pack()
    app.mainloop()
