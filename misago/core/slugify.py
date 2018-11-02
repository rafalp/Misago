from unidecode import unidecode

from django.template.defaultfilters import slugify as django_slugify


def default(string):
    string = str(string)
    string = unidecode(string)
    return django_slugify(string.replace('_', ' ').strip())
