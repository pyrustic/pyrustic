Welcome to the second part of the [tutorial](https://github.com/pyrustic/pyrustic/blob/master/docs/tutorial/README.md). It is the continuation of the previous [first part](https://github.com/pyrustic/pyrustic/blob/master/docs/tutorial/tutorial-1.md).

In this second part of the tutorial, we will discuss how to create an application to generate primes with the [Pyrustic Framework](https://github.com/pyrustic/pyrustic#readme). The graphical interface of the application will be similar to the one in the first part of the tutorial.


<!-- Image -->
<div align="center">
    <img src="https://raw.githubusercontent.com/pyrustic/misc/master/media/primes.gif" alt="Figure 1" width="650">
    <p align="center">
    <b> Figure 1 - Primes </b>
    </p>
</div>

`Primes` displays the list of all primes inferior or equal to the number entered by the user.



## Table Of Contents
- [Get Pyrustic](#get-pyrustic)
- [Project Creation](#project-creation)
- [Project Structure](#project-structure)
- [The Concept Of View](#the-concept-of-view)
- [Implementation](#implementation)
- [Distribute Your App With Hubstore](#distribute-your-your-app-with-hubstore)  
- [Going Further](#going-further)


## Get Pyrustic
### What is Pyrustic
Pyrustic is a lightweight framework to develop, package, and publish `Python` desktop applications. Learn more about [Pyrustic](https://github.com/pyrustic/pyrustic#readme) !

### Install Pyrustic
`Pyrustic` is available on [PyPI](https://pypi.org/) (the Python Package Index). If you have never installed a package from PyPI, you must install the `pip` tool enabling you to download and install a PyPI package. There are several methods which are described on this [page](https://pip.pypa.io/en/latest/installing/).

```bash
$ pip install pyrustic
```

To upgrade `Pyrustic`:

```bash
$ pip install pyrustic --upgrade --upgrade-strategy eager
```

Now that you have Pyrustic installed on your computer, let's move on to creating the `primes` project.


## Project Creation
Create the project folder. Name it `primes`. Type `pyrustic` on the command-line to start [Pyrustic Manager](https://github.com/pyrustic/pyrustic#the-manager).

```bash
$ pyrustic

Welcome to Pyrustic Manager !
Version: 0.1.0
Type "help" or "?" to list commands. Type "exit" to leave.

(pyrustic) 
```

Link the project to `Pyrustic Manager` by indicating the path of the project folder. This could be a relative path or even a dot to indicate the current working directory.

```bash
(pyrustic) link /path/to/primes

Successfully linked !
[primes] /path/to/primes
Not yet initialized project (check 'help init')
```

From now on, the project linked to `Pyrustic Manager` will be called the `Target`. You can issue the `target` command to see the currently linked project.

```bash
(pyrustic) target

[primes] /path/to/primes
Not yet initialized project (check 'help init')
```

Now you can initialize your project with the command `init`. Initializing the project will simply create a basic project structure.

```bash
(pyrustic) init

Successfully initialized !
```

If you quit Pyrustic Manager, the next time you want to link the same project, run the `relink` command or use the `recent` command.

## Project Structure
If you issue the command `init`, `Pyrustic Manager` will generate files and directories to create a base project following the conventional Python project structure as described in the [Python Packaging User Guide](https://packaging.python.org/tutorials/packaging-projects/).

This is what your project structure will look like:

```bash
primes/  # the folder you created yourself ($PROJECT_DIR) [1]
    primes/  # this is the app package ($APP_PKG) [2]
        pyrustic_data/  # Pyrustic stores config here
            gui.json  # config file for the GUI [3]
            hubstore.json  # config file for Hubstore [4]
        view/  # the View package
            __init__.py
            main_view.py  # the main view module [5]
        __init__.py
        __main__.py  # the mighty entry point of your app ! [6]
        version.py  # unique location to define the version of the app [7]
    tests/
        __init__.py
    LICENSE  # empty license file, please don't forget to fill it
    MANIFEST.in  # already filled with convenient lines of rules [8]
    pyproject.toml  # the new unified Python project settings file [9]
    README.md  # default nice README (there are even an image inside) [10]
    setup.cfg  # define here your name, email, dependencies, and more [11]
    setup.py  # it is not a redundancy, don't remove it, don't edit it [12]
```

- `[1]` This is the project directory ($PROJECT_DIR), also knows as the `target`.
- `[2]` Your codebase lives in the app package ($APP_PKG).
- `[3]` Define here some GUI config.
- `[4]` Define here Hubstore config. Example: the cover picture of your app.
- `[5]` This module contains code to display the graphical equivalent of a 'hello world'.
- `[6]` Here, you set the theme, the main view. This is the entry point of your app.
- `[7]` By default, `__version__ =  "0.0.1"` is defined inside this module.
- `[8]` This file contains rule lines so that resources files are not excluded from $APP_PKG.
- `[9]` Read [What the heck is pyproject.toml ?](https://snarky.ca/what-the-heck-is-pyproject-toml/) and the [PEP 518](https://www.python.org/dev/peps/pep-0518/).
- `[10]` The default README looks like [this](https://github.com/pyrustic/demo#readme).
- `[11]` Read this [user guide](https://setuptools.readthedocs.io/en/latest/userguide/declarative_config.html) to edit the `setup.cfg` file.
- `[12]` If you want editable installs you still need a `setup.py` [shim](https://twitter.com/pganssle/status/1241161328137515008).

In order to avoid confusion, let's agree on the following points:
- `primes.view.main_view` is the dotted name of the `main_view.py` module present in the `view` package located in the `$APP_PKG`.
- `$APP_PKG.view.main_view` is the equivalent of `primes.view.main_view`.
- The `setup.cfg` file can be represented as `$PROJECT_DIR/setup.cfg` or `/path/to/setup.cfg` but never as `primes/setup.cfg` !
- `$APP_DIR` exists. See the next point.
- `$APP_DIR` and `$APP_PKG` represent the same directory. The nuance is that it is more elegant to write `$APP_DIR/misc/data.json` than `$APP_PKG/misc/data.json`.
- `$PROJECT_PKG` does not exist. Only `$PROJECT_DIR` exists.

## The Concept Of View
In the previous section, we created a basic project structure using the Pyrustic Manager `init` command. This basic project is executable. To prove it, enter the command `run` in Pyrustic Manager.

Pyrustic Manager will launch a graphical equivalent of "Hello World".

Under the hood, the `run` command executes the `$APP_PKG.__main__` module.

Here is the content of the `$ APP_PKG.__main__` module:

```python
from pyrustic.app import App
from tk_cyberpunk_theme.main import Cyberpunk
from primes.view.main_view import MainView


def main():
    # The App
    app = App(__package__)
    # Set theme
    app.theme = Cyberpunk()
    # Set view
    app.view = MainView(app)
    # Center the window
    app.center()
    # Lift off !
    app.start()


if __name__ == "__main__":
    main()
```

A `pyrustic.app.App` object is created in the `$APP_PKG.__main__` module. The cyberpunk theme and the `main_view` are passed to this object.

Here is the content of the `$APP_PKG.view.main_view` module which represents the main view:

```python
# a "view" module generated by Pyrustic Manager
import tkinter as tk
from pyrustic.view import View
from pyrustic.widget.toast import Toast


class MainView(View):

    def __init__(self, app):
        super().__init__()
        self._app = app
        self._root = app.root
        self._body = None
        self._btn_max = None

    def _on_build(self):
        self._body = tk.Frame(self._root)
        self._root.geometry("500x300")
        # Label
        label = tk.Label(self._body, text="Hello Friend !")
        label.pack(expand=1, fill=tk.BOTH)
        # Footer
        footer = tk.Frame(self._body)
        footer.pack(side=tk.BOTTOM, fill=tk.X)
        # Button Leave
        btn_leave = tk.Button(footer, text="Leave",
                              command=self._on_click_btn_leave)
        btn_leave.pack(side=tk.RIGHT, padx=2, pady=2)
        # Button Maximize
        self._btn_max = tk.Button(footer, text="Maximize",
                                  command=self._on_click_btn_max)
        self._btn_max.pack(side=tk.RIGHT, pady=2)

    def _on_display(self):
        pass

    def _on_destroy(self):
        pass

    def _on_click_btn_max(self):
        self._app.maximize()
        self._btn_max.destroy()

    def _on_click_btn_leave(self):
        toast = Toast(self._body, message="Goodbye Friend !")
        toast.wait_window()
        self._app.exit()
```

A `View` brings the concept of `View Lifecycle` to your GUI. This means that the view will go through formally defined states giving you the ability to define the actions to be performed for each state such as hooking.
A view is an object that has a `body` that represents a tkinter widget. To create a view, subclass `pyrustic.view.View` and implement the`_on_build()` method. In the `_on_build()` method, set the value of the `_body` instance variable. The view has other methods that we can optionally implement.

Here are the attributes of View:
- `_body`: private attribute, contains the tkinter widget object defined in `_on_build()`.
- `body`: public getter property, returns `_body`.
- `state`: public getter property, one of the states _"new"_, _"built"_, _"displayed"_ and _"destroyed"_.
- `build()`: public method, call it to execute the `_on_build()` method, returns the `body`.
- `build_pack(*args, **kwargs)`: same as execute `build()` then execute tkinter's `pack(*args, **kwargs)`.
- `build_grid(*args, **kwargs)`: same as execute `build()` then execute tkinter's `pack(*args, **kwargs)`.
- `build_place(*args, **kwargs)`: same as execute `build()` then execute tkinter's `pack(*args, **kwargs)`.
- `build_wait(*args, **kwargs)`: same as execute `build()` then execute the tkinter's `wait_window()`. Use it if your view's `body` is a toplevel widget and you want to have a flow-blocking dialog.
- `destroy()`: elegantly destroys the View.
- `_on_build()`: mandatory private method to implement, you must define the `_body` here.
- `_on_display()`: optional private method to implement, executed when the View is displayed.
- `_on_destroy()`: optional private method to implement, executed when the View is destroyed
- `_toplevel_geometry()`: if your View's `body` is a toplevel, you can implement this private method to alter the geometry of the View. By default, the view is centered (if the view is a toplevel).


## Implementation
The source code for the Primes project is available on [Github](https://github.com/pyrustic/primes).

Clone the Primes project on your computer:

```bash
$ git clone https://github.com/pyrustic/primes
```

The project is divided into two main parts, the frontend and the backend.

### The Frontend
The frontend of the project consists of:

- `$APP_PKG.view.main_view`: represents the entire graphical interface. The other Views are assembled together in this module.
- `$APP_PKG.view.top_view`: represents the top of the GUI. The status of the application is displayed in this View. This is where "Welcome !" is displayed.
- `$APP_PKG.view.center_view`: represents the middle of the GUI. This is where the primes are displayed.
- `$APP_PKG.view.bottom_view`: represents the bottom of the GUI. This is where the user controls the application.

### The Backend
The backend of the project consists of:

- `$APP_PKG.core.primes_generator`: this module performs the primes generation.
- `$APP_PKG.host.main_host`: this module is the link between the View and the primes generator.

### How It Works ?
#### Communicating Between Components And Event Notification
How to design a smooth communication between the components of this project ?

One solution would be to make sure that each of the components has a reference to the other components. The components would be tightly coupled with each other. It's a good idea but the maintenance will be difficult to do in the future.

The project uses the libary `pyrustic.com` to achieve a smooth communication between component and a loose coopling, embracing Events notifications ! 

`pyrustic.com.Com` combines multiple solutions to facilitate communication between multiple components. Here are some features of `pyrustic.com.Com`:
- [Publish-Subscribe](https://en.wikipedia.org/wiki/Publish%E2%80%93subscribe_pattern);
- event notification;
- register resources;
- request for registered resources;
- and more.

This library describes an Event as a sequence of words. This flexibility offers a lot of power and possibilities.

I defined events that could occur in the app. I want the structure of an Event to be intuitive. So I made events description follow the [SVO](https://en.wikipedia.org/wiki/Subject%E2%80%93verb%E2%80%93object) (Subject-Verb-Object) structure.

Here are the Events defined for the Primes project:
- `user submit number`: Event triggered when the user clicks the Start button after entering a number. The data associated with this Event is the number entered.
- `"user click stop"`: Event triggered when the user clicks on the Stop button.
- `"user click clear"`: Event triggered when the user clicks on the Clear button.
- `"user click exit"`: Event triggered when the user clicks on the Exit button.
- `"host send prime"`: Event triggered when a new prime is published by the main_host.
- `"core end computation"`: Event triggered when the primes generator ends the generation of primes.
- `"gui end displaying"`: Event triggered when the `center_view` has finished displaying primes.

The great thing about `pyrustic.com.Com` is that you can subscribe to a sub-part of the Event. It is therefore possible to subscribe to all events where the user clicks a button. The sequence will therefore be `"user click"` and therefore automatically includes `"user click stop"`, `"user click clear"` and `"user click exit"`.

The following is a realistic pseudo-code to show a bit of the power of `pyrustic.com`:

```python
from pyrustic.com import Com


class Host:
    def __init__(self, com):
        # register the resources self.get_books as "library"
        com.res("library", self.get_books)

    def get_books(self, category):
        # return the list of books
        return ["book1", "book2", "book2"]


class DisplayView:
    def __init__(self, com):
        # subscribe to the event "user click books"
        com.sub("user click books", self._event_handler)

    def _event_handler(self, event, data):
        # the argument 'fantasy'
        res_args = (data, )
        # it will be like running host.get_books("fantasy")
        # and send the returned data to self.display
        com.req("library", res_args=res_args,
                consumer=self.display)

    def display(self, data):
        for book in data:
            # display book
            pass


class ControlView:
    def __init__(self, com):
        # publish the event "user click books"
        # with the linked data "fantasy" as books category
        com.pub("user click books", data="fantasy")


com = Com()
Host(com)
DisplayView(com)
ControlView(com)
```

As can be seen in the code above, the components communicate easily without knowing each other. In addition, with the SVO-Events, the code is easily understood.

#### Multithreading and Queueing
The calculation of primes is an intensive task. To provide a smooth user experience, our program will perform the calculation in the background with `pyrustic.threadom`, a library to perform a `gui-toolkit-compatible` smooth `multithreading`.

The following lines of code are realistic pseudo-code. Read this code snippet to understand how `pyrustic.threadom` could be used to achieve multithreading and queueing:

```python
import tkinter as tk
from pyrustic.threadom import Threadom


class Host:
    def compute(self, number, queue):
        # use number to generate primes
        # push primes in the queue
        for prime in _primes_generator(number):
            queue.put(prime)

    def _primes_generator(self, number):
        # code to generate primes
        pass

def display_prime(prime):
    # display prime
    pass

user_input = 1000  # assume the user submitted '1000' and then clicked start
threadom = Threadom(tk.Tk())  # Threadom needs a tk object to work
queue = threadom.q()  # get a queue
host = Host()
target = host.compute
target_args = (user_input, queue)
# run this in a new thread: host.compute(input_number, queue)
threadom.run(target=target, target_args=target_args)
# start queue consuming loop (it doesn't block the GUI at all)
queue_id = threadom.consume(queue, consumer=display_prime)
# ...
threadom.stop(queue_id)  # this stop the queue consuming loop
```


## Distribute Your Your App With Hubstore
Link the project directory to Pyrustic Manager
```bash
(pyrustic) link /path/to/primes
```

Then build a distribution package (Wheel).
```bash
(pyrustic) build
```

Publish your app:
```bash
(pyrustic) publish
```

You need a personal access token to publish your app. It is easy to generate a personal access token. Read this [article](https://docs.github.com/en/free-pro-team@latest/github/authenticating-to-github/creating-a-personal-access-token).


Once the app published, distribute it to users and friends via Hubstore. Discover [Hubstore](https://github.com/pyrustic/pyrustic#hubstore---to-connect-apps-with-users) !


## Going Further
- Join the [Discord](https://discord.gg/fSZ6nxzVd6) !
- Learn [Tkinter](https://github.com/pyrustic/pyrustic#introduction-to-tkinter)
- Learn [Python](https://github.com/pyrustic/pyrustic#introduction-to-python)
- Discover [Pyrustic](https://github.com/pyrustic/pyrustic#readme)

[< Previous](https://github.com/pyrustic/pyrustic/blob/master/docs/tutorial/tutorial-1.md) | [Home](https://github.com/pyrustic/pyrustic/blob/master/docs/tutorial/README.md) 
