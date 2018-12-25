from django.urls import reverse
from django.utils.translation import gettext as _
from django.utils.translation import ngettext
from rest_framework import serializers

__all__ = ["NewVoteSerializer", "PollVoteSerializer"]


class NewVoteSerializer(serializers.Serializer):
    choices = serializers.ListField(child=serializers.CharField())

    def validate_choices(self, data):
        if len(data) > self.context["allowed_choices"]:
            message = ngettext(
                "This poll disallows voting for more than %(choices)s choice.",
                "This poll disallows voting for more than %(choices)s choices.",
                self.context["allowed_choices"],
            )
            raise serializers.ValidationError(
                message % {"choices": self.context["allowed_choices"]}
            )

        valid_choices = [c["hash"] for c in self.context["choices"]]
        clean_choices = []

        for choice in data:
            if choice in valid_choices and choice not in clean_choices:
                clean_choices.append(choice)

        if len(clean_choices) != len(data):
            raise serializers.ValidationError(
                _("One or more of poll choices were invalid.")
            )

        if not clean_choices:
            raise serializers.ValidationError(_("You have to make a choice."))

        return clean_choices


class PollVoteSerializer(serializers.Serializer):
    voted_on = serializers.DateTimeField()
    username = serializers.SerializerMethodField()

    url = serializers.SerializerMethodField()

    class Meta:
        fields = ["voted_on", "username", "url"]

    def get_username(self, obj):
        return obj["voter_name"]

    def get_url(self, obj):
        if obj["voter_id"]:
            return reverse(
                "misago:user", kwargs={"pk": obj["voter_id"], "slug": obj["voter_slug"]}
            )
