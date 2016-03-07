from django.core.urlresolvers import reverse
from rest_framework import serializers

from misago.categories.serializers import BasicCategorySerializer

from misago.threads.models import Thread


__all__ = [
    'ThreadSerializer',
    'ThreadListSerializer',
]


class ThreadSerializer(serializers.ModelSerializer):
    category = BasicCategorySerializer()
    is_read = serializers.SerializerMethodField()
    top_category = BasicCategorySerializer()
    acl = serializers.SerializerMethodField()

    class Meta:
        model = Thread
        fields = (
            'id',
            'title',
            'category',
            'top_category',
            'is_read',
            'acl',
        )

    def get_is_read(self, obj):
        try:
            return obj.is_read
        except AttributeError:
            return None

    def get_acl(self, obj):
        try:
            return obj.acl
        except AttributeError:
            return {}


class ThreadListSerializer(ThreadSerializer):
    category = serializers.PrimaryKeyRelatedField(read_only=True)
    top_category = serializers.SerializerMethodField()

    class Meta:
        model = Thread
        fields = (
            'id',
            'title',
            'category',
            'top_category',
            'is_read',
            'acl',
        )

    def get_top_category(self, obj):
        try:
            return obj.top_category.pk
        except AttributeError:
            return None

    def get_acl(self, obj):
        try:
            return obj.acl
        except AttributeError:
            return {}