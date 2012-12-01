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


"""
Date formats
"""    
from django.conf import settings
from django.utils.importlib import import_module
from misago import get_version

try:
    locale_formats = import_module('django.conf.locale.%s.formats' % settings.LANGUAGE_CODE)
    formats = {
               'DATE_FORMAT': locale_formats.DATE_FORMAT,
               'TIME_FORMAT': locale_formats.TIME_FORMAT,
               'DATETIME_FORMAT': locale_formats.DATETIME_FORMAT,
               'SHORT_DATE_FORMAT': locale_formats.SHORT_DATE_FORMAT,
               'SHORT_DATETIME_FORMAT': locale_formats.SHORT_DATETIME_FORMAT,
               }
except (ImportError, AttributeError):
    formats = {
               'DATE_FORMAT': settings.DATE_FORMAT,
               'TIME_FORMAT': settings.TIME_FORMAT,
               'DATETIME_FORMAT': settings.DATETIME_FORMAT,
               'SHORT_DATE_FORMAT': settings.SHORT_DATE_FORMAT,
               'SHORT_DATETIME_FORMAT': settings.SHORT_DATETIME_FORMAT,
               }

formats['DATE_FORMAT'] = unicode(formats['DATE_FORMAT'].replace('P', 'g:i a'))
formats['TIME_FORMAT'] = unicode(formats['TIME_FORMAT'].replace('P', 'g:i a'))
formats['DATETIME_FORMAT'] = unicode(formats['DATETIME_FORMAT'].replace('P', 'g:i a'))
formats['SHORT_DATE_FORMAT'] = unicode(formats['SHORT_DATE_FORMAT'].replace('P', 'g:i a'))
formats['SHORT_DATETIME_FORMAT'] = unicode(formats['SHORT_DATETIME_FORMAT'].replace('P', 'g:i a'))