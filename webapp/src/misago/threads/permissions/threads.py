from django import forms
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.http import Http404
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.utils.translation import ngettext

from ...acl import algebra
from ...acl.decorators import return_boolean
from ...acl.models import Role
from ...acl.objectacl import add_acl_to_obj
from ...admin.forms import YesNoSwitch
from ...categories.models import Category, CategoryRole
from ...categories.permissions import get_categories_roles
from ..models import Post, Thread

__all__ = [
    "allow_see_thread",
    "can_see_thread",
    "allow_start_thread",
    "can_start_thread",
    "allow_reply_thread",
    "can_reply_thread",
    "allow_edit_thread",
    "can_edit_thread",
    "allow_pin_thread",
    "can_pin_thread",
    "allow_unhide_thread",
    "can_unhide_thread",
    "allow_hide_thread",
    "can_hide_thread",
    "allow_delete_thread",
    "can_delete_thread",
    "allow_move_thread",
    "can_move_thread",
    "allow_merge_thread",
    "can_merge_thread",
    "allow_approve_thread",
    "can_approve_thread",
    "allow_see_post",
    "can_see_post",
    "allow_edit_post",
    "can_edit_post",
    "allow_unhide_post",
    "can_unhide_post",
    "allow_hide_post",
    "can_hide_post",
    "allow_delete_post",
    "can_delete_post",
    "allow_protect_post",
    "can_protect_post",
    "allow_approve_post",
    "can_approve_post",
    "allow_move_post",
    "can_move_post",
    "allow_merge_post",
    "can_merge_post",
    "allow_unhide_event",
    "can_unhide_event",
    "allow_split_post",
    "can_split_post",
    "allow_hide_event",
    "can_hide_event",
    "allow_delete_event",
    "can_delete_event",
    "exclude_invisible_threads",
    "exclude_invisible_posts",
]


class RolePermissionsForm(forms.Form):
    legend = _("Threads")

    can_see_unapproved_content_lists = YesNoSwitch(
        label=_("Can see unapproved content list"),
        help_text=_(
            'Allows access to "unapproved" tab on threads lists for '
            "easy listing of threads that are unapproved or contain "
            "unapproved posts. Despite the tab being available on all "
            "threads lists, it will only display threads belonging to "
            "categories in which the user has permission to approve "
            "content."
        ),
    )
    can_see_reported_content_lists = YesNoSwitch(
        label=_("Can see reported content list"),
        help_text=_(
            'Allows access to "reported" tab on threads lists for '
            "easy listing of threads that contain reported posts. "
            "Despite the tab being available on all categories "
            "threads lists, it will only display threads belonging to "
            "categories in which the user has permission to see posts "
            "reports."
        ),
    )
    can_omit_flood_protection = YesNoSwitch(
        label=_("Can omit flood protection"),
        help_text=_("Allows posting more frequently than flood protection would."),
    )


class CategoryPermissionsForm(forms.Form):
    legend = _("Threads")

    can_see_all_threads = forms.TypedChoiceField(
        label=_("Can see threads"),
        coerce=int,
        initial=0,
        choices=[(0, _("Started threads")), (1, _("All threads"))],
    )

    can_start_threads = YesNoSwitch(label=_("Can start threads"))
    can_reply_threads = YesNoSwitch(label=_("Can reply to threads"))

    can_edit_threads = forms.TypedChoiceField(
        label=_("Can edit threads"),
        coerce=int,
        initial=0,
        choices=[(0, _("No")), (1, _("Own threads")), (2, _("All threads"))],
    )
    can_hide_own_threads = forms.TypedChoiceField(
        label=_("Can hide own threads"),
        help_text=_(
            "Only threads started within time limit and "
            "with no replies can be hidden."
        ),
        coerce=int,
        initial=0,
        choices=[(0, _("No")), (1, _("Hide threads")), (2, _("Delete threads"))],
    )
    thread_edit_time = forms.IntegerField(
        label=_("Time limit for own threads edits, in minutes"),
        help_text=_("Enter 0 to don't limit time for editing own threads."),
        initial=0,
        min_value=0,
    )
    can_hide_threads = forms.TypedChoiceField(
        label=_("Can hide all threads"),
        coerce=int,
        initial=0,
        choices=[(0, _("No")), (1, _("Hide threads")), (2, _("Delete threads"))],
    )

    can_pin_threads = forms.TypedChoiceField(
        label=_("Can pin threads"),
        coerce=int,
        initial=0,
        choices=[(0, _("No")), (1, _("Locally")), (2, _("Globally"))],
    )
    can_close_threads = YesNoSwitch(label=_("Can close threads"))
    can_move_threads = YesNoSwitch(label=_("Can move threads"))
    can_merge_threads = YesNoSwitch(label=_("Can merge threads"))

    can_edit_posts = forms.TypedChoiceField(
        label=_("Can edit posts"),
        coerce=int,
        initial=0,
        choices=[(0, _("No")), (1, _("Own posts")), (2, _("All posts"))],
    )
    can_hide_own_posts = forms.TypedChoiceField(
        label=_("Can hide own posts"),
        help_text=_(
            "Only last posts to thread made within edit time limit can be hidden."
        ),
        coerce=int,
        initial=0,
        choices=[(0, _("No")), (1, _("Hide posts")), (2, _("Delete posts"))],
    )
    post_edit_time = forms.IntegerField(
        label=_("Time limit for own post edits, in minutes"),
        help_text=_("Enter 0 to don't limit time for editing own posts."),
        initial=0,
        min_value=0,
    )
    can_hide_posts = forms.TypedChoiceField(
        label=_("Can hide all posts"),
        coerce=int,
        initial=0,
        choices=[(0, _("No")), (1, _("Hide posts")), (2, _("Delete posts"))],
    )

    can_see_posts_likes = forms.TypedChoiceField(
        label=_("Can see posts likes"),
        coerce=int,
        initial=0,
        choices=[
            (0, _("No")),
            (1, _("Number only")),
            (2, _("Number and list of likers")),
        ],
    )
    can_like_posts = YesNoSwitch(
        label=_("Can like posts"),
        help_text=_("Only users with this permission to see likes can like posts."),
    )

    can_protect_posts = YesNoSwitch(
        label=_("Can protect posts"),
        help_text=_("Only users with this permission can edit protected posts."),
    )
    can_move_posts = YesNoSwitch(
        label=_("Can move posts"),
        help_text=_("Will be able to move posts to other threads."),
    )
    can_merge_posts = YesNoSwitch(label=_("Can merge posts"))
    can_approve_content = YesNoSwitch(
        label=_("Can approve content"),
        help_text=_("Will be able to see and approve unapproved content."),
    )
    can_report_content = YesNoSwitch(label=_("Can report posts"))
    can_see_reports = YesNoSwitch(label=_("Can see reports"))

    can_hide_events = forms.TypedChoiceField(
        label=_("Can hide events"),
        coerce=int,
        initial=0,
        choices=[(0, _("No")), (1, _("Hide events")), (2, _("Delete events"))],
    )

    require_threads_approval = YesNoSwitch(label=_("Require threads approval"))
    require_replies_approval = YesNoSwitch(label=_("Require replies approval"))
    require_edits_approval = YesNoSwitch(label=_("Require edits approval"))


def change_permissions_form(role):
    if isinstance(role, Role) and role.special_role != "anonymous":
        return RolePermissionsForm
    if isinstance(role, CategoryRole):
        return CategoryPermissionsForm


def build_acl(acl, roles, key_name):
    acl.update(
        {
            "can_see_unapproved_content_lists": False,
            "can_see_reported_content_lists": False,
            "can_omit_flood_protection": False,
            "can_approve_content": [],
            "can_see_reports": [],
        }
    )

    acl = algebra.sum_acls(
        acl,
        roles=roles,
        key=key_name,
        can_see_unapproved_content_lists=algebra.greater,
        can_see_reported_content_lists=algebra.greater,
        can_omit_flood_protection=algebra.greater,
    )

    categories_roles = get_categories_roles(roles)
    categories = list(Category.objects.all_categories(include_root=True))

    for category in categories:
        category_acl = acl["categories"].get(category.pk, {"can_browse": 0})
        if category_acl["can_browse"]:
            category_acl = acl["categories"][category.pk] = build_category_acl(
                category_acl, category, categories_roles, key_name
            )

            if category_acl.get("can_approve_content"):
                acl["can_approve_content"].append(category.pk)
            if category_acl.get("can_see_reports"):
                acl["can_see_reports"].append(category.pk)

    return acl


def build_category_acl(acl, category, categories_roles, key_name):
    category_roles = categories_roles.get(category.pk, [])

    final_acl = {
        "can_see_all_threads": 0,
        "can_start_threads": 0,
        "can_reply_threads": 0,
        "can_edit_threads": 0,
        "can_edit_posts": 0,
        "can_hide_own_threads": 0,
        "can_hide_own_posts": 0,
        "thread_edit_time": 0,
        "post_edit_time": 0,
        "can_hide_threads": 0,
        "can_hide_posts": 0,
        "can_protect_posts": 0,
        "can_move_posts": 0,
        "can_merge_posts": 0,
        "can_pin_threads": 0,
        "can_close_threads": 0,
        "can_move_threads": 0,
        "can_merge_threads": 0,
        "can_report_content": 0,
        "can_see_reports": 0,
        "can_see_posts_likes": 0,
        "can_like_posts": 0,
        "can_approve_content": 0,
        "require_threads_approval": 0,
        "require_replies_approval": 0,
        "require_edits_approval": 0,
        "can_hide_events": 0,
    }
    final_acl.update(acl)

    algebra.sum_acls(
        final_acl,
        roles=category_roles,
        key=key_name,
        can_see_all_threads=algebra.greater,
        can_start_threads=algebra.greater,
        can_reply_threads=algebra.greater,
        can_edit_threads=algebra.greater,
        can_edit_posts=algebra.greater,
        can_hide_threads=algebra.greater,
        can_hide_posts=algebra.greater,
        can_hide_own_threads=algebra.greater,
        can_hide_own_posts=algebra.greater,
        thread_edit_time=algebra.greater_or_zero,
        post_edit_time=algebra.greater_or_zero,
        can_protect_posts=algebra.greater,
        can_move_posts=algebra.greater,
        can_merge_posts=algebra.greater,
        can_pin_threads=algebra.greater,
        can_close_threads=algebra.greater,
        can_move_threads=algebra.greater,
        can_merge_threads=algebra.greater,
        can_report_content=algebra.greater,
        can_see_reports=algebra.greater,
        can_see_posts_likes=algebra.greater,
        can_like_posts=algebra.greater,
        can_approve_content=algebra.greater,
        require_threads_approval=algebra.greater,
        require_replies_approval=algebra.greater,
        require_edits_approval=algebra.greater,
        can_hide_events=algebra.greater,
    )

    return final_acl


def add_acl_to_category(user_acl, category):
    category_acl = user_acl["categories"].get(category.pk, {})

    category.acl.update(
        {
            "can_see_all_threads": 0,
            "can_see_own_threads": 0,
            "can_start_threads": 0,
            "can_reply_threads": 0,
            "can_edit_threads": 0,
            "can_edit_posts": 0,
            "can_hide_own_threads": 0,
            "can_hide_own_posts": 0,
            "thread_edit_time": 0,
            "post_edit_time": 0,
            "can_hide_threads": 0,
            "can_hide_posts": 0,
            "can_protect_posts": 0,
            "can_move_posts": 0,
            "can_merge_posts": 0,
            "can_pin_threads": 0,
            "can_close_threads": 0,
            "can_move_threads": 0,
            "can_merge_threads": 0,
            "can_report_content": 0,
            "can_see_reports": 0,
            "can_see_posts_likes": 0,
            "can_like_posts": 0,
            "can_approve_content": 0,
            "require_threads_approval": category.require_threads_approval,
            "require_replies_approval": category.require_replies_approval,
            "require_edits_approval": category.require_edits_approval,
            "can_hide_events": 0,
        }
    )

    algebra.sum_acls(
        category.acl,
        acls=[category_acl],
        can_see_all_threads=algebra.greater,
        can_see_posts_likes=algebra.greater,
    )

    if user_acl["is_authenticated"]:
        algebra.sum_acls(
            category.acl,
            acls=[category_acl],
            can_start_threads=algebra.greater,
            can_reply_threads=algebra.greater,
            can_edit_threads=algebra.greater,
            can_edit_posts=algebra.greater,
            can_hide_threads=algebra.greater,
            can_hide_posts=algebra.greater,
            can_hide_own_threads=algebra.greater,
            can_hide_own_posts=algebra.greater,
            thread_edit_time=algebra.greater_or_zero,
            post_edit_time=algebra.greater_or_zero,
            can_protect_posts=algebra.greater,
            can_move_posts=algebra.greater,
            can_merge_posts=algebra.greater,
            can_pin_threads=algebra.greater,
            can_close_threads=algebra.greater,
            can_move_threads=algebra.greater,
            can_merge_threads=algebra.greater,
            can_report_content=algebra.greater,
            can_see_reports=algebra.greater,
            can_like_posts=algebra.greater,
            can_approve_content=algebra.greater,
            require_threads_approval=algebra.greater,
            require_replies_approval=algebra.greater,
            require_edits_approval=algebra.greater,
            can_hide_events=algebra.greater,
        )

    if user_acl["can_approve_content"]:
        category.acl.update(
            {
                "require_threads_approval": 0,
                "require_replies_approval": 0,
                "require_edits_approval": 0,
            }
        )

    category.acl["can_see_own_threads"] = not category.acl["can_see_all_threads"]


def add_acl_to_thread(user_acl, thread):
    category_acl = user_acl["categories"].get(thread.category_id, {})

    thread.acl.update(
        {
            "can_reply": can_reply_thread(user_acl, thread),
            "can_edit": can_edit_thread(user_acl, thread),
            "can_pin": can_pin_thread(user_acl, thread),
            "can_pin_globally": False,
            "can_hide": can_hide_thread(user_acl, thread),
            "can_unhide": can_unhide_thread(user_acl, thread),
            "can_delete": can_delete_thread(user_acl, thread),
            "can_close": category_acl.get("can_close_threads", False),
            "can_move": can_move_thread(user_acl, thread),
            "can_merge": can_merge_thread(user_acl, thread),
            "can_move_posts": category_acl.get("can_move_posts", False),
            "can_merge_posts": category_acl.get("can_merge_posts", False),
            "can_approve": can_approve_thread(user_acl, thread),
            "can_see_reports": category_acl.get("can_see_reports", False),
        }
    )

    if thread.acl["can_pin"] and category_acl.get("can_pin_threads") == 2:
        thread.acl["can_pin_globally"] = True


def add_acl_to_post(user_acl, post):
    if post.is_event:
        add_acl_to_event(user_acl, post)
    else:
        add_acl_to_reply(user_acl, post)


def add_acl_to_event(user_acl, event):
    can_hide_events = 0

    if user_acl["is_authenticated"]:
        category_acl = user_acl["categories"].get(
            event.category_id, {"can_hide_events": 0}
        )

        can_hide_events = category_acl["can_hide_events"]

    event.acl.update(
        {
            "can_see_hidden": can_hide_events > 0,
            "can_hide": can_hide_event(user_acl, event),
            "can_delete": can_delete_event(user_acl, event),
        }
    )


def add_acl_to_reply(user_acl, post):
    category_acl = user_acl["categories"].get(post.category_id, {})

    post.acl.update(
        {
            "can_reply": can_reply_thread(user_acl, post.thread),
            "can_edit": can_edit_post(user_acl, post),
            "can_see_hidden": post.is_first_post or category_acl.get("can_hide_posts"),
            "can_unhide": can_unhide_post(user_acl, post),
            "can_hide": can_hide_post(user_acl, post),
            "can_delete": can_delete_post(user_acl, post),
            "can_protect": can_protect_post(user_acl, post),
            "can_approve": can_approve_post(user_acl, post),
            "can_move": can_move_post(user_acl, post),
            "can_merge": can_merge_post(user_acl, post),
            "can_report": category_acl.get("can_report_content", False),
            "can_see_reports": category_acl.get("can_see_reports", False),
            "can_see_likes": category_acl.get("can_see_posts_likes", 0),
            "can_like": False,
        }
    )

    if not post.acl["can_see_hidden"]:
        post.acl["can_see_hidden"] = post.id == post.thread.first_post_id
    if user_acl["is_authenticated"] and post.acl["can_see_likes"]:
        post.acl["can_like"] = category_acl.get("can_like_posts", False)


def register_with(registry):
    registry.acl_annotator(Category, add_acl_to_category)
    registry.acl_annotator(Thread, add_acl_to_thread)
    registry.acl_annotator(Post, add_acl_to_post)


def allow_see_thread(user_acl, target):
    category_acl = user_acl["categories"].get(
        target.category_id, {"can_see": False, "can_browse": False}
    )

    if not (category_acl["can_see"] and category_acl["can_browse"]):
        raise Http404()

    if target.is_hidden and (
        user_acl["is_anonymous"] or not category_acl["can_hide_threads"]
    ):
        raise Http404()

    if user_acl["is_anonymous"] or user_acl["user_id"] != target.starter_id:
        if not category_acl["can_see_all_threads"]:
            raise Http404()

        if target.is_unapproved and not category_acl["can_approve_content"]:
            raise Http404()


can_see_thread = return_boolean(allow_see_thread)


def allow_start_thread(user_acl, target):
    if user_acl["is_anonymous"]:
        raise PermissionDenied(_("You have to sign in to start threads."))

    category_acl = user_acl["categories"].get(target.pk, {"can_start_threads": False})

    if not category_acl["can_start_threads"]:
        raise PermissionDenied(
            _("You don't have permission to start new threads in this category.")
        )

    if target.is_closed and not category_acl["can_close_threads"]:
        raise PermissionDenied(
            _("This category is closed. You can't start new threads in it.")
        )


can_start_thread = return_boolean(allow_start_thread)


def allow_reply_thread(user_acl, target):
    if user_acl["is_anonymous"]:
        raise PermissionDenied(_("You have to sign in to reply threads."))

    category_acl = user_acl["categories"].get(
        target.category_id, {"can_reply_threads": False}
    )

    if not category_acl["can_reply_threads"]:
        raise PermissionDenied(_("You can't reply to threads in this category."))

    if not category_acl["can_close_threads"]:
        if target.category.is_closed:
            raise PermissionDenied(
                _("This category is closed. You can't reply to threads in it.")
            )
        if target.is_closed:
            raise PermissionDenied(
                _("You can't reply to closed threads in this category.")
            )


can_reply_thread = return_boolean(allow_reply_thread)


def allow_edit_thread(user_acl, target):
    if user_acl["is_anonymous"]:
        raise PermissionDenied(_("You have to sign in to edit threads."))

    category_acl = user_acl["categories"].get(
        target.category_id, {"can_edit_threads": False}
    )

    if not category_acl["can_edit_threads"]:
        raise PermissionDenied(_("You can't edit threads in this category."))

    if category_acl["can_edit_threads"] == 1:
        if user_acl["user_id"] != target.starter_id:
            raise PermissionDenied(
                _("You can't edit other users threads in this category.")
            )

        if not has_time_to_edit_thread(user_acl, target):
            message = ngettext(
                "You can't edit threads that are older than %(minutes)s minute.",
                "You can't edit threads that are older than %(minutes)s minutes.",
                category_acl["thread_edit_time"],
            )
            raise PermissionDenied(
                message % {"minutes": category_acl["thread_edit_time"]}
            )

    if not category_acl["can_close_threads"]:
        if target.category.is_closed:
            raise PermissionDenied(
                _("This category is closed. You can't edit threads in it.")
            )
        if target.is_closed:
            raise PermissionDenied(_("This thread is closed. You can't edit it."))


can_edit_thread = return_boolean(allow_edit_thread)


def allow_pin_thread(user_acl, target):
    if user_acl["is_anonymous"]:
        raise PermissionDenied(_("You have to sign in to change threads weights."))

    category_acl = user_acl["categories"].get(
        target.category_id, {"can_pin_threads": 0}
    )

    if not category_acl["can_pin_threads"]:
        raise PermissionDenied(_("You can't change threads weights in this category."))

    if not category_acl["can_close_threads"]:
        if target.category.is_closed:
            raise PermissionDenied(
                _("This category is closed. You can't change threads weights in it.")
            )
        if target.is_closed:
            raise PermissionDenied(
                _("This thread is closed. You can't change its weight.")
            )


can_pin_thread = return_boolean(allow_pin_thread)


def allow_unhide_thread(user_acl, target):
    if user_acl["is_anonymous"]:
        raise PermissionDenied(_("You have to sign in to hide threads."))

    category_acl = user_acl["categories"].get(
        target.category_id, {"can_close_threads": False}
    )

    if not category_acl["can_close_threads"]:
        if target.category.is_closed:
            raise PermissionDenied(
                _("This category is closed. You can't reveal threads in it.")
            )
        if target.is_closed:
            raise PermissionDenied(_("This thread is closed. You can't reveal it."))


can_unhide_thread = return_boolean(allow_unhide_thread)


def allow_hide_thread(user_acl, target):
    if user_acl["is_anonymous"]:
        raise PermissionDenied(_("You have to sign in to hide threads."))

    category_acl = user_acl["categories"].get(
        target.category_id, {"can_hide_threads": 0, "can_hide_own_threads": 0}
    )

    if (
        not category_acl["can_hide_threads"]
        and not category_acl["can_hide_own_threads"]
    ):
        raise PermissionDenied(_("You can't hide threads in this category."))

    if not category_acl["can_hide_threads"] and category_acl["can_hide_own_threads"]:
        if user_acl["user_id"] != target.starter_id:
            raise PermissionDenied(
                _("You can't hide other users theads in this category.")
            )

        if not has_time_to_edit_thread(user_acl, target):
            message = ngettext(
                "You can't hide threads that are older than %(minutes)s minute.",
                "You can't hide threads that are older than %(minutes)s minutes.",
                category_acl["thread_edit_time"],
            )
            raise PermissionDenied(
                message % {"minutes": category_acl["thread_edit_time"]}
            )

    if not category_acl["can_close_threads"]:
        if target.category.is_closed:
            raise PermissionDenied(
                _("This category is closed. You can't hide threads in it.")
            )
        if target.is_closed:
            raise PermissionDenied(_("This thread is closed. You can't hide it."))


can_hide_thread = return_boolean(allow_hide_thread)


def allow_delete_thread(user_acl, target):
    if user_acl["is_anonymous"]:
        raise PermissionDenied(_("You have to sign in to delete threads."))

    category_acl = user_acl["categories"].get(
        target.category_id, {"can_hide_threads": 0, "can_hide_own_threads": 0}
    )

    if (
        category_acl["can_hide_threads"] != 2
        and category_acl["can_hide_own_threads"] != 2
    ):
        raise PermissionDenied(_("You can't delete threads in this category."))

    if (
        category_acl["can_hide_threads"] != 2
        and category_acl["can_hide_own_threads"] == 2
    ):
        if user_acl["user_id"] != target.starter_id:
            raise PermissionDenied(
                _("You can't delete other users theads in this category.")
            )

        if not has_time_to_edit_thread(user_acl, target):
            message = ngettext(
                "You can't delete threads that are older than %(minutes)s minute.",
                "You can't delete threads that are older than %(minutes)s minutes.",
                category_acl["thread_edit_time"],
            )
            raise PermissionDenied(
                message % {"minutes": category_acl["thread_edit_time"]}
            )

    if not category_acl["can_close_threads"]:
        if target.category.is_closed:
            raise PermissionDenied(
                _("This category is closed. You can't delete threads in it.")
            )
        if target.is_closed:
            raise PermissionDenied(_("This thread is closed. You can't delete it."))


can_delete_thread = return_boolean(allow_delete_thread)


def allow_move_thread(user_acl, target):
    if user_acl["is_anonymous"]:
        raise PermissionDenied(_("You have to sign in to move threads."))

    category_acl = user_acl["categories"].get(
        target.category_id, {"can_move_threads": 0}
    )

    if not category_acl["can_move_threads"]:
        raise PermissionDenied(_("You can't move threads in this category."))

    if not category_acl["can_close_threads"]:
        if target.category.is_closed:
            raise PermissionDenied(
                _("This category is closed. You can't move it's threads.")
            )
        if target.is_closed:
            raise PermissionDenied(_("This thread is closed. You can't move it."))


can_move_thread = return_boolean(allow_move_thread)


def allow_merge_thread(user_acl, target, otherthread=False):
    if user_acl["is_anonymous"]:
        raise PermissionDenied(_("You have to sign in to merge threads."))

    category_acl = user_acl["categories"].get(
        target.category_id, {"can_merge_threads": 0}
    )

    if not category_acl["can_merge_threads"]:
        if otherthread:
            raise PermissionDenied(_("Other thread can't be merged with."))
        raise PermissionDenied(_("You can't merge threads in this category."))

    if not category_acl["can_close_threads"]:
        if target.category.is_closed:
            if otherthread:
                raise PermissionDenied(
                    _("Other thread's category is closed. You can't merge with it.")
                )
            raise PermissionDenied(
                _("This category is closed. You can't merge it's threads.")
            )
        if target.is_closed:
            if otherthread:
                raise PermissionDenied(
                    _("Other thread is closed and can't be merged with.")
                )
            raise PermissionDenied(
                _("This thread is closed. You can't merge it with other threads.")
            )


can_merge_thread = return_boolean(allow_merge_thread)


def allow_approve_thread(user_acl, target):
    if user_acl["is_anonymous"]:
        raise PermissionDenied(_("You have to sign in to approve threads."))

    category_acl = user_acl["categories"].get(
        target.category_id, {"can_approve_content": 0}
    )

    if not category_acl["can_approve_content"]:
        raise PermissionDenied(_("You can't approve threads in this category."))

    if not category_acl["can_close_threads"]:
        if target.category.is_closed:
            raise PermissionDenied(
                _("This category is closed. You can't approve threads in it.")
            )
        if target.is_closed:
            raise PermissionDenied(_("This thread is closed. You can't approve it."))


can_approve_thread = return_boolean(allow_approve_thread)


def allow_see_post(user_acl, target):
    category_acl = user_acl["categories"].get(
        target.category_id, {"can_approve_content": False, "can_hide_events": False}
    )

    if not target.is_event and target.is_unapproved:
        if user_acl["is_anonymous"]:
            raise Http404()

        if (
            not category_acl["can_approve_content"]
            and user_acl["user_id"] != target.poster_id
        ):
            raise Http404()

    if target.is_event and target.is_hidden and not category_acl["can_hide_events"]:
        raise Http404()


can_see_post = return_boolean(allow_see_post)


def allow_edit_post(user_acl, target):
    if user_acl["is_anonymous"]:
        raise PermissionDenied(_("You have to sign in to edit posts."))

    if target.is_event:
        raise PermissionDenied(_("Events can't be edited."))

    category_acl = user_acl["categories"].get(
        target.category_id, {"can_edit_posts": False}
    )

    if not category_acl["can_edit_posts"]:
        raise PermissionDenied(_("You can't edit posts in this category."))

    if (
        target.is_hidden
        and not target.is_first_post
        and not category_acl["can_hide_posts"]
    ):
        raise PermissionDenied(_("This post is hidden, you can't edit it."))

    if category_acl["can_edit_posts"] == 1:
        if target.poster_id != user_acl["user_id"]:
            raise PermissionDenied(
                _("You can't edit other users posts in this category.")
            )

        if target.is_protected and not category_acl["can_protect_posts"]:
            raise PermissionDenied(_("This post is protected. You can't edit it."))

        if not has_time_to_edit_post(user_acl, target):
            message = ngettext(
                "You can't edit posts that are older than %(minutes)s minute.",
                "You can't edit posts that are older than %(minutes)s minutes.",
                category_acl["post_edit_time"],
            )
            raise PermissionDenied(
                message % {"minutes": category_acl["post_edit_time"]}
            )

    if not category_acl["can_close_threads"]:
        if target.category.is_closed:
            raise PermissionDenied(
                _("This category is closed. You can't edit posts in it.")
            )
        if target.thread.is_closed:
            raise PermissionDenied(
                _("This thread is closed. You can't edit posts in it.")
            )


can_edit_post = return_boolean(allow_edit_post)


def allow_unhide_post(user_acl, target):
    if user_acl["is_anonymous"]:
        raise PermissionDenied(_("You have to sign in to reveal posts."))

    category_acl = user_acl["categories"].get(
        target.category_id, {"can_hide_posts": 0, "can_hide_own_posts": 0}
    )

    if not category_acl["can_hide_posts"]:
        if not category_acl["can_hide_own_posts"]:
            raise PermissionDenied(_("You can't reveal posts in this category."))

        if user_acl["user_id"] != target.poster_id:
            raise PermissionDenied(
                _("You can't reveal other users posts in this category.")
            )

        if target.is_protected and not category_acl["can_protect_posts"]:
            raise PermissionDenied(_("This post is protected. You can't reveal it."))

        if not has_time_to_edit_post(user_acl, target):
            message = ngettext(
                "You can't reveal posts that are older than %(minutes)s minute.",
                "You can't reveal posts that are older than %(minutes)s minutes.",
                category_acl["post_edit_time"],
            )
            raise PermissionDenied(
                message % {"minutes": category_acl["post_edit_time"]}
            )

    if target.is_first_post:
        raise PermissionDenied(_("You can't reveal thread's first post."))

    if not category_acl["can_close_threads"]:
        if target.category.is_closed:
            raise PermissionDenied(
                _("This category is closed. You can't reveal posts in it.")
            )
        if target.thread.is_closed:
            raise PermissionDenied(
                _("This thread is closed. You can't reveal posts in it.")
            )


can_unhide_post = return_boolean(allow_unhide_post)


def allow_hide_post(user_acl, target):
    if user_acl["is_anonymous"]:
        raise PermissionDenied(_("You have to sign in to hide posts."))

    category_acl = user_acl["categories"].get(
        target.category_id, {"can_hide_posts": 0, "can_hide_own_posts": 0}
    )

    if not category_acl["can_hide_posts"]:
        if not category_acl["can_hide_own_posts"]:
            raise PermissionDenied(_("You can't hide posts in this category."))

        if user_acl["user_id"] != target.poster_id:
            raise PermissionDenied(
                _("You can't hide other users posts in this category.")
            )

        if target.is_protected and not category_acl["can_protect_posts"]:
            raise PermissionDenied(_("This post is protected. You can't hide it."))

        if not has_time_to_edit_post(user_acl, target):
            message = ngettext(
                "You can't hide posts that are older than %(minutes)s minute.",
                "You can't hide posts that are older than %(minutes)s minutes.",
                category_acl["post_edit_time"],
            )
            raise PermissionDenied(
                message % {"minutes": category_acl["post_edit_time"]}
            )

    if target.is_first_post:
        raise PermissionDenied(_("You can't hide thread's first post."))

    if not category_acl["can_close_threads"]:
        if target.category.is_closed:
            raise PermissionDenied(
                _("This category is closed. You can't hide posts in it.")
            )
        if target.thread.is_closed:
            raise PermissionDenied(
                _("This thread is closed. You can't hide posts in it.")
            )


can_hide_post = return_boolean(allow_hide_post)


def allow_delete_post(user_acl, target):
    if user_acl["is_anonymous"]:
        raise PermissionDenied(_("You have to sign in to delete posts."))

    category_acl = user_acl["categories"].get(
        target.category_id, {"can_hide_posts": 0, "can_hide_own_posts": 0}
    )

    if category_acl["can_hide_posts"] != 2:
        if category_acl["can_hide_own_posts"] != 2:
            raise PermissionDenied(_("You can't delete posts in this category."))

        if user_acl["user_id"] != target.poster_id:
            raise PermissionDenied(
                _("You can't delete other users posts in this category.")
            )

        if target.is_protected and not category_acl["can_protect_posts"]:
            raise PermissionDenied(_("This post is protected. You can't delete it."))

        if not has_time_to_edit_post(user_acl, target):
            message = ngettext(
                "You can't delete posts that are older than %(minutes)s minute.",
                "You can't delete posts that are older than %(minutes)s minutes.",
                category_acl["post_edit_time"],
            )
            raise PermissionDenied(
                message % {"minutes": category_acl["post_edit_time"]}
            )

    if target.is_first_post:
        raise PermissionDenied(_("You can't delete thread's first post."))

    if not category_acl["can_close_threads"]:
        if target.category.is_closed:
            raise PermissionDenied(
                _("This category is closed. You can't delete posts in it.")
            )
        if target.thread.is_closed:
            raise PermissionDenied(
                _("This thread is closed. You can't delete posts in it.")
            )


can_delete_post = return_boolean(allow_delete_post)


def allow_protect_post(user_acl, target):
    if user_acl["is_anonymous"]:
        raise PermissionDenied(_("You have to sign in to protect posts."))

    category_acl = user_acl["categories"].get(
        target.category_id, {"can_protect_posts": False}
    )

    if not category_acl["can_protect_posts"]:
        raise PermissionDenied(_("You can't protect posts in this category."))
    if not can_edit_post(user_acl, target):
        raise PermissionDenied(_("You can't protect posts you can't edit."))


can_protect_post = return_boolean(allow_protect_post)


def allow_approve_post(user_acl, target):
    if user_acl["is_anonymous"]:
        raise PermissionDenied(_("You have to sign in to approve posts."))

    category_acl = user_acl["categories"].get(
        target.category_id, {"can_approve_content": False}
    )

    if not category_acl["can_approve_content"]:
        raise PermissionDenied(_("You can't approve posts in this category."))
    if target.is_first_post:
        raise PermissionDenied(_("You can't approve thread's first post."))
    if (
        not target.is_first_post
        and not category_acl["can_hide_posts"]
        and target.is_hidden
    ):
        raise PermissionDenied(_("You can't approve posts the content you can't see."))

    if not category_acl["can_close_threads"]:
        if target.category.is_closed:
            raise PermissionDenied(
                _("This category is closed. You can't approve posts in it.")
            )
        if target.thread.is_closed:
            raise PermissionDenied(
                _("This thread is closed. You can't approve posts in it.")
            )


can_approve_post = return_boolean(allow_approve_post)


def allow_move_post(user_acl, target):
    if user_acl["is_anonymous"]:
        raise PermissionDenied(_("You have to sign in to move posts."))

    category_acl = user_acl["categories"].get(
        target.category_id, {"can_move_posts": False}
    )

    if not category_acl["can_move_posts"]:
        raise PermissionDenied(_("You can't move posts in this category."))
    if target.is_event:
        raise PermissionDenied(_("Events can't be moved."))
    if target.is_first_post:
        raise PermissionDenied(_("You can't move thread's first post."))
    if not category_acl["can_hide_posts"] and target.is_hidden:
        raise PermissionDenied(_("You can't move posts the content you can't see."))

    if not category_acl["can_close_threads"]:
        if target.category.is_closed:
            raise PermissionDenied(
                _("This category is closed. You can't move posts in it.")
            )
        if target.thread.is_closed:
            raise PermissionDenied(
                _("This thread is closed. You can't move posts in it.")
            )


can_move_post = return_boolean(allow_move_post)


def allow_merge_post(user_acl, target):
    if user_acl["is_anonymous"]:
        raise PermissionDenied(_("You have to sign in to merge posts."))

    category_acl = user_acl["categories"].get(
        target.category_id, {"can_merge_posts": False}
    )

    if not category_acl["can_merge_posts"]:
        raise PermissionDenied(_("You can't merge posts in this category."))
    if target.is_event:
        raise PermissionDenied(_("Events can't be merged."))
    if (
        target.is_hidden
        and not category_acl["can_hide_posts"]
        and not target.is_first_post
    ):
        raise PermissionDenied(_("You can't merge posts the content you can't see."))

    if not category_acl["can_close_threads"]:
        if target.category.is_closed:
            raise PermissionDenied(
                _("This category is closed. You can't merge posts in it.")
            )
        if target.thread.is_closed:
            raise PermissionDenied(
                _("This thread is closed. You can't merge posts in it.")
            )


can_merge_post = return_boolean(allow_merge_post)


def allow_split_post(user_acl, target):
    if user_acl["is_anonymous"]:
        raise PermissionDenied(_("You have to sign in to split posts."))

    category_acl = user_acl["categories"].get(
        target.category_id, {"can_move_posts": False}
    )

    if not category_acl["can_move_posts"]:
        raise PermissionDenied(_("You can't split posts in this category."))
    if target.is_event:
        raise PermissionDenied(_("Events can't be split."))
    if target.is_first_post:
        raise PermissionDenied(_("You can't split thread's first post."))
    if not category_acl["can_hide_posts"] and target.is_hidden:
        raise PermissionDenied(_("You can't split posts the content you can't see."))

    if not category_acl["can_close_threads"]:
        if target.category.is_closed:
            raise PermissionDenied(
                _("This category is closed. You can't split posts in it.")
            )
        if target.thread.is_closed:
            raise PermissionDenied(
                _("This thread is closed. You can't split posts in it.")
            )


can_split_post = return_boolean(allow_split_post)


def allow_unhide_event(user_acl, target):
    if user_acl["is_anonymous"]:
        raise PermissionDenied(_("You have to sign in to reveal events."))

    category_acl = user_acl["categories"].get(
        target.category_id, {"can_hide_events": 0}
    )

    if not category_acl["can_hide_events"]:
        raise PermissionDenied(_("You can't reveal events in this category."))

    if not category_acl["can_close_threads"]:
        if target.category.is_closed:
            raise PermissionDenied(
                _("This category is closed. You can't reveal events in it.")
            )
        if target.thread.is_closed:
            raise PermissionDenied(
                _("This thread is closed. You can't reveal events in it.")
            )


can_unhide_event = return_boolean(allow_unhide_event)


def allow_hide_event(user_acl, target):
    if user_acl["is_anonymous"]:
        raise PermissionDenied(_("You have to sign in to hide events."))

    category_acl = user_acl["categories"].get(
        target.category_id, {"can_hide_events": 0}
    )

    if not category_acl["can_hide_events"]:
        raise PermissionDenied(_("You can't hide events in this category."))

    if not category_acl["can_close_threads"]:
        if target.category.is_closed:
            raise PermissionDenied(
                _("This category is closed. You can't hide events in it.")
            )
        if target.thread.is_closed:
            raise PermissionDenied(
                _("This thread is closed. You can't hide events in it.")
            )


can_hide_event = return_boolean(allow_hide_event)


def allow_delete_event(user_acl, target):
    if user_acl["is_anonymous"]:
        raise PermissionDenied(_("You have to sign in to delete events."))

    category_acl = user_acl["categories"].get(
        target.category_id, {"can_hide_events": 0}
    )

    if category_acl["can_hide_events"] != 2:
        raise PermissionDenied(_("You can't delete events in this category."))

    if not category_acl["can_close_threads"]:
        if target.category.is_closed:
            raise PermissionDenied(
                _("This category is closed. You can't delete events in it.")
            )
        if target.thread.is_closed:
            raise PermissionDenied(
                _("This thread is closed. You can't delete events in it.")
            )


can_delete_event = return_boolean(allow_delete_event)


def can_change_owned_thread(user_acl, target):
    if user_acl["is_anonymous"] or user_acl["user_id"] != target.starter_id:
        return False

    if target.category.is_closed or target.is_closed:
        return False

    return has_time_to_edit_thread(user_acl, target)


def has_time_to_edit_thread(user_acl, target):
    edit_time = (
        user_acl["categories"].get(target.category_id, {}).get("thread_edit_time", 0)
    )
    if edit_time:
        diff = timezone.now() - target.started_on
        diff_minutes = int(diff.total_seconds() / 60)
        return diff_minutes < edit_time

    return True


def has_time_to_edit_post(user_acl, target):
    edit_time = (
        user_acl["categories"].get(target.category_id, {}).get("post_edit_time", 0)
    )
    if edit_time:
        diff = timezone.now() - target.posted_on
        diff_minutes = int(diff.total_seconds() / 60)
        return diff_minutes < edit_time

    return True


def exclude_invisible_threads(
    user_acl, categories, queryset
):  # pylint: disable=too-many-branches
    show_all = []
    show_accepted_visible = []
    show_accepted = []
    show_visible = []
    show_owned = []
    show_owned_visible = []

    for category in categories:
        add_acl_to_obj(user_acl, category)

        if not (category.acl["can_see"] and category.acl["can_browse"]):
            continue

        can_hide = category.acl["can_hide_threads"]
        if category.acl["can_see_all_threads"]:
            can_mod = category.acl["can_approve_content"]

            if can_mod and can_hide:
                show_all.append(category)
            elif user_acl["is_authenticated"]:
                if not can_mod and not can_hide:
                    show_accepted_visible.append(category)
                elif not can_mod:
                    show_accepted.append(category)
                elif not can_hide:
                    show_visible.append(category)
            else:
                show_accepted_visible.append(category)
        elif user_acl["is_authenticated"]:
            if can_hide:
                show_owned.append(category)
            else:
                show_owned_visible.append(category)

    conditions = None
    if show_all:
        conditions = Q(category__in=show_all)

    if show_accepted_visible:
        if user_acl["is_authenticated"]:
            condition = Q(
                Q(starter_id=user_acl["user_id"]) | Q(is_unapproved=False),
                category__in=show_accepted_visible,
                is_hidden=False,
            )
        else:
            condition = Q(
                category__in=show_accepted_visible, is_hidden=False, is_unapproved=False
            )

        if conditions:
            conditions = conditions | condition
        else:
            conditions = condition

    if show_accepted:
        condition = Q(
            Q(starter_id=user_acl["user_id"]) | Q(is_unapproved=False),
            category__in=show_accepted,
        )

        if conditions:
            conditions = conditions | condition
        else:
            conditions = condition

    if show_visible:
        condition = Q(category__in=show_visible, is_hidden=False)

        if conditions:
            conditions = conditions | condition
        else:
            conditions = condition

    if show_owned:
        condition = Q(category__in=show_owned, starter_id=user_acl["user_id"])

        if conditions:
            conditions = conditions | condition
        else:
            conditions = condition

    if show_owned_visible:
        condition = Q(
            category__in=show_owned_visible,
            starter_id=user_acl["user_id"],
            is_hidden=False,
        )

        if conditions:
            conditions = conditions | condition
        else:
            conditions = condition

    if not conditions:
        return Thread.objects.none()

    return queryset.filter(conditions)


def exclude_invisible_posts(user_acl, categories, queryset):
    if hasattr(categories, "__iter__"):
        return exclude_invisible_posts_in_categories(user_acl, categories, queryset)
    return exclude_invisible_posts_in_category(user_acl, categories, queryset)


def exclude_invisible_posts_in_categories(
    user_acl, categories, queryset
):  # pylint: disable=too-many-branches
    show_all = []
    show_approved = []
    show_approved_owned = []

    hide_invisible_events = []

    for category in categories:
        add_acl_to_obj(user_acl, category)

        if category.acl["can_approve_content"]:
            show_all.append(category.pk)
        else:
            if user_acl["is_authenticated"]:
                show_approved_owned.append(category.pk)
            else:
                show_approved.append(category.pk)

        if not category.acl["can_hide_events"]:
            hide_invisible_events.append(category.pk)

    conditions = None
    if show_all:
        conditions = Q(category__in=show_all)

    if show_approved:
        condition = Q(category__in=show_approved, is_unapproved=False)

        if conditions:
            conditions = conditions | condition
        else:
            conditions = condition

    if show_approved_owned:
        condition = Q(
            Q(poster_id=user_acl["user_id"]) | Q(is_unapproved=False),
            category__in=show_approved_owned,
        )

        if conditions:
            conditions = conditions | condition
        else:
            conditions = condition

    if hide_invisible_events:
        queryset = queryset.exclude(
            category__in=hide_invisible_events, is_event=True, is_hidden=True
        )

    if not conditions:
        return Post.objects.none()

    return queryset.filter(conditions)


def exclude_invisible_posts_in_category(user_acl, category, queryset):
    add_acl_to_obj(user_acl, category)

    if not category.acl["can_approve_content"]:
        if user_acl["is_authenticated"]:
            queryset = queryset.filter(
                Q(is_unapproved=False) | Q(poster_id=user_acl["user_id"])
            )
        else:
            queryset = queryset.exclude(is_unapproved=True)

    if not category.acl["can_hide_events"]:
        queryset = queryset.exclude(is_event=True, is_hidden=True)

    return queryset
