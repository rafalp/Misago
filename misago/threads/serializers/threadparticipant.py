from rest_framework import serializers

from misago.threads.models import ThreadParticipant


class ThreadParticipantSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()
    slug = serializers.SerializerMethodField()
    avatars = serializers.SerializerMethodField()

    class Meta:
        model = ThreadParticipant
        fields = ['id', 'username', 'slug', 'avatars', 'is_owner']

    def get_id(self, obj):
        return obj.user.id

    def get_username(self, obj):
        return obj.user.username

    def get_slug(self, obj):
        return obj.user.slug

    def get_avatars(self, obj):
        return obj.user.avatars
