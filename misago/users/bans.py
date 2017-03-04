"""
API for checking values for bans

Calling this instead of Ban.objects.find_ban is preffered, if you don't want
to use validate_X_banned validators
"""
from datetime import timedelta

from django.utils import timezone
from django.utils.dateparse import parse_datetime

from misago.core import cachebuster

from .models import Ban, BanCache


CACHE_SESSION_KEY = 'misago_ip_check'
VERSION_KEY = 'misago_bans'


def get_username_ban(username, registration_only=False):
    try:
        return Ban.objects.get_username_ban(username, registration_only)
    except Ban.DoesNotExist:
        return None


def get_email_ban(email, registration_only=False):
    try:
        return Ban.objects.get_email_ban(email, registration_only)
    except Ban.DoesNotExist:
        return None


def get_ip_ban(ip, registration_only=False):
    try:
        return Ban.objects.get_ip_ban(ip, registration_only)
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
    ban_cache.bans_version = cachebuster.get_version(VERSION_KEY)

    try:
        user_ban = Ban.objects.get_ban(username=user.username, email=user.email)

        ban_cache.ban = user_ban
        ban_cache.expires_on = user_ban.expires_on
        ban_cache.user_message = user_ban.user_message
        ban_cache.staff_message = user_ban.staff_message
    except Ban.DoesNotExist:
        ban_cache.ban = None
        ban_cache.expires_on = None
        ban_cache.user_message = None
        ban_cache.staff_message = None

    ban_cache.save()
    return ban_cache


def get_request_ip_ban(request):
    """
    Utility for checking if request came from banned IP

    This check may be performed frequently, which is why there is extra
    boilerplate that caches ban check result in session
    """
    session_ban_cache = _get_session_bancache(request)
    if session_ban_cache:
        if session_ban_cache['is_banned']:
            return session_ban_cache
        else:
            return False

    found_ban = get_ip_ban(request.user_ip)

    ban_cache = request.session[CACHE_SESSION_KEY] = {
        'version': cachebuster.get_version(VERSION_KEY),
        'ip': request.user_ip,
    }

    if found_ban:
        if found_ban.expires_on:
            ban_cache['expires_on'] = found_ban.expires_on.isoformat()
        else:
            ban_cache['expires_on'] = None

        ban_cache.update({'is_banned': True, 'message': found_ban.user_message})
        request.session[CACHE_SESSION_KEY] = ban_cache
        return _hydrate_session_cache(request.session[CACHE_SESSION_KEY])
    else:
        ban_cache['is_banned'] = False
        request.session[CACHE_SESSION_KEY] = ban_cache
        return None


def _get_session_bancache(request):
    try:
        ban_cache = request.session[CACHE_SESSION_KEY]
        ban_cache = _hydrate_session_cache(ban_cache)
        if ban_cache['ip'] != request.user_ip:
            return None
        if not cachebuster.is_valid(VERSION_KEY, ban_cache['version']):
            return None
        if ban_cache.get('expires_on'):
            if ban_cache['expires_on'] < timezone.today():
                return None
        return ban_cache
    except KeyError:
        return None


def _hydrate_session_cache(ban_cache):
    hydrated = ban_cache.copy()

    if hydrated.get('expires_on'):
        hydrated['expires_on'] = parse_datetime(hydrated['expires_on'])

    return hydrated


# Utilities for front-end based bans
def ban_user(user, user_message=None, staff_message=None, length=None, expires_on=None):
    if not expires_on and length:
        expires_on = timezone.now() + timedelta(**length)

    ban = Ban.objects.create(
        banned_value=user.username.lower(),
        user_message=user_message,
        staff_message=staff_message,
        expires_on=expires_on
    )
    Ban.objects.invalidate_cache()
    return ban


def ban_ip(ip, user_message=None, staff_message=None, length=None, expires_on=None):
    if not expires_on and length:
        expires_on = timezone.now() + timedelta(**length)

    ban = Ban.objects.create(
        check_type=Ban.IP,
        banned_value=ip,
        user_message=user_message,
        staff_message=staff_message,
        expires_on=expires_on
    )
    Ban.objects.invalidate_cache()
    return ban
