from rest_framework import serializers

from misago.users.models import UsernameChange

from .user import UserSerializer as BaseUserSerializer


__all__ = ['UsernameChangeSerializer']

UserSerializer = BaseUserSerializer.subset_fields('id', 'username', 'avatars', 'url')


class UsernameChangeSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)
    changed_by = UserSerializer(many=False, read_only=True)

    class Meta:
        model = UsernameChange
        fields = [
            'id',
            'user',
            'changed_by',
            'changed_by_username',
            'changed_on',
            'new_username',
            'old_username',
        ]
