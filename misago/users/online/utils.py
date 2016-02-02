from datetime import timedelta

from django.utils import timezone

from misago.users.bans import get_user_ban
from misago.users.models import Online


ACTIVITY_CUTOFF = timedelta(minutes=15)


def get_user_status(user, acl):
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
        if not user.is_hiding_presence or acl['can_see_hidden_users']:
            online_tracker = user.online_tracker
            if online_tracker.last_click >= timezone.now() - ACTIVITY_CUTOFF:
                user_status['is_online'] = True
                user_status['last_click'] = online_tracker.last_click
    except Online.DoesNotExist:
        pass

    if user_status['is_hidden']:
        if acl['can_see_hidden_users']:
            if user_status['is_online']:
                user_status['is_online_hidden'] = True
            else:
                user_status['is_offline_hidden'] = True
        else:
            user_status['is_hidden'] = True
    else:
        if user_status['is_online']:
            user_status['is_online'] = True
        else:
            user_status['is_offline'] = True

    return user_status
