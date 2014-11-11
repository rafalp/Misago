
"""
API for testing values for bans

Calling this instead of Ban.objects.find_ban is preffered, if you don't want
to use validate_X_banned validators
"""
from datetime import date, datetime, timedelta

from django.utils import timezone

from misago.core import cachebuster
from misago.users.models import BAN_IP, Ban, BanCache


BAN_CACHE_SESSION_KEY = 'misago_ip_check'
BAN_VERSION_KEY = 'misago_bans'


def get_username_ban(username):
    try:
        return Ban.objects.find_ban(username=username)
    except Ban.DoesNotExist:
        return None


def get_email_ban(email):
    try:
        return Ban.objects.find_ban(email=email)
    except Ban.DoesNotExist:
        return None


def get_ip_ban(ip):
    try:
        return Ban.objects.find_ban(ip=ip)
    except Ban.DoesNotExist:
        return None


def get_user_ban(user):
    """
    This function checks if user is banned

    When user model is available, this is preffered to calling
    get_email_ban(user.email) and get_username_ban(user.username)
    because it sets ban cache on user model
    """
    try:
        ban_cache = user.ban_cache
        if not ban_cache.is_valid:
            _set_user_ban_cache(user)
    except BanCache.DoesNotExist:
        user.ban_cache = BanCache(user=user)
        user.ban_cache = _set_user_ban_cache(user)

    if user.ban_cache.ban:
        return user.ban_cache
    else:
        return None


def _set_user_ban_cache(user):
    ban_cache = user.ban_cache
    ban_cache.bans_version = cachebuster.get_version(BAN_VERSION_KEY)

    try:
        user_ban = Ban.objects.find_ban(username=user.username,
                                        email=user.email)
        ban_cache.ban = user_ban
        ban_cache.valid_until = user_ban.valid_until
        ban_cache.user_message = user_ban.user_message
        ban_cache.staff_message = user_ban.staff_message
    except Ban.DoesNotExist:
        ban_cache.ban = None
        ban_cache.valid_until = None
        ban_cache.user_message = None
        ban_cache.staff_message = None

    ban_cache.save()
    return ban_cache


"""
Utility for checking if request came from banned IP

This check may be performed frequently, which is why there is extra
boilerplate that caches ban check result in session
"""
def get_request_ip_ban(request):
    session_ban_cache = _get_session_bancache(request)
    if session_ban_cache:
        if session_ban_cache['is_banned']:
            return session_ban_cache
        else:
            return False

    found_ban = get_ip_ban(request._misago_real_ip)

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
        return None


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
            if ban_cache.get('valid_until') < date.today():
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


"""
Utility for banning naughty IPs
"""
def ban_ip(ip, user_message=None, staff_message=None, length=None):
    if length:
        valid_until = (timezone.now() + timedelta(days=length)).date()
    else:
        valid_until = None

    Ban.objects.create(
        test=BAN_IP,
        banned_value=ip,
        user_message=user_message,
        staff_message=staff_message,
        valid_until=valid_until
    )
    Ban.objects.invalidate_cache()
