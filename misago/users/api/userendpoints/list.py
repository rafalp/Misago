from datetime import timedelta

from django.contrib.auth import get_user_model
from django.db.models import Count
from django.http import Http404
from django.utils import timezone

from rest_framework.response import Response

from misago.conf import settings
from misago.core.apipaginator import ApiPaginator
from misago.core.cache import cache
from misago.core.shortcuts import get_int_or_404, get_object_or_404

from ...activepostersranking import get_active_posters_ranking
from ...models import Rank
from ...online.utils import make_users_status_aware
from ...serializers import ScoredUserSerializer, UserSerializer


Paginator = ApiPaginator(settings.MISAGO_USERS_PER_PAGE, 4)


def active(request):
    ranking = get_active_posters_ranking()
    make_users_status_aware(request.user, ranking['users'], fetch_state=True)

    return Response({
        'tracked_period': settings.MISAGO_RANKING_LENGTH,
        'results': ScoredUserSerializer(ranking['users'], many=True).data,
        'count': ranking['users_count']
    })


def generic(request):
    allow_name_search = True
    queryset = get_user_model().objects

    if not request.user.is_staff:
        queryset = queryset.filter(is_active=True)

    if request.query_params.get('followers'):
        user_pk = get_int_or_404(request.query_params.get('followers'))
        queryset = get_object_or_404(queryset, pk=user_pk).followed_by
    elif request.query_params.get('follows'):
        user_pk = get_int_or_404(request.query_params.get('follows'))
        queryset = get_object_or_404(queryset, pk=user_pk).follows
    elif request.query_params.get('rank'):
        rank_pk = get_int_or_404(request.query_params.get('rank'))
        rank = get_object_or_404(Rank.objects, pk=rank_pk, is_tab=True)
        queryset = queryset.filter(rank=rank)
        allow_name_search = False
    else:
        raise Http404() # don't use this api for searches

    if request.query_params.get('name'):
        name_starts_with = request.query_params.get('name').strip().lower()
        if name_starts_with and allow_name_search:
            queryset = queryset.filter(slug__startswith=name_starts_with)
        else:
            raise Http404()

    queryset = queryset.select_related('rank', 'ban_cache', 'online_tracker')

    paginator = Paginator()
    users = paginator.paginate_queryset(queryset.order_by('slug'), request)

    make_users_status_aware(request.user, users)
    return paginator.get_paginated_response(
        UserSerializer(users, many=True).data)


LISTS = {
    'active': active,
}


def list_endpoint(request):
    list_type = request.query_params.get('list')
    list_handler = LISTS.get(list_type)

    if list_handler:
        return list_handler(request)
    else:
        return generic(request)
