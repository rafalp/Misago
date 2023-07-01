from django.core.exceptions import ValidationError
from django.utils.module_loading import import_string
from django.utils.translation import npgettext, pgettext

from .. import hooks
from ..categories import THREADS_ROOT_NAME
from ..categories.models import Category
from ..categories.permissions import can_browse_category, can_see_category
from ..conf import settings
from ..core.validators import validate_sluggable
from .threadtypes import trees_map


def validate_category(user_acl, category_id, allow_root=False):
    try:
        threads_tree_id = trees_map.get_tree_id_for_root(THREADS_ROOT_NAME)
        category = Category.objects.get(tree_id=threads_tree_id, id=category_id)
    except Category.DoesNotExist:
        category = None

    # Skip ACL validation for root category?
    if allow_root and category and not category.level:
        return category

    if not category or not can_see_category(user_acl, category):
        raise ValidationError(
            pgettext(
                "thread category validator", "Requested category could not be found."
            )
        )

    if not can_browse_category(user_acl, category):
        raise ValidationError(
            pgettext(
                "thread category validator",
                "You don't have permission to access this category.",
            )
        )
    return category


def validate_thread_title(settings, title):
    validate_thread_title_length(settings, title)

    error_not_sluggable = pgettext(
        "thread title validator",
        "Thread title should contain alpha-numeric characters.",
    )
    error_slug_too_long = pgettext(
        "thread title validator", "Thread title is too long."
    )
    validate_sluggable(error_not_sluggable, error_slug_too_long)(title)


def validate_thread_title_length(settings, value):
    value_len = len(value)

    if not value_len:
        raise ValidationError(
            pgettext(
                "thread title length validator", "You have to enter an thread title."
            )
        )

    if value_len < settings.thread_title_length_min:
        # pylint: disable=line-too-long
        message = npgettext(
            "thread title length validator",
            "Thread title should be at least %(limit_value)s character long (it has %(show_value)s).",
            "Thread title should be at least %(limit_value)s characters long (it has %(show_value)s).",
            settings.thread_title_length_min,
        )
        raise ValidationError(
            message
            % {"limit_value": settings.thread_title_length_min, "show_value": value_len}
        )

    if value_len > settings.thread_title_length_max:
        # pylint: disable=line-too-long
        message = npgettext(
            "thread title length validator",
            "Thread title cannot be longer than %(limit_value)s character (it has %(show_value)s).",
            "Thread title cannot be longer than %(limit_value)s characters (it has %(show_value)s).",
            settings.thread_title_length_max,
        )
        raise ValidationError(
            message
            % {"limit_value": settings.thread_title_length_max, "show_value": value_len}
        )


def validate_post_length(settings, value):
    value_len = len(value)

    if not value_len:
        raise ValidationError(
            pgettext("post length validator", "You have to enter a message.")
        )

    if value_len < settings.post_length_min:
        # pylint: disable=line-too-long
        message = npgettext(
            "post length validator",
            "Posted message should be at least %(limit_value)s character long (it has %(show_value)s).",
            "Posted message should be at least %(limit_value)s characters long (it has %(show_value)s).",
            settings.post_length_min,
        )
        raise ValidationError(
            message % {"limit_value": settings.post_length_min, "show_value": value_len}
        )

    if settings.post_length_max and value_len > settings.post_length_max:
        # pylint: disable=line-too-long
        message = npgettext(
            "post length validator",
            "Posted message cannot be longer than %(limit_value)s character (it has %(show_value)s).",
            "Posted message cannot be longer than %(limit_value)s characters (it has %(show_value)s).",
            settings.post_length_max,
        )
        raise ValidationError(
            message % {"limit_value": settings.post_length_max, "show_value": value_len}
        )


# Post validation framework
validators_list = settings.MISAGO_POST_VALIDATORS
POST_VALIDATORS = list(map(import_string, validators_list))


def validate_post(context, data, validators=None):
    validators = validators or POST_VALIDATORS

    for validator in validators:
        data = validator(context, data) or data
    for validator in hooks.post_validators:
        data = validator(context, data) or data

    return data
