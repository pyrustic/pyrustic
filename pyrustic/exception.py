"""
Pyrustic exceptions
"""


class PyrusticException(Exception):
    pass

class PyrusticAppException(PyrusticException):
    pass


class PyrusticWidgetException(PyrusticException):
    pass


class PyrusticTableException(PyrusticWidgetException):
    pass
