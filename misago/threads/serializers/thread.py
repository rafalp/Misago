from math import ceil

from django.urls import reverse
from rest_framework import serializers

from ...categories.serializers import CategorySerializer
from ...core.serializers import MutableFields
from ...notifications.threads import ThreadNotifications
from ..models import Thread
from .poll import PollSerializer
from .threadparticipant import ThreadParticipantSerializer

__all__ = ["ThreadSerializer", "PrivateThreadSerializer", "ThreadsListSerializer"]

BasicCategorySerializer = CategorySerializer.subset_fields(
    "id",
    "parent",
    "name",
    "short_name",
    "color",
    "description",
    "is_closed",
    "css_class",
    "level",
    "lft",
    "rght",
    "is_read",
    "url",
)


class ThreadSerializer(serializers.ModelSerializer, MutableFields):
    category = BasicCategorySerializer(many=False, read_only=True)

    acl = serializers.SerializerMethodField()
    has_unapproved_posts = serializers.SerializerMethodField()
    is_new = serializers.SerializerMethodField()
    is_read = serializers.SerializerMethodField()
    path = BasicCategorySerializer(many=True, read_only=True)
    poll = PollSerializer(many=False, read_only=True)
    pages = serializers.SerializerMethodField()
    best_answer = serializers.PrimaryKeyRelatedField(read_only=True)
    best_answer_marked_by = serializers.PrimaryKeyRelatedField(read_only=True)
    notifications = serializers.SerializerMethodField()
    starter = serializers.SerializerMethodField()
    last_poster = serializers.SerializerMethodField()

    api = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()

    class Meta:
        model = Thread
        fields = [
            "id",
            "category",
            "title",
            "replies",
            "has_unapproved_posts",
            "started_on",
            "starter_name",
            "last_post_on",
            "last_post_is_event",
            "last_post",
            "last_poster_name",
            "is_unapproved",
            "is_hidden",
            "is_closed",
            "weight",
            "best_answer",
            "best_answer_is_protected",
            "best_answer_marked_on",
            "best_answer_marked_by",
            "best_answer_marked_by_name",
            "best_answer_marked_by_slug",
            "acl",
            "is_new",
            "is_read",
            "path",
            "poll",
            "notifications",
            "starter",
            "last_poster",
            "pages",
            "api",
            "url",
        ]

    def get_acl(self, obj):
        try:
            return obj.acl
        except AttributeError:
            return {}

    def get_has_unapproved_posts(self, obj):
        try:
            acl = obj.acl
        except AttributeError:
            return False
        return acl.get("can_approve") and obj.has_unapproved_posts

    def get_is_new(self, obj):
        try:
            return obj.is_new
        except AttributeError:
            return None

    def get_is_read(self, obj):
        try:
            return obj.is_read
        except AttributeError:
            return None

    def get_participants(self, obj):
        return ThreadParticipantSerializer(obj.participants_list, many=True).data

    def get_notifications(self, obj):
        if self.context:
            watched_thread = self.context.get("watched_thread")
            if watched_thread:
                if watched_thread.send_emails:
                    return ThreadNotifications.SITE_AND_EMAIL
                return ThreadNotifications.SITE_ONLY

            watched_threads = self.context.get("watched_threads")
            if watched_threads:
                return watched_threads.get(obj.id)

        return None

    def get_starter(self, obj):
        if obj.starter_id:
            return {
                "id": obj.starter_id,
                "username": obj.starter.username,
                "real_name": obj.starter.get_real_name(),
                "avatars": obj.starter.avatars,
            }

    def get_last_poster(self, obj):
        if obj.last_poster_id:
            return {
                "id": obj.last_poster_id,
                "username": obj.last_poster.username,
                "real_name": obj.last_poster.get_real_name(),
                "avatars": obj.last_poster.avatars,
            }

    def get_pages(self, obj):
        settings = self.context["settings"]

        posts_per_page = settings.posts_per_page - 1
        posts_per_page_orphans = settings.posts_per_page_orphans

        if posts_per_page_orphans:
            posts_per_page_orphans += 1

        total_posts = obj.replies + 1
        if total_posts <= posts_per_page + posts_per_page_orphans:
            return 1

        hits = total_posts - posts_per_page_orphans
        return ceil(hits / posts_per_page)

    def get_api(self, obj):
        return {
            "index": obj.get_api_url(),
            "editor": obj.get_editor_api_url(),
            "merge": obj.get_merge_api_url(),
            "poll": obj.get_poll_api_url(),
            "watch": obj.get_watch_api_url(),
            "posts": {
                "index": obj.get_posts_api_url(),
                "merge": obj.get_post_merge_api_url(),
                "move": obj.get_post_move_api_url(),
                "split": obj.get_post_split_api_url(),
            },
        }

    def get_url(self, obj):
        return {
            "index": obj.get_absolute_url(),
            "new_post": obj.get_new_post_url(),
            "last_post": obj.get_last_post_url(),
            "best_answer": obj.get_best_answer_url(),
            "unapproved_post": obj.get_unapproved_post_url(),
            "starter": self.get_starter_url(obj),
            "last_poster": self.get_last_poster_url(obj),
        }

    def get_starter_url(self, obj):
        if obj.starter_id:
            return reverse(
                "misago:user", kwargs={"slug": obj.starter_slug, "pk": obj.starter_id}
            )

    def get_last_poster_url(self, obj):
        if obj.last_poster_id:
            return reverse(
                "misago:user",
                kwargs={"slug": obj.last_poster_slug, "pk": obj.last_poster_id},
            )


class PrivateThreadSerializer(ThreadSerializer):
    participants = serializers.SerializerMethodField()

    class Meta:
        model = Thread
        fields = ThreadSerializer.Meta.fields + ["participants"]


class ThreadsListSerializer(ThreadSerializer):
    category = serializers.PrimaryKeyRelatedField(read_only=True)
    last_post = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Thread
        fields = ThreadSerializer.Meta.fields + ["has_poll"]


ThreadsListSerializer = ThreadsListSerializer.exclude_fields("path", "poll")
