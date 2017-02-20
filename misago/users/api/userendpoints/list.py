from rest_framework.response import Response

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from misago.core.shortcuts import get_int_or_404
from misago.users.models import Rank
from misago.users.serializers import UserCardSerializer
from misago.users.viewmodels import ActivePosters, RankUsers


UserModel = get_user_model()


def active(request):
    users = ActivePosters(request)
    return Response(users.get_frontend_context())


def rank_users(request):
    rank_pk = get_int_or_404(request.query_params.get('rank'))
    rank = get_object_or_404(Rank.objects, pk=rank_pk, is_tab=True)

    page = get_int_or_404(request.GET.get('page', 0))
    if page == 1:
        page = 0  # api allows explicit first page

    users = RankUsers(request, rank, page)
    return Response(users.get_frontend_context())


LISTS = {
    'active': active,
}


def list_endpoint(request):
    list_type = request.query_params.get('list')
    list_handler = LISTS.get(list_type)

    if list_handler:
        return list_handler(request)
    else:
        return rank_users(request)


ScoredUserSerializer = UserCardSerializer.extend_fields('meta')
