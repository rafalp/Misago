from django.conf import settings
from django.utils.importlib import import_module
from misago import get_version

# Get formats
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

# Register context processors
def core(request):
    return {
        'board_address': settings.BOARD_ADDRESS,
        'version': get_version(),
        'f': formats
    }