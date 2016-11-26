import warnings


class RemovedInMisagoWarning(Warning):
    pass


def warn(message, category=RemovedInMisagoWarning, stacklevel=0):
    warnings.warn(message, category, stacklevel + 3)
