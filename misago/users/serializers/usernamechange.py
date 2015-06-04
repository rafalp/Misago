from rest_framework import serializers

from misago.users.models import UsernameChange
from misago.users.serializers.user import BasicUserSerializer


class UsernameChangeSerializer(serializers.ModelSerializer):
    user = BasicUserSerializer(many=False, read_only=True)
    changed_by = BasicUserSerializer(many=False, read_only=True)

    class Meta:
        model = UsernameChange
        fields = (
            'id',
            'user',
            'changed_by',
            'changed_by_username',
            'changed_on',
            'new_username',
            'old_username'
        )
