[Home](https://github.com/pyrustic/pyrustic#readme) | [Tutorial](https://github.com/pyrustic/pyrustic/blob/master/docs/tutorial/README.md) | [Guide](https://github.com/pyrustic/pyrustic/blob/master/docs/guide/README.md) | [Reference](https://github.com/pyrustic/pyrustic/blob/master/docs/reference/README.md) | [Website](https://pyrustic.github.io)

# Start a project

Once you have [installed](https://github.com/pyrustic/pyrustic#installation) `Pyrustic Framework`, you can start a project via the command line tool `Project Manager`.

```bash
$ pyrustic
Pyrustic Project Manager
Version: 0.1.6
Type "help" or "?" to list commands. Type "exit" to leave.

(pyrustic) 

```

### Step 1: Link the project directory

Link the project to `Project Manager` by indicating the path of the project folder. This could be a relative path or even a dot to indicate the current working directory.

If you don't submit a path, a file-chooser dialog will open.

```bash
(pyrustic) link /home/alex/demo

Successfully linked !
[demo] /home/alex/demo

Not yet initialized project (check 'help init')

```
From now on, the project linked to `Project Manager` will be called the `Target`. You can issue the `target` command to see the currently linked project.

```bash
(pyrustic) target

[demo] /home/alex/demo
Not yet initialized project (check 'help init')
```

### Step 2: Initialize the project directory

Now you can initialize your project with the command `init`. Initializing the project will simply create a basic [project structure](https://github.com/pyrustic/pyrustic/blob/master/docs/guide/content/project-structure.md).

```bash
(pyrustic) init

Successfully initialized !
```
You can then run the project with the command `run`.

If you quit `Project Manager`, the next time you want to link the same project, run the `relink` command or use the `recent` command.



### One line command
You can initialize a project with just 1 step:
```bash
$ pyrustic init
```

`Project Manager` will assume that the `target` is the current working directory.