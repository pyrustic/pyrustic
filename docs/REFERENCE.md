# Pyrustic Framework Reference
- [pyrustic.app.App](#pyrusticappapp) 

- [pyrustic.com.Com](#pyrusticcomcom) 

- [pyrustic.dao.Dao](#pyrusticdaodao) 

- [pyrustic.exception.PyrusticAppException](#pyrusticexceptionpyrusticappexception) 

- [pyrustic.exception.PyrusticException](#pyrusticexceptionpyrusticexception) 

- [pyrustic.exception.PyrusticTableException](#pyrusticexceptionpyrustictableexception) 

- [pyrustic.exception.PyrusticWidgetException](#pyrusticexceptionpyrusticwidgetexception) 

- [pyrustic.gurl.Gurl](#pyrusticgurlgurl) 

- [pyrustic.gurl.Response](#pyrusticgurlresponse) 

- [pyrustic.jasonix.Jasonix](#pyrusticjasonixjasonix) 

- [pyrustic.manager.command](#pyrusticmanagercommand) 

- [pyrustic.theme.Theme](#pyrusticthemetheme) 

- [pyrustic.threadom.Threadom](#pyrusticthreadomthreadom) 

- [pyrustic.view.View](#pyrusticviewview) 

- [pyrustic.widget.choice.Choice](#pyrusticwidgetchoicechoice) 

- [pyrustic.widget.confirm.Confirm](#pyrusticwidgetconfirmconfirm) 

- [pyrustic.widget.scrollbox.Scrollbox](#pyrusticwidgetscrollboxscrollbox) 

- [pyrustic.widget.table.Table](#pyrusticwidgettabletable) 

- [pyrustic.widget.toast.Toast](#pyrusticwidgettoasttoast) 

- [pyrustic.widget.tree.Tree](#pyrusticwidgettreetree) 

<br>

## pyrustic.app.App


<details>
<summary>expand | collapse</summary>



<br>


### `App` 
Pyrustic Framework's entry point.
This class should be instantiated inside the file "main.py".

<br>


### `__init__` (self, package)
Create an App instance.
package: the name of the package in which the caller is. Use __package__.

It's recommended to don't write any code above this instantiation.
<br><br>

### `exit_hook` 
None
<br><br>

### `gui_config` 
Setter et Getter
Get a dict-like deepcopy of your config file if it exists and is valid.
Else you will get the default config dict.
<br><br>

### `root` 
Get the main tk root
<br><br>

### `theme` 
Get the theme object
For more information about what a theme is:
- check 'pyrustic.theme.Theme';
- then check the beautiful theme 'pyrustic.theme.cyberpunk'
<br><br>

### `view` 
Get the view object.
A view should implement "pyrustic.viewable.Viewable"
<br><br>

### `center` (self)
Center the window
<br><br>

### `exit` (self)
Exit, simply ;-)
Depending on your config file, the application will close quickly or not.
A quick exit will ignore the lifecycle of a Viewable (pyrustic.viewable).
In others words, '_on_destroy()' methods won't be called.
Exit quickly if you don't care clean-up but want the app to close as fast as possible.
<br><br>

### `maximize` (self)
Maximize the window
<br><br>

### `restart` (self)
Call this method to restart the app.
You would need to submit a new view first before calling this method.
<br><br>

### `start` (self)
Call this method to start the app.
It should be called once and put on the last line of the file.


</details>
<br><br>

## pyrustic.com.Com


<details>
<summary>expand | collapse</summary>



<br>


### `Com` 
The Event Notification Comprehension 

<br>


### `__init__` (self, tk=None, event_sep=None)
Initialize self.  See help(type(self)) for accurate signature.
<br><br>

### `event_sep` 
None
<br><br>

### `resources` 
None
<br><br>

### `subscribers` 
None
<br><br>

### `tk` 
None
<br><br>

### `pub` (self, event, data=None, sync=False)
None
<br><br>

### `req` (self, resource, res_args=None, res_kwargs=None, consumer=None, sync=False)
None
<br><br>

### `res` (self, name, handler)
None
<br><br>

### `sub` (self, event, consumer)
None
<br><br>

### `unres` (self, name)
None
<br><br>

### `unsub` (self, sid)
None


</details>
<br><br>

## pyrustic.dao.Dao


<details>
<summary>expand | collapse</summary>



<br>


### `Dao` 
It's recommended to use Dao by composition. Meaning: don't subclass it.
DAO: Data Access Object (this one is built to work with SQLite).
You give an SQL request with some params or not, it spills out the result nicely !
You can even get the list of tables or columns.

<br>


### `__init__` (self, path, creational_script=None, raise_exception=True, raise_warning=True, connection_kwargs=None)
- path: absolute path to database file

- creational_script: a path to a file, a file-like object or a string of sql code
    Example_a: "CREATE TABLE my_table(id INTEGER NOT NULL PRIMARY KEY);"
    Example_b: "/path/to/script.sql"

- raise_exception: By default, True, so exceptions (sqlite.Error) will be raised

- raise_warning: By default, True, so exceptions (sqlite.Warning) will be raised

- connection_kwargs: connections arguments used while calling the
 method "sqlite.connect()"
<br><br>

### `con` 
Connection object
<br><br>

### `creational_script` 
None
<br><br>

### `is_new` 
Returns True if the database has just been created, otherwise returns False
<br><br>

### `path` 
None
<br><br>

### `close` (self)
Well, it closes the connection
<br><br>

### `columns` (self, table)
Returns the list of columns names of the given table name
A column is like:
    (int_id, str_column_name, str_column_datatype, int_boolean_nullability,
    default_value, int_primary_key)
Example:
    [(0, "id", "INTEGER", 1, None, 1),
    (1, "name", "TEXT", 0, None, 0),
    (2, "age", "INTEGER", 1, None, 0)]

This method can raise sqlite.Error, sqlite.Warning
<br><br>

### `edit` (self, sql, param=None)
Use this method to edit your database.
Formally: Data Definition Language (DDL) and Data Manipulation Language (DML).
It returns True or False or raises sqlite.Error, sqlite.Warning
Example:
    edit( "SELECT * FROM table_x WHERE age=?", param=(15, ) )
<br><br>

### `export` (self)
export the database: it returns a string of sql code.
This method can raise sqlite.Error, sqlite.Warning
<br><br>

### `query` (self, sql, param=None)
Use this method to query your database.
Formally: Data Query Language (DQL)
It returns a tuple: (data, description).
        Data is a list with data from ur query.
        Description is a list with the name of columns related to data
    Example: ( [1, "Jack", 50], ["id", "name", "age"] )
    This method can raise sqlite.Error, sqlite.Warning
<br><br>

### `script` (self, script)
Executes the script as an sql-script. Meaning: there are multiple lines of sql.
This method returns nothing but could raise sqlite.Error, sqlite.Warning.

script could be a path to a file, a file-like object or just a string.
<br><br>

### `tables` (self)
Returns the list of tables names.
Example: ["table_1", "table_2"]
This method can raise sqlite.Error, sqlite.Warning
<br><br>

### `test` (self)
Returns True if this is a legal database, otherwise returns False


</details>
<br><br>

## pyrustic.exception.PyrusticAppException


<details>
<summary>expand | collapse</summary>



<br>


### `PyrusticAppException` 
Common base class for all non-exit exceptions.

<br>




</details>
<br><br>

## pyrustic.exception.PyrusticException


<details>
<summary>expand | collapse</summary>



<br>


### `PyrusticException` 
Common base class for all non-exit exceptions.

<br>




</details>
<br><br>

## pyrustic.exception.PyrusticTableException


<details>
<summary>expand | collapse</summary>



<br>


### `PyrusticTableException` 
Common base class for all non-exit exceptions.

<br>




</details>
<br><br>

## pyrustic.exception.PyrusticWidgetException


<details>
<summary>expand | collapse</summary>



<br>


### `PyrusticWidgetException` 
Common base class for all non-exit exceptions.

<br>




</details>
<br><br>

## pyrustic.gurl.Gurl


<details>
<summary>expand | collapse</summary>



<br>


### `Gurl` 
Gurl is a great suite for accessing the web!

<br>


### `__init__` (self, token=None, headers=None, web_cache=True, response_cache=True)
PARAMETERS:

- token: Authentication token

- headers: dict of headers. Example:
        { "Accept": "application/vnd.github.v3+json",
          "User-Agent": "Mozilla/5.0" )

- web_cache: bool, set it to True to activate the web cache

- response_cache: bool, set it to True to access cached responses
<br><br>

### `headers` 
None
<br><br>

### `token` 
None
<br><br>

### `web_cache` 
None
<br><br>

### `request` (self, url, body=None, method='GET', headers=None)
Returns a Response object 


</details>
<br><br>

## pyrustic.gurl.Response


<details>
<summary>expand | collapse</summary>



<br>


### `Response` 
None

<br>


### `__init__` (self, native=None, error=None, cached_response=None)
Initialize self.  See help(type(self)) for accurate signature.
<br><br>

### `body` 
None
<br><br>

### `cached_response` 
None
<br><br>

### `code` 
None
<br><br>

### `error` 
None
<br><br>

### `error_reason` 
None
<br><br>

### `headers` 
None
<br><br>

### `json` 
None
<br><br>

### `native` 
None
<br><br>

### `reason` 
None
<br><br>

### `status` 
None
<br><br>

### `url` 
None
<br><br>

### `header` (self, name, default=None)
None
<br><br>

### `show` (self, include_headers=False, include_body=False)
None


</details>
<br><br>

## pyrustic.jasonix.Jasonix


<details>
<summary>expand | collapse</summary>



<br>


### `Jasonix` 
Jasonix allows you to play with JSON files like toys ! (really)

<br>


### `__init__` (self, target, default=None, readonly=False)
PARAMETERS:

- target: file-like object or a path to a json file. If target is a path
 and this path doesn't exist, a new file will be created or not according
to the parameter "default

- default: file-like object or a path or a dict.

- readonly: bool
<br><br>

### `data` 
The dict-like representation of the JSON file
<br><br>

### `default` 
None
<br><br>

### `target` 
None
<br><br>

### `reload` (self)
Reload data from JSON file
<br><br>

### `save` (self)
"
Push data into the JSON file (not the default file !) if 'readonly' is False


</details>
<br><br>

## pyrustic.manager.command


<details>
<summary>expand | collapse</summary>



<br>


### `command` (line=None, target=None)
Param:
    - line is a string
    - target is a string

<br>



</details>
<br><br>

## pyrustic.theme.Theme


<details>
<summary>expand | collapse</summary>



<br>


### `Theme` 
A theme is a collection of styles and... others theme.

<br>


### `__init__` (self)
Initialize self.  See help(type(self)) for accurate signature.
<br><br>

### `styles` 
Get a list of styles that this theme contains
<br><br>

### `themes` 
Get a list of theme that this theme contains
<br><br>

### `add_style` (self, style, scope=None)
Add a style to this theme.
The style is an instance of 'pyrustic.default_style._Style'.
You don't have to directly subclass the private class '_Style'.
Instead, subclass one of the public classes in the module 'pyrustic.default_style'.
The scope here is an optional string.
When you don't set the scope, the style will be applied as it.
Example. If you add a Button style in your theme, this style will be
applied to all buttons widgets. But you can restrict this effect to a scope.
This scope could be by example "*Canvas*Button.", meaning all buttons
that are living on all Canvas, are candidates for the given style.
<br><br>

### `add_theme` (self, theme)
Add a theme to this... theme
<br><br>

### `target` (self, master)
Set this theme to master. Master here should be the root widget of your app.
You need to set the theme to master before installing others widgets on the master.


</details>
<br><br>

## pyrustic.threadom.Threadom


<details>
<summary>expand | collapse</summary>



<br>


### `Threadom` 
None

<br>


### `__init__` (self, tk, sync=False)
- tk: a tk.Tk instance or any tkinter object
- sync: boolean
<br><br>

### `consume` (self, queue, consumer=None, unpack_result=False, exception_handler=None, latency=10)
Loops through the queue, pick data, then run the callback 'consumer' with
data as argument.
Example, assume that there are these integers 3, 4 and 5 in the queue.
3 -> consumer(3); 4 -> consumer(4); 5 -> consumer(5)

- queue: the queue. See Threadom's method 'q'.
- consumer: the callback that accepts one argument or more than one if unpack_result is True
- unpack_result: if True, the result will be unpacked.
- exception_handler: callback that accepts one argument to handle any occurred exception.
- latency: integer. Milliseconds between each loop to consume the queue. By default: 10

Returns the 'qid'. You will need this 'qid' to stop, pause, resume the loop or to get info.
<br><br>

### `info` (self, qid=None)
Retrieve info from the process launched by the method 'consume'.
Returns a dict:
 {"queue": queue, "active": boolean, "consumer": callback, "unpack_result": boolean,
 "exception_handler": callback, "latency": integer}
<br><br>

### `pause` (self, qid)
Pause the process launched by the method 'consume'.
Put 0 to pause all processes
<br><br>

### `q` (self)
Creates a new Queue
<br><br>

### `resume` (self, qid)
Resume the process launched by the method 'consume'
Put 0 to resume all processes
<br><br>

### `run` (self, target, target_args=None, target_kwargs=None, consumer=None, sync=None, daemon=True, unpack_result=False, upstream_exception_handler=None, downstream_exception_handler=None)
Runs a target in background. Return False if the target is in WAITING state (sync)
- target: the callable to run
- target_args: tuple, arguments to use
- target_kwargs: dict, keyword-arguments to use
- consumer: the callback with parameter(s) that will consume the returned value by target
- sync: None or boolean to override the constructor's argument sync
- unpack_result: boolean, True, to unpack the result returned by target
- upstream_exception_handler: one parameter callback to handle the exception
    raised while running the target
- downstream_exception_handler: one parameter callback to handle the exception
    raised while calling the consumer
<br><br>

### `stop` (self, qid)
Stop the process launched by the method 'consume'.
Set 0 to stop them all.


</details>
<br><br>

## pyrustic.view.View


<details>
<summary>expand | collapse</summary>



<br>


### `View` 
Subclass this if you are going to create a view.

Lifecycle of a view:
    1- you instantiate the view
    2- '__init__()' is implicitly called
    3- you call the method '.build()'
    4- '_on_build()' is implicitly called
    5- '_on_display()' is implicitly called once the widget is visible
    6- '_on_destroy()' is implicitly called when the widget is destroyed/closed

The rules to create your view is simple:
- You need to subclass Viewable.
- You need to implement the methods '_on_build()', and optionally
    implement '_on_display()' and '_on_destroy()'.
- You need to set an instance variable '_body' with either a tk.Frame or tk.Toplevel
    in the method '_on_build()'
That's all ! Of course, when you are ready to use the view, just call the 'build()' method.
Calling the 'build()' method will return the body of the view. The one that you assigned
to the instance variable '_body'. The same body can be retrieved with the property 'body'.
The 'build()' method should be called once. Calling it more than once will still return
the body object, but the view won't be built again.
You can't re-build your same view instance after destroying its body.
You can destroy the body directly, by calling the conventional tkinter destruction method
 on the view's body. But it's recommended to destroy the view by calling the view's method
 'destroy()' inherited from the class Viewable.
The difference between these two ways of destruction is that when u call the Viewable's
 'destroy()' method, the method '_on_destroy()' will be called BEFORE the effective
 destruction of the body. If u call directly 'destroy' conventionally on the tkinter
 object (the body), the method '_on_destroy()' will be called AFTER the beginning
  of destruction of the body.

  By the way, you can use convenience methods "build_pack", "build_grid", "build_place"
  to build and pack/grid/place your widget in the master !!
  Use "build_wait" for toplevels if you want the app to wait till the window closes

<br>


### `__init__` (self)
Initialize self.  See help(type(self)) for accurate signature.
<br><br>

### `body` 
Get the body of this view.
<br><br>

### `state` 
Return the current state of the Viewable instance.
States are integers, you can use these constants:
    - viewable.NEW: the state just after instantiation;
    - viewable.BUILT: the state after the call of on_body
    - viewable.DISPLAYED: the state after the call of on_display
    - viewable.DESTROYED: the state after the call of on_destroy
<br><br>

### `build` (self)
Build the view. Return the body
<br><br>

### `build_grid` (self, cnf=None, **kwargs)
None
<br><br>

### `build_pack` (self, cnf=None, **kwargs)
None
<br><br>

### `build_place` (self, cnf=None, **kwargs)
None
<br><br>

### `build_wait` (self)
Build the view. Return the body
<br><br>

### `destroy` (self)
Destroy the body of this view


</details>
<br><br>

## pyrustic.widget.choice.Choice


<details>
<summary>expand | collapse</summary>



<br>


### `Choice` 
Choice is a dialog box to make the user select some items among others.
The Choice could be implemented with either radiobuttons or checkbuttons.

Example:

    import tkinter as tk
    from pyrustic.widget.choice import Choice

    def my_handler(result):
        print(result)

    root = tk.Tk()
    my_items = ("first", "second", "third")
    choice = Choice(root, title="Choice", header="Make a choice",
                    items=my_items, handler=my_handler)
    choice.build()
    root.mainloop()

<br>


### `__init__` (self, master=None, title=None, header=None, message=None, items=None, selected=None, flavor='radio', handler=None, geometry=None, options=None, extra_options=None)
PARAMETERS:

- master: widget parent. Example: an instance of tk.Frame

- title: title of dialog box

- header: the text to show as header

- message: the text to show as message

- use_scrollbox: bool, set it to True to make the Dialog scrollable

- items: a sequence of strings. Example: ("banana", "apple").

- selected: a sequence of indexes to indicate default selection.
Set it to None if u don't need it.

- flavor: it could be either RADIO or CHECK
for respectively radiobutton and checkbutton

- handler: a callback to be executed immediately
after closing the dialog box.
The callback should allow one parameter, the result:

    - If the flavor is RADIO,
     then, result is a tuple like: (the selected index, item string).

    - If the flavor is CHECK,
     then, result is a sequence of tuples.
     Each tuple is like: (integer, item string),
     with integer being 1 if the button has been clicked, else 0.

- geometry: str, as the dialog box is a toplevel (BODY),
 you can edit its geometry. Example: "500x300"

- options: dictionary of widgets options
    The widgets keys are: BODY, LABEL_HEADER, SCROLLBOX, LABEL_MESSAGE,
    FRAME_PANE, FRAME_FOOTER, BUTTON_CONTINUE, BUTTON_CANCEL,
    RADIOBUTTONS, CHECKBUTTONS.

    Example: Assume that you want to set the LABEL_MESSAGE's background to black
    and the BODY's background to red:
        options = { BODY: {"background": "red"},
                    LABEL_MESSAGE: {"background": "black"} }
<br><br>

### `components` 
Get the components (widgets instances) used to build this dialog.

This property returns a dict. The keys are:
    BODY, LABEL_HEADER, SCROLLBOX, LABEL_MESSAGE,
    FRAME_PANE, FRAME_FOOTER, BUTTON_CONTINUE, BUTTON_CANCEL,
    RADIOBUTTONS, CHECKBUTTONS.

Warning: radiobuttons and checkbuttons are sequences of widgets positioned
in the sequence according to the index.

Another Warning: check the presence of key before usage.
<br><br>

### `flavor` 
None
<br><br>

### `handler` 
None
<br><br>

### `header` 
None
<br><br>

### `items` 
None
<br><br>

### `message` 
None
<br><br>

### `selected` 
- If the flavor is RADIO,
     then, result is a tuple like: (the selected index, item string).
     Example: 3 items, the second has been selected:
        result = (1, "Item at index 1")

- If the flavor is CHECK,
 then, result is a sequence of tuples, each positioned in
 the sequence according to its index number.
 Each tuple is like: (integer, item string),
 with integer being 1 if the button has been clicked, else 0.
 Example: 3 items, only the last 2 are checked:
    result = ( (0, "item 1"), (1, "item 2"), (1, "item 3") )


</details>
<br><br>

## pyrustic.widget.confirm.Confirm


<details>
<summary>expand | collapse</summary>



<br>


### `Confirm` 
Confirm is a dialog box to ask the user to confirm an action.

Example:

    import tkinter as tk
    from pyrustic.widget.confirm import Confirm

    def my_handler(result):
        print(result)

    root = tk.Tk()
    confirm = Confirm(root, title="Confirm", header="Confirmation",
                    message="Do you really want to continue ?",
                    handler=my_handler)
    confirm.build()
    root.mainloop()

<br>


### `__init__` (self, master=None, title=None, header=None, message=None, handler=None, geometry=None, options=None, extra_options=None)
PARAMETERS:

- master: widget parent. Example: an instance of tk.Frame

- title: title of dialog box

- header: the text to show as header

- message: the text to show as message

- handler: a callback to be executed immediately after closing the dialog box.
    This callback should accept a boolean positional argument.
    True means Ok, confirmed.

- geometry: str, as the dialog box is a toplevel (BODY),
 you can edit its geometry. Example: "500x300"

- options: dictionary of widgets options
    The widgets keys are: BODY, LABEL_HEADER,
     LABEL_MESSAGE, FRAME_FOOTER, BUTTON_CANCEL, BUTTON_CONFIRM.

    Example: Assume that you want to set the LABEL_MESSAGE's background to black
    and the BODY's background to red:
        options = { BODY: {"background": "red"},
                    LABEL_MESSAGE: {"background": "black"} }
<br><br>

### `components` 
Get the components (widgets instances) used to build this dialog.

This property returns a dict. The keys are:
    BODY, LABEL_HEADER,
    LABEL_MESSAGE, FRAME_FOOTER, BUTTON_CANCEL, BUTTON_CONFIRM

Warning: check the presence of key before usage
<br><br>

### `handler` 
None
<br><br>

### `header` 
None
<br><br>

### `message` 
None
<br><br>

### `ok` 
Returns True if user confirmed, else get False


</details>
<br><br>

## pyrustic.widget.scrollbox.Scrollbox


<details>
<summary>expand | collapse</summary>



<br>


### `Scrollbox` 
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

<br>


### `__init__` (self, master=None, orient='vertical', box_sticky='nswe', resizable_box=True, options=None, extra_options=None)
- master: widget parent. Example: an instance of tk.Frame

- orient: could be one of: VERTICAL, HORIZONTAL, BOTH

- options: dictionary of widgets options
    The widgets keys are: BODY, CANVAS, BOX, HSB, VSB
    Example: Assume that you want to set the CANVAS background to red
        options = {CANVAS: {"background": "red"}}
<br><br>

### `box` 
None
<br><br>

### `components` 
Get the components (widgets instances) used to build this scrollbox.

This property returns a dict. The keys are:
    BODY, CANVAS, BOX, HSB, VSB

Warning: check the presence of key before usage. Example,
the widget linked to the HSB key may be missing because
only VSB is used
<br><br>

### `orient` 
None
<br><br>

### `box_config` (self, **options)
As the BOX is an item compared to CANVAS, some
the options concerning the BOX can be edited only via
CANVAS "itemconfig" method.
Use this method to edit these options.
itemconfig options are: anchor, state, height, width.

Warning: these options are not the same as the arguments
 of BOX's own constructor !
<br><br>

### `clear` (self)
Clears the Scrollbox.
This method doesn't destruct this object but BOX's children
<br><br>

### `xview_moveto` (self, fraction)
Calls canvas's method 'xview_moveto'
Set:
    - 0: to scroll to left
    - 1: to scroll to right
<br><br>

### `yview_moveto` (self, fraction)
Calls canvas's method 'yview_moveto'
Set:
    - 0: to scroll to top
    - 1: to scroll to bottom


</details>
<br><br>

## pyrustic.widget.table.Table


<details>
<summary>expand | collapse</summary>



<br>


### `Table` 
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

<br>


### `__init__` (self, master=None, titles=None, data=None, hidden_columns=None, sorting=True, mask=None, select_mode='browse', layout='equally', orient='both', options=None, extra_options=None)
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
<br><br>

### `components` 
Get the components (widgets instances) used to build this dialog.

This property returns a dict. The keys are:
    BODY, VSB, HSB, CANVAS, FRAME_BACKGROUND,
    FRAMES_HEADERS, LISTBOXES_COLUMNS, LABELS_SORTING and LABELS_TITLES
Warning: FRAMES_HEADERS, LABELS_TITLES, LABELS_SORTING
 and LISTBOXES_COLUMNS are sequences of widgets by index
<br><br>

### `data` 
None
<br><br>

### `hidden_columns` 
None
<br><br>

### `layout` 
None
<br><br>

### `mask` 
None
<br><br>

### `orient` 
None
<br><br>

### `select_mode` 
None
<br><br>

### `selection` 
Return a sequence of the current selection.
selection = ( item_1, item_2, ...)
item_i = {"index": int, "data": data}
data = a sequence of string representing the row at the index.
<br><br>

### `table_size` 
returns the length of columns and rows: (rows, cols)
Example:
    Assume that the table has 3 columns and 10 rows,
    this property will return (10, 3)
<br><br>

### `titles` 
None
<br><br>

### `cget_column` (self, index=None, option='background')
If index is None, returns a sequence of options of listboxes (columns).
Else returns the options of the column at the given index
<br><br>

### `clear` (self)
Clear the table
<br><br>

### `config_column` (self, index=None, **options)
Configure column. If index is None, all columns will be configured
<br><br>

### `delete` (self, index_start, index_end=None)
Deletes lines (rows) from the table
<br><br>

### `fill` (self, titles=None, data=None)
This will overwrite the titles and/or data with the new given titles or data
<br><br>

### `get` (self, index_start, index_end=None)
Returns a line if you don't give a 'index_end'.
Returns a sequence of lines if you give a 'index_end'.
<br><br>

### `handle_row_event` (self, sequence, handler)
This callback will be called at a specific row event (sequence = string):
    handler(table, row_data, row_index, column_index)
<br><br>

### `handle_row_selected` (self, handler)
This callback will be called at the event 'row selection':
    handler(table, row_data, row_index, column_index)
<br><br>

### `insert` (self, index, data)
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
<br><br>

### `see` (self, index='end')
The table will scroll to the given index


</details>
<br><br>

## pyrustic.widget.toast.Toast


<details>
<summary>expand | collapse</summary>



<br>


### `Toast` 
A toast is a dialog box with or without decoration
that is displayed for a given duration.

Any "click" action on the Toast's body will close it.

Example:
    import tkinter as tk
    from pyrustic.widget.toast import Toast

    root = tk.Tk()
    toast = Toast(root, header="My Header", message="My Message")
    toast.build()
    root.mainloop()

<br>


### `__init__` (self, master=None, title=None, header=None, message=None, duration=1234, decoration=False, geometry=None, options=None, extra_options=None)
PARAMETERS:

- master: widget parent. Example: an instance of tk.Frame

- title: title of dialog box

- header: the text to show as header

- message: the text to show as message

- duration: int, in milliseconds.
    You can set None to duration to cancel the self-destroying timer

- decoration: True or False to allow Window decoration

- geometry: str, as the dialog box is a toplevel (BODY),
 you can edit its geometry. Example: "500x300"

- options: dictionary of widgets options
    The widgets keys are: BODY, LABEL_HEADER, LABEL_MESSAGE.

    Example: Assume that you want to set the LABEL_MESSAGE's background to black
    and the BODY's background to red:
        options = { BODY: {"background": "red"},
                    LABEL_MESSAGE: {"background": "black"} }
<br><br>

### `components` 
Get the components (widgets instances) used to build this Toast.

This property returns a dict. The keys are:
    BODY, LABEL_HEADER, LABEL_MESSAGE,
<br><br>

### `decoration` 
None
<br><br>

### `duration` 
None
<br><br>

### `header` 
None
<br><br>

### `message` 
None


</details>
<br><br>

## pyrustic.widget.tree.Tree


<details>
<summary>expand | collapse</summary>



<br>


### `Tree` 
Tree is the megawidget to use to display the data as a tree.
To use Tree, you need to subclass it.

pyrustic.tree.SimpleTree is a nice example to study.

Scroll to the bottom of this file at the top-level script
environment to see the usage of SimpleTree

<br>


### `__init__` (self, master=None, indent=50, spacing=10, options=None, extra_options=None)
PARAMETERS:

- master: widget parent. Example: an instance of tk.Frame

- indent: left indent

- spacing: space between two nodes

- options: dictionary of widgets options
    The widgets keys are: BODY, NODE_FRAME, HEADER_FRAME, and BOX_FRAME.
    Example: Assume that you want to set the NODE_FRAME's background to black
    and the BODY's background to red:
        options = {BODY: {"background": "red"},
                   NODE_FRAME: {"background": "black"}}
<br><br>

### `hook` 
None
<br><br>

### `indent` 
None
<br><br>

### `nodes` 
Returns sequence of nodes. Check the method 'node()' to
see how an individual node data structure looks like.
<br><br>

### `root` 
None
<br><br>

### `spacing` 
None
<br><br>

### `attach` (self, node_id)
Attaches (again) a detached node. Returns True if it worked, else False
<br><br>

### `clear` (self, node_id)
Deletes the descendants of this node. Returns True if all right, else False.
<br><br>

### `collapse` (self, node_id)
Collapses this node. Returns True if it worked, else returns False
<br><br>

### `collexp` (self, node_id)
Useful method to toggle the state collapsed/expanded of the node
<br><br>

### `delete` (self, node_id)
Deletes this node.
Returns True or False
<br><br>

### `descendants` (self, node_id)
List of descendants nodes.
[ node, node, ...]

Please check the doc of the method "node()" to learn more about
the structure of a node object (a dict in fact)
<br><br>

### `detach` (self, node_id)
Detaches an attached node. Returns True if it worked, else False.
The detached node won't be visible anymore.
The detached node's descendants won't be visible anymore.
<br><br>

### `expand` (self, node_id)
Expands this node. Returns True if it worked, else returns False
<br><br>

### `expanded` (self, node_id)
Returns True if this node is actually expanded, else returns False
<br><br>

### `feed` (self, node_id, *args, **kwargs)
This method will call "_on_feed(*args, **kwargs").
Use it to feed some data to the tree
<br><br>

### `ghost` (self, node_id)
Hide the header frame of the node whose node_id is given.
Note that the descendants nodes will still be visible.
Use this method to give illusion that descendants nodes
don't have a root at all (kind of floating without root).
This method returns a boolean (True to indicate that all right, else False)
<br><br>

### `insert` (self, parent=None, title='', index='end', data=None, container=True, expand=False)
Insert a node.
- parent: the node_id of the parent or None if this is the root node of the tree
- title: string
- index: an integer to indicate where to put the node between
 its parent's descendants.
    Put "end" to indicate that this node should be added at the the end
- data: None or dictionary to contain whatever data you want. It could help later.
- container: boolean. True, if the node should contain another node. False else.
- expand: boolean, True if this node should be expanded from creation. False else.
Returns:
    None if failed to insert the node, else returns the newly created node_id
<br><br>

### `move` (self, node_id, parent_id=None, index=0)
Moves a node to another index. Returns True if all right, else False.
<br><br>

### `node` (self, id_or_path)
Returns a node by its node_id or its dotted path.
A node is a dictionary of data:
node = {"parent": int, "node_id": int, "container": bool,
        "index": int, "expanded": bool, "data": dict, "title": str,
        "frame_node": tk.Frame, "frame_header": tk.Frame,
        "frame_box": tk.Frame, "attached": bool, "ghosted": bool}
Example of dotted path (each number in the path is a position index):
    Hub
        Africa
        America
        Asia
            China
    china node = "0.2.0"
<br><br>

### `tag` (self, node_id, data=None)
Edits this node's data. Data should be None or a dict
Returns the data
<br><br>

### `title` (self, node_id, title=None)
Use this method to display or edit the title of a node.
Returns this node's title if you don't set a title as argument
<br><br>

### `unghost` (self, node_id)
Reveals the header frame of the node whose node_id is given.
This method returns a boolean (True to indicate that all right, else False)
<br><br>

### `untag` (self, node_id, data=None)
Edits this node's data. Data should be a sequence of keys.
Returns the data
<br><br>

### `walk` (self, node_id)
Walks throughout the node.
Example:
    for node_id, descendants in tree.walk(2):
        print(node_id, len(descendants))


</details>