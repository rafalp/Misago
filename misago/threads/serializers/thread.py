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
    last_post = serializers.PrimaryKeyRelatedField(read_only=True)
    last_poster_url = serializers.SerializerMethodField()
    top_category = serializers.SerializerMethodField()

    class Meta:
        model = Thread
        fields = (
            'id',
            'title',
            'category',
            'top_category',
            'started_on',
            'last_post',
            'last_poster_name',
            'last_poster_url',
            'last_post_on',
            'is_read',
            'acl',
        )

    def get_last_poster_url(self, obj):
        if self.last_poster_id:
            return return reverse('misago:user', kwargs={
                'user_slug': self.last_poster_slug,
                'user_id': self.last_poster_id,
            })
        else:
            return None

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