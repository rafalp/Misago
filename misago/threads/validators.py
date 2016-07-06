from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext

from misago.conf import settings
from misago.core.validators import validate_sluggable


def validate_title(title):
    title_len = len(title)

    if not title_len:
        raise ValidationError(_("Enter thread title."))

    if title_len < settings.thread_title_length_min:
        message = ungettext(
            "Thread title should be at least %(limit)s character long.",
            "Thread title should be at least %(limit)s characters long.",
            settings.thread_title_length_min)
        message = message % {'limit': settings.thread_title_length_min}
        raise ValidationError(message)

    if title_len > settings.thread_title_length_max:
        message = ungettext(
            "Thread title can't be longer than %(limit)s character.",
            "Thread title can't be longer than %(limit)s characters.",
            settings.thread_title_length_max,)
        message = message % {'limit': settings.thread_title_length_max}
        raise ValidationError(message)

    error_not_sluggable = _("Thread title should contain "
                            "alpha-numeric characters.")
    error_slug_too_long = _("Thread title is too long.")
    slug_validator = validate_sluggable(error_not_sluggable,
                                        error_slug_too_long)
    slug_validator(title)
    return title
