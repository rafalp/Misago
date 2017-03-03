from django import forms
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.http import Http404
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext

from misago.acl import add_acl, algebra
from misago.acl.decorators import return_boolean
from misago.acl.models import Role
from misago.categories.models import Category, CategoryRole
from misago.categories.permissions import get_categories_roles
from misago.core.forms import YesNoSwitch
from misago.threads.models import Post, Thread


__all__ = [
    'allow_see_thread',
    'can_see_thread',
    'allow_start_thread',
    'can_start_thread',
    'allow_reply_thread',
    'can_reply_thread',
    'allow_edit_thread',
    'can_edit_thread',
    'allow_see_post',
    'can_see_post',
    'allow_edit_post',
    'can_edit_post',
    'allow_unhide_post',
    'can_unhide_post',
    'allow_hide_post',
    'can_hide_post',
    'allow_delete_post',
    'can_delete_post',
    'allow_protect_post',
    'can_protect_post',
    'allow_approve_post',
    'can_approve_post',
    'allow_move_post',
    'can_move_post',
    'allow_delete_event',
    'can_delete_event',
    'exclude_invisible_threads',
    'exclude_invisible_posts',
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
        choices=[
            (0, _("Started threads")),
            (1, _("All threads")),
        ],
    )

    can_start_threads = YesNoSwitch(label=_("Can start threads"))
    can_reply_threads = YesNoSwitch(label=_("Can reply to threads"))

    can_edit_threads = forms.TypedChoiceField(
        label=_("Can edit threads"),
        coerce=int,
        initial=0,
        choices=[
            (0, _("No")),
            (1, _("Own threads")),
            (2, _("All threads")),
        ],
    )
    can_hide_own_threads = forms.TypedChoiceField(
        label=_("Can hide own threads"),
        help_text=_(
            "Only threads started within time limit and "
            "with no replies can be hidden."
        ),
        coerce=int,
        initial=0,
        choices=[
            (0, _("No")),
            (1, _("Hide threads")),
            (2, _("Delete threads")),
        ],
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
        choices=[
            (0, _("No")),
            (1, _("Hide threads")),
            (2, _("Delete threads")),
        ],
    )

    can_pin_threads = forms.TypedChoiceField(
        label=_("Can pin threads"),
        coerce=int,
        initial=0,
        choices=[
            (0, _("No")),
            (1, _("Locally")),
            (2, _("Globally")),
        ],
    )
    can_close_threads = YesNoSwitch(label=_("Can close threads"))
    can_move_threads = YesNoSwitch(label=_("Can move threads"))
    can_merge_threads = YesNoSwitch(label=_("Can merge threads"))

    can_edit_posts = forms.TypedChoiceField(
        label=_("Can edit posts"),
        coerce=int,
        initial=0,
        choices=[
            (0, _("No")),
            (1, _("Own posts")),
            (2, _("All posts")),
        ],
    )
    can_hide_own_posts = forms.TypedChoiceField(
        label=_("Can hide own posts"),
        help_text=_("Only last posts to thread made within edit time limit can be hidden."),
        coerce=int,
        initial=0,
        choices=[
            (0, _("No")),
            (1, _("Hide posts")),
            (2, _("Delete posts")),
        ],
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
        choices=[
            (0, _("No")),
            (1, _("Hide posts")),
            (2, _("Delete posts")),
        ],
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
        label=_("Can move posts"), help_text=_("Will be able to move posts to other threads.")
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
        choices=[
            (0, _("No")),
            (1, _("Hide events")),
            (2, _("Delete events")),
        ],
    )

    require_threads_approval = YesNoSwitch(label=_("Require threads approval"))
    require_replies_approval = YesNoSwitch(label=_("Require replies approval"))
    require_edits_approval = YesNoSwitch(label=_("Require edits approval"))


def change_permissions_form(role):
    if isinstance(role, Role) and role.special_role != 'anonymous':
        return RolePermissionsForm
    elif isinstance(role, CategoryRole):
        return CategoryPermissionsForm
    else:
        return None


def build_acl(acl, roles, key_name):
    acl.update({
        'can_see_unapproved_content_lists': False,
        'can_see_reported_content_lists': False,
        'can_omit_flood_protection': False,
        'can_approve_content': [],
        'can_see_reports': [],
    })

    acl = algebra.sum_acls(
        acl,
        roles=roles,
        key=key_name,
        can_see_unapproved_content_lists=algebra.greater,
        can_see_reported_content_lists=algebra.greater,
        can_omit_flood_protection=algebra.greater
    )

    categories_roles = get_categories_roles(roles)
    categories = list(Category.objects.all_categories(include_root=True))

    for category in categories:
        category_acl = acl['categories'].get(category.pk, {'can_browse': 0})
        if category_acl['can_browse']:
            category_acl = acl['categories'][category.pk] = build_category_acl(
                category_acl, category, categories_roles, key_name
            )

            if category_acl.get('can_approve_content'):
                acl['can_approve_content'].append(category.pk)
            if category_acl.get('can_see_reports'):
                acl['can_see_reports'].append(category.pk)

    return acl


def build_category_acl(acl, category, categories_roles, key_name):
    category_roles = categories_roles.get(category.pk, [])

    final_acl = {
        'can_see_all_threads': 0,
        'can_start_threads': 0,
        'can_reply_threads': 0,
        'can_edit_threads': 0,
        'can_edit_posts': 0,
        'can_hide_own_threads': 0,
        'can_hide_own_posts': 0,
        'thread_edit_time': 0,
        'post_edit_time': 0,
        'can_hide_threads': 0,
        'can_hide_posts': 0,
        'can_protect_posts': 0,
        'can_move_posts': 0,
        'can_merge_posts': 0,
        'can_pin_threads': 0,
        'can_close_threads': 0,
        'can_move_threads': 0,
        'can_merge_threads': 0,
        'can_report_content': 0,
        'can_see_reports': 0,
        'can_see_posts_likes': 0,
        'can_like_posts': 0,
        'can_approve_content': 0,
        'require_threads_approval': 0,
        'require_replies_approval': 0,
        'require_edits_approval': 0,
        'can_hide_events': 0,
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


def add_acl_to_category(user, category):
    category_acl = user.acl_cache['categories'].get(category.pk, {})

    category.acl.update({
        'can_see_all_threads': 0,
        'can_see_own_threads': 0,
        'can_start_threads': 0,
        'can_reply_threads': 0,
        'can_edit_threads': 0,
        'can_edit_posts': 0,
        'can_hide_own_threads': 0,
        'can_hide_own_posts': 0,
        'thread_edit_time': 0,
        'post_edit_time': 0,
        'can_hide_threads': 0,
        'can_hide_posts': 0,
        'can_protect_posts': 0,
        'can_move_posts': 0,
        'can_merge_posts': 0,
        'can_pin_threads': 0,
        'can_close_threads': 0,
        'can_move_threads': 0,
        'can_merge_threads': 0,
        'can_report_content': 0,
        'can_see_reports': 0,
        'can_see_posts_likes': 0,
        'can_like_posts': 0,
        'can_approve_content': 0,
        'require_threads_approval': category.require_threads_approval,
        'require_replies_approval': category.require_replies_approval,
        'require_edits_approval': category.require_edits_approval,
        'can_hide_events': 0,
    })

    algebra.sum_acls(
        category.acl,
        acls=[category_acl],
        can_see_all_threads=algebra.greater,
        can_see_posts_likes=algebra.greater,
    )

    if user.is_authenticated:
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

    if user.acl_cache['can_approve_content']:
        category.acl.update({
            'require_threads_approval': 0,
            'require_replies_approval': 0,
            'require_edits_approval': 0,
        })

    category.acl['can_see_own_threads'] = not category.acl['can_see_all_threads']


def add_acl_to_thread(user, thread):
    category_acl = user.acl_cache['categories'].get(thread.category_id, {})

    thread.acl.update({
        'can_reply': can_reply_thread(user, thread),
        'can_edit': can_edit_thread(user, thread),
        'can_hide': category_acl.get('can_hide_threads', False),
        'can_pin': 0,
        'can_close': category_acl.get('can_close_threads', False),
        'can_move': False,
        'can_merge': False,
        'can_move_posts': False,
        'can_merge_posts': False,
        'can_approve': category_acl.get('can_approve_content', False),
        'can_see_reports': category_acl.get('can_see_reports', False),
    })

    if not category_acl.get('can_close_threads'):
        thread_is_protected = thread.is_closed or thread.category.is_closed
    else:
        thread_is_protected = False

    if (can_change_owned_thread(user, thread) and not thread_is_protected
            and not thread.replies and not thread.acl['can_hide']):
        can_hide_thread = category_acl.get('can_hide_own_threads')
        thread.acl['can_hide'] = can_hide_thread

    if not thread_is_protected:
        thread.acl['can_pin'] = category_acl.get('can_pin_threads', 0)
        thread.acl['can_move'] = category_acl.get('can_move_threads', False)
        thread.acl['can_merge'] = category_acl.get('can_merge_threads', False)

        thread.acl['can_move_posts'] = category_acl.get('can_move_posts', False)
        thread.acl['can_merge_posts'] = category_acl.get('can_merge_posts', False)


def add_acl_to_post(user, post):
    if post.is_event:
        add_acl_to_event(user, post)
    else:
        add_acl_to_reply(user, post)


def add_acl_to_event(user, event):
    if user.is_authenticated:
        category_acl = user.acl_cache['categories'].get(event.category_id, {})
        can_hide_events = category_acl.get('can_hide_events', 0)
    else:
        can_hide_events = 0

    event.acl.update({
        'can_see_hidden': can_hide_events > 0,
        'can_hide': can_hide_events > 0,
        'can_delete': can_hide_events == 2,
    })


def add_acl_to_reply(user, post):
    category_acl = user.acl_cache['categories'].get(post.category_id, {})

    post.acl.update({
        'can_reply': can_reply_thread(user, post.thread),
        'can_edit': can_edit_post(user, post),
        'can_see_hidden': post.is_first_post or category_acl.get('can_hide_posts'),
        'can_unhide': can_unhide_post(user, post),
        'can_hide': can_hide_post(user, post),
        'can_delete': can_delete_post(user, post),
        'can_protect': can_protect_post(user, post),
        'can_approve': can_approve_post(user, post),
        'can_move': can_move_post(user, post),
        'can_report': category_acl.get('can_report_content', False),
        'can_see_reports': category_acl.get('can_see_reports', False),
        'can_see_likes': category_acl.get('can_see_posts_likes', 0),
        'can_like': False,
    })

    if not post.acl['can_see_hidden']:
        post.acl['can_see_hidden'] = post.id == post.thread.first_post_id
    if user.is_authenticated and post.acl['can_see_likes']:
        post.acl['can_like'] = category_acl.get('can_like_posts', False)


def register_with(registry):
    registry.acl_annotator(Category, add_acl_to_category)
    registry.acl_annotator(Thread, add_acl_to_thread)
    registry.acl_annotator(Post, add_acl_to_post)


def allow_see_thread(user, target):
    category_acl = user.acl_cache['categories'].get(
        target.category_id, {
            'can_see': False,
            'can_browse': False,
        }
    )

    if not (category_acl['can_see'] and category_acl['can_browse']):
        raise Http404()

    if target.is_hidden and (user.is_anonymous or not category_acl['can_hide_threads']):
        raise Http404()

    if user.is_anonymous or user.pk != target.starter_id:
        if not category_acl['can_see_all_threads']:
            raise Http404()

        if target.is_unapproved and not category_acl['can_approve_content']:
            raise Http404()


can_see_thread = return_boolean(allow_see_thread)


def allow_start_thread(user, target):
    if user.is_anonymous:
        raise PermissionDenied(_("You have to sign in to start threads."))

    category_acl = user.acl_cache['categories'].get(
        target.pk, {
            'can_close_threads': False,
            'can_start_threads': False,
        }
    )

    if target.is_closed and not category_acl['can_close_threads']:
        raise PermissionDenied(_("This category is closed. You can't start new threads in it."))

    if not category_acl['can_start_threads']:
        raise PermissionDenied(
            _("You don't have permission to start new threads in this category.")
        )


can_start_thread = return_boolean(allow_start_thread)


def allow_reply_thread(user, target):
    if user.is_anonymous:
        raise PermissionDenied(_("You have to sign in to reply threads."))

    category_acl = user.acl_cache['categories'].get(
        target.category_id, {
            'can_close_threads': False,
            'can_reply_threads': False,
        }
    )

    if not category_acl['can_close_threads']:
        if target.category.is_closed:
            raise PermissionDenied(_("This category is closed. You can't reply to threads in it."))
        if target.is_closed:
            raise PermissionDenied(_("You can't reply to closed threads in this category."))

    if not category_acl['can_reply_threads']:
        raise PermissionDenied(_("You can't reply to threads in this category."))


can_reply_thread = return_boolean(allow_reply_thread)


def allow_edit_thread(user, target):
    if user.is_anonymous:
        raise PermissionDenied(_("You have to sign in to edit threads."))

    category_acl = user.acl_cache['categories'].get(
        target.category_id, {'can_edit_threads': False}
    )

    if not category_acl['can_edit_threads']:
        raise PermissionDenied(_("You can't edit threads in this category."))

    if category_acl['can_edit_threads'] == 1:
        if target.starter_id != user.pk:
            raise PermissionDenied(_("You can't edit other users threads in this category."))

        if not category_acl['can_close_threads']:
            if target.category.is_closed:
                raise PermissionDenied(_("This category is closed. You can't edit threads in it."))
            if target.is_closed:
                raise PermissionDenied(_("You can't edit closed threads in this category."))

        if not has_time_to_edit_thread(user, target):
            message = ungettext(
                "You can't edit threads that are older than %(minutes)s minute.",
                "You can't edit threads that are older than %(minutes)s minutes.",
                category_acl['thread_edit_time']
            )
            raise PermissionDenied(message % {'minutes': category_acl['thread_edit_time']})


can_edit_thread = return_boolean(allow_edit_thread)


def allow_see_post(user, target):
    category_acl = user.acl_cache['categories'].get(
        target.category_id, {
            'can_approve_content': False,
            'can_hide_events': False,
        }
    )

    if not target.is_event and target.is_unapproved:
        if user.is_anonymous:
            raise Http404()

        if not category_acl['can_approve_content'] and user.id != target.poster_id:
            raise Http404()

    if target.is_event and target.is_hidden and not category_acl['can_hide_events']:
        raise Http404()


can_see_post = return_boolean(allow_see_post)


def allow_edit_post(user, target):
    if user.is_anonymous:
        raise PermissionDenied(_("You have to sign in to edit posts."))

    if target.is_event:
        raise PermissionDenied(_("Events can't be edited."))

    category_acl = user.acl_cache['categories'].get(target.category_id, {'can_edit_posts': False})

    if not category_acl['can_edit_posts']:
        raise PermissionDenied(_("You can't edit posts in this category."))

    if not category_acl['can_close_threads']:
        if target.category.is_closed:
            raise PermissionDenied(_("This category is closed. You can't edit posts in it."))
        if target.thread.is_closed:
            raise PermissionDenied(_("This thread is closed. You can't edit posts in it."))

    if target.is_hidden and not target.is_first_post and not category_acl['can_hide_posts']:
        raise PermissionDenied(_("This post is hidden, you can't edit it."))

    if category_acl['can_edit_posts'] == 1:
        if target.poster_id != user.pk:
            raise PermissionDenied(_("You can't edit other users posts in this category."))

        if target.is_protected and not category_acl['can_protect_posts']:
            raise PermissionDenied(_("This post is protected. You can't edit it."))

        if not has_time_to_edit_post(user, target):
            message = ungettext(
                "You can't edit posts that are older than %(minutes)s minute.",
                "You can't edit posts that are older than %(minutes)s minutes.",
                category_acl['post_edit_time'],
            )
            raise PermissionDenied(message % {'minutes': category_acl['post_edit_time']})


can_edit_post = return_boolean(allow_edit_post)


def allow_unhide_post(user, target):
    if user.is_anonymous:
        raise PermissionDenied(_("You have to sign in to reveal posts."))

    category_acl = user.acl_cache['categories'].get(
        target.category_id, {
            'can_hide_posts': 0,
            'can_hide_own_posts': 0,
        }
    )

    if not category_acl['can_hide_posts']:
        if not category_acl['can_hide_own_posts']:
            raise PermissionDenied(_("You can't reveal posts in this category."))

        if user.id != target.poster_id:
            raise PermissionDenied(_("You can't reveal other users posts in this category."))

        if not category_acl['can_close_threads']:
            if target.category.is_closed:
                raise PermissionDenied(_("This category is closed. You can't reveal posts in it."))
            if target.thread.is_closed:
                raise PermissionDenied(_("This thread is closed. You can't reveal posts in it."))

        if target.is_protected and not category_acl['can_protect_posts']:
            raise PermissionDenied(_("This post is protected. You can't reveal it."))

        if not has_time_to_edit_post(user, target):
            message = ungettext(
                "You can't reveal posts that are older than %(minutes)s minute.",
                "You can't reveal posts that are older than %(minutes)s minutes.",
                category_acl['post_edit_time'],
            )
            raise PermissionDenied(message % {'minutes': category_acl['post_edit_time']})

    if target.is_first_post:
        raise PermissionDenied(_("You can't reveal thread's first post."))


can_unhide_post = return_boolean(allow_unhide_post)


def allow_hide_post(user, target):
    if user.is_anonymous:
        raise PermissionDenied(_("You have to sign in to hide posts."))

    category_acl = user.acl_cache['categories'].get(
        target.category_id, {
            'can_hide_posts': 0,
            'can_hide_own_posts': 0,
        }
    )

    if not category_acl['can_hide_posts']:
        if not category_acl['can_hide_own_posts']:
            raise PermissionDenied(_("You can't hide posts in this category."))

        if user.id != target.poster_id:
            raise PermissionDenied(_("You can't hide other users posts in this category."))

        if not category_acl['can_close_threads']:
            if target.category.is_closed:
                raise PermissionDenied(_("This category is closed. You can't hide posts in it."))
            if target.thread.is_closed:
                raise PermissionDenied(_("This thread is closed. You can't hide posts in it."))

        if target.is_protected and not category_acl['can_protect_posts']:
            raise PermissionDenied(_("This post is protected. You can't hide it."))

        if not has_time_to_edit_post(user, target):
            message = ungettext(
                "You can't hide posts that are older than %(minutes)s minute.",
                "You can't hide posts that are older than %(minutes)s minutes.",
                category_acl['post_edit_time'],
            )
            raise PermissionDenied(message % {'minutes': category_acl['post_edit_time']})

    if target.is_first_post:
        raise PermissionDenied(_("You can't hide thread's first post."))


can_hide_post = return_boolean(allow_hide_post)


def allow_delete_post(user, target):
    if user.is_anonymous:
        raise PermissionDenied(_("You have to sign in to delete posts."))

    category_acl = user.acl_cache['categories'].get(
        target.category_id, {
            'can_hide_posts': 0,
            'can_hide_own_posts': 0,
        }
    )

    if category_acl['can_hide_posts'] != 2:
        if category_acl['can_hide_own_posts'] != 2:
            raise PermissionDenied(_("You can't delete posts in this category."))

        if user.id != target.poster_id:
            raise PermissionDenied(_("You can't delete other users posts in this category."))

        if not category_acl['can_close_threads']:
            if target.category.is_closed:
                raise PermissionDenied(_("This category is closed. You can't delete posts in it."))
            if target.thread.is_closed:
                raise PermissionDenied(_("This thread is closed. You can't delete posts in it."))

        if target.is_protected and not category_acl['can_protect_posts']:
            raise PermissionDenied(_("This post is protected. You can't delete it."))

        if not has_time_to_edit_post(user, target):
            message = ungettext(
                "You can't delete posts that are older than %(minutes)s minute.",
                "You can't delete posts that are older than %(minutes)s minutes.",
                category_acl['post_edit_time'],
            )
            raise PermissionDenied(message % {'minutes': category_acl['post_edit_time']})

    if target.is_first_post:
        raise PermissionDenied(_("You can't delete thread's first post."))


can_delete_post = return_boolean(allow_delete_post)


def allow_protect_post(user, target):
    if user.is_anonymous:
        raise PermissionDenied(_("You have to sign in to protect posts."))

    category_acl = user.acl_cache['categories'].get(
        target.category_id, {'can_protect_posts': False}
    )

    if not category_acl['can_protect_posts']:
        raise PermissionDenied(_("You can't protect posts in this category."))
    if not can_edit_post(user, target):
        raise PermissionDenied(_("You can't protect posts you can't edit."))


can_protect_post = return_boolean(allow_protect_post)


def allow_approve_post(user, target):
    if user.is_anonymous:
        raise PermissionDenied(_("You have to sign in to approve posts."))

    category_acl = user.acl_cache['categories'].get(
        target.category_id, {'can_approve_content': False}
    )

    if not category_acl['can_approve_content']:
        raise PermissionDenied(_("You can't approve posts in this category."))
    if target.is_first_post:
        raise PermissionDenied(_("You can't approve thread's first post."))
    if not target.is_first_post and not category_acl['can_hide_posts'] and target.is_hidden:
        raise PermissionDenied(_("You can't approve posts the content you can't see."))


can_approve_post = return_boolean(allow_approve_post)


def allow_move_post(user, target):
    if user.is_anonymous:
        raise PermissionDenied(_("You have to sign in to move posts."))

    category_acl = user.acl_cache['categories'].get(target.category_id, {'can_move_posts': False})

    if not category_acl['can_move_posts']:
        raise PermissionDenied(_("You can't move posts in this category."))
    if target.is_event:
        raise PermissionDenied(_("Events can't be moved."))
    if target.is_first_post:
        raise PermissionDenied(_("You can't move thread's first post."))
    if not category_acl['can_hide_posts'] and target.is_hidden:
        raise PermissionDenied(_("You can't move posts the content you can't see."))


can_move_post = return_boolean(allow_move_post)


def allow_delete_event(user, target):
    if user.is_anonymous:
        raise PermissionDenied(_("You have to sign in to delete events."))

    category_acl = user.acl_cache['categories'].get(target.category_id)

    if not category_acl or category_acl['can_hide_events'] != 2:
        raise PermissionDenied(_("You can't delete events in this category."))


can_delete_event = return_boolean(allow_delete_event)


def can_change_owned_thread(user, target):
    if user.is_anonymous or user.pk != target.starter_id:
        return False

    if target.category.is_closed or target.is_closed:
        return False

    return has_time_to_edit_thread(user, target)


def has_time_to_edit_thread(user, target):
    edit_time = user.acl_cache['categories'].get(target.category_id, {}).get('thread_edit_time', 0)
    if edit_time:
        diff = timezone.now() - target.started_on
        diff_minutes = int(diff.total_seconds() / 60)

        return diff_minutes < edit_time
    else:
        return True


def has_time_to_edit_post(user, target):
    edit_time = user.acl_cache['categories'].get(target.category_id, {}).get('post_edit_time', 0)
    if edit_time:
        diff = timezone.now() - target.posted_on
        diff_minutes = int(diff.total_seconds() / 60)

        return diff_minutes < edit_time
    else:
        return True


def exclude_invisible_threads(user, categories, queryset):
    show_all = []
    show_accepted_visible = []
    show_accepted = []
    show_visible = []
    show_owned = []
    show_owned_visible = []

    for category in categories:
        add_acl(user, category)

        if not (category.acl['can_see'] and category.acl['can_browse']):
            continue

        can_hide = category.acl['can_hide_threads']
        if category.acl['can_see_all_threads']:
            can_mod = category.acl['can_approve_content']

            if can_mod and can_hide:
                show_all.append(category)
            elif user.is_authenticated:
                if not can_mod and not can_hide:
                    show_accepted_visible.append(category)
                elif not can_mod:
                    show_accepted.append(category)
                elif not can_hide:
                    show_visible.append(category)
            else:
                show_accepted_visible.append(category)
        elif user.is_authenticated:
            if can_hide:
                show_owned.append(category)
            else:
                show_owned_visible.append(category)

    conditions = None
    if show_all:
        conditions = Q(category__in=show_all)

    if show_accepted_visible:
        if user.is_authenticated:
            condition = Q(
                Q(starter=user) | Q(is_unapproved=False),
                category__in=show_accepted_visible,
                is_hidden=False,
            )
        else:
            condition = Q(
                category__in=show_accepted_visible,
                is_hidden=False,
                is_unapproved=False,
            )

        if conditions:
            conditions = conditions | condition
        else:
            conditions = condition

    if show_accepted:
        condition = Q(
            Q(starter=user) | Q(is_unapproved=False),
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
        condition = Q(category__in=show_owned, starter=user)

        if conditions:
            conditions = conditions | condition
        else:
            conditions = condition

    if show_owned_visible:
        condition = Q(
            category__in=show_owned_visible,
            starter=user,
            is_hidden=False,
        )

        if conditions:
            conditions = conditions | condition
        else:
            conditions = condition

    if conditions:
        return queryset.filter(conditions)
    else:
        return Thread.objects.none()


def exclude_invisible_posts(user, category, queryset):
    if not category.acl['can_approve_content']:
        if user.is_authenticated:
            queryset = queryset.filter(Q(is_unapproved=False) | Q(poster=user))
        else:
            queryset = queryset.exclude(is_unapproved=True)

    if not category.acl['can_hide_events']:
        queryset = queryset.exclude(is_event=True, is_hidden=True)

    return queryset
