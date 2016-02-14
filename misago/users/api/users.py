from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.db.models import F
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext as _

from rest_framework import mixins, status, viewsets
from rest_framework.decorators import detail_route, list_route
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.response import Response

from misago.acl import add_acl
from misago.core.cache import cache

from misago.users.forms.options import ForumOptionsForm
from misago.users.online.utils import get_user_status
from misago.users.permissions.profiles import (allow_browse_users_list,
                                               allow_follow_user)

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

    def get_queryset(self):
        relations = ('rank', 'online_tracker', 'ban_cache')
        return self.queryset.select_related(*relations)

    def list(self, request):
        allow_browse_users_list(request.user)
        return list_endpoint(request)

    def create(self, request):
        return create_endpoint(request)

    def retrieve(self, request, pk=None):
        profile = get_object_or_404(self.get_queryset(), id=pk)

        add_acl(request.user, profile)
        profile.status = get_user_status(profile, request.user.acl)

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

    @detail_route(methods=['post'])
    def follow(self, request, pk=None):
        profile = get_object_or_404(self.get_queryset(), id=pk)
        allow_follow_user(request.user, profile)

        profile_followers = profile.followers

        with transaction.atomic():
            if request.user.is_following(profile):
                request.user.follows.remove(profile)
                followed = False

                profile_followers -= 1
                profile.followers = F('followers') - 1
                request.user.following = F('following') - 1
            else:
                request.user.follows.add(profile)
                followed = True

                profile_followers += 1
                profile.followers = F('followers') + 1
                request.user.following = F('following') + 1

            profile.save(update_fields=['followers'])
            request.user.save(update_fields=['following'])

            return Response({
                'is_followed': followed,
                'followers': profile_followers
            })