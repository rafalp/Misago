from datetime import timedelta

from django.contrib.auth import get_user_model
from django.db.models import Count
from django.http import Http404
from django.utils import timezone

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from misago.conf import settings
from misago.core.apipaginator import ApiPaginator
from misago.core.cache import cache
from misago.core.shortcuts import get_object_or_404
from misago.forums.models import Forum

from misago.users.views.lists import get_active_posters_rankig
from misago.users.models import Rank
from misago.users.online.utils import make_users_status_aware
from misago.users.serializers import UserSerializer, ScoredUserSerializer


Paginator = ApiPaginator(settings.MISAGO_USERS_PER_PAGE, 4)


def active(request):
    ranking = get_active_posters_rankig()
    make_users_status_aware(
        ranking['users'], request.user.acl, fetch_state=True)

    return Response({
        'tracked_period': settings.MISAGO_RANKING_LENGTH,
        'results': ScoredUserSerializer(ranking['users'], many=True).data,
        'count': ranking['users_count']
    })


def rank(request):
    rank_slug = request.query_params.get('rank')
    if not rank_slug:
        raise Http404()

    rank = get_object_or_404(Rank.objects, slug=rank_slug, is_tab=True)
    queryset = rank.user_set.select_related(
        'rank', 'ban_cache', 'online_tracker').order_by('slug')

    paginator = Paginator()
    users = paginator.paginate_queryset(queryset, request)

    make_users_status_aware(users, request.user.acl)
    return paginator.get_paginated_response(
        UserSerializer(users, many=True).data)


LISTS = {
    'active': active,
    'rank': rank,
}


def list_endpoint(request):
    list_type = request.query_params.get('list')
    list_handler = LISTS.get(list_type)

    if list_handler:
        return list_handler(request)
    else:
        raise Http404()
