from django.urls import reverse
from django.utils.crypto import get_random_string
from django.utils.translation import gettext as _
from django.utils.translation import ngettext
from rest_framework import serializers

from ..models import Poll

__all__ = [
    "PollSerializer",
    "EditPollSerializer",
    "NewPollSerializer",
    "PollChoiceSerializer",
]

MAX_POLL_OPTIONS = 16


class PollSerializer(serializers.ModelSerializer):
    acl = serializers.SerializerMethodField()
    choices = serializers.SerializerMethodField()

    api = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()

    class Meta:
        model = Poll
        fields = [
            "id",
            "poster_name",
            "posted_on",
            "length",
            "question",
            "allowed_choices",
            "allow_revotes",
            "votes",
            "is_public",
            "acl",
            "choices",
            "api",
            "url",
        ]

    def get_api(self, obj):
        return {"index": obj.get_api_url(), "votes": obj.get_votes_api_url()}

    def get_url(self, obj):
        return {"poster": self.get_poster_url(obj)}

    def get_poster_url(self, obj):
        if obj.poster_id:
            return reverse(
                "misago:user", kwargs={"slug": obj.poster_slug, "pk": obj.poster_id}
            )

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
    choices = serializers.ListField(allow_empty=False, child=serializers.DictField())

    class Meta:
        model = Poll
        fields = ["length", "question", "allowed_choices", "allow_revotes", "choices"]

    def validate_choices(self, choices):
        clean_choices = list(map(self.clean_choice, choices))

        # generate hashes for added choices
        choices_map = {}
        for choice in self.instance.choices:
            choices_map[choice["hash"]] = choice

        final_choices = []
        for choice in clean_choices:
            if choice["hash"] in choices_map:
                choices_map[choice["hash"]].update({"label": choice["label"]})
                final_choices.append(choices_map[choice["hash"]])
            else:
                choice.update({"hash": get_random_string(12), "votes": 0})
                final_choices.append(choice)

        self.validate_choices_num(final_choices)

        return final_choices

    def clean_choice(self, choice):
        clean_choice = {
            "hash": choice.get("hash", get_random_string(12)),
            "label": choice.get("label", ""),
        }

        serializer = PollChoiceSerializer(data=clean_choice)
        if not serializer.is_valid():
            raise serializers.ValidationError(
                _("One or more poll choices are invalid.")
            )

        return serializer.data

    def validate_choices_num(self, choices):
        total_choices = len(choices)

        if total_choices < 2:
            raise serializers.ValidationError(
                _("You need to add at least two choices to a poll.")
            )

        if total_choices > MAX_POLL_OPTIONS:
            # pylint: disable=line-too-long
            message = ngettext(
                "You can't add more than %(limit_value)s option to a single poll (added %(show_value)s).",
                "You can't add more than %(limit_value)s options to a single poll (added %(show_value)s).",
                MAX_POLL_OPTIONS,
            )
            raise serializers.ValidationError(
                message % {"limit_value": MAX_POLL_OPTIONS, "show_value": total_choices}
            )

    def validate(self, data):
        if data["allowed_choices"] > len(data["choices"]):
            raise serializers.ValidationError(
                _(
                    "Number of allowed choices can't be "
                    "greater than number of all choices."
                )
            )
        return data

    def update(self, instance, validated_data):
        if instance.choices:
            self.update_choices(instance, validated_data["choices"])

        return super().update(instance, validated_data)

    def update_choices(self, instance, cleaned_choices):
        removed_hashes = []

        final_hashes = [c["hash"] for c in cleaned_choices]
        for choice in instance.choices:
            if choice["hash"] not in final_hashes:
                instance.votes -= choice["votes"]
                removed_hashes.append(choice["hash"])

        if removed_hashes:
            instance.pollvote_set.filter(choice_hash__in=removed_hashes).delete()


class NewPollSerializer(EditPollSerializer):
    class Meta:
        model = Poll
        fields = [
            "length",
            "question",
            "allowed_choices",
            "allow_revotes",
            "is_public",
            "choices",
        ]

    def validate_choices(self, choices):
        clean_choices = list(map(self.clean_choice, choices))

        self.validate_choices_num(clean_choices)

        for choice in clean_choices:
            choice.update({"hash": get_random_string(12), "votes": 0})

        return clean_choices


class PollChoiceSerializer(serializers.Serializer):
    hash = serializers.CharField(required=True, min_length=12, max_length=12)
    label = serializers.CharField(required=True, max_length=255)
