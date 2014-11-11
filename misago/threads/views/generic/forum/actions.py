from django.contrib import messages
from django.db.transaction import atomic
from django.shortcuts import render
from django.utils import timezone
from django.utils.translation import ugettext_lazy, ugettext as _, ungettext

from misago.forums.lists import get_forum_path

from misago.threads import moderation
from misago.threads.forms.moderation import MergeThreadsForm, MoveThreadsForm
from misago.threads.models import Thread
from misago.threads.views.generic.threads import Actions, ReloadAfterDelete


__all__ = ['ForumActions', 'ReloadAfterDelete']


class ForumActions(Actions):
    def get_available_actions(self, kwargs):
        self.forum = kwargs['forum']

        actions = []

        if self.forum.acl['can_change_threads_labels'] == 2:
            for label in self.forum.labels:
                actions.append({
                    'action': 'label:%s' % label.slug,
                    'icon': 'tag',
                    'name': _('Label as "%(label)s"') % {'label': label.name}
                })

            if self.forum.labels:
                actions.append({
                    'action': 'unlabel',
                    'icon': 'times-circle',
                    'name': _("Remove labels")
                })

        if self.forum.acl['can_pin_threads']:
            actions.append({
                'action': 'pin',
                'icon': 'star',
                'name': _("Pin threads")
            })
            actions.append({
                'action': 'unpin',
                'icon': 'circle',
                'name': _("Unpin threads")
            })

        if self.forum.acl['can_review_moderated_content']:
            actions.append({
                'action': 'approve',
                'icon': 'check',
                'name': _("Approve threads")
            })

        if self.forum.acl['can_move_threads']:
            actions.append({
                'action': 'move',
                'icon': 'arrow-right',
                'name': _("Move threads")
            })

        if self.forum.acl['can_merge_threads']:
            actions.append({
                'action': 'merge',
                'icon': 'reply-all',
                'name': _("Merge threads")
            })

        if self.forum.acl['can_close_threads']:
            actions.append({
                'action': 'open',
                'icon': 'unlock-alt',
                'name': _("Open threads")
            })
            actions.append({
                'action': 'close',
                'icon': 'lock',
                'name': _("Close threads")
            })

        if self.forum.acl['can_hide_threads']:
            actions.append({
                'action': 'unhide',
                'icon': 'eye',
                'name': _("Reveal threads")
            })
            actions.append({
                'action': 'hide',
                'icon': 'eye-slash',
                'name': _("Hide threads")
            })
        if self.forum.acl['can_hide_threads'] == 2:
            actions.append({
                'action': 'delete',
                'icon': 'times',
                'name': _("Delete threads"),
                'confirmation': _("Are you sure you want to delete selected "
                                  "threads? This action can't be undone.")
            })

        return actions

    def action_label(self, request, threads, label_slug):
        for label in self.forum.labels:
            if label.slug == label_slug:
                break
        else:
            raise moderation.ModerationError(self.invalid_action_message)

        changed_threads = 0
        for thread in threads:
            if moderation.label_thread(request.user, thread, label):
                changed_threads += 1

        if changed_threads:
            message = ungettext(
                '%(changed)d thread was labeled "%(label)s".',
                '%(changed)d threads were labeled "%(label)s".',
            changed_threads)
            messages.success(request, message % {
                'changed': changed_threads,
                'label': label.name
            })
        else:
            message = _("No threads were labeled.")
            messages.info(request, message)

    def action_unlabel(self, request, threads):
        changed_threads = 0
        for thread in threads:
            if moderation.unlabel_thread(request.user, thread):
                changed_threads += 1

        if changed_threads:
            message = ungettext(
                '%(changed)d thread label was removed.',
                '%(changed)d threads labels were removed.',
            changed_threads)
            messages.success(request, message % {'changed': changed_threads})
        else:
            message = _("No threads were unlabeled.")
            messages.info(request, message)

    def action_pin(self, request, threads):
        changed_threads = 0
        for thread in threads:
            if moderation.pin_thread(request.user, thread):
                changed_threads += 1

        if changed_threads:
            message = ungettext(
                '%(changed)d thread was pinned.',
                '%(changed)d threads were pinned.',
            changed_threads)
            messages.success(request, message % {'changed': changed_threads})
        else:
            message = _("No threads were pinned.")
            messages.info(request, message)

    def action_unpin(self, request, threads):
        changed_threads = 0
        for thread in threads:
            if moderation.unpin_thread(request.user, thread):
                changed_threads += 1

        if changed_threads:
            message = ungettext(
                '%(changed)d thread was unpinned.',
                '%(changed)d threads were unpinned.',
            changed_threads)
            messages.success(request, message % {'changed': changed_threads})
        else:
            message = _("No threads were unpinned.")
            messages.info(request, message)

    move_threads_full_template = 'misago/threads/move/full.html'
    move_threads_modal_template = 'misago/threads/move/modal.html'

    def action_move(self, request, threads):
        form = MoveThreadsForm(acl=request.user.acl, forum=self.forum)

        if request.method == "POST" and 'submit' in request.POST:
            form = MoveThreadsForm(
                request.POST, acl=request.user.acl, forum=self.forum)
            if form.is_valid():
                new_forum = form.cleaned_data['new_forum']
                with atomic():
                    self.forum.lock()

                    for thread in threads:
                        moderation.move_thread(request.user, thread, new_forum)

                    self.forum.synchronize()
                    self.forum.save()
                    new_forum.synchronize()
                    new_forum.save()

                changed_threads = len(threads)
                message = ungettext(
                    '%(changed)d thread was moved to "%(forum)s".',
                    '%(changed)d threads were moved to "%(forum)s".',
                changed_threads)
                messages.success(request, message % {
                    'changed': changed_threads,
                    'forum': new_forum.name
                })

                return None # trigger threads list refresh

        if request.is_ajax():
            template = self.move_threads_modal_template
        else:
            template = self.move_threads_full_template

        return render(request, template, {
            'form': form,
            'forum': self.forum,
            'path': get_forum_path(self.forum),
            'threads': threads
        })

    merge_threads_full_template = 'misago/threads/merge/full.html'
    merge_threads_modal_template = 'misago/threads/merge/modal.html'

    def action_merge(self, request, threads):
        if len(threads) == 1:
            message = _("You have to select at least two threads to merge.")
            raise moderation.ModerationError(message)

        form = MergeThreadsForm()

        if request.method == "POST" and 'submit' in request.POST:
            form = MergeThreadsForm(request.POST)
            if form.is_valid():
                thread_title = form.cleaned_data['merged_thread_title']

                with atomic():
                    merged_thread = Thread()
                    merged_thread.forum = self.forum
                    merged_thread.set_title(
                        form.cleaned_data['merged_thread_title'])
                    merged_thread.starter_name = "-"
                    merged_thread.starter_slug = "-"
                    merged_thread.last_poster_name = "-"
                    merged_thread.last_poster_slug = "-"
                    merged_thread.started_on = timezone.now()
                    merged_thread.last_post_on = timezone.now()
                    merged_thread.is_pinned = max(t.is_pinned for t in threads)
                    merged_thread.is_closed = max(t.is_closed for t in threads)
                    merged_thread.save()

                    for thread in threads:
                        moderation.merge_thread(
                            request.user, merged_thread, thread)

                    merged_thread.synchronize()
                    merged_thread.save()

                with atomic():
                    self.forum.synchronize()
                    self.forum.save()

                changed_threads = len(threads)
                message = ungettext(
                    '%(changed)d thread was merged into "%(thread)s".',
                    '%(changed)d threads were merged into "%(thread)s".',
                changed_threads)
                messages.success(request, message % {
                    'changed': changed_threads,
                    'thread': merged_thread.title
                })

                return None # trigger threads list refresh

        if request.is_ajax():
            template = self.merge_threads_modal_template
        else:
            template = self.merge_threads_full_template

        return render(request, template, {
            'form': form,
            'forum': self.forum,
            'path': get_forum_path(self.forum),
            'threads': threads
        })

    def action_close(self, request, threads):
        changed_threads = 0
        for thread in threads:
            if moderation.close_thread(request.user, thread):
                changed_threads += 1

        if changed_threads:
            message = ungettext(
                '%(changed)d thread was closed.',
                '%(changed)d threads were closed.',
            changed_threads)
            messages.success(request, message % {'changed': changed_threads})
        else:
            message = _("No threads were closed.")
            messages.info(request, message)

    def action_open(self, request, threads):
        changed_threads = 0
        for thread in threads:
            if moderation.open_thread(request.user, thread):
                changed_threads += 1

        if changed_threads:
            message = ungettext(
                '%(changed)d thread was opened.',
                '%(changed)d threads were opened.',
            changed_threads)
            messages.success(request, message % {'changed': changed_threads})
        else:
            message = _("No threads were opened.")
            messages.info(request, message)

    def action_unhide(self, request, threads):
        changed_threads = 0
        for thread in threads:
            if moderation.unhide_thread(request.user, thread):
                changed_threads += 1

        if changed_threads:
            with atomic():
                self.forum.synchronize()
                self.forum.save()

            message = ungettext(
                '%(changed)d thread was made visible.',
                '%(changed)d threads were made visible.',
            changed_threads)
            messages.success(request, message % {'changed': changed_threads})
        else:
            message = _("No threads were made visible.")
            messages.info(request, message)

    def action_hide(self, request, threads):
        changed_threads = 0
        with atomic():
            self.forum.lock()
            for thread in threads:
                if moderation.hide_thread(request.user, thread):
                    changed_threads += 1

            if changed_threads:
                self.forum.synchronize()
                self.forum.save()

        if changed_threads:
            message = ungettext(
                '%(changed)d thread was hidden.',
                '%(changed)d threads were hidden.',
            changed_threads)
            messages.success(request, message % {'changed': changed_threads})
        else:
            message = _("No threads were hidden.")
            messages.info(request, message)

    def action_delete(self, request, threads):
        changed_threads = 0
        with atomic():
            self.forum.lock()
            for thread in threads:
                if moderation.delete_thread(request.user, thread):
                    changed_threads += 1

            if changed_threads:
                self.forum.synchronize()
                self.forum.save()

        if changed_threads:
            message = ungettext(
                '%(changed)d thread was deleted.',
                '%(changed)d threads were deleted.',
            changed_threads)
            messages.success(request, message % {'changed': changed_threads})

            return ReloadAfterDelete()
        else:
            message = _("No threads were deleted.")
            messages.info(request, message)
