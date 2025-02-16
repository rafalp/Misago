from functools import wraps
from time import sleep

from django.db import IntegrityError
from django.db.transaction import TransactionManagementError


def retry_on_db_error(f):
    @wraps(f)
    def wrapped_fake_function(*args, **kwargs):
        while True:
            try:
                return f(*args, **kwargs)
            except (IntegrityError, TransactionManagementError):
                sleep(0.2)

    return wrapped_fake_function
