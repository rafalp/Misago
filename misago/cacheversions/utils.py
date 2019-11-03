from ..utils.strings import get_random_string


def generate_version_string() -> str:
    return get_random_string(8)
