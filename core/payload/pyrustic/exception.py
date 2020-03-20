"""
Pyrustic exceptions
"""


class PyrusticException(Exception):
    pass


class PyrusticWidgetException(PyrusticException):
    pass


class PyrusticTableException(PyrusticWidgetException):
    pass
