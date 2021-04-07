Welcome to this short and fun tutorial ! I will show you how easy Python GUI development could be.

Take a look at the following image:


<!-- Image -->
<div align="center">
    <img src="https://raw.githubusercontent.com/pyrustic/misc/master/media/tutorial-1-figure-1.png" alt="Figure 1" width="650">
    <p align="center">
    <b> Figure 1 - Demo GUI with the cyberpunk theme </b>
    </p>
</div>


At the end of the reading, you will be able to reproduce the graphical user interface (GUI) of `Figure 1`. It was built with Tkinter and Pyrustic.

Tkinter is Python's default GUI toolkit. Pyrustic is a lightweight framework to develop, package, and publish Python desktop applications .

In the following image, I will schematically reproduce the graphical interface of figure 1.


<!-- Image -->
<div align="center">
    <img src="https://raw.githubusercontent.com/pyrustic/misc/master/media/tutorial-1-figure-2.png" alt="Figure 2" width="850">
    <p align="center">
    <b> Figure 2 - Layout sketch </b>
    </p>
</div>


The elements inside the window in `Figure 2` are called _Widgets_:
- _Frame_: container widget to contain other widgets;
- _Text_: this widget is used to display editable multiline text;
- _Entry_: this widget is an editable entry field;
- _Button_: this widget is a clickable button.

Here's what it takes to build a window:

```python
import tkinter as tk

root = tk.Tk()  # instantiation of the root (basically, it's the window)
root.mainloop()  # the window will close when this loop stops !
```

To add a button to this window:

```python
import tkinter as tk

root = tk.Tk()  # you create the root first before any other widget
button = tk.Button(master=root, text="Hello")  # create a button
button.pack()  # actually install the button on the parent (root)
root.mainloop()  # don't add any widget after this line
```

Each widget has options which can be changed after instantiation. For example, the Button widget has a `text` option that allows you to define the text to be displayed on the button. All widgets have a `master` option which allows you to indicate the parent widget. In the preceding code, the button's parent is the root window.

The options are filled in as arguments when instantiating the widget. To modify the options of a widget, call the `config` method of the widget. The `cget` method allows you to retrieve the value of an option. The following code snippet summarizes it:

```python
import tkinter as tk

root = tk.Tk()
button = tk.Button(master=root, text="Hello", background="pink")
button.pack()

# Modify the value of the options "text" and "background"
button.config(text="Defaced", background="blue")

# Print the new values
text_value = button.cget("text")
background_value = button.cget("background")
print("Text value: ", text_value)
print("Background value: ", background_value)

root.mainloop()
```

To know the list of options of a widget, call the `config` method of the widget without any arguments. This method returns a `dict` with useful information:

```python
import tkinter as tk

root = tk.Tk()
button = tk.Button(master=root, text="Hello")
button.pack()

# Get the options dict AKA config dict
config_dict = button.config()
# Show the names of the options available for the Button widget
for option in config_dict.keys():
    print(option)

root.mainloop()
```

Now let's talk about installing a widget on its parent. There are three geometry managers to install widgets:
- `pack`: pack widgets around edges of cavity;
- `grid`: arrange widgets in a grid;
- `place`: place a widget according to x, y coordinates.

Voilà ! We know enough to build the user interface in `Figure 1` !

```python
import tkinter as tk


def get_main_view(root):
    # the body of this view
    body = tk.Frame(root)
    # the Label 'Welcome'
    label = tk.Label(body, text="Welcome")
    label.pack(anchor="w")  # anchor the label to 'west' side
    # the Text widget
    text = tk.Text(body, width=70, height=20)
    text.pack()
    # the footer Frame
    footer = tk.Frame(body)
    footer.pack(fill=tk.X)  # stretch the footer horizontally to fill the width
    # the Entry widget
    entry = tk.Entry(footer, width=20)
    entry.pack(side=tk.LEFT)  # stick the Entry to the left side of the footer
    # the Button 'Run'
    button_run = tk.Button(footer, text="Run")
    button_run.pack(side=tk.LEFT)
    # the Button 'Exit'
    button_exit = tk.Button(footer, text="Exit")
    button_exit.pack(side=tk.RIGHT) #  stick the button to the right side of the footer
    # return the body object
    return body


# The main window
root = tk.Tk()
# Set the window's title
root.title("Demo application")
# install the main_view
main_view = get_main_view(root)
main_view.pack()
# the main loop
root.mainloop()
```


<!-- Image -->
<div align="center">
    <img src="https://raw.githubusercontent.com/pyrustic/misc/master/media/tutorial-1-figure-3.png" alt="Figure 3" width="650">
    <p align="center">
    <b> Figure 3 - Demo GUI without any theme </b>
    </p>
</div>



The GUI in `Figure 3` has no theme. We are going to use the cyberpunk theme available on PyPI to make the interface look pretty.

Install the cyberpunk theme:

```bash
pip install tk-cyberpunk-theme
```

Theme usage:

```python
import tkinter as tk
from tk_cyberpunk_theme.main import Cyberpunk


root = tk.Tk()

# set the cyberpunk theme
cyberpunk_theme = Cyberpunk()
cyberpunk_theme.target(root)

# install widgets from here
# ...

root.mainloop()
```

Updated GUI snippet code to look like `Figure 1`:

```python
import tkinter as tk
from tk_cyberpunk_theme.main import Cyberpunk


def main_view(root):
    # the body of the view
    body = tk.Frame(root)
    # the Label 'Welcome'
    label = tk.Label(body, text="Welcome")
    label.pack(anchor="w", padx=2, pady=2)
    # the Text widget
    text = tk.Text(body, width=70, height=20)
    text.pack(padx=2, pady=2)
    # the footer Frame
    footer = tk.Frame(body)
    footer.pack(fill=tk.X, padx=2, pady=2)
    # the Entry widget
    entry = tk.Entry(footer, width=20)
    entry.pack(side=tk.LEFT)
    # the Button 'Run'
    button_run = tk.Button(footer, text="Run")
    button_run.pack(side=tk.LEFT, padx=(2, 0))
    # the Button 'Exit'
    button_exit = tk.Button(footer, text="Exit")
    button_exit.pack(side=tk.RIGHT)
    # return the body object
    return body


# The main window
root = tk.Tk()
# Set the window's title
root.title("Demo application")
# Set the cyberpunk theme
cyberpunk_theme = Cyberpunk()
cyberpunk_theme.target(root)
# install the main_view
main_view = main_view(root)
main_view.pack()
# the main loop
root.mainloop()
```


So much for this first part of the tutorial ! In the next part, we will use the Pyrustic framework and take it to the next level.

[Home](https://github.com/pyrustic/pyrustic/blob/master/docs/tutorial/README.md) | [Next >](https://github.com/pyrustic/pyrustic/blob/master/docs/tutorial/tutorial-2.md)

Join the [Discord](https://discord.gg/fSZ6nxzVd6) !

Learn [Tkinter](https://github.com/pyrustic/pyrustic#introduction-to-tkinter) | Learn [Python](https://github.com/pyrustic/pyrustic#introduction-to-python) | Discover [Pyrustic](https://github.com/pyrustic/pyrustic#readme)
