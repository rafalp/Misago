from django.core.exceptions import ValidationError
from django.utils.translation import npgettext


def validate_attachments_limit(value: int, limit_value: int):
    if value > limit_value:
        raise ValidationError(
            message=npgettext(
                "attachments limit validator",
                "Posted message cannot have more than %(limit_value)s attachment (it currently has %(show_value)s).",
                "Posted message cannot have more than %(limit_value)s attachments (it currently has %(show_value)s).",
                limit_value,
            ),
            code="attachments_limit",
            params={
                "limit_value": limit_value,
                "show_value": value,
            },
        )
