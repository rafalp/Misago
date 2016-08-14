from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _, ungettext

from misago.conf import settings
from misago.core.validators import validate_sluggable


def validate_post(post):
    post_len = len(post)

    if not post_len:
        raise ValidationError(_("You have to enter a message."))

    if post_len < settings.post_length_min:
        message = ungettext(
            "Posted message should be at least %(limit_value)s character long (it has %(show_value)s).",
            "Posted message should be at least %(limit_value)s characters long (it has %(show_value)s).",
            settings.post_length_min)
        raise ValidationError(message % {
            'limit_value': settings.post_length_min,
            'show_value': post_len
        })

    if settings.post_length_max and post_len > settings.post_length_max:
        message = ungettext(
            "Posted message cannot be longer than %(limit_value)s character (it has %(show_value)s).",
            "Posted message cannot be longer than %(limit_value)s characters (it has %(show_value)s).",
            settings.post_length_max)
        raise ValidationError(message % {
            'limit_value': settings.post_length_max,
            'show_value': post_len
        })


def validate_title(title):
    title_len = len(title)

    if not title_len:
        raise ValidationError(_("You have to enter thread title."))

    if title_len < settings.thread_title_length_min:
        message = ungettext(
            "Thread title should be at least %(limit_value)s character long (it has %(show_value)s).",
            "Thread title should be at least %(limit_value)s characters long (it has %(show_value)s).",
            settings.thread_title_length_min)
        raise ValidationError(message % {
            'limit_value': settings.thread_title_length_min,
            'show_value': title_len
        })

    if title_len > settings.thread_title_length_max:
        message = ungettext(
            "Thread title cannot be longer than %(limit_value)s character (it has %(show_value)s).",
            "Thread title cannot be longer than %(limit_value)s characters (it has %(show_value)s).",
            settings.thread_title_length_max)
        raise ValidationError(message % {
            'limit_value': settings.thread_title_length_max,
            'show_value': title_len
        })

    error_not_sluggable = _("Thread title should contain alpha-numeric characters.")
    error_slug_too_long = _("Thread title is too long.")
    validate_sluggable(error_not_sluggable, error_slug_too_long)(title)

    return title
