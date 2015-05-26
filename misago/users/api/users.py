from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.utils.translation import ugettext as _

from rest_framework import status, viewsets
from rest_framework.decorators import detail_route
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.response import Response

from misago.users.rest_permissions import (BasePermission,
    IsAuthenticatedOrReadOnly, UnbannedAnonOnly)
from misago.users.forms.options import ForumOptionsForm

from misago.users.api.userendpoints.avatar import avatar_endpoint
from misago.users.api.userendpoints.create import create_endpoint
from misago.users.api.userendpoints.signature import signature_endpoint


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
    queryset = get_user_model().objects.all()

    def list(self, request):
        pass

    def create(self, request):
        return create_endpoint(request)

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
    def signature(self, request, pk=None):
        message = _("You can't change other users signatures.")
        allow_self_only(request.user, pk, message)

        if not request.user.acl['can_have_signature']:
            raise PermissionDenied(
                _("You don't have permission to change signature."))

        return signature_endpoint(request)
