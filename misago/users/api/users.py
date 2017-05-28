from rest_framework import status, viewsets
from rest_framework.decorators import detail_route
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.response import Response

from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.db.models import F
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext as _

from misago.acl import add_acl
from misago.categories.models import Category
from misago.core.rest_permissions import IsAuthenticatedOrReadOnly
from misago.core.shortcuts import get_int_or_404
from misago.threads.moderation import hide_post, hide_thread
from misago.users.bans import get_user_ban
from misago.users.online.utils import get_user_status
from misago.users.permissions import (
    allow_browse_users_list, allow_delete_user, allow_follow_user, allow_moderate_avatar,
    allow_rename_user, allow_see_ban_details)
from misago.users.serializers import BanDetailsSerializer, ForumOptionsSerializer, UserSerializer
from misago.users.viewmodels import Followers, Follows, UserPosts, UserThreads

from .rest_permissions import BasePermission, UnbannedAnonOnly
from .userendpoints.avatar import avatar_endpoint, moderate_avatar_endpoint
from .userendpoints.changeemail import change_email_endpoint
from .userendpoints.changepassword import change_password_endpoint
from .userendpoints.create import create_endpoint
from .userendpoints.list import list_endpoint
from .userendpoints.signature import signature_endpoint
from .userendpoints.username import moderate_username_endpoint, username_endpoint


UserModel = get_user_model()


class UserViewSetPermission(BasePermission):
    def has_permission(self, request, view):
        if view.action == 'create':
            policy = UnbannedAnonOnly()
        else:
            policy = IsAuthenticatedOrReadOnly()
        return policy.has_permission(request, view)


def allow_self_only(user, pk, message):
    if user.is_anonymous:
        raise PermissionDenied(_("You have to sign in to perform this action."))
    if user.pk != int(pk):
        raise PermissionDenied(message)


class UserViewSet(viewsets.GenericViewSet):
    permission_classes = (UserViewSetPermission, )
    parser_classes = (FormParser, JSONParser, MultiPartParser)
    queryset = UserModel.objects

    def get_queryset(self):
        relations = ('rank', 'online_tracker', 'ban_cache')
        return self.queryset.select_related(*relations)

    def get_user(self, request, pk):
        user = get_object_or_404(self.get_queryset(), pk=get_int_or_404(pk))
        if not user.is_active and not request.user.is_staff:
            raise Http404()
        return user

    def list(self, request):
        allow_browse_users_list(request.user)
        return list_endpoint(request)

    def create(self, request):
        return create_endpoint(request)

    def retrieve(self, request, pk=None):
        profile = self.get_user(request, pk)

        add_acl(request.user, profile)
        profile.status = get_user_status(request.user, profile)

        serializer = UserProfileSerializer(profile, context={'user': request.user})
        profile_json = serializer.data

        if not profile.is_active:
            profile_json['is_active'] = False

        return Response(profile_json)

    @detail_route(methods=['get', 'post'])
    def avatar(self, request, pk=None):
        get_int_or_404(pk)
        allow_self_only(request.user, pk, _("You can't change other users avatars."))

        return avatar_endpoint(request)

    @detail_route(methods=['post'])
    def forum_options(self, request, pk=None):
        get_int_or_404(pk)
        allow_self_only(request.user, pk, _("You can't change other users options."))

        serializer = ForumOptionsSerializer(request.user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'detail': _("Your forum options have been changed.")})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @detail_route(methods=['get', 'post'])
    def username(self, request, pk=None):
        get_int_or_404(pk)
        allow_self_only(request.user, pk, _("You can't change other users names."))

        return username_endpoint(request)

    @detail_route(methods=['get', 'post'])
    def signature(self, request, pk=None):
        get_int_or_404(pk)
        allow_self_only(request.user, pk, _("You can't change other users signatures."))

        return signature_endpoint(request)

    @detail_route(methods=['post'])
    def change_password(self, request, pk=None):
        get_int_or_404(pk)
        allow_self_only(request.user, pk, _("You can't change other users passwords."))

        return change_password_endpoint(request)

    @detail_route(methods=['post'])
    def change_email(self, request, pk=None):
        get_int_or_404(pk)
        allow_self_only(request.user, pk, _("You can't change other users e-mail addresses."))

        return change_email_endpoint(request)

    @detail_route(methods=['post'])
    def follow(self, request, pk=None):
        profile = self.get_user(request, pk)
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

            return Response({'is_followed': followed, 'followers': profile_followers})

    @detail_route()
    def ban(self, request, pk=None):
        profile = self.get_user(request, pk)
        allow_see_ban_details(request.user, profile)

        ban = get_user_ban(profile)
        if ban:
            return Response(BanDetailsSerializer(ban).data)
        else:
            return Response({})

    @detail_route(methods=['get', 'post'])
    def moderate_avatar(self, request, pk=None):
        profile = self.get_user(request, pk)
        allow_moderate_avatar(request.user, profile)

        return moderate_avatar_endpoint(request, profile)

    @detail_route(methods=['get', 'post'])
    def moderate_username(self, request, pk=None):
        profile = self.get_user(request, pk)
        allow_rename_user(request.user, profile)

        return moderate_username_endpoint(request, profile)

    @detail_route(methods=['get', 'post'])
    def delete(self, request, pk=None):
        profile = self.get_user(request, pk)
        allow_delete_user(request.user, profile)

        if request.method == 'POST':
            with transaction.atomic():
                profile.lock()

                if request.data.get('with_content'):
                    profile.delete_content()
                else:
                    categories_to_sync = set()

                    threads = profile.thread_set.select_related('category', 'first_post')
                    for thread in threads.filter(is_hidden=False).iterator():
                        categories_to_sync.add(thread.category_id)
                        hide_thread(request, thread)

                    posts = profile.post_set.select_related(
                        'category', 'thread', 'thread__category'
                    )
                    for post in posts.filter(is_hidden=False).iterator():
                        categories_to_sync.add(post.category_id)
                        hide_post(request.user, post)
                        post.thread.synchronize()
                        post.thread.save()

                    categories = Category.objects.filter(id__in=categories_to_sync)
                    for category in categories.iterator():
                        category.synchronize()
                        category.save()

                profile.delete()

        return Response({'detail': 'ok'})

    @detail_route(methods=['get'])
    def followers(self, request, pk=None):
        profile = self.get_user(request, pk)

        page = get_int_or_404(request.query_params.get('page', 0))
        if page == 1:
            page = 0  # api allows explicit first page

        search = request.query_params.get('search')

        users = Followers(request, profile, page, search)

        return Response(users.get_frontend_context())

    @detail_route(methods=['get'])
    def follows(self, request, pk=None):
        profile = self.get_user(request, pk)

        page = get_int_or_404(request.query_params.get('page', 0))
        if page == 1:
            page = 0  # api allows explicit first page

        search = request.query_params.get('search')

        users = Follows(request, profile, page, search)

        return Response(users.get_frontend_context())

    @detail_route(methods=['get'])
    def threads(self, request, pk=None):
        profile = self.get_user(request, pk)

        page = get_int_or_404(request.query_params.get('page', 0))
        if page == 1:
            page = 0  # api allows explicit first page

        feed = UserThreads(request, profile, page)

        return Response(feed.get_frontend_context())

    @detail_route(methods=['get'])
    def posts(self, request, pk=None):
        profile = self.get_user(request, pk)

        page = get_int_or_404(request.query_params.get('page', 0))
        if page == 1:
            page = 0  # api allows explicit first page

        feed = UserPosts(request, profile, page)

        return Response(feed.get_frontend_context())


UserProfileSerializer = UserSerializer.subset_fields(
    'id',
    'username',
    'slug',
    'email',
    'joined_on',
    'rank',
    'title',
    'avatars',
    'is_avatar_locked',
    'signature',
    'is_signature_locked',
    'followers',
    'following',
    'threads',
    'posts',
    'acl',
    'is_followed',
    'is_blocked',
    'status',
    'api',
    'url',
)
