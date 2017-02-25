from rest_framework import serializers

from misago.core.utils import format_plaintext_for_html
from misago.users.models import Rank


__all__ = ['RankSerializer']


class RankSerializer(serializers.ModelSerializer):
    description = serializers.SerializerMethodField()
    absolute_url = serializers.SerializerMethodField()

    class Meta:
        model = Rank
        fields = [
            'id',
            'name',
            'slug',
            'description',
            'title',
            'css_class',
            'is_default',
            'is_tab',
            'absolute_url',
        ]

    def get_description(self, obj):
        if obj.description:
            return format_plaintext_for_html(obj.description)
        else:
            return ''

    def get_absolute_url(self, obj):
        return obj.get_absolute_url()
