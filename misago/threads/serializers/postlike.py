from rest_framework import serializers

from django.urls import reverse

from misago.threads.models import PostLike


class PostLikeSerializer(serializers.ModelSerializer):
    avatars = serializers.SerializerMethodField()
    liker_id = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()
    slug = serializers.SerializerMethodField()

    class Meta:
        model = PostLike
        fields = [
            'id',
            'liked_on',
            'liker_id',
            'username',
            'slug',
            'avatars',
        ]
    def get_liker_id(self, obj):
        return obj['liker_id']

    def get_username(self, obj):
        return obj['liker_name']

    def get_slug(self, obj):
        return obj['liker_slug']

    def get_avatars(self, obj):
        return obj.get('liker__avatars')
