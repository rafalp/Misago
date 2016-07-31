from django.core.urlresolvers import reverse

from rest_framework import serializers

from misago.categories.serializers import BasicCategorySerializer

from ..models import Thread


__all__ = [
    'ThreadSerializer',
    'ThreadsListSerializer',
]


class ThreadSerializer(serializers.ModelSerializer):
    category = BasicCategorySerializer(many=False, read_only=True)

    acl = serializers.SerializerMethodField()
    is_new = serializers.SerializerMethodField()
    is_read = serializers.SerializerMethodField()
    path = BasicCategorySerializer(many=True, read_only=True)
    subscription = serializers.SerializerMethodField()

    api = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()

    class Meta:
        model = Thread
        fields = (
            'id',
            'category',
            'title',
            'replies',
            'has_unapproved_posts',
            'started_on',
            'last_post_on',
            'last_post',
            'last_poster_name',
            'is_unapproved',
            'is_hidden',
            'is_closed',
            'weight',

            'acl',
            'is_new',
            'is_read',
            'path',
            'subscription',

            'api',
            'url',
        )

    def get_acl(self, obj):
        try:
            return obj.acl
        except AttributeError:
            return {}

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

    def get_top_category(self, obj):
        try:
            return obj.top_category.pk
        except AttributeError:
            return None

    def get_subscription(self, obj):
        try:
            return obj.subscription.send_email
        except AttributeError:
            return None

    def get_api(self, obj):
        return {
            'index': obj.get_api_url(),
            'posts': reverse('misago:api:thread-post-list', kwargs={
                'thread_pk': obj.pk
            }),
            'read': 'nada',
        }

    def get_url(self, obj):
        return {
            'index': obj.get_absolute_url(),
            'new_post': obj.get_new_post_url(),
            'last_post': obj.get_last_post_url(),
            'unapproved_post': obj.get_unapproved_post_url(),
            'last_poster': self.get_last_poster_url(obj),
        }

    def get_last_poster_url(self, obj):
        if obj.last_poster_id:
            return reverse('misago:user', kwargs={
                'slug': obj.last_poster_slug,
                'pk': obj.last_poster_id,
            })
        else:
            return None


class ThreadsListSerializer(ThreadSerializer):
    category = serializers.PrimaryKeyRelatedField(read_only=True)
    last_post = serializers.PrimaryKeyRelatedField(read_only=True)

    top_category = serializers.SerializerMethodField()

    class Meta:
        model = Thread
        fields = (
            'id',
            'category',
            'title',
            'replies',
            'has_unapproved_posts',
            'started_on',
            'last_post_on',
            'last_post',
            'last_poster_name',
            'weight',
            'is_unapproved',
            'is_hidden',
            'is_closed',

            'acl',
            'is_new',
            'is_read',
            'subscription',
            'top_category',

            'api',
            'url',
        )
