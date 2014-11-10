from django.contrib import messages
from django.db.transaction import atomic
from django.utils.translation import ungettext, ugettext_lazy, ugettext as _

from misago.threads import moderation
from misago.threads.views.generic.actions import ActionsBase


__all__ = ['PostsActions']


def atomic_post_action(f):
    def decorator(self, request, posts):
        with atomic():
            self.forum.lock()
            self.thread.lock()

            for post in posts:
                post.thread = self.thread

            response = f(self, request, posts)

            self.thread.synchronize()
            self.thread.save()
            self.forum.synchronize()
            self.forum.save()

            return response
    return decorator


class PostsActions(ActionsBase):
    select_items_message = ugettext_lazy(
        "You have to select at least one post.")
    is_mass_action = True

    def get_available_actions(self, kwargs):
        self.thread = kwargs['thread']
        self.forum = self.thread.forum

        actions = []

        if self.forum.acl['can_hide_posts']:
            actions.append({
                'action': 'unhide',
                'icon': 'eye',
                'name': _("Unhide posts")
            })
            actions.append({
                'action': 'hide',
                'icon': 'eye-slash',
                'name': _("Hide posts")
            })
        if self.forum.acl['can_hide_posts'] == 2:
            actions.append({
                'action': 'delete',
                'icon': 'times',
                'name': _("Delete posts"),
                'confirmation': _("Are you sure you want to delete selected "
                                  "posts? This action can't be undone.")
            })

        return actions

    @atomic_post_action
    def action_unhide(self, request, posts):
        changed_posts = 0
        for post in posts:
            if moderation.unhide_post(request.user, post):
                changed_posts += 1

        if changed_posts:
            message = ungettext(
                '%(changed)d post was made visible.',
                '%(changed)d posts were made visible.',
            changed_posts)
            messages.success(request, message % {'changed': changed_posts})
        else:
            message = _("No posts were made visible.")
            messages.info(request, message)

    @atomic_post_action
    def action_hide(self, request, posts):
        changed_posts = 0
        for post in posts:
            if moderation.hide_post(request.user, post):
                changed_posts += 1

        if changed_posts:
            message = ungettext(
                '%(changed)d post was hidden.',
                '%(changed)d posts were hidden.',
            changed_posts)
            messages.success(request, message % {'changed': changed_posts})
        else:
            message = _("No posts were hidden.")
            messages.info(request, message)
        pass

    @atomic_post_action
    def action_delete(self, request, posts):
        changed_posts = 0
        first_deleted = None

        for post in posts:
            if moderation.delete_post(request.user, post):
                changed_posts += 1
                if not first_deleted:
                    first_deleted = post

        if changed_posts:
            message = ungettext(
                '%(changed)d post was deleted.',
                '%(changed)d posts were deleted.',
            changed_posts)
            messages.success(request, message % {'changed': changed_posts})


        else:
            message = _("No posts were deleted.")
            messages.info(request, message)
