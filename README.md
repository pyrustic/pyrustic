# Pyrustic
`Pyrustic Framework` is a lightweight framework to develop, package, and publish `Python` desktop applications.

[Installation](#installation) | [Tutorial](https://github.com/pyrustic/pyrustic/tree/master/docs/tutorial#readme) | [Guide](https://github.com/pyrustic/pyrustic/tree/master/docs/guide#readme) | [Reference](https://github.com/pyrustic/pyrustic/tree/master/docs/reference#readme) | [Website](https://pyrustic.github.io)

# Table Of Contents
- [Overview](#overview)
- [Installation](#installation)
- [Documentation](#documentation)
- [External Learning Resources](#external-learning-resources)
- [Linked Projects](#linked-projects)
  - [Hubstore](#hubstore)
  - [Dresscode](#dresscode)
- [License](#license)
- [Contact](#contact)

# Overview

`Python` is one of the world's most [popular](https://www.wired.com/story/python-language-more-popular-than-ever/) programming languages. It's used in many application domains from machine learning to web development. Desktop application development is exciting. `Pyrustic Framework` aims to help you build great desktop apps.

## Batteries included

`Pyrustic Framework` comes with batteries included:
- `Project Manager`: command-line tool that allows you to initialize a project directory with a structure as described in the [Python Packaging User Guide](https://packaging.python.org/tutorials/packaging-projects/), perform `versioning`, `build` a [distribution package](https://wheel.readthedocs.io/en/stable/story.html), `publish` the distribution package, and more. This tool comes with a nice `hooking` mechanism and an `API` so you could easily automate your workflow with `Python` code.
- [Viewable](https://github.com/pyrustic/viewable): subclass it to implement a view with a transparent `lifecycle` mechanism that will make it easier to build and maintain your `GUI`.
- [Megawidget](https://github.com/pyrustic/megawidget): a set of useful megawidgets like `Table`, `Scrollbox`, `Toast`, `Tree` and more.
- [Themebase](https://github.com/pyrustic/themebase) and [stylebase](https://github.com/pyrustic/stylebase): a style/theme mechanism to make it easy for you to create your own `styles` and `themes`. 
- [Cyberpunk-theme](https://github.com/pyrustic/cyberpunk-theme): give a modern look to your desktop app with this `dark theme`.
- [Winter-theme](https://github.com/pyrustic/winter-theme): give a modern look to your desktop app with this `light theme`.
- [Threadom](https://github.com/pyrustic/threadom): it is well known how difficult it is to implement `multithreading` in a `Tkinter` application. `Threadom` is a library to make it easy to develop multithreading applications. You can retrieve from the main thread the values returned and the exceptions raised by the functions executed in other threads.
- [Shared](https://github.com/pyrustic/shared): library to store, expose, read, and edit `collections` of data.
- [Diaspora](https://github.com/pyrustic/diaspora): as a software grows, so is its complexity. `Diaspora` allows loosely coupled components to exchange data, subscribe to events and publish events notifications.
- [Jayson](https://github.com/pyrustic/jayson): intuitive interaction with [JSON](https://en.wikipedia.org/wiki/JSON) files. With `Jayson`, you can initialize preferences/configuration/whatever `JSON` files easily, thanks to its internal mechanism that creates a fresh copy of the given default `JSON` file at the target path. `Jayson` also comes with a lock to open `JSON` files in readonly mode.
- [Kurl](https://github.com/pyrustic/kurl): `library` to fetch resources with an implementation of [conditional request](https://developer.mozilla.org/en-US/docs/Web/HTTP/Conditional_requests) and a smart responses caching system.
- [Litedao](https://github.com/pyrustic/litedao): `library` to simplify the connection to your [SQLite](https://www.sqlite.org/index.html) database with some cool features like the ability to specify what I call a `creational script` that will be used to create a new database when it is missing.

As you can see, the framework covers various topics, from GUI to database connection, and it enforces good practices like the project structure by example.


## Examples

This is the typical content of `__main__.py`:

<details>
    <summary>Click to expand (or collapse)</summary>

```python
from pyrustic.app import App
from cyberpunk_theme import Cyberpunk
# the framework comes with a graphical 'Hello World' view
from pyrustic.hello import HelloView


def main():
    # The App
    app = App()
    # Set the theme
    app.theme = Cyberpunk()
    # Set the main view (it could be a plain old Tkinter object)
    app.view = HelloView(app) 
    # Center the window
    app.center()
    # Lift off !
    app.start()


if __name__ == "__main__":
    main()

```

</details>


This is an example of a `view` definition:

<details>
    <summary>Click to expand (or collapse)</summary>

```python
import tkinter as tk
from viewable import Viewable


class View(Viewable):
    def __init__(self, master):
        super().__init__()
        self._master = master

    def _build(self):
        self._body = tk.Frame(self._master)
        label = tk.Label(self._body, text="Hello !")
        label.pack()

    def _on_map(self):
        """ This method is called when the view is mapped for the first time """

    def _on_destroy(self):
        """ This method is called when the view is destroyed """


if __name__ == "__main__":
    root = tk.Tk()
    view = View(root)
    # the method build_pack() builds then packs the view.
    # In fact you could do:
    #   view.build() then view.pack()
    # or:
    #   view.build() then view.body.pack()
    view.build_pack()  # it accepts arguments like the Tkinter pack() method
    root.mainloop()
    
```

</details>

This is an example of a `naked view` (a view that doesn't subclass `Viewable`):

<details>
    <summary>Click to expand (or collapse)</summary>

```python
import tkinter as tk
from pyrustic.app import App
from cyberpunk_theme import Cyberpunk


def view(app):
    """ A Naked View is a function that accepts the app reference as argument
    and returns a Tkinter object (generally a container like tk.Frame) """
    master = app.root
    # The body of this naked view is a tk.Frame
    body = tk.Frame(master)
    label = tk.Label(body, text="Hello !")
    label.pack()
    return body  # mandatory !


if __name__ == "__main__":
    app = App()
    app.theme = Cyberpunk()
    app.view = view  # Naked view reference
    app.start()
    
```

</details>

# Installation
## Requirements

`Pyrustic Framework` is `cross platform` and versions under `1.0.0` will be considered `Beta` at best. It is built on [Ubuntu](https://ubuntu.com/download/desktop) with [Python 3.8](https://www.python.org/downloads/) and should work on `Python 3.5`.

As `Pyrustic Framework` is built with `Python` for `Python developers` you may need to learn [Python](#introduction-to-python) and [Tkinter](#introduction-to-tkinter).

## First time
Install for the first time:

```bash
$ pip install pyrustic
```

## Upgrade
To upgrade `Pyrustic Framework`:

```bash
$ pip install pyrustic --upgrade --upgrade-strategy eager
```

I recommend upgrading `Pyrustic Framework` with the `eager` upgrade strategy as specified since the project is under active development.

# Documentation

## FAQ
Read the [FAQ](https://github.com/pyrustic/pyrustic/blob/master/docs/faq#readme).

## Tutorial
Read the [Tutorial](https://github.com/pyrustic/pyrustic/blob/master/docs/tutorial#readme).

## Guide
Read the [Guide](https://github.com/pyrustic/pyrustic/blob/master/docs/guide#readme).

## Glossary
Read the [Glossary](https://github.com/pyrustic/pyrustic/blob/master/docs/glossary#readme).

## Reference
Read the [Reference](https://github.com/pyrustic/pyrustic/blob/master/docs/reference#readme).

# External Learning Resources
Some interesting links below to get started with `Python`, `Tkinter` and `SQLite`.

## Introduction to Python
- [python-guide](https://docs.python-guide.org/intro/learning/)
- [python tutorial](https://www.python-course.eu/python3_course.php)
- freeCodeCamp on [Youtube](https://www.youtube.com/watch?v=rfscVS0vtbw)

## Introduction to Tkinter
- [tkdocs](https://tkdocs.com/)
- [tkinter tutorial](https://www.python-course.eu/python_tkinter.php)
- freeCodeCamp on [Youtube](https://www.youtube.com/watch?v=YXPyB4XeYLA)

## Introduction to SQLite
- [sqlitetutorial](https://www.sqlitetutorial.net/)
- freeCodeCamp on [Youtube](https://www.youtube.com/watch?v=byHcYRpMgI4)

`Note:` I am not affiliated with any of these entities. A simple web search brings them up.



# Linked Projects
`Pyrustic Framework` is part of the [Open Pyrustic Ecosystem](https://pyrustic.github.io). Let's discover some other ecosystem projects.

## Hubstore
Once you have published your app to Github with the command `publish` in the `Project Manager`, the next question that arises is: "How to make the `find-download-install-run` process easier for users ?". This is where `Hubstore` comes in.

<!-- Image -->
<div align="center">
    <img src="https://raw.githubusercontent.com/pyrustic/misc/master/media/hubstore_cover.png" alt="Hubstore" width="650">
    <p align="center">
    <i> Hubstore - To Connect Apps With Users </i>
    </p>
</div>



With `Hubstore`, it's easy to showcase, distribute, install, and manage your Python desktop apps.

Note that any Python Wheel app is compatible with `Hubstore`, in others words, you don't need to use the `Pyrustic Framework` to have a `Hubstore` compatible app.

<!-- Image -->
<div align="center">
    <img src="https://raw.githubusercontent.com/pyrustic/misc/master/media/pyrustic_hubstore.png" alt="Pyrustic Hubstore" width="650">
    <p align="center">
    <i> The Pyrustic Open Pipeline to distribute apps </i>
    </p>
</div>

`Hubstore` itself is built with `Pyrustic Framework` and is available on `PyPI`.

Do you want to learn more about `Hubstore` ? Discover [Hubstore](https://github.com/pyrustic/hubstore#readme) !


## Dresscode
If `Pyrustic Framework` is [C](https://en.wikipedia.org/wiki/C_(programming_language)), `Dresscode` would be Python. 

`Dresscode` is a high productivity framework for developing a graphical user interface without prior knowledge of using a GUI Toolkit.

As a high productivity framework, `Dresscode` is suitable for teaching, prototyping, testing, adding a GUI to command-line scripts, developing simple to complex desktop applications, etc.

<div align="center">
    <img src="https://raw.githubusercontent.com/pyrustic/misc/master/media/dresscode-figure-3.gif" alt="Pyrustic Hubstore" width="650">
    <p align="center">
    <i> Dresscode demo built with 1 hex-digit lines of Python code </i>
    </p>
</div>

Under the hood, `Dresscode` uses `Pyrustic Framework`.

Discover [Dresscode](https://github.com/pyrustic/dresscode#readme) !

## Desktop apps built with  Pyrustic Framework
Here are some desktop apps built with `Pyrustic Framework`

<details>
    <summary>Click to expand (or collapse)</summary>

<br>

<div align="center">
    <img src="https://raw.githubusercontent.com/pyrustic/misc/master/media/jupitest.gif" alt="Jupitest" width="650">
    <p align="center">
      <i> <a href="https://github.com/pyrustic/jupitest#readme">Jupitest</a> - Graphical test runner </i>
    </p>
</div>

<br>

<div align="center">
    <img src="https://raw.githubusercontent.com/pyrustic/misc/master/media/rustiql.gif" alt="Rustiql" width="650">
    <p align="center">
      <i> <a href="https://github.com/pyrustic/rustiql#readme">Rustiql</a> - Graphical SQL editor </i>
    </p>
</div>

</details>

# License
`Pyrustic Framework` is licensed under the terms of the permissive free software license `MIT License`.

<!-- Contact -->

# Contact

Hi ! I'm Alex, operating by ["Crocker's Rules"](http://sl4.org/crocker.html)
<!-- Image -->
![email](https://raw.githubusercontent.com/pyrustic/misc/master/media/email.png)

