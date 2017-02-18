from datetime import timedelta

from rest_framework.response import Response

from django.contrib.auth import get_user_model
from django.db.models import Count
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils import timezone

from misago.conf import settings
from misago.core.cache import cache
from misago.core.shortcuts import get_int_or_404, paginate, paginated_response
from misago.users.models import Rank
from misago.users.online.utils import make_users_status_aware
from misago.users.serializers import UserCardSerializer
from misago.users.viewmodels import ActivePosters


UserModel = get_user_model()


def active(request):
    model = ActivePosters(request)
    return Response(model.get_frontend_context())


def generic(request):
    page = get_int_or_404(request.GET.get('page', 0))
    if page == 1:
        page = 0 # api allows explicit first page

    allow_name_search = True
    queryset = UserModel.objects

    if not request.user.is_staff:
        queryset = queryset.filter(is_active=True)

    if request.query_params.get('rank'):
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

    queryset = queryset.select_related(
        'rank', 'ban_cache', 'online_tracker').order_by('slug')

    list_page = paginate(queryset, page, settings.MISAGO_USERS_PER_PAGE, 4)

    make_users_status_aware(request.user, list_page.object_list)

    return paginated_response(list_page, serializer=UserCardSerializer)


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


ScoredUserSerializer = UserCardSerializer.extend_fields('meta')
