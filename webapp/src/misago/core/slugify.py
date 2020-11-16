from django.template.defaultfilters import slugify as django_slugify
from unidecode import unidecode


def default(string):
    string = str(string)
    string = unidecode(string)
    return django_slugify(string.replace("_", " ").strip())
