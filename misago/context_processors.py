from django.conf import settings
from misago import __version__
from misago.admin import ADMIN_PATH, site

def common(request):
    try:
        return {
            'acl': request.acl,
            'ADMIN_PATH': ADMIN_PATH,
            'board_address': settings.BOARD_ADDRESS,
            'csrf_id': request.csrf.csrf_id,
            'csrf_token': request.csrf.csrf_token,
            'is_banned': request.ban.is_banned(),
            'is_jammed': request.jam.is_jammed(),
            'messages' : request.messages.messages,
            'monitor': request.monitor,
            'request_path': request.get_full_path(),
            'settings': request.settings,
            'stopwatch': request.stopwatch.time(),
            'user': request.user,
            'version': __version__,
        }
    except AttributeError:
        # If request lacks required service, let template crash in context processor's stead
        return  {}


def admin(request):
    return site.get_admin_navigation(request)