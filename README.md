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



# Pyrustic Open Ecosystem
**Pyrustic** is a collection of lightweight [Python](https://www.python.org/) projects that share the **same policy**.

The goal is to build and maintain a reliable, consistent, easy-to-use and relevant Python codebase for novice and experienced developers.

These projects cover various topics: data persistence and exchange, GUI, themes, widgets, multithreading, markup, utilities, project management, et cetera. 

## Projects
Projects can be subdivided into the following subsections: frameworks, libraries, themes, command line tools, and apps.

### Frameworks
|Name | Description                                       |
|---|---------------------------------------------------|
|[Gaspium](https://github.com/pyrustic/gaspium) | Reference framework to build `GASP` apps |

> **Note:** Previously, two frameworks were listed: **TkF** and **Gaspium**. Both allow to make desktop applications. **TkF** is now obsolete since **Gaspium** has become the best at this game.

### Libraries

| Name | Description |
| --- | --- |
| [Shared](https://github.com/pyrustic/shared) | Data exchange and persistence |
| [Jesth](https://github.com/pyrustic/backstage) | Just Extract Sections Then Hack ! |
| [Subrun](https://github.com/pyrustic/subrun) | Intuitive API to safely start and communicate with processes in Python |
| [TkStyle](https://github.com/pyrustic/tkstyle) | Library to create styles and themes for Python apps |
| [Litemark](https://github.com/pyrustic/litemark) | Lightweight Markdown dialect for Python apps |
| [Megawidget](https://github.com/pyrustic/megawidget) | Collection of megawidgets to build graphical user interfaces for Python apps |
| [Viewable](https://github.com/pyrustic/viewable) | Python library to implement a GUI view with lifecycle |
| [Threadom](https://github.com/pyrustic/threadom) | Tkinter-compatible multithreading |
| [Suggestion](https://github.com/pyrustic/suggestion) | Democratizing auto-complete(suggest) for Python desktop applications |
| [Kurl](https://github.com/pyrustic/kurl) | Konnection URL: HTTP requests in Python with an implementation of conditional request and a responses caching system |
| [Probed](https://github.com/pyrustic/probed) | Probed collections for Python |

> **Note:** The framework **Gaspium** comes with batteries included. These lightweight libraries listed above are the batteries. 



### Themes
|Name | Description|
|---|---|
|[Cyberpunk-Theme](https://github.com/pyrustic/cyberpunk-theme) | A modern `dark theme` for Python apps|
|[Winter-Theme](https://github.com/pyrustic/winter-theme) | A modern `light theme` for Python apps|

> **Note:** The **cyberpunk-theme** is the default theme used by the framework **Gaspium**. The **winter-theme** will come soon and will be the default theme.

### Command line tools

| Name | Description |
| --- | --- |
| [Backstage](https://github.com/pyrustic/backstage) | Extensible command line tool for managing software projects |
| [Setupinit](https://github.com/pyrustic/buildver) | Initialize Python projects |
| [Buildver](https://github.com/pyrustic/buildver) | Tool to build Python packages with built-in intuitive versioning mechanism |

> **Note:** These command line tools are used to setup and manage all the projects listed on this page.
>
> **Fun fact:** The tool **backstage** is used to release a new version of **backstage**


### Apps
|Name | Description|
|---|---|
|[Codegame](https://github.com/pyrustic/codegame) | Python app to create, distribute, discover, and run `codegames`|
|[Hubstore](https://github.com/pyrustic/hubstore) | Distribute, promote, discover, install, and run Python desktop applications|
|[Jupitest](https://github.com/pyrustic/jupitest) | Graphical test runner|
|[Rustiql](https://github.com/pyrustic/rustiql) | Graphical SQL editor|

> **Note:** The apps listed above may not work as the underlying framework and libraries are under heavy development. 
>
> **These applications will be gradually updated.**


## Installation
### For the first time
Each package listed above can be installed individually from [PyPI](https://pypi.org). You can still install all the packages with just one single command:

```bash
pip install pyrustic
```

### Upgrade
```bash
$ pip install pyrustic --upgrade --upgrade-strategy eager

```
