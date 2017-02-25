from rest_framework import serializers


class MockSerializer(serializers.Serializer):
    id = serializers.SerializerMethodField()

    class Meta:
        fields = [
            'id',
        ]

    def get_id(self, obj):
        return obj * 2
