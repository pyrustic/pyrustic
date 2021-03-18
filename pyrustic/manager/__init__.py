from pyrustic import pymisc
from pyrustic.manager.main import main


__all__ = ["command"]


def command(line=None, target=None):
    """
    Param:
        - line is a string
        - target is a string
    """
    print("EXECUTION")
    args = None
    if line is not None:
        args = pymisc.parse_cmd(line)
    main(argv=args, target=target)
