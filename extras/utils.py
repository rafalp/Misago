import tokenize

from django.utils import six


def generate_tokens(filesource):
    return list(tokenize.generate_tokens(six.StringIO(filesource).readline))
