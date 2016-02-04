from datetime import timedelta

from django.contrib.auth import get_user_model
from django.db.models import Count
from django.utils import timezone

from rest_framework.pagination import PageNumberPagination

from misago.conf import settings
from misago.core.cache import cache
from misago.core.shortcuts import get_object_or_404
from misago.forums.models import Forum

from misago.users.views.lists import get_active_posters_rankig
from misago.users.models import Rank
from misago.users.online.utils import make_users_status_aware
from misago.users.serializers import ScoredUserSerializer


def active(request):
    ranking = get_active_posters_rankig()
    make_users_status_aware(ranking['users'], request.user.acl)

    return {
        'tracked_period': settings.MISAGO_RANKING_LENGTH,
        'results': ScoredUserSerializer(ranking['users'], many=True).data,
        'count': ranking['users_count']
    }


def rank(request, queryset):
    rank_slug = request.query_params.get('rank')
    if not rank_slug:
        return

    rank = get_object_or_404(Rank.objects.filter(is_tab=True), slug=rank_slug)
    queryset = queryset.filter(rank=rank).order_by('slug')

    return {'queryset': queryset, 'paginate': True}


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
        return
