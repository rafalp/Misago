from misago.core.cache import cache

from misago.users.models import Rank
from misago.users.online.utils import get_online_queryset


RANKS_CACHE_NAME = 'misago_ranks_online'
RANKS_CACHE_TIME = 3 * 60


def get_ranks_online(viewer):
    viewer_is_listed = viewer.is_authenticated() and viewer.rank.is_on_index

    cached_online = cache.get(RANKS_CACHE_NAME, 'nada')
    if viewer_is_listed and ranks_list_missing_viewer(viewer, cached_online):
        cached_online = 'nada'

    if cached_online == 'nada':
        cached_online = get_ranks_from_db(viewer if viewer_is_listed else None)
        cache.set(RANKS_CACHE_NAME, cached_online, RANKS_CACHE_TIME)

    if not viewer.acl['can_see_hidden_users']:
        return filter_visiblity_preference(viewer, cached_online)
    else:
        return cached_online


def ranks_list_missing_viewer(viewer, online_list):
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


def filter_visiblity_preference(viewer, ranks_online):
    visible_ranks = []
    for rank in ranks_online:
        visible_users = []
        if rank['has_ninjas']:
            for user in rank['online']:
                if viewer.is_authenticated() and user['pk'] == viewer.pk:
                    is_viewer = True
                else:
                    is_viewer = False
                if is_viewer or not user['is_hiding_presence']:
                    visible_users.append(user)
            if visible_users:
                rank['online'] = visible_users
                visible_ranks.append(rank)
        else:
            visible_ranks.append(rank)
    return visible_ranks


def get_ranks_from_db(include_viewer):
    displayed_ranks = []

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
            'has_ninjas': False,
            'online': []
        }
        displayed_ranks.append(ranks_dict[rank.pk])

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

            if tracker.user.is_hiding_presence:
                ranks_dict[tracker.user.rank_id]['has_ninjas'] = True

    if include_viewer and include_viewer.rank_id in ranks_dict:
        viewer_rank = ranks_dict[include_viewer.rank_id]
        if include_viewer.is_hiding_presence:
            viewer_rank['has_ninjas'] = True
        for online in viewer_rank['online']:
            if online['pk'] == include_viewer.pk:
                break
        else:
            viewer_rank['online'].append({
                'id': include_viewer.id,
                'pk': include_viewer.pk,
                'username': include_viewer.username,
                'slug': include_viewer.slug,
                'title': include_viewer.title,
                'is_hiding_presence': include_viewer.is_hiding_presence
            })

    ranks_online = []
    for rank in displayed_ranks:
        if rank['online']:
            ranks_online.append(rank)
    return ranks_online


def clear_ranks_online_cache():
    cache.delete(RANKS_CACHE_NAME)
