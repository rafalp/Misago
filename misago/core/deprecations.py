"""
Utility module useful for refactors,

Defines utility function for easy raising of warnings in deprecated functions.

This function is set to use stacklevel 3 as default making following code in test.py:

def depreacted_function():
    warn("This function is deprecated")


def other_function():
    deprecated_function()


Will raise warning about 1st line in other_function calling deprecated function.
"""
import warnings


class RemovedInMisagoWarning(Warning):
    pass


def warn(message, category=RemovedInMisagoWarning, stacklevel=0):
    warnings.warn(message, category, stacklevel + 3)
