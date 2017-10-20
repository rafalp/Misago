from rest_framework import serializers

from misago.threads.validators import validate_post_length


class MarkupSerializer(serializers.Serializer):
    post = serializers.CharField(required=False, allow_blank=True)

    def validate(self, data):
        validate_post_length(data.get('post', ''))
        return data
