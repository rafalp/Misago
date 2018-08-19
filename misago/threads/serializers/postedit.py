from rest_framework import serializers

from django.urls import reverse

from misago.threads.models import PostEdit


__all__ = [
    'PostEditSerializer',
]


class PostEditSerializer(serializers.ModelSerializer):
    diff = serializers.SerializerMethodField()

    url = serializers.SerializerMethodField()

    class Meta:
        model = PostEdit
        fields = [
            'id',
            'edited_on',
            'editor_name',
            'editor_slug',
            'diff',
            'url',
        ]

    def get_diff(self, obj):
        return obj.get_diff()

    def get_url(self, obj):
        return {
            'editor': self.get_editor_url(obj),
        }

    def get_editor_url(self, obj):
        if obj.editor_id:
            return reverse(
                'misago:user', kwargs={
                    'slug': obj.editor_slug,
                    'pk': obj.editor_id,
                }
            )
        else:
            return None
