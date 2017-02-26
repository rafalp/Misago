from rest_framework import serializers

from django.urls import reverse

from misago.core.serializers import MutableFields
from misago.core.utils import format_plaintext_for_html

from .models import Category


__all__ = ['CategorySerializer']


def last_activity_detail(f):
    """util for serializing last activity details"""

    def decorator(self, obj):
        if not obj.last_thread_id:
            return None

        acl = self.get_acl(obj)
        tested_acls = (acl.get('can_see'), acl.get('can_browse'), acl.get('can_see_all_threads'), )

        if not all(tested_acls):
            return None

        return f(self, obj)

    return decorator


class CategorySerializer(serializers.ModelSerializer, MutableFields):
    parent = serializers.PrimaryKeyRelatedField(read_only=True)
    description = serializers.SerializerMethodField()
    is_read = serializers.SerializerMethodField()
    subcategories = serializers.SerializerMethodField()
    absolute_url = serializers.SerializerMethodField()
    last_poster_url = serializers.SerializerMethodField()
    last_post_url = serializers.SerializerMethodField()
    last_thread_url = serializers.SerializerMethodField()
    acl = serializers.SerializerMethodField()
    api_url = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = [
            'id',
            'parent',
            'name',
            'description',
            'is_closed',
            'threads',
            'posts',
            'last_post_on',
            'last_thread_title',
            'last_poster_name',
            'css_class',
            'is_read',
            'subcategories',
            'absolute_url',
            'last_thread_url',
            'last_post_url',
            'last_poster_url',
            'acl',
            'api_url',
            'level',
            'lft',
            'rght',
        ]

    def get_description(self, obj):
        if obj.description:
            return {
                'plain': obj.description,
                'html': format_plaintext_for_html(obj.description),
            }
        else:
            return None

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

    def get_absolute_url(self, obj):
        return obj.get_absolute_url()

    @last_activity_detail
    def get_last_thread_url(self, obj):
        return obj.get_last_thread_url()

    @last_activity_detail
    def get_last_post_url(self, obj):
        return obj.get_last_post_url()

    @last_activity_detail
    def get_last_poster_url(self, obj):
        if obj.last_poster_id:
            return reverse(
                'misago:user', kwargs={
                    'slug': obj.last_poster_slug,
                    'pk': obj.last_poster_id,
                }
            )
        else:
            return None

    def get_acl(self, obj):
        try:
            return obj.acl
        except AttributeError:
            return {}

    def get_api_url(self, obj):
        return {
            'read': obj.get_read_api_url(),
        }
