from rest_framework import serializers

from django.urls import reverse
from django.utils.translation import ugettext as _
from django.utils.translation import ungettext


class NewVoteSerializer(serializers.Serializer):
    choices = serializers.ListField(
        child=serializers.CharField(),
    )

    def validate_choices(self, data):
        if len(data) > self.context['allowed_choices']:
            message = ungettext(
                "This poll disallows voting for more than %(choices)s choice.",
                "This poll disallows voting for more than %(choices)s choices.",
                self.context['allowed_choices']
            )
            raise serializers.ValidationError(
                message % {'choices': self.context['allowed_choices']},
            )

        valid_choices = [c['hash'] for c in self.context['choices']]
        clean_choices = []

        for choice in data:
            if choice in valid_choices and choice not in clean_choices:
                clean_choices.append(choice)

        if len(clean_choices) != len(data):
            raise serializers.ValidationError(
                _("One or more of poll choices were invalid."),
            )
        if not len(clean_choices):
            raise serializers.ValidationError(
                _("You have to make a choice."),
            )

        return clean_choices


class PollVoteSerializer(serializers.Serializer):
    id = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()
    slug = serializers.SerializerMethodField()
    voted_on = serializers.DateTimeField()

    class Meta:
        fields = [
            'id',
            'username',
            'slug'
            'voted_on',
        ]

    def get_id(self, obj):
        return obj['voter_id']

    def get_username(self, obj):
        return obj['voter_name']

    def get_slug(self, obj):
        return obj['voter_slug']
