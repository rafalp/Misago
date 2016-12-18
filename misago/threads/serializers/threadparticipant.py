from rest_framework import serializers

from ..models import ThreadParticipant


__all__ = ['ThreadParticipantSerializer']


class ThreadParticipantSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()
    avatar_hash = serializers.SerializerMethodField()

    url = serializers.SerializerMethodField()

    class Meta:
        model = ThreadParticipant
        fields = (
            'id',
            'username',
            'avatar_hash',
            'url',
            'is_owner'
        )

    def get_id(self, obj):
        return obj.user.id

    def get_username(self, obj):
        return obj.user.username

    def get_avatar_hash(self, obj):
        return obj.user.avatar_hash

    def get_url(self, obj):
        return obj.user.get_absolute_url()
