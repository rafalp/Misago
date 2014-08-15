from datetime import timedelta

from django.utils import timezone

from misago.core.cache import cache

from misago.users.models import Online, Rank
from misago.users.online.utils import get_online_queryset


RANKS_CACHE_NAME = 'misago_ranks_online'
RANKS_CACHE_TIME = 3 * 60


def get_ranks_online(viewer):
    cached_online = cache.get(RANKS_CACHE_NAME, 'nada')

    if viewer and ranks_list_missing_viewer(viewer, cached_online):
        cached_online = 'nada'

    if cached_online == 'nada':
        cached_online = get_ranks_from_db()
        cache.set(RANKS_CACHE_NAME, cached_online, RANKS_CACHE_TIME)

    if not viewer.acl['can_see_hidden_users']:
        return filter_visiblity_preference(viewer, cached_online)
    else:
        return cached_online


def ranks_list_missing_viewer(viewer, online_list):
    if viewer.is_authenticated() and viewer.rank.is_on_index:
        if online_list != 'nada':
            for rank in online_list:
                if rank['pk'] == viewer.rank_id:
                    for user in rank['online']:
                        if user['id'] == viewer.pk:
                            cache_is_hiding = user['is_hiding_presence']
                            viewer_is_hiding = viewer.is_hiding_presence
                            return cache_is_hiding != viewer_is_hiding
                    else:
                        return True
            else:
                return True
    else:
        return False


def filter_visiblity_preference(viewer, ranks_online):
    visible_ranks = []
    for rank in ranks_online:
        visible_users = []
        for user in rank['online']:
            see_self = viewer.is_authenticated() and user['pk'] == viewer.pk
            if see_self or not user['is_hiding_presence']:
                visible_users.append(user)
        if visible_users:
            rank['online'] = visible_users
            visible_ranks.append(rank)
    return visible_ranks


def get_ranks_from_db():
    _displayed_ranks = []

    ranks_dict = {}
    for rank in Rank.objects.filter(is_on_index=True).order_by('order'):
        ranks_dict[rank.pk] = {
            'id': rank.id,
            'pk': rank.pk,
            'name': rank.name,
            'slug': rank.slug,
            'description': rank.description,
            'title': rank.title,
            'css_class': rank.css_class,
            'online': []
        }
        _displayed_ranks.append(ranks_dict[rank.pk])

    queryset = get_online_queryset().filter(is_visible_on_index=True)
    for tracker in queryset.iterator():
        if tracker.user.rank_id in ranks_dict:
            ranks_dict[tracker.user.rank_id]['online'].append({
                'id': tracker.user.id,
                'pk': tracker.user.pk,
                'username': tracker.user.username,
                'slug': tracker.user.slug,
                'title': tracker.user.title,
                'is_hiding_presence': tracker.user.is_hiding_presence
            })

    ranks_online = []
    for rank in _displayed_ranks:
        if rank['online']:
            ranks_online.append(rank)
    return ranks_online


def clear_ranks_online_cache():
    cache.delete(RANKS_CACHE_NAME)
