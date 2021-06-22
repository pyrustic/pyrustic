"""Pyrustic Project Manager entry point"""
from pyrustic.manager.cmdline import Cmdline
from pyrustic.manager import oneline
import sys
import os


def main():
    """
    Pyrustic Project Manager launcher
    Opens the interactive loop if there are not command line arguments
    else starts pyrustic.manager.oneline.command and uses os.getcwd() as target
    """
    argv = sys.argv
    if len(argv) > 1:
        oneline.command(argv[1:], target=os.getcwd())
    else:
        Cmdline().cmdloop()


if __name__ == "__main__":
    main()
