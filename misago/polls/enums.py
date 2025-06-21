from enum import StrEnum

from django.utils.translation import pgettext_lazy


class AllowedPublicPolls(StrEnum):
    ALLOWED = "allowed"
    FORBIDDEN_NEW = "forbidden_new"
    FORBIDDEN = "forbidden"

    @classmethod
    def get_choices(cls):
        return (
            (
                cls.ALLOWED.value,
                pgettext_lazy(
                    "allowed public polls type", "Allow creation of public polls"
                ),
            ),
            (
                cls.FORBIDDEN_NEW.value,
                pgettext_lazy(
                    "allowed public polls", "Forbid creation of new public polls"
                ),
            ),
            (
                cls.FORBIDDEN.value,
                pgettext_lazy("allowed public polls", "Forbid all public polls"),
            ),
        )
