from pyrustic import PROJECTS

TEXT = """
Pyrustic Open Ecosystem
=======================

This is a collection of lightweight Python projects that share the same policy.
The goal is to build and maintain a reliable, consistent, easy-to-use 
and relevant Python codebase for tech enthusiasts.

These projects cover various topics: automation, data persistence 
and exchange, GUI, themes, widgets, multithreading, markup, utilities, 
project management, et cetera.

https://pyrustic.github.io

Projects:
=========

"""


def main():
    cache = list()
    for key, value in PROJECTS.items():
        description, link = value
        item = "- {}: {}\n{}".format(key, description, link)
        cache.append(item)
    s = "\n\n".join(cache)
    print(TEXT + s)


if __name__ == "__main__":
    main()
