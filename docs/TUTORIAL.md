<!-- Image -->
<div align="center">
    <img src="https://raw.githubusercontent.com/pyrustic/misc/master/media/primes.gif" alt="Primes" width="650">
    <p align="center">
    Primes
    </p>
</div>


## Table Of Contents
- [Introduction](#introduction)
- [Install Pyrustic](#install-pyrustic)
- [Project Creation](#project-creation)
- [Project Structure](#project-structure)
- [Masterplan](#masterplan)
    - [Separation of concerns](#separation-of-concerns)
    - [The View](#the-view)
    - [Multithreading and Queueing](#multithreading-and-queueing)
- [Communicating Between Components](#communicating-between-components)
    - [Subject-Verb-Object Event: intuitive description of an Event](#subject-verb-object-event-intuitive-description-of-an-event)
    - [Realistic Example](#realistic-example)
- [Implementation](#implementation)
    - [What is a view ?](#what-is-a-view-)
- [Distribute Your App](#distribute-your-app)
- [Conclusion](#conclusion)


## Introduction
[Pyrustic](https://github.com/pyrustic/pyrustic#readme) is a lightweight framework and software suite to help develop, package, and publish `Python` desktop applications. The project is designed so that one can use only one component and ignore the others. For example, we can only use the `pyrustic.table` widget in an existing project.

In this tutorial we will create a program that calculates [primes](https://en.wikipedia.org/wiki/Prime_number). The project will allow us to cover different aspects of Pyrustic such as multithreading or communicating between components.

## Install Pyrustic
`Pyrustic` is available on [PyPI](https://pypi.org/) (the Python Package Index). If you have never installed a package from PyPI, you must install the `pip` tool enabling you to download and install a PyPI package. There are several methods which are described on this [page](https://pip.pypa.io/en/latest/installing/).

```bash
$ pip install pyrustic

$ pyrustic
Welcome to Pyrustic Manager !
Version: 0.1.0
Type "help" or "?" to list commands. Type "exit" to leave.

(pyrustic) 
```

To upgrade `Pyrustic`:

```bash
$ pip install pyrustic --upgrade --upgrade-strategy eager
```

Now that you have Pyrustic installed on your computer, let's move on to creating the `primes` project.

## Project Creation
Create the project folder. Name it `primes`. Then start [Pyrustic Manager](https://github.com/pyrustic/pyrustic#the-manager) by typing `pyrustic` on the command line.

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

From now on, the project linked to `Pyrustic Manager` will be called the `Target`. You can issue the` target` command to see the currently linked project.

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

If you quit Pyrustic Manager, the next time you want to link the same project, run the `relink` command or use the `last` command.

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

## Masterplan

This section of the tutorial aims to present how the project should work. The implementation of the project will be discussed in the section [Implementation](#implementation).

### Separation of concerns

<!-- Image -->
<div align="center">
    <img src="https://raw.githubusercontent.com/pyrustic/misc/master/media/primes_tutorial_figure_1.png" alt="Figure" width="650">
    <p align="center">
    Figure 1: Separation of concerns
    </p>
</div>

The project will be divided into two logical parts:
- View: user input, button to start/stop computation, display prime numbers;
- Host: generate prime numbers.

### The View
<!-- Image -->
<div align="center">
    <img src="https://raw.githubusercontent.com/pyrustic/misc/master/media/primes_tutorial_figure_2.png" alt="Figure" width="650">
    <p align="center">
    Figure 2: The View
    </p>
</div>


The user submits a number in the Entry then clicks on the Enter button. The generated primes are displayed in the ScrolledText.


### Multithreading and Queueing

<div align="center">
    <img src="https://raw.githubusercontent.com/pyrustic/misc/master/media/primes_tutorial_figure_3.png" alt="Figure" width="650">
    <p align="center">
    Figure 3: Multithreading and Queueing 
    </p>
</div>

The calculation of primes is an intensive task. To provide a smooth user experience, our program will perform the calculation in the background. The View will send to the Host the input number and also the Queue in which insert the primes. The View then will consume the contents of the Queue. `Pyrustic` comes with `pyrustic.threadom.Threadom`, a library to perform a `gui-toolkit-compatible` smooth `multithreading`.

The following lines of code are intended to explain programmatically the `Figure 3`. It's a realistic pseudo-code. Do not run it, this is not the [implementation](#implementation).

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

## Communicating Between Components

In this project, we can identify these main components:
- View: the entire graphical interface
    - footer_view: this is where the user enters a number and clicks Start
    - central_view: this is where the primes generated by Host are displayed
- Host: use the submitted number to generate primes.

We know that the View is executing the Host in a thread with Threadom. But how to manage the communication between the footer_view, the central_view and the Host?

One solution would be to make sure that each of the components has a reference to the other components. The components would be tightly coupled with each other. It's a good idea but the maintenance will be difficult to do in the future.

Pyrustic comes with `pyrustic.com.Com`, a library that combines multiple solutions to facilitate communication between multiple components. Here are some features of `pyrustic.com.Com`:
- [Publish-Subscribe](https://en.wikipedia.org/wiki/Publish%E2%80%93subscribe_pattern);
- event notification;
- register resources;
- request for registered resources.

### Subject-Verb-Object Event: intuitive description of an Event

The `pyrustic.com.Com` library describes an Event as a sequence of words. This flexibility offers a lot of power and possibilities. For our Primes project, I defined the Events according to the [SVO](https://en.wikipedia.org/wiki/Subject%E2%80%93verb%E2%80%93object) (Subject-Verb-Object) structure.

Here are the Events defined for the Primes project:
- `user submit number`: Event triggered when the user clicks the Start button after entering a number. The data associated with this Event is the number entered.
- `"user click stop"`: Event triggered when the user clicks on the Stop button.
- `"user click clear"`: Event triggered when the user clicks on the Clear button.
- `"user click exit"`: Event triggered when the user clicks on the Exit button.
- `"host compute prime"`: Event triggered when the View retrieves a prime number generated by Host.
- `"host stop computation"`: Event triggered when the Host stops the generation of primes.
- `"gui stop displaying"`: Event triggered when the `central_view` has finished displaying primes. Remember that the Host is executed in another thread, so there is an asynchronous relationship between the Host and the View. When the Host finishes generating the primes, the View is busy consuming the Queue and displaying the primes one by one.

The great thing about `pyrustic.com.Com` is that you can subscribe to a sub-part of the Event. It is therefore possible to subscribe to all events where the user clicks a button. The sequence will therefore be `"user click"` and therefore automatically includes `"user click stop"`, `"user click clear"` and `"user click exit"`.

### Realistic Example
The following is a realistic pseudo-code to show a bit of the power of `pyrustic.com.Com`:

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


## Implementation
The project is available [here](https://github.com/pyrustic/primes).

You can clone it and play with it locally:

```bash
$ git clone https://github.com/pyrustic/primes
```

### What is a view ?
Pyrustic comes with the concept of views. Views are optional to use and are compatible with Tkinter. In fact, Views provides an intuitive lifecycle mechanism that will make it easier to build and maintain your GUI. To create a view, subclass `pyrustic.view.View`.

Following is an example to illustrate this section:

```python
import tkinter as tk
from pyrustic.view import View

class MyView(View):
    
    def __init__(self, master):
        super().__init__()
        self._master = master
        self._body = None
        
    def _on_build(self):  # the only mandatory method to implement
        self._body = tk.Frame(self._master)
        label = tk.Label(self._body, text="Hello World")
        label.pack()
        button = tk.Button(self._body, text="Destroy",
                           command=self.destroy)
        button.pack()
    
    def _on_display(self):  # optional
        # code here will be executed when the body
        # of this view is visible for the first time
        pass

    def _on_destroy(self):  # optional
        # code here will be executed when you destroy
        # the body of this view
        pass

    def my_custom_method(self):
        pass


root = tk.Tk()
my_view = MyView(root)
# the next line is equivalent to:
# my_view.build() then my_view.body.pack()
my_view.build_pack()  # build_grid and build_place also exist
# now you can access the body property 'my_view.body'
my_view.body.config(background="red")
# You can destroy the view: my_view.destroy()
# mainloop
root.mainloop()
```

The next example shows the typical content of `__main__.py`
```python
from pyrustic.app import App
from pyrustic.theme.cyberpunk import Cyberpunk
from demo.view.main_view import MainView


def main():
    # The App
    app = App(__package__)
    # Set theme
    app.theme = Cyberpunk()
    # Set view
    app.view = MainView(app)  # it could be a Tkinter object
    # Center the window
    app.center()
    # Lift off !
    app.start()


if __name__ == "__main__":
    main()
```

## Distribute Your App
Link the project directory to Pyrustic Manager
```bash
(pyrustic) link /path/to/primes
```

Then build a distribution package (Wheel).
```bash
(pyrustic) build
```

Open [Hubway](https://github.com/pyrustic/pyrustic#hubway---release-your-app-to-the-world), publish it ! You need a personal access token to publish a release via `Hubway` or to increase the API rate limit.
It is easy to generate a personal access token. Read this [article](https://docs.github.com/en/free-pro-team@latest/github/authenticating-to-github/creating-a-personal-access-token).

```bash
(pyrustic) hub
```

Once the app published, consume it, share it to your friends via Hubstore. Discover [Hubstore](https://github.com/pyrustic/pyrustic#hubstore---to-connect-apps-with-users) !


## Conclusion
This tutorial covers a tiny part of what can be done with Pyrustic. This is a work in progress, an improved version of this tutorial will come later. A Guide will also be added to the documentation. Thank you for your attention !
