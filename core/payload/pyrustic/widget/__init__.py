import tkinter.font as tkfont

def charsize(char="m", family="Colibri", size="14", weight="bold"):
    font = tkfont.Font(family=family, size=size, weight=weight)
    return font.measure(char)


def grid(parent, child, cnf={}, **kwargs):
    child.grid(cnf=cnf, in_=parent, **kwargs)


def pack(parent, child, cnf={}, **kwargs):
    child.pack(cnf=cnf, in_=parent, **kwargs)


def place(parent, child, cnf={}, **kwargs):
    child.pack(cnf=cnf, in_=parent, **kwargs)


def clean(parent):
    for child in parent.winfo_children():
        child.destroy()

def merge(options={}, **kwargs):
    # options have higher priority.
    # Kwargs will be added in options if the key doesn't exist yet in options
    for key, value in kwargs.items():
        if key in options:
            continue
        options[key] = value
    return options


if __name__ == "__main__":
    options = {"background": "red", "foreground" : "yellow"}
    results = merge(options, foreground="black", cursor="blue")
    print(results)