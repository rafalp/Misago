from datetime import datetime

from django.utils import timezone
from misago.core import cachebuster

from misago.users.models import Ban


"""
Utils for checking bans
"""
BAN_CACHE_SESSION_KEY = 'misago_ip_check'
BAN_VERSION_KEY = 'misago_bans'


def is_user_banned(user):
    pass


def is_ip_banned(request):
    session_ban_cache = _get_session_bancache(request)
    if session_ban_cache:
        if session_ban_cache['is_banned']:
            return session_ban_cache
        else:
            return False

    found_ban = Ban.objects.find_ban(ip=request._misago_real_ip)

    ban_cache = request.session[BAN_CACHE_SESSION_KEY] = {
        'version': cachebuster.get_version(BAN_VERSION_KEY),
        'ip': request._misago_real_ip,
    }

    if found_ban:
        if found_ban.valid_until:
            valid_until_as_string = found_ban.valid_until.strftime('%Y-%m-%d')
            ban_cache['valid_until'] = valid_until_as_string
        else:
            ban_cache['valid_until'] = None

        ban_cache.update({
                'is_banned': True,
                'message': found_ban.user_message
            })
        request.session[BAN_CACHE_SESSION_KEY] = ban_cache
        return _hydrate_session_cache(request.session[BAN_CACHE_SESSION_KEY])
    else:
        ban_cache['is_banned'] = False
        request.session[BAN_CACHE_SESSION_KEY] = ban_cache
        return False


def _get_session_bancache(request):
    try:
        ban_cache = request.session[BAN_CACHE_SESSION_KEY]
        ban_cache = _hydrate_session_cache(ban_cache)
        if ban_cache['ip'] != request._misago_real_ip:
            return None
        if not cachebuster.is_valid(BAN_VERSION_KEY, ban_cache['version']):
            return None
        if ban_cache.get('valid_until'):
            """
            Make two timezone unaware dates and compare them
            """
            if ban_cache.get('valid_until') < timezone.now().date():
                return None
        return ban_cache
    except KeyError:
        return None


def _hydrate_session_cache(ban_cache):
    hydrated = ban_cache.copy()

    if hydrated.get('valid_until'):
        expiration_datetime = datetime.strptime(ban_cache.get('valid_until'),
                                                '%Y-%m-%d')
        hydrated['valid_until'] = expiration_datetime.date()

    return hydrated
