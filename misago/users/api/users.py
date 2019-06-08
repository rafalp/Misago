from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.db.models import F
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext as _
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.response import Response

from ...acl.objectacl import add_acl_to_obj
from ...categories.models import Category
from ...core.rest_permissions import IsAuthenticatedOrReadOnly
from ...core.shortcuts import get_int_or_404
from ...threads.moderation import hide_post, hide_thread
from ..bans import get_user_ban
from ..datadownloads import request_user_data_download, user_has_data_download_request
from ..online.utils import get_user_status
from ..permissions import (
    allow_browse_users_list,
    allow_delete_user,
    allow_edit_profile_details,
    allow_follow_user,
    allow_moderate_avatar,
    allow_rename_user,
    allow_see_ban_details,
)
from ..profilefields import profilefields, serialize_profilefields_data
from ..serializers import (
    BanDetailsSerializer,
    DataDownloadSerializer,
    DeleteOwnAccountSerializer,
    ForumOptionsSerializer,
    UserSerializer,
)
from ..viewmodels import Followers, Follows, UserPosts, UserThreads
from .rest_permissions import BasePermission, UnbannedAnonOnly
from .userendpoints.avatar import avatar_endpoint, moderate_avatar_endpoint
from .userendpoints.changeemail import change_email_endpoint
from .userendpoints.changepassword import change_password_endpoint
from .userendpoints.create import create_endpoint
from .userendpoints.editdetails import edit_details_endpoint
from .userendpoints.list import list_endpoint
from .userendpoints.signature import signature_endpoint
from .userendpoints.username import moderate_username_endpoint, username_endpoint

User = get_user_model()


class UserViewSetPermission(BasePermission):
    def has_permission(self, request, view):
        if view.action == "create":
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
    permission_classes = (UserViewSetPermission,)
    parser_classes = (FormParser, JSONParser, MultiPartParser)
    queryset = User.objects

    def get_queryset(self):
        relations = ("rank", "online_tracker", "ban_cache")
        return self.queryset.select_related(*relations)

    def get_user(self, request, pk):
        user = get_object_or_404(self.get_queryset(), pk=get_int_or_404(pk))
        if not user.is_active and not request.user.is_staff:
            raise Http404()
        return user

    def list(self, request):
        allow_browse_users_list(request.user_acl)
        return list_endpoint(request)

    def create(self, request):
        return create_endpoint(request)

    def retrieve(self, request, pk=None):
        profile = self.get_user(request, pk)

        add_acl_to_obj(request.user_acl, profile)
        profile.status = get_user_status(request, profile)

        serializer = UserProfileSerializer(profile, context={"request": request})
        profile_json = serializer.data

        if not profile.is_active:
            profile_json["is_active"] = False
        if profile.is_deleting_account:
            profile_json["is_deleting_account"] = True

        return Response(profile_json)

    @action(methods=["get", "post"], detail=True)
    def avatar(self, request, pk=None):
        get_int_or_404(pk)
        allow_self_only(request.user, pk, _("You can't change other users avatars."))

        return avatar_endpoint(request)

    @action(
        methods=["post"],
        detail=True,
        url_name="forum-options",
        url_path="forum-options",
    )
    def forum_options(self, request, pk=None):
        get_int_or_404(pk)
        allow_self_only(request.user, pk, _("You can't change other users options."))

        serializer = ForumOptionsSerializer(request.user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": _("Your forum options have been changed.")})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=["get", "post"], detail=True)
    def username(self, request, pk=None):
        get_int_or_404(pk)
        allow_self_only(request.user, pk, _("You can't change other users names."))

        return username_endpoint(request)

    @action(methods=["get", "post"], detail=True)
    def signature(self, request, pk=None):
        get_int_or_404(pk)
        allow_self_only(request.user, pk, _("You can't change other users signatures."))

        return signature_endpoint(request)

    @action(
        methods=["post"],
        detail=True,
        url_path="change-password",
        url_name="change-password",
    )
    def change_password(self, request, pk=None):
        get_int_or_404(pk)
        allow_self_only(request.user, pk, _("You can't change other users passwords."))

        return change_password_endpoint(request)

    @action(
        methods=["post"], detail=True, url_path="change-email", url_name="change-email"
    )
    def change_email(self, request, pk=None):
        get_int_or_404(pk)
        allow_self_only(
            request.user, pk, _("You can't change other users e-mail addresses.")
        )

        return change_email_endpoint(request)

    @action(methods=["get"], detail=True)
    def details(self, request, pk=None):
        profile = self.get_user(request, pk)
        data = serialize_profilefields_data(request, profilefields, profile)
        return Response(data)

    @action(
        methods=["get", "post"],
        detail=True,
        url_path="edit-details",
        url_name="edit-details",
    )
    def edit_details(self, request, pk=None):
        profile = self.get_user(request, pk)
        allow_edit_profile_details(request.user_acl, profile)
        return edit_details_endpoint(request, profile)

    @action(
        methods=["post"],
        detail=True,
        url_path="delete-own-account",
        url_name="delete-own-account",
    )
    def delete_own_account(self, request, pk=None):
        serializer = DeleteOwnAccountSerializer(
            data=request.data, context={"user": request.user}
        )
        serializer.is_valid(raise_exception=True)
        serializer.mark_account_for_deletion(request)
        return Response({})

    @action(methods=["post"], detail=True)
    def follow(self, request, pk=None):
        profile = self.get_user(request, pk)
        allow_follow_user(request.user_acl, profile)

        profile_followers = profile.followers

        with transaction.atomic():
            if request.user.is_following(profile):
                request.user.follows.remove(profile)
                followed = False

                profile_followers -= 1
                profile.followers = F("followers") - 1
                request.user.following = F("following") - 1
            else:
                request.user.follows.add(profile)
                followed = True

                profile_followers += 1
                profile.followers = F("followers") + 1
                request.user.following = F("following") + 1

            profile.save(update_fields=["followers"])
            request.user.save(update_fields=["following"])

            return Response({"is_followed": followed, "followers": profile_followers})

    @action(detail=True)
    def ban(self, request, pk=None):
        profile = self.get_user(request, pk)
        allow_see_ban_details(request.user_acl, profile)

        ban = get_user_ban(profile, request.cache_versions)
        if ban:
            return Response(BanDetailsSerializer(ban).data)
        return Response({})

    @action(
        methods=["get", "post"],
        detail=True,
        url_path="moderate-avatar",
        url_name="moderate-avatar",
    )
    def moderate_avatar(self, request, pk=None):
        profile = self.get_user(request, pk)
        allow_moderate_avatar(request.user_acl, profile)

        return moderate_avatar_endpoint(request, profile)

    @action(
        methods=["get", "post"],
        detail=True,
        url_path="moderate-username",
        url_name="moderate-username",
    )
    def moderate_username(self, request, pk=None):
        profile = self.get_user(request, pk)
        allow_rename_user(request.user_acl, profile)

        return moderate_username_endpoint(request, profile)

    @action(
        methods=["post"],
        detail=True,
        url_path="request-data-download",
        url_name="request-data-download",
    )
    def request_data_download(self, request, pk=None):
        get_int_or_404(pk)
        allow_self_only(
            request.user, pk, _("You can't request data downloads for other users.")
        )

        if not request.settings.allow_data_downloads:
            raise PermissionDenied(_("You can't download your data."))

        if user_has_data_download_request(request.user):
            raise PermissionDenied(
                _(
                    "You can't have more than one data download request at a single time."
                )
            )

        request_user_data_download(request.user)

        return Response({"detail": "ok"})

    @action(methods=["get", "post"], detail=True)
    def delete(self, request, pk=None):
        profile = self.get_user(request, pk)
        allow_delete_user(request.user_acl, profile)

        if request.method == "POST":
            with transaction.atomic():
                profile.lock()

                if request.data.get("with_content"):
                    profile.delete_content()
                else:
                    categories_to_sync = set()

                    threads = profile.thread_set.select_related(
                        "category", "first_post"
                    )
                    for thread in threads.filter(is_hidden=False).iterator():
                        categories_to_sync.add(thread.category_id)
                        hide_thread(request, thread)

                    posts = profile.post_set.select_related(
                        "category", "thread", "thread__category"
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

                profile.delete(anonymous_username=request.settings.anonymous_username)

        return Response({})

    @action(
        methods=["get"],
        detail=True,
        url_path="data-downloads",
        url_name="data-downloads",
    )
    def data_downloads(self, request, pk=None):
        get_int_or_404(pk)
        allow_self_only(
            request.user, pk, _("You can't see other users data downloads.")
        )

        queryset = request.user.datadownload_set.all()[:5]
        serializer = DataDownloadSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=["get"], detail=True)
    def followers(self, request, pk=None):
        profile = self.get_user(request, pk)

        page = get_int_or_404(request.query_params.get("page", 0))
        if page == 1:
            page = 0  # api allows explicit first page

        search = request.query_params.get("search")

        users = Followers(request, profile, page, search)

        return Response(users.get_frontend_context())

    @action(methods=["get"], detail=True)
    def follows(self, request, pk=None):
        profile = self.get_user(request, pk)

        page = get_int_or_404(request.query_params.get("page", 0))
        if page == 1:
            page = 0  # api allows explicit first page

        search = request.query_params.get("search")

        users = Follows(request, profile, page, search)

        return Response(users.get_frontend_context())

    @action(methods=["get"], detail=True)
    def threads(self, request, pk=None):
        profile = self.get_user(request, pk)
        start = get_int_or_404(request.query_params.get("start", 0))
        feed = UserThreads(request, profile, start)
        return Response(feed.get_frontend_context())

    @action(methods=["get"], detail=True)
    def posts(self, request, pk=None):
        profile = self.get_user(request, pk)
        start = get_int_or_404(request.query_params.get("start", 0))
        feed = UserPosts(request, profile, start)
        return Response(feed.get_frontend_context())


UserProfileSerializer = UserSerializer.subset_fields(
    "id",
    "username",
    "slug",
    "email",
    "joined_on",
    "rank",
    "title",
    "avatars",
    "is_avatar_locked",
    "signature",
    "is_signature_locked",
    "followers",
    "following",
    "threads",
    "posts",
    "acl",
    "is_followed",
    "is_blocked",
    "real_name",
    "status",
    "api",
    "url",
)
