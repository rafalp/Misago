from rest_framework import serializers

from ..threads.validators import validate_post_length


class MarkupSerializer(serializers.Serializer):
    post = serializers.CharField(required=False, allow_blank=True)

    def validate(self, data):
        settings = self.context["settings"]
        validate_post_length(settings, data.get("post", ""))
        return data
