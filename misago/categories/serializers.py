from django.core.urlresolvers import reverse
from rest_framework import serializers

from misago.core.utils import format_plaintext_for_html

from misago.categories.models import Category


__all__ = ['CategorySerializer']


class CategorySerializer(serializers.ModelSerializer):
    description = serializers.SerializerMethodField()
    is_read = serializers.SerializerMethodField()
    subcategories = serializers.SerializerMethodField()
    absolute_url = serializers.SerializerMethodField()
    last_poster_url = serializers.SerializerMethodField()
    last_thread_url = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = (
            'id',
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
            'last_poster_url',
        )

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

    def get_last_thread_url(self, obj):
        return obj.get_last_thread_url()

    def get_last_poster_url(self, obj):
        if obj.last_poster_id:
            return reverse('misago:user', kwargs={
                'user_slug': obj.last_poster_slug,
                'user_id': obj.last_poster_id,
            })
        else:
            return None