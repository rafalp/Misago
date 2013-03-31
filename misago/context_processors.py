from django.conf import settings
from misago import __version__
from misago.admin import site
from misago.models import Forum

def common(request):
    try:
        context = {
            'acl': request.acl,
            'board_address': settings.BOARD_ADDRESS,
            'messages' : request.messages.messages,
            'monitor': request.monitor,
            'request_path': request.get_full_path(),
            'settings': request.settings,
            'stopwatch': request.stopwatch.time(),
            'user': request.user,
            'version': __version__,
        }
        context.update({
            'csrf_id': request.csrf.csrf_id,
            'csrf_token': request.csrf.csrf_token,
            'is_banned': request.ban.is_banned(),
            'is_jammed': request.jam.is_jammed(),
            'private_threads': Forum.objects.special_model('private_threads'),
            'reports': Forum.objects.special_model('reports'),
        })
    except AttributeError as e:
        pass
    return context


def admin(request):
    return site.get_admin_navigation(request)