from rest_framework import serializers

from misago.threads.models import ThreadParticipant


__all__ = ['ThreadParticipantSerializer']


class ThreadParticipantSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()
    avatars = serializers.SerializerMethodField()

    url = serializers.SerializerMethodField()

    class Meta:
        model = ThreadParticipant
        fields = ['id', 'username', 'avatars', 'url', 'is_owner']

    def get_id(self, obj):
        return obj.user.id

    def get_username(self, obj):
        return obj.user.username

    def get_avatars(self, obj):
        return obj.user.avatars

    def get_url(self, obj):
        return obj.user.get_absolute_url()
