from django.utils.crypto import get_random_string


def get_random_version():
    return get_random_string(8)
