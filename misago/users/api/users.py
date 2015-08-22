from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext as _

from rest_framework import mixins, status, viewsets
from rest_framework.decorators import detail_route, list_route
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.response import Response

from misago.acl import add_acl
from misago.core.apipaginator import ApiPaginator
from misago.core.cache import cache

from misago.users.forms.options import ForumOptionsForm
from misago.users.permissions.profiles import (allow_browse_users_list,
                                               allow_see_users_online_list)

from misago.users.rest_permissions import (BasePermission,
    IsAuthenticatedOrReadOnly, UnbannedAnonOnly)
from misago.users.serializers import UserSerializer, UserProfileSerializer

from misago.users.api.userendpoints.list import list_endpoint
from misago.users.api.userendpoints.avatar import avatar_endpoint
from misago.users.api.userendpoints.create import create_endpoint
from misago.users.api.userendpoints.signature import signature_endpoint
from misago.users.api.userendpoints.username import username_endpoint
from misago.users.api.userendpoints.changeemail import change_email_endpoint
from misago.users.api.userendpoints.changepassword import change_password_endpoint


class UserViewSetPermission(BasePermission):
    def has_permission(self, request, view):
        if view.action == 'create':
            policy = UnbannedAnonOnly()
        else:
            policy = IsAuthenticatedOrReadOnly()
        return policy.has_permission(request, view)


def allow_self_only(user, pk, message):
    if user.is_anonymous():
        raise PermissionDenied(
            _("You have to sign in to perform this action."))
    if user.pk != int(pk):
        raise PermissionDenied(message)


class UserViewSet(viewsets.GenericViewSet):
    permission_classes = (UserViewSetPermission,)
    parser_classes=(JSONParser, MultiPartParser)
    serializer_class = UserSerializer
    queryset = get_user_model().objects
    pagination_class = ApiPaginator(settings.MISAGO_USERS_PER_PAGE, 4)

    def get_queryset(self):
        relations = ('rank', 'online_tracker', 'ban_cache')
        return self.queryset.select_related(*relations)

    def get_users_count(self):
        users_count = cache.get('users_count')
        if not users_count:
            users_count = self.queryset.count()
            cache.set('users_count', users_count, 15 * 60)
        return users_count

    def list(self, request):
        import time
        time.sleep(10)

        allow_browse_users_list(request.user)

        response_dict = {
            'results': [],
            'users': self.get_users_count(),
        }

        list_dict = list_endpoint(request, self.get_queryset())
        if not list_dict:
            return Response([])

        if list_dict.get('meta'):
            response_dict.update(list_dict['meta'])

        if list_dict.get('results'):
            response_dict['results'] = list_dict['results']
        elif list_dict.get('queryset'):
            queryset = list_dict['queryset']
            if list_dict.get('paginate'):
                queryset = self.paginate_queryset(list_dict['queryset'])
                response_dict.update(self.paginator.get_meta())

            if list_dict.get('serializer'):
                SerializerClass = list_dict.get('serializer')
            else:
                SerializerClass = self.serializer_class

            serializer = SerializerClass(
                queryset, many=True, context={'user': request.user})
            response_dict['results'] = serializer.data

        return Response(response_dict)

    def create(self, request):
        return create_endpoint(request)

    def retrieve(self, request, pk=None):
        qs = self.get_queryset()
        profile = get_object_or_404(self.get_queryset(), id=pk)

        add_acl(request.user, profile)

        serializer = UserProfileSerializer(
            profile, context={'user': request.user})
        return Response(serializer.data)

    @detail_route(methods=['get', 'post'])
    def avatar(self, request, pk=None):
        allow_self_only(
            request.user, pk, _("You can't change other users avatars."))

        return avatar_endpoint(request)

    @detail_route(methods=['post'])
    def forum_options(self, request, pk=None):
        allow_self_only(
            request.user, pk, _("You can't change other users options."))

        form = ForumOptionsForm(request.data, instance=request.user)
        if form.is_valid():
            form.save()
            return Response({
                'detail': _("Your forum options have been changed.")
            })
        else:
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

    @detail_route(methods=['get', 'post'])
    def username(self, request, pk=None):
        allow_self_only(
            request.user, pk, _("You can't change other users names."))

        return username_endpoint(request)

    @detail_route(methods=['get', 'post'])
    def signature(self, request, pk=None):
        allow_self_only(
            request.user, pk, _("You can't change other users signatures."))

        return signature_endpoint(request)

    @detail_route(methods=['post'])
    def change_password(self, request, pk=None):
        allow_self_only(
            request.user, pk, _("You can't change other users passwords."))

        return change_password_endpoint(request)

    @detail_route(methods=['post'])
    def change_email(self, request, pk=None):
        allow_self_only(request.user, pk,
                        _("You can't change other users e-mail addresses."))

        return change_email_endpoint(request)
