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
    'allow_mark_as_best_answer',
    'can_mark_as_best_answer',
    'allow_unmark_best_answer',
    'can_unmark_best_answer',
]


class CategoryPermissionsForm(forms.Form):
    legend = _("Best answers")

    can_mark_best_answers = forms.TypedChoiceField(
        label=_("Can mark posts as best answers"),
        coerce=int,
        initial=0,
        choices=[
            (0, _("No")),
            (1, _("Own threads")),
            (2, _("All threads")),
        ],
    )
    can_change_marked_answers = forms.TypedChoiceField(
        label=_("Can change marked answers"),
        coerce=int,
        initial=0,
        choices=[
            (0, _("No")),
            (1, _("Own threads")),
            (2, _("All threads")),
        ],
    )
    best_answer_change_time = forms.IntegerField(
        label=_("Time limit for changing marked best answer in owned thread, in minutes"),
        help_text=_("Enter 0 to don't limit time for changing marked best answer in owned thread."),
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
        'can_mark_best_answers': 0,
        'can_change_marked_answers': 0,
        'best_answer_change_time': 0,
    }
    final_acl.update(acl)

    algebra.sum_acls(
        final_acl,
        roles=category_roles,
        key=key_name,
        can_mark_best_answers=algebra.greater,
        can_change_marked_answers=algebra.greater,
        best_answer_change_time=algebra.greater_or_zero,
    )

    return final_acl


def add_acl_to_post(user, post):
    post.acl.update({
        'can_mark_as_best_answer': can_mark_as_best_answer(user, post),
        'can_unmark_best_answer': can_unmark_best_answer(user, post),
    })


def register_with(registry):
    registry.acl_annotator(Post, add_acl_to_post)


def allow_mark_as_best_answer(user, target):
    if user.is_anonymous:
        raise PermissionDenied(_("You have to sign in to mark best answers."))

    if target.is_event:
        raise PermissionDenied(_("Events can't be marked as best answers."))

    category_acl = user.acl_cache['categories'].get(
        target.category_id, {
            'can_mark_best_answers': 0,
        }
    )

    if not category_acl['can_mark_best_answers']:
        raise PermissionDenied(
            _(
                'You don\'t have permission to mark best answers in the "%(category)s" category.'
            ) % {
                'category': target.category,
            }
        )

    if category_acl['can_mark_best_answers'] == 1 and target.thread.starter != user:
        raise PermissionDenied(
            _(
                "You don't have permission to mark best answer in this thread because you "
                "didn't start it."
            )
        )

    if target.is_first_post:
        raise PermissionDenied(_("First post in a thread can't be marked as best answer."))

    if target.is_hidden:
        raise PermissionDenied(_("Hidden posts can't be marked as best answers."))

    if target.is_unapproved:
        raise PermissionDenied(_("Unapproved posts can't be marked as best answers."))

    if target.is_answer:
        raise PermissionDenied(_("This post is already marked as best answer."))

    if target.thread.best_answer_id:
        if not category_acl['can_change_marked_answers']:
            raise PermissionDenied(
                _(
                    'You don\'t have permission to change marked best answers in the '
                    '"%(category)s" category.'
                ) % {
                    'category': target.category,
                }
            )

        if (category_acl['can_change_marked_answers'] == 1 and
                not has_time_to_change_answer(user, target)):
            raise PermissionDenied(
                ungettext(
                    (
                        "You don't have permission to change best answer that was marked for more "
                        "than %(minutes)s minute."
                    ),
                    (
                        "You don't have permission to change best answer that was marked for more "
                        "than %(minutes)s minutes."
                    ),
                    category_acl['answer_change_time'],
                ) % {
                    'minutes': category_acl['answer_change_time'],
                }
            )

        if target.thread.best_answer_is_protected and not category_acl['can_protect_posts']:
            raise PermissionDenied(
                _(
                    "You don't have permission to change this thread's marked best answer because "
                    "a moderator has protected it."
                )
            )
        
    if not category_acl['can_close_threads']:
        if target.category.is_closed:
            raise PermissionDenied(
                _(
                    'You don\'t have permission to mark this post as best answer because its '
                    'category "%(category)s" is closed.'
                ) % {
                    'category': target.category,
                }
            )
        if target.thread.is_closed:
            raise PermissionDenied(
                _(
                    "You can't mark this post as best answer because its thread is closed and you "
                    "don't have permission to open it."
                )
            )

    if target.is_protected and not category_acl['can_protect_posts']:
        raise PermissionDenied(
            _(
                "You don't have permission to mark this post as best answer because a moderator "
                "has protected it."
            )
        )


can_mark_as_best_answer = return_boolean(allow_mark_as_best_answer)


def allow_unmark_best_answer(user, target):
    if user.is_anonymous:
        raise PermissionDenied(_("You have to sign in to unmark best answers."))

    category_acl = user.acl_cache['categories'].get(
        target.category_id, {
            'can_mark_best_answers': 0,
        }
    )

    if not category_acl['can_mark_best_answers']:
        raise PermissionDenied(
            _(
                'You don\'t have permission to unmark threads answers in the "%(category)s" '
                'category.'
            ) % {
                'category': target.category,
            }
        )

    if not target.is_answer:
        raise PermissionDenied(
            _(
                "This post can't be unmarked because it's not currently marked as best answer."
            )
        )

    if category_acl['can_mark_best_answers'] == 1:
        if target.thread.starter != user:
            raise PermissionDenied(
                _(
                    "You don't have permission to unmark this best answer because you are not a "
                    "thread starter."
                )
            )
        if not has_time_to_change_answer(user, target):
            raise PermissionDenied(
                ungettext(
                    (
                        "You don't have permission to unmark best answer that was marked for more "
                        "than %(minutes)s minute."
                    ),
                    (
                        "You don't have permission to unmark best answer that was marked for more "
                        "than %(minutes)s minutes."
                    ),
                    category_acl['answer_change_time'],
                ) % {
                    'minutes': category_acl['answer_change_time'],
                }
            )
        
    if not category_acl['can_close_threads']:
        if target.category.is_closed:
            raise PermissionDenied(
                _(
                    'You don\'t have permission to unmark this best answer because its category '
                    '"%(category)s" is closed.'
                ) % {
                    'category': target.category,
                }
            )
        if target.thread.is_closed:
            raise PermissionDenied(
                _(
                    "You can't unmark this best answer because its thread is closed and you don't "
                    "have permission to open it."
                )
            )

    if target.is_protected and not category_acl['can_protect_posts']:
        raise PermissionDenied(
            _(
                "You don't have permission to unmark this best answer because a moderator has "
                "protected it."
            )
        )


can_unmark_best_answer = return_boolean(allow_unmark_best_answer)


def has_time_to_change_answer(user, target):
    category_acl = user.acl_cache['categories'].get(target.category_id, {})
    change_time = category_acl.get('best_answer_change_time', 0)

    if change_time:
        diff = timezone.now() - target.thread.best_answer_set_on
        diff_minutes = int(diff.total_seconds() / 60)
        return diff_minutes < change_time
    else:
        return True
