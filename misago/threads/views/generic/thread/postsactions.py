from django.contrib import messages
from django.db.transaction import atomic
from django.http import Http404
from django.shortcuts import redirect, render
from django.utils import timezone
from django.utils.translation import ungettext, ugettext_lazy, ugettext as _

from misago.categories.lists import get_category_path

from misago.threads import moderation
from misago.threads.forms.moderation import MovePostsForm, SplitThreadForm
from misago.threads.models import Thread
from misago.threads.paginator import Paginator
from misago.threads.views.generic.actions import ActionsBase, ReloadAfterDelete


__all__ = ['PostsActions']


def thread_aware_posts(f):
    def decorator(self, request, posts):
        for post in posts:
            post.thread = self.thread

        return f(self, request, posts)
    return decorator


def changes_thread_state(f):
    @thread_aware_posts
    def decorator(self, request, posts):
        with atomic():
            self.thread.lock()

            response = f(self, request, posts)

            self.thread.synchronize()
            self.thread.save()

            self.category.lock()
            self.category.synchronize()
            self.category.save()

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
        self.category = self.thread.category

        actions = []

        if self.thread.acl['can_review']:
            if self.thread.has_moderated_posts:
                actions.append({
                    'action': 'approve',
                    'icon': 'check',
                    'name': _("Approve posts")
                })

        if self.category.acl['can_merge_posts']:
            actions.append({
                'action': 'merge',
                'icon': 'compress',
                'name': _("Merge posts into one")
            })

        if self.category.acl['can_move_posts']:
            actions.append({
                'action': 'move',
                'icon': 'arrow-right',
                'name': _("Move posts to other thread")
            })

        if self.category.acl['can_split_threads']:
            actions.append({
                'action': 'split',
                'icon': 'code-fork',
                'name': _("Split posts to new thread")
            })

        if self.category.acl['can_protect_posts']:
            actions.append({
                'action': 'unprotect',
                'icon': 'unlock-alt',
                'name': _("Release posts")
            })
            actions.append({
                'action': 'protect',
                'icon': 'lock',
                'name': _("Protect posts")
            })

        if self.category.acl['can_hide_posts']:
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
        if self.category.acl['can_hide_posts'] == 2:
            actions.append({
                'action': 'delete',
                'icon': 'times',
                'name': _("Delete posts"),
                'confirmation': _("Are you sure you want to delete selected "
                                  "posts? This action can't be undone.")
            })

        return actions

    @changes_thread_state
    def action_approve(self, request, posts):
        changed_posts = 0
        for post in posts:
            if moderation.approve_post(request.user, post):
                changed_posts += 1

        if changed_posts:
            message = ungettext(
                '%(changed)d post was approved.',
                '%(changed)d posts were approved.',
            changed_posts)
            messages.success(request, message % {'changed': changed_posts})
        else:
            message = _("No posts were approved.")
            messages.info(request, message)

    @changes_thread_state
    def action_merge(self, request, posts):
        first_post = posts[0]

        changed_posts = len(posts)
        if changed_posts < 2:
            message = _("You have to select at least two posts to merge.")
            raise moderation.ModerationError(message)

        for post in posts:
            if not post.poster_id or first_post.poster_id != post.poster_id:
                message = _("You can't merge posts made by different authors.")
                raise moderation.ModerationError(message)

        for post in posts[1:]:
            post.merge(first_post)
            post.delete()

        first_post.save()

        message = ungettext(
            '%(changed)d post was merged.',
            '%(changed)d posts were merged.',
        changed_posts)
        messages.success(request, message % {'changed': changed_posts})

    move_posts_full_template = 'misago/thread/move_posts/full.html'
    move_posts_modal_template = 'misago/thread/move_posts/modal.html'

    @changes_thread_state
    def action_move(self, request, posts):
        if posts[0].id == self.thread.first_post_id:
            message = _("You can't move thread's first post.")
            raise moderation.ModerationError(message)

        form = MovePostsForm(user=request.user, thread=self.thread)

        if 'submit' in request.POST or 'follow' in request.POST:
            form = MovePostsForm(request.POST,
                                 user=request.user,
                                 thread=self.thread)
            if form.is_valid():
                for post in posts:
                    post.move(form.new_thread)
                    post.save()

                form.new_thread.lock()
                form.new_thread.synchronize()
                form.new_thread.save()

                if form.new_thread.category != self.category:
                    form.new_thread.category.lock()
                    form.new_thread.category.synchronize()
                    form.new_thread.category.save()

                changed_posts = len(posts)
                message = ungettext(
                    '%(changed)d post was moved to "%(thread)s".',
                    '%(changed)d posts were moved to "%(thread)s".',
                changed_posts)
                messages.success(request, message % {
                    'changed': changed_posts,
                    'thread': form.new_thread.title
                })

                if 'follow' in request.POST:
                    return redirect(form.new_thread.get_absolute_url())
                else:
                    return None # trigger thread refresh

        if request.is_ajax():
            template = self.move_posts_modal_template
        else:
            template = self.move_posts_full_template

        return render(request, template, {
            'form': form,
            'category': self.category,
            'thread': self.thread,
            'path': get_category_path(self.category),

            'posts': posts
        })

    split_thread_full_template = 'misago/thread/split/full.html'
    split_thread_modal_template = 'misago/thread/split/modal.html'

    @changes_thread_state
    def action_split(self, request, posts):
        if posts[0].id == self.thread.first_post_id:
            message = _("You can't split thread's first post.")
            raise moderation.ModerationError(message)

        form = SplitThreadForm(acl=request.user.acl)

        if 'submit' in request.POST or 'follow' in request.POST:
            form = SplitThreadForm(request.POST, acl=request.user.acl)
            if form.is_valid():
                split_thread = Thread()
                split_thread.category = form.cleaned_data['category']
                split_thread.set_title(
                    form.cleaned_data['thread_title'])
                split_thread.starter_name = "-"
                split_thread.starter_slug = "-"
                split_thread.last_poster_name = "-"
                split_thread.last_poster_slug = "-"
                split_thread.started_on = timezone.now()
                split_thread.last_post_on = timezone.now()
                split_thread.save()

                for post in posts:
                    post.move(split_thread)
                    post.save()

                split_thread.synchronize()
                split_thread.save()

                if split_thread.category != self.category:
                    split_thread.category.lock()
                    split_thread.category.synchronize()
                    split_thread.category.save()

                changed_posts = len(posts)
                message = ungettext(
                    '%(changed)d post was split to "%(thread)s".',
                    '%(changed)d posts were split to "%(thread)s".',
                changed_posts)
                messages.success(request, message % {
                    'changed': changed_posts,
                    'thread': split_thread.title
                })

                if 'follow' in request.POST:
                    return redirect(split_thread.get_absolute_url())
                else:
                    return None # trigger thread refresh

        if request.is_ajax():
            template = self.split_thread_modal_template
        else:
            template = self.split_thread_full_template

        return render(request, template, {
            'form': form,
            'category': self.category,
            'thread': self.thread,
            'path': get_category_path(self.category),

            'posts': posts
        })

    def action_unprotect(self, request, posts):
        changed_posts = 0
        for post in posts:
            if moderation.unprotect_post(request.user, post):
                changed_posts += 1

        if changed_posts:
            message = ungettext(
                '%(changed)d post was released from protection.',
                '%(changed)d posts were released from protection.',
            changed_posts)
            messages.success(request, message % {'changed': changed_posts})
        else:
            message = _("No posts were released from protection.")
            messages.info(request, message)

    def action_protect(self, request, posts):
        changed_posts = 0
        for post in posts:
            if moderation.protect_post(request.user, post):
                changed_posts += 1

        if changed_posts:
            message = ungettext(
                '%(changed)d post was made protected.',
                '%(changed)d posts were made protected.',
            changed_posts)
            messages.success(request, message % {'changed': changed_posts})
        else:
            message = _("No posts were made protected.")
            messages.info(request, message)

    @changes_thread_state
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

    @changes_thread_state
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

    @changes_thread_state
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
