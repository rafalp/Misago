from datetime import timedelta

from django.utils import timezone

from misago.core.cache import cache

from misago.users.models import Online, Rank
from misago.users.online.utils import get_online_queryset


RANKS_CACHE_NAME = 'misago_ranks_online'
RANKS_CACHE_TIME = 3 * 60


def get_ranks_online():
    cached_online = cache.get(RANKS_CACHE_NAME, 'nada')
    if cached_online == 'nada':
        cached_online = get_ranks_from_db()
        cache.set(RANKS_CACHE_NAME, cached_online, RANKS_CACHE_TIME)
        return cached_online
    else:
        return cached_online


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
            })

    ranks_online = []
    for rank in _displayed_ranks:
        if rank['online']:
            ranks_online.append(rank)
    return ranks_online


def clear_ranks_online_cache():
    cache.delete(RANKS_CACHE_NAME)
