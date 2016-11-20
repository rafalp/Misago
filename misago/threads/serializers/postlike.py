from django.core.urlresolvers import reverse

from rest_framework import serializers

from ..models import PostLike


__all__ = [
    'PostLikeSerializer',
]


class PostLikeSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()

    url = serializers.SerializerMethodField()

    class Meta:
        model = PostLike
        fields = (
            'liked_on',

            'id',
            'username',

            'url',
        )

    def get_id(self, obj):
        return obj['user_id']

    def get_username(self, obj):
        return obj['user_name']

    def get_url(self, obj):
        if obj['user_id']:
            return reverse('misago:user', kwargs={
                'slug': obj['user_slug'],
                'pk': obj['user_id'],
            })
        else:
            return None
