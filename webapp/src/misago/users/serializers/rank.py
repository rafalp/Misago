from rest_framework import serializers

from ...core.utils import format_plaintext_for_html
from ..models import Rank

__all__ = ["RankSerializer"]


class RankSerializer(serializers.ModelSerializer):
    description = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()

    class Meta:
        model = Rank
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "title",
            "css_class",
            "is_default",
            "is_tab",
            "url",
        ]

    def get_description(self, obj):
        if obj.description:
            return format_plaintext_for_html(obj.description)
        return ""

    def get_url(self, obj):
        return obj.get_absolute_url()
