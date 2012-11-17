from django.conf import settings
from misago import get_version

# Register context processors
def core(request):
    return {
        'board_address': settings.BOARD_ADDRESS,
        'version': get_version(),
        'f': {
                    'DATE_FORMAT': settings.DATE_FORMAT,
                    'TIME_FORMAT': settings.TIME_FORMAT,
                    'DATETIME_FORMAT': settings.DATETIME_FORMAT,
                    'SHORT_DATETIME_FORMAT': settings.SHORT_DATETIME_FORMAT,
                    }
    }