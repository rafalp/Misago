from django import forms
from django.core.exceptions import PermissionDenied
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.utils.translation import ngettext

from ...acl import algebra
from ...acl.decorators import return_boolean
from ...categories.models import Category, CategoryRole
from ...categories.permissions import get_categories_roles
from ..models import Post, Thread

__all__nope = [
    "allow_mark_best_answer",
    "can_mark_best_answer",
    "allow_mark_as_best_answer",
    "can_mark_as_best_answer",
    "allow_unmark_best_answer",
    "can_unmark_best_answer",
    "allow_hide_best_answer",
    "can_hide_best_answer",
    "allow_delete_best_answer",
    "can_delete_best_answer",
]


class CategoryPermissionsForm(forms.Form):
    legend = _("Best answers")

    can_mark_best_answers = forms.TypedChoiceField(
        label=_("Can mark posts as best answers"),
        coerce=int,
        initial=0,
        choices=[(0, _("No")), (1, _("Own threads")), (2, _("All threads"))],
    )
    can_change_marked_answers = forms.TypedChoiceField(
        label=_("Can change marked answers"),
        coerce=int,
        initial=0,
        choices=[(0, _("No")), (1, _("Own threads")), (2, _("All threads"))],
    )
    best_answer_change_time = forms.IntegerField(
        label=_(
            "Time limit for changing marked best answer in owned thread, in minutes"
        ),
        help_text=_(
            "Enter 0 to don't limit time for changing marked best answer in "
            "owned thread."
        ),
        initial=0,
        min_value=0,
    )


def change_permissions_form(role):
    if isinstance(role, CategoryRole):
        return CategoryPermissionsForm


def build_acl(acl, roles, key_name):
    categories_roles = get_categories_roles(roles)
    categories = list(Category.objects.all_categories(include_root=True))

    for category in categories:
        category_acl = acl["categories"].get(category.pk, {"can_browse": 0})
        if category_acl["can_browse"]:
            acl["categories"][category.pk] = build_category_acl(
                category_acl, category, categories_roles, key_name
            )

    private_category = Category.objects.private_threads()
    private_threads_acl = acl["categories"].get(private_category.pk)
    if private_threads_acl:
        private_threads_acl.update(
            {
                "can_mark_best_answers": 0,
                "can_change_marked_answers": 0,
                "best_answer_change_time": 0,
            }
        )

    return acl


def build_category_acl(acl, category, categories_roles, key_name):
    category_roles = categories_roles.get(category.pk, [])

    final_acl = {
        "can_mark_best_answers": 0,
        "can_change_marked_answers": 0,
        "best_answer_change_time": 0,
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


def add_acl_to_thread(user_acl, thread):
    thread.acl.update(
        {
            "can_mark_best_answer": can_mark_best_answer(user_acl, thread),
            "can_change_best_answer": can_change_best_answer(user_acl, thread),
            "can_unmark_best_answer": can_unmark_best_answer(user_acl, thread),
        }
    )


def add_acl_to_post(user_acl, post):
    post.acl.update(
        {
            "can_mark_as_best_answer": can_mark_as_best_answer(user_acl, post),
            "can_hide_best_answer": can_hide_best_answer(user_acl, post),
            "can_delete_best_answer": can_delete_best_answer(user_acl, post),
        }
    )


def register_with(registry):
    registry.acl_annotator(Thread, add_acl_to_thread)
    registry.acl_annotator(Post, add_acl_to_post)


def allow_mark_best_answer(user_acl, target):
    if user_acl["is_anonymous"]:
        raise PermissionDenied(_("You have to sign in to mark best answers."))

    category_acl = user_acl["categories"].get(target.category_id, {})

    if not category_acl.get("can_mark_best_answers"):
        raise PermissionDenied(
            _(
                "You don't have permission to mark best answers in the "
                '"%(category)s" category.'
            )
            % {"category": target.category}
        )

    if (
        category_acl["can_mark_best_answers"] == 1
        and user_acl["user_id"] != target.starter_id
    ):
        raise PermissionDenied(
            _(
                "You don't have permission to mark best answer in this thread "
                "because you didn't start it."
            )
        )

    if not category_acl["can_close_threads"]:
        if target.category.is_closed:
            raise PermissionDenied(
                _(
                    "You don't have permission to mark best answer in this thread "
                    'because its category "%(category)s" is closed.'
                )
                % {"category": target.category}
            )
        if target.is_closed:
            raise PermissionDenied(
                _(
                    "You can't mark best answer in this thread because it's closed "
                    "and you don't have permission to open it."
                )
            )


can_mark_best_answer = return_boolean(allow_mark_best_answer)


def allow_change_best_answer(user_acl, target):
    if not target.has_best_answer:
        return  # shortcircut permission test

    category_acl = user_acl["categories"].get(target.category_id, {})

    if not category_acl.get("can_change_marked_answers"):
        raise PermissionDenied(
            _(
                "You don't have permission to change this thread's marked answer "
                'because it\'s in the "%(category)s" category.'
            )
            % {"category": target.category}
        )

    if category_acl["can_change_marked_answers"] == 1:
        if user_acl["user_id"] != target.starter_id:
            raise PermissionDenied(
                _(
                    "You don't have permission to change this thread's marked answer "
                    "because you are not a thread starter."
                )
            )
        if not has_time_to_change_answer(user_acl, target):
            # pylint: disable=line-too-long
            message = ngettext(
                "You don't have permission to change best answer that was marked for more than %(minutes)s minute.",
                "You don't have permission to change best answer that was marked for more than %(minutes)s minutes.",
                category_acl["best_answer_change_time"],
            )
            raise PermissionDenied(
                message % {"minutes": category_acl["best_answer_change_time"]}
            )

    if target.best_answer_is_protected and not category_acl["can_protect_posts"]:
        raise PermissionDenied(
            _(
                "You don't have permission to change this thread's best answer "
                "because a moderator has protected it."
            )
        )


can_change_best_answer = return_boolean(allow_change_best_answer)


def allow_unmark_best_answer(user_acl, target):
    if user_acl["is_anonymous"]:
        raise PermissionDenied(_("You have to sign in to unmark best answers."))

    if not target.has_best_answer:
        return  # shortcircut test

    category_acl = user_acl["categories"].get(target.category_id, {})

    if not category_acl.get("can_change_marked_answers"):
        raise PermissionDenied(
            _(
                "You don't have permission to unmark threads answers in "
                'the "%(category)s" category.'
            )
            % {"category": target.category}
        )

    if category_acl["can_change_marked_answers"] == 1:
        if user_acl["user_id"] != target.starter_id:
            raise PermissionDenied(
                _(
                    "You don't have permission to unmark this best answer "
                    "because you are not a thread starter."
                )
            )
        if not has_time_to_change_answer(user_acl, target):
            # pylint: disable=line-too-long
            message = ngettext(
                "You don't have permission to unmark best answer that was marked for more than %(minutes)s minute.",
                "You don't have permission to unmark best answer that was marked for more than %(minutes)s minutes.",
                category_acl["best_answer_change_time"],
            )
            raise PermissionDenied(
                message % {"minutes": category_acl["best_answer_change_time"]}
            )

    if not category_acl["can_close_threads"]:
        if target.category.is_closed:
            raise PermissionDenied(
                _(
                    "You don't have permission to unmark this best answer "
                    'because its category "%(category)s" is closed.'
                )
                % {"category": target.category}
            )
        if target.is_closed:
            raise PermissionDenied(
                _(
                    "You can't unmark this thread's best answer "
                    "because it's closed and you don't have permission to open it."
                )
            )

    if target.best_answer_is_protected and not category_acl["can_protect_posts"]:
        raise PermissionDenied(
            _(
                "You don't have permission to unmark this thread's best answer "
                "because a moderator has protected it."
            )
        )


can_unmark_best_answer = return_boolean(allow_unmark_best_answer)


def allow_mark_as_best_answer(user_acl, target):
    if user_acl["is_anonymous"]:
        raise PermissionDenied(_("You have to sign in to mark best answers."))

    if target.is_event:
        raise PermissionDenied(_("Events can't be marked as best answers."))

    category_acl = user_acl["categories"].get(target.category_id, {})

    if not category_acl.get("can_mark_best_answers"):
        raise PermissionDenied(
            _(
                "You don't have permission to mark best answers "
                'in the "%(category)s" category.'
            )
            % {"category": target.category}
        )

    if (
        category_acl["can_mark_best_answers"] == 1
        and user_acl["user_id"] != target.thread.starter_id
    ):
        raise PermissionDenied(
            _(
                "You don't have permission to mark best answer in this thread "
                "because you didn't start it."
            )
        )

    if target.is_first_post:
        raise PermissionDenied(
            _("First post in a thread can't be marked as best answer.")
        )

    if target.is_hidden:
        raise PermissionDenied(_("Hidden posts can't be marked as best answers."))

    if target.is_unapproved:
        raise PermissionDenied(_("Unapproved posts can't be marked as best answers."))

    if target.is_protected and not category_acl["can_protect_posts"]:
        raise PermissionDenied(
            _(
                "You don't have permission to mark this post as best answer "
                "because a moderator has protected it."
            )
        )


can_mark_as_best_answer = return_boolean(allow_mark_as_best_answer)


def allow_hide_best_answer(user_acl, target):
    if target.is_best_answer:
        raise PermissionDenied(
            _("You can't hide this post because its marked as best answer.")
        )


can_hide_best_answer = return_boolean(allow_hide_best_answer)


def allow_delete_best_answer(user_acl, target):
    if target.is_best_answer:
        raise PermissionDenied(
            _("You can't delete this post because its marked as best answer.")
        )


can_delete_best_answer = return_boolean(allow_delete_best_answer)


def has_time_to_change_answer(user_acl, target):
    category_acl = user_acl["categories"].get(target.category_id, {})
    change_time = category_acl.get("best_answer_change_time", 0)

    if change_time:
        diff = timezone.now() - target.best_answer_marked_on
        diff_minutes = int(diff.total_seconds() / 60)
        return diff_minutes < change_time

    return True
