from django.core.exceptions import ValidationError
from django.utils.module_loading import import_string
from django.utils.translation import ugettext as _
from django.utils.translation import ungettext

from misago.categories import THREADS_ROOT_NAME
from misago.categories.models import Category
from misago.categories.permissions import can_browse_category, can_see_category
from misago.conf import settings
from misago.core.validators import validate_sluggable

from .threadtypes import trees_map


def validate_category(user, category_id, allow_root=False):
    try:
        threads_tree_id = trees_map.get_tree_id_for_root(THREADS_ROOT_NAME)
        category = Category.objects.get(
            tree_id=threads_tree_id,
            id=category_id,
        )
    except Category.DoesNotExist:
        category = None

    # Skip ACL validation for root category?
    if allow_root and category and not category.level:
        return category

    if not category or not can_see_category(user, category):
        raise ValidationError(_("Requested category could not be found."))

    if not can_browse_category(user, category):
        raise ValidationError(_("You don't have permission to access this category."))
    return category


def validate_title(title):
    title_len = len(title)

    if not title_len:
        raise ValidationError(_("You have to enter thread title."))

    if title_len < settings.thread_title_length_min:
        message = ungettext(
            "Thread title should be at least %(limit_value)s character long (it has %(show_value)s).",
            "Thread title should be at least %(limit_value)s characters long (it has %(show_value)s).",
            settings.thread_title_length_min,
        )
        raise ValidationError(
            message % {
                'limit_value': settings.thread_title_length_min,
                'show_value': title_len,
            }
        )

    if title_len > settings.thread_title_length_max:
        message = ungettext(
            "Thread title cannot be longer than %(limit_value)s character (it has %(show_value)s).",
            "Thread title cannot be longer than %(limit_value)s characters (it has %(show_value)s).",
            settings.thread_title_length_max,
        )
        raise ValidationError(
            message % {
                'limit_value': settings.thread_title_length_max,
                'show_value': title_len,
            }
        )

    error_not_sluggable = _("Thread title should contain alpha-numeric characters.")
    error_slug_too_long = _("Thread title is too long.")
    validate_sluggable(error_not_sluggable, error_slug_too_long)(title)

    return title


def validate_post_length(post):
    post_len = len(post)

    if not post_len:
        raise ValidationError(_("You have to enter a message."))

    if post_len < settings.post_length_min:
        message = ungettext(
            "Posted message should be at least %(limit_value)s character long (it has %(show_value)s).",
            "Posted message should be at least %(limit_value)s characters long (it has %(show_value)s).",
            settings.post_length_min,
        )
        raise ValidationError(
            message % {
                'limit_value': settings.post_length_min,
                'show_value': post_len,
            }
        )

    if settings.post_length_max and post_len > settings.post_length_max:
        message = ungettext(
            "Posted message cannot be longer than %(limit_value)s character (it has %(show_value)s).",
            "Posted message cannot be longer than %(limit_value)s characters (it has %(show_value)s).",
            settings.post_length_max,
        )
        raise ValidationError(
            message % {
                'limit_value': settings.post_length_max,
                'show_value': post_len,
            }
        )


# Post validation framework
validators_list = settings.MISAGO_POST_VALIDATORS
POST_VALIDATORS = list(map(import_string, validators_list))


def validate_post(context, data, validators=None):
    validators = validators or POST_VALIDATORS

    for validator in validators:
        data = validator(context, data) or data

    return data
