from enum import StrEnum

from django.utils.translation import pgettext_lazy


class PublicPollsAvailability(StrEnum):
    ENABLED = "enabled"
    DISABLED_NEW = "disabled_new"
    DISABLED = "disabled"

    @classmethod
    def get_choices(cls):
        return (
            (
                cls.ENABLED.value,
                pgettext_lazy(
                    "allowed public polls type", "Enable creation of public polls"
                ),
            ),
            (
                cls.DISABLED_NEW.value,
                pgettext_lazy(
                    "allowed public polls", "Disable creation of new public polls"
                ),
            ),
            (
                cls.DISABLED.value,
                pgettext_lazy("allowed public polls", "Disable all public polls"),
            ),
        )


class PollTemplate(StrEnum):
    EDIT = "misago/poll/edit.html"
    RESULTS = "misago/poll/results.html"
    START = "misago/poll/start.html"
    VOTE = "misago/poll/vote.html"
