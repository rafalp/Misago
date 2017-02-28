from datetime import timedelta

from django.utils import timezone

from misago.users.bans import get_user_ban
from misago.users.models import BanCache, Online


ACTIVITY_CUTOFF = timedelta(minutes=2)


def get_user_status(viewer, user):
    user_status = {
        'is_banned': False,
        'is_hidden': user.is_hiding_presence,
        'is_online_hidden': False,
        'is_offline_hidden': False,
        'is_online': False,
        'is_offline': False,
        'banned_until': None,
        'last_click': user.last_login or user.joined_on,
    }

    user_ban = get_user_ban(user)
    if user_ban:
        user_status['is_banned'] = True
        user_status['banned_until'] = user_ban.expires_on

    try:
        online_tracker = user.online_tracker
        is_hidden = user.is_hiding_presence and not viewer.acl_cache['can_see_hidden_users']

        if online_tracker and not is_hidden:
            if online_tracker.last_click >= timezone.now() - ACTIVITY_CUTOFF:
                user_status['is_online'] = True
                user_status['last_click'] = online_tracker.last_click
    except Online.DoesNotExist:
        pass

    if user_status['is_hidden']:
        if viewer.acl_cache['can_see_hidden_users']:
            user_status['is_hidden'] = False
            if user_status['is_online']:
                user_status['is_online_hidden'] = True
                user_status['is_online'] = False
            else:
                user_status['is_offline_hidden'] = True
                user_status['is_offline'] = False
        else:
            user_status['is_hidden'] = True
    else:
        if user_status['is_online']:
            user_status['is_online'] = True
        else:
            user_status['is_offline'] = True

    return user_status


def make_users_status_aware(viewer, users, fetch_state=False):
    users_dict = {}
    for user in users:
        users_dict[user.pk] = user

    if fetch_state:
        # Fill ban cache on users
        for ban_cache in BanCache.objects.filter(user__in=users_dict.keys()):
            users_dict[ban_cache.user_id].ban_cache = ban_cache

        # Fill user online trackers
        for online_tracker in Online.objects.filter(user__in=users_dict.keys()):
            users_dict[online_tracker.user_id].online_tracker = online_tracker

    # Fill user states
    for user in users:
        user.status = get_user_status(viewer, user)
