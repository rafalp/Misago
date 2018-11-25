from django.utils.crypto import get_random_string


def generate_version_string():
    return get_random_string(8)
