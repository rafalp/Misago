from django.db import IntegrityError
from django.db.transaction import TransactionManagementError


def retry_on_db_error(f):
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except (IntegrityError, TransactionManagementError):
            return wrapper(*args, **kwargs)

    return wrapper
