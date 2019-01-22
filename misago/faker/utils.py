from django.db import IntegrityError


def retry_on_db_error(f):
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except IntegrityError:
            return wrapper(*args, **kwargs)

    return wrapper
