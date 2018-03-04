from django import forms
from django.core.exceptions import PermissionDenied
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _, ungettext

from misago.acl import algebra
from misago.acl.decorators import return_boolean
from misago.categories.models import Category, CategoryRole
from misago.categories.permissions import get_categories_roles
from misago.core.forms import YesNoSwitch
from misago.threads.models import Post


__all__nope = [
    'allow_select_answer',
    'can_select_answer',
    'allow_remove_answer',
    'can_remove_answer',
]


class CategoryPermissionsForm(forms.Form):
    legend = _("Answers")

    can_set_answers = forms.TypedChoiceField(
        label=_("Can set answers"),
        coerce=int,
        initial=0,
        choices=[
            (0, _("No")),
            (1, _("Own threads")),
            (2, _("All threads")),
        ],
    )
    can_change_answers = forms.TypedChoiceField(
        label=_("Can change answers"),
        coerce=int,
        initial=0,
        choices=[
            (0, _("No")),
            (1, _("Own threads")),
            (2, _("All threads")),
        ],
    )
    answer_change_time = forms.IntegerField(
        label=_("Time limit for owned thread answer change, in minutes"),
        help_text=_("Enter 0 to don't limit time for changing own thread answer."),
        initial=0,
        min_value=0,
    )


def change_permissions_form(role):
    if isinstance(role, CategoryRole):
        return CategoryPermissionsForm
    else:
        return None


def build_acl(acl, roles, key_name):
    categories_roles = get_categories_roles(roles)
    categories = list(Category.objects.all_categories(include_root=True))

    for category in categories:
        category_acl = acl['categories'].get(category.pk, {'can_browse': 0})
        if category_acl['can_browse']:
            category_acl = acl['categories'][category.pk] = build_category_acl(
                category_acl, category, categories_roles, key_name
            )

    return acl


def build_category_acl(acl, category, categories_roles, key_name):
    category_roles = categories_roles.get(category.pk, [])

    final_acl = {
        'can_set_answers': 0,
        'can_change_answers': 0,
        'answer_change_time': 0,
    }
    final_acl.update(acl)

    algebra.sum_acls(
        final_acl,
        roles=category_roles,
        key=key_name,
        can_set_answers=algebra.greater,
        can_change_answers=algebra.greater,
        answer_change_time=algebra.greater_or_zero,
    )

    return final_acl


def add_acl_to_post(user, post):
    post.acl.update({
        'can_set_answer': can_set_answer(user, post),
        'can_unset_answer': can_unset_answer(user, post),
    })


def register_with(registry):
    registry.acl_annotator(Post, add_acl_to_post)


def allow_set_answer(user, target):
    if user.is_anonymous:
        raise PermissionDenied(_("You have to sign in to set posts as answers."))

    if target.is_event:
        raise PermissionDenied(_("Events can't be set as answers."))

    category_acl = user.acl_cache['categories'].get(
        target.category_id, {
            'can_set_answers': 0,
        }
    )

    if not category_acl['can_set_answers']:
        raise PermissionDenied(
            _(
                'You don\'t have permission to set answers in the "%(category)s" category.'
            ) % {
                'category': target.category,
            }
        )

    if category_acl['can_set_answers'] == 1 and target.thread.starter != user:
        raise PermissionDenied(
            _(
                "You dont't have permission to set this post as an answer "
                "because you are not the thread starter."
            )
        )

    if target.is_first_post:
        raise PermissionDenied(_("First post in a thread can't be set as an answer."))

    if target.is_hidden:
        raise PermissionDenied(_("Hidden posts can't be set as answers."))

    if target.is_unapproved:
        raise PermissionDenied(_("Unapproved posts can't be set as answers."))

    if target.is_answer:
        raise PermissionDenied(_("This post is already set as an answer."))

    if category_acl['can_set_answers'] == 1 and target.thread.answer_id:
        if not has_time_to_change_answer(user, target):
            raise PermissionDenied(
                ungettext(
                    (
                        "You don't have permission to change thread's answer that was set "
                        "for more than %(minutes)s minute."),
                    (
                        "You don't have permission to change thread's answer that was set "
                        "for more than %(minutes)s minutes."),
                    category_acl['answer_change_time'],
                ) % {
                    'minutes': category_acl['answer_change_time'],
                }
            )

        if target.thread.answer_is_protected and not category_acl['can_protect_posts']:
            raise PermissionDenied(
                _(
                    "You don't have permission to change this thread's answer because moderator "
                    "has protected it."
                )
            )
        
    if not category_acl['can_close_threads']:
        if target.category.is_closed:
            raise PermissionDenied(
                _(
                    'You can\'t sets this post as an answer because it\'s category '
                    '"%(category)s" is closed.'
                ) % {
                    'category': target.category,
                }
            )
        if target.thread.is_closed:
            raise PermissionDenied(
                _(
                    "You can't set this post as an answer because it's thread is closed and you "
                    "don't have permission to open it."
                )
            )

    if target.is_protected and not category_acl['can_protect_posts']:
        raise PermissionDenied(
            _("You can't sets this post as an answer because moderator has protected it.")
        )


can_set_answer = return_boolean(allow_set_answer)


def allow_unset_answer(user, target):
    if user.is_anonymous:
        raise PermissionDenied(_("You have to sign in to unset threads answers."))

    category_acl = user.acl_cache['categories'].get(
        target.category_id, {
            'can_change_answers': 0,
        }
    )

    if not category_acl['can_change_answers']:
        raise PermissionDenied(
            _(
                'You don\'t have permission to unset threads answers in the "%(category)s" '
                'category.'
            ) % {
                'category': target.category,
            }
        )

    if not target.is_answer:
        raise PermissionDenied(
            _(
                "You can't unset."
            )
        )

    if category_acl['can_change_answers'] == 1 and target.thread.starter != user:
        raise PermissionDenied(
            _(
                "You dont't have permission to unset this answer because "
                "you are not a thread starter."
            )
        )
        
    if not category_acl['can_close_threads']:
        if target.category.is_closed:
            raise PermissionDenied(
                _(
                    'You can\'t unset this answer because it\'s scategory "%(category)s" is closed.'
                ) % {
                    'category': target.category,
                }
            )
        if target.thread.is_closed:
            raise PermissionDenied(
                _(
                    "You don't have permission to unset this answer because it's thread is closed "
                    "and you don't have permission to open it."
                )
            )

    if target.is_protected and not category_acl['can_protect_posts']:
        raise PermissionDenied(
            _(
                "You don't have permission to unset this thread's answer because moderator has "
                "protected it."
            )
        )


can_unset_answer = return_boolean(allow_unset_answer)


def has_time_to_change_answer(user, target):
    category_acl = user.acl_cache['categories'].get(target.category_id, {})
    change_time = category_acl.get('answer_change_time', 0)

    if change_time:
        diff = timezone.now() - target.thread.answer_set_on
        diff_minutes = int(diff.total_seconds() / 60)
        return diff_minutes < change_time
    else:
        return True
