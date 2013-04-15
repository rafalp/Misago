from django.template.defaultfilters import slugify as django_slugify
from django.utils import crypto
try:
    from unidecode import unidecode
    use_unidecode = True
except ImportError:
    use_unidecode = False

def slugify(string):
    string = unicode(string)
    if use_unidecode:
        string = unidecode(string)
    return django_slugify(string)


def random_string(length):
    return crypto.get_random_string(length, "1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM")


def short_string(string, length=16):
    if len(string) <= length:
        return string;
    length -= 3
    string = string[0:length]
    bits = string.split()
    if len(bits[-1]) > length:
        bits[-1] = bits[-1][0:length]
    if len(bits[-1]) < 3:
        bits.pop()
    return '%s...' % (' '.join(bits))

def html_escape(html):
    html = html.replace('&', '&amp;')
    html = html.replace('<', '&lt;')
    html = html.replace('>', '&gt;')
    return html.replace('"', '&quot;')