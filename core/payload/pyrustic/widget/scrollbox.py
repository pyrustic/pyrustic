import tkinter as tk
from pyrustic.abstract.viewable import Viewable


"""
Skroll helps you to easily integrate scrollbars in your Tkinter-based application.
Scrollbox is part of Pyrustic Project.

Note: The 'box' is the frame on which u put your widgets. The 'box' is inside a canvas.
This canvas is packed in a frame called 'body'.
And around this canvas, there are scrollbars 'hsb' and 'vsb'.


Scrollbox(self, master=None, stylesheet=None, style=None, orient="both",
    canvas_padx=(0, 0), canvas_pady=(0, 0), sticky="nswe", options={},
    canvas_options={}, box_options={}, vsb_options={}, hsb_options={})

    PARAMETERS
    ==========
    - master: the tk object serving as parent
    
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
    
    - canvas_options: options for canvas. Example: {"background": "red", "foreground": "red"}
    
    - box_options: options for box. Example: {"background": "red", "foreground": "red"}
    
    - vsb_options: options for vertical scrollbar.
        Example: {"background": "red", "foreground": "red"}
    
    - hsb_options: options for horizontal scrollbar.
        Example: {"background": "red", "foreground": "red"} 

    PROPERTIES
    ==========
    - master:   get
    - body:     get
    - canvas:   get
    - box:      get|set
    - orient:   get
    - vsb:      get the widget vsb instance
    - hsb:      get the widget hsb instance

    METHODS
    =======
    - xview_moveto(self, fraction): xview scroll
    - yview_moveto(self, fraction): yview scroll
    - box_moveto(self, x, y): move box to (x, y) coordinates on the canvas
    - box_config(self, **options): to alter these specific options: anchor, state, height, width
    - clean(self): destroy the box. A new box will be created when needed
    - destroy(self): nicely destroy this table

    EXAMPLE
    =======
    import tkinter as tk
    from scrollbox import Scrollbox
    app = tk.Tk()
    scrollbox = Scrollbox(app)
    scrollbox.pack(expand=1, fill=tk.BOTH)
    tk.Button(scrollbox.box, text="Click").pack()
    app.mainloop()
"""




class Scrollbox(Viewable):



    def __init__(self,
                 master=None,
                 stylesheet=None,
                 style=None,
                 orient="both",
                 canvas_padx=(0, 0),
                 canvas_pady=(0, 0),
                 sticky="n",
                 options={},
                 canvas_options={},
                 box_options={},
                 vsb_options={},
                 hsb_options={}):
        self._body = tk.Frame(master=master, class_="Scrollbox", **options)
        self._master = master
        self._orient = orient
        self._canvas_padx = canvas_padx
        self._canvas_pady = canvas_pady
        self._sticky = sticky
        self._options = options
        self._canvas_options = canvas_options
        self._box_options = box_options
        self._vsb_options = vsb_options
        self._hsb_options = hsb_options
        self._canvas = None
        self._box = None
        self._box_id = None
        self._vsb = None
        self._hsb = None
        self._hsb_under_mouse = False
        self._is_scrollable = False
        self._bind_func_ids = ()
        self._style(stylesheet, style)
        self.build()

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
    def canvas(self):
        return self._canvas

    @property
    def box(self):
        if not self._box and self._body:
            self._create_box(tk.Frame(self._canvas))
        return self._box

    @box.setter
    def box(self, box):
        if box and self._body:
            self.clean()
            self._create_box(box)

    @property
    def orient(self):
        return self._orient

    @property
    def vsb(self):
        return self._vsb

    @property
    def hsb(self):
        return self._hsb

    # ==============================================
    #                 PUBLIC METHODS
    # ==============================================

    def xview_moveto(self, fraction):
        if self._canvas:
            self._canvas.xview_moveto(fraction)

    def yview_moveto(self, fraction):
        if self._canvas:
            self._canvas.yview_moveto(fraction)

    def box_moveto(self, x, y):
        if not self._box:
            return
        box_x, box_y = self._canvas.coords(self._box_id)
        add_x = add_y = 0
        if box_x == 0:
            add_x = x
        elif box_x < 0:
            add_x = (box_x * -1) + x
        elif box_x > 0:
            add_x = x - box_x
        if box_y == 0:
            add_y = y
        elif box_y < 0:
            add_y = (box_y * -1) + y
        elif box_y > 0:
            add_y = y - box_y
        self._canvas.move(self._box_id, add_x, add_y)

    def box_config(self, **options):
        """ options are: anchor, state, height, width """
        if self._box:
            self._canvas.itemconfig(self._box_id, **options)

    def clean(self):
        if self._box:
            self._canvas.delete(self._box_id)
            self._box.destroy()
            self._box_id = None
            self._box = None

    def destroy(self):
        if self._body:
            self._unbind_funcs()
            self._body.destroy()
            for key, val in self.__dict__.items():
                self.__dict__[key] = None

    # ==============================================
    #                 PRIVATE METHODS
    # ==============================================
    def _on_start(self):
        self._body.bind("<Enter>", self._on_enter_body, "+")
        self._body.bind("<Leave>", self._on_leave_body, "+")
        self._body.bind("<Unmap>", self._on_unmap_body, "+")
        self._body.bind("<Destroy>", self._on_destroy_body, "+")
        id_1 = self._body.bind_all("<MouseWheel>", self._on_mouse_wheel, "+")
        id_2 = self._body.bind_all("<Button-4>", self._on_mouse_wheel, "+")
        id_3 = self._body.bind_all("<Button-5>", self._on_mouse_wheel, "+")
        self._bind_func_ids = (id_1, id_2, id_3)
        self._body.columnconfigure(0, weight=1)
        self._body.rowconfigure(0, weight=1)
        self._canvas = tk.Canvas(self._body, **self._canvas_options)

    def _on_build(self):
        self._canvas.grid(row=0, column=0, padx=self._canvas_padx,
                          pady=self._canvas_pady, sticky=self._sticky)
        self._set_scrollbars()
        return self._body

    def _on_display(self):
        pass

    def _on_close(self, **kwargs):
        pass

    def _style(self, stylesheet, style):
        if not self._body:
            return
        if isinstance(stylesheet, str):
            self._body.option_readfile(stylesheet)
        elif isinstance(stylesheet, tuple):
            self._body.option_readfile(stylesheet[0], stylesheet[1])
        if style:
            for x in style:
                if len(x) == 2 or len(x) == 3:
                    self._body.option_add(*x)

    def _create_box(self, box, x=0, y=0, anchor="nw"):
        self._box = box
        self._box_id = self._canvas.create_window(x, y, window=self._box, anchor=anchor)
        self._box.bind("<Configure>", self._on_configure, "+")

    def _on_mouse_wheel(self, event):
        if not self._orient or not self._is_scrollable:
            return
        # scroll down   (value: 1)   ->  event.num = 5   or  event.delta < 0
        # scroll up     (value: -1)  ->  event.num = 4   or  event.delta >= 0
        scroll = 1 if event.num == 5 or event.delta < 0 else -1
        if self._orient in ("horizontal", "x", "h"):
            self._canvas.xview_scroll(scroll, "units")
        elif self._orient in ("both", "vertical", "y", "v"):
            if self._hsb_under_mouse:
                self._canvas.xview_scroll(scroll, "units")
            else:
                self._canvas.yview_scroll(scroll, "units")

    def _set_scrollbars(self):
        if self._orient in ("both", "horizontal", "h", "x"):
            self._hsb = tk.Scrollbar(self._body, orient="horizontal",
                                     command=self._canvas.xview, **self._hsb_options)
            self._hsb.grid(row=1, column=0, columnspan=2, sticky="we")
            self._canvas.config(xscrollcommand=self._hsb.set)
            self._bind_enter_leave_to_hsb()
        if self._orient in ("both", "vertical", "v", "y"):
            self._vsb = tk.Scrollbar(self._body, orient="vertical",
                                     command=self._canvas.yview, **self._vsb_options)
            self._vsb.grid(row=0, column=1, sticky="ns")
            self._canvas.config(yscrollcommand=self._vsb.set)

    def _bind_enter_leave_to_hsb(self):
        def enter_hsb(event):
            self._hsb_under_mouse = True
        def leave_hsb(event):
            self._hsb_under_mouse = False
        self._hsb.bind('<Enter>', enter_hsb, "+")
        self._hsb.bind('<Leave>', leave_hsb, "+")

    def _on_configure(self, event):
        if self._box:
            self._canvas.config(height=self._box.winfo_height())
            self._canvas.config(width=self._box.winfo_width())
            self._canvas.config(scrollregion=self._canvas.bbox("all"))

    def _on_enter_body(self, event):
        self._is_scrollable = True

    def _on_leave_body(self, event):
        self._is_scrollable = False

    def _on_unmap_body(self, event):
        self._is_scrollable = False

    def _on_destroy_body(self, event):
        self._is_scrollable = False

    def _unbind_funcs(self):
        if not self._bind_func_ids or len(self._bind_func_ids) != 3:
            return
        try:
            for i, val in enumerate(("<MouseWheel>", "<Button-4>", "<Button-5>")):
                self._body.unbind(val, self._bind_func_ids[i])
        except Exception as e:
            pass
        self._bind_func_ids = []

    def _center_box(self, axis="x"): # is this method still useful ??? TODO: delete it ?
        """ axis could be: 'x', 'y' or 'both' """
        if not self._box or (axis not in ("both", "x", "y")):
            return
        x = y = 0
        if axis in ("x", "both"):
            body_width = self._body.winfo_width()
            box_width = self._box.winfo_width()
            width_diff = body_width - box_width
            if width_diff > 0:
                x = width_diff // 2
        if axis in ("y", "both"):
            body_height = self._body.winfo_height()
            box_height = self._box.winfo_height()
            height_diff = body_height - box_height
            if height_diff > 0:
                y = height_diff // 2
        self.box_moveto(x, y)

    def __getattr__(self, item):
        return getattr(self._body, item)


if __name__ == "__main__":
    app = tk.Tk()
    scrollbox = Scrollbox(app)
    scrollbox.pack(expand=1, fill=tk.BOTH)
    tk.Button(scrollbox.box, text="Click").pack()
    app.mainloop()
