from django.contrib import messages
from django.db.transaction import atomic
from django.http import Http404
from django.shortcuts import redirect
from django.utils.translation import ungettext, ugettext_lazy, ugettext as _

from misago.threads import moderation
from misago.threads.paginator import Paginator
from misago.threads.views.generic.actions import ActionsBase, ReloadAfterDelete


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

    def redirect_after_deletion(self, request, queryset):
        paginator = Paginator(queryset, 10, 3)
        current_page = int(request.resolver_match.kwargs.get('page', 0))

        if paginator.num_pages < current_page:
            namespace = request.resolver_match.namespace
            url_name = request.resolver_match.url_name
            kwars = request.resolver_match.kwargs
            kwars['page'] = paginator.num_pages
            if kwars['page'] == 1:
                del kwars['page']
            return redirect('%s:%s' % (namespace, url_name), **kwars)
        else:
            return redirect(request.path)

    def get_available_actions(self, kwargs):
        self.thread = kwargs['thread']
        self.forum = self.thread.forum

        actions = []

        if self.forum.acl['can_hide_posts']:
            actions.append({
                'action': 'unhide',
                'icon': 'eye',
                'name': _("Reveal posts")
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
            return ReloadAfterDelete()
        else:
            message = _("No posts were deleted.")
            messages.info(request, message)
