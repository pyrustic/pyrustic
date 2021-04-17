import tkinter as tk
from pyrustic import widget
from pyrustic.tkmisc import merge_cnfs
from pyrustic.view import View


# Components
CANVAS = "canvas"
BOX = "box"
HSB = "hsb"
VSB = "vsb"

# Orient
BOTH = "both"
VERTICAL = "vertical"
HORIZONTAL = "horizontal"


class Scrollbox(widget.Frame):
    """
    Scrollbox is a scrollable surface. You just need to use its property "box" as
    your layout's parent.

    Example:

        import tkinter as tk
        from pyrustic.widget.scrollbox import Scrollbox

        root = tk.Tk()
        scrollbox = Scrollbox(root)
        scrollbox.build_pack()
        # Pack 50 Label on the box
        for i in range(50):
            label = tk.Label(scrollbox.box, text="Label {}".format(i))
            label.pack(anchor=tk.W)
        root.mainloop()

    """
    def __init__(self,
                 master=None,
                 orient=VERTICAL,
                 box_sticky="nswe",
                 resizable_box=True,
                 cnfs=None):
        """
        - master: widget parent. Example: an instance of tk.Frame

        - orient: could be one of: VERTICAL, HORIZONTAL, BOTH

        - options: dictionary of widgets options
            The widgets keys are: BODY, CANVAS, BOX, HSB, VSB
            Example: Assume that you want to set the CANVAS background to red
                options = {CANVAS: {"background": "red"}}
        """
        self.__cnfs = merge_cnfs(None, cnfs,
                                 components=("body", CANVAS, BOX, HSB, VSB))
        super().__init__(master=master,
                         class_="Scrollbox",
                         cnf=self.__cnfs["body"],
                         on_build=self.__on_build,
                         on_display=self.__on_display,
                         on_destroy=self.__on_destroy)
        self.__orient = orient
        self.__box_sticky = box_sticky
        self.__resizable_box = resizable_box
        self.__canvas_options = None
        self.__canvas = None
        self.__box = None
        self.__box_id = None
        self.__vsb = None
        self.__hsb = None
        self.__hsb_under_mouse = False
        self.__is_scrollable = False
        self.__components = {}
        # build
        self.__view = self.build()
    # ==============================================
    #                   PROPERTIES
    # ==============================================


    @property
    def box(self):
        return self.__box

    @property
    def orient(self):
        return self.__orient

    @property
    def components(self):
        """
        Get the components (widgets instances) used to build this scrollbox.

        This property returns a dict. The keys are:
            BODY, CANVAS, BOX, HSB, VSB

        Warning: check the presence of key before usage. Example,
        the widget linked to the HSB key may be missing because
        only VSB is used
        """
        return self.__components

    # ==============================================
    #                 PUBLIC METHODS
    # ==============================================

    def xview_moveto(self, fraction):
        """
        Calls canvas's method 'xview_moveto'
        Set:
            - 0: to scroll to left
            - 1: to scroll to right
        """
        if self.__canvas:
            self.update_idletasks()
            self.__canvas.xview_moveto(fraction)

    def yview_moveto(self, fraction):
        """
        Calls canvas's method 'yview_moveto'
        Set:
            - 0: to scroll to top
            - 1: to scroll to bottom
        """
        if self.__canvas:
            self.update_idletasks()
            self.__canvas.yview_moveto(fraction)

    def box_config(self, **options):
        """
        As the BOX is an item compared to CANVAS, some
        the options concerning the BOX can be edited only via
        CANVAS "itemconfig" method.
        Use this method to edit these options.
        itemconfig options are: anchor, state, height, width.

        Warning: these options are not the same as the arguments
         of BOX's own constructor !
        """
        if self.__box:
            self.__canvas.itemconfig(self.__box_id, cnf=options)

    def clear(self):
        """
        Clears the Scrollbox.
        This method doesn't destruct this object but BOX's children
        """
        if self.__box:
            for x in self.__box.winfo_children():
                x.destroy()


    # ==============================================
    #                 PRIVATE METHODS
    # ==============================================

    def __on_build(self):
        self.bind("<Enter>", self.__on_enter_body, "+")
        self.bind("<Leave>", self.__on_leave_body, "+")
        self.bind("<Unmap>", self.__on_unmap_body, "+")
        self.bind("<Destroy>", self.__on_destroy_body, "+")
        self.bind_all("<MouseWheel>", self.__on_mouse_wheel, "+")
        self.bind_all("<Button-4>", self.__on_mouse_wheel, "+")
        self.bind_all("<Button-5>", self.__on_mouse_wheel, "+")
        self.columnconfigure(0, weight=1, uniform=1)
        self.rowconfigure(0, weight=1, uniform=1)
        self.winfo_toplevel().bind("<Configure>",
                                   self.__on_configure_box_canvas, "+")
        # canvas
        self.__canvas = tk.Canvas(self,
                                  name=CANVAS,
                                  width=0,
                                  height=0,
                                  cnf=self.__cnfs[CANVAS])
        self.__components[CANVAS] = self.__canvas
        self.__canvas.grid(row=0, column=0, sticky=self.__box_sticky)
        # box
        self.__box = tk.Frame(self.__canvas,
                              name=BOX,
                              cnf=self.__cnfs[BOX])
        self.__components[BOX] = self.__box
        self.__box_id = self.__canvas.create_window(0, 0, window=self.__box, anchor="nw")
        self.__box.bind("<Configure>", self.__on_configure_box_canvas, "+")
        # scrollbar
        self.__set_scrollbars()

    def __on_display(self):
        pass

    def __on_destroy(self):
        self.__unbind_funcs()

    def __on_mouse_wheel(self, event):
        if not self.__orient or not self.__is_scrollable:
            return
        # scroll down   (value: 1)   ->  event.num = 5   or  event.delta < 0
        # scroll up     (value: -1)  ->  event.num = 4   or  event.delta >= 0
        scroll = 1 if event.num == 5 or event.delta < 0 else -1
        if self.__orient in ("horizontal", "x", "h"):
            self.__canvas.xview_scroll(scroll, "units")
        elif self.__orient in ("both", "vertical", "y", "v"):
            if self.__hsb_under_mouse:
                self.__canvas.xview_scroll(scroll, "units")
            else:
                self.__canvas.yview_scroll(scroll, "units")

    def __set_scrollbars(self):
        if self.__orient in ("both", "horizontal", "h", "x"):
            self.__hsb = tk.Scrollbar(self, orient="horizontal",
                                      name=HSB,
                                      command=self.__canvas.xview,
                                      cnf=self.__cnfs[HSB])
            self.__components[HSB] = self.__hsb
            self.__hsb.grid(row=1, column=0, columnspan=2, sticky="swe")
            self.__canvas.config(xscrollcommand=self.__hsb.set)
            self.__bind_enter_leave_to_hsb()
        if self.__orient in ("both", "vertical", "v", "y"):
            self.__vsb = tk.Scrollbar(self, orient="vertical",
                                      name=VSB,
                                      command=self.__canvas.yview,
                                      cnf=self.__cnfs[VSB])
            self.__components[VSB] = self.__vsb
            self.__vsb.grid(row=0, column=1, sticky=self.__box_sticky)
            self.__canvas.config(yscrollcommand=self.__vsb.set)

    def __bind_enter_leave_to_hsb(self):
        def enter_hsb(event):
            self.__hsb_under_mouse = True
        def leave_hsb(event):
            self.__hsb_under_mouse = False
        self.__hsb.bind('<Enter>', enter_hsb, "+")
        self.__hsb.bind('<Leave>', leave_hsb, "+")

    def __on_configure_box_canvas(self, event):
        if self.__box.winfo_exists():
            if self.__orient in ("horizontal", "h", "x"):
                if self.__resizable_box:
                    self.__canvas.itemconfig(self.__box_id,
                                             height=self.__canvas.winfo_height())
                else:
                    self.__canvas.config(height=self.__box.winfo_height())
            elif self.__orient in ("vertical", "v", "y"):
                if self.__resizable_box:
                    self.__canvas.itemconfig(self.__box_id,
                                             width=self.__canvas.winfo_width())
                else:
                    self.__canvas.config(width=self.__box.winfo_width())
            self.__canvas.config(scrollregion=self.__canvas.bbox("all"))

    def __on_enter_body(self, event):
        self.__is_scrollable = True

    def __on_leave_body(self, event):
        self.__is_scrollable = False

    def __on_unmap_body(self, event):
        self.__is_scrollable = False

    def __on_destroy_body(self, event):
        self.__is_scrollable = False

    def __unbind_funcs(self):
        try:
            for val in ("<Enter>", "<Leave>",
                        "<Unmap>", "<Destroy>",
                        "<MouseWheel>", "<Button-4>",
                        "<Button-5>", "<Configure>"):
                self.unbind(val)
        except Exception as e:
            pass


class _ScrollboxTest(View):

    def __init__(self, root):
        super().__init__()
        self._root = root
        self._body = None

    def _on_build(self):
        self._body = tk.Frame(self._root)
        # Pane 1
        pane_1 = tk.Frame(self._root)
        pane_1.pack(side=tk.LEFT, padx=10,
                    pady=10, expand=1, fill=tk.BOTH)
        # Scrollbox 1
        scrollbox_1 = Scrollbox(pane_1, orient=VERTICAL)
        scrollbox_1.pack(pady=5, expand=1, fill=tk.BOTH)
        # Button 1
        command = (lambda self=self, box=scrollbox_1.box, side=tk.TOP:
                   self._on_click_add(box, side))
        button_1 = tk.Button(pane_1, text="Add",
                             command=command)
        button_1.pack(side=tk.BOTTOM)
        # Pane 2
        pane_2 = tk.Frame(self._root)
        pane_2.pack(side=tk.LEFT, padx=10,
                    pady=10, expand=1, fill=tk.BOTH)
        # Scrollbox 2
        scrollbox_2 = Scrollbox(pane_2, orient=HORIZONTAL)
        scrollbox_2.pack(pady=5, expand=1, fill=tk.BOTH)
        # Button 2
        command = (lambda self=self, box=scrollbox_2.box, side=tk.LEFT:
                   self._on_click_add(box, side))
        button_2 = tk.Button(pane_2, text="Add",
                             command=command)
        button_2.pack(side=tk.BOTTOM)

    def _on_display(self):
        pass

    def _on_destroy(self):
        pass

    def _on_click_add(self, frame, side=tk.TOP):
        label = tk.Label(frame, text="Hello Friend")
        label.pack(side=side)


if __name__ == "__main__":
    root = tk.Tk()
    scrollbox_test = _ScrollboxTest(root)
    scrollbox_test.build_pack(fill=tk.BOTH, expand=1)
    root.mainloop()
