from django.forms import ValidationError
from django.template import RequestContext
from django.utils import timezone
from django.utils.translation import ugettext as _
from misago import messages
from misago.messages import Message
from misago.models import Forum, Thread, Post
from misago.monitor import monitor, UpdatingMonitor
from misago.shortcuts import render_to_response
from misago.apps.threadtype.list.forms import MoveThreadsForm, MergeThreadsForm
from misago.utils.strings import slugify

class ThreadsListModeration(object):
    def action_accept(self, ids):
        if self._action_accept(ids):
            messages.success(self.request, _('Selected threads have been marked as reviewed and made visible to other members.'), 'threads')
        else:
            messages.info(self.request, _('No threads were marked as reviewed.'), 'threads')

    def _action_accept(self, ids):
        accepted = 0
        users = []
        for thread in self.threads:
            if thread.pk in ids and thread.moderated:
                accepted += 1
                # Sync thread and post
                thread.moderated = False
                thread.replies_moderated -= 1
                thread.save(force_update=True)
                thread.start_post.moderated = False
                thread.start_post.save(force_update=True)
                thread.set_checkpoint(self.request, 'accepted')
                thread.update_current_dates()
                # Sync user
                if thread.last_post.user:
                    thread.start_post.user.threads += 1
                    thread.start_post.user.posts += 1
                    users.append(thread.start_post.user)
        if accepted:
            with UpdatingMonitor() as cm:
                monitor.increase('threads', accepted)
                monitor.increase('posts', accepted)
            self.forum.sync()
            self.forum.save(force_update=True)
            for user in users:
                user.save(force_update=True)
        return accepted

    def action_annouce(self, ids):
        if self._action_annouce(ids):
            messages.success(self.request, _('Selected threads have been turned into announcements.'), 'threads')
        else:
            messages.info(self.request, _('No threads were turned into announcements.'), 'threads')

    def _action_annouce(self, ids):
        acl = self.request.acl.threads.get_role(self.forum)
        annouced = []
        for thread in self.threads:
            if thread.pk in ids and thread.weight < 2:
                annouced.append(thread.pk)
        if annouced:
            Thread.objects.filter(id__in=annouced).update(weight=2)
        return annouced

    def action_sticky(self, ids):
        if self._action_sticky(ids):
            messages.success(self.request, _('Selected threads have been sticked to the top of list.'), 'threads')
        else:
            messages.info(self.request, _('No threads were turned into stickies.'), 'threads')

    def _action_sticky(self, ids):
        acl = self.request.acl.threads.get_role(self.forum)
        sticky = []
        for thread in self.threads:
            if thread.pk in ids and thread.weight != 1 and (acl['can_pin_threads'] == 2 or thread.weight < 2):
                sticky.append(thread.pk)
        if sticky:
            Thread.objects.filter(id__in=sticky).update(weight=1)
        return sticky

    def action_normal(self, ids):
        if self._action_normal(ids):
            messages.success(self.request, _('Selected threads weight has been removed.'), 'threads')
        else:
            messages.info(self.request, _('No threads have had their weight removed.'), 'threads')

    def _action_normal(self, ids):
        normalised = []
        for thread in self.threads:
            if thread.pk in ids and thread.weight > 0:
                normalised.append(thread.pk)
        if normalised:
            Thread.objects.filter(id__in=normalised).update(weight=0)
        return normalised

    def action_move(self, ids):
        threads = []
        for thread in self.threads:
            if thread.pk in ids:
                threads.append(thread)
        if self.request.POST.get('origin') == 'move_form':
            form = MoveThreadsForm(self.request.POST, request=self.request, forum=self.forum)
            if form.is_valid():
                new_forum = form.cleaned_data['new_forum']
                for thread in threads:
                    thread.move_to(new_forum)
                    thread.save(force_update=True)
                    thread.set_checkpoint(self.request, 'moved', forum=self.forum)
                    thread.update_current_dates()
                new_forum.sync()
                new_forum.save(force_update=True)
                self.forum.sync()
                self.forum.save(force_update=True)
                messages.success(self.request, _('Selected threads have been moved to "%(forum)s".') % {'forum': new_forum.name}, 'threads')
                return None
            self.message = Message(form.non_field_errors()[0], messages.ERROR)
        else:
            form = MoveThreadsForm(request=self.request, forum=self.forum)
        return render_to_response('%ss/move_threads.html' % self.type_prefix,
                                  {
                                  'type_prefix': self.type_prefix,
                                  'search_in': self.search_in,
                                  'message': self.message,
                                  'forum': self.forum,
                                  'parents': self.parents,
                                  'threads': threads,
                                  'form': form,
                                  },
                                  context_instance=RequestContext(self.request));

    def action_merge(self, ids):
        if len(ids) < 2:
            raise ValidationError(_("You have to pick two or more threads to merge."))
        threads = []
        for thread in self.threads:
            if thread.pk in ids:
                threads.append(thread)
        if self.request.POST.get('origin') == 'merge_form':
            form = MergeThreadsForm(self.request.POST, request=self.request, threads=threads)
            if form.is_valid():
                new_thread = Thread.objects.create(
                                                   forum=form.cleaned_data['new_forum'],
                                                   name=form.cleaned_data['thread_name'],
                                                   slug=slugify(form.cleaned_data['thread_name']),
                                                   start=timezone.now(),
                                                   last=timezone.now()
                                                   )
                merged = []
                for thread in reversed(threads):
                    merged.append(thread.pk)
                    thread.merge_with(new_thread)

                new_thread.sync()
                new_thread.save(force_update=True)
                new_thread.update_current_dates()

                poll_action = form.cleaned_data.get('final_poll', 'no')
                if poll_action == 'no':
                    for thread in threads:
                        if thread.has_poll:
                            thread.poll.move_to(forum=new_thread.forum, thread=new_thread)
                            new_thread.has_poll = True
                            new_thread.save(force_update=True)
                            break
                else:
                    if poll_action > 0:
                        for thread in threads:
                            if thread.pk == poll_action:
                                thread.poll.move_to(forum=new_thread.forum, thread=new_thread)
                                new_thread.has_poll = True
                                new_thread.save(force_update=True)
                                break

                for thread in Thread.objects.filter(id__in=merged):
                    thread.delete()

                self.forum.sync()
                self.forum.save(force_update=True)
                if form.cleaned_data['new_forum'].pk != self.forum.pk:
                    form.cleaned_data['new_forum'].sync()
                    form.cleaned_data['new_forum'].save(force_update=True)
                messages.success(self.request, _('Selected threads have been merged into new one.'), 'threads')
                return None
            self.message = Message(form.non_field_errors()[0], messages.ERROR)
        else:
            form = MergeThreadsForm(request=self.request, threads=threads)

        warning = None
        lookback = threads[-1]
        for thread in reversed(threads[:-1]):
            if thread.start_post_id < lookback.last_post_id:
                warning = Message(_("Warning: Posting times in one or more of threads that you are going to merge are overlapping. This may result in disturbed flow of merged thread."), 'warning')
                break
            else:
                lookback = thread

        return render_to_response('%ss/merge.html' % self.type_prefix,
                                  {
                                  'type_prefix': self.type_prefix,
                                  'search_in': self.search_in,
                                  'message': self.message,
                                  'warning': warning,
                                  'forum': self.forum,
                                  'parents': self.parents,
                                  'threads': threads,
                                  'form': form,
                                  },
                                  context_instance=RequestContext(self.request));

    def action_open(self, ids):
        if self._action_open(ids):
            messages.success(self.request, _('Selected threads have been opened.'), 'threads')
        else:
            messages.info(self.request, _('No threads were opened.'), 'threads')

    def _action_open(self, ids):
        opened = []
        for thread in self.threads:
            if thread.pk in ids and thread.closed:
                opened.append(thread.pk)
                thread.set_checkpoint(self.request, 'opened')
        if opened:
            Thread.objects.filter(id__in=opened).update(closed=False)
        return opened

    def action_close(self, ids):
        if self._action_close(ids):
            messages.success(self.request, _('Selected threads have been closed.'), 'threads')
        else:
            messages.info(self.request, _('No threads were closed.'), 'threads')

    def _action_close(self, ids):
        closed = []
        for thread in self.threads:
            if thread.pk in ids and not thread.closed:
                closed.append(thread.pk)
                thread.set_checkpoint(self.request, 'closed')
        if closed:
            Thread.objects.filter(id__in=closed).update(closed=True)
        return closed

    def action_undelete(self, ids):
        if self._action_undelete(ids):
            messages.success(self.request, _('Selected threads have been restored.'), 'threads')
        else:
            messages.info(self.request, _('No threads were restored.'), 'threads')

    def _action_undelete(self, ids):
        undeleted = []
        for thread in self.threads:
            if thread.pk in ids and thread.deleted:
                undeleted.append(thread.pk)
                thread.start_post.deleted = False
                thread.start_post.save(force_update=True)
                thread.sync()
                thread.save(force_update=True)
                thread.set_checkpoint(self.request, 'undeleted')
                thread.update_current_dates()
        if undeleted:
            self.forum.sync()
            self.forum.save(force_update=True)
        return undeleted

    def action_soft(self, ids):
        if self._action_soft(ids):
            messages.success(self.request, _('Selected threads have been hidden.'), 'threads')
        else:
            messages.info(self.request, _('No threads were hidden.'), 'threads')

    def _action_soft(self, ids):
        deleted = []
        for thread in self.threads:
            if thread.pk in ids and not thread.deleted:
                deleted.append(thread.pk)
                thread.start_post.deleted = True
                thread.start_post.save(force_update=True)
                thread.sync()
                thread.save(force_update=True)
                thread.set_checkpoint(self.request, 'deleted')
                thread.update_current_dates()
        if deleted:
            self.forum.sync()
            self.forum.save(force_update=True)
        return deleted

    def action_hard(self, ids):
        if self._action_hard(ids):
            messages.success(self.request, _('Selected threads have been deleted.'), 'threads')
        else:
            messages.info(self.request, _('No threads were deleted.'), 'threads')

    def _action_hard(self, ids):
        deleted = []
        for thread in self.threads:
            if thread.pk in ids:
                deleted.append(thread.pk)
                thread.delete()
        if deleted:
            self.forum.sync()
            self.forum.save(force_update=True)
        return deleted
