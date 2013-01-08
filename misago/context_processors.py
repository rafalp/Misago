from django.conf import settings
from misago import get_version

# Register context processors
def core(request):
    return {
        'board_address': settings.BOARD_ADDRESS,
        'version': get_version(),
    }
