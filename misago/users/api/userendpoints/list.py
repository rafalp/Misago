from datetime import timedelta

from django.contrib.auth import get_user_model
from django.db.models import Count
from django.utils import timezone

from rest_framework.pagination import PageNumberPagination

from misago.conf import settings
from misago.core.cache import cache
from misago.core.shortcuts import get_object_or_404
from misago.forums.models import Forum

from misago.users.online.utils import get_online_queryset
from misago.users.permissions.profiles import allow_see_users_online_list
from misago.users.models import Rank
from misago.users.serializers import OnlineUserSerializer, ScoredUserSerializer


def active(request, queryset):
    cache_key = 'misago_active_posters_ranking'
    ranking = cache.get(cache_key, False)
    if ranking is False:
        ranking = real_active()
        cache.set(cache_key, ranking, 18*3600)
    return ranking


def real_active():
    tracked_period = settings.MISAGO_RANKING_LENGTH
    tracked_since = timezone.now() - timedelta(days=tracked_period)

    ranked_forums = [forum.pk for forum in Forum.objects.all_forums()]

    User = get_user_model()
    queryset = User.objects.filter(posts__gt=0)
    queryset = queryset.filter(post__posted_on__gte=tracked_since,
                               post__forum__in=ranked_forums)
    queryset = queryset.annotate(num_posts=Count('post'))
    queryset = queryset.select_related('user__rank')
    queryset = queryset.order_by('-num_posts', 'slug')

    users_ranking = []
    for result in queryset[:settings.MISAGO_RANKING_SIZE]:
        result.score = result.num_posts
        users_ranking.append(result)
    return {'data': ScoredUserSerializer(users_ranking, many=True).data}


def online(request, queryset):
    allow_see_users_online_list(request.user)

    cache_key = 'users_online_cache_%s' % request.user.acl_key
    online_list = cache.get(cache_key, False)
    if online_list is False:
        online_list = real_online(request)
        cache.set(cache_key, online_list, settings.MISAGO_ONLINE_LIST_CACHE)
    return online_list


def real_online(request):
    queryset = get_online_queryset(request.user).order_by('last_click')
    queryset = queryset[:settings.MISAGO_ONLINE_LIST_SIZE]

    users_online = []
    for result in queryset:
        result.user.last_click = result.last_click
        users_online.append(result.user)

    return {'data': OnlineUserSerializer(users_online, many=True).data}


def rank(request, queryset):
    rank_slug = request.query_params.get('rank')
    if not rank_slug:
        return

    rank = get_object_or_404(Rank.objects.filter(is_tab=True), slug=rank_slug)
    queryset = queryset.filter(rank=rank).order_by('slug')

    return {'queryset': queryset, 'paginate': True}


LISTS = {
    'active': active,
    'online': online,
    'rank': rank,
}


def list_endpoint(request, queryset):
    list_type = request.query_params.get('list')
    list_handler = LISTS.get(list_type)

    if list_handler:
        return list_handler(request, queryset)
    else:
        return
