from rest_framework import serializers


class MarkupSerializer(serializers.Serializer):
    post = serializers.CharField(required=False, allow_blank=True)

    def validate(self, data):
        return data
