from rest_framework import serializers

from django.urls import reverse

from misago.threads.models import PostLike


__all__ = [
    'PostLikeSerializer',
]


class PostLikeSerializer(serializers.ModelSerializer):
    liker_id = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()

    url = serializers.SerializerMethodField()

    class Meta:
        model = PostLike
        fields = [
            'id',
            'liked_on',
            'liker_id',
            'username',
            'url',
        ]

    def get_liker_id(self, obj):
        return obj['liker_id']

    def get_username(self, obj):
        return obj['liker_name']

    def get_url(self, obj):
        if obj['liker_id']:
            return reverse(
                'misago:user', kwargs={
                    'slug': obj['liker_slug'],
                    'pk': obj['liker_id'],
                }
            )
        else:
            return None
