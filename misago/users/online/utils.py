from datetime import timedelta

from django.utils import timezone

from misago.users.bans import get_user_ban
from misago.users.models import Online


ACTIVITY_CUTOFF = timedelta(minutes=15)


def get_online_queryset(viewer=None):
    min_last_click = timezone.now() - ACTIVITY_CUTOFF
    queryset = Online.objects.filter(last_click__gte=min_last_click)

    if viewer and not viewer.acl['can_see_hidden_users']:
        queryset = queryset.filter(user__is_hiding_presence=False)

    return queryset.select_related('user')


def get_user_state(user, acl):
    user_state = {
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
        user_state['is_banned'] = True
        user_state['banned_until'] = user_ban.expires_on

        ban_expiration_date = user_ban.formatted_expiration_date
        user_state['formatted_ban_expiration_date'] = ban_expiration_date

    try:
        if not user.is_hiding_presence or acl['can_see_hidden_users']:
            online_tracker = user.online_tracker
            if online_tracker.last_click >= timezone.now() - ACTIVITY_CUTOFF:
                user_state['is_online'] = True
                user_state['last_click'] = online_tracker.last_click
    except Online.DoesNotExist:
        pass

    if user_state['is_hidden']:
        if acl['can_see_hidden_users']:
            if user_state['is_online']:
                user_state['is_online_hidden'] = True
            else:
                user_state['is_offline_hidden'] = True
        else:
            user_state['is_hidden'] = True
    else:
        if user_state['is_online']:
            user_state['is_online'] = True
        else:
            user_state['is_offline'] = True

    return user_state
