from django.core.urlresolvers import reverse
from django.utils.crypto import get_random_string
from django.utils.translation import ugettext as _, ungettext

from rest_framework import serializers

from ..models import Poll


MAX_POLL_OPTIONS = 16


class PollSerializer(serializers.ModelSerializer):
    acl = serializers.SerializerMethodField()
    choices = serializers.SerializerMethodField()

    api = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()

    class Meta:
        model = Poll
        fields = (
            'poster_name',
            'poster_slug',
            'posted_on',
            'length',
            'question',
            'allowed_choices',
            'allow_revotes',
            'votes',
            'is_public',

            'acl',
            'choices',

            'api',
            'url',
        )

    def get_api(self, obj):
        return {
            'index': reverse('misago:api:thread-poll-list', kwargs={
                'thread_pk': obj.thread_id
            }),
        }

    def get_url(self, obj):
        return {
            'poster': self.get_last_poster_url(obj),
        }

    def get_last_poster_url(self, obj):
        if obj.poster_id:
            return reverse('misago:user', kwargs={
                'slug': obj.poster_slug,
                'pk': obj.poster_id,
            })
        else:
            return None

    def get_acl(self, obj):
        try:
            return obj.acl
        except AttributeError:
            return None

    def get_choices(self, obj):
        return obj.choices


class EditPollSerializer(serializers.ModelSerializer):
    length = serializers.IntegerField(required=True, min_value=0, max_value=180)
    question = serializers.CharField(required=True, max_length=255)
    allowed_choices = serializers.IntegerField(required=True, min_value=1)
    choices = serializers.ListField(
       allow_empty=False,
       child=serializers.DictField(),
    )

    class Meta:
        model = Poll
        fields = (
            'length',
            'question',
            'allowed_choices',
            'allow_revotes',
            'choices',
        )

    def validate_choices(self, choices):
        clean_choices = map(self.clean_choice, choices)

    def clean_choice(self, choice):
        clean_choice = {
            'hash': choice.get('hash', get_random_string(12)),
            'label': choice.get('label', ''),
        }

        serializer = PollChoiceSerializer(data=clean_choice)
        if not serializer.is_valid():
            raise serializers.ValidationError(_("One or more poll choices are invalid."))

        return serializer.data

    def validate_choices_num(self, choices):
        total_choices = len(choices)

        if total_choices < 2:
            raise serializers.ValidationError(_("You need to add at least two choices to a poll."))

        if total_choices > MAX_POLL_OPTIONS:
            message = ungettext(
                "You can't add more than %(limit_value)s option to a single poll (added %(show_value)s).",
                "You can't add more than %(limit_value)s options to a single poll (added %(show_value)s).",
                MAX_POLL_OPTIONS)
            raise serializers.ValidationError(message % {
                'limit_value': MAX_POLL_OPTIONS,
                'show_value': total_choices
            })

    def validate(self, data):
        if data['allowed_choices'] > len(data['choices']):
            raise serializers.ValidationError(
                _("Number of allowed choices can't be greater than number of all choices."))
        return data


class NewPollSerializer(EditPollSerializer):
    class Meta:
        model = Poll
        fields = (
            'length',
            'question',
            'allowed_choices',
            'allow_revotes',
            'is_public',
            'choices',
        )

    def validate_choices(self, choices):
        clean_choices = map(self.clean_choice, choices)

        self.validate_choices_num(clean_choices)

        for choice in clean_choices:
            choice.update({
                'hash': get_random_string(12),
                'votes': 0
            })

        return clean_choices


class PollChoiceSerializer(serializers.Serializer):
    hash = serializers.CharField(required=True, min_length=12, max_length=12)
    label = serializers.CharField(required=True, max_length=255)

