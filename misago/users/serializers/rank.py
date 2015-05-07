from rest_framework import serializers

from misago.users.models import Rank


__ALL__ = ['RankSerializer']


class RankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rank
        fields = (
            'id',
            'name',
            'slug',
            'description',
            'title',
            'css_class',
            'is_tab')
