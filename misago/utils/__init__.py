"""
Smart slugify
"""
import django.template.defaultfilters
use_unidecode = True
try:
    from unidecode import unidecode
except ImportError:
    use_unidecode = False
    
def slugify(string):
    if use_unidecode:
        string = unidecode(string)
    return django.template.defaultfilters.slugify(string)

"""
Lazy translate that allows us to access original message
"""
from django.utils import translation
def ugettext_lazy(str):
    t = translation.ugettext_lazy(str)
    t.message = str
    return t
def get_msgid(gettext):
    try:
        return gettext.message
    except AttributeError:
        return None