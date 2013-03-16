from django.template.defaultfilters import slugify
from django.utils import crypto
try:
    from unidecode import unidecode
    use_unidecode = True
except ImportError:
    use_unidecode = False

def slugify(string):
    if use_unidecode:
        string = unidecode(string)
    return django.template.defaultfilters.slugify(string)


def random_string(length):
    return crypto.get_random_string(length, "1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM")
