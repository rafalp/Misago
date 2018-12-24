from django.urls import reverse
from rest_framework import serializers

from ..core.serializers import MutableFields
from ..core.utils import format_plaintext_for_html
from .models import Category

__all__ = ["CategorySerializer"]


def last_activity_detail(f):
    """util for serializing last activity details"""

    def decorator(self, obj):
        if not obj.last_thread_id:
            return None

        acl = self.get_acl(obj)
        tested_acls = (
            acl.get("can_see"),
            acl.get("can_browse"),
            acl.get("can_see_all_threads"),
        )

        if not all(tested_acls):
            return None

        return f(self, obj)

    return decorator


class CategorySerializer(serializers.ModelSerializer, MutableFields):
    parent = serializers.PrimaryKeyRelatedField(read_only=True)
    description = serializers.SerializerMethodField()
    is_read = serializers.SerializerMethodField()
    subcategories = serializers.SerializerMethodField()
    acl = serializers.SerializerMethodField()

    url = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = [
            "id",
            "parent",
            "name",
            "description",
            "is_closed",
            "threads",
            "posts",
            "last_post_on",
            "last_thread_title",
            "last_poster",
            "last_poster_name",
            "css_class",
            "is_read",
            "subcategories",
            "acl",
            "level",
            "lft",
            "rght",
            "url",
        ]

    def get_description(self, obj):
        if obj.description:
            return {
                "plain": obj.description,
                "html": format_plaintext_for_html(obj.description),
            }

    def get_is_read(self, obj):
        try:
            return obj.is_read
        except AttributeError:
            return None

    def get_subcategories(self, obj):
        try:
            return CategorySerializer(obj.subcategories, many=True).data
        except AttributeError:
            return []

    def get_acl(self, obj):
        try:
            return obj.acl
        except AttributeError:
            return {}

    @last_activity_detail
    def get_last_poster(self, obj):
        if obj.last_poster_id:
            return {
                "id": obj.last_poster_id,
                "avatars": obj.last_poster.avatars,
                "url": reverse(
                    "misago:user",
                    kwargs={"slug": obj.last_poster_slug, "pk": obj.last_poster_id},
                ),
            }

    def get_url(self, obj):
        return {
            "index": obj.get_absolute_url(),
            "last_thread": self.get_last_thread_url(obj),
            "last_thread_new": self.get_last_thread_new_url(obj),
            "last_post": self.get_last_post_url(obj),
        }

    @last_activity_detail
    def get_last_thread_url(self, obj):
        return obj.get_last_thread_url()

    @last_activity_detail
    def get_last_thread_new_url(self, obj):
        return obj.get_last_thread_new_url()

    @last_activity_detail
    def get_last_post_url(self, obj):
        return obj.get_last_post_url()


class CategoryWithPosterSerializer(CategorySerializer):
    last_poster = serializers.SerializerMethodField()

    def get_subcategories(self, obj):
        try:
            return CategoryWithPosterSerializer(obj.subcategories, many=True).data
        except AttributeError:
            return []


CategoryWithPosterSerializer = CategoryWithPosterSerializer.extend_fields("last_poster")
