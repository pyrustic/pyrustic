[Home](https://github.com/pyrustic/pyrustic#readme) | [Tutorial](https://github.com/pyrustic/pyrustic/blob/master/docs/tutorial/README.md) | [Guide](https://github.com/pyrustic/pyrustic/blob/master/docs/guide/README.md) | [Reference](https://github.com/pyrustic/pyrustic/blob/master/docs/reference/README.md) | [Website](https://pyrustic.github.io)

## Manage a project

This is an overview of available commands in `Project Manager`. You can learn more about any command with `help <command>`.

- `link`: Link your `Target project` to the Project Manager.
- `unlink`: Use this command to unlink the currently linked Target.
- `relink`: Link again the previously linked Target or one of
    recent linked Targets.
- `recent`: List of recent Targets.
- `target`: Use this command to check the currently linked Target.
- `init`: Use this command to initialize your project.
- `run`: Use this command to run a module.
- `add`: Use this command to add an empty file, a package or a regular
    folder to the Target.
- `build`: Use this command to build a distribution package
    that could be published later with the 'publish'
    command.
- `publish`: Use this command to publish the latest distribution
    package previously built with the command 'build'.
- `hub`: Use this command to retrieve useful information
    from a Github repository.
- `help`: List available commands with "help" or detailed help with "help cmd".
- `exit`: This command closes the program graciously.

You can issue these commands programmatically via the function `pyrustic.manager.oneline.command`.

```python
from pyrustic.manager.oneline import command

# build the demo project
command(line="build", target="/home/alex/demo")
```

The `Project Manager` exposes an `API` in the module `pyrustic.manager` (technically in `__init__.py` located in the package `pyrustic.manager`).

```python
from pyrustic import manager

# build the demo project
target = "/home/alex/demo"
app_pkg = manager.get_app_pkg(target)  # returns 'demo'
manager.build(target, app_pkg)
```

Read more about the `API` and `pyrustic.manager.oneline.command` in the [reference](https://github.com/pyrustic/pyrustic/blob/master/docs/reference/README.md).
