from rest_framework import serializers

from django.urls import reverse

from misago.threads.models import PostEdit


class PostEditSerializer(serializers.ModelSerializer):
    editor = serializers.PrimaryKeyRelatedField(read_only=True)
    diff = serializers.SerializerMethodField()

    class Meta:
        model = PostEdit
        fields = [
            'id',
            'edited_on',
            'editor',
            'editor_name',
            'editor_slug',
            'diff',
        ]

    def get_diff(self, obj):
        return obj.get_diff()
