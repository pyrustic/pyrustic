<!-- Image -->
<div align="center">
    <img src="https://raw.githubusercontent.com/pyrustic/misc/master/media/cover.png" alt="Cover">
    <br>
    <p align="center">
    The Pyrustic software suite with the cyberpunk theme
    </p>
</div>

<!-- Intro Text -->
# Pyrustic
`Pyrustic` is a lightweight framework and software suite to help develop, package, and publish `Python` `desktop applications`.

This is an [emailware](https://en.wiktionary.org/wiki/emailware). You are encouraged to send a [feedback](#contact).

<!-- Quick Links -->
[Demo](#demo-video) | [Installation](#installation) | [Documentation](#documentation) | [Hubstore](#hubstore---to-connect-apps-with-users)

<!-- Table of contents -->
# Table Of Contents
- [Overview](#overview)
- [The Framework](#the-framework)
  - [Standard Project Structure](#standard-project-structure)
  - [GUI](#gui)
  - [Multithreading](#multithreading)
  - [Fetching Resources](#fetching-resources)
  - [Communicating Between Components And Event Notification](#communicating-between-components-and-event-notification)
  - [Database Access Object](#database-access-object)
  - [And More](#and-more)
- [The Manager](#the-manager)
- [The Software Suite](#the-software-suite)
  - [Rustiql - The Graphical SQL Editor](#rustiql---the-graphical-sql-editor)
  - [Jupitest - The Graphical Test Runner](#jupitest---the-graphical-test-runner)
  - [Hubway -  Release Your App To The World](#hubway---release-your-app-to-the-world)
- [Hubstore - To Connect Apps With Users](#hubstore---to-connect-apps-with-users)
- [Demo Video](#demo-video)
- [Requirements](#requirements)
- [Installation](#installation)
- [Documentation](#documentation)
    - [FAQ](#faq)
    - [Tutorial](#tutorial)
    - [Glossary](#glossary)
    - [Framework Reference](#framework-reference)
- [External Learning Resources](#external-learning-resources)
- [Philosophy](#philosophy)
- [License](#license)
- [Contact](#contact)

<!-- Overview -->
# Overview
Python is one of the world's most [popular](https://www.wired.com/story/python-language-more-popular-than-ever/) programming languages. There are some great frameworks for building web application with Python. Pyrustic targets Python desktop application development.

A framework alone is not enough to build a great app. `Pyrustic` comes with batteries included, just like the Python language itself which comes with an amazing standard library. `Pyrustic` is a lightweight framework and software suite to help develop, package, and publish Python `desktop applications`.

Pyrustic is flexible enough that you can use both the framework and the software suite or just one of the components. For example, you can decide to only use the `Table` widget from the` pyrustic.widget` package in your existing `Tkinter` codebase. Another example is to only use Pyrustic to build a [Wheel](https://wheel.readthedocs.io/en/stable/story.html) and then publish it.

The framework and the software suite are useful for a new project as well as for an existing project.


# The Framework
The Framework covers various topics, from GUI to database connection, and more.

## Standard Project Structure
The `Framework` is easy to use and flexible with only three constraints:
- you have to follow the conventional Python project structure as described in the [Python Packaging User Guide](https://packaging.python.org/tutorials/packaging-projects/);
- you need to have a `__main__.py` file in the source package;
- the project name should be the same as the source package.

In fact, these aren't constraints but simply `elegance` and [proactivity](https://en.wikipedia.org/wiki/Proactivity). It will save you a lot of trouble in the future (believe me). By the way, the command-line tool [Manager](#the-manager) will take care of these details for you, you will just need to link a project directory, then issue the command `init`.

## GUI
Pyrustic proudly uses `Tkinter` as `GUI Toolkit`. Remember that the entire software suite was built with Pyrustic.

Some features related to the GUI:
- The `Framework` comes with many awesome widgets (mega-widgets to be precise): `Table`, `Scrollbox`, `Toast`, `Tree` and more.
- `pyrustic.default_style` and `pyrustic.theme`: a style/theme system to make it easy for you to build beautiful GUIs.
- `pyrustic.theme.cyberpunk`: a dark theme ready to use, the one used as base theme by the entire software suite.
- `pyrustic.view.View`: Pyrustic comes with the concept of `views`. `Views` are optional to use and are compatible with Tkinter. In fact, Views provides an intuitive lifecycle mechanism that will make it easier to build and maintain your GUI.
- and more...

### Example of typical `__main__.py` content

<details>
    <summary>Click to expand (or collapse)</summary>

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

</details>


## Multithreading
It is well known how difficult it is to implement multithreading in a Tkinter application. Pyrustic comes with `pyrustic.threadom`: a `library` to make it easy to develop multithreading applications. You can retrieve from the main thread the values returned by the functions executed in other threads and also the exceptions raised by these functions.

Jupitest the Pyrustic `Test Runner` makes extensive use of the `pyrustic.threadom` library to perform smooth real-time test reporting.

## Fetching Resources
Pyrustic comes with `pyrustic.gurl`: a `library` to fetch resources with an implementation of conditional request and a smart responses caching system.

`Hubway`, the Pyrustic app to publish application, uses this library to fetch resources as a good API citizen.

## Communicating Between Components And Event Notification
As a software grows, so is its complexity. Pyrustic comes with pyrustic.com a library to allow loosely coupled components to exchange data, subscribe to and publish events.

Please read the [tutorial](#tutorial) to geet a deep understanding of this section.


## Database Access Object
Pyrustic comes with `pyrustic.dao`: a `library` to simplify the connection to your SQLite database.
This library has some cool features like the ability to specify what I call a `creational script` that will be used to create a new database when it is missing.

## And More
- `pyrustic.jasonix`: a `library` included in the `Framework` which makes it so cool to work with `JSON` files. `Pyrustic` uses extensively this `library` to store user preferences, configuration data and more. With this `library`, you can initialize preferences/configuration/whatever files easily, thanks to the internal mechanism of `Jasonix` that creates a fresh copy of the given default `JSON` file at the target path. `Jasonix` also comes with a lock to open `JSON` files in readonly mode.
- for obvious reasons (clue: `beta`), `Pyrustic` does not take the risk of deleting the files it needs to get rid of, instead it moves them to a `trash` folder.
- and more...

# The Manager
<!-- Image -->
<div align="center">
    <img src="https://raw.githubusercontent.com/pyrustic/misc/master/media/manager.gif" alt="Manager" width="650">
    <p align="center">
    Manager
    </p>
</div>

The `Manager` is the entry point to the software suite. It's an optional command-line application with an API that you can use programmatically to automate your workflow.

Via the `Manager` you can:
- create a project with battery included (project structure, pyproject.toml, etc);
- easily add `packages`, `modules` or `files` to your project;
- run a specific `module` of your project;
- view recent projects list and quickly switch between projects;
- launch the `SQL Editor`, `Test Runner` and `Hubway` (respectively with commands `sql`, `test` and `hub`);
- build a distribution package according to setup.cfg and MANIFEST.in;
- find out if the project is installed ('pip install -e') in the current virtual env;  
- and more...

The `build` command builds a package that could be published with the application `Hubway`.

# The Software Suite
The lightweight software suite is made of:
- `Rustiql`: a graphical `SQL Editor`;
- `Jupitest`: a graphical `Test Runner`;
- and `Hubway`: an application to publish your project.

## Rustiql - The Graphical SQL Editor
<!-- Image -->
<div align="center">
    <img src="https://raw.githubusercontent.com/pyrustic/misc/master/media/rustiql.gif" alt="SQL Editor" width="650">
    <p align="center">
    SQL Editor
    </p>
</div>

The graphical `SQL Editor` allows you to:
- visualize your databases content;
- edit your database (CRUD);
- import SQL scripts;
- open in-memory database;
- and more...

The `SQL Editor` makes extensive use of the `pyrustic.dao` library.

## Jupitest - The Graphical Test Runner
<!-- Image -->
<div align="center">
    <img src="https://raw.githubusercontent.com/pyrustic/misc/master/media/jupitest.gif" alt="Test Runner" width="650">
    <p align="center">
    Test Runner
    </p>
</div>

The `Test Runner` reproduces the tree structure of the `tests` folder in your project. The `Test Runner` allows you to:
- run test `packages`;
- run test `modules`;
- run test `classes`;
- and even run test `methods`;
- and more...

The `Test Runner` makes extensive use of the `pyrustic.threadom` library to perform smooth real-time test reporting.

## Hubway - Release Your App To The World
<!-- Image -->
<div align="center">
    <img src="https://raw.githubusercontent.com/pyrustic/misc/master/media/hubway.gif" alt="Hubway" width="650">
    <p align="center">
    Hubway
    </p>
</div>

`Hubway` is an application that allows you to publish a new release of your application on `Github`. Once published, you can track your project, see metrics like the number of `stargazers`, `subscribers` or releases `downloads`.

`Hubway` makes extensive use of `pyrustic.gurl` to fetch resources.

You need a personal access token to publish a release via `Hubway` or to increase the API rate limit.
It is easy to generate a personal access token. Read this [article](https://docs.github.com/en/free-pro-team@latest/github/authenticating-to-github/creating-a-personal-access-token).



# Hubstore - To Connect Apps With Users
<!-- Image -->
<div align="center">
    <img src="https://raw.githubusercontent.com/pyrustic/misc/master/media/pyrustic_hubstore.png" alt="Pyrustic Hubstore" width="650">
    <p align="center">
    Pyrustic - Hubstore
    </p>
</div>

Once you are ready to release a new version of your app, `Pyrustic` allows you to build a distribution package with the `build` command and then publish it to Github with `Hubway`.

Then the question that arises is "How to make the `find-download-install-run` process easier for users?". This is where the `Hubstore` comes in.

With `Hubstore`, it's easy to showcase, distribute, install, and manage your Python desktop apps.

`Hubstore` is available on PyPI and yes it's also built with `Pyrustic` !

Do you want to learn more about `Hubstore` ? Discover [Hubstore](https://github.com/pyrustic/hubstore#readme) !


<!-- Demo -->
# Demo Video
This is the _now obsolete_ demo video but still worth watching.

Watch the [video](https://pyrustic.github.io) !

I will upload an up-to-date video later.

To open the page in a new tab, you can just do a CTRL+click (on Windows and Linux) or CMD+click (on MacOS) on the link.


<!-- Requirements -->
# Requirements
`Pyrustic` is a `cross platform` software suite. It should work on your computer (or nope, haha, versions under `1.0.0` will be considered `Beta` at best). It is built on [Ubuntu](https://ubuntu.com/download/desktop) with `Python 3.5`. `Pyrustic` comes with absolutely no warranty. So... à la guerre comme à la guerre.

As `Pyrustic` is built with `Python` for `Python developers` and also makes extensive use of `Tkinter`, you may need to learn [Python](#introduction-to-python) and [Tkinter](#introduction-to-tkinter).

<!-- Installation -->
# Installation
`Pyrustic` is available on [PyPI](https://pypi.org/) (the Python Package Index) to simplify the life of Python developers.

If you have never installed a package from PyPI, you must install the pip tool enabling you to download and install a PyPI package. There are several methods which are described on this [page](https://pip.pypa.io/en/latest/installing/).

```bash
$ pip install pyrustic

$ pyrustic
Welcome to Pyrustic Manager !
Version: 0.0.9
Type "help" or "?" to list commands. Type "exit" to leave.

(pyrustic) 
```

To upgrade `Pyrustic`:

```bash
$ pip install pyrustic --upgrade --upgrade-strategy eager
```


<!-- Documentation -->
# Documentation
Pyrustic is a work in progress. The versions of `Pyrustic` under `1.0.0` are aimed at an audience of early adopters. Check the FAQ and the Tutorial.
## FAQ
Read the [FAQ](https://github.com/pyrustic/pyrustic/blob/master/docs/FAQ.md).

## Tutorial
Read the [Tutorial](https://github.com/pyrustic/pyrustic/blob/master/docs/TUTORIAL.md).

## Glossary
Read the [Glossary](https://github.com/pyrustic/pyrustic/blob/master/docs/GLOSSARY.md).

## Framework Reference
Read the [Framework Reference](https://github.com/pyrustic/pyrustic/blob/master/docs/REFERENCE.md).

# External Learning Resources
Interesting links below to get started with Python, Tkinter and SQLite.

## Introduction to Python
- [python-guide](https://docs.python-guide.org/intro/learning/).
- [python tutorial](https://www.python-course.eu/python3_course.php). 
- freeCodeCamp on [Youtube](https://www.youtube.com/watch?v=rfscVS0vtbw).

## Introduction to Tkinter
- [tkdocs](https://tkdocs.com/).
- [tkinter tutorial](https://www.python-course.eu/python_tkinter.php).
- freeCodeCamp on [Youtube](https://www.youtube.com/watch?v=YXPyB4XeYLA).

## Introduction to SQLite
- [sqlitetutorial](https://www.sqlitetutorial.net/).
- freeCodeCamp on [Youtube](https://www.youtube.com/watch?v=byHcYRpMgI4).

Note: I am not affiliated with any of these entities. A simple web search brings them up.


<!-- Philosophy -->
# Philosophy
<details>
    <summary>Click to expand (or collapse)</summary>

## Wisdom from Antiquity
<!-- Image -->
<div align="center">
    <img src="https://raw.githubusercontent.com/pyrustic/misc/master/media/diogenes.jpg" alt="Diogenes" width="650">
    <p align="center">
    By <a href="https://en.wikipedia.org/wiki/en:Jean-L%C3%A9on_G%C3%A9r%C3%B4me" class="extiw" title="w:en:Jean-Léon Gérôme">Jean-Léon Gérôme</a> - <a href="https://en.wikipedia.org/wiki/en:Walters_Art_Museum" class="extiw" title="w:en:Walters Art Museum">Walters Art Museum</a>: <a href="https://thewalters.org/" rel="nofollow"></a> <a rel="nofollow" class="external text" href="https://thewalters.org/">Home page</a>&nbsp;<a href="https://art.thewalters.org/detail/31957" rel="nofollow"></a> <a rel="nofollow" class="external text" href="https://art.thewalters.org/detail/31957">Info about artwork</a>, Public Domain, <a href="https://commons.wikimedia.org/w/index.php?curid=323523">Link</a>
    </p>
</div>

<br>

> He owned a cup which served also as a bowl for food but threw it away when he saw a boy drinking water from his hands and realized one did not even need a cup to sustain oneself.</p>
>
>    --Mark, J. J. (2014, August 02). [Diogenes of Sinope](href="https://www.ancient.eu/Diogenes_of_Sinope/). Ancient History Encyclopedia. Retrieved from https://www.ancient.eu/Diogenes_of_Sinope/

<br>

## Advertisement from the twentieth century
<!-- Image -->
<div align="center">
    <img src="https://raw.githubusercontent.com/pyrustic/misc/master/media/ibm.jpg" alt="IBM" width="500">
    <p align="justify">
    By Cecile &amp; Presbrey advertising agency for International Business Machines. - Scanned from the December 1951 issue of Fortune by <a href="//commons.wikimedia.org/wiki/User:Swtpc6800" title="User:Swtpc6800">User:Swtpc6800</a> Michael Holley. The image was touched up with Adobe Photo Elements., Public Domain, <a href="https://commons.wikimedia.org/w/index.php?curid=17480483">Link</a>
    </p>
</div>

<br>

> 150 Extra Engineers
>
> An IBM Electronic Calculator speeds through thousands of intricate computations so quickly that on many complex problems it's like having 150 EXTRA Engineers.
>
> No longer must valuable engineering personnel ... now in critical shortage ... spend priceless creative time at routine repetive figuring.
>
> Thousands of IBM Electronic Business Machines ... vital to our nation's defense ... are at work for science, industry, and the armed forces, in laboratories, factories, and offices, helping to meet urgent demands for greater production.
>
> -- IBM International Business Machines

</details>


<!-- License -->
# License
`Pyrustic` is licensed under the terms of the permissive free software license `MIT License`.

<!-- Contact -->
# Contact
<details>
    <summary>Click to expand (or collapse)</summary>

<br>

Hi ! I'm Alex, operating by ["Crocker's Rules"](http://sl4.org/crocker.html)
<!-- Image -->
![email](https://raw.githubusercontent.com/pyrustic/misc/master/media/email.png)

<!-- xoxo -->
<details>
    <summary></summary>
        <br>
        <br>
        Congratz ! You just found the Easter Meggs !
        <br>
        <br>
        <!-- Image -->
        <div align="center">
            <img src="https://raw.githubusercontent.com/pyrustic/misc/master/media/meme_1.jpg" alt="Meme">
            <br>
            <br>
            <br>
            <img src="https://raw.githubusercontent.com/pyrustic/misc/master/media/meme_5.jpg" alt="Meme">
            <br>
            <br>
            <br>
            <img src="https://raw.githubusercontent.com/pyrustic/misc/master/media/meme_6.jpg" alt="Meme">
            <br>
            <br>
            <br>
            <img src="https://raw.githubusercontent.com/pyrustic/misc/master/media/meme_7.jpg" alt="Meme">
            <br>
            <br>
            <br>
        </div>
</details>

</details>


