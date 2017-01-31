from unidecode import unidecode

from django.template.defaultfilters import slugify as django_slugify
from django.utils import six


def default(string):
    string = six.text_type(string)
    string = unidecode(string)
    return django_slugify(string.replace('_', ' ').strip())
