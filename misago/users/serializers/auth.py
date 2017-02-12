from rest_framework import serializers

from misago.acl import serialize_acl


class AuthenticatedUserSerializer(serializers.ModelSerializer):
    is_authenticated = serializers.SerializerMethodField()

    def get_is_authenticated(self, obj):
        return False
    pass


class AnonymousUserSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    acl = serializers.SerializerMethodField()
    is_authenticated = serializers.SerializerMethodField()

    def get_acl(self, obj):
        if hasattr(obj, 'acl'):
            return serialize_acl(obj)
        else:
            return {}

    def get_is_authenticated(self, obj):
        return False
