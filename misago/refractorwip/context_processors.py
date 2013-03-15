from django.conf import settings
from misago import get_version

# Register context processors
def core(request):
    return {
        'request_path': request.get_full_path(),
        'board_address': settings.BOARD_ADDRESS,
        'version': get_version(),
    }
