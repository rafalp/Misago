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
    last_poster_url = serializers.SerializerMethodField()
    absolute_url = serializers.SerializerMethodField()
    last_post_url = serializers.SerializerMethodField()
    new_post_url = serializers.SerializerMethodField()
    subscription = serializers.SerializerMethodField()
    api_url = serializers.SerializerMethodField()
    acl = serializers.SerializerMethodField()

    class Meta:
        model = Thread
        fields = (
            'id',
            'title',
            'weight',
            'category',
            'replies',
            'is_closed',
            'is_hidden',
            'is_read',
            'absolute_url',
            'last_poster_url',
            'last_post_url',
            'new_post_url',
            'subscription',
            'api_url',
            'acl',
        )

    def get_is_read(self, obj):
        try:
            return obj.is_read
        except AttributeError:
            return None

    def get_last_poster_url(self, obj):
        if obj.last_poster_id:
            return reverse('misago:user', kwargs={
                'slug': obj.last_poster_slug,
                'pk': obj.last_poster_id,
            })
        else:
            return None

    def get_absolute_url(self, obj):
        return obj.get_absolute_url()

    def get_last_post_url(self, obj):
        return obj.get_last_post_url()

    def get_new_post_url(self, obj):
        return obj.get_new_post_url()

    def get_subscription(self, obj):
        try:
            return obj.subscription.send_email
        except AttributeError:
            return None

    def get_api_url(self, obj):
        return obj.get_api_url()

    def get_acl(self, obj):
        try:
            return obj.acl
        except AttributeError:
            return {}


class ThreadListSerializer(ThreadSerializer):
    category = serializers.PrimaryKeyRelatedField(read_only=True)
    last_post = serializers.PrimaryKeyRelatedField(read_only=True)
    top_category = serializers.SerializerMethodField()

    class Meta:
        model = Thread
        fields = (
            'id',
            'title',
            'weight',
            'category',
            'top_category',
            'replies',
            'started_on',
            'last_post',
            'last_poster_name',
            'last_poster_url',
            'last_post_on',
            'is_closed',
            'is_hidden',
            'is_read',
            'absolute_url',
            'last_post_url',
            'new_post_url',
            'subscription',
            'api_url',
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