<!-- Image -->
<div align="center">
    <img src="https://raw.githubusercontent.com/pyrustic/misc/master/media/cover.png" alt="Cover">
    <br>
    <p align="center">
    Pyrustic Suite
    </p>
</div>

<!-- Intro Text -->
# Pyrustic Suite
`Pyrustic Suite` is a lightweight software suite to help develop, package, and publish `Python` `desktop applications`.

This is an [emailware](https://en.wiktionary.org/wiki/emailware). You are encouraged to send a [feedback](#contact).

<!-- Quick Links -->
[Demo](#demo) | [Features](#features) | [Download](#download) | [Tutorial](#tutorial) | [Memes](#memes)

<!-- Table of contents -->
## Table Of Contents
- [Overview](#overview)
- [Demo](#demo)
- [Philosophy](#philosophy)
- [Features](#features)
- [Requirements](#requirements)
- [Download](#download)
- [Installation](#installation)
- [Tutorial](#tutorial)
- [Documentation](#documentation)
- [License](#license)
- [Memes](#memes)
- [Contact](#contact)

<!-- Overview -->
## Overview
Since `Python` comes with battery included, `Pyrustic Suite` makes extensive use of `Tkinter` as GUI Toolkit and `SQLite` as database engine.
`Pyrustic Suite` is made up of:
- `Manager`: a command-line application to rule them all;
- a graphical `SQL Editor`;
- a graphical `Test Runner`;
- `Hub`: a smart application to publish your project;
- and a `Framework`, on which all other components are based.

### The Manager
<!-- Image -->
<div align="center">
    <img src="https://raw.githubusercontent.com/pyrustic/misc/master/media/manager.gif" alt="Manager">
    <p align="center">
    Manager
    </p>
</div>

The `Manager` is the entry point to the `Suite`.
Via the `Manager` you can:
- create a project with battery included;
- add `packages`, `modules` or `files` to your project;
- run a specific `module` of your project;
- update the `Framework` of your project;
- update `Pyrustic Suite` itself;
- view recent projects list and quickly switch between projects;
- launch the `SQL Editor`, `Test Runner` and `Hub`;
- and more...

The `update` command creates a backup of the current version, erases the current version, then installs the latest version. If you want the `update` command to run smoothly, make sure you gave the correct permissions to the files and folders in `pyrustic` during the first install.

### The SQL Editor
<!-- Image -->
<div align="center">
    <img src="https://raw.githubusercontent.com/pyrustic/misc/master/media/sql_editor.gif" alt="SQL Editor">
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

The `SQL Editor` makes extensive use of the `pyrustic.litedao` library.

### The Test Runner
<!-- Image -->
<div align="center">
    <img src="https://raw.githubusercontent.com/pyrustic/misc/master/media/test_runner.gif" alt="Test Runner">
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

The `Test Runner` makes extensive use of the `pyrustic.threadium` library to perform smooth real-time test reporting.

### The Hub
<!-- Image -->
<div align="center">
    <img src="https://raw.githubusercontent.com/pyrustic/misc/master/media/hub.gif" alt="Hub">
    <p align="center">
    Hub
    </p>
</div>

The `Hub` is an application that allows you to package your project then publish it as new release on `Github`. Once published, you can track your project, see metrics like the number of `stargazers`, `subscribers` or releases `downloads`.
The metaphor of a drama is used for the process:
- a script named `Prolog` will be executed as the prologue;
- a script named `Epilog` will be executed as the epilogue.

The `Hub` thus gives you the possibility to influence this drama.
For example, in the `Prolog` you can set a flag in the ready-to-publish project to indicate that it is no longer in `dev` mode. 
You could even automate a part of your `git` workflow in the `Prolog` and/or `Epilog` script(s).

The `Hub` makes extensive use of `pyrustic.gurl` to fetch resources.

You need a personal access token to publish a release via `Hub` or to increase the API rate limit.
It is easy to generate a personal access token. Read this [article](https://docs.github.com/en/free-pro-team@latest/github/authenticating-to-github/creating-a-personal-access-token).

### The Framework
`Pyrustic Suite` is based on a `Framework`. This `Framework` can be injected into your project if you wish.
The `Framework` contains libraries that target:
- GUI;
- multithreading;
- fetching resources;
- database connection;
- and more...

You can update the `Framework` of your Target project by executing the command `sync` in the `Manager`.

<!-- Demo -->
## Demo
This is the [demo video](https://pyrustic.github.io).

To open the video in a new tab, you can just do a CTRL+click (on Windows and Linux) or CMD+click (on MacOS) on the link.

<!-- Philosophy -->
## Philosophy
### Wisdom from Antiquity
<!-- Image -->
<div align="center">
    <img src="https://raw.githubusercontent.com/pyrustic/misc/master/media/diogenes.jpg" alt="Diogenes">
    <p align="center">
    By <a href="https://en.wikipedia.org/wiki/en:Jean-L%C3%A9on_G%C3%A9r%C3%B4me" class="extiw" title="w:en:Jean-Léon Gérôme">Jean-Léon Gérôme</a> - <a href="https://en.wikipedia.org/wiki/en:Walters_Art_Museum" class="extiw" title="w:en:Walters Art Museum">Walters Art Museum</a>: <a href="https://thewalters.org/" rel="nofollow"></a> <a rel="nofollow" class="external text" href="https://thewalters.org/">Home page</a>&nbsp;<a href="https://art.thewalters.org/detail/31957" rel="nofollow"></a> <a rel="nofollow" class="external text" href="https://art.thewalters.org/detail/31957">Info about artwork</a>, Public Domain, <a href="https://commons.wikimedia.org/w/index.php?curid=323523">Link</a>
    </p>
</div>

<br>

>He owned a cup which served also as a bowl for food but threw it away when he saw a boy drinking water from his hands and realized one did not even need a cup to sustain oneself.</p>
>
>    --Mark, J. J. (2014, August 02). [Diogenes of Sinope](href="https://www.ancient.eu/Diogenes_of_Sinope/). Ancient History Encyclopedia. Retrieved from https://www.ancient.eu/Diogenes_of_Sinope/

<br>

### Advertisement from the twentieth century
<!-- Image -->
<div align="center">
    <img src="https://raw.githubusercontent.com/pyrustic/misc/master/media/ibm.jpg" alt="IBM">
    <p align="justify">
    By Cecile &amp; Presbrey advertising agency for International Business Machines. - Scanned from the December 1951 issue of Fortune by <a href="//commons.wikimedia.org/wiki/User:Swtpc6800" title="User:Swtpc6800">User:Swtpc6800</a> Michael Holley. The image was touched up with Adobe Photo Elements., Public Domain, <a href="https://commons.wikimedia.org/w/index.php?curid=17480483">Link</a>
    </p>
</div>


<!-- Features -->
## Features
A non-exhaustive list of features:
- `Manager`: entry-point, command-line application to help you to manage your project.
- `Test Runner`: a graphical `Test Runner` to run test `packages`, `modules`, `classes` and `methods`.
- `SQL Editor`: a graphical `SQL Editor` to edit your database, open `in-memory` database, load scripts.
- `Hub`: package your app, publish it, track it and see the metrics like the number of `stargazers`, `subscribers` or `downloads`.
- An optional `Framework` to inject in your project. The same `Framework` used by `Pyrustic Suite`.
- `pyrustic.threadium`: a `library` included in the `Framework` to make it easy to develop multithreading applications.
- `pyrustic.litedao`: a `library` included in the `Framework` to simplify the connection to your database.
- `pyrustic.gurl`: a `library` included in the `Framework` to fetch resources with an implementation of conditional request and a smart responses caching system. `Hub` uses this library to fetch resources as a good API citizen.
- `pyrustic.default_style` and `pyrustic.theme`: a style/theme system to make it easy for you to build beautiful GUIs.
- `pyrustic.themes.darkmatter`: a dark theme ready to use, the one used as base theme by the `SQL Editor`, `Test Runner` and the `Hub`.
- `pyrustic.viewable.Viewable`: bring an intuitive lifecycle system to your `Views` by making them implement `Viewable`. The mega-widgets in this framework implement `Viewable`.
- the `Framework` comes with many awesome widgets (mega-widgets to be precise): `Table`, `Scrollbox`, `Toast`, `Tree` and more.
- `pyrustic.jasonix`: a `library` included in the `Framework` which makes it so cool to work with `JSON` files. `Pyrustic Suite` uses extensively this `library` to store user preferences, configuration data and more. With this `library`, you can initialize preferences/configuration/whatever files easily, thanks to the internal mechanism of `Jasonix` that creates a copy of the given default `JSON` file at the target path. `Jasonix` also comes with a lock to open `JSON` files in readonly mode.
- for obvious reasons (clue: `beta`), `Pyrustic Suite` does not take the risk of deleting the files it needs to get rid of, instead it moves them to a `cache` folder.
- and more...

<!-- Requirements -->
## Requirements
`Pyrustic Suite` is a `cross platform` software suite. It should work on your computer (or nope haha, versions under `1.0.0` will be considered `Beta` at best). It is built on [Ubuntu](https://ubuntu.com/download/desktop) with `Python 3.5`. `Pyrustic Suite` comes with absolutely no warranty. So... à la guerre comme à la guerre.

As `Pyrustic Suite` is built with `Python` for `Python developers` and also makes extensive use of `Tkinter`, you may need to learn [Python](#introduction-to-python) and [Tkinter](#introduction-to-tkinter).

<!-- Download -->
## Download
Get the latest release version `0.0.3` [here](https://github.com/pyrustic/pyrustic/releases/download/v0.0.3/pyrustic-v0.0.3-released-by-pyrustic.zip).

<!-- Installation -->
## Installation
- Download the latest release [here](#download);
- uncompress the archive wherever you want (please choose a decent location);
- make sure you gave the correct permissions to the files and folders in `pyrustic` otherwise you couldn't update `pyrustic` later;
- go to the `ROOT_DIR`: the folder with files `main.py`, `install.py` and `about.py` inside;
- from the `ROOT_DIR`, run `install.py`;
- from the `ROOT_DIR`, run `main.py` to launch the `Manager`;
- welcome to `Pyrustic Suite` ! Type `help` in the `Manager` to discover the commands.

If you want to be able to run `Pyrustic Suite` after installation just by typing `pyrustic` in the shell, then consider making a small change to your system's `PATH`.
If you are not on `Windows`, check this [article](https://opensource.com/article/17/6/set-path-linux).

<!-- Tutorial -->
## Tutorial
- Create a `demo` folder to contain the project you want to start. This folder will be the `ROOT_DIR` of your project.
- Run `main.py` in `Pyrustic Suite` to open the `Manager`.
- Link your project to the `Manager` by typing the command `link` in the `Manager`. A dialog will appear so you could choose your demo project folder. You can also put the absolute path of the folder directly in front of the `link` command. The `link` command does not make any change in your project.
- Your project is now linked to the `Manager` and becomes the Target project. The `target` command displays the path to the Target project (its `ROOT_DIR`). You can unlink it with the command `unlink`. Whenever you come back to the `Manager`, just type `relink` to link again your previous Target project. Use the command `last` to see the list of last projects.
- You can now inject `Pyrustic Framework` in your project as well as other files/folders like for example the `tests` folder or the hidden folder `pyrustic_data`. You just have to type `kstart` in the `Manager` to perform a Kickstart. The `kstart` command modifies your project.
- You can run your project with the `run` command without arguments. You can also run a specific `module` in your project. Example: `run host.calc.addition`.
- Type `sql`, `test` or `hub` commands in the `Manager` to launch the `SQL Editor`, `Test Runner` or `Hub` respectively.
- Your project has an entry point which is `main.py`. In the `main.py` file, there is an instance of `pyrustic.app.App` to which the first `View` to display is passed.
- A `View` is a class that implements `pyrustic.viewable.Viewable`. In a `View` you must implement the `on_build()` method in which you assign a `Tk` object (`tk.Frame` or `tk.Toplevel`) to the `_body` instance variable.
- The `life cycle` of a `View` that implements `pyrustic.viewable.Viewable` is:
    - the call of the method `__init__()` at the `View` class instantiation;
    - then the call of the method `on_build()`;
    - then the call of the method `on_display()` when the `View` is visible;
    - and the call of the method `on_destroy()` when the `View` is destroyed.
- To run a `View`, call the `build()` method which will execute `on_build()` and will return the content of the `_body` instance variable. The `build_pack()` method builds the `View` then calls the method `pack()` on the `body` in a single call. Same stuff with `build_grid()` and `build_place()`. The method `build_wait()` is used for `View` built with a `Toplevel` as `_body`, thus, execution of the next instructions is paused until the destruction of the `View`. To destroy a `View`, call the method `destroy()`.

Note: Initializing your project with the `kstart` command in the `Manager` will create the `pyrustic_data` folder at the root of your project (`ROOT_DIR`). This folder may be hidden, so check your operating system settings. Take a look at this folder. The `Hub` application checks this folder to use some data like your project version or the path to the `Prolog` and `Epilog` scripts.

A better tutorial will come later. Use the `kstart` command in the `Manager` to get an equivalent of a graphical `Hello World` demo project, then explore the contents of your project. Start with `main.py`, then `view/main_view.py`. Good luck !

<!-- Documentation -->
## Documentation
The versions of `Pyrustic Suite` under `1.0.0` are aimed at an audience of early adopters. The documentation is precarious but public classes and methods have minimal documentation in the source code. You can also check the command `help` in the `Manager`.

### Introduction to Python
- [python-guide](https://docs.python-guide.org/intro/learning/).
- freeCodeCamp on [Youtube](https://www.youtube.com/watch?v=rfscVS0vtbw).

### Introduction to Tkinter
- [tkdocs](https://tkdocs.com/).
- freeCodeCamp on [Youtube](https://www.youtube.com/watch?v=YXPyB4XeYLA).

### Introduction to SQLite
- [sqlitetutorial](https://www.sqlitetutorial.net/).
- freeCodeCamp on [Youtube](https://www.youtube.com/watch?v=byHcYRpMgI4).

Note: I am not affiliated with any of these entities. A simple web search brings them up.

<!-- License -->
## License
`Pyrustic Suite` is licensed under the terms of the permissive free software license `MIT License`.

<!-- Memes -->
## Memes
<details>
    <summary>Click to expand (or collapse)</summary>
        <br>
        <!-- Image -->
        <div align="center">
            <img src="https://raw.githubusercontent.com/pyrustic/misc/master/media/meme_1.jpg" alt="Meme">
            <br>
            <br>
            <img src="https://raw.githubusercontent.com/pyrustic/misc/master/media/meme_2.jpg" alt="Meme">
            <br>
            <br>
            <img src="https://raw.githubusercontent.com/pyrustic/misc/master/media/meme_3.jpg" alt="Meme">
            <br>
            <br>
            <img src="https://raw.githubusercontent.com/pyrustic/misc/master/media/meme_4.jpg" alt="Meme">
            <br>
            <br>
            <img src="https://raw.githubusercontent.com/pyrustic/misc/master/media/meme_5.jpg" alt="Meme">
            <br>
            <br>
            <img src="https://raw.githubusercontent.com/pyrustic/misc/master/media/meme_6.jpg" alt="Meme">
            <br>
            <br>
            <img src="https://raw.githubusercontent.com/pyrustic/misc/master/media/meme_7.jpg" alt="Meme">
            <br>
            <br>
            <img src="https://raw.githubusercontent.com/pyrustic/misc/master/media/meme_8.jpg" alt="Meme">
            <br>
            <br>
            <img src="https://raw.githubusercontent.com/pyrustic/misc/master/media/meme_9.jpg" alt="Meme">
            <br>
            <br>
            <img src="https://raw.githubusercontent.com/pyrustic/misc/master/media/meme_10.jpg" alt="Meme">
            <br>
            <br>
            <img src="https://raw.githubusercontent.com/pyrustic/misc/master/media/meme_11.jpg" alt="Meme">
        </div>
</details>

<!-- Contact -->
## Contact
Hi ! I'm Alex, operating by ["Crocker's Rules"](http://sl4.org/crocker.html)
<!-- Image -->
![email](https://raw.githubusercontent.com/pyrustic/misc/master/media/email.png)
