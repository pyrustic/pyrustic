import tkinter as tk
from pyrustic.abstract.viewable import Viewable


class Scrollbox(Viewable):
    """
    Scrollbox is the container to use when your layout to be able to scroll up or down, right or left.
    To use Scrollbox, you just need to instantiate it, then use its property 'box'
    to be your layout's parent.
    Example:
        import tkinter as tk
        from pyrustic.widget.scrollbox import Scrollbox
        root = tk.Tk()
        scrollbox = Scrollbox(root)
        scrollbox.body.pack()
        button = Button(scrollbox.box, text="Hello")
        button.pack()
        root.mainloop()
    """
    def __init__(self,
                 master=None,
                 orient="both",
                 options={}):
        """
        - master: widget's parent
        - orient: could be 'vertical' or 'v', or 'horizontal' or 'h', or 'both' or None
        - options: dictionary, these options will be used as arguments to the widget's constructors.
            The widgets are: body, canvas, box, hsb and vsb.
            Example: Assume that you want to set the label_message's background to black
            and the body's background to red:
                options = {"body": {"background": "red"},
                           "label_message": {"background": "black"}}
        """
        self._master = master
        self._orient = orient
        self._options = options
        self._body_options = None
        self._canvas_options = None
        self._box_options = None
        self._vsb_options = None
        self._hsb_options = None
        self._parse_options(options)
        self._body = None
        self._canvas = None
        self._box = None
        self._box_id = None
        self._vsb = None
        self._hsb = None
        self._hsb_under_mouse = False
        self._is_scrollable = False
        self._bind_func_ids = ()
        self._components = {}
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
    def box(self):
        return self._box

    @property
    def orient(self):
        return self._orient

    @property
    def options(self):
        return self._options

    @property
    def components(self):
        """
        Get the components used to build this scrollbox.
        This property returns a dict. The keys are:
            'body', 'canvas', 'box', 'hsb', and 'vsb'
        """
        return self._components

    # ==============================================
    #                 PUBLIC METHODS
    # ==============================================

    def xview_moveto(self, fraction):
        """
        Edit canvas's method 'xview_moveto'
        """
        if self._canvas:
            self._canvas.xview_moveto(fraction)

    def yview_moveto(self, fraction):
        """
        Edit canvas's method 'yview_moveto'
        """
        if self._canvas:
            self._canvas.yview_moveto(fraction)

    def box_moveto(self, x, y):
        """
        Move the box on the canvas
        """
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
        """
        Use this method to edit canvas's itemconfig options for the box.
        itemconfig options: anchor, state, height, width
        Warning: these options aren't the same as box's own constructor's arguments !
        """
        if self._box:
            self._canvas.itemconfig(self._box_id, **options)

    def clear(self):
        """
        Clear the Scrollbox. This method doesn't destruct this object but destroy box's children
        """
        if self._box:
            for x in self._box.winfo_children():
                x.destroy()

    # ==============================================
    #                 PRIVATE METHODS
    # ==============================================

    def _on_build(self):
        self._body = tk.Frame(self._master,
                              class_="Scrollbox",
                              cnf=self._body_options)
        self._components["body"] = self._body
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
        self._body.winfo_toplevel().bind("<Configure>", self._on_configure_box_canvas, "+")
        # canvas
        self._canvas = tk.Canvas(self._body,
                                 name="canvas",
                                 cnf=self._canvas_options)
        self._components["canvas"] = self._canvas
        self._canvas.grid(row=0, column=0, sticky="nswe")
        # box
        self._box = tk.Frame(self._canvas,
                             name="box",
                             cnf=self._box_options)
        self._components["box"] = self._box
        self._box_id = self._canvas.create_window(0, 0, window=self._box, anchor="nw")
        self._box.bind("<Configure>", self._on_configure_box_canvas, "+")
        # scrollbar
        self._set_scrollbars()

    def _on_display(self):
        if not self._master:
            self._master = self._body.master

    def _on_destroy(self):
        if self._body:
            self._unbind_funcs()

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
                                     name="hsb",
                                     command=self._canvas.xview,
                                     cnf=self._hsb_options)
            self._components["hsb"] = self._hsb
            self._hsb.grid(row=1, column=0, columnspan=2, sticky="we")
            self._canvas.config(xscrollcommand=self._hsb.set)
            self._bind_enter_leave_to_hsb()
        if self._orient in ("both", "vertical", "v", "y"):
            self._vsb = tk.Scrollbar(self._body, orient="vertical",
                                     name="vsb",
                                     command=self._canvas.yview,
                                     cnf=self._vsb_options)
            self._components["vsb"] = self._vsb
            self._vsb.grid(row=0, column=1, sticky="ns")
            self._canvas.config(yscrollcommand=self._vsb.set)

    def _bind_enter_leave_to_hsb(self):
        def enter_hsb(event):
            self._hsb_under_mouse = True
        def leave_hsb(event):
            self._hsb_under_mouse = False
        self._hsb.bind('<Enter>', enter_hsb, "+")
        self._hsb.bind('<Leave>', leave_hsb, "+")

    def _on_configure_box_canvas(self, event):
        if self._box:
            if self._orient in ("horizontal", "h", "x"):
                self._canvas.itemconfig(self._box_id, height=self._canvas.winfo_height())
            elif self._orient in ("vertical", "v", "y"):
                self._canvas.itemconfig(self._box_id, width=self._canvas.winfo_width())
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
                self._master.unbind(val, self._bind_func_ids[i])
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

    def _parse_options(self, options):
        self._body_options = options["body"] if "body" in options else {}
        self._canvas_options = options["canvas"] if "canvas" in options else {}
        self._box_options = options["box"] if "box" in options else {}
        self._vsb_options = options["vsb"] if "vsb" in options else {}
        self._hsb_options = options["hsb"] if "hsb" in options else {}


if __name__ == "__main__":
    def add_data_horizontally(frame):
        tk.Label(frame, text="Horizontally...", bg="pink").pack(side=tk.LEFT)

    def add_data_vertically(frame):
        tk.Label(frame, text="Vertically...",bg="violet",
                 anchor="w", justify=tk.LEFT).pack(side=tk.TOP,
                                                   expand=1,
                                                   fill=tk.X)

    root = tk.Tk()
    root.geometry("+0+0")
    # Scrollbox
    scrollbox = Scrollbox(root)
    # colors
    scrollbox.components["body"].config(bg="black")
    scrollbox.components["canvas"].config(bg="blue")
    scrollbox.components["box"].config(bg="yellow")
    # labels
    h_data_frame = tk.Frame(scrollbox.box)
    v_data_frame = tk.Frame(scrollbox.box)
    # button
    command = lambda frame=h_data_frame: add_data_horizontally(frame)
    h_button = tk.Button(root,
                         text="Add Data Horizontally",
                         command=command)
    command = lambda frame=v_data_frame: add_data_vertically(frame)
    v_button = tk.Button(root,
                         text="Add Data Vertically",
                         command=command)
    tk.Button(root, text="xview LEFT", command=lambda :scrollbox.xview_moveto(0)).pack()
    tk.Button(root, text="xview RIGHT", command=lambda :scrollbox.xview_moveto(1)).pack()
    tk.Button(root, text="yview UP", command=lambda :scrollbox.yview_moveto(0)).pack()
    tk.Button(root, text="yview DOWN", command=lambda :scrollbox.yview_moveto(1)).pack()
    # pack
    scrollbox.body.pack(fill=tk.BOTH, expand=1)
    h_data_frame.pack()
    v_data_frame.pack(expand=1, fill=tk.X)
    h_button.pack()
    v_button.pack()
    #
    root.mainloop()
