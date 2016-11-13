from django.core.urlresolvers import reverse

from rest_framework import serializers


class PollVoteSerializer(serializers.Serializer):
    voted_on = serializers.DateTimeField()
    username = serializers.SerializerMethodField()
    slug = serializers.SerializerMethodField()

    url = serializers.SerializerMethodField()

    class Meta:
        fields = (
            'voted_on',

            'username',
            'slug',

            'url',
        )

    def get_username(self, obj):
        return obj['voter_name']

    def get_slug(self, obj):
        return obj['voter_slug']

    def get_url(self, obj):
        if obj['voter_id']:
            return reverse('misago:user', kwargs={
                'pk': obj['voter_id'],
                'slug': obj['voter_slug'],
            })
